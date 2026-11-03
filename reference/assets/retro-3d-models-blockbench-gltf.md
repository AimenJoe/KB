---
title: 레트로 3D 모델 파이프라인 — Blockbench 상자 모델 → glTF(부위 강체 애니메이션) → 직접 로더
type: reference
tags: [assets, 3d, blockbench, gltf, animation, gamedev, pixel-art]
status: draft
created: 2026-11-03
updated: 2026-11-03
verified: |
  1차 출처로 확인(2026-11-03):
  - Blockbench 레포 `js/formats/bbmodel.js`: `.bbmodel`은 JSON이고 상위 키는 `meta{format_version "5.0", model_format, box_uv}`·`resolution`·`elements`·`groups`·`outliner`·`textures`·`animations`(있을 때)·`animation_controllers` 등.
    애니메이션은 `animators`(본 uuid 키) → `keyframes[]` → `channel`('position'|'rotation'|…)·`data_points[{x,y,z}]`·`interpolation`(bezier면 `bezier_*`). 상자 요소의 `from/to/origin/rotation`은 이 파일이 아니라 각 클래스의 `getSaveCopy`에 있어 **이번엔 못 봤다**.
  - Blockbench 위키 "bbmodel": "완전한 JSON 사양은 아직 없다", 5.0에서 `groups`와 `outliner`(트리만, 노드는 `uuid`·`isOpen`·`children`)를 분리, 5.0 전에는 위치 X·회전 X/Y 키프레임이 **반대 부호**였다.
  - `gltf` 크레이트 docs.rs: 최신 1.4.1, `animation` 모듈(채널·타깃·샘플러), `scene`(노드 트리), `skin`, `gltf::import`(.gltf + 버퍼 + 이미지).
  2차 출처만 있음(Defold 포럼 가이드, 2024): Blockbench `File > Export > glTF Model`에 **Export Animations**·**Groups As Armatures**(그룹을 본으로)·Model Scale(기본 16)·Embed textures 옵션이 있고, 그룹을 피벗으로 쓰는 "변형만 하는" 애니메이션을 그대로 내보낼 수 있다. 공식 Blockbench 문서에서는 이 옵션 이름을 확인하지 못했다.
  확인 못 함: 내보낸 glTF에서 그룹이 노드 TRS 애니메이션으로 가는지 아니면 스킨(joints)으로 가는지(가이드는 Defold에서 "skeleton"에 붙이는 것으로 보아 스킨일 수 있다 — 그러면 부위가 강체여도 조인트 하나 = 가중치 1.0이라 CPU 변형이 행렬 하나로 끝난다), 회전 단위(도)와 축 방향, 실제 파일을 열어 본 적 없음.
sources:
  - https://github.com/JannisX11/blockbench/blob/master/js/formats/bbmodel.js
  - https://www.blockbench.net/wiki/docs/bbmodel
  - https://www.blockbench.net/wiki/blockbench/formats
  - https://forum.defold.com/t/blockbench-animation-guide/82193
  - https://docs.rs/gltf/latest/gltf/
---

# 레트로 3D 모델 파이프라인 — Blockbench → glTF → 직접 로더

## 요약
"마인크래프트보다 조금만 정교한" 로우폴리 캐릭터는 **상자 몇 개를 부위 트리로 묶고 부위마다 회전 키프레임**을 주면 된다(스키닝 없음). Blockbench(무료, 브라우저/데스크톱)가 바로 그 도구이고, glTF로 내보내면 Rust `gltf` 크레이트가 노드 트리와 애니메이션 채널을 읽어 준다. 로더가 없는 엔진(macroquad)에서는 이 조합이 가장 짧은 길이다. 단, 내보내기 옵션과 축·단위는 **실제 파일 하나로 먼저 확인**해야 한다(2차 출처뿐).

## 본문

