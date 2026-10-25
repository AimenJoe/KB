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
- [그림 못 그려도 도트 게임 만들기](../guides/pixel-art-without-an-artist.md) — 에셋 팩 하나 중심, 라이선스 확인, Aseprite 손보기
- [게임 그림 외주 맡기기](../guides/commissioning-game-art.md) — 임시 그림으로 먼저 판정, 사양서(안전 영역·색 약속), 계약: 저작재산권 + 2차적저작물작성권 특약(한국 제45조②), 공개 레포 커밋 허락

## 보상·경제
- [회복과 화폐 드롭](../concepts/roguelite-healing-and-currency.md) — 깎인 만큼 확률 + 불운 보정, 자석·줍기 지연·오르는 소리
- [능력치·장비 설계](../concepts/action-rpg-stats-and-equipment.md) — 무기는 모양·장신구는 수치·성장은 영구, 공격 속도 = 시계 배율, 큰 회복 = 목숨

## 월드 구조
- [탑다운 모험 구조](../concepts/adventure-field-and-procedural-dungeon.md) — 격자 하나, 카메라 경계 사각형(연속 스크롤 = 큰 경계, 방 밀기 = 경계 바뀜), 방 그래프 던전·잠금, 저장 지점 부활
- [선형 진행을 갈래 길로 느끼게 하는 지도](../concepts/branching-route-map.md) — 층 + 이어진 구간(엇갈림 없음·합류), 칸 종류가 결과를 바꿈, 다음 한 걸음 + 보스만 보이기(StS 지도·Hades 문)

## 게임 루프·전투감
- [고정 타임스텝 게임 루프와 히트스톱](../concepts/fixed-timestep-and-hitstop.md) — 누적기 루프, 입력 래치, 보간, 히트스톱은 로직 시계만, trauma² 흔들림
- [공격 타이밍 패링](../concepts/timing-parry.md) — 버튼 없이 스윙 첫 창 + 앞쪽, 회피 = 안전·패링 = 이득
- [모든 행동에 재사용 대기](../concepts/action-reuse-gating.md) — 동작 시간·대기·게이지·쓰는 시간을 행동마다 고르기, 회복 = 먹는 시간 + 시작부터 대기, 패링 창 = 열린 순간부터 대기·성공하면 해제
- [필살기의 임팩트](../concepts/special-move-impact.md) — 시동 정지(슈퍼 플래시), 화면 한 폭 거리, 넉백 > 속도로 끌고 가기, 소리 하나

## 이야기
- [로그라이트 다회차의 세 축](../concepts/roguelite-replay-axes.md) — 실력(단계식·골라 묶기 난이도)·다양성(캐릭터·결)·궁금함(엔딩 뒤 이야기·도감·허브), 일일 시드·보스 다시, 도움 모드, 옆으로 넓히기
- [로그라이트에서 이야기를 전하는 방법](../concepts/roguelite-narrative-delivery.md) — 죽음에 세계 안의 이유, 귀환 대사 = 조건 + 가장 구체적인 것 + 대비책 + 한 번만, 지는 사람도 이야기를 본다, 환경·허브 변화
- [다시 만나는 보스](../concepts/recurring-boss.md) — 만날 때마다 한 수·말 한 줄·눈에 보이는 흔적, 지면 길을 비킨다, 숨는 상태는 hittable 하나로, 같은 시드 = 같은 굴, HUD가 싸움을 가리는 함정
- [캐릭터 설정에 쓰는 실제 동물·생태 사실](../reference/nature/animal-behavior-for-character-design.md) — 두더지 독립·침의 독, 라쿤 "손 씻기"는 씻기가 아님, 땅강아지 수렴 진화, 뽕나무버섯, 균근 공생, 다람쥐 저장

## 테스트·연출
- [개발용 시나리오 진입점과 스텝 스크립트 컷씬](../concepts/dev-scenarios-and-scripted-cutscenes.md) — 시나리오 목록 → 월드 구성, JRPG식 대화창, 건너뛰기, 배우 좌표계·싸움 끝 연타 함정, 일러스트 장면(2배 밀도 한 장 그림·패닝·입자·내레이션, 홀수 배율)

## 입력·접근성
- [컨트롤러 버튼 배치와 다시 붙이기](../concepts/controller-layout-and-remapping.md) — 오른쪽 넷 = 자주 쓰는 넷, 키보드 다이아몬드, 겹치면 맞바꿈, 메뉴 키 고정, 안내는 배치를 따라

## 다국어
- [작은 게임 다국어 구조](../guides/small-game-localization.md) — 고정 키 표, 자리표시자, 폰트 커버리지 테스트, 브라우저 언어 읽기
- [중국어·일본어 픽셀 폰트](../reference/fonts/cjk-pixel-fonts.md) — 중국어 폰트 ≠ 일본어 폰트, Ark Pixel·Fusion·Galmuri 범위와 라이선스

## 엔진·플랫폼 선택
- [Rust 게임 엔진 비교: 웹 + Android 핸드헬드 + 컨트롤러](../reference/rust-game-engines/web-android-gamepad-support.md) — macroquad / Bevy / Godot, Android 게임패드가 공통 공백

## macroquad
- 입력
  - [게임패드와 Android 입력 현황](../reference/macroquad/gamepad-and-android-input.md) — `gamepads` 크레이트, miniquad Android 백엔드의 공백과 패치 범위, 메뉴 스틱 탐색(히스테리시스)
- 렌더링
  - [픽셀 퍼펙트 렌더링](../reference/macroquad/pixel-perfect-rendering.md) — 내부 해상도 320×180, render target, Nearest, 정수 배율
  - [글자 그리기 비용과 브라우저 프레임레이트](../reference/macroquad/text-rendering-and-browser-frame-rate.md) — 아틀라스 통째 올리기, 픽셀 폰트는 원래 크기로 굽고 정수배, 미리 굽기, WebGL 안티에일리어싱 끄기, Safari 저전력 30fps
- 빌드·배포
  - [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](../guides/macroquad-wasm-netlify-github-actions.md) — 전체 절차
  - [macroquad를 GitHub Actions에서 Android APK로](../guides/macroquad-android-apk-github-actions.md) — cargo-quad-apk git 고정, 러너 내장 SDK/NDK, gamepads 제외
  - [WASM 빌드와 JS 번들](../reference/macroquad/wasm-build.md) — 번들 버전 계약, 에셋 로딩, 정수로 주고받는 내 플러그인(localStorage 설정 저장), 번들을 고치지 않는 로딩 화면
  - [정적 WASM 호스팅](../concepts/static-wasm-hosting.md) — 왜 번들러가 없어도 되는가
  - [0001 빌드는 CI, 호스팅은 Netlify](../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md)

## 아직 없는 것
- 상태 관리, 게임 저장 파일(설정 저장은 wasm-build 노트), 사운드(에셋 파이프라인) — 노트가 생기면 추가

## 다른 지도
- [Rust](rust.md) · [CI/CD와 호스팅](ci-cd-hosting.md)
