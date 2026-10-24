---
title: CI에서 netlify-cli로 배포
type: reference
tags: [netlify, ci, deploy, hosting]
status: verified
created: 2026-10-24
updated: 2026-10-24
verified: |
  1차 출처로 확인: Netlify 공식 에이전트 컨텍스트(netlify-deploy, netlify-config, cli-commands, deployment-patterns),
  Netlify 빌드 의존성 문서(rustup/cargo 사전설치, 기본 툴체인 없음, rust-toolchain 파일).
  2차 출처만 있음: 스태프의 "서드파티 액션 미지원" 발언(포럼), CLI `Response is not defined` 회귀(포럼),
  `.wasm` Content-Type/캐시 헤더 사례(블로그).
sources:
  - https://docs.netlify.com/cli/get-started/
  - https://docs.netlify.com/build/configure-builds/manage-dependencies/
  - https://docs.netlify.com/build/configure-builds/available-software-at-build-time/
  - https://answers.netlify.com/t/build-netlify-in-github-actions/42902
  - https://answers.netlify.com/t/guide-for-deploy-using-github-actions/2981
  - https://github.com/QuantEcon/lecture-python.myst/pull/599
  - https://answers.netlify.com/t/netlify-cli-referenceerror-response-is-not-defined/147257
  - https://www.bentopdf.com/docs/self-hosting/netlify
  - https://answers.netlify.com/t/bug-incorrect-docs-only-matches-one-component-in-headers/42925
---

# CI에서 netlify-cli로 배포

## 요약
외부 CI에서 빌드한 결과물을 Netlify에 올릴 때는 **공식 `netlify-cli`** 를 쓰고, 그 사이트에는 **Git 연동(Continuous Deployment)을 걸지 않는다.** 인증은 `NETLIFY_AUTH_TOKEN` + `NETLIFY_SITE_ID` 환경변수.

## 두 가지 배포 모델

| | Git CD (Netlify가 빌드) | CLI 업로드 (CI가 빌드) |
|---|---|---|
| 트리거 | push / PR | CI가 `netlify deploy` 실행 |
| 빌드 위치 | Netlify 빌드 이미지 | 내 CI |
| PR 미리보기 | 자동 (Deploy Preview) | 직접 `--alias`로 구현 |
| 빌드 분 | Netlify 빌드 분 소모 | CI 분 소모 |
| 캐시 | 언어별 제한적 (cargo 캐시 없음) | CI 캐시 자유 |
| 적합 | JS 프레임워크 | Rust/Go 등 컴파일 무거운 것, 아티팩트 재사용 |

Netlify 자체 문서도 "Git CD가 기본, CLI는 프로토타입·Git 없는 프로젝트·**CI가 빌드한 아티팩트 업로드**용"으로 구분한다.

### 둘을 섞으면 안 되는 이유
Git CD가 연결된 사이트에 CLI로 `--prod` 배포하면, 다음 push 때 Netlify가 자체 빌드를 돌려 **CLI 배포를 조용히 덮어쓴다.** 따라서 CLI 모델을 택했으면 사이트를 `netlify init --manual`(또는 UI "Deploy manually")로 만들고 레포를 연결하지 않는다.

## 명령

```sh
# 인증: 환경변수. CI에서는 netlify login 안 함.
export NETLIFY_AUTH_TOKEN=...   # User settings → Applications → Personal access token
export NETLIFY_SITE_ID=...      # Site configuration → General → Site ID (API ID)

netlify deploy --dir=dist                 # draft (고유 URL)
netlify deploy --dir=dist --prod          # production
netlify deploy --dir=dist --alias=pr-12   # pr-12--<site>.netlify.app
netlify deploy --dir=dist --prod --message="$GIT_SHA"
```

- `deploy`는 **빌드를 하지 않는다.** `--build`를 주지 않으면 `--dir`의 파일을 그대로 올린다. CI에서 빌드 단계를 먼저 둔다.
- `--site`에는 사이트 **ID**를 준다. 폴더 경로를 넣는 실수가 흔하다(성공한 척하고 아무것도 안 올라감).
- 배포는 원자적이다. 모든 파일이 올라간 뒤에 스위치되므로 중간 상태가 없다.
- 실패한 배포는 발행되지 않으므로 롤백 개념이 없다. 잘못 발행했으면 커밋을 revert해 앞으로 고친다.
- 종료 코드: 0 성공, 2 인증 오류, 3 사이트 없음, 4 빌드 실패.

### 버전 고정
`npx netlify-cli@<major>`로 메이저를 고정한다. Node가 낮으면 `ReferenceError: Response is not defined`로 깨진 사례가 있어 Node 20 이상을 쓴다.

### 공식 CLI vs 서드파티 액션
Netlify 스태프는 포럼에서 "서드파티 액션은 지원하지 않으며 공식 CLI를 쓰라"고 답했다. `nwtgck/actions-netlify`에서 공식 CLI로 갈아탄 사례(QuantEcon, 2025-09)도 있다. PR 코멘트 같은 부가 기능이 꼭 필요할 때만 서드파티를 고려한다.

## 포크 PR
`pull_request` 이벤트에서 포크에서 온 PR에는 시크릿이 전달되지 않는다. 미리보기 단계에 `github.event.pull_request.head.repo.fork == false` 조건을 건다.

## 헤더와 캐시
- Netlify 기본 캐시는 `max-age=0, must-revalidate` + ETag다. 원자적 배포와 잘 맞아 **그대로 두면 된다.**
- `immutable` 장기 캐시는 파일명에 해시가 있을 때만. 없으면 배포 후에도 옛 파일이 로드된다.
- `.wasm`을 `application/wasm`으로 내는지 배포 후 `curl -I`로 한 번 확인한다. 필요하면 `netlify.toml`:
  ```toml
  [[headers]]
    for = "/*.wasm"
    [headers.values]
    Content-Type = "application/wasm"
  ```
  헤더 글롭 `*`가 경로 한 단계만 매칭했다는 포럼 보고가 있으니 중첩 경로는 따로 확인한다.
- `[[headers]]`/`[[redirects]]`는 컨텍스트별로 못 나눈다(항상 전역).

## Netlify에서 Rust를 직접 빌드할 때 (참고)
- 빌드 이미지(Ubuntu 24.04 Noble)에 rustup/cargo는 있지만 **기본 툴체인이 없다.** `rust-toolchain` 파일을 두거나 build command에서 `rustup toolchain install`/`rustup default stable`을 실행해야 한다.
- wasm 타깃도 직접 `rustup target add wasm32-unknown-unknown`.
- cargo 빌드 캐시가 없어 매번 풀 빌드다. → [decisions/0001](../../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md)

## 기타
- `.netlify/` 디렉터리(`state.json`)는 커밋하지 않는다. `.gitignore`에 추가.
- 비밀값은 `netlify.toml`에 쓰지 않는다. 커밋되는 파일이다.
- 시크릿 스캐너가 걸리면 진짜 비밀값이 산출물에 들어간 것이다. `SECRETS_SCAN_ENABLED=false`로 끄지 말고 원인을 고친다.

## 관련 노트
- [guides/macroquad-wasm-netlify-github-actions.md](../../guides/macroquad-wasm-netlify-github-actions.md)
- [reference/github-actions/rust-wasm-build.md](../github-actions/rust-wasm-build.md)
