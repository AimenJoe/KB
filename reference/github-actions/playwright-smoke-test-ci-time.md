---
title: GitHub Actions에서 Playwright 연기 시험이 느려질 때 — `--with-deps`의 apt 글꼴과 같은 커밋 두 번 돌리기
type: reference
tags: [github-actions, ci-cd, playwright, testing, web]
status: draft
created: 2026-11-04
updated: 2026-11-10
verified: |
  1차 출처로 확인:
  - 직접 실행(knellroot deploy-web, 2026-11-04, ubuntu-latest = 24.04, playwright@1.47.2):
    `npx playwright install --with-deps chromium`이 apt로 받은 새 패키지는 글꼴뿐이었다(fonts-ipafont-gothic·fonts-wqy-zenhei·
    fonts-freefont-ttf·fonts-unifont·fonts-tlwg-loma-otf·xfonts-cyrillic·xfonts-scalable·xfonts-encodings·xfonts-utils, 21.1MB).
    브라우저가 쓰는 라이브러리(libnss3·libgbm1·libxkbcommon0·libasound2t64·xvfb …)는 모두 "already the newest version".
    그날 apt 미러가 128kB/s라 글꼴 받기만 2분 44초. 브라우저 본체(165MB)는 Playwright CDN에서 약 4초.
    같은 워크플로의 전날 실행(v0.1.1)은 연기 시험 단계 전체가 1분 37초 — 미러 속도에 따라 크게 흔들린다.
  - 직접 실행: 그 배포는 push부터 운영 반영까지 7분. 그중 연기 시험 단계가 5분 8초(설치 약 2분 50초 + 시험 2분), 빌드·검사 전체는 약 1분.
  - 공식 문서(playwright.dev/docs/ci, 2026-11-04 읽음): CI 예시는 `npx playwright install --with-deps`. "Caching browser binaries is not
    recommended" — 캐시 복원이 받기와 비슷하게 걸리고, Linux OS 의존성은 캐시할 수 없다고 적혀 있다. 공식 컨테이너 이미지
    `mcr.microsoft.com/playwright`를 쓰는 방법도 있다.
  - 공식 문서(playwright.dev/docs/docker, 2026-11-04 읽음): 이미지 태그는 `mcr.microsoft.com/playwright:v<버전>-noble`, "browsers and browser system dependencies"가 들어 있고 playwright 패키지는 따로 설치한다.
  - 직접 실행(nail-under-the-roots smoke-web, 2026-11-04, ubuntu-24.04 이미지 20261025.353.1, playwright@1.63.0):
    최근 실행 12개의 "Install Playwright" 단계는 18~41초(잡 전체 4~5분). 한 실행을 로그로 나누면 npm 2초, apt(목록 9.9MB + 같은 글꼴 9개 21.1MB를
    32MB/s로) 약 10초, 브라우저 본체 약 7초 — 미러가 빠른 날은 `--with-deps`가 10초 남짓이다. 잡 시간의 대부분은 시험 자체(약 3분).
  - 직접 실행(같은 레포, 작업 갈래에서 손으로 한 번, run 41851593291): `--with-deps`를 빼고 `npx playwright install chromium`만 해도
    Chromium이 떠서 연기 시험 39개 확인이 모두 통과, 설치 단계 8초. 즉 이 러너 이미지에는 브라우저가 쓰는 OS 라이브러리가 이미 다 있다.
  확인 못 함:
  - 러너 이미지가 바뀐 뒤에도 그대로인지(이미지 버전마다 다를 수 있다 — 깨지면 브라우저가 안 떠서 시험이 크게 실패하므로 조용히 틀리지는 않는다).
  직접 측정(knellroot 0135, 2026-11-10): 헤드리스 시험이 `page.on('console')`에서 `type() === 'error'`만 모았다. 같은 시험 한 판에
    엔진 경고 `geometry() exceeded max drawcall size, clamping`(macroquad `warn!` → 콘솔 warning)이 2,350번 있었는데 "통과"였다 —
    외곽선·그림자가 매 프레임 잘리던 버그. 리눅스 데스크톱 빌드의 stderr에서 처음 보고 찾았다. 고친 뒤 0번.
sources:
  - https://playwright.dev/docs/ci
  - https://playwright.dev/docs/docker
---

# GitHub Actions에서 Playwright 연기 시험이 느려질 때

## 요약
배포 앞에 헤드리스 연기 시험을 두면, 배포 시간은 그 시험의 **가장 느린 외부 다운로드**에 묶인다. ubuntu-latest에서 `playwright install --with-deps chromium`이 실제로 새로 받는 것은 대부분 **글꼴 apt 패키지**다(다국어 웹 페이지용). 캔버스에 자기 글꼴로 그리는 게임에는 필요 없는데, apt 미러가 느린 날에는 이것 하나로 몇 분이 늘어난다. 또 운영 갈래에 올린 커밋이 개발 갈래에서 이미 같은 시험을 통과했다면, 운영 배포 때 다시 돌리는 것은 같은 일을 두 번 하는 것이다.

