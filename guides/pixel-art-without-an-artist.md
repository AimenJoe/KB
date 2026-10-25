---
title: 그림 못 그려도 도트 게임 만들기 (에셋 전략)
type: guide
tags: [gamedev, pixel-art, assets, licensing, solo-dev]
status: draft
created: 2026-10-24
updated: 2026-10-25
verified: |
  1차 출처로 확인: 직접 실행(2026-10-25, nail-under-the-roots): 문자 격자 + 자동 외곽선 스프라이트 생성, 흰 실루엣 플래시,
  환경 색조·장식·어둠 마스크, 비공개 에셋 레포 checkout CI 단계(YAML 검증). Sunnyside World 라이선스 V1은 itch.io 페이지 원문으로 확인(2026-10-25).
  그 밖의 팩(Gridwright, DeepDive)은 원문 미확인 — 내려받을 때 반드시 팩의 라이선스를 직접 읽을 것.
  2차 출처/경험: 1인 개발 통념(한 팩 중심, 해상도 통일, Aseprite 손보기). Creative Commons 라이선스 종류 자체는 공식 정의를 따른다.
sources:
  - https://creativecommons.org/share-your-work/cclicenses/
  - https://itch.io/game-assets/free/tag-pixel-art
  - https://opengameart.org/
  - https://danieldiggle.itch.io/sunnyside
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

## 3/4 탑다운 16×16 팩 후보 (2026-10-25 조사, 2차 출처: itch.io 페이지 요약)
"귀여운 동물 + 3/4 탑다운 + 16×16 + 상업 가능"을 모두 만족하는 팩은 없었다. 동물(두더지·고슴도치·아르마딜로·개미핥기)은 어느 팩에도 없어서 **캐릭터는 따로 그리거나 의뢰**하고, 팩은 타일·소품·UI·적 템플릿으로 쓴다고 생각해야 한다.

| 팩 | 내용 | 라이선스(페이지 기준, 구매 전 재확인) |
|---|---|---|
| [Sprout Lands](https://cupnooble.itch.io/sprout-lands-asset-pack) (Cup Nooble) | 농장 타일·소품, 닭·소·양 | 무료판 비상업, 프리미엄($3.99+) 상업 가능, 재배포 금지 |
| [Mystic Woods](https://game-endeavor.itch.io/mystic-woods) (Game Endeavor) | 숲 타일·소품, 슬라임·해골 등 적, 16×16 탑다운 | 무료판 비상업, 유료판 상업 가능 |
| [Sunnyside World](https://danieldiggle.itch.io/sunnyside) (danieldiggle) | 타일셋, 사람·고블린 20동작 | **원문 확인(V1, 2026-10-25)**: 무료·상업 사용, 수정 가능, 크레딧 불필요. 재배포는 튜토리얼·교육 과정에 링크와 함께만. 수정해도 재포장·재판매 금지(NFT 포함). AI 학습 금지. Name your own price. 동물 없음 → 공개 레포엔 넣지 않는다 |
| [Gridwright Animals & Pets](https://v3su.itch.io/animals-pets-16x16-pixel-art-top-down-sprites) | 15종 32마리 탑다운 동물(고슴도치 포함), 4방향 | "Royalty Free" 표기, 원문 미확인 |
| [Animal Asset Pack 16×16](https://deepdivegamestudio.itch.io/animalassetpack) (DeepDive) | 45종 동물 스프라이트, 판타지·로그라이크 톤 | Name your own price, 원문 미확인 |

고르는 기준: (1) 바닥·벽 타일과 소품이 먼저(방이 게임의 80%), (2) 적 템플릿이 있으면 팔레트를 맞춰 동물로 고친다, (3) 팔레트가 좁은 팩이 섞어 쓰기 쉽다. 두더지 주인공은 어차피 직접 그려야 하니 팩의 팔레트·해상도에 맞춰 그린다.

## 공개 레포에서 유료 팩 다루기
- "게임에 넣어 배포는 되지만 에셋 자체의 재배포·재판매는 금지"는 유료 팩의 흔한 조건이다. **공개 GitHub 레포에 원본 PNG를 커밋하면 누구나 원본을 받아 갈 수 있어 재배포로 볼 여지가 크다.** 레포가 공개인지 먼저 확인한다.
- 분리 방법: 팩은 `assets/vendor/`(gitignore)에 두고, CI는 비공개 에셋 레포를 `actions/checkout`(repository·token 입력)으로 같은 경로에 받는다. 시크릿이 없으면 대체 그림으로 빌드되게 해 두면 외부 기여자 PR도 깨지지 않는다.
  ```yaml
  - name: Fetch vendor assets (private repo)
    if: env.ASSETS_REPO != ''          # job env: ASSETS_REPO: ${{ secrets.ASSETS_REPO }}
    uses: actions/checkout@v4
    with: { repository: ${{ secrets.ASSETS_REPO }}, token: ${{ secrets.ASSETS_TOKEN }}, path: assets/vendor }
  ```
  `secrets`는 `if:`에서 직접 못 쓰므로 job `env`로 옮겨 검사한다.
- "AI 학습 금지" 조항이 있는 팩은 이미지를 생성형 AI 도구(업스케일·스타일 변환 포함)에 넣지 않는다.

## 직접 찍기: 코드로 그리는 스프라이트
- 문자 격자(한 글자 = 한 픽셀, 글자 = 팔레트 색)로 채움만 적고 **외곽선은 자동**(채운 칸에 4방향으로 닿은 빈 칸)으로 두르면, 부위를 옮겨 동작 프레임을 만들어도 외곽선이 깨지지 않는다. 걷기는 1px 통통 튀기 + 발 이동, 공격은 상체 기울기 + 발 위치, 피격은 눈 모양 교체로 원본에서 파생한다.
- 피격 흰 플래시는 셰이더 없이 **흰 실루엣 줄**을 시트에 함께 만들어 그 칸을 그리면 된다.
- 원본 스크립트를 레포에 두고 PNG는 산출물로 커밋한다. 손으로 PNG를 고치면 다음 생성에서 사라진다.
- 도구로 다듬을 때(2026-10, 기억 기반, 가격·라이선스는 각 사이트에서 재확인): **Aseprite**(유료, 소스 공개 EULA, 산출물 상업 사용 가능), **LibreSprite**(Aseprite 옛 버전의 GPL 포크, 무료), **Pixelorama**(MIT, 무료, 웹판 있음). AI 스프라이트 생성기는 산출물 권리·스타일 일관성·팩 라이선스(AI 금지) 문제를 먼저 확인한다.

## 3/4 환경을 "깊이"로 바꾸기
같은 타일에 색조(바닥·벽 따로), 장식표(꽃 → 뿌리·조약돌 → 이끼·빛나는 버섯), 바닥 재질(풀 → 흙), 화면 어둠(플레이어 주변만 밝은 원형 마스크)을 단계별로 입히면 타일 세트를 더 사지 않고도 "내려갈수록 어둡고 음습해지는" 흐름이 나온다. 칸 경계가 보이지 않게 반대 재질 얼룩(가장자리 불규칙, 투명 배경)을 반 칸 어긋나게 덮는다. 빛나는 장식은 어둠을 그린 뒤 한 번 더 그린다.

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
