---
title: GitHub Actions의 Node 20 폐기 — 액션을 node24 판으로 올리기
type: reference
tags: [github-actions, ci-cd, node]
status: verified
created: 2026-11-03
updated: 2026-11-03
verified: |
  1차 출처로 확인(2026-11-03, 각 레포 태그의 action.yml·README·CHANGELOG를 raw.githubusercontent.com·git clone으로 읽음):
  - node20인 판: actions/checkout@v4, setup-node@v4, upload-artifact@v4, cache@v4, softprops/action-gh-release@v2.
  - node24인 판: checkout v5~v7.0.1, setup-node v5~v7.1.0, upload-artifact v6~v7.0.2(v5.0.0은 아직 node20),
    cache v5~v6.1.0, action-gh-release v3.0.0~v3.0.3, Swatinem/rust-cache v2(떠 있는 v2 태그가 이미 node24),
    configure-pages v6·deploy-pages v5. upload-pages-artifact v5는 composite이고 안에서 upload-artifact v7.0.0을 부른다.
    dtolnay/rust-toolchain@stable은 composite(Node를 안 씀).
  - 메이저마다 바뀐 것: 아래 표의 글은 각 README의 What's new / Breaking changes와 action-gh-release CHANGELOG에서.
  - 직접 실행(nail-under-the-roots, 2026-11-03): 워크플로 여섯의 액션을 위 최신 메이저로 올리고 release/** push로 CI를 돌림 — 결과는 아래 "직접 해 본 것".
  2차 출처만 있음(GitHub changelog 글은 이 세션에서 github.blog이 막혀 검색 요약으로만 봄):
  - 러너가 2026-06-16부터 node24를 기본으로 쓰고, Node 20은 2026-09-23에 러너에서 지운다(처음 발표는 2025-09-19, 날짜는 편집자 주로 몇 번 바뀜).
  - `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true`로 미리 시험, `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION=true`로 node20에 되돌리기는 지우기 전까지만.
  - node24 액션은 러너 v2.327.1 이상이 필요하다(checkout·setup-node·cache README에도 같은 수 — 이건 1차).
  확인 못 한 것: Node 20 EOL 2026-04-30(Node.js 릴리스 일정 — 이번에 다시 보지 않음). Node 20을 지운 뒤 node20 액션이 경고만 내고 node24로 도는지, 실패하는지.
sources:
  - https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
  - https://github.com/actions/checkout/blob/main/README.md
  - https://github.com/actions/setup-node/blob/main/README.md
  - https://github.com/actions/cache/blob/main/README.md
  - https://github.com/actions/upload-artifact/blob/main/README.md
  - https://github.com/softprops/action-gh-release/blob/master/CHANGELOG.md
---

# GitHub Actions의 Node 20 폐기 — 액션을 node24 판으로 올리기

## 요약
JavaScript 액션은 `action.yml`의 `runs.using`(`node20`·`node24`)으로 어느 Node에서 돌지 정한다. GitHub이 러너에서 Node 20을 걷어 내면서 `using: node20`인 판(`checkout@v4` 등)은 폐기 경고를 낸다. 고치는 법은 워크플로의 `@v4`를 node24 메이저로 올리는 것뿐이다. 우리가 깐 Node(`setup-node`의 `node-version`)와는 상관없다. 올리기 전에 각 메이저의 깨지는 변경이 내 사용법에 걸리는지 본다.

## 본문

### 어느 판이 node24인가 (2026-11-03 기준 최신)
| 액션 | node20 | node24 최신 | 메이저를 올릴 때 볼 것 |
|---|---|---|---|
| actions/checkout | v4 | v7 | v6: `persist-credentials`의 토큰을 `.git/config`가 아니라 `$RUNNER_TEMP`의 따로 된 파일에 둔다. 뒤 단계의 `git push`는 그대로 되지만, Docker 컨테이너 액션 안에서 git 인증을 쓰려면 러너 v2.329.0 이상이 필요하다. v7: `pull_request_target`·`workflow_run`에서 포크 PR 코드를 받는 것을 기본으로 거절한다(`allow-unsafe-pr-checkout: true`). |
| actions/setup-node | v4 | v7 | v5: `cache`를 안 주면 패키지 관리자를 알아서 찾아 캐시를 켠다(끄기 `package-manager-cache: false`). v6: npm 자동 캐시는 `package.json`의 `packageManager`(또는 `devEngines.packageManager`)가 npm일 때만, `always-auth` 입력이 없어졌다. v7: `registry-url`만 주고 `NODE_AUTH_TOKEN`이 없을 때 넣던 가짜 토큰을 없앴다. |
| actions/upload-artifact | v4, v5.0.0 | v7 | v7: `archive: false`로 파일 하나를 압축 없이 올릴 수 있다(기본은 그대로 zip). GHES에서는 여전히 v3.2.2만 된다. |
| actions/cache | v4 | v6 | v5: node24. v6: 속 패키지 메이저 올림·ESM(입력 같음). |
| softprops/action-gh-release | v2(v2.6.2에서 멈춤) | v3 | v3.0.0은 런타임만 node24로. v2는 더 고치지 않는다. |
| Swatinem/rust-cache | — | v2 | 떠 있는 `v2` 태그가 이미 node24. 바꿀 것 없음. |
| dtolnay/rust-toolchain | — | `@stable` | composite. 바꿀 것 없음. |

### 확인하는 법
```sh
# 지금 쓰는 판
grep -rhn "uses: [a-zA-Z]" .github/workflows/ | sed 's/.*uses: //' | sort | uniq -c
# 한 판이 어느 Node에서 도는지 (태그의 action.yml을 직접)
curl -sfL https://raw.githubusercontent.com/actions/checkout/v7/action.yml | grep using:
# 최신 태그
git ls-remote --tags --refs https://github.com/actions/checkout | awk -F/ '{print $NF}' | sort -V | tail -1
```
`using: composite`이면 그 안의 `uses:`도 따라가 본다(upload-pages-artifact v5는 안에서 upload-artifact v7을 부른다).

### 직접 해 본 것 (nail-under-the-roots, 2026-11-03)
워크플로 여섯의 checkout v4→v7, setup-node v4→v7, upload-artifact v4→v7, cache v4→v6, action-gh-release v2→v3을 한 커밋으로 올렸다. 걸리는 변경은 없었다.
- `package.json`이 없으니 setup-node 자동 캐시가 켜지지 않는다.
- 스크립트용 Node는 22 → 26(최신 LTS: nodejs/Release `schedule.json`에서 v26 Lithium이 2026-10-28 LTS, v24는 2026-10-20부터 Maintenance). `lts/*`는 다음 LTS로 조용히 넘어가므로 숫자를 박았다. 쓰는 npm 도구의 `engines`(netlify-cli@23 `>=20.12.2`, playwright@1.63 `>=20`)에 위쪽 제한이 없는 것을 먼저 봤다.
- `pull_request_target`을 쓰지 않는다.
- 뒤 단계의 `git push`(태그)는 v6 뒤에도 그대로 된다.

## 왜?
액션은 러너가 가진 Node 바이너리로 돈다. 그래서 러너가 어떤 Node를 지원하는지가 액션 판의 수명을 정한다. GitHub은 Node가 지원 종료(EOL)에 가까워지면 러너에서 그 Node를 걷어 낸다. Node 20의 EOL은 2026-04다(verified 참고). 액션 쪽은 `using`을 바꾼 새 **메이저**를 낸다. 런타임이 바뀌면 필요한 최소 러너 판이 오르므로, 이는 깨지는 변경으로 친다. 떠 있는 `v4` 태그는 옛 런타임에 머물고, 같은 메이저 안에서 런타임을 올려 주지 않는다. 예외는 Swatinem/rust-cache v2처럼 메이저 안에서 올린 경우다. 그래서 워크플로를 고치지 않으면 경고는 사라지지 않는다.

`setup-node`의 `node-version`(예: `26`)은 **내 스크립트**가 쓰는 Node다. **액션 자신**이 도는 Node와는 별개다. 경고가 나는데 `node-version`만 올리면 아무것도 바뀌지 않는다.

## 함정
- `upload-artifact`는 v5.0.0까지 node20이다. 다른 액션처럼 v5에서 node24가 되지 않으니 v6 이상으로 올린다.
- 셀프 호스트 러너는 v2.327.1 이상이어야 node24 액션이 돈다. ARM32 셀프 호스트는 Node 20 뒤로 지원이 끊긴다(2차).
- 메이저를 한 번에 여럿 건너뛰면 setup-node의 자동 캐시처럼 조용히 동작이 바뀌는 것이 있다. 권한이 높은 워크플로에서는 캐시 오염을 피하려고 `package-manager-cache: false`를 명시하기도 한다(setup-node README 권고).

## 관련 노트
- [Rust → wasm32 빌드 워크플로](rust-wasm-build.md)
- [GitHub Pages에 정적 페이지](pages-static-site.md)
- [버전 올리기 = 릴리스](release-from-version-bump.md)
