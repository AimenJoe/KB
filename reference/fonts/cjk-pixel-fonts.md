---
title: 중국어·일본어 픽셀 폰트 — 한자 통합, 글자 범위, 12px 후보
type: reference
tags: [fonts, pixel-art, i18n, localization, licensing, cjk]
status: draft
created: 2026-10-25
updated: 2026-10-25
verified: |
  1차 출처로 확인(2026-10-25, 직접 실행):
  - 파이썬 코덱으로 일본 상용 한자 20자를 GB2312·Big5·Shift_JIS에 넣어 봄: 気楽図駅売読険歩剣闘鉄広戦·働込畑峠 17자가 GB2312·Big5 모두 없음.
    GB2312에는 히라가나·가타카나가 들어 있음.
  - Galmuri 2.40.3(npm galmuri) cmap을 fontTools로 셈: Galmuri11 한자 6,477(JIS X 0208 6,356자 전부, GB2312 한자 3,363/6,763),
    Galmuri11 Condensed·Bold 한자 0(Condensed는 가나 173). README "Legal Stuff": Regular 계열의 라틴-1·가나·한자·일부 한글은 제작자 창작이 아님.
  - Ark Pixel Font 레포(TakWolf/ark-pixel-font, 2026-10-25 develop, 얕은 클론): LICENSE-OFL에 Reserved Font Name 없음. 12px 글자 원본 PNG를
    언어별 파일명(`76F4.png`, `76F4 zh_hant,ja,ko.png`)으로 둔다 — 直·骨의 지역별 모양 차이를 PNG로 직접 확인. 12px(비례) PNG로 계산한 범위:
    JIS 제1수준 한자 2,782/2,965(93.8%), GB2312 1급 3,641/3,755(97.0%), 가나 176/176. 없는 예: 撃 違 縁 概 歓 換(일본어), 搬 陛 餐 窗(간체).
    문서 docs/info-12px-proportional.md의 통계(Shift-JIS 한자 91.5%, GB2312 1급 96.96%)와 대체로 맞음.
  - Fusion Pixel Font 레포(TakWolf/fusion-pixel-font): Ark를 바탕으로 Cubic 11·Galmuri·美咲 등 OFL 계열을 섞음(README 라이선스 표,
    assets/configs/fallback.yaml). 현재 레포 LICENSE-OFL엔 Reserved Font Name이 없지만, npm @fontsource/fusion-pixel-*-jp 5.3.0의 LICENSE에는
    "Reserved Font Name 'Fusion Pixel'"이 있다 — 판마다 다르니 서브셋은 이름을 바꿔 둔다. fontsource 패키지는 라틴 서브셋 파일만 들어 있어 CJK용으로 못 쓴다.
  2차 출처만 있음: 한자 통합(Han unification) 일반 설명, 범CJK 폰트가 언어별 빌드를 내는 이유.
  직접 빌드(2026-10-25): Ark 12px PNG → fontTools FontBuilder TTF(픽셀 줄마다 이어진 칸을 사각형 하나로, upem 1200 = 12px).
    기준선은 pixel-font-knife의 `horizontal_offset` 식(offset_y = baseline − em − bottom_space; 12×12 한자는 −1, 18px 캔버스 라틴은 −4)을 그대로.
    게임 표의 글자만 넣어 일본어 377자 77KB, 간체 406자 100KB. 실제로 없던 글자: 層(일), 奖·摇·纵(간) → 문구를 바꿈.
    macroquad 0.4.16에서 Galmuri와 같은 줄 높이(ascent 1200/descent −200)로 섞어 찍어 어긋남 없음을 헤드리스 Chromium 스크린숏으로 확인.
  확인 못 함: GitHub 릴리스 TTF(이 환경에서 릴리스 다운로드가 막힘), Zpix·PixelMplus·k8x12의 현재 라이선스 원문.
sources:
  - https://github.com/TakWolf/ark-pixel-font
  - https://github.com/TakWolf/fusion-pixel-font
  - https://github.com/quiple/galmuri
  - https://www.unicode.org/iuc/iuc15/a307.html
  - https://unicodefyi.com/zh-hans/glossary/han-unification/
---

# 중국어·일본어 픽셀 폰트

## 요약
**중국어 폰트가 있다고 일본어가 되지 않는다(반대도 마찬가지).** 일본 한자는 간체도 번체도 아닌 일본식 약자(気·楽·図)와 일본에서 만든 글자(働·込)가 많아 중국어 글자 집합에 없고, 같은 코드 포인트라도 지역마다 모양이 다르다(直·骨). 픽셀 게임 12px이면 **Ark Pixel Font(OFL, 언어별 모양)** 원본에서 쓰는 글자만 뽑아 언어별 폰트를 만드는 것이 가장 깨끗하다. 빠진 글자는 문구를 바꾸거나 직접 찍는다.

