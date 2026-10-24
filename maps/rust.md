---
title: "지도: Rust"
type: map
tags: [rust, wasm]
status: verified
created: 2026-10-24
updated: 2026-10-24
---

# 지도: Rust

## WASM 타깃
- [GitHub Actions에서 Rust → wasm32 빌드](../reference/github-actions/rust-wasm-build.md) — 툴체인 액션, rust-cache, rust-toolchain.toml
- [macroquad WASM 빌드와 JS 번들](../reference/macroquad/wasm-build.md) — 번들러 없는 wasm32-unknown-unknown 빌드, release 프로파일로 크기 축소
- [정적 WASM 호스팅](../concepts/static-wasm-hosting.md)

## 빌드·CI
- [0001 Rust WASM은 GitHub Actions에서 빌드](../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md) — 호스팅 빌더에 cargo 캐시가 없다는 점이 결정적

## 다른 지도
- [게임 개발](gamedev.md) · [CI/CD와 호스팅](ci-cd-hosting.md)
