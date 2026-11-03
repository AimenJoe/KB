---
title: 게임 UI용 한글 명조 — 고운바탕 vs 함렛, 가변 글꼴과 macroquad, 서브셋 크기
type: reference
tags: [fonts, i18n, macroquad, licensing, hud]
status: draft
created: 2026-11-03
updated: 2026-11-03
verified: |
  1차 출처로 확인(2026-11-03, fontTools로 직접 셈 · Google Fonts 레포 원본 · fontdue 0.9.5 소스):
  - 고운바탕 Regular(google/fonts ofl/gowunbatang): 한글 음절 11,172/11,172, KS X 1001 2,350/2,350, 라틴 확장 A 127/128, ◆◇…·▲▼▶ 있음, 키릴·가나·한자 0, 정적 glyf, 8.2MB. Bold 파일 따로.
  - 함렛(ofl/hahmlet, Hahmlet[wght].ttf): 가변 wght 100~900(기본 400), 한글 음절 2,788/11,172, KS X 1001 2,350/2,350, 라틴 확장 A 124/128, 3.5MB.
  - 두 OFL.txt 모두 Reserved Font Name 없음. NeoDunggeunmo LICENSE(neodgm-webfont)는 RFN "Neo둥근모"·"NeoDunggeunmo" 있음.
  - fontdue 0.9.5 소스에 가변 축(variation) 설정 API가 없다 → macroquad `load_ttf_font_from_bytes`로 가변 글꼴을 넣으면 기본 인스턴스만 나온다.
  - 서브셋(fontTools, 표 글자 439자 + 라틴): 고운바탕 보통 95KB·굵게 93KB. KS X 1001 2,350자를 다 넣으면 두 파일 2.7MB.
  확인 못 함: 함렛을 varLib.instancer로 굵기 고정했을 때의 결과(이번엔 안 만듦), 작은 크기(13px 1배)에서의 실기 가독성.
sources:
  - https://github.com/google/fonts/tree/main/ofl/gowunbatang
  - https://github.com/google/fonts/tree/main/ofl/hahmlet
  - https://github.com/neodgm/neodgm
  - https://github.com/mooman219/fontdue
---

# 게임 UI용 한글 명조

## 요약
어두운 판타지 분위기의 게임 UI에 명조를 쓸 때, OFL 후보 중 **고운바탕**이 엔진 호환성이 가장 좋다: 한글 11,172자 전부, 보통·굵게가 따로 된 정적 파일. **함렛**은 멋있지만 한글이 2,788자뿐이고 가변 글꼴 하나라, 가변 축을 못 고르는 엔진(macroquad = fontdue)에서는 기본 굵기만 나온다. 어느 쪽이든 원본(수 MB)을 그대로 싣지 말고 **쓰는 글자만 서브셋**(수십~백 KB)하고, 빠진 글자를 시험으로 잡는다.

## 비교
| | 고운바탕 | 함렛 | (참고) 네오둥근모 |
|---|---|---|---|
| 한글 음절 | 11,172 | 2,788 | 11,172 |
| 파일 | 보통·굵게 정적 | 가변 하나(wght 100~900) | 정적, 16px 격자 픽셀 |
| 라틴 확장 A | 127/128 | 124/128 | 1/128 |
| 라이선스 | OFL, RFN 없음 | OFL, RFN 없음 | OFL, **RFN 있음** → 서브셋은 이름 바꾸기 |
| 원본 크기 | 8.2MB(굵게 8.2MB) | 3.5MB | 수 MB |

키릴·가나·한자는 셋 다 없다 — 그 언어는 언어별 글꼴을 따로(KB [CJK 픽셀 폰트](cjk-pixel-fonts.md)).

## 넣는 법
- 서브셋: i18n 표의 모든 문자열에서 글자를 모으고 + ASCII·라틴-1·라틴 확장 A + 코드에 직접 쓰는 기호. fontTools `Subsetter`(힌팅 버림, `kern` 유지).
- 시험: 표의 모든 글자가 **두 파일 모두**의 cmap에 있는가(굵게만 빠지는 실수를 잡는다).
- 가변 글꼴을 꼭 써야 하면 `fontTools.varLib.instancer`로 원하는 굵기의 정적 인스턴스를 만든 뒤 서브셋.
- 명조는 픽셀 격자가 아니므로 텍스처 필터는 Linear, 크기는 자유(픽셀 글꼴처럼 격자 배수에 맞출 필요 없음).

## 왜?
- 글자 수가 모자라면 번역·이름에 쓴 한 글자 때문에 빈칸이 생긴다. KS X 1001(2,350자)은 일상어 대부분이지만 "똠·쀍" 같은 조합은 없다 — 11,172자 글꼴이면 그 걱정이 없다.
- 가변 글꼴은 웹 CSS에서는 편하지만, 게임 엔진의 글자 래스터라이저(fontdue·stb_truetype 계열)는 축을 지원하지 않는 경우가 많다.
- 명조는 글자 하나의 윤곽이 무거워(곡선·세리프) 2,350자만 넣어도 1MB를 넘는다 — 웹 게임에서는 표 글자 서브셋이 맞다.

## 함정
- 개발 메뉴처럼 표 밖에서 쓰는 영어 글도 서브셋에 들어가야 한다(라틴 블록을 통째로 넣으면 안전).
- 큰 제목만 굵게 쓰면 굵게 파일의 글자 집합도 똑같이 맞춘다.

## 관련 노트
- [CJK 픽셀 폰트](cjk-pixel-fonts.md)
- [작은 게임 다국어](../../guides/small-game-localization.md)
