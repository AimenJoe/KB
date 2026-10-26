---
title: "지도: 게임 개발"
type: map
tags: [gamedev, macroquad, rust, game-design, pixel-art, game-feel]
status: verified
created: 2026-10-24
updated: 2026-10-25
---

# 지도: 게임 개발

게임 개발 관련 노트의 입구. 저장 위치는 종류별 폴더에 있고, 여기서는 도메인 관점으로 모은다.

## 설계
- [1인 개발용 액션 로그라이트 설계 원칙](../concepts/action-roguelite-for-solo-dev.md) — 런 구조 vs 메트로배니아, 탑다운 vs 사이드뷰, 전투감 먼저, 캐릭터=반복 단위, 장기 프로젝트 단계
- [그림 못 그려도 도트 게임 만들기](../guides/pixel-art-without-an-artist.md) — 에셋 팩 하나 중심, 라이선스 확인, 공개 레포 + 비공개 에셋 레포(토큰·비용·AI 조항), 둥근 지형 굽기, 눈에 띄어야 하는 물체(더하기 빛·움직임), 16×16 공격 동작(들기·치기·거두기, 발 번갈아), 타이틀 키 아트(글 자리 먼저, 이음매 굴리기)
- [작곡가·음향 담당 없이 게임 소리 넣기](../guides/game-audio-without-a-composer.md) — CC0 출처(Kenney·OGA), 숫자로 거르기(길이·밝기·폭·이음매), 표 + 변환 스크립트, 변형·메뉴 소리 한 곳·덕킹
- [무료 그림·사진 구하는 곳](../reference/assets/free-image-sources.md) — Openverse·미술관 CC0·사진 사이트, PDM과 CC0, API 요령(Met v1.1, UA)
- [게임 그림 외주 맡기기](../guides/commissioning-game-art.md) — 임시 그림으로 먼저 판정, 사양서(안전 영역·색 약속), 계약: 저작재산권 + 2차적저작물작성권 특약(한국 제45조②), 공개 레포 커밋 허락

## 보상·경제
- [회복과 화폐 드롭](../concepts/roguelite-healing-and-currency.md) — 깎인 만큼 확률 + 불운 보정, 자석·줍기 지연·오르는 소리, 메타 화폐 맡기기(쉼터 자동)·둘 중 하나 영구 기술·살 수 있을 때 쓰는 곳이 빛나기
- [능력치·장비 설계](../concepts/action-rpg-stats-and-equipment.md) — 무기는 모양·장신구는 수치·성장은 영구, 공격 속도 = 시계 배율, 큰 회복 = 목숨
- [로그라이트 저널(목표 목록)](../concepts/roguelite-journal-goals.md) — 평소 플레이를 런을 넘는 목표로, 앞 목표 뒤에 펼쳐짐, 받기 보상(재화·힘 아닌 것·옆으로), 진행은 기록에서 계산
- [저장 슬롯·이어하기·런 중단 저장](../concepts/roguelite-save-slots-and-continue.md) — 기록과 런을 나누기, 슬롯은 기록 단위·설정은 밖, 시작하기/이어하기 → 슬롯 고르기, 옛 저장 = 슬롯 1, 두 번 눌러 지우기, 런 저장은 죽음이 런을 끝내나로 고르기(한 번 쓰는 중단 저장 vs 마지막 체크포인트)

## 월드 구조
- [탑다운 모험 구조](../concepts/adventure-field-and-procedural-dungeon.md) — 격자 하나, 카메라 경계 사각형(연속 스크롤 = 큰 경계, 방 밀기 = 경계 바뀜), 방 그래프 던전·잠금, 저장 지점 부활, 보스 뒤 출구는 쓰러진 자리에서 멀리·밟을 때만
- [선형 진행을 갈래 길로 느끼게 하는 지도](../concepts/branching-route-map.md) — 층 + 이어진 구간(엇갈림 없음·합류), 칸 종류가 결과를 바꿈, 다음 한 걸음 + 보스만 보이기(StS 지도·Hades 문)

