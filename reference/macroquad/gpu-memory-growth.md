---
title: macroquad 앱이 오래 켜면 죽을 때 — GPU 메모리가 자라는 두 원인과 재는 법
type: reference
tags: [macroquad, rust, webgl, memory, performance, debugging, wasm]
status: draft
created: 2026-11-03
updated: 2026-11-03
verified: |
  1차 출처로 확인(2026-11-03, macroquad 0.4.16 소스 + 직접 실행):
  - `telemetry::capture_frame()`을 부르면 다음 프레임의 그리기 호출마다 `track_drawcall`(telemetry.rs)이
    `new_render_texture(128×128)` + `new_render_pass`를 만들어 `drawcalls` 목록에 넣고 지우지 않는다.
    Knellroot에서 30프레임마다 불렀더니 헤드리스 Chromium에서 텍스처가 150초에 152 → 5,329장(GL 텍스처 28 → 352MB),
    호출 스택이 `set_camera → perform_render_passes → QuadGl::draw → new_render_texture`. 부르는 줄을 지우자 120초 동안 17장 그대로.
  - QuadGl은 그리기 호출 칸(`draw_calls_bindings`)마다 정점·색인 버퍼를 잡고 줄이지 않는다(quad_gl.rs `draw`,
    칸이 모자랄 때만 `push`). 버퍼 수는 "가장 많았던 프레임"까지 오르고 평평 — 새는 것이 아니라 최댓값을 붙잡음.
    같은 탐침에서 버퍼 82 → 98(스테이지)·140(잡몹 80)에서 멈춤.
  - wasm 선형 메모리(`wasm_memory.buffer.byteLength`)는 같은 시간 40.6MB 그대로.
  확인 못 함(이번에 실행하지 않음): 아래 Rust 힙 도구들의 현재 사용법 — 이름과 용도만 적는다.
sources:
  - https://github.com/not-fl3/macroquad/blob/master/src/telemetry.rs
  - https://github.com/not-fl3/macroquad/blob/master/src/quad_gl.rs
  - https://docs.rs/dhat/latest/dhat/
---

# macroquad 앱이 오래 켜면 죽을 때

## 요약
"한참 두면 화면 일부가 하얗게 됐다가 꺼진다"(특히 Android·핸드헬드 브라우저)는 대개 **GPU 메모리가 차서 WebGL 문맥을 잃는 것**이다. Rust의 소유권은 CPU 힙만 지키고, GPU 자원(텍스처·버퍼)은 엔진 API를 어떻게 부르느냐에 달렸다. macroquad 0.4에서 본 원인 둘: ① **`telemetry::capture_frame()`이 잡을 때마다 그리기 호출 수만큼 128×128 텍스처를 흘린다** — 측정 코드가 측정 대상을 죽인다. ② 그리기 호출 칸마다 잡은 버퍼(정점 10,000개분 ≈ 400KB)를 줄이지 않는다 — 한 번이라도 호출이 많았던 프레임이 있으면 그만큼 계속 쥔다. 재는 법: 브라우저에서 WebGL 함수를 감싸 살아 있는 텍스처·버퍼 수를 시간에 따라 찍는다.

## 재는 법 (WebGL 탐침)
- Playwright `addInitScript`로 `WebGLRenderingContext.prototype`의 `createTexture/deleteTexture`, `createBuffer/deleteBuffer`, `bufferData`·`texImage2D`(크기)를 감싸 **살아 있는 수와 바이트**를 센다. WebGL1에서 miniquad는 `ANGLE_instanced_arrays`로 그리므로 그리기 횟수는 `getExtension`이 돌려준 객체의 `drawElementsInstancedANGLE`을 감싼다.
- 10초마다 찍기: 텍스처·버퍼 수, `wasm_memory.buffer.byteLength`(miniquad JS 번들의 전역), `performance.memory.usedJSHeapSize`. 게임은 자동 입력으로 계속 움직이게.
- 읽기: **시간에 비례해 계속 오르면 샌다**, 처음 몇십 초 오르다 평평해지면 최댓값을 붙잡은 것. 새는 쪽이 보이면 `createTexture` 안에서 `new Error().stack`을 몇 개 모은다 — wasm 이름 구역이 남아 있으면(릴리스 기본) Rust 함수 이름까지 나온다.
- 예: Knellroot `tools/test/leak.js`.

## Rust 힙(CPU) 쪽 도구 — 이름만(이번엔 쓰지 않음)
| 도구 | 무엇 |
|---|---|
| `dhat` 크레이트 | 전역 할당자를 바꿔 할당 위치별 바이트·수명 기록(데스크톱 빌드) |
| heaptrack / Valgrind massif | 리눅스에서 네이티브 바이너리의 힙 성장 그래프 |
| AddressSanitizer·LeakSanitizer | nightly `-Zsanitizer=address`, 종료 때 안 풀린 할당 보고 |
| 브라우저 | wasm 선형 메모리는 줄지 않고 자라기만 한다 — `byteLength`가 계속 오르면 Rust 쪽, 그대로면 GPU·JS 쪽 |
GPU 자원은 위 도구에 안 잡힌다(드라이버 메모리). 그래서 WebGL 탐침이 먼저다.

## 왜?
- Rust에서 `Box::leak`·`mem::forget`·순환 `Rc`는 **안전한** 누수다. 엔진이 GPU 핸들을 벡터에 계속 넣고 지우지 않는 것도 Rust가 보기엔 정상 코드다.
- macroquad의 telemetry는 디버그 창(드로콜 미리보기 그림)을 위해 만든 것이라 그림을 텍스처로 떠 둔다. 한 번 잡고 보는 용도이지, 계속 부르는 계측용이 아니다.
- 그리기 호출 칸은 다음 프레임에 다시 쓰려고 쥐고 있다(할당을 피하려는 설계). 그래서 **최대 호출 수 × 400KB**가 GPU 몫으로 남는다 — 선·면을 번갈아 그리면 호출이 늘어나는 이유와 같이 볼 것([3D 렌더링](3d-rendering.md)).

## 함정
- 측정 줄에 `telemetry::drawcalls().len()`을 띄우려고 `capture_frame()`을 주기적으로 부르면 바로 이 누수다. 호출 수는 자기 배치가 보낸 횟수로 세거나, 바깥(탐침)에서 잰다.
- 데스크톱에서는 GPU 메모리가 넉넉해 몇 시간 멀쩡하고, 핸드헬드 브라우저에서만 몇 분 만에 죽는다 — "기기 탓"으로 넘기기 쉽다.
- 헤드리스 Chromium(SwiftShader)도 같은 수를 보여 준다. 실기 없이 CI에서 잡을 수 있다.

## 관련 노트
- [macroquad 3D 렌더링](3d-rendering.md)
- [글자 그리기 비용과 브라우저 프레임레이트](text-rendering-and-browser-frame-rate.md) — 프레임 중간 아틀라스 키우기와 지워진 텍스처
