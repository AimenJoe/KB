---
title: macroquad 3D 렌더링 — Camera3D·Mesh·배치·조명 없음·모델 로더 없음
type: reference
tags: [macroquad, rust, gamedev, 3d, rendering, camera]
status: verified
created: 2026-11-03
updated: 2026-11-04
verified: |
  1차 출처로 확인(2026-11-03, macroquad master 소스 — `src/models.rs`·`src/camera.rs`·`src/quad_gl.rs`·`src/window.rs`, Cargo 0.4.16과 같은 줄기):
  - `Vertex { position: Vec3, uv: Vec2, color: [u8; 4], normal: Vec4 }`, `Mesh { vertices: Vec<Vertex>, indices: Vec<u16>, texture: Option<Texture2D> }`.
  - `draw_mesh(&Mesh)`는 텍스처를 묶고 `gl.geometry(&vertices, &indices)`를 부를 뿐이다. 버퍼는 `BufferUsage::Stream`으로 **매 프레임 다시 올린다**
    (`draw()`가 드로콜마다 `buffer_update`, 끝에 배치 벡터를 비움). 한 `geometry()` 호출은 `max_vertices`·`max_indices`로 **조용히 잘린다**(`[0..min(cap, len)]`).
  - 새 드로콜이 갈리는 조건: 텍스처·클립·뷰포트·모델 행렬·파이프라인·렌더 패스·드로 모드가 바뀔 때, 배치가 넘칠 때, `pipeline()`·`set_uniform()`이 `break_batching`을 켤 때.
  - 기본 셰이더는 `gl_Position = Projection * Model * vec4(position, 1)`, `gl_FragColor = color * texture2D(Texture, uv)`. 정점 속성 `normal`은 **선언만 있고 쓰지 않는다**(Metal 정점 구조체엔 아예 없음).
  - `Camera3D` 기본값: `position (0,-10,0)`, `target 0`, `up (0,0,1)`(**z-up**), `fovy 45°(라디안)`, `Perspective`, `z_near 0.01`, `z_far 10000`, `aspect None`(매 프레임 화면 비율).
    `depth_enabled()`는 `Camera3D`가 `true`, `Camera2D`가 `false`. `Projection::Orthographics`는 `top = fovy/2, right = top*aspect`로 **fovy를 세로 폭(월드 단위)** 으로 쓴다(구조체 주석 "near plane width"와 다르다).
  - 모델 파일 로더(obj·gltf)는 없다. `models.rs`에는 `draw_cube/sphere/cylinder/plane/line_3d/grid`와 `Mesh`뿐.
  - 드로콜 용량: 숨은 헬퍼 `gl_set_drawcall_buffer_capacity(max_vertices, max_indices)`(window.rs), 또는 **macroquad `conf::Conf`의 `draw_call_vertex_capacity`·`draw_call_index_capacity`(기본 10,000 / 5,000, 0.4.16 `lib.rs` 1차)**. `#[macroquad::main]` 함수가 miniquad `Conf`를 돌려주면 `From`이 기본값으로 고정한다 — 바꾸려면 macroquad `Conf { miniquad_conf, draw_call_index_capacity, .. }`를 돌려준다(knellroot 0036: 둥근 모델 한 벌 인덱스 ≈ 7,800이 5,000에서 잘려 몸·다리가 사라졌다).
  - miniquad `Conf`: `high_dpi` 기본 false(Android는 true), `sample_count` 기본 1, `platform.webgl_version` 기본 **WebGL1**(conf.rs).
  렌더 타깃 깊이(2026-11-04, 0.4.16 `texture.rs` 소스 + knellroot 0033 헤드리스 스크린숏): `render_target(w, h)` = `RenderTargetParams::default()` = **`depth: false`**.
    `Camera3D`가 깊이 시험을 켜도 붙은 깊이 버퍼가 없으면 시험이 없는 것과 같아 **그린 순서로만 덮인다**(모델 부위 상자·벽이 엉킴) — `render_target_ex(.., RenderTargetParams { depth: true, .. })`로 고쳐 확인.
    파이프라인 컬링: macroquad 기본 파이프라인은 `cull_face` 기본값(Nothing), 커스텀 `load_material`의 `PipelineParams { cull_face, .. }`는 miniquad `set_cull_face`로 그대로 먹는다(소스). 렌더 타깃 + y-up Camera3D + glTF(반시계 앞면)에서 키운 상자의 앞면을 버리는 것은 `CullFace::Front`(스크린숏).
  2차 출처만 있음: 없음. 확인 못 함: 실제 기본 max_vertices/max_indices 값, `draw_mesh` 수백 개(적 20마리 × 부위 6)일 때의 프레임 비용(측정 전), WebGL1에서 깊이 버퍼 정밀도.
