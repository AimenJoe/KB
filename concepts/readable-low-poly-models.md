---
title: 작게 보이는 로우폴리 모델을 읽히게 — 깊이·외곽선·빛 단계·실루엣, 그리고 하지 말 것
type: concept
tags: [gamedev, 3d, rendering, art, low-poly, macroquad, ai-assets]
status: draft
created: 2026-11-04
updated: 2026-11-04
verified: |
  1차 출처로 확인(knellroot 0033, 2026-11-04 — 직접 구현·헤드리스 Chromium 스크린숏·개발 줄):
  - 렌더 타깃 깊이 버퍼가 없어(macroquad `render_target` 기본) 모델 부위·벽이 그린 순서로 엉켰다 → 깊이를 붙이자 효과 없이도 모델이 읽혔다. 비용은 헤드리스에서 차이 없음.
  - 키운 상자 뒷면 외곽선(축마다 부호로 밀기 + 앞면 버리는 재질, 두께 = 그 거리의 화면 1px)은 깊이가 있어야만 된다(없을 때 앞면·뒷면 컬링 둘 다 몸을 덮었다). 배우 정점 ×2, 잡몹 80에서 CPU 6.0 → 10.1ms(소프트웨어 GL, 상대값).
  - 껍데기를 카메라에서 0.18m 뒤로 밀면(knellroot 0035) 30px 배우의 안쪽 선이 줄어 몸이 까맣게 뭉개지지 않고 바깥 테는 남는다(전·후 스크린숏).
  - 빛 단계(달빛 2단·화로 3단)는 상자 면엔 거의 차이가 없고(면이 이미 평평) 바닥의 빛 웅덩이를 또렷한 고리로 바꾼다.
  - 쿼터뷰 픽셀 밀도(tuning 기본값으로 셈): 1m ≈ 17.6px, 키 1.8m 캐릭터 ≈ 30px — 2~3cm 베벨은 1px 미만.
  2차 출처만 있음: hull 외곽선이 후처리(깊이·법선 가장자리)보다 싸고 안쪽 선이 없다는 비교(MS MixedReality MeshOutlines 문서 성격), 모바일에서 깊이 텍스처 후처리가 비싸다(포럼).
  AI 3D 생성 약관(서브에이전트 조사, 2026-11-04): Meshy 무료 = CC BY 4.0·유료 = 소유(도움말 1차), Hunyuan3D 2.x 라이선스는 한국·EU·영국 제외(라이선스 원문 미러 1차),
  Meshy 요금 페이지(1차, 2026-11-04 확인): 무료 = 월 100 크레딧·**다운로드 월 10개, Meshy 6 Lite 모델만**(Meshy 6 정식으로 만든 것은 못 받는다)·CC BY 4.0(상업 사용 가능, 출처 표기), Pro 월 $20 = 다운로드 무제한·"Private & Customer owned". 형식은 fbx·obj·usdz·glb·stl·blend(FAQ). 요금·한도는 자주 바뀐다.
  TRELLIS.2 = MIT(모델 카드 1차), Tripo 무료 출력은 Tripo 권리(도움말 요약만 — 원문 403), Rodin 약관은 확인 못 함. Synty는 공개 레포 재배포 불가(EULA 1차), Kenney·Quaternius CC0(2차 포함).
  확인 못 함: 외곽선의 실제 폰·WebGL 비용, Blockbench glTF 내보내기 옵션 이름, AI 생성 저폴리 품질(판매사 자료뿐).
sources:
  - https://github.com/not-fl3/macroquad/blob/master/src/texture.rs
  - https://github.com/not-fl3/miniquad/blob/master/src/graphics/gl.rs
  - https://docs.blender.org/manual/en/4.0/render/cycles/baking.html
  - https://www.blockbench.net/wiki/docs/bbmodel
  - https://raw.githubusercontent.com/jasonjgardner/blockbench-mcp-plugin/HEAD/headless/README.md
  - https://help.meshy.ai/en/articles/9992001-can-i-use-my-generated-assets-for-commercial-projects
  - https://www.meshy.ai/pricing
  - https://huggingface.co/tencent/Hunyuan3D-2/blob/main/LICENSE
  - https://huggingface.co/microsoft/TRELLIS.2-4B
  - https://syntystore.com/pages/one-time-purchase-licence
  - https://quaternius.com/packs/universalanimationlibrary.html
  - https://www.github.com/microsoft/MixedReality-GraphicsTools-Unreal/blob/main/Docs/MeshOutlines.md
---

# 작게 보이는 로우폴리 모델을 읽히게

## 요약
쿼터뷰에서 캐릭터는 화면 30px 남짓이다. 이 크기에서 "상자 더미" 인상을 바꾸는 것은 지오메트리 디테일(베벨·폴리곤)이 아니라 **실루엣과 명도**다. 고치는 순서는 ① 깊이 버퍼가 실제로 있는지부터(없으면 부위가 엉켜 무엇을 해도 소용없다) ② 렌더 쪽(외곽선·빛 단계·가장자리 빛 — 모든 모델에 한 번에) ③ 모델 하나로 실루엣·비율·텍스처 고유 칸 시범 ④ 그래도 모자라면 사람이 텍스처만 칠하기. AI 3D 생성·에셋 팩은 화풍·리그·폴리 예산·약관이 맞을 때만.

## 본문

