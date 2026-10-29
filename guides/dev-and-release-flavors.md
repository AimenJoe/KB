---
title: 운영판과 개발판을 갈라 내보내기 — 마일스톤 갈래, Cargo 기능, 따로 열고 따로 깔기
type: guide
tags: [ci, deploy, github-actions, netlify, android, rust, gamedev]
status: draft
created: 2026-10-28
updated: 2026-10-29
verified: |
  1차 출처로 확인:
    - 직접 실행(nail-under-the-roots 0227, 2026-10-28): release/v0.6에 쌓인 고침·그림을 main에 합쳐 v0.5.1로 냈다(release·deploy-web·build-android·pages·build-ios·smoke-web 모두 성공, Release에 APK).
    - 직접 실행(nail-under-the-roots 0193, 2026-10-28): release/v0.5 push에서 Netlify `--alias=dev` 배포 뒤 별칭 주소의 build.txt가 그 커밋 SHA였다(deploy-web 157·159 성공). 같은 push의 build-android가 패키지 `io.github.aimenjoe.nail.dev`, 이름 "Naïl dev"인 APK를 지어(aapt2 badging) 미리 보기 Release `dev`에 올렸다(351). main은 `--no-default-features`로 지었고 APK가 개발 판보다 작았다(17 968 002 vs 17 984 386 바이트).
    - cargo-quad-apk 소스(rev d411c8f): `package_name`으로 Java 패키지 경로·`TARGET_PACKAGE_NAME`·JNI 함수 이름(`Java_<패키지>`)을 함께 짓는다. `build` 명령은 cargo의 `--features`/`--no-default-features`를 받는다(`arg_features`, `compile_options`).
    - GitHub API: `releases/latest`와 위 노트의 site.js 필터가 prerelease를 건너뛴다(Release `dev`가 prerelease=true로 잡힘).
  2차 출처(포럼)만 있음:
    - 같은 `--alias`를 다시 쓰면 그 주소가 가장 새 배포를 가리킨다는 답과, 옛 배포에 머문다는 답이 엇갈린다(Netlify Answers). 공식 CLI 문서는 이 세션 네트워크에서 열리지 않았다. 그래서 배포 뒤 확인 단계를 둔다 — 한 번은 새 배포를 가리켰다.
  확인 못 함: 별칭 배포의 검색 색인(noindex 헤더가 자동으로 붙는지). 그래서 HTML에 robots 메타를 직접 넣는다.
sources:
  - https://answers.netlify.com/t/netlify-cli-alias-urls-not-found/17831/6
  - https://answers.netlify.com/t/latest-branch-deploy-url-always-pointing-to-the-old-permalink-from-a-stale-deploy/160152
  - https://github.com/not-fl3/cargo-quad-apk
  - https://docs.github.com/en/rest/releases/releases#get-the-latest-release
---

# 운영판과 개발판을 갈라 내보내기

## 요약
1인 게임에서 큰 마일스톤을 만드는 동안 운영 중인 판을 지키려면 세 가지를 함께 가른다. **갈래**(main = 운영, `release/vX.Y` = 개발판), **빌드 기능**(운영판은 개발 기능을 빼고 짓는다), **나가는 자리**(주소·패키지·내려받기를 달리해 저장이 섞이지 않게). 마지막 것이 빠지면 개발판을 여는 순간 운영판 기록을 덮는다.

## 본문
### 갈래
- `main` = 운영판, 패치만. `release/vX.Y` = 마일스톤 모음. 작업 브랜치는 release로 합친다.
- 패치는 main에 넣고 release로도 합친다(main → release). 거꾸로(release → main)는 마일스톤을 닫을 때 한 번.
- 마일스톤 범위가 바뀌어 release에 쌓인 것이 고침·그림뿐이면, 닫지 않고 **release → main을 패치 버전으로** 내도 된다(nail-under-the-roots 0227: v0.6을 오래 걸리는 큰 기능 하나로 바꾸며 개발판 고침을 v0.5.1·v0.5.2로 냈다 — 두 갈래가 같아지고, 다음 큰 것은 release에서 시작). 이때도 버전 규칙(마이너 = 마일스톤)은 그대로라 버전은 패치만 올린다.

