---
title: "웹 게임을 PWA로: 설치·오프라인·전체 화면·가로 잠금(Chrome·Android·iPhone)"
type: reference
tags: [web, pwa, service-worker, manifest, fullscreen, orientation, ios, android, netlify, wasm]
status: draft
created: 2026-11-02
updated: 2026-11-07
verified: |
  2026-11-05 더함: localStorage·서비스 워커 캐시가 출처(scheme+host+port)마다 따로라는 것은 웹 표준의 동일 출처 규칙(MDN Web Storage·Same-origin policy) — 옮겨 본 실험은 하지 않음.
  1차 출처로 확인:
  - Chrome의 설치 조건에서 fetch 처리기 요구가 빠진 것(모바일 108·데스크톱 112), 자동 설치 안내(beforeinstallprompt)는 여전히 처리기가 있어야 한다는 것 — Chrome for Developers 블로그.
  - WebKit의 ScreenOrientation lock은 전체 화면 API가 있어야 돈다 — WebKit Bugzilla 257695.
  - 직접 실행(헤드리스 Chromium, Playwright, 2026-11-02): 매니페스트·아이콘 응답, 서비스 워커 activated, 네트워크를 끊은 두 번째 로드가 캐시로 뜬다, 터치 세로 화면에서 회전 안내가 뜬다. (nail-under-the-roots `tools/test/smoke.js`). 같은 틀을 둘째 게임 knellroot에 옮겨 2026-11-05 다시 통과(`tools/test/pwa.js` — 캐시 이름 = 빌드 아이디, wasm 미리 담김, 오프라인 다시 읽기). 2026-11-07 knellroot 0082: 세로 폰 화면에서 회전 안내가 덮이고, 누르면 잠금 시도 → 헤드리스는 잠금이 안 돼 0.7초 뒤 세로로 계속(`tools/test/touch.js`).
  - 직접 실행(사람, iPhone 실기, 2026-11-02): 홈 화면에 추가한 앱은 Safari 탭과 localStorage가 따로다 — Safari에서 하던 기록이 따라오지 않는다.
  2차 출처(포럼/블로그)만 있음:
  - iPhone Safari에 요소 전체 화면 API가 없다(iPad는 접두어판), orientation.lock 미지원(26.5까지) — caniuse·firt.dev·Apple 포럼.
  - Android Chrome에서 전체 화면 안의 orientation.lock('landscape')가 되고, 설치 앱이 매니페스트 orientation을 따른다.
  확인 못 함:
  - iOS 홈 화면 앱이 매니페스트 orientation을 따르는지. Android 설치 앱이 브라우저 탭과 기록을 함께 쓰는지(같은 출처라 그럴 것으로 봄).
sources:
  - https://developer.chrome.com/blog/update-install-criteria
  - https://bugs.webkit.org/show_bug.cgi?id=257695
  - https://caniuse.com/wf-screen-orientation-lock
  - https://caniuse.com/screen-orientation
  - https://firt.dev/notes/pwa-ios/
  - https://developer.apple.com/forums/thread/133248
---

# 웹 게임을 PWA로: 설치·오프라인·전체 화면·가로 잠금

## 요약
정적 호스트에 올린 WASM 게임을 "홈 화면에 추가 → 주소창 없이·오프라인에서도" 돌게 하는 최소 묶음은 **매니페스트 + 아이콘 + 서비스 워커 + 캐시 헤더**다. 가로 잠금과 전체 화면은 **Android·데스크톱 Chrome에서만** 기대하고, iPhone은 "홈 화면에 추가" 안내와 세로일 때의 회전 안내로 메운다. 파일 이름에 해시가 없는 빌드라면 서비스 워커 캐시 이름에 **빌드 SHA**를 넣는 것이 갱신의 열쇠다.

## 본문

### 1. 매니페스트(`manifest.webmanifest`)
- `name`·`short_name`·`start_url: "./"`·`scope: "./"`·`display: "fullscreen"`(못 하면 브라우저가 standalone으로 내린다)·`orientation: "landscape"`·`background_color`/`theme_color`(로딩 화면 색).
- `icons`: 192·512 + `purpose: "maskable"` 512(안전 영역 약 80%). iPhone은 매니페스트 아이콘 대신 `<link rel="apple-touch-icon">`(180)을 본다.
- 개발판을 같은 기기에 나란히 깔려면 `id`와 이름을 다르게(CI에서 바꿔 넣는다).

### 2. 서비스 워커
- **캐시 이름 = 빌드 SHA**(`nail-<sha>`): CI가 `sw.js`의 자리표시를 배포 SHA로 바꾼다 → 배포마다 `sw.js` 바이트가 바뀌어 새 워커가 깔리고, `activate`에서 옛 이름의 캐시를 지운다.
- 설치 때 핵심 파일만 미리 받는다(페이지·JS·wasm·그림·글꼴·효과음). 큰 음악은 들을 때 받아 담는다.
- 페이지(`/`·`index.html`)·`build.txt`·매니페스트는 **네트워크 먼저**, 실패하면 캐시. 나머지는 **이 판 캐시 먼저**.
- `skipWaiting()`을 쓰지 않는다: 실행 중인 게임에 새 판 파일이 섞이지 않게, 새 판은 다음 실행부터.
- 등록은 https(또는 localhost)에서만, PR 미리 보기 주소에는 걸지 않는다(옛 워커가 남아 헷갈린다).

