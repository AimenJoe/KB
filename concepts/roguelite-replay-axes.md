---
title: 로그라이트 다회차의 세 축 — 실력·다양성·궁금함
type: concept
tags: [gamedev, game-design, roguelite, narrative, solo-dev]
status: draft
created: 2026-10-25
updated: 2026-10-25
verified: |
  1차 출처로 확인: 기록 형식(깃발 + 수, 문자열 키, 모르는 키 보존)과 도움 모드 피해 분산(소수 누적)을 직접 구현·단위 테스트(nail-under-the-roots 0041, 2026-10-25).
  난이도 축(실뜨기)·캐릭터는 아직 구현 전.
  2차 출처만 있음(공략·리뷰·팬 위키·포럼·영상 자막): Hades Pact of Punishment(첫 탈출 뒤 열림, 조건 15개, 열기 = 보상과 묶임,
  Bastion·Transistor 조건 시스템의 후계), Hades 에필로그(여러 번 깬 뒤, 출처마다 횟수가 다름), Hades God Mode(피해 저항 20% 시작,
  쓰러질 때마다 +2%, 최대 80%), Slay the Spire Ascension(캐릭터별 1~20 하나씩, 져도 안 내려감), Dead Cells Boss Cells(깰 때마다 하나,
  적 등급·밀도↑·회복↓, 낮추기 가능), 영구 수치 성장이 난이도와 자기 평가를 흐린다는 논점(GMTK 영상, 블로그, 플레이어 토론).
  개발사가 쓴 설계 이유 글은 찾지 못했다.
sources:
  - https://kotaku.com/everything-you-need-to-know-about-hades-endgame-1845239105
  - https://shacknews.com/article/121621/how-to-unlock-the-epilogue-hades
  - https://caniplaythat.com/2021/08/11/hades-god-mode-explained-by-supergiant-games
  - https://www.pocketgamer.com/slay-the-spire/ascension-guide
  - https://deadcells.wiki.gg/wiki/BSC
  - https://amara.org/subtitles/7doGHxwrhRpX/en/1/download/Roguelikes%20Persistency%20and%20Progression%20%20Game%20Makers%20Toolkit.en.txt
  - https://bugnet.io/blog/how-to-design-a-roguelite-meta-progression
---

# 로그라이트 다회차의 세 축

## 요약
반복하는 이유는 셋이다: **실력**(더 어렵게), **다양성**(다른 캐릭터·빌드), **궁금함**(이야기·수집·허브의 변화). 다회차도 두 겹이다.
- **엔딩 전 반복**: 메타 진행.
- **엔딩 뒤 반복**: 스스로 고르는 난이도, 캐릭터, 이어지는 이야기.

1인 개발은 이미 만든 콘텐츠(보스·던전 생성기·대사 표)를 다시 쓰는 축부터 고른다.

## 본문
| 축 | 장치 | 참조 | 싸게 만드는 법 |
|---|---|---|---|
| 실력 | 단계식 난이도 | StS Ascension(캐릭터별 1~20, 깰 때마다 하나) | 이미 있는 수치(적 체력·예고·회복 드롭·가게 값)를 단계마다 하나씩 바꾼다 |
| 실력 | 골라 묶는 조건 | Hades Pact of Punishment(조건 열몇 개, 합계 = 열기, 보상과 묶음) | 조합 균형·UI 비용이 크다. 단계식 다음에 |
| 실력 | 하나씩 얻는 난이도 아이템 | Dead Cells Boss Cells(낮추기 가능) | 단계식과 같은 자료 구조 |
| 다양성 | 캐릭터 | 보스 → 동료 → 플레이어블 | 보스 패턴이 곧 기술 세트(가장 비싸다) |
| 다양성 | 무기 결·기술 변형 | Hades Aspect | 수치표 한 줄씩 |
| 궁금함 | 엔딩 뒤 이야기 | Hades(첫 클리어 뒤에도 계속, 에필로그는 여러 번 뒤) | 귀환 대사 표에 조건만 더한다 |
| 궁금함 | 도감·앨범·허브 꾸미기 | — | "본 것" 표시 + 화면 하나 |
| 변주 | 일일 시드 | — | 같은 시드 = 같은 던전이면 날짜를 시드로. 서버 없이 혼자 보는 기록부터 |
| 변주 | 보스 다시 싸우기 | Hollow Knight Godhome | 방 하나 + 보스 목록 |
| 접근성 | 쓰러질수록 단단해지는 도움 모드 | Hades God Mode(20% + 2%/죽음, 최대 80%) | 받는 피해 배율 하나 + 누적 저장 |

