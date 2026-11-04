---
title: GitHub Actions의 액션과 Rust 버전 고정하기 — SHA 고정·Dependabot·잠금 파일, dtolnay/rust-toolchain을 SHA로 쓸 때
type: reference
tags: [github-actions, ci-cd, security, rust, supply-chain]
status: draft
created: 2026-11-04
updated: 2026-11-04
verified: |
  1차 출처로 확인(2026-11-04, GitHub docs 원문 저장소의 마크다운을 curl로 받아 읽음):
  - "Secure use reference": 액션 하나가 뚫리면 그 잡의 시크릿·GITHUB_TOKEN에 닿는다. 가장 강한 방법은 워크플로 잠금 파일,
    못 쓰면 **전체 길이 커밋 SHA로 고정**, 태그는 만든 이를 믿을 때만(태그는 옮겨지거나 지워질 수 있다).
  - "Workflow dependency lockfiles": `.github/workflows/actions.lock`을 `gh actions-lock`(gh 확장)이 만든다. 간접 의존 액션까지 커밋과
    저장소 아이디(owner_id·repo_id)를 적고 실행 때 확인한다. 재사용 워크플로 호출(`jobs.<id>.uses`)은 덮지 않는다 — 그건 SHA로.
    문서가 기능 플래그(`actions-workflow-lockfiles`) 아래에 있다.
  - "Available rules for rulesets": "Require status checks to pass before merging" — 켜면 필수 검사가 다 통과해야 그 갈래에 합칠 수 있다.
  - "Dependabot options reference": `directories`(여러 폴더), `target-branch`(기본 갈래가 아닌 곳으로 PR, 이때 보안 업데이트에는 일부 옵션이 안 먹는다).
  - dtolnay/rust-toolchain README: 툴체인은 **@rev 이름이 정한다**(@stable, @1.89.0). 입력 `toolchain`을 넘기면 @master를 쓰라고 하고,
    SHA로 고정할 때는 **master 역사 안의 SHA**여야 한다(아니면 언젠가 GC되어 워크플로가 깨진다).
  - netlify-cli 23.15.1 소스(npm 패키지): `deploy --json`의 출력에 `--prod`일 때만 `url`(사이트 주소)이 붙는다. 그 밖에는 `deploy_url`.
  직접 해 봄(nail-under-the-roots, 2026-11-04): 액션 11종을 SHA + `# v태그` 주석으로 바꾸고, Rust를 `rust-toolchain.toml`의 1.99.1로,
  dtolnay(master SHA + `toolchain` 입력)·rust-cache를 묶은 액션 하나로 — 결과는 아래 "실행 결과".
  확인 못 함: macOS 러너에서 묶은 액션이 도는지(장애로 못 돌림), 잠금 파일 기능을 무료 공개 레포에서 지금 쓸 수 있는지(문서가 기능 플래그 아래), Dependabot이 `# master` 주석의 SHA를 어떻게 올리는지.
sources:
  - https://docs.github.com/en/actions/reference/security/secure-use
  - https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
  - https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference
  - https://github.com/dtolnay/rust-toolchain
---

# GitHub Actions의 액션과 Rust 버전 고정하기

## 요약
`uses: 주인/액션@v2`의 `v2`는 움직이는 이름이다. 그 레포가 뚫려 태그가 옮겨지면 그 코드가 **같은 잡의 시크릿·쓰기 토큰 곁에서** 돈다. 시크릿이 있는 잡의 액션은 **커밋 SHA로 고정**하고(`@<40자> # v2.9.3`), 낡지 않게 Dependabot(github-actions)이 올리게 한다. 같은 이유로 `rust-toolchain.toml`의 `channel = "stable"`도 움직이는 이름이다 — 숫자로 고정하고 일부러 올린다. 고정이 끝나면 "main에 빨간 CI가 못 들어가게"(필수 상태 검사)까지 켜야 고정한 검사가 실제로 무엇을 막는다.

## 본문
### 액션
1. SHA 찾기: `git ls-remote https://github.com/<주인>/<액션> 'refs/tags/v7^{}'`(주석 태그면 `^{}` 쪽이 커밋). 주석에는 그 SHA를 가리키는 가장 구체적인 태그(`v7.0.1`)를 적는다 — Dependabot이 그 주석을 읽고 같이 올린다.
2. GitHub 공식 액션(`actions/*`)도 같이 고정하면 규칙이 하나라 쉽다.
3. `.github/dependabot.yml`: `package-ecosystem: github-actions`, `directories`에 `/`(워크플로)와 **로컬 묶은 액션 폴더**(`/.github/actions/<이름>`)를 둘 다, `groups`로 달마다 PR 하나. 개발 갈래가 따로 있으면 `target-branch`.
4. 잠금 파일(`actions.lock`)이 쓸 수 있으면 그쪽이 더 강하다(간접 의존·저장소 아이디까지). 재사용 워크플로 호출은 여전히 SHA로.