### 3. 헤더(Netlify `_headers` 예)
- `sw.js`·`index.html`·`/`·매니페스트는 `Cache-Control: no-cache`(늘 다시 확인). 매니페스트 Content-Type은 `application/manifest+json`으로 박아 둔다.
- 해시 없는 파일에 immutable·긴 max-age를 주지 않는다([CI에서 netlify-cli로 배포](../netlify/deploy-from-ci.md)의 캐시 함정과 같은 이유).

### 4. 전체 화면·가로
| 환경 | 요소 전체 화면 | orientation.lock | 할 일 |
|---|---|---|---|
| 데스크톱 Chrome | 됨 | 해당 없음 | 설정에 "전체 화면" 줄 |
| Android Chrome(탭·설치 앱) | 됨 | 전체 화면 안에서 됨 | 사용자 입력에서 `documentElement.requestFullscreen()` → `screen.orientation.lock('landscape')` 시도, 실패는 조용히 |
| iPhone Safari·홈 화면 앱 | 없음 | 없음 | 그 줄을 숨기고 "홈 화면에 추가하면 주소창 없이" 안내 |
- 지원 여부는 `document.fullscreenEnabled`로 묻고, 지원할 때만 UI를 보인다.
- 터치 기기(`pointer: coarse`)가 세로면 글 없는 회전 픽토그램을 덮고 게임을 자동 일시정지 — 강제하지 않고 탭하면 그대로 세로로.
- 회전 안내를 누를 때 전체 화면을 쓸 수 있으면(Android) **전체 화면 + 가로 잠금을 먼저 시도**하고, 잠시(0.7초) 뒤에도 세로면 안내를 걷는다 — 잠금을 거절하는 브라우저(헤드리스 Chromium이 그랬다)에서 플레이어가 안내에 갇히지 않게. 매니페스트 `orientation`은 설치 앱만 따르니, 브라우저 탭의 "가로가 기본"은 이 안내 + 첫 사용자 입력에서의 잠금이 전부다(knellroot 0082).

### 5. 저장소
- 웹 기록(localStorage)은 출처마다 따로다. 운영·개발판·PR 주소는 출처가 달라 서로 안 섞인다.
- **iPhone 홈 화면 앱은 Safari와 저장소가 따로다**(실기 확인). 브라우저에서 하던 기록을 옮기려면 내보내기·가져오기 같은 별도 장치가 필요하다 — 안내만 할지 정해 둔다.

## 왜?
- 해시 없는 빌드에서 갱신을 보장하는 유일하게 싼 방법이 "워커 파일 자체가 배포마다 바뀌게" 하는 것이다. 브라우저는 `sw.js` 바이트가 바뀌어야 새 워커를 깐다.
- `skipWaiting`을 빼는 이유: 게임은 실행 중에도 파일(음악 등)을 늦게 받는다. 중간에 워커가 바뀌면 옛 wasm과 새 에셋이 섞일 수 있다.
- iPhone 가로 잠금은 WebKit이 잠금을 전체 화면 API에 묶어 두었고 iPhone에는 그 API가 없어서 막혔다 — 우회 대신 안내로 처리하는 것이 유지 비용이 적다.

## 함정
- **웹 게임의 주소(도메인)를 옮기지 않는다.** localStorage 기록·설치한 PWA·서비스 워커 캐시는 출처(scheme+host+port)마다 따로라, 새 도메인으로 옮기면 기존 플레이어에게는 기록이 사라진 것처럼 보인다. 회사·소개 페이지만 새 도메인으로 두고 게임은 처음 주소에 남기거나, 옮겨야 하면 기록 내보내기·가져오기를 먼저 만든다.
- 서비스 워커를 PR·임시 주소에 걸면 그 출처에 옛 캐시가 남아 "고쳤는데 안 바뀐다"가 된다.
- `index.html`을 캐시 먼저로 두면 새 배포가 한 번 늦게 보인다(네트워크 먼저로).
- 헤드리스 시험에서 오프라인 재로드는 `context.setOffline(true)` 뒤 `reload`로 본다 — 워커가 activated 된 다음에.
- 매니페스트 `display: fullscreen`만으로는 iPhone에서 주소창이 사라지지 않는다(홈 화면 앱일 때만).

## 관련 노트
- [CI에서 netlify-cli로 배포](../netlify/deploy-from-ci.md) — 헤더·캐시
- [정적 WASM 호스팅](../../concepts/static-wasm-hosting.md)
- [macroquad WASM 빌드·JS 번들](../macroquad/wasm-build.md)
- [운영판과 개발판을 갈라 내보내기](../../guides/dev-and-release-flavors.md)
- [게임패드와 입력 현황](../macroquad/gamepad-and-android-input.md) — iPad 홈 화면 웹앱에서 실제 키보드가 안 듣는 것(touchstart preventDefault·탭 전 포커스 없음)