## 게임 루프·전투감
- [고정 타임스텝 게임 루프와 히트스톱](../concepts/fixed-timestep-and-hitstop.md) — 누적기 루프, 입력 래치, 보간, 히트스톱은 로직 시계만, trauma² 흔들림
- [공격 타이밍 패링](../concepts/timing-parry.md) — 버튼 없이 스윙 첫 창 + 앞쪽, 회피 = 안전·패링 = 이득, 거울(막는 보스: 튕기고 반격, 아래·필살기로 뚫기)
- [모든 행동에 재사용 대기](../concepts/action-reuse-gating.md) — 동작 시간·대기·게이지·쓰는 시간을 행동마다 고르기, 회복 = 먹는 시간 + 시작부터 대기, 패링 창 = 열린 순간부터 대기·성공하면 해제
- [필살기의 임팩트](../concepts/special-move-impact.md) — 시동 정지(슈퍼 플래시), 화면 한 폭 거리, 넉백 > 속도로 끌고 가기, 소리 하나
- [도트 액션의 손맛 효과](../concepts/game-feel-particles-and-light.md) — 입자 세 무리(타격·몸짓·분위기), 흙덩이 높이·중력, 맞은 쪽 불똥, 상태 없는 환경 입자, 더하기 빛 겹
- [근접 주인공의 원거리 보스](../concepts/ranged-boss-for-melee-player.md) — 부채꼴 탄 + 되받아치기, 바닥 위험은 발밑 + 둘레·고리 둘(어디·언제)·파내기·무적 굴, 표시 끝 = 판정, 위험물은 적이 아니라 별도 목록

## 이야기
- [로그라이트 다회차의 세 축](../concepts/roguelite-replay-axes.md) — 실력(단계식·골라 묶기 난이도)·다양성(캐릭터·결)·궁금함(엔딩 뒤 이야기·도감·허브), 일일 시드·보스 다시, 도움 모드, 옆으로 넓히기
- [로그라이트에서 이야기를 전하는 방법](../concepts/roguelite-narrative-delivery.md) — 죽음에 세계 안의 이유, 귀환 대사 = 조건 + 가장 구체적인 것 + 대비책 + 한 번만, 지는 사람도 이야기를 본다, 환경·허브 변화
- [다시 만나는 보스](../concepts/recurring-boss.md) — 만날 때마다 한 수·말 한 줄·눈에 보이는 흔적, 지면 길을 비킨다, 숨는 상태는 hittable 하나로, 같은 시드 = 같은 굴, HUD가 싸움을 가리는 함정, 다시 싸우기 모드(이긴 보스만·기록만·러시)
- [두 번째 플레이어 캐릭터](../concepts/second-playable-character.md) — 같은 버튼 자리에 다른 동사(회피·특기·무기 종류), 기록·난이도·엔딩은 캐릭터마다, 보스였던 캐릭터는 그 런 보스를 끄기
- [캐릭터 설정에 쓰는 실제 동물·생태 사실](../reference/nature/animal-behavior-for-character-design.md) — 두더지 독립·침의 독, 라쿤 "손 씻기"는 씻기가 아님, 땅강아지 수렴 진화, 뽕나무버섯, 균근 공생, 다람쥐 저장

## 테스트·연출
- [개발용 시나리오 진입점과 스텝 스크립트 컷씬](../concepts/dev-scenarios-and-scripted-cutscenes.md) — 시나리오 목록 → 월드 구성, JRPG식 대화창, 건너뛰기, 배우 좌표계·싸움 끝 연타 함정, 일러스트 장면(2배 밀도 한 장 그림·패닝·입자·내레이션, 홀수 배율)