### Rust 툴체인
- `rust-toolchain.toml`: `channel = "1.99.1"`. 올릴 때는 그 줄만 바꾸고 로컬 검사(clippy -D warnings 포함)를 다 돌려서 커밋.
- `dtolnay/rust-toolchain`을 SHA로 고정하면 @rev가 버전을 못 정한다 → `toolchain:` 입력으로 넘긴다. 같은 숫자를 워크플로 여러 곳에 쓰지 않도록 **로컬 묶은 액션**(`.github/actions/rust/action.yml`, `using: composite`)이 toml의 `channel` 줄을 읽어 넘긴다. rust-cache도 그 안에.
- 액션이 까는 툴체인과 toml이 가리키는 툴체인이 **같은 이름**이어야 한다. 액션은 `stable`을 깔았는데 toml이 `1.99.1`이면 cargo가 처음 돌 때 rustup이 1.99.1을 또 받고, 액션에 준 `targets`(android·ios 등)는 엉뚱한 쪽에 깔려 있다.
- 로컬에서 같은 버전의 `stable`이 이미 있으면 `RUSTUP_TOOLCHAIN=stable`로 그대로 검사할 수 있다(환경 변수가 toml보다 앞선다) — 다시 받지 않아도 된다.

### 필수 상태 검사
- 규칙(Rulesets) → 운영 갈래 → "Require status checks to pass" → PR에서 도는 빌드·시험 잡 이름. 혼자 하는 레포면 본인은 우회 목록에 두되, 기본 흐름은 막히게.

## 왜?
고정의 목적은 "리뷰한 코드가 실행되는 코드"가 되게 하는 것이다. 태그·`stable`은 리뷰한 뒤에도 바뀐다. SHA·버전 숫자는 바뀌지 않고, 바꿀 때는 커밋(PR)으로 보인다 — 그래서 변경이 기록되고 되돌릴 수 있다. 대가는 올리기 수고인데, 그것은 Dependabot·toml 한 줄로 줄인다.

## 함정
- dtolnay/rust-toolchain의 `@stable`·`@1.89.0` 갈래 커밋은 master 역사 밖이라 SHA로 고정하면 사라질 수 있다 — master의 SHA + `toolchain` 입력.
- 로컬 묶은 액션(`uses: ./.github/actions/x`)은 checkout 뒤에만 쓸 수 있다.
- Dependabot의 `target-branch`를 마일스톤 갈래로 두면 갈래가 바뀔 때 같이 바꿔야 한다(안 바꾸면 없는 갈래로 PR을 못 만든다).
- cargo 의존성을 Dependabot 올리기에 넣으면 라이선스 고지 파일·복사해 둔 JS 번들·패치한 크레이트처럼 "같이 움직여야 하는 것"이 PR에 안 따라온다 — 그런 레포는 취약점 알림만 켠다.
- 고정은 액션 코드만 막는다. 러너 이미지·`npx 패키지@메이저`·`curl | sh`는 따로다.

## 실행 결과
nail-under-the-roots `5689511`(2026-11-04):
- 통과: deploy-web(fmt·clippy·test·wasm 빌드 + 개발판 배포 확인), smoke-web(개발판 시나리오 + 운영판 타이틀), build-android, build-desktop의 Windows·Linux — 묶은 액션(SHA 고정 dtolnay + `toolchain: 1.99.1` + rust-cache)이 리눅스·윈도 러너에서 그대로 돌았다.
- 못 돌림: macOS 러너 잡 둘(PC 묶음의 Mac판·iOS) — GitHub Actions 장애(상태 페이지 "Incident with Actions and Pages")로 러너를 못 받아 두 번 다 단계 하나 없이 취소("The job was not acquired by Runner of type hosted even after multiple attempts"). macOS에서의 동작은 **확인 못 함**.

## 관련 노트
- [공개 레포에서 배포 파이프라인 지키기](../../guides/protect-deploy-pipeline-in-public-repo.md)
- [Rust → wasm32 빌드 워크플로](rust-wasm-build.md)
- [Node 20 폐기 — 액션을 node24 판으로](node24-action-runtime.md)
