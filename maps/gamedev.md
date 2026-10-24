---
title: "지도: 게임 개발"
type: map
tags: [gamedev, macroquad, rust]
status: verified
created: 2026-10-24
updated: 2026-10-24
---

# 지도: 게임 개발

게임 개발 관련 노트의 입구. 저장 위치는 종류별 폴더에 있고, 여기서는 도메인 관점으로 모은다.

## macroquad
- 빌드·배포
  - [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](../guides/macroquad-wasm-netlify-github-actions.md) — 전체 절차
  - [WASM 빌드와 JS 번들](../reference/macroquad/wasm-build.md) — 번들 버전 계약, 에셋 로딩
  - [정적 WASM 호스팅](../concepts/static-wasm-hosting.md) — 왜 번들러가 없어도 되는가
  - [0001 빌드는 CI, 호스팅은 Netlify](../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md)

## 아직 없는 것
- 게임 루프/상태 관리, 에셋 파이프라인, 입력 처리 — 노트가 생기면 여기에 추가

## 다른 지도
- [Rust](rust.md) · [CI/CD와 호스팅](ci-cd-hosting.md)
