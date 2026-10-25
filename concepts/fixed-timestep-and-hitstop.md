---
title: 고정 타임스텝 게임 루프와 히트스톱
type: concept
tags: [gamedev, game-feel, input, rust]
status: draft
created: 2026-10-24
updated: 2026-10-25
verified: |
  1차 출처로 확인: 직접 구현·실행(nail-under-the-roots 1단계 프로토타입, macroquad 0.4.16, 2026-10-24). 누적기 루프, 입력 래치,
  보간, 히트스톱 중 로직 시계 정지, 일시정지·히트스톱 중 보간 prev 동기화를 코드로 넣고 Xvfb 캡처·헤드리스 Chromium으로 동작을 확인했다.
  2차 출처만 있음: Glenn Fiedler "Fix Your Timestep!"(누적기·보간·프레임 시간 상한의 원형. 이 세션에서는 사이트에 접속되지 않아 기억에 의존),
  Squirrel Eiserloh GDC 2016 "Math for Game Programmers: Juicing Your Cameras With Math"(trauma² 흔들림).
  긴 프레임이 전환 연출을 건너뛰는 함정(2026-10-25, nail-under-the-roots 0068): 헤드리스 Chromium에서 장소 전환 중 한 프레임 133~150ms → 나눠 굽기 + 틱 멈춤 뒤 가장 긴 프레임 33ms로 측정.
  확인 못 함: "손맛"이 실제로 좋은지는 사람이 플레이해야 안다. 수치는 전부 가설.
sources:
  - https://gafferongames.com/post/fix_your_timestep/
  - https://www.youtube.com/watch?v=tu-Qe66AvtY
  - https://github.com/AimenJoe/nail-under-the-roots
---

# 고정 타임스텝 게임 루프와 히트스톱

## 요약
로직은 고정 간격(예: 1/60초)으로만 전진시키고, 렌더는 프레임마다 돌리되 마지막 두 로직 상태를 보간해 그린다. 입력의 "눌림"은 래치에 모아 로직 틱이 소비한다. 히트스톱은 **로직 시계만** 멈추는 것이고, 흔들림 같은 연출 시계는 계속 간다. 이 구조여야 손맛 수치(0.12초, 3프레임…)가 어느 기기에서나 같은 뜻을 가진다.

## 본문

### 누적기 루프
```rust
acc += frame_dt.min(MAX_FRAME_DT);      // 상한: 느린 프레임이 틱 폭주로 이어지는 "죽음의 나선" 방지
while acc >= DT { let a = input.take(); world.tick(&a); acc -= DT; }
let alpha = acc / DT;                    // 0..1, 마지막 틱 이후 지난 비율
render(&world, alpha);                   // pos = prev.lerp(cur, alpha)
```
- 모든 움직이는 것은 `prev_pos`를 갖고, 틱 시작에서 `prev_pos = pos`.
- 픽셀 게임이면 보간 결과를 **정수로 반올림**해 그린다.

### 입력 래치
`is_key_pressed()` 같은 "이번 프레임에 눌림"은 렌더 프레임 단위다. 틱이 프레임당 0번(고주사율)이면 눌림이 사라지고, 2번이면 두 틱이 같은 눌림을 본다.
- 프레임마다 `poll()`: 눌림을 `pending |= pressed`로 모으고, 축(스틱·이동 방향)은 최신 값으로 덮는다.
- 틱마다 `take()`: `pending`을 돌려주고 비운다. 축은 최신 값.
- 게임 로직은 `Actions` 구조체만 본다. 키보드·패드 번역은 이 레이어 안에서 끝낸다.

