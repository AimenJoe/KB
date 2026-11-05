---
title: AI 3D 메시(Meshy 등)를 작은 게임용 강체 부위 모델로 — 줄이기·색 굽기·부위 자르기
type: guide
tags: [3d, ai-assets, blender, gltf, animation, gamedev, art-pipeline]
status: draft
created: 2026-11-04
updated: 2026-11-04
verified: |
  1차(직접 실행, 2026-11-04, knellroot 0038 — Blender 4.0.2 apt 판, 헤드리스 bpy):
  - Meshy Image to 3D(무료, Meshy 6 Lite) GLB = 한 덩어리 메시 삼각형 101,304·정점 57,152, 2048² 이미지 셋(base color·금속거칠기·노멀), 뼈·동작 없음.
  - glTF로 가져온 메시는 UV 이음매마다 정점이 갈라져 있다(같은 자리 정점 합치기 57,152 → 50,651). 합치지 않고 Decimate(Collapse)하면 이음매가 벌어져 금이 간다.
  - Meshy UV는 아주 잘게 쪼개져 있어 원래 UV로 텍스처를 128로 줄이면 조각 경계가 번진다. 줄인 메시에 Smart UV(89°)를 새로 펴고 원본 base color를 selected→active로 구우면(EMIT 패스, 원본 재질의 base color를 Emission에 이어서) 정점 1,900·삼각형 2,100·텍스처 256에서 원본과 거의 같아 보였다.
  - 굽기가 검게 나오는 원인 둘: ① 구울 이미지 노드를 그 재질의 입력(Base Color)에 이어 두면 "Circular dependency" — 굽고 나서 잇는다. ② 이 Blender 빌드는 OpenImageDenoiser 없이 빌드돼 `cycles.use_denoising`이 켜져 있으면 렌더는 "Build without OpenImageDenoiser" 오류, 굽기는 오류 없이 검정 → 끈다.
  - 메시 정점을 `v.co`로 직접 옮긴 뒤 `mesh.update()`를 부르지 않으면 Cycles가 옛 자리를 본다(이번 검정의 원인은 아니었지만 같이 넣음).
  - glTF 가져오기는 법선을 사용자 법선(custom split normals)으로 붙인다 → 면마다 `use_smooth`를 바꿔도 내보낼 때 무시된다. `mesh.customdata_custom_splitnormals_clear` 뒤에야 접힌 면(면 법선 · 정점 법선 < 0, 7/2,352)을 각지게 만들 수 있었다.
  - 면 가운데 자리로 부위를 나눠(머리·몸·팔·다리·꼬리) 뼈에 parent_type BONE으로 붙이면 기존 동작 표 17개가 그대로 돌았다. 목은 옷깃(목도리)이 아니라 두건 가장자리에서 잘라야 고개를 젖혀도 자른 자리가 안 보였다.
  - 로더가 이미지 하나만 읽어서 구운 텍스처(256²)와 코드 아틀라스(128²)를 512×256 한 장으로 합치고 UV를 옮겼다(왼쪽 반 / 오른쪽 위).
  2차 출처만 있음: Meshy 문서의 입력 권장(정면·중립 자세·민짜 바탕·1040px 넘게)은 문서·블로그 요약으로만 봤다. Multi-view(최대 4장)는 1차로 다시 봤다(2026-11-05): Meshy 7.1 + 유료만 — 무료는 정면 한 장 + 6 Lite(텍스처 없음).
  확인 못 함: 다른 AI 3D 서비스(Tripo·TRELLIS)의 출력 UV·법선 꼴, 스키닝 리그를 그대로 쓰는 길(로더가 스키닝을 안 해서 안 해 봄).
sources:
  - https://docs.meshy.ai/en/webapp/image-to-3d
  - https://www.meshy.ai/pricing
  - https://docs.blender.org/api/4.0/bpy.ops.object.html#bpy.ops.object.bake
---

# AI 3D 메시를 작은 게임용 강체 부위 모델로

