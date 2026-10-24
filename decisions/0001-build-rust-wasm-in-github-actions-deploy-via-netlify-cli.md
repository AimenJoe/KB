---
title: "0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다"
type: decision
tags: [rust, wasm, netlify, github-actions, ci, macroquad]
status: verified
created: 2026-10-24
updated: 2026-10-24
verified: |
  근거 사실은 reference/netlify/deploy-from-ci.md, reference/github-actions/rust-wasm-build.md의 verified 항목 참조.
sources:
  - reference/netlify/deploy-from-ci.md
  - reference/github-actions/rust-wasm-build.md
  - https://answers.netlify.com/t/build-netlify-in-github-actions/42902
---

# 0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다

- 상태: 채택 (2026-10-24)
- 적용 범위: macroquad 등 번들러 없는 Rust → WASM 정적 사이트

## 맥락
macroquad 게임을 웹에 올리려 한다. 산출물은 정적 파일 셋(wasm, html, js 글루)이다. 선택지는 세 가지였다.

1. Netlify Git CD에 레포를 연결해 Netlify가 Rust를 빌드
2. GitHub Actions에서 빌드하고 `netlify-cli`로 업로드
3. GitHub Actions에서 빌드하고 GitHub Pages에 배포

## 결정
**2번.** 빌드는 GitHub Actions, 호스팅은 Netlify, 연결은 공식 CLI. Netlify 사이트에는 Git 연동을 걸지 않는다.

## 왜

### Netlify가 빌드하면 안 되는 이유 (1번 기각)
- 빌드 이미지에 rustup/cargo는 있지만 **기본 Rust 툴체인이 없다.** `rust-toolchain` 파일이나 build command로 매번 설치해야 한다.
- **cargo 캐시가 없다.** 매 배포가 풀 빌드이고 Netlify 빌드 분을 소모한다. GitHub Actions는 `rust-cache`로 증분 빌드가 되고 무료 분량도 훨씬 크다.
- 빌드 환경을 내가 제어하지 못한다(이미지 전환, mise 자동 감지 같은 미문서 동작이 포럼에 보고됨).
- 결과물이 정적 파일이라 Netlify의 빌드 기능에서 얻는 이점이 없다.

### 그래도 Netlify를 쓰는 이유 (3번 대신)
- 커스텀 헤더/리다이렉트, PR 미리보기(alias 배포), 커스텀 도메인 설정이 GitHub Pages보다 편하다.
- 배포가 원자적이고 각 배포에 고유 URL이 남아 비교·공유가 쉽다.
- 단, 이 이점이 필요 없다면 3번이 더 단순하다(토큰 불필요). 프로젝트별로 재검토한다.

### 서드파티 액션 대신 공식 CLI
- Netlify 스태프가 서드파티 액션은 지원하지 않는다고 명시했다.
- CLI는 `--alias`, `--message`, 종료 코드 등으로 필요한 제어가 다 된다.

## 결과
- 장점: 빠른 증분 빌드, 빌드 환경 완전 제어, 산출물을 다른 호스트에도 재사용 가능.
- 단점/비용: PR 미리보기를 직접 구현해야 함, 포크 PR은 미리보기 불가, Netlify 개인 토큰을 GitHub Secrets에 보관해야 함, Git CD와 섞으면 덮어쓰기 사고가 난다는 운영 규칙을 기억해야 함.

## 재검토 조건
- Netlify가 Rust 기본 툴체인과 cargo 캐시를 제공하게 되면 1번 재평가.
- 헤더/미리보기/도메인이 불필요한 소규모 프로젝트면 3번.

## 관련 노트
- [guides/macroquad-wasm-netlify-github-actions.md](../guides/macroquad-wasm-netlify-github-actions.md)
