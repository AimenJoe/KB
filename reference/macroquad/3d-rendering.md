---
title: macroquad 3D 렌더링 — Camera3D·Mesh·배치·조명 없음·모델 로더 없음
type: reference
tags: [macroquad, rust, gamedev, 3d, rendering, camera]
status: verified
created: 2026-11-03
updated: 2026-11-14
verified: |
  1차(소스 + 직접 실행, 2026-11-14, knellroot 0186, macroquad 0.4.16·miniquad 0.4.11 웹): `get_internal_gl().flush()` 뒤 `get_active_render_pass`·
  `get_projection_matrix`로 같은 패스·투영에 miniquad 고정 버퍼(Immutable)를 그려 구운 지형의 85%(정원: 바닥 72k + 고정 175k 정점)를 상주시켰다.
  같은 장면 스크린숏이 같고(그림자·풀 흔들림·외곽선), 헤드리스 Chromium(SwiftShader)에서 프레임마다 올리는 정점 351k → 104k, 우리 코드 CPU 30~35 → 13~16ms,
  `leak.js` 70초 버퍼 수 평평. **실기기(GPU) 숫자는 아직 없다** — SwiftShader는 GPU를 CPU로 흉내 내 업로드 몫이 기기와 다르다.
  1차(직접 구현·헤드리스 실행, 2026-11-10, knellroot 0142, macroquad 0.4.16 웹): 사용자 재질의 정점 셰이더에 `attribute vec4 normal;`을 적으면 `Vertex.normal`(Vec4)이
  그대로 들어온다 — xyz에 면 법선, **w에 정점마다의 값**(흔들림 몫)을 실어 한 번 구운 지형 메시의 풀 끝·잎·불꽃만 움직였다(멈춘 장면 0.5초 간격 스크린숏에서 그 화소만 달라짐).
  기본 셰이더는 이 칸을 읽지 않는다(아래 소스 확인과 같은 줄기). 폰·핸드헬드에서의 비용은 재지 않았다.
  1차(소스·직접 실행, 2026-11-10, knellroot 0135): 0.4.16 `quad_gl.rs` `geometry()`는 정점·색인이 용량 **이상**이면 `warn!("geometry() exceeded max drawcall size, clamping")`을 찍고 자른다.
  여러 모델을 정점 수로만 끊어 모은 배치(외곽선·그림자)가 색인 19,000~25,000이 되어 15,000에서 잘렸다 — Meshy 모델(정점 공유)은 색인 ≈ 정점 × 2.4.
  리눅스 데스크톱 빌드의 stderr에서 처음 봤고(12초에 1,449번), 웹에도 같았다(헤드리스 한 판 2,350번 — 시험이 console error만 모아 놓쳤다). 둘 다 세게 고친 뒤 0.
  1차(직접 구현·시험, 2026-11-07, knellroot 0084): 바닥 표시 32곳의 평판을 땅을 따라 접는 한 함수로 — 시험이 발밑 0·가슴 0.9·턱 위·땅 없음을 본다.
  소스로 확인(2026-11-04, macroquad 0.4.16·miniquad 0.4.11): `render_target_ex(.., depth: true)`는 깊이 텍스처를 만들어 렌더 패스에 붙이지만
  돌려주는 `RenderTarget.depth_texture`는 None — 깊이를 셰이더에서 읽을 수 없다. miniquad 웹은 WebGL1(`getContext("webgl")`)이고
  `WEBGL_depth_texture`를 켠다. `Camera3D`의 정사영은 `fovy` = 세로 전체 높이(m), `matrix()`는 `Camera` 트레이트 메서드라 `use macroquad::camera::Camera`.
  재질은 `MaterialParams { uniforms: Vec<UniformDesc>, textures: Vec<String> }` + `set_uniform`·`set_texture`, 기본 꼭짓점 입력 `position`·`texcoord`·`color0`(÷255), `Model`·`Projection`.
  직접 실행(2026-11-04, knellroot 0044·0045): (1) 굽는 지형의 달빛 그림자를 0.25m 가림 높이 지도 + 광선으로 셈해 바닥 빛 지도 텍스처(가장 가까운 픽셀)에 담으니
  또렷한 픽셀 그림자가 됐다. (2) 캐릭터 그림자는 달 쪽 정사영 카메라로 실루엣을 256² 렌더 타깃에 흰색으로 찍고, 바닥 재질이 월드 자리를 같은 행렬로 옮겨 읽게 했다
  (깊이 비교 없는 가림판 — 위 이유로 깊이를 못 읽어서). 같은 행렬로 찍고 읽으니 렌더 타깃 위아래 뒤집힘을 따로 맞출 필요가 없었다. 120초 누수 시험 평평·60fps(헤드리스).
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
- **GPU에 머무는 메시는 없다.** 매 프레임 모든 정점이 다시 올라간다(움직이지 않는 지형도 — 아래 "섞어 쓰기"). 그래서 CPU에서 정점을 변형(부위별 회전, 스키닝)해 보내도 추가 비용이 거의 없다 — 모델 행렬을 바꾸는 것(`gl.push_model_matrix`)은 드로콜을 가르지만, 정점을 미리 월드 좌표로 바꿔 한 텍스처로 보내면 **한 드로콜**이다. 레트로 3D에서는 "아틀라스 텍스처 하나 + CPU 변형 + 한 배치"가 정석이다.
- 한 번의 `geometry()`가 용량을 넘으면 **에러 없이 잘린다**. 큰 지형 메시는 청크로 나누고, 용량은 `gl_set_drawcall_buffer_capacity`(숨김 함수)로 올릴 수 있다.
- 새 드로콜이 갈리는 조건(텍스처·모델 행렬·파이프라인·유니폼)을 알고 그리기 순서를 정하면 드로콜 수가 수십 → 몇 개가 된다.

