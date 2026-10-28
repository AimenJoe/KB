---
title: 인디 게임 공식 페이지 — 무엇을 싣고, 도트 게임답게 움직이기
type: guide
tags: [gamedev, marketing, static-site, pixel-art, css]
status: draft
created: 2026-10-27
updated: 2026-10-28
verified: |
  1차 출처로 확인(2026-10-27, nail-under-the-roots 0155 직접 실행, 헤드리스 Chromium):
  - 16px 칸 가로 띠 + CSS 변수(--n 칸 수, --s 칸 크기)로 background-size·steps(var(--n))·keyframes의
    background-position-x: calc(var(--n) * var(--s) * -1)이 Chromium에서 돈다(칸 수가 다른 띠를 한 규칙으로).
  - Playwright fullPage 스크린숏은 loading="lazy" 그림을 불러오지 않아 빈 칸으로 찍힌다. 먼저 끝까지 스크롤하면 찍힌다.
  - Playwright recordVideo(VP8 webm, 25fps)는 도트 그림을 흐리게 뭉갰다 → 소개 영상으로 쓰지 않았다.
  1차 출처로 확인(2026-10-28, nail-under-the-roots 0228 직접 실행, Playwright 1.63 + 헤드리스 Chromium swiftshader):
  - page.clock.install() 뒤 clock.runFor(1000/30) + 스크린숏을 되풀이하면 macroquad(WASM, requestAnimationFrame·Date.now)
    게임이 칸마다 정확히 1/30초씩 나아간다 → 30fps 고른 무손실 칸. 키 입력(keyboard.down/up)은 시계와 상관없이 들어간다.
  - 960×540(3배) 칸을 ffmpeg libx264 -tune animation -crf 16 -pix_fmt yuv420p로 묶으면 확대 비교에서 원본과 구분되지 않았다
    (12초 1.6 MB, crf 12 = 2.1 MB, crf 20 = 1.1 MB).
  - 브라우저 셋을 동시에 돌리면 칸당 4초 넘게 느려지고 게임 메뉴 키를 놓쳤다. 하나씩이면 480칸에 약 1분.
  - video[data-src] + IntersectionObserver로 화면 가까이 와서야 src를 넣고 재생하면 첫 화면 무게가 그대로다(헤드리스에서 src 없음 → 스크롤 뒤 재생 확인).
  - 가로 넘침 검사(scrollWidth = innerWidth, 화면 밖으로 나간 요소 목록)를 1440·390·320px, 한국어·영어로.
  2차 출처만 있음: 페이지에 실을 것(첫 화면: 무슨 게임·한 줄 소개·어디서 하나, 트레일러를 크게, 기능 목록,
  UI·메뉴가 아닌 좋은 순간의 스크린숏, 팩트시트·로고·연락처, 낡지 않게 고치기) — 프레스킷 도구 회사·마케팅 블로그 글.
  presskit()(Rami Ismail, Vlambeer)이 팩트시트·설명·역사·기능·영상·그림·로고·수상·연락처 칸의 원형이라는 것도 2차.
sources:
  - https://presskit.gg/field-guides/developer-website-guide
  - https://presskit.gg/blog/indie-game-press-kit-guide
  - https://www.gamedeveloper.com/business/presskits-the-what-and-the-why
  - https://dopresskit.com/
  - https://impress.games/blog/biggest-indie-game-press-kit-mistakes
---

# 인디 게임 공식 페이지

## 요약
첫 화면이 "무슨 게임인지, 어디서 하는지"에 바로 답하게 한다. 그 아래에 볼거리(기능·스크린숏), 할 것(해 보기·조작), 기자·친구가 찾는 것(팩트시트·연락·크레딧)을 둔다. 꾸미기는 게임의 한 줄 이야기를 페이지 구조로 옮기면 가장 싸고 어울린다(예: 땅속으로 내려가는 게임 → 스크롤하면 내려가는 페이지). 도트 게임은 게임 그림과 스프라이트를 그대로 키워 쓰고 CSS로 움직인다.

## 본문
### 싣는 것(관례, 2차)
| 칸 | 내용 |
|---|---|
| 첫 화면 | 대표 그림(키 아트·타이틀), 이름, 한 줄 소개, **해 보기 단추**(브라우저·스토어·APK), 무료·장치 같은 짧은 사실 |
| 볼거리 | 핵심 동사 3~4개(키캡과 함께), 지대·스테이지, 캐릭터, 스크린숏(메뉴·게임오버 말고 좋은 순간) |
| 영상 | 트레일러나 짧은 반복 클립이 가장 힘이 세다. 없으면 스프라이트 움직임으로 대신한다. 사람이 녹화하기 전에는 가짜 시계로 찍은 클립(아래) |
| 해 보기 | 플랫폼별 설치, 기본 조작 표, 저장 위치 |
| 팩트시트 | 장르·플랫폼·가격·언어·만든 곳·상태 |
| 자주 묻는 것 | 저장·패드·폰·난이도 |
| 소식·다음 | 릴리스에서 읽어 오기, 다음 버전 한 줄(줄거리는 흐리게) |
| 크레딧 | 에셋·음악·폰트·생성 그림 고지(라이선스 기록과 맞춘다) |

