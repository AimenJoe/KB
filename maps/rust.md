---
title: "지도: Rust"
type: map
tags: [rust, wasm, gamedev]
status: verified
created: 2026-10-24
updated: 2026-10-24
---

# 지도: Rust

## WASM 타깃
- [GitHub Actions에서 Rust → wasm32 빌드](../reference/github-actions/rust-wasm-build.md) — 툴체인 액션, rust-cache, rust-toolchain.toml
- [macroquad WASM 빌드와 JS 번들](../reference/macroquad/wasm-build.md) — 번들러 없는 wasm32-unknown-unknown 빌드, release 프로파일로 크기 축소
- [정적 WASM 호스팅](../concepts/static-wasm-hosting.md)

## 게임 엔진
- [Rust 게임 엔진 비교: 웹 + Android 핸드헬드 + 컨트롤러](../reference/rust-game-engines/web-android-gamepad-support.md) — macroquad / Bevy / Godot(gdext) 플랫폼 커버리지
- [macroquad 게임패드와 Android 입력 현황](../reference/macroquad/gamepad-and-android-input.md) — gilrs가 Android 미지원인 것이 생태계 공통 제약
- [macroquad 픽셀 퍼펙트 렌더링](../reference/macroquad/pixel-perfect-rendering.md)

## 빌드·CI
- [0001 Rust WASM은 GitHub Actions에서 빌드](../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md) — 호스팅 빌더에 cargo 캐시가 없다는 점이 결정적

## 다른 지도
- [게임 개발](gamedev.md) · [CI/CD와 호스팅](ci-cd-hosting.md)
- [1인 게임 코드의 건강 신호](../concepts/solo-game-codebase-health-signals.md) — 부작용 핸들(`&Sfx`)을 받는 로직 함수는 테스트 밖, 소리는 큐로, 글은 구조체 필드로(언어별 파일, 실행 시간 맵은 아님)