### 섞어 쓰기: 움직이지 않는 것만 miniquad 고정 버퍼로
- macroquad를 버리지 않고 그 아래 miniquad를 직접 부른다: `unsafe { get_internal_gl() }` → `.flush()`(쌓인 macroquad 그리기를 지금 카메라로
  먼저 보낸다) → `quad_gl.get_active_render_pass()`·`quad_gl.get_projection_matrix()`로 **같은 렌더 패스·같은 투영**을 얻어 `quad_context`에
  `begin_pass(pass, PassAction::Nothing)` → 우리 파이프라인·`BufferUsage::Immutable` 버퍼로 그린다 → `end_render_pass()`.
  깊이 버퍼는 렌더 타깃 것을 그대로 쓰니 macroquad로 그린 몸들과 서로 가린다.
- 정점 형식은 macroquad `Vertex`(위치 Float3·`texcoord` Float2·`color0` Byte4·`normal` Float4 = 40바이트) 그대로 올리고, 셰이더는
  원래 macroquad 재질의 GLSL을 **같은 상수로** 함께 쓴다(유니폼 `Projection`·`Model`은 우리가 채운다 — `Model`은 단위).
  텍스처는 `Texture2D::raw_miniquad_id()`, 1×1 흰 텍스처를 하나 두고 텍스처 없는 덩어리에 쓴다.
- 지형을 다시 구우면 옛 버퍼를 `delete_buffer`로 지운다 — 안 그러면 GPU 메모리가 자란다([GPU 메모리](gpu-memory-growth.md)).
- 덩어리마다 투명도가 바뀌는 것(가리면 옅어지는 벽)은 배치에 남겨 둔다 — 고정 버퍼로 옮기면 덩어리 수만큼 그리기 호출이 는다.