## 요약
Meshy 같은 이미지 → 3D 서비스는 수만~십만 삼각형의 한 덩어리 메시와 큰 텍스처를 준다. 화면에서 20~50px로 보이는 캐릭터라면 **정점 합치기 → 줄이기 → 새 UV → 원본 색 굽기 → 면 자리로 부위 자르기 → 기존 뼈에 강체로 붙이기**로 2천 정점대 모델을 만들고, 이미 있는 동작 표를 그대로 쓸 수 있다. 스키닝 없는 로더(PS1식 부위 애니메이션)에서도 된다.

## 본문
1. **입력 그림부터 작게 읽히게**: 화면 키를 먼저 계산한다(카메라 거리·FOV·내부 해상도). 그림 모델에는 "작은 크기에서 읽히게, 넓은 평면색, 평평한 빛, A-pose, 민짜 바탕, 손에 아무것도 없이"를 준다. 가는 소품(칼)은 따로 만든다. 그림을 미리 그 크기로 줄여 보고 거른다([이미지 생성 모델로 게임 일러스트](image-model-for-game-illustrations.md)).
2. **가운데·키**: 옆으로 뻗은 꼬리 같은 것이 경계 상자 가운데를 끌고 가므로 머리(위쪽 일부)로 가운데를 잡는다. 발 = z 0, 앞 = 기존 규칙.
3. **정점 합치기**(거리 1e-4) → **Decimate Collapse**: 목표는 내보낸 glTF 정점(UV 이음매로 갈라진 수 포함)으로 이분 탐색.
4. **새 UV + 굽기**: Smart UV를 크게(조각이 적어야 같은 정점 예산에 삼각형이 많다) → 원본을 selected, 줄인 것을 active로 EMIT 굽기(여백을 둬서 줄여도 안 번지게, 4배 크게 굽고 줄인다). 금속·노멀 맵은 버린다 — 빛은 게임 렌더가 얹는다.
5. **부위 자르기**: 면 가운데 자리 규칙 하나(높이 띠·원기둥 거리)로 나누고, 부위마다 다른 색으로 칠해 앞·옆·뒤·위에서 확인하며 고친다. 팔은 "어깨 → 손끝 선분 둘레 원기둥"이 옷자락·목도리 끝을 덜 섞는다.
6. **뼈·동작**: 뼈 자리만 새 몸에 맞추면 동작 표는 그대로 쓴다. 동작마다 프레임 띠를 찍어 관절 틈·자른 자리를 본다.

## 왜?
- 작은 화면에서 남는 것은 실루엣과 큰 색 덩어리다. 고폴리 조각은 줄여도 거의 안 보이고, 칠한 텍스처가 정점보다 많은 것을 말한다(t3ssel8r식 룩의 "절반은 미술").
- AI 서비스의 리그(스키닝)를 쓰지 않는 까닭: 로더·렌더가 강체 부위만 다루면 스키닝은 새 일과 비용이다. 대신 지금 동작 표·도구(미리보기·검사)를 그대로 쓴다.
- 굽는 까닭: 원래 UV는 조각이 너무 작아 텍스처를 줄이는 순간 경계가 번진다. 새 UV에 다시 구워야 작은 텍스처가 성립한다.

## 함정
- 합치기 전에 줄이면 금이 간다. 구울 이미지를 재질에 이어 두면 검정. 노이즈 제거 없는 Blender 빌드는 조용히 검정.
- 사용자 법선이 남아 있으면 면 매끈/각짐 설정이 먹지 않는다.
- 머리가 큰 캐릭터는 숄더뷰에서 과녁을 가린다 — 카메라 어깨 오프셋은 원근 때문에 가까운 큰 대상에선 다 비켜나지 못한다(knellroot 0038, 다섯 벌 비교).
- 무료 플랜 약관(다운로드 수·버전 제한, CC BY 표기)을 받기 전에 확인한다([작게 보이는 로우폴리 모델](../concepts/readable-low-poly-models.md) verified).

## 관련 노트
- [레트로 3D 모델 파이프라인 — Blockbench → glTF](../reference/assets/retro-3d-models-blockbench-gltf.md)
- [작게 보이는 로우폴리 모델을 읽히게](../concepts/readable-low-poly-models.md)
- [이미지 생성 모델로 게임 일러스트 그리기](image-model-for-game-illustrations.md)