## 본문
### 어디서 시간이 가는가(재 보기)
- 잡 단계별 시간은 API `GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs`의 `steps[].started_at/completed_at`. 단계 안은 로그 타임스탬프로 나눈다.
- 한 번만 보지 말고 같은 워크플로의 이전 실행 몇 개와 비교한다. 네트워크 다운로드 단계는 날마다 몇 배씩 흔들린다.

### 줄이는 방법(효과가 큰 순)
1. **`--with-deps`를 빼거나 줄인다**: 러너에 라이브러리가 이미 있으면 `npx playwright install chromium`만. 웹 글꼴이 필요 없는 캔버스 게임이면 잃는 것이 없다.
   OS 의존성까지 확실히 해야 하면 공식 이미지 `mcr.microsoft.com/playwright:v<버전>-noble`을 잡의 `container:`로 쓴다(브라우저·OS 의존성이 들어 있고 playwright 패키지만 따로 — 다만 Rust 툴체인 등 다른 단계도 그 안에서 돈다).
2. **같은 커밋을 두 번 시험하지 않는다**: 개발 갈래 → 운영 갈래로 같은 SHA를 올리는 흐름이면, 운영 push에서는 그 SHA의 개발 갈래 시험이 성공했는지만 보고 건너뛴다(직접 운영에 넣은 패치처럼 처음 보는 커밋일 때만 돌린다). 시험이 배포를 막는 구조라면 운영 반영 시간이 그만큼 준다.
3. **시험을 배포와 떼어 놓는다**: 시험을 다른 워크플로(또는 `needs` 없는 잡)로 두면 배포는 기다리지 않는다. 대신 시험이 실패해도 이미 배포된 뒤라는 것을 받아들여야 한다 — 개발 갈래에서 먼저 걸러진다면 괜찮은 거래.
4. 브라우저 캐시는 하지 않는다: 공식 문서가 권하지 않고, 실제로도 본체 받기는 몇 초였다.

## 왜?
- `--with-deps`는 "이 브라우저가 어떤 Linux에서든 웹 페이지를 제대로 그리게"가 목적이라 CJK·태국어 같은 글꼴까지 넣는다. 일반 웹 앱 E2E에는 맞지만, 글자를 직접 그리는 WebGL 게임의 연기 시험에는 목적이 다르다.
- apt는 러너 지역의 공유 미러에서 받는다. Playwright CDN(브라우저 본체)은 빠른데 apt 미러는 느린 날이 있어, 작은 21MB가 165MB보다 오래 걸릴 수 있다.
- 배포 앞의 시험은 "운영에 나가기 전 마지막 확인"인데, 같은 SHA를 이미 같은 시험이 봤다면 새 정보가 없다.

## 함정
- 운영판이 개발 기능을 뺀 빌드라 시험이 개발 빌드를 따로 짓는다면(개발 메뉴로 장면에 들어가는 시험), 그 시험은 **운영 빌드를 보지 않는다** — 그러면 실제로 나가는 빌드는 아무도 띄워 보지 않은 셈이다. 운영 빌드를 따로 조립해 타이틀까지만이라도 띄운다(nail 0277). 건너뛰기를 따질 것은 개발 시나리오 시험뿐이다. → [개발판·운영판 나누기](../../guides/dev-and-release-flavors.md)
- **콘솔 error만 모으면 엔진 경고를 놓친다.** 엔진이 "잘라 냄·대체함·실패해서 건너뜀"을 경고 한 줄로만 알리는 경우가 있다(macroquad: 그리기 호출 용량을 넘긴 기하를 `warn!` 한 줄 찍고 자른다 — 화면에서는 조용하다). warning도 모아 **알려진 잡음 목록 밖이면 실패**하게 하거나, 최소한 종류별 개수를 찍어 늘어나면 보이게 한다. 한 번은 네이티브 빌드를 터미널에서 켜서 stderr를 읽어 보는 것도 싸다.
- 시험 단계를 건너뛸 때 SHA 비교는 "같은 커밋"이어야 한다. 운영 갈래를 PR로 합치면(merge·squash·rebase 모두) 새 커밋이 생겨 SHA가 늘 달라 건너뛰기가 한 번도 걸리지 않는다. 그 흐름에서 같은 내용인지 보려면 커밋이 아니라 **트리 해시**(`git rev-parse HEAD^{tree}`)를 비교해야 한다 — 다만 그만큼 워크플로가 복잡해지니, 시험이 배포를 막지 않는 구조면 그냥 두 번 돌리는 편이 싸다.
- 설치 단계가 길다고 느껴지면 먼저 단계를 나눠 잰다. 미러가 빠른 날은 `--with-deps`가 10초 남짓이라, 연기 시험이 느린 진짜 이유는 시험 안의 고정 대기(`waitForTimeout`)인 경우가 많다.

## 관련 노트
- [WASM 빌드와 JS 번들 — 헤드리스로 웹 빌드 확인](../macroquad/wasm-build.md#헤드리스로-웹-빌드-확인-playwright)
- [Rust → wasm32 빌드 워크플로](rust-wasm-build.md)
- [개발판·운영판 나누기](../../guides/dev-and-release-flavors.md)