### 조명·재질
- 기본 셰이더는 `color × texture`뿐. `normal`은 정점에 실려 가지만 **셰이더가 안 읽는다**. 램버트 한 줄이라도 `load_material`(커스텀 GLSL, WebGL1 = GLSL ES 1.0)로 쓴다. 2D에서 더하기 빛(`light_material`)을 쓰던 방식과 같다.
- 레트로풍이면 조명을 **정점 색**에 미리 구워(`Vertex.color`) 기본 셰이더로 끝낼 수도 있다 — 부위별 회전이 있으면 법선이 돌아가므로 CPU 변형 때 색을 다시 계산한다.
- 그림자는 엔진에 없다. 직접 하는 길(가벼운 순):
  1. 바닥 원판(접촉 그림자).
  2. **구운 그림자**(움직이지 않는 것): 굽기 때 높이 지도 + 광선으로 가려짐을 셈해 정점 색이나 바닥 **빛 지도 텍스처**(가장 가까운 픽셀이면 픽셀 그림자)에.
  3. **가림판**(움직이는 것): 빛 쪽 정사영 카메라로 실루엣을 작은 렌더 타깃에 찍고, 받는 면의 재질이 같은 행렬로 읽는다. 깊이 비교가 없어 빛과 물체 사이의 면도 어두워질 수 있다.
  4. 진짜 셰도맵: 깊이를 RGBA에 싸서(WebGL1) 빛 쪽에서 찍고 비교 — `RenderTarget`이 깊이 텍스처를 내주지 않아 색으로 싸야 한다.

### 모델·애니메이션
- 로더가 없다. 선택지: ① `gltf` 크레이트(1.4.x, 노드 트리·애니메이션 채널 읽기 지원)로 읽어 `Mesh`로 옮김, ② 자체 JSON(상자 목록 + 부위 트리). 스켈레탈 스키닝은 직접 써야 하므로, **부위가 강체로 도는 애니메이션**(마인크래프트식)이 이 스택과 맞는다 → [레트로 3D 모델 파이프라인](../assets/retro-3d-models-blockbench-gltf.md).

### 구운 메시를 움직이기(정점 셰이더)
- 지형처럼 한 번 구워 매 프레임 그대로 보내는 메시를 CPU에서 다시 만들지 않고 움직이려면 **정점에 "얼마나 움직이나"를 싣고 정점 셰이더에서 민다**. `Vertex`에 남는 칸은 `normal: Vec4`뿐이다 — 기본 셰이더가 안 읽으니 xyz는 면 법선(법선 패스·빛 굽기용), **w는 정점마다의 값**으로 쓸 수 있다(`attribute vec4 normal;`).
- 값의 약속 하나로 여러 움직임을 가른다: 예) 1 = 가만히, 1 + s = 느린 바람(풀 끝 1·잎 0.3), 1 − f = 빠른 일렁임(불꽃). 0을 "가만히"로 두지 않는 까닭 — 법선 칸을 안 채운 정점(전부 0)과 구별하려고.
- 같은 메시를 여러 패스(색·법선·그림자)로 그리면 **모든 패스의 정점 셰이더가 같은 식**이어야 한다 — 하나만 밀면 윤곽선·그림자가 몸에서 떨어진다.
- uniform은 재질마다 따로 넣는다(시각·세기·밟는 이의 자리 등 `vec4` 하나면 족했다).

## 왜?
macroquad는 2D 즉시 모드 라이브러리에 3D 카메라를 얹은 것이다. 모든 그리기가 "정점 배열을 매 프레임 배치해 올리기"라서 상태를 가진 GPU 자원(VBO에 상주하는 메시, 본 행렬 유니폼 배열)이 없다. 그 단순함이 웹 번들 400KB와 빠른 컴파일의 대가다. 이 전제를 알고 설계하면(작은 메시, 아틀라스, CPU 변형) 3D도 무리 없이 돌고, 모르고 Unity식으로 짜면(메시마다 드로콜·머티리얼) 드로콜이 폭발한다.