### 히트스톱
- 명중 순간 `hitstop = max(hitstop, n초)`. 틱 머리에서 `hitstop > 0`이면 `hitstop -= DT`만 하고 **로직을 건너뛴다**.
- 건너뛰는 동안에도 **입력 버퍼는 갱신**한다(히트스톱 중 누른 다음 공격이 끝나자마자 나가야 한다).
- 건너뛰는 동안 `prev_pos = pos`로 맞춰 둔다. 안 그러면 보간이 지난 틱과 현재 사이를 계속 왕복해 멈춘 화면이 미끄러진다. 일시정지도 같다.
- 연출 타이머는 두 종류다. 흔들림·히트스톱 자체는 **계속 가야** 하고(멈춘 화면 위에서 흔들려야 "묵직"), 피격 플래시는 로직 시계에 묶어 **멈춰 있다가** 풀리면 사라지는 편이 자연스럽다.

### 화면 흔들림 (trauma)
- `trauma`(0..1)를 명중마다 더하고 초당 일정량 감쇠. 오프셋 = `max_px × trauma²` × 틱마다 새 난수(-1..1). 제곱이라 작은 타격은 거의 안 흔들리고 큰 타격만 크게 흔들린다.
- 픽셀 게임은 오프셋을 정수로 반올림해 카메라 target에 더한다.

## 왜?
- **결정성과 조정 가능성**: 가변 dt에서는 "3프레임 히트스톱", "0.1초 버퍼"가 기기마다 다른 뜻이 된다. 손맛 수치를 한 파일에 모아 조정하려면 시간 단위가 고정돼야 한다.
- **물리 안정성**: 돌진 230px/s 같은 빠른 이동은 dt가 튀면 벽을 뚫는다. 고정 dt면 터널링 조건이 상수다.
- **히트스톱의 정의**: "세상이 멈춘다"는 로직 시계가 멈춘다는 뜻이다. 렌더까지 멈추면 흔들림·플래시가 보이지 않아 효과가 반감된다.

## 함정
- `MAX_FRAME_DT`를 안 두면 탭 전환 뒤 수백 틱이 한 번에 돌아 적이 순간이동한다.
- **무거운 일 한 프레임이 연출을 건너뛴다**: 장소 전환의 검정 한가운데에서 무거운 일(지도 굽기·레벨 생성)을 한 프레임에 하면, 멈춤 자체는 검정이라 안 보여도 그 시간이 누적기에 쌓여 다음 프레임에 틱이 몰아 돈다. 밝아짐(로직 시계로 도는 페이드)의 앞부분이 건너뛰어져 검정 → 반쯤 밝음으로 튄다.
  - 고치기: 무거운 일이 끝날 때까지 **로직 틱을 멈추고 누적기를 비운다**(그동안의 눌림도 버린다). 그러면 연출이 처음부터 돈다.
  - 일 자체는 줄 단위 등으로 **나눠 프레임마다 시간 예산만큼** 한다. 웹(WASM 한 스레드)에서는 한 프레임 수백 ms가 입력·소리까지 밀고, 느린 기기일수록 길어진다. 화면이 검정인 동안은 예산을 넉넉히 잡아도 보이지 않는다.
- 보간을 넣고 일시정지·히트스톱에서 prev를 동기화하지 않으면 멈춘 화면이 떨린다.
- 사운드는 틱이 아니라 **이벤트**에서 재생한다. 틱이 프레임당 여러 번이면 같은 소리가 겹칠 수 있으니 이벤트는 틱당 한 번만 모은다.
- 웹에서 `AudioContext`는 사용자 제스처 뒤에만 시작된다(macroquad 번들이 첫 클릭에서 resume). 첫 소리가 안 나는 건 버그가 아닐 수 있다.

## 관련 노트
- [reference/macroquad/gamepad-and-android-input.md](../reference/macroquad/gamepad-and-android-input.md) — 입력 래치가 필요한 이유(웹 just_pressed 의미)
- [reference/macroquad/pixel-perfect-rendering.md](../reference/macroquad/pixel-perfect-rendering.md) — 정수 반올림, 카메라
- [concepts/action-roguelite-for-solo-dev.md](action-roguelite-for-solo-dev.md) — 전투감을 먼저 만드는 이유
