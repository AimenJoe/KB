---
title: "지도: CI/CD와 호스팅"
type: map
tags: [ci, deploy, hosting, github-actions, netlify]
status: verified
created: 2026-10-24
updated: 2026-10-24
---

# 지도: CI/CD와 호스팅

## GitHub Actions
- [Rust → wasm32 빌드 워크플로](../reference/github-actions/rust-wasm-build.md) — 툴체인 액션 비교, 캐시, concurrency

## Netlify
- [CI에서 netlify-cli로 배포](../reference/netlify/deploy-from-ci.md) — Git CD vs CLI 업로드, 섞으면 덮어쓰기, 헤더/캐시
- [정적 WASM 호스팅](../concepts/static-wasm-hosting.md) — 정적 호스트가 제공해야 하는 것

## 엮은 절차
- [macroquad WASM → GitHub Actions → Netlify](../guides/macroquad-wasm-netlify-github-actions.md)
- [0001 빌드는 CI에서, 호스팅은 CLI 업로드로](../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md)

## 다른 지도
- [게임 개발](gamedev.md) · [Rust](rust.md)