sources:
  - https://github.com/not-fl3/macroquad/blob/master/src/models.rs
  - https://github.com/not-fl3/macroquad/blob/master/src/camera.rs
  - https://github.com/not-fl3/macroquad/blob/master/src/quad_gl.rs
  - https://github.com/not-fl3/macroquad/blob/master/src/window.rs
  - https://github.com/not-fl3/miniquad/blob/master/src/conf.rs
  - https://docs.rs/macroquad/latest/macroquad/camera/struct.Camera3D.html
---

# macroquad 3D 렌더링

## 요약
macroquad의 3D는 **"카메라 행렬 + 즉시 모드 삼각형"** 까지다. `Camera3D`로 투영·깊이 테스트를 켜고 `Mesh`를 `draw_mesh`로 던지면 끝이고, 그 위(모델 로딩·스켈레탈 애니메이션·조명·그림자·카메라 충돌)는 전부 직접 쓴다. 2D에서 쓰던 렌더 타깃·정수 배율·커스텀 머티리얼 요령은 그대로 통한다. 레트로 로우폴리(마인크래프트보다 조금 정교한 수준)라면 이 범위로 충분하고, 그 이상(스키닝·PBR)을 바라면 엔진을 바꾸는 편이 싸다.

## 본문

### 카메라
| 항목 | 사실 |
|---|---|
| 좌표계 | 기본 `up = (0,0,1)` **z-up**. y-up으로 쓰려면 `up: vec3(0,1,0)`을 **매번** 적는다(기본값에 기대면 바닥이 벽이 된다) |
| 투영 | `Perspective`(fovy 라디안, `perspective_rh_gl`) / `Orthographics`(fovy = 세로 폭 월드 단위) |
| 행렬 | `matrix() = projection * look_at_rh(position, target, up)`. 화면→월드 광선은 `matrix().inverse()`로 직접 |
| 깊이 | `Camera3D`를 `set_camera`하면 깊이 테스트 켜짐. **그러나 렌더 타깃에 그릴 때는 타깃에 깊이 버퍼가 붙어 있어야 한다** — `render_target()`은 깊이 없음, `render_target_ex(.., depth: true)`. 2D HUD는 `set_default_camera()` 뒤에 |
| 렌더 타깃 | `render_target: Some(rt)` + `aspect: Some(w/h)`(안 적으면 화면 비율로 찌그러진다). 낮은 해상도(예 480×270)에 그려 `Nearest`로 키우면 PS1 느낌 |
| near/far | `z_near 0.01`·`z_far 10000` 기본 — WebGL1 깊이 24bit에서 z-fighting이 나면 near를 0.1~0.5로 올린다(확인 전) |

### 메시와 배치
- `Mesh`는 `Vec<Vertex>` + `Vec<u16>` 인덱스 + 텍스처 하나. 정점 65,536개 넘는 메시는 쪼갠다.
- **GPU에 머무는 메시는 없다.** 매 프레임 모든 정점이 다시 올라간다. 그래서 CPU에서 정점을 변형(부위별 회전, 스키닝)해 보내도 추가 비용이 거의 없다 — 모델 행렬을 바꾸는 것(`gl.push_model_matrix`)은 드로콜을 가르지만, 정점을 미리 월드 좌표로 바꿔 한 텍스처로 보내면 **한 드로콜**이다. 레트로 3D에서는 "아틀라스 텍스처 하나 + CPU 변형 + 한 배치"가 정석이다.
- 한 번의 `geometry()`가 용량을 넘으면 **에러 없이 잘린다**. 큰 지형 메시는 청크로 나누고, 용량은 `gl_set_drawcall_buffer_capacity`(숨김 함수)로 올릴 수 있다.
- 새 드로콜이 갈리는 조건(텍스처·모델 행렬·파이프라인·유니폼)을 알고 그리기 순서를 정하면 드로콜 수가 수십 → 몇 개가 된다.

