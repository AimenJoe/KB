---
title: 버전 올리기 = 릴리스 — CI가 태그를 만들고 빌드를 직접 부르기
type: reference
tags: [github-actions, ci-cd, release, android, rust]
status: verified
created: 2026-10-25
updated: 2026-10-25
verified: |
  1차 출처로 확인(GitHub 문서 원본 github/docs 레포 main, 2026-10-25 — docs.github.com은 세션 프록시가 막아 raw.githubusercontent.com으로 읽음):
  GITHUB_TOKEN이 일으킨 이벤트는 workflow_dispatch·repository_dispatch 말고는 새 워크플로를 만들지 않는다(재귀 방지, data/reusables/actions/actions-do-not-trigger-workflows.md).
  재사용 워크플로 안의 `github` 컨텍스트는 항상 호출한 쪽 것, 호출받은 쪽은 GITHUB_TOKEN 권한을 낮출 수만 있다, 호출·피호출이 같은 concurrency group +
  cancel-in-progress면 서로 취소한다, `github.workflow`는 호출한 쪽 이름(content/actions/reference/workflows-and-actions/reusing-workflow-configurations.md).
  `secrets: inherit`(content/actions/how-tos/reuse-automations/reuse-workflows.md).
  직접 실행(2026-10-25, nail-under-the-roots v0.1.0·v0.1.1·v0.1.2): main push 한 번으로 태그 → APK 빌드 → Release(본문 + APK) 생성, 태그가 이미 있으면 건너뜀,
  softprops/action-gh-release@v2가 `body_path` 뒤에 `generate_release_notes`의 "Full Changelog"를 붙임, 막 만든 Release가 "not yet discoverable"이면 스스로 재시도함(로그).
  `env!("CARGO_PKG_VERSION")` + `option_env!("GITHUB_SHA")`로 타이틀에 "v0.1.2 · <커밋 7자>"가 찍히는 것을 웹 배포에서 확인.
  확인 못 함: 태그 push가 프록시에서 거부되는 이유(세션 환경의 정책으로만 관찰).
sources:
  - https://github.com/github/docs/blob/main/data/reusables/actions/actions-do-not-trigger-workflows.md
  - https://github.com/github/docs/blob/main/content/actions/reference/workflows-and-actions/reusing-workflow-configurations.md
  - https://github.com/github/docs/blob/main/content/actions/how-tos/reuse-automations/reuse-workflows.md
  - https://github.com/softprops/action-gh-release
---

# 버전 올리기 = 릴리스

## 요약
태그를 사람이(또는 세션이) push하지 않고, **버전 숫자와 릴리스 본문 파일을 main에 올리면 CI가 태그를 만들고 빌드·Release까지** 한다. 핵심 함정은 하나다. **`GITHUB_TOKEN`으로 만든 태그는 `on: push: tags`를 깨우지 않는다.** 그래서 태그를 만든 워크플로가 빌드 워크플로를 `workflow_call`로 직접 부르고, 태그 이름을 입력으로 넘긴다.

## 본문

### 흐름
```
main push (Cargo.toml / docs/releases/** 바뀜)
 └ release.yml / job tag
     버전 읽기 → docs/releases/v<버전>.md 없으면 끝 → 태그 이미 있으면 끝
     → git tag -a v<버전> && git push (GITHUB_TOKEN, contents: write)
 └ release.yml / job apk  (needs: tag, if: 태그를 만들었을 때만)
     uses: ./.github/workflows/build-android.yml
     with: { release_tag: v<버전> }   secrets: inherit   permissions: contents: write
       └ 빌드 → softprops/action-gh-release (tag_name·body_path = 입력값)
```
- 본문 파일이 "릴리스 스위치"다. 버전만 올리고 본문이 없으면 아무 일도 없다 → 실수로 올린 버전이 릴리스가 되지 않는다.
- 태그가 이미 있으면 건너뛴다 → 같은 커밋을 다시 push하거나 `workflow_dispatch`로 다시 돌려도 안전하다.