### 먼저 셈: 몇 px로 보이나
- 1m가 화면 몇 px인지 = `내부 세로 / (2·거리·tan(시야/2))`. 쿼터뷰(거리 20, 42°, 세로 270)는 ≈17.6px/m, 숄더뷰(거리 7, 58°)는 ≈35px/m.
- 그 아래 디테일(베벨 2~3cm, 작은 장식)은 1px도 안 된다 — 만들어도 안 보인다. 반대로 머리·손·무기를 키우고 명도를 3단(어둠·중간·밝음)으로 가르면 바로 보인다(일반적인 미술 원칙 — 출처로 확인하진 않았다).

### 렌더 쪽(값싼 순)
| 방법 | 하는 일 | 비용 |
|---|---|---|
| 깊이 버퍼 확인 | 부위·벽이 그린 순서로 엉키는 것을 없앤다 | 거의 0 |
| 빛 단계(툰) | 정점 빛을 2~3단으로 끊는다 — 바닥 빛 웅덩이가 또렷해진다. 평평한 상자 면엔 차이가 작다 | 0(정점 색 굽기 안) |
| 가장자리 빛 | `(1 - n·v)²` × 차가운 색 — 어두운 바닥 위 실루엣 | 0 |
| 껍데기 외곽선 | 부위마다 상자를 키운 뒷면만 어둡게 — 바깥 테 + 부위 사이 선 | 배우 정점 ×2, 재질 하나 |
| 깊이 후처리 외곽선 | 안쪽 선까지 | 패스 하나 + 깊이 텍스처(WebGL1 확장) |
| 팔레트·디더 후처리 | 화풍 통일(t3ssel8r 쪽) | 셰이더 하나 |

- 껍데기 외곽선: 면마다 정점이 따로인 상자는 **법선으로 밀면 모서리가 벌어진다** → 상자 가운데에서 축마다 부호로 민다. 두께는 그 거리의 화면 1px(위 셈)로 — 쿼터뷰·숄더뷰 어디서나 1px.
- 부위마다 껍데기를 두면 부위 사이에도 선이 생긴다. 큰 모델(숄더뷰 보스)엔 좋지만 작은 배우는 안쪽 선이 몸을 덮는다 → **껍데기 정점을 카메라에서 조금(0.1~0.2m) 뒤로 민다**: 뒤 부위가 그만큼 떨어진 곳에만 안쪽 선이 남는다.

### 모델 쪽
- 스크립트로 계속 만든다면: 실루엣(후드 끝·망토 자락 쐐기, 어깨 덧), 비율(머리·손·무기 크게), 텍스처 고유 칸(얼굴·가슴·띠), 위 모서리 1px 밝은 선(가짜 베벨). 판정은 미리보기가 아니라 **게임 안 스크린숏**으로(미리보기는 입체감을 과장한다).
- 손으로: Blockbench(`.bbmodel`은 JSON이라 글로 쓸 수는 있지만 공개 사양이 없고, glTF 내보내기는 사람이 GUI에서). 사람 시간이 아까우면 "지오메트리는 코드, 텍스처만 사람" 이 가장 싸다.
- AI 3D 생성(Meshy·Tripo·TRELLIS·Hunyuan3D): 유기적 형태엔 강하지만 폴리 예산이 10배 넘고(리메시 프리셋이 수천부터), 리그가 스키닝이라 부위 강체 파이프라인과 안 맞고, 약관이 서비스마다 갈린다(위 verified — **Hunyuan3D는 한국 제외**). 쓴다면 공개 문구(Steam 등)와 출처 표기.
- 에셋 팩: CC0(Kenney·Quaternius)는 쓸 수 있지만 화풍이 밝고 휴머노이드 스키닝. Synty는 공개 레포에 넣을 수 없다.

## 왜?
작게 보이는 대상에서 사람은 덩어리 모양(실루엣)과 밝고 어두움의 대비로 먼저 알아본다. 지오메트리를 늘리는 것은 그 두 가지를 바꾸지 못하면 비용만 든다. 렌더 쪽 장치(외곽선·빛 단계)는 모든 모델에 한 번에 걸리고 되돌리기 쉬워서 먼저 시험할 값어치가 있다. 그리고 그 전에 **화면이 지금 맞게 그려지는지**(깊이)부터 봐야 한다 — 틀린 그림 위에서 화풍을 판정하면 엉뚱한 것을 고친다.

## 함정
- 깊이 없는 렌더 타깃: 오류가 없어 화풍 문제로 착각한다(→ [macroquad 3D](../reference/macroquad/3d-rendering.md)).
- 외곽선 컬링 방향은 렌더 타깃 뒤집기·감김에 따라 바뀐다 — 스크린숏 한 장으로 정한다. 깊이가 없으면 어느 쪽이든 몸을 덮는다.
- 툰 빛을 켜고 끄면 미리 구운 지형도 다시 구워야 한다(빛이 정점에 있다).
- 깊이를 붙이면 그동안 순서로만 가려지던 것이 드러난다 — 바닥 아래 "허공 판"이 꺼진 땅(배경 높낮이)을 덮었다. 배경 판은 가장 낮은 지형보다 아래로.
- 비용은 데스크톱 헤드리스로 상대값만 — 폰은 따로 잰다.

## 관련 노트
- [macroquad 3D 렌더링](../reference/macroquad/3d-rendering.md)
- [레트로 3D 모델 파이프라인 — Blockbench → glTF](../reference/assets/retro-3d-models-blockbench-gltf.md)
- [게임 손맛: 입자와 빛](game-feel-particles-and-light.md)