### 조명·재질
- 기본 셰이더는 `color × texture`뿐. `normal`은 정점에 실려 가지만 **셰이더가 안 읽는다**. 램버트 한 줄이라도 `load_material`(커스텀 GLSL, WebGL1 = GLSL ES 1.0)로 쓴다. 2D에서 더하기 빛(`light_material`)을 쓰던 방식과 같다.
- 레트로풍이면 조명을 **정점 색**에 미리 구워(`Vertex.color`) 기본 셰이더로 끝낼 수도 있다 — 부위별 회전이 있으면 법선이 돌아가므로 CPU 변형 때 색을 다시 계산한다.
- 그림자는 없다. 바닥에 원판(2D에서 쓰던 `draw_circle`을 바닥 평면에) 또는 투영 메시를 직접.

### 모델·애니메이션
- 로더가 없다. 선택지: ① `gltf` 크레이트(1.4.x, 노드 트리·애니메이션 채널 읽기 지원)로 읽어 `Mesh`로 옮김, ② 자체 JSON(상자 목록 + 부위 트리). 스켈레탈 스키닝은 직접 써야 하므로, **부위가 강체로 도는 애니메이션**(마인크래프트식)이 이 스택과 맞는다 → [레트로 3D 모델 파이프라인](../assets/retro-3d-models-blockbench-gltf.md).

## 왜?
macroquad는 2D 즉시 모드 라이브러리에 3D 카메라를 얹은 것이다. 모든 그리기가 "정점 배열을 매 프레임 배치해 올리기"라서 상태를 가진 GPU 자원(VBO에 상주하는 메시, 본 행렬 유니폼 배열)이 없다. 그 단순함이 웹 번들 400KB와 빠른 컴파일의 대가다. 이 전제를 알고 설계하면(작은 메시, 아틀라스, CPU 변형) 3D도 무리 없이 돌고, 모르고 Unity식으로 짜면(메시마다 드로콜·머티리얼) 드로콜이 폭발한다.

## 함정
- **`render_target()`에는 깊이 버퍼가 없다.** 3D를 저해상도 타깃에 그리면 깊이 시험이 조용히 사라지고 그린 순서로만 덮인다 — 상자 모델이 "속이 비치거나 엉켜" 보이고 벽이 얇은 판처럼 겹친다. 오류도 경고도 없어서 화풍 문제로 착각하기 쉽다(knellroot는 첫 스테이지까지 모르고 왔다). 3D 타깃은 처음부터 `render_target_ex(.., depth: true)`.
- `Camera3D::default()`의 z-up. 2D 머리로 y-up을 가정하고 `position (0,10,-10)`을 주면 세상이 옆으로 눕는다.
- 렌더 타깃에 3D를 그릴 때 `aspect`를 빼먹으면 화면 비율로 찌그러진다.
- 정점이 잘리는 실패는 조용하다 — 큰 메시가 "일부만 그려지면" 용량부터 의심. **인덱스가 먼저 찬다**(기본 5,000 = 삼각형 1,666개) — 둥근(부드러운) 모델은 정점은 적어도 삼각형이 많다. 모델 한 벌이 용량 안에 드는지 시험으로 지킨다.
- `Orthographics`의 `fovy`는 각도가 아니라 세로 폭. 45(라디안 아님)를 주면 45 월드 단위가 세로로 보인다.
- 기본 WebGL1: `#version 300 es` 셰이더 문법·정수 텍스처·MRT 없음. 레트로엔 상관없지만 커스텀 GLSL은 ES 1.0으로.

## 관련 노트
- [픽셀 퍼펙트 렌더링](pixel-perfect-rendering.md) — 렌더 타깃·정수 배율(3D에서도 같다)
- [레트로 3D 모델 파이프라인 — Blockbench → glTF](../assets/retro-3d-models-blockbench-gltf.md)
- [시점 전환(쿼터뷰 ↔ 숄더뷰)과 락온 카메라](../../concepts/camera-mode-switch-and-lock-on.md)
- [Rust 게임 엔진 비교](../rust-game-engines/web-android-gamepad-support.md)
