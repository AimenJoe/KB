---
title: 로그라이트에서 이야기를 전하는 방법
type: concept
tags: [gamedev, game-design, roguelite, narrative, dialogue]
status: draft
created: 2026-10-25
updated: 2026-10-25
verified: |
  1차 출처로 확인: 없음. 아래 설계는 nail-under-the-roots 스토리 초안(docs/story-brainstorm.md)에 적용 중이고, 아직 구현·플레이로 확인하지 않았다.
  2차 출처만 있음: Hades — 죽음을 "게임 오버"가 아니라 구조의 일부로, 끝맺음 지점을 여러 번(Kasavin 인터뷰, Tom's Guide),
  난이도 벽에 막힌 플레이어도 이야기가 나아가게(GDC Podcast ep.16 소개글). Valve 대사 규칙 DB — 세계의 사실 수백 개를
  규칙 수천 개에 맞춰 보고 "가장 구체적인 규칙"을 고르고 덜 구체적인 규칙이 대비책(Emily Short·Radiator 블로그의 GDC 2012 Ruskin 강연 요약,
  GDC Vault 소개글). Hollow Knight 환경 서사·Dead Cells 조각 단서(리뷰·분석글). Spiritfarer — 무거운 주제를 부드러운 그림으로(개발자 인터뷰 기사). 상태와 어긋난 대사 불만(Steam 토론, 일화).
  확인 못 함: Hades가 대사를 고르는 실제 우선순위 규칙(GDC 2021 강연 원문을 못 봤다), Ruskin 강연의 "구체성" 계산법(슬라이드를 못 봤다).
sources:
  - https://www.tomsguide.com/uk/features/hades-exclusive-interview-supergiant
  - https://gdconf.com/news/roguelikes-and-narrative-design-hades-creative-director-greg-kasavin-gdc-podcast-ep-16
  - https://gdcvault.com/play/1026975/Breathing-Life-into-Greek-Myth
  - https://www.gdcvault.com/play/1015528/AI-driven-Dynamic-Dialog-through
  - https://emshort.blog/2012/03/16/gdc-2012-talk-on-dynamic-dialogue/
  - https://www.blog.radiator.debacle.us/2012/07/rule-databases-for-contextual-narrative.html
  - https://mechanicsofmagic.com/2025/05/16/critical-play-worldbuilding-dorian-gulley
  - https://www.gameskinny.com/culture/thunder-lotus-on-spiritfarer-death-hugs-and-legacies/
  - https://steamcommunity.com/app/1145360/discussions/0/2987539784417139179
---

# 로그라이트에서 이야기를 전하는 방법

## 요약
로그라이트는 같은 길을 수십 번 다시 간다. 그래서 이야기를 "한 번 보는 줄거리"로 두면 반복과 싸우게 된다. 대신 **반복과 죽음 자체를 이야기의 박자로 쓴다.**
1. 죽음과 귀환에 세계 안의 이유를 준다.
2. 돌아올 때마다 상태에 맞는 짧은 대사를 한 번씩만 꺼낸다(조건 + 가장 구체적인 것 우선 + 대비책).
3. 이기지 못해도 이야기가 나아가게 한다.
4. 큰 사실은 대사가 아니라 환경과 눈에 보이는 진행으로 보여 준다.

## 본문
### 1. 죽음을 이야기 안에 넣는다
- "왜 다시 여기서 깨어나나"에 세계관 답을 준다. Hades는 저승 왕자라 죽으면 집(저승)으로 돌아간다. 죽음이 실패 화면이 아니라 귀가가 된다.
- 답은 세계의 비밀과 묶을수록 좋다. 예: 누가/무엇이 데려오는지가 나중에 밝혀질 진실의 첫 단서가 된다.

### 2. 귀환 대사: 조건 + 우선순위 + 한 번만
- 대사 한 줄 = (조건들, 글, 본 적 있음).
  - 조건 예: 쓰러진 장소, 이긴 보스, 처음인가, 어떤 동료가 돌아왔나.
- 돌아올 때 맞는 것 중 **조건이 가장 많이(구체적으로) 맞는 줄**을 고른다. 아무것도 안 맞으면 평소 대사(대비책)가 나온다. Valve의 규칙 DB(Left 4 Dead 2·Dota 2 대사 시스템)가 이 구조다.
- 이야기 대사는 한 번 보면 표시해서 다시 안 꺼낸다. 평소 대사만 돌려쓴다.
- 짧게 쓴다. 한 번 돌아올 때 한두 줄이면 된다. 10~15분짜리 런 사이를 대사가 붙잡으면 안 된다.

### 3. 지는 플레이어도 이야기를 본다
- 이기는 것만 비트를 열면, 난이도 벽에 막힌 사람은 이야기도 같이 막힌다. Kasavin이 이 문제를 직접 짚었다.
- 그래서 **쓰러진 횟수·장소도 조건**으로 쓴다. 예: 처음 쓰러졌을 때, 특정 보스에게 처음 졌을 때, 가장 깊은 곳에서 처음 쓰러졌을 때.
- 끝맺음 지점을 여러 번 둔다. 첫 도달은 반쪽 엔딩, 조건을 채우면 참 엔딩. 중간에 그만둬도 이야기가 끊긴 느낌이 덜하다.

### 4. 환경과 눈에 보이는 진행
- **환경**: 빈 집, 무엇을 감은 뿌리, 한 방향으로 휜 지형. 글 없이 의심하게 만든다(Hollow Knight의 배치·색, Dead Cells의 시체 옆 쪽지).
- **도감**: 돌아온 상대의 설명이 한 줄 바뀐다. 데이터 표 하나로 이야기가 쌓인다.
- **허브의 변화**: 빈 자리, 늘어나는 이웃, 커지는 불처럼 메타 진행 자체를 이야기 그림으로 만든다.

### 5. 톤: 그림이 무게를 받친다
무거운 주제(상실, 죽음)는 부드럽고 귀여운 그림 위에서 오히려 편하게 꺼낼 수 있다. Spiritfarer 개발자들이 그렇게 말했다. 슬프다고 대사로 말하지 않는다. 빈 자리와 여백이 그 일을 한다.

## 왜?
- 반복이 구조의 중심이면, 이야기가 반복을 **보상**해야 반복이 의미가 생긴다. "또 죽었다"가 "그래서 이번엔 무슨 말을 들을까"가 된다.
- 조건 + 가장 구체적인 것 + 대비책 구조는 대사 수가 적어도 맥락에 맞게 들린다. 줄을 늘리면 늘린 만큼 정밀해지고, 빠진 경우는 평소 대사가 막는다. 1인 개발이 대사를 조금씩 늘려 가기에 맞다.
- 환경 서사는 글을 번역할 필요가 없다. 다국어 비용 0이다.

## 함정
- 조건이 상태를 잘못 읽으면 "벌써 한 일을 처음인 듯 말하는" 대사가 된다. Hades 플레이어도 이 불만을 적었다(Steam 토론). 조건은 실제로 저장되는 상태만 쓴다.
- 본 적 있음 표시는 저장 데이터다. 저장 형식이 바뀔 때 함께 옮긴다.
- 같은 보스를 이야기상 여러 번 이겨야 하는 연출(점점 돌아오는 상대)은 반복이 지루해질 수 있다. 매번 장소·패턴을 바꾸고, 진행을 막지 않게 한다.

## 관련 노트
- [선형 진행을 갈래 길로 느끼게 하는 지도](branching-route-map.md)
- [개발용 시나리오 진입점과 스텝 스크립트 컷씬](dev-scenarios-and-scripted-cutscenes.md)
- [작은 게임 다국어 구조](../guides/small-game-localization.md)
- [캐릭터 설정에 쓰는 실제 동물·생태 사실](../reference/nature/animal-behavior-for-character-design.md)
