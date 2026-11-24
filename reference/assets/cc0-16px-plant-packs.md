---
title: CC0 16px 식물 그림 팩 — 화단용(크고 또렷한 것)과 바탕용(작고 평평한 것)
type: reference
tags: [assets, licensing, pixel-art, gamedev, vegetation]
status: draft
created: 2026-11-24
updated: 2026-11-24
verified: |
  1차 출처로 확인(2026-11-24, nail-under-the-roots 0306):
  - 아래 네 팩의 다운로드 페이지를 받아 라이선스 칸을 직접 읽었다. OpenGameArt 셋은 `field-name-field-art-licenses` 칸이 "CC0" 하나,
    itch.io PixelFarm은 "Creative Commons Zero v1.0 Universal". ansimuz zip 안 `license.txt`도 CC0. SpiderDave 설명 "No attribution required".
  - 파일을 받아 크기·칸을 확인했다: Idylwild 시트 240×320(16칸), SpiderDave 936×24(12×24 칸 78개, 바탕색 (34,32,52) 불투명).
  - Sunnyside World(16px) 마을 화면 스크린숏에 3배로 얹은 시안 13개를 만들어 비교했고, 고른 것을 게임에 넣어 헤드리스 화면으로 확인했다.
  - "큼지막한 Idylwild는 화단, 작은 SpiderDave는 배경"은 사장 판정(2026-11-24). 결이 맞는지는 사람 판정.
  2차 출처만 있음: 검색 결과 요약의 Kenney Tiny Town(16px, CC0 — 식물이 있는지는 못 봄), Bushes 2(절차 생성 덤불, 라이선스 미확인).
  확인 못 함: PixelFarm 무료판의 실제 파일(페이지 설명만 읽었다).
sources:
  - https://opengameart.org/node/171914
  - https://opengameart.org/content/flowers
  - https://opengameart.org/content/trees-bushes
  - https://lushmustache.itch.io/pixelfarm
---

# CC0 16px 식물 그림 팩

## 요약
3/4 탑다운 16px 게임에 꽃·덤불을 더할 때 쓸 수 있는 CC0 팩. **크고 명암이 촘촘한 꽃무리(Idylwild)는 플레이어가 놓는 자리(화단)**에,
**작고 평평한 들꽃(SpiderDave)은 지형을 구울 때 바탕에 섞어** 쓰면 둘 다 제자리를 찾는다. CC0라 공개 레포에 원본까지 둘 수 있다.

## 본문
| 팩 | 크기·꼴 | 내용 | 라이선스(원문) | 쓰임 |
|---|---|---|---|---|
| [Idylwild's Foliage Pack](https://opengameart.org/node/171914) | 16×16, 시트 240×320, SNES풍(명암 촘촘), `.ase`·`.psd` 원본 포함 | 나무 8(과일), 덤불 8(꽃·열매 있음/없음), 꽃무리 10(파랑·보라·분홍·라벤더·금잔화·노랑…), 큰 잎·덩굴·버섯·돌·상자·통·모닥불 | CC0 | **화단·플레이어가 놓는 꽃**: 들꽃 위에서 한 덩어리로 또렷 |
| [SpiderDave — Flowers](https://opengameart.org/content/flowers) | 12×24 칸 78개(한 줄 936×24), db32 팔레트, 평평 | 들꽃·잡초·버섯·덩굴·풀·부들 | CC0("No attribution required") | **바탕 굽기**: 화단으로는 가늘어 안 보이지만 들판에 흩으면 결이 맞는다 |
| [ansimuz — Trees & Bushes](https://opengameart.org/content/trees-bushes) | 큰 나무 위주, 짙은 녹색 | 나무·덤불·작은 꽃·고사리 | CC0(zip `license.txt`) | 밝은 마을엔 어둡다(숲 지대 후보) |
| [LushMustache — PixelFarm](https://lushmustache.itch.io/pixelfarm) | 16×16 | 무료판: 열매 없는 덤불·나무·젖은 흙·길·풀·당근(자라는 단계) | CC0 | 무료판은 적다(작물 단계는 유료판) |

- 크기 맞추기: 16px 타일셋(Sunnyside) 화면에 같은 배율로 얹어 본다. 16칸 꽃무리는 1칸에 한 덩어리, 12×24 들꽃은 1칸에 한 포기(아래 맞춤).
- 바탕색이 불투명한 시트(SpiderDave)는 그 색을 투명으로 바꿔 쓴다.
- 쓰는 칸만 잘라 한 장으로 만드는 스크립트를 두고, 원본은 레포의 원본 폴더에(CC0라 공개 레포 가능), 출처는 에셋 라이선스 표에.

## 왜?
- 그림체가 다른 팩을 섞으면 같은 자리에서 부딪친다. **역할을 나누면**(눈이 가는 자리 = 촘촘한 그림, 배경 = 평평하고 작은 그림) 크기·명암 차이가
  오히려 위계가 된다. 화단 꽃이 구운 들꽃과 구별되어야 "내가 심은 것"이 보인다.
- 쓰던 팩(Sunnyside)에 이미 파는 꾸미기(버섯·해바라기·소나무·꽃 덤불)와 같은 것을 다시 쓰면 "사는 것 vs 기르는 것"이 헷갈린다 — 겹치지
  않는 종류를 바깥에서 찾는 까닭.

## 함정
- 검색 요약의 라이선스는 틀리거나 섞여 있다(한 페이지 글에 CC-BY·OGA-BY가 함께 보였다 — 댓글·옆 칸 글자). 라이선스 칸 자체를 읽는다.
- 무료판·유료판이 갈린 itch 팩은 무료판에 들어 있는 것만 본다.
- 버섯·부들처럼 이미 다른 뜻(빛나는 버섯 꾸미기·물가)이 있는 것은 바탕에서 뺀다.

## 관련 노트
- [그림 못 그려도 도트 게임 만들기](../../guides/pixel-art-without-an-artist.md) — "쓰던 에셋부터, 없으면 CC0, 시안은 게임 화면에"
- [무료 그림·사진 구하는 곳](free-image-sources.md) — 그림·사진(일러스트 바탕)
- [로그라이트 메타 재화 점검](../../guides/roguelite-economy-check.md) — 이 꽃을 쓴 끝없는 쓸 곳(돌려 심는 화단)
