---
title: 그림 못 그려도 도트 게임 만들기 (에셋 전략)
type: guide
tags: [gamedev, pixel-art, assets, licensing, solo-dev]
status: draft
created: 2026-10-24
updated: 2026-10-25
verified: |
  1차 출처로 확인: 없음. 특정 에셋 팩의 현재 라이선스는 확인하지 않았다 — 내려받을 때 반드시 팩의 라이선스 파일을 직접 읽을 것.
  2차 출처/경험: 1인 개발 통념(한 팩 중심, 해상도 통일, Aseprite 손보기). Creative Commons 라이선스 종류 자체는 공식 정의를 따른다.
sources:
  - https://creativecommons.org/share-your-work/cclicenses/
  - https://itch.io/game-assets/free/tag-pixel-art
  - https://opengameart.org/
---

# 그림 못 그려도 도트 게임 만들기

## 요약
에셋 팩 **하나를 메인으로 정하고 세계를 거기 맞춘다.** 해상도(16×16 등)와 팔레트를 통일하고, 부족한 건 그리기가 아니라 "손보기"(팔레트 교체, 반전, 합성)로 채운다. 라이선스는 팩마다 다르니 받을 때마다 확인한다.

## 절차

1. **해상도와 내부 화면을 먼저 정한다.** 타일 16×16, 내부 해상도 320×180이면 팩도 16×16 기준으로만 본다. 32×32 팩을 섞으면 선 두께가 달라 바로 티가 난다. → [픽셀 퍼펙트 렌더링](../reference/macroquad/pixel-perfect-rendering.md)
2. **메인 팩을 고른다. 기준은 "주인공 애니메이션 종류".** 대기·이동·공격·회피·피격·사망이 있는 캐릭터 팩이 먼저다. 전투감의 절반은 애니메이션 타이밍이라 프레임이 부족한 주인공은 나중에 반드시 발목을 잡는다. 타일셋·적·UI는 그 팩 작가의 다른 팩이나 같은 팔레트 계열에서 보충한다.
3. **라이선스를 읽는다.** 자주 보이는 종류:
   - CC0: 제한 없음. 출처 표기 불필요.
   - CC-BY: 상용 가능, 출처 표기 필수(크레딧 화면에 적는다).
   - CC-BY-NC: 비상용만. 판매·광고 수익이 있으면 쓸 수 없다.
   - 작가 고유 라이선스: "게임에 포함 가능, 에셋 재배포 금지"가 보통이다. 레포를 공개할 거면 **에셋을 공개 레포에 넣어도 되는지**가 별도 질문이다.
   확인한 내용은 레포의 `assets/LICENSES.md`에 팩 이름·작가·URL·라이선스·받은 날짜로 기록한다.
4. **손보기 도구는 Aseprite 하나로 충분하다.** 그림 실력 없이 되는 것: 팔레트 교체(적 바리에이션은 색만 바꿔도 된다), 좌우 반전, 두 스프라이트 합성(몸 + 장비), 프레임 복제·타이밍 조절, 이펙트는 단색 도형 몇 프레임.
5. **공개 레포라면 에셋은 분리한다.** 재배포 불가 팩은 `.gitignore` 하거나 private 서브모듈/릴리스 첨부로 두고, 레포에는 `assets/README.md`에 "어디서 받아 어디에 두는지"를 적는다.

## 함정
- 팩 여러 개를 섞으면 해상도가 같아도 **팔레트와 외곽선 스타일**(검은 외곽선 유무, 선 두께)이 달라 어색하다. 섞어야 하면 팔레트를 메인 팩 것으로 재매핑한다.
- 캐릭터 후보(해금 캐릭터 등)는 세계관으로 먼저 정하지 말고 **쓸 수 있는 팩에 그 동물·직업이 있는지**로 먼저 거른다.
- 무료 팩은 작가가 라이선스를 바꾸거나 내릴 수 있다. 받은 시점의 라이선스 파일을 함께 보관한다.

## 한글 UI 폰트 (에셋 팩과 별개의 인프라)
게임 엔진 내장 폰트에는 한글이 없다. 픽셀 게임에 맞는 한글 폰트는 다음 조건으로 고른다: OFL 같은 재배포 허용 라이선스, 픽셀 격자(8·10·12px)에 맞는 윤곽선 TTF, 2,350자 이상.

- **Galmuri** ([quiple/galmuri](https://github.com/quiple/galmuri), OFL 1.1): Galmuri14/11/9/7. README "Legal Stuff"에 따르면 Regular 계열은 일부 글리프(라틴-1, 가나·한자, 일부 기호, 한글 2,355자)가 닌텐도 DS 폰트에서 유래하고, **Galmuri11 Bold·Condensed는 모든 글리프가 제작자의 순수 창작**이다. 걱정 없이 쓰려면 Bold나 Condensed. 320×180이면 Condensed(12px 격자)가 글자 수를 벌어 준다.
- 용량: 원본 TTF는 2.6MB(한글 11,172자). 웹 첫 로딩을 위해 서브셋한다. `pyftsubset`(fonttools)로 KS X 1001 완성형 2,350자 + ASCII + Latin-1(ï 등) + 필요한 기호(▶◀♥♡■□…·)만 남기면 약 450KB.
  ```sh
  pip install fonttools
  python3 -c "print(''.join(chr(c) for c in range(0xAC00,0xD7A4) if (lambda b: b and 0xB0<=b[0]<=0xC8 and 0xA1<=b[1]<=0xFE)(chr(c).encode('cp949','ignore'))), end='')" > ksx1001.txt
  pyftsubset Galmuri11-Condensed.ttf --text-file=ksx1001.txt --unicodes="U+0020-007E,U+00A0-00FF,U+2010-2027,U+2190-2193,U+25A0-25CF,U+2660-2667,U+3131-318E" --output-file=assets/fonts/Galmuri11-Condensed.ttf --name-IDs='*'
  ```
  파이썬 `euc_kr` 코덱은 11,172자를 모두 인코딩하므로(cp949 호환) 2,350자 필터는 EUC-KR 순수 2바이트 영역(B0A1~C8FE)으로 거른다. 서브셋 밖 글자(예: 똠)는 안 나오니 UI 문구를 쓸 때 기억한다.
- 라이선스는 `assets/LICENSES.md`에 파일·출처·라이선스·가공 내용을 표로 남긴다(OFL은 폰트 파일 name 테이블에도 명시돼 있다).
- macroquad에서 찍는 법: [reference/macroquad/pixel-perfect-rendering.md](../reference/macroquad/pixel-perfect-rendering.md) "텍스트" 항목.

## 관련 노트
- [concepts/action-roguelite-for-solo-dev.md](../concepts/action-roguelite-for-solo-dev.md)
- [reference/macroquad/pixel-perfect-rendering.md](../reference/macroquad/pixel-perfect-rendering.md)
