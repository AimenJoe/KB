---
title: macroquad 앱이 백그라운드로 갈 때 — 플랫폼별로 엔진이 하는 것과 안 하는 것
type: reference
tags: [macroquad, miniquad, android, ios, wasm, audio, lifecycle, save]
status: draft
created: 2026-11-19
updated: 2026-11-19
verified: |
  1차 출처로 확인(소스, 2026-11-19, Naïl 0298): macroquad 0.4.16 `src/lib.rs` — `window_minimized_event`는 오디오 멈춤(`audio_context.pause()`)이
  `#[cfg(target_os = "android")]`에만 있고, 누르던 키·마우스를 놓고 터치를 Ended로 만들고 입력 구독자에게 `WindowMinimized`를 보낸다.
  `window_restored_event`도 오디오 재개는 Android만. 사용자 코드(main future)는 `EventHandler::draw` 안에서 `exec::resume`으로 돈다.
  `input::utils::register_input_subscriber`·`repeat_all_miniquad_input`(매 프레임 비워야 쌓이지 않는다).
  miniquad 0.4.x `src/native/android.rs` — Java onPause/onResume → `Message::Pause/Resume` → `window_minimized/restored_event`,
  surface가 없으면 `frame()`이 update만 하고 draw를 건너뛴다. `ios.rs` — applicationWillResignActive/DidBecomeActive → Pause/Resume.
  `wasm.rs` `focus(bool)` → minimized/restored. `windows.rs` WM_SIZE SIZE_MINIMIZED, `macos.rs`·`linux_x11.rs`도 최소화 사건.
  번들 `mq_js_bundle.js`: `document.hasFocus() && visibilityState=="visible"`이 바뀔 때(visibilitychange·focus·blur) `wasm_exports.focus`,
  오디오 플러그인은 AudioContext 클래스를 IIFE에서 읽어 두고(생성자 교체가 안 먹는다) 소리마다 `createGain`.
  직접 시험(헤드리스 Chromium, Naïl `tools/test/smoke.js bg:`): createGain 감싸기로 모은 컨텍스트를 숨김에서 suspend → "suspended",
  보이면 "running", 자동 일시정지를 끈 빌드에서는 일시정지 확인 시험이 실패하고 켠 빌드에서는 통과.
  확인 못 함: 실기기(Android onPause 뒤 surface가 사라지기 전 프레임이 실제로 도는지, iOS 홈 화면 웹앱에서 resume이 막히는지), PC 최소화 중 루프가 계속 도는지.
sources:
  - https://github.com/not-fl3/macroquad
  - https://github.com/not-fl3/miniquad
  - https://developer.chrome.com/docs/web-platform/page-lifecycle-api
  - https://developer.mozilla.org/en-US/docs/Web/API/BaseAudioContext/state
---

# macroquad 앱이 백그라운드로 갈 때

## 요약
엔진은 모든 플랫폼에서 **"최소화" 사건만** 낸다. 소리를 멈춰 주는 것은 **Android 네이티브뿐**이고, 게임을 멈추거나 저장하는 것은 아무 데서도 안 해 준다. 그래서 게임이 직접: 사건을 들어 **일시정지 창 + 적기**, 웹은 JS에서 **AudioContext suspend/resume**.

## 플랫폼별
| | 사건 | 소리 | 게임 루프 |
|---|---|---|---|
| Android | onPause/onResume → minimized/restored | 엔진이 멈추고 켠다 | surface가 사라지면 draw를 건너뛰어 멈춘다(사용자 코드는 draw 안) — onPause와 surface 파괴 사이엔 몇 프레임 돌 수 있다 |
| iOS | WillResignActive/DidBecomeActive | 엔진은 안 건드림(앱이 정지되면 같이 멈춤, 제어 센터 정도에선 계속) | 정지되면 멈춤 |
| 웹 | 번들이 `hasFocus && visible`의 변화를 `focus(bool)`로 → minimized/restored. **창 포커스만 잃어도** 온다 | **안 멈춘다**(휴대폰 브라우저 탭 전환에도 음악) | 숨으면 rAF가 멈춰 같이 멈춤 |
| PC | 창 최소화(WM_SIZE 등). 포커스 잃음은 아님 | 안 멈춘다 | 계속 돌 수 있다 |

## 게임 쪽에서 하는 것
- **사건 듣기**: `let sub = register_input_subscriber();` → 매 프레임 `repeat_all_miniquad_input(&mut h, sub)`, `h`는 `EventHandler`(update·draw 빈 함수 + `window_minimized_event`에서 깃발). 구독은 매 프레임 비워야 쌓이지 않는다.
- **멈추고 적기**: 깃발이 서면 싸움 장면에서 일시정지 창을 연다 — 일시정지가 이미 저장 지점이면 저장은 따라온다. 소리(확인음)는 내지 않는다(돌아온 순간 울린다).
- **웹 소리**: 번들의 오디오 플러그인은 `AudioContext` 클래스를 미리 읽어 둬서 `window.AudioContext`를 바꿔도 안 먹는다. **`AudioContext.prototype.createGain`을 감싸** 컨텍스트를 모으고 `visibilitychange`에서 `suspend()`/`resume()`, `pagehide`/`pageshow`도. iOS처럼 돌아와 resume이 막히면(interrupted) 다음 터치·키에서 다시.
- **시험(헤드리스)**: `document.visibilityState`·`hidden`을 `defineProperty`로 덮고 `visibilitychange`를 보낸다(헤드리스는 진짜로 숨지 않는다). 일시정지 여부는 화면이 아니라 **다음 Esc의 소리**로 — `AudioBufferSourceNode.prototype.start`를 감싸 버퍼마다 번호를 매기고, 손으로 열고 닫을 때의 소리와 견준다.

## 왜?
엔진은 "앱이 내려갔다"는 사실만 안다 — 그때 무엇을 해야 하는지(멈출지, 무엇을 적을지)는 게임 규칙이라 엔진이 정할 수 없다. 소리만은 OS 정책이 갈려서(Android는 백그라운드 재생이 그대로 들린다) macroquad가 Android에서만 대신 해 주고, 웹은 브라우저가 대신 해 줄 거라 보고 비워 둔 것으로 읽힌다 — 실제로는 휴대폰 브라우저가 해 주지 않는다.

## 함정
- 웹은 숨으면 프레임이 멈추므로 **숨는 순간의 저장은 게임 루프 밖(JS)에서 동기로**만 된다. 대개는 포커스를 잃는 순간(숨기 전)에 사건이 와서 일시정지 창 → 저장이 먼저 돈다.
- 웹의 최소화 사건은 **창 포커스만 잃어도** 온다(주소창 클릭·다른 창). 일시정지는 괜찮지만, 다른 용도(예: 정산)에 쓰면 너무 자주 불린다.
- 앱인토스 게임 체크리스트처럼 "백그라운드에서 소리 즉시 종료"를 보는 곳이 있다 — 웹뷰로 나가는 게임은 JS 쪽 처리가 필수.

## 관련 노트
- [로그라이트 저장 슬롯과 이어하기](../../concepts/roguelite-save-slots-and-continue.md) — 저장 지점·웹 visibilitychange
- [소리(quad-snd)](audio.md)
- [WASM 빌드와 JS 번들](wasm-build.md)
