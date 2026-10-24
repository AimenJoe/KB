---
title: "지도: 게임 개발"
type: map
tags: [gamedev, macroquad, rust, game-design, pixel-art, game-feel]
status: verified
created: 2026-10-24
updated: 2026-10-24
---

# 지도: 게임 개발

게임 개발 관련 노트의 입구. 저장 위치는 종류별 폴더에 있고, 여기서는 도메인 관점으로 모은다.

## 설계
- [1인 개발용 액션 로그라이트 설계 원칙](../concepts/action-roguelite-for-solo-dev.md) — 런 구조 vs 메트로배니아, 탑다운 vs 사이드뷰, 전투감 먼저, 캐릭터=반복 단위, 장기 프로젝트 단계
- [그림 못 그려도 도트 게임 만들기](../guides/pixel-art-without-an-artist.md) — 에셋 팩 하나 중심, 라이선스 확인, Aseprite 손보기

## 게임 루프·전투감
- [고정 타임스텝 게임 루프와 히트스톱](../concepts/fixed-timestep-and-hitstop.md) — 누적기 루프, 입력 래치, 보간, 히트스톱은 로직 시계만, trauma² 흔들림

## 엔진·플랫폼 선택
- [Rust 게임 엔진 비교: 웹 + Android 핸드헬드 + 컨트롤러](../reference/rust-game-engines/web-android-gamepad-support.md) — macroquad / Bevy / Godot, Android 게임패드가 공통 공백

## macroquad
- 입력
  - [게임패드와 Android 입력 현황](../reference/macroquad/gamepad-and-android-input.md) — `gamepads` 크레이트, miniquad Android 백엔드의 공백과 패치 범위
- 렌더링
  - [픽셀 퍼펙트 렌더링](../reference/macroquad/pixel-perfect-rendering.md) — 내부 해상도 320×180, render target, Nearest, 정수 배율
- 빌드·배포
  - [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](../guides/macroquad-wasm-netlify-github-actions.md) — 전체 절차
  - [WASM 빌드와 JS 번들](../reference/macroquad/wasm-build.md) — 번들 버전 계약, 에셋 로딩
  - [정적 WASM 호스팅](../concepts/static-wasm-hosting.md) — 왜 번들러가 없어도 되는가
  - [0001 빌드는 CI, 호스팅은 Netlify](../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md)

## 아직 없는 것
- 상태 관리, 절차적 방 생성, 저장(localStorage/파일), 사운드(에셋 파이프라인) — 노트가 생기면 추가

## 다른 지도
- [Rust](rust.md) · [CI/CD와 호스팅](ci-cd-hosting.md)