### 원칙
- **위로 쌓기보다 옆으로 넓히기.** 영구 수치 성장은 상한을 둔다. 영구로 여는 것은 새 선택지다.
- **어려움은 첫 클리어 뒤에, 스스로, 되돌릴 수 있게.**
- **이야기는 지는 사람에게도 간다**: 귀환 횟수·장소도 조건으로 쓴다.
- **쉬움은 따로 켜는 것으로**: 기본 난이도를 깎지 않고 도움 모드로 끝을 보게 한다.
- 난이도 장치에 세계관 이름과 모양을 입힌다(Hades = 저승의 계약). 같은 숫자라도 "왜 어려워지나"가 이야기가 된다.

## 왜?
- 영구 수치 성장이 크면 실력과 성장을 구별할 수 없게 되고, 다 키운 뒤에는 난이도가 사라진다(GMTK의 roguelike/roguelite 논점, 플레이어 토론). 옆으로 넓히면 새 것을 써 보는 재미는 남고 난이도 곡선은 유지된다.
- 단계식은 숫자 하나라 UI·균형이 싸다. 골라 묶기는 자유롭지만 조합 폭발이 있다. 핸드헬드·1인 개발이면 단계식부터 만든다.
- 일일 시드·보스 다시 싸우기는 이미 있는 생성기·보스를 다시 쓴다. 콘텐츠 1단위당 플레이 시간이 가장 크다.

## 함정
- 난이도 단계 보상을 힘(영구 수치)으로 주면 다시 쉬워진다. 꾸미기·이야기·털빛처럼 힘이 아닌 것으로 준다.
- 캐릭터별 단계를 따로 세면 캐릭터가 늘수록 할 일이 곱으로 는다. 좋은 점이지만, 공통 진행(마을)과 캐릭터 진행(단계)을 화면에서 분리해 보인다.
- 저장 형식: 정수 칸 몇 개로 시작한 설정 저장으로는 모자란다. 기록은 따로 둔다.
  - 형식(직접 구현, nail-under-the-roots 0041): **깃발 + 수**만 쓴다. 이름은 안정된 문자열 키(`tutorial`, `deaths`, `mob.<종>`, `illust.<그림>`, `line.<대사>`)다.
  - 줄 단위 글, 머리줄에 버전을 둔다. 모르는 키도 지우지 않고 다시 쓴다(새 버전 기록을 옛 버전이 망가뜨리지 않게). 깨진 줄은 그 줄만 버린다.
  - 기능이 늘어도 형식을 바꾸지 않고 키만 더한다.
- 개발 시나리오(시험 방)는 이야기 기록을 남기지 않게 막는다. 시험하다 "쓰러진 수"가 쌓여 도움 모드·대사가 엉킨다.

## 관련 노트
- [1인 개발용 액션 로그라이트 설계 원칙](action-roguelite-for-solo-dev.md) — 반복 단위 = 캐릭터
- [로그라이트에서 이야기를 전하는 방법](roguelite-narrative-delivery.md) — 귀환 대사 표, 지는 사람도 이야기를 본다
- [능력치·장비 설계](action-rpg-stats-and-equipment.md) — 영구 성장 상한
- [모든 행동에 재사용 대기](action-reuse-gating.md)