### 빌드 기능(Cargo feature)
- 개발 메뉴·검사 도구를 `dev` 기능 뒤에 두고, 로컬 편의를 위해 `default = ["dev"]`로 두되 **운영 빌드는 CI가 `--no-default-features`**로 짓는다. 갈래는 워크플로 한 단계에서 `GITHUB_REF`로 정해 `$GITHUB_ENV`에 `FEATURES`를 적는다.
- clippy를 **두 갈래 다** `-D warnings`로 돌린다. 처음 돌리면 `cfg(feature)` 안에서만 쓰이던 것이 죽은 코드로 걸린다(메뉴 장면 변종, 검사용 함수).
- 연기 시험이 개발 메뉴로 장면에 들어간다면 그 시험만은 개발 빌드로 돈다(나가지 않는 빌드).

### 따로 열기 — 웹
- Netlify(CLI 업로드 모델): 같은 사이트에 `netlify deploy --alias=dev`(`--prod` 없이). 주소 `dev--<사이트>.netlify.app`. 오리진이 달라 localStorage가 운영판과 갈린다.
- 배포 뒤 확인: `dist/build.txt`에 커밋 SHA를 써 두고, 별칭 주소에서 읽어 비교 — 다르면 CI 실패. `--json` 출력의 `deploy_url`이 별칭 주소다.
- 개발판 HTML에 `<meta name="robots" content="noindex, nofollow">`와 탭 이름 표시.

### 따로 깔기 — Android·iOS
- Android: CI 안에서만 `package_name`을 `….dev`, 이름을 "… dev"로 바꿔 짓는다. 다른 패키지라 운영 앱 옆에 깔리고 앱 폴더도 따로다.
- **앱 코드에 패키지 이름이 박혀 있으면 깨진다**(예: 기록 폴더 `/data/data/<패키지>/files`). 실행 중 프로세스 이름(`/proc/self/cmdline` 첫 칸 = 패키지)에서 읽고, 아는 이름이 아니면 운영 이름으로.
- iOS: `CFBundleIdentifier`·표시 이름만 바꿔 아티팩트로.

### 내려받기 자리
- 미리 보기(prerelease) Release 하나(`dev`)를 계속 갈아 끼운다: `git tag -f dev $SHA && git push -f origin refs/tags/dev`, `gh release create/edit --prerelease`, `gh release upload … --clobber`. 주소가 고정된다(`releases/download/dev/<파일>`).
- `releases/latest`는 prerelease를 건너뛴다. 릴리스 목록을 읽는 페이지는 prerelease를 거르고, 목록을 넉넉히 받아 거른 뒤 자른다(그러지 않으면 소식 칸 하나를 먹는다).
- 태그 이름이 `v*` 같은 릴리스 트리거 패턴에 걸리지 않게 한다.

## 왜?
- **반쯤 된 것이 운영판에 섞이지 않게** — 갈래가 막는다.
- **운영판에서 길을 건너뛰는 도구를 치운다** — 개발 메뉴는 기록을 꼬이게 하고 첫인상을 흐린다. 빌드 기능이 막는다.
- **만드는 사람이 운영판과 개발판을 나란히 본다** — 저장이 주소·패키지에 묶이니, 둘을 다르게 하면 따로 저장된다. 이것이 빠지면 앞의 둘을 해도 개발판을 여는 순간 운영 기록이 덮인다.

## 함정
- `GITHUB_TOKEN`으로 민 태그는 다른 워크플로를 깨우지 않는다(그래서 `dev` 태그 이동이 빌드를 다시 부르지 않는다 — 원하는 대로). 반대로 그 태그로 무언가를 돌리고 싶으면 `workflow_call`.
- `paths` 필터가 있는 워크플로는 **새 브랜치를 처음 push할 때** 돌지 않을 수 있다(이 레포의 첫 release/v0.5 push에서 경로 필터 없는 deploy-web만 돌았다). 첫 개발판을 바로 보려면 수동 실행하거나 다음 커밋을 기다린다.
- 같은 갈래에 연달아 push하면 `concurrency … cancel-in-progress`로 앞 실행이 취소된다. 확인은 가장 새 커밋의 실행으로.

## 관련 노트
- [CI에서 netlify-cli로 배포](../reference/netlify/deploy-from-ci.md) — `--alias`, Git CD와 섞지 않기
- [버전 올리기 = 릴리스](../reference/github-actions/release-from-version-bump.md)
- [Android APK 빌드](macroquad-android-apk-github-actions.md) — 덮어 설치 = 같은 키 + 큰 versionCode
