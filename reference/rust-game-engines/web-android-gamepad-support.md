---
title: Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준
type: reference
tags: [rust, gamedev, macroquad, bevy, godot, gamepad, android, wasm]
status: verified
created: 2026-10-24
updated: 2026-10-26
verified: |
  2026-10-26 후속(1차, nail-under-the-roots 0075): miniquad Android 버튼은 keycodes.rs 패치 13줄로 들어온다(F13~F25 키로). 축(아날로그 스틱)은 여전히 안 들어온다.
  cargo-quad-apk는 릴리스 없이 git master 커밋을 고정해 CI에서 쓴다(2026-07 커밋, 동작 확인).
  1차 출처로 확인: miniquad Android 백엔드 소스(게임패드 미지원), gamepads 크레이트 매니페스트(android는 winit 전용),
  gilrs 지원표(Android ✕), godot(gdext) docs.rs(experimental-wasm feature 설명).
  2차 출처만 있음: Bevy가 bevy_gilrs 기반이라는 점(docs.rs 크레이트 설명), wasm 크기 벤치마크(macroquad ~385KB, Bevy ~17MB,
  Fyrox ~16MB; 서드파티 비교 레포), Godot 4 웹 내보내기 크기와 single-thread 기본값(뉴스/블로그), Bevy 릴리스 주기와 breaking change(블로그).
  확인 못 함: Bevy Android에서 winit 경로로 게임패드 입력이 어느 정도 들어오는지. Godot 4 웹 빌드의 실제 바이트 크기.
sources:
  - https://github.com/not-fl3/miniquad
  - https://github.com/fornwall/gamepads
  - https://docs.rs/crate/gilrs/^0.10.2
  - https://docs.rs/bevy_gilrs
  - https://docs.rs/godot
  - https://github.com/imbolc/rust-game-engine-comparsion
  - https://aarambhdevhub.medium.com/rust-game-engines-in-2026-bevy-vs-macroquad-vs-ggez-vs-fyrox-which-one-should-you-actually-use-9bf93669e83f
---

# Rust 게임 엔진 비교: 웹 + Android 핸드헬드 + 컨트롤러

## 요약
"브라우저에서 바로 뜨고, 나중에 Android 핸드헬드에서 컨트롤러로 플레이"라는 요구를 Rust 엔진 중 **온전히 만족하는 것은 없다.** Android 게임패드가 공통 공백이다(gilrs가 Android 미지원 → gilrs 기반인 macroquad용 `gamepads`, Bevy 모두 영향). 공백이 가장 작고 경계가 분명한 쪽은 macroquad(처음 어림은 포크 200줄, 실제로 버튼만은 키코드 표 패치 13줄로 됐다 — 축은 아직), 플랫폼 커버리지가 가장 넓은 쪽은 Godot(단, Rust는 웹에서 실험적).

## 비교표

| | macroquad | Bevy | Godot 4 (+gdext) |
|---|---|---|---|
| 웹 빌드 크기 | ~385KB (벤치, 2차) | ~17MB (벤치, 2차) | 수십 MB (2차) |
| 웹 게임패드 | `gamepads` 크레이트 + JS 플러그인 | bevy_gilrs(gilrs wasm 백엔드) | 내장 |
| 데스크톱 게임패드 | `gamepads` → gilrs | bevy_gilrs | 내장 |
| **Android 게임패드** | 기본은 **없음**(miniquad가 축을 받지 않고 버튼 키코드 미매핑, 1차). 버튼은 miniquad 패치로 해결(1차, 2026-10-26), 축은 아직 | gilrs Android ✕ (1차). 대체 경로 미확인 | 내장 |
| Android 빌드 도구 | `cargo-quad-apk`, 릴리스는 4년+ 없음(2차) — git 커밋 고정으로 쓴다(1차) | cargo-apk/xbuild, GameActivity | 공식 내보내기 |
| Rust 비중 | 100% | 100% | gdext: 웹은 `experimental-wasm` feature, "not yet well tested" (1차) |
| 1인 개발 생산성 | 에디터 없음, 전부 코드 | ECS 학습, 릴리스마다 breaking change (2차) | 에디터·타일맵·애니메이션 내장 |

## 각 선택의 의미
- **macroquad 유지**: 웹 경량성과 단순함을 지키고, Android 컨트롤러는 miniquad 포크로 해결. 비용은 포크 유지와 `cargo-quad-apk` 노화. → [macroquad 게임패드와 Android 입력 현황](../macroquad/gamepad-and-android-input.md)
- **Godot 전환**: 플랫폼 문제가 전부 사라지고 생산성이 오르지만 Rust가 거의 빠지고(웹 타깃에서 gdext는 실험적) 웹 첫 로딩이 무거워진다.
- **Bevy**: 이 요구사항에서는 이점이 없다. Android 게임패드 공백은 같고 웹은 훨씬 무겁다.

## 결정 원칙
핸드헬드가 "나중"이라면 **지금 엔진을 바꾸지 말고, 리스크를 콘텐츠가 쌓이기 전에 실측**한다. hello-world APK를 실기 컨트롤러로 테스트하는 스파이크를 초기 단계에 넣고, 일주일 안에 끝나지 않으면 그때 전환한다. 입력을 액션 단위로 추상화해 두면 어느 쪽으로 가도 전투 코드는 살아남는다.

## 관련 노트
- [reference/macroquad/gamepad-and-android-input.md](../macroquad/gamepad-and-android-input.md)
- [concepts/action-roguelite-for-solo-dev.md](../../concepts/action-roguelite-for-solo-dev.md)