### 왜 상자 + 부위 강체인가
- 스켈레탈 스키닝(정점마다 본 가중치)은 로더·셰이더·블렌딩을 다 써야 한다. 부위 강체는 "부위 메시 × 부모 행렬" 곱 하나다. macroquad처럼 정점을 매 프레임 올리는 엔진에서는 CPU에서 곱해 보내면 끝이다([macroquad 3D](../macroquad/3d-rendering.md)).
- 실루엣이 각져서 쿼터뷰(작게 보임)에서 종류 구분이 쉽고, 숄더뷰(크게 보임)에서도 픽셀 텍스처가 스타일로 읽힌다.
- 동작 수가 적다(대기·걷기·공격·회피·피격·쓰러짐). 2D에서 칸 8개를 찍던 일과 같은 양이다.

### 파이프라인 후보
| 단계 | 도구 | 비고 |
|---|---|---|
| 모델링·UV·텍스처 | Blockbench Generic Model | 텍스처는 16~64px 아틀라스, 칸 단위 UV |
| 애니메이션 | Blockbench 타임라인(그룹 = 피벗) | 채널 rotation/position/scale, 보간 linear/step/catmullrom/bezier |
| 내보내기 | `File > Export > glTF Model`, Export Animations 켬 | Groups As Armatures 켜는 쪽이 "그룹을 본으로" — 실제 출력 구조 확인 필요 |
| 읽기 | `gltf = "1.4"` | `document.nodes()`로 트리·TRS, `document.animations()`로 채널·샘플러 → 자체 `Model { parts, clips }` |
| 대안 | `.bbmodel` JSON 직접 파싱 | 사양이 없고 버전마다 바뀐다(5.0에서 부호 뒤집힘). glTF가 안전 |

### 프롬프트·AI 생성은?
2D에서 이미지 모델(나노바나나) 원본을 도트로 옮기던 흐름([이미지 생성 모델로 게임 일러스트](../../guides/image-model-for-game-illustrations.md))의 3D판(Meshy·Tripo 같은 메시 생성)은 삼각형 수천 개의 유기적 메시를 내놓아 **레트로 상자 스타일과 맞지 않고** 라이선스·공개 의무도 따로 봐야 한다. 참고 그림(콘셉트·텍스처 색감)에는 쓰되 메시는 손으로 상자를 쌓는 쪽이 일관된다. AI를 썼으면 어디에 썼는지 숨기지 않는다([판매 규칙](../game-business/selling-an-indie-game-rules-and-numbers.md)).

## 왜?
3D의 비용은 폴리곤이 아니라 **리그와 애니메이션 파이프라인**이다. 상자 + 강체 부위로 제한하면 그 비용이 2D 스프라이트 칸 찍기 수준으로 내려오고, 엔진이 해 줄 일(스키닝 셰이더·본 행렬 팔레트)이 사라져 macroquad를 유지할 수 있다. "조금만 정교하게"는 취향이 아니라 **엔진을 바꾸지 않기 위한 기술 결정**이다.

## 함정
- Blockbench 단위: 1 블록 = 16 단위. Model Scale 옵션과 게임 단위(1m)를 처음에 못 박는다.
- 축: Blockbench는 y-up. macroquad `Camera3D` 기본은 z-up — 한쪽으로 통일(권장 y-up).
- 5.0 이전 파일의 키프레임 부호 반전 — 옛 파일을 섞지 않는다.
- 텍스처 임베드(data URL)는 glTF 크기를 키운다. 따로 저장해 아틀라스 하나로.
- 첫 모델을 만들기 전에 **"상자 2개 + 회전 1채널" 파일 하나**로 로더를 끝까지 통과시킨다. 캐릭터부터 만들면 로더 버그와 모델 버그가 섞인다.

## 관련 노트
- [macroquad 3D 렌더링](../macroquad/3d-rendering.md)
- [그림 못 그려도 도트 게임 만들기](../../guides/pixel-art-without-an-artist.md) — 2D에서의 같은 고민