## 입력·접근성
- [작은 픽셀 HUD 읽히게 하기](../concepts/hud-readability-and-quick-slots.md) — 바탕판·테두리 글자, 게이지 굵게·가득 신호, 퀵 슬롯 자리 고정·저절로 바꾸기 + 깜빡임, 창 밑 HUD 숨기기
- [컨트롤러 버튼 배치와 다시 붙이기](../concepts/controller-layout-and-remapping.md) — 오른쪽 넷 = 자주 쓰는 넷, 키보드 다이아몬드, 겹치면 맞바꿈, 메뉴 키 고정, 안내는 배치를 따라, 격자 끝에서 옆 탭으로

## 다국어
- [작은 게임 다국어 구조](../guides/small-game-localization.md) — 고정 키 표, 자리표시자, 폰트 커버리지 테스트, 브라우저 언어 읽기
- [중국어·일본어 픽셀 폰트](../reference/fonts/cjk-pixel-fonts.md) — 중국어 폰트 ≠ 일본어 폰트, Ark Pixel·Fusion·Galmuri 범위와 라이선스

## 엔진·플랫폼 선택
- [Rust 게임 엔진 비교: 웹 + Android 핸드헬드 + 컨트롤러](../reference/rust-game-engines/web-android-gamepad-support.md) — macroquad / Bevy / Godot, Android 게임패드가 공통 공백(macroquad는 버튼만 패치로 해결)

## macroquad
- 입력
  - [게임패드와 Android 입력 현황](../reference/macroquad/gamepad-and-android-input.md) — `gamepads` 크레이트, miniquad Android 백엔드의 공백과 패치 범위, 메뉴 스틱 탐색(히스테리시스)
- 렌더링
  - [픽셀 퍼펙트 렌더링](../reference/macroquad/pixel-perfect-rendering.md) — 내부 해상도 320×180, render target, Nearest, 정수 배율
  - [글자 그리기 비용과 브라우저 프레임레이트](../reference/macroquad/text-rendering-and-browser-frame-rate.md) — 아틀라스 통째 올리기, 픽셀 폰트는 원래 크기로 굽고 정수배, 미리 굽기, WebGL 안티에일리어싱 끄기, Safari 저전력 30fps
- 빌드·배포
  - [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](../guides/macroquad-wasm-netlify-github-actions.md) — 전체 절차
  - [macroquad를 GitHub Actions에서 Android APK로](../guides/macroquad-android-apk-github-actions.md) — cargo-quad-apk git 고정, 러너 내장 SDK/NDK, gamepads 제외, 서명 키는 Secret에
  - [macroquad iOS 빌드](../reference/macroquad/ios-build.md) — macOS 러너로 서명 안 한 .ipa, Info.plist 최소 키, 샌드박스 저장 자리, 서명 갈림길(무료 7일 / $99 TestFlight), 패드는 gilrs에 iOS 없음
  - [버전 올리기 = 릴리스](../reference/github-actions/release-from-version-bump.md) — 본문 파일이 스위치, CI가 태그·APK·Release
  - [WASM 빌드와 JS 번들](../reference/macroquad/wasm-build.md) — 번들 버전 계약, 에셋 로딩, 정수로 주고받는 내 플러그인(localStorage 설정 저장), 번들을 고치지 않는 로딩 화면
  - [소리(quad-snd)](../reference/macroquad/audio.md) — 네이티브 wav·ogg만·통째로 f32 44.1kHz(1분 ≈ 21MB)·가까운 점 리샘플·음높이 없음, 웹 mp3/네이티브 ogg, 교차는 직접, 들을 때 읽고 놓기(네이티브는 푸는 동안 멈칫)
  - [정적 WASM 호스팅](../concepts/static-wasm-hosting.md) — 왜 번들러가 없어도 되는가
  - [0001 빌드는 CI, 호스팅은 Netlify](../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md)

## 아직 없는 것
- 상태 관리 — 노트가 생기면 추가

## 다른 지도
- [Rust](rust.md) · [CI/CD와 호스팅](ci-cd-hosting.md)