## 함정
- **`render_target()`에는 깊이 버퍼가 없다.** 3D를 저해상도 타깃에 그리면 깊이 시험이 조용히 사라지고 그린 순서로만 덮인다 — 상자 모델이 "속이 비치거나 엉켜" 보이고 벽이 얇은 판처럼 겹친다. 오류도 경고도 없어서 화풍 문제로 착각하기 쉽다(knellroot는 첫 스테이지까지 모르고 왔다). 3D 타깃은 처음부터 `render_target_ex(.., depth: true)`.
- `Camera3D::default()`의 z-up. 2D 머리로 y-up을 가정하고 `position (0,10,-10)`을 주면 세상이 옆으로 눕는다.
- 렌더 타깃에 3D를 그릴 때 `aspect`를 빼먹으면 화면 비율로 찌그러진다.
- **여러 모델을 한 배치로 모을 때는 정점과 색인을 둘 다 센다.** 정점만 보고 끊으면 색인이 먼저 넘친다 — 정점을 나눠 쓰는 모델(Meshy 등 AI 메시를 줄인 것)은 색인이 정점의 2배를 넘는다. "넣기 전에 `v + nv < MAX_V && i + ni < MAX_I`인지 보고 아니면 먼저 보낸다"를 함수 하나로 두고 모든 배치(몸·외곽선·그림자)가 같이 쓴다(knellroot 0135 `render::fits`). 잘림 경고는 `warn!` 한 줄뿐이라 웹에서는 콘솔 warning이다 — 헤드리스 시험이 error만 모으면 못 본다. 데스크톱 빌드를 터미널에서 한 번 켜 보면 stderr에 바로 보인다.
- 정점이 잘리는 실패는 화면에서는 조용하다(경고는 위처럼 로그에만) — 큰 메시가 "일부만 그려지면" 용량부터 의심. **인덱스가 먼저 찬다**(기본 5,000 = 삼각형 1,666개) — 둥근(부드러운) 모델은 정점은 적어도 삼각형이 많다. 모델 한 벌이 용량 안에 드는지 시험으로 지킨다.
- `Orthographics`의 `fovy`는 각도가 아니라 세로 폭. 45(라디안 아님)를 주면 45 월드 단위가 세로로 보인다.
- 기본 WebGL1: `#version 300 es` 셰이더 문법·정수 텍스처·MRT 없음. 레트로엔 상관없지만 커스텀 GLSL은 ES 1.0으로.
- **높낮이 있는 땅의 바닥 표시는 한 길로**: 예고만 땅을 따라 접고 나머지(그림자·발밑 고리·쉼터 테·범위 원 등)를 가운데 높이 평판으로 두면, 경사로·턱에서 한쪽은 땅 속에 묻히고 한쪽은 뜬다 — 서른 곳 넘게 흩어진 평판을 다 찾아야 했다(knellroot 0084). 바닥 그림 함수는 "점마다 그 자리 땅 높이 + (그림 가운데가 땅보다 위인 만큼)" 하나로 두고 평평한 함수는 없앤다(가슴 높이 휘두름 부채꼴도 같은 함수로 땅 위 0.9m를 따라 굽는다). 선 테두리처럼 가운데가 아닌 점에서 시작하는 그림은 높이를 **그림의 기준점**(적의 발)에서 재야 낮은 단 위의 모서리가 뜨지 않는다. 지도 표지(쉼터·문 가운데)도 땅 높이로 내려 앉힌다.

## 관련 노트
- [픽셀 퍼펙트 렌더링](pixel-perfect-rendering.md) — 렌더 타깃·정수 배율(3D에서도 같다)
- [레트로 3D 모델 파이프라인 — Blockbench → glTF](../assets/retro-3d-models-blockbench-gltf.md)
- [시점 전환(쿼터뷰 ↔ 숄더뷰)과 락온 카메라](../../concepts/camera-mode-switch-and-lock-on.md)
- [Rust 게임 엔진 비교](../rust-game-engines/web-android-gamepad-support.md)
