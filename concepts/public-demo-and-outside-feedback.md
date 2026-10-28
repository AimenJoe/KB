---
title: 인디 게임 공개 데모와 바깥 의견 받기
type: concept
tags: [gamedev, playtest, demo, itch-io, solo-dev, roguelite]
status: draft
created: 2026-10-28
updated: 2026-10-28
verified: |
  1차 출처로 확인: itch.io HTML5 올리기 형식(ZIP 맨 위 index.html, 필요한 파일 모두, 이름 대소문자, 한 장짜리 html은 ZIP 없이)은 공식 문서 https://itch.io/docs/creators/html5 (검색 요약으로 읽음, 페이지 원문은 세션 네트워크 사정으로 직접 열지 못함).
  2차 출처(블로그·포럼·3자 정리)만 있음: 무엇을 시험하는지 먼저 정하기, 한 번에 한두 가지, 기술 문제(멈춤·깨짐)가 메커닉을 가린다, 척도 + 고르기 + 자유 글 설문(Wayline 글 여럿). 설문 응답이 적고 버전이 어긋난 사례(itch.io 데브로그 한 편). 로그라이트 데모는 한 바퀴를 온전히·깊이는 잠가서, 20~40분, 완주율 40% 아래면 길다(Zukowski 자료를 옮긴 3자 글 — 원문 howtomarketagame.com은 못 열어 숫자 미확인). 데모는 행사 전에 미리 내기(Zukowski, Unity 블로그 인터뷰).
  직접 해 보지 않음: 설문·완주율 기준을 실제 데모에 적용한 결과는 아직 없다(nail-under-the-roots 0223, 2026-10-28 계획 단계).
sources:
  - https://itch.io/docs/creators/html5
  - https://itch.io/blog/560526/acquiring-tester-feedback
  - https://www.wayline.io/blog/effective-playtesting-sessions-indie-game-success
  - https://www.wayline.io/blog/optimizing-game-iteration-player-feedback-game-demos
  - https://www.steampageanalyzer.com/blog/how-long-should-a-steam-demo-be
  - https://bugnet.io/blog/how-long-should-your-steam-demo-be
  - https://itch.io/t/5209594/how-long-should-a-demo-be-mine-might-be-too-long
  - https://unity.com/blog/steam-next-fest-developer-tips-unity
---

# 인디 게임 공개 데모와 바깥 의견 받기

## 요약
게임이 이미 웹에 무료로 떠 있어도 **찾아오는 곳**과 **의견을 남기는 길**이 없으면 바깥 의견은 모이지 않는다. 공개 데모는 세 가지를 함께 준비하는 일이다: 처음 15분(첫 경험)과 기술 점검, 버전이 저절로 붙는 짧은 설문, 게임을 찾는 곳(itch.io 등)의 페이지. 로그라이트라면 "한 바퀴는 온전히, 깊이는 잠가서"가 기본 모양이고, 해금 구조가 이미 있다면 전체 판이 그대로 그런 모양일 수 있다.

## 본문
### 무엇을 시험하나 먼저
- 첫 경험(온보딩)·새 메커닉·전체 루프 중 하나를 고른다. 공개 데모는 대개 **첫 경험**이다.
- 한 번에 한두 가지만. 기능을 다 보이려 하면 의견이 흩어진다.

### 범위: 로그라이트 데모
- 한 바퀴(런 하나, 첫 지도 하나)를 끝까지 주고, 깊이(캐릭터·지대·특전)를 잠근다. 선형 게임처럼 "궁금한 순간에 끊기"는 로그라이트에 덜 맞는다.
- 3자 정리 기준 20~40분. 완주 비율이 중앙값 분보다 낫고, 40% 아래면 길다는 말이 있다(숫자는 원문 확인 전).
- 끝이 먼 판(전체 공개)이면 완주율 대신 중간 지점(첫 체크포인트·첫 보스)까지 간 비율을 본다.

### 기술 점검이 먼저
- 멈추거나 깨지는 데모는 좋은 메커닉도 가린다. 첫 로딩 크기·느린 회선, 브라우저별, 저사양, 소리 시작(브라우저는 첫 입력 전 소리를 막는다), 오류 때 빈 화면 대신 알림.
- 공개 전에 비공개로 여러 번 돌린다.

### 의견 받는 길
- 설문은 짧게: 척도 몇 개 + 고르기 + 끝에 자유 글. "그만두고 싶었던 곳"을 묻는다.
- **버전·언어·장치·어디까지 갔나를 게임이 채워서** 설문을 연다. 사람에게 맡기면 내지 않거나 다른 버전으로 낸다.
- 몰래 재는 통계 대신 사람이 누르는 설문으로만 받으면 동의·개인정보 안내 화면이 필요 없다(대신 숫자가 적다).

### 찾아오는 곳
- itch.io HTML5: ZIP 맨 위 `index.html`, 실행에 필요한 파일 전부, 파일 이름 대소문자 정확히. HTML 게임은 기본이 후원 결제다. 용량 한도·전체 화면·모바일 옵션은 올릴 때 화면에서 확인.
- 데모는 행사(축제·소개) **전에** 미리 내 둔다 — 행사는 시험장이 아니라 진열대.

## 왜?
- 바깥 의견은 데모가 없어서가 아니라 **의견을 남기는 비용**이 높아서 안 모인다. 그 비용(버전 적기, 어디까지 갔는지 설명)을 게임이 대신 내면 응답이 는다.
- 첫 경험을 시험 대상으로 고르는 것: 모르는 사람은 처음 몇 분에 그만둔다. 뒤쪽 콘텐츠의 의견은 그 문을 넘은 사람에게서만 나온다.
- 로그라이트에서 길이로 자르기 어려운 것: 반복이 핵심이라 "첫 길만"은 그 축을 못 보여 준다. 해금으로 이미 잠겨 있으면 따로 자른 데모 빌드는 고칠 곳만 둘로 늘린다(1인 개발).

## 함정
- 버전이 안 붙은 설문 → 이미 고친 버그 보고가 섞인다.
- 행사 당일 데모 첫 공개 → 깨진 판이 가장 많은 사람에게 보인다.
- 3자 정리의 숫자(20~40분, 40%)를 그대로 목표로 삼기 → 원문·장르마다 다르다. 기준선으로만.

## 관련 노트
- [1인 개발용 액션 로그라이트 설계 원칙](action-roguelite-for-solo-dev.md)
- [로그라이트 다회차의 세 축](roguelite-replay-axes.md)
- [인디 게임 공식 페이지](../guides/indie-game-landing-page.md)
- [버전 올리기 = 릴리스](../reference/github-actions/release-from-version-bump.md)