## 왜 따로인가
| 문제 | 예 | 결과 |
|---|---|---|
| 일본식 약자·일본 고유 글자 | 気(간체 气, 번체 氣), 図, 駅, 働, 込 | 중국어 폰트에 없음 → 빈칸 |
| 한자 통합: 같은 번호, 다른 모양 | 直, 骨 | 찍히긴 하지만 그 나라 사람 눈에 "남의 글씨" |
| 간체 ≠ 번체 | 气/氣, 树/樹 | 간체 폰트로 대만·홍콩은 안 됨 |
| 가나 | GB2312에 포함 | 중국어 폰트로 가나는 나오지만 위 두 문제는 남음 |

## 후보 (12px, 2026-10-25)
| 폰트 | 라이선스 | 일본어 | 간체 | 비고 |
|---|---|---|---|---|
| **Ark Pixel 12px** (TakWolf) | OFL, RFN 없음(레포) | JIS 1수준 93.8% + 가나 전부, ja 전용 모양 | GB2312 1급 97.0%, zh_hans 전용 모양 | 원본이 PNG(언어별 파일명). 제작자 창작 |
| Fusion Pixel 12px | OFL(판에 따라 RFN 'Fusion Pixel') | Ark + 보충 | Ark + 보충 | 여러 OFL 폰트를 꿰맨 것. 릴리스 TTF는 GitHub 릴리스에서 |
| Galmuri11 (Regular) | OFL | JIS X 0208 한자 100% | 63% | 한글 폰트와 같은 가족이라 어울림. 단 가나·한자는 제작자 창작이 아님(README) |
| Cubic 11 | OFL | — | — | 12px 번체(대만) 보충용 |

## 게임에 넣는 법 (서브셋 폰트 + 표)
- 언어마다 폰트 파일 하나. 문자열 표에서 **그 언어가 실제로 쓰는 글자 + 가나 전부 + ASCII**만 뽑아 만들면 수십 KB라 웹 첫 로딩 부담이 없다(전체 한자 폰트는 MB 단위).
- PNG 원본에서 만들 때는 각 검은 픽셀을 정사각형 윤곽으로 바꿔 TTF를 짓는다(fontTools FontBuilder). 언어 고르기: `XXXX <언어>.png`가 있으면 그것, 없으면 `XXXX.png`.
- 빠진 글자가 나오면 빌드를 실패시키고 ① 문구를 바꾸거나(攻撃 → こうげき: 귀여운 톤엔 히라가나가 오히려 맞다) ② 12×12 PNG를 직접 찍어 보충한다.
- 서브셋·가공한 폰트는 OFL의 "수정본"이다. RFN이 있는 판에서 나왔다면 원래 이름을 쓰면 안 된다 → 늘 이름을 바꿔 두면 안전하다. 고지 파일에 OFL 원문과 출처를 싣는다.
- 테스트는 [작은 게임 다국어](../../guides/small-game-localization.md)의 "모든 글자가 폰트 cmap에 있는가"를 언어별 폰트로 돌린다.

## PNG 원본에서 TTF 짓기 (확인한 방법)
- 글자 고르기: `XXXX <언어>.png`가 있으면 그것, 없으면 `XXXX.png`. `proportional/`이 `common/`보다 우선. `monospaced/`는 쓰지 않는다.
- 잉크: 알파 > 127. 줄마다 이어진 잉크 칸을 사각형 윤곽 하나로(시계 방향). 전진 폭 = PNG 폭 × 100.
- 세로 위치: `offset_y = baseline(11) − em(12) − (캔버스높이 − 12)/2`, 픽셀 행 r의 아래 y = `(offset_y + 높이 − 1 − r) × 100`.
- 줄 높이(hhea)는 함께 쓰는 한글 폰트와 같게 두면 언어를 바꿔도 화면 배치가 그대로다.
- 넣는 글자: 그 언어 문자열 표 + ASCII + 코드에 직접 쓴 UI 기호(▶ ♥ …) + (일본어) 가나 전부. 표에 없는 글자를 실수로 쓰면 커버리지 테스트가 잡는다.
- 없는 기호는 같은 격자의 OFL 폰트(예: Galmuri Condensed)에서 윤곽을 복사해 와도 된다. 한자가 없으면 빌드를 실패시키고 문구를 바꾼다.

## 함정
- npm `@fontsource/fusion-pixel-*`는 웹용 라틴 조각만 들어 있다(CJK는 CDN 조각 로딩용이라 패키지에 없음).
- 번체는 별개 언어다. 대만(zh-TW)과 홍콩(zh-HK)도 모양 기준이 다르다.
- 같은 12px라도 한글 폰트(Galmuri Condensed)보다 한자 칸이 넓다(12×12). 한 줄 길이는 글자 수가 줄어 대개 비슷하지만 화면으로 확인한다.

## 관련 노트
- [작은 게임 다국어 구조](../../guides/small-game-localization.md)
- [그림 못 그려도 도트 게임 만들기](../../guides/pixel-art-without-an-artist.md) — 한글 UI 폰트(Galmuri) 서브셋