### 도트 게임답게 움직이기
- **그림은 그대로 키운다**: `image-rendering: pixelated`. 큰 바탕은 `object-fit: cover` + `object-position`으로 주인공 쪽을 남긴다. 폰에서는 덮지 말고 16:9로 두고 글을 아래로.
- **스프라이트 띠**: 16px 칸을 가로로 이은 PNG를 빌드 스크립트로 잘라 둔다. CSS 하나로 칸 수가 다른 띠를 다 돌린다.
  ```css
  .sprite { --s: 48px; width: var(--s); height: var(--s);
    background: var(--sp) 0 0 / calc(var(--n) * var(--s)) var(--s) no-repeat;
    image-rendering: pixelated; animation: frames calc(var(--n) * .16s) steps(var(--n)) infinite; }
  @keyframes frames { to { background-position-x: calc(var(--n) * var(--s) * -1); } }
  ```
  `<span class="sprite" style="--sp: url(img/sp_mole.png); --n: 4">`. 걷기는 위 칸 넘기기 + `left`를 옮기는 둘째 애니메이션.
- **이야기를 스크롤로**: 층(section)마다 바탕을 짙게 하고, 층 사이에 계단 가장자리를 둔다. 고정 눈금에 주인공이 스크롤 비율만큼 내려가고, 화면 가운데 층 이름이 밝아진다(`scroll` + `requestAnimationFrame` 한 번).
- **반딧불·먼지 같은 분위기 입자**: 스크립트로 몇 개만 뿌리고(자리·주기·지연을 하나씩 다르게) CSS로 떠다니게 한다.
- **가짜 시계로 찍는 게임 클립**: 실시간 녹화는 도트를 뭉개거나 칸 간격이 고르지 않다. 브라우저 게임이면 Playwright `page.clock.install()`로 시계를 멈추고 `clock.runFor(1000/30)` → 스크린숏을 되풀이해 고른 무손실 칸을 얻는다(requestAnimationFrame·Date를 쓰는 엔진이면 그대로 따라온다). 대본대로 누르는 손은 적을 못 보니 찍기 전용 빌드에서 피해를 끄고, 페이지에 그렇다고 적는다. 묶기는 H.264 `-tune animation -crf 16`, 소리 없이 `muted loop playsinline`, 화면 가까이 와서야 받는다(IntersectionObserver), 움직임 줄이기면 재생 단추만.
- **움직임 줄이기**: `prefers-reduced-motion: reduce`면 반복 애니메이션을 끄고 제자리에 세운다.

## 왜?
- 방문자는 첫 화면에서 떠날지를 정한다. "무엇·어디서"가 바로 안 보이면 아래 내용은 읽히지 않는다.
- 게임의 한 줄 이야기를 페이지 구조로 옮기면, 새 그림 없이도 페이지가 게임과 같은 결이 된다. 장식이 아니라 내용을 따라 내려가게 된다.
- 스프라이트를 직접 움직이면 이미지·영상보다 가볍고 선명하다(도트가 뭉개지지 않는다). 게임 에셋이 바뀌면 빌드 스크립트 한 번으로 따라간다.

## 함정
- 헤드리스 녹화(Playwright `recordVideo`)는 압축이 세서 도트가 흐려진다. 가짜 시계로 한 칸씩 찍어 직접 묶거나, 실제 기기에서 화면 녹화(무손실 또는 높은 비트레이트, 정수 배율).
- 헤드리스 찍기를 여러 개 동시에 돌리기 → 소프트웨어 GPU(swiftshader)가 서로 느려져 키 입력을 놓치고 엉뚱한 화면이 찍힌다. 하나씩.
- `fullPage` 스크린숏으로 확인할 때 lazy 그림은 빈 칸이다. 끝까지 스크롤한 뒤 찍는다.
- 글을 바꾸면 줄인 픽셀 글꼴(페이지 글자만 남긴 서브셋)을 다시 만든다. 빠진 글자는 대체 글꼴로 섞여 나온다.
- 낡은 숫자("v0.2", 옛 크레딧)를 페이지에 박지 않는다. 버전·소식은 릴리스에서 읽고, 크레딧은 라이선스 기록과 같이 고친다.
- 스크린숏의 HUD 언어는 하나뿐이다. 다른 언어 페이지에서는 그렇다고 받아들이거나 언어별로 찍는다.

## 관련 노트
- [GitHub Pages에 정적 페이지 올리기](../reference/github-actions/pages-static-site.md) — 배포·릴리스에서 읽는 값·글꼴 줄이기
- [그림 못 그려도 도트 게임 만들기](pixel-art-without-an-artist.md) — 에셋 크레딧·타이틀 키 아트
- [작곡가·음향 담당 없이 게임 소리 넣기](game-audio-without-a-composer.md) — 음악 크레딧