### 빌드 워크플로 쪽
```yaml
on:
  push: { tags: ['v*'] }          # 사람이 태그를 push해도 여전히 동작
  workflow_call:
    inputs: { release_tag: { type: string, required: true } }
concurrency:
  group: android-${{ inputs.release_tag || github.ref }}   # 호출한 쪽과 다른 그룹
...
- if: startsWith(github.ref, 'refs/tags/v') || inputs.release_tag != ''
  uses: softprops/action-gh-release@v2
  with:
    tag_name:  ${{ inputs.release_tag || github.ref_name }}
    body_path: docs/releases/${{ inputs.release_tag || github.ref_name }}.md
    files: target/.../*.apk
    generate_release_notes: true   # 본문 뒤에 비교 링크·PR 목록
```
- `workflow_call`로 불리면 `github.ref`는 **호출한 쪽 것(refs/heads/main)**이다. 태그 조건을 `github.ref`로만 보면 Release 단계가 건너뛰어진다 → 입력으로 받는다.
- 권한은 호출한 job의 `permissions`가 상한이다. 피호출 쪽에서 `contents: write`를 올릴 수 없다.

### 앱 안에 버전 찍기 (Rust)
- `env!("CARGO_PKG_VERSION")`은 Cargo.toml 버전이라 릴리스와 저절로 맞는다. 화면에 숫자를 따로 적지 않는다.
- Actions 러너는 `GITHUB_SHA`를 환경 변수로 준다. `option_env!("GITHUB_SHA")`(로컬 빌드에선 `None`)로 앞 7자를 붙이면 웹 빌드가 어느 커밋인지 보인다.

## 왜?
- GitHub가 `GITHUB_TOKEN` 이벤트로 새 워크플로를 만들지 않는 것은 **재귀 방지**다. 워크플로가 push했더니 push 워크플로가 또 돌고… 를 막는다. PAT으로 태그를 push하면 태그 워크플로가 깨지만, 그러면 토큰 관리가 하나 늘고 그 토큰이 할 수 있는 일이 넓어진다. 같은 워크플로 안에서 직접 부르면 토큰이 필요 없다.
- 버전·본문·코드가 **한 커밋**에 들어가므로 "어느 커밋이 v0.1.2인가"가 흔들리지 않는다. 태그를 손으로 다는 절차는 사람이 빠뜨리거나 다른 커밋에 다는 일이 생긴다.
- 태그 push를 받지 않는 환경(일부 git 프록시, 권한이 좁은 봇)에서도 릴리스할 수 있다.

## 함정
- 호출·피호출 워크플로에 **같은 concurrency group + `cancel-in-progress: true`**를 쓰면 서로를 취소한다. `${{ github.workflow }}`도 피호출 쪽에선 호출한 쪽 이름이라 같은 값이 된다 → 그룹에 태그 이름을 넣어 다르게.
- `paths` 필터는 태그 push에 적용되지 않는다(Android 가이드 참조). 반대로 release.yml의 `paths`에 본문 폴더를 빼먹으면 "본문만 나중에 올린" 경우 릴리스가 안 된다.
- main push 하나가 일반 빌드(브랜치용)와 릴리스 빌드를 **둘 다** 돌린다. 분량이 작으면 그냥 두고, 크면 일반 빌드에 `paths-ignore`나 조건을 둔다.
- Android는 **versionCode를 매번 올리고 같은 키로 서명**해야 덮어 설치된다. 디버그 키를 Actions 캐시에만 두면 7일 뒤 사라질 수 있다 → [Android APK 가이드의 함정](../../guides/macroquad-android-apk-github-actions.md#함정).

## 관련 노트
- [macroquad를 GitHub Actions에서 Android APK로](../../guides/macroquad-android-apk-github-actions.md)
- [Rust → wasm32 빌드 워크플로](rust-wasm-build.md) — concurrency
- [macroquad WASM → Netlify](../../guides/macroquad-wasm-netlify-github-actions.md)
