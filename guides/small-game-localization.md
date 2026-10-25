---
title: 작은 게임 다국어(현지화) 구조 — 고정 키 표, 자리표시자, 폰트 커버리지 테스트
type: guide
tags: [gamedev, i18n, localization, fonts, rust, testing]
status: draft
created: 2026-10-25
updated: 2026-10-25
verified: |
  1차 출처로 확인: 직접 실행(2026-10-25, nail-under-the-roots, Rust + macroquad 0.4.16): 언어별 `static Strings` 구조체(키 누락 = 컴파일 에러),
  `{0}` 자리표시자 + 언어 간 일치 테스트, 선호 목록 고르기(navigator.languages를 ['ja-JP','ko-KR'] / ['fr-FR','de'] / ['ko-KR']로 바꿔
  각각 한국어·영어·한국어로 시작함을 헤드리스 Chromium에서 확인), TTF cmap(형식 4·12)을 직접 읽는 폰트 커버리지 테스트(fontTools 결과와 교차 확인 — 285자 모두 있음,
  가나 'あ'는 없음), 헤드리스 Chromium `locale` 옵션으로 ko-KR/en-US 화면 스크린숏을 찍어 영어에서 넘치는 곳 3군데를 찾아 고침.
  sys-locale 0.3.2 소스(src/android.rs가 `__system_property_get("persist.sys.locale")`, wasm은 wasm-bindgen 선택 기능)를 읽음.
  Galmuri11 Condensed(npm galmuri 2.40.3)의 cmap: 가나 있음(히라가나 82·가타카나 84), 한자(U+4E00–9FFF) 0, 키릴 140.
  2차 출처만 있음: 현지화 일반 원칙(고정 ID, 텍스트 팽창 30~50%, 의사 현지화, 문장 조각 잇기 금지, 폰트 폴백) — 업체·블로그 글.
  Steam 언어 비율(영어·중국어 간체가 1·2위를 오감, 러시아어 3위)은 월별 보도이며 Valve 보정 논란이 있다.
sources:
  - https://translated.com/resources/game-localization-developer-guide
  - https://alconost.com/en/blog/game-localization-rework
  - https://bugnet.io/blog/game-localization-testing-common-bugs
  - https://www.gamingonlinux.com/2026/10/steam-survey-for-september-2026-shows-a-drop-in-linux-with-simplified-chinese-rising/
  - https://github.com/1Password/sys-locale
  - https://github.com/quiple/galmuri
---

# 작은 게임 다국어 구조

## 요약
글 100~수백 개, 언어 2~3개인 1인 게임이면 **언어별 문자열 표 하나 + 고정 키 + 테스트 세 개**(폰트 커버리지, 자리표시자 일치, 빈 글)가 가장 싸다. 번역 크레이트·외부 파일은 언어가 늘거나 번역가가 코드 밖에서 일할 때 도입한다. 가장 흔한 사고는 "번역은 있는데 서브셋 폰트에 글자가 없음"과 "영어가 길어서 넘침"이다.

## 절차
1. **글을 코드에서 빼서 표로**: 키 = 의미 있는 고정 이름(`gift_title`), 값 = 언어별 글. Rust라면 `struct Strings { gift_title: &'static str, … }`와 언어마다 `static KO/EN: Strings` — 한 언어라도 필드가 빠지면 컴파일이 안 된다. 키 목록은 매크로 한 번으로 구조체와 `all()`(테스트용 열거)을 같이 만든다.
2. **데이터 표는 글 대신 "글을 고르는 함수"를 든다**: `type Tr = fn(&Strings) -> &'static str;` 무기·퀘스트·대사 표에 `name: |s| s.w_mole`. 게임 로직은 언어를 모르고, 그릴 때만 지금 언어로 꺼낸다.
3. **숫자는 자리표시자**: `"{0}연타 · 마지막 타 피해 {1}"` / `"{0}-hit combo · finisher damage {1}"`. 위치 번호라 어순이 달라도 된다. 문장을 조각으로 이어 붙이지 않는다.
4. **시작 언어 = 기기 언어, 설정에서 바꿈**: 첫 선호 언어만 보지 말고 **선호 목록을 앞에서부터 보고 가진 첫 언어**, 하나도 없으면 영어. 일본어·한국어 순으로 둔 사람은 한국어를, 프랑스어·독일어만 둔 사람은 영어를 받는다. 웹은 `navigator.languages`, 네이티브는 OS 선호 목록(`sys_locale::get_locales()`). 언어 이름은 그 언어로 쓴다("한국어", "English").
5. **테스트 세 개**(CI): (a) 모든 언어의 모든 글자가 쓰는 폰트의 cmap에 있는가 (b) 같은 키의 자리표시자 집합이 언어끼리 같은가 (c) 빈 글이 없는가.
6. **두 언어로 화면을 찍어 본다**: 헤드리스 브라우저의 로캘 옵션(Playwright `newContext({ locale })`)으로 언어별 스크린숏. 고정 폭 칸·한 줄 안내가 넘친다. 칸 폭은 가장 긴 글에 맞추고 긴 안내는 줄바꿈한다.

## macroquad(wasm-bindgen 없음)에서 브라우저 언어 읽기
- `sys-locale`은 웹에서 wasm-bindgen 선택 기능을 쓴다. macroquad는 wasm-bindgen을 쓰지 않으므로 **wasm에서는 빼고** 작은 miniquad 플러그인으로 읽는다: `index.html`에서 `miniquad_add_plugin({ name, version, register_plugin(io) { io.env.nail_locale = () => … } })`, Rust는 `extern "C" { fn nail_locale(i: u32) -> u32; }` — i번째 선호 언어의 주 언어 두 글자를 `(c0 << 8) | c1` 정수로 접어 받고 0이면 끝. 문자열을 넘기지 않고, 지원 언어 목록은 Rust 쪽(`Lang::from_tag`) 한 곳에만 둔다. 링크는 `--import-undefined`(wasm-build 노트).
- 플러그인에 `name`·`version`을 주면 번들이 `<name>_crate_version` 내보내기를 찾는다. 없으면 콘솔 로그만 남지만, 같은 값을 돌려주는 `#[no_mangle] extern "C" fn` 하나를 두면 깔끔하다.
- 옛 `index.html`(플러그인 없음)에서는 번들이 빈 함수를 끼워 넣어 `undefined` → 0이 된다. 0을 "모름"으로 두면 안전하다.
- 데스크톱·Android는 `sys-locale`(Android는 시스템 속성 `persist.sys.locale`).

## 폰트
- 서브셋 폰트는 언어를 늘릴 때마다 다시 만든다. 일본어는 가나만으로도 쓸 수 있지만(어린이용 게임의 히라가나 모드처럼) 한자가 필요하면 한자 있는 픽셀 폰트를 따로 들여야 한다. 라이선스부터 확인.
- 예: Galmuri11 Condensed는 한글 11,172자·가나·키릴은 있고 한자는 없다(npm galmuri 2.40.3 기준).

## 왜?
- **고정 키 vs 원문 키(gettext)**: 원문을 키로 쓰면 원문을 고칠 때 번역이 끊긴다. 고정 키 + 컴파일 검사는 "빠진 번역"을 실행 전에 없앤다. 대신 키를 짓는 수고가 든다.
- **표 vs 크레이트(fluent 등)**: 복수형·성별 굴절·런타임 파일 로드가 필요 없으면 크레이트는 의존성과 런타임 실패(키 오타)만 늘린다. 러시아어처럼 복수형이 복잡한 언어를 넣을 때 다시 본다.
- **폰트 테스트가 먼저인 이유**: 빠진 글자는 원어민이 아니면 리뷰에서 못 본다. 기계가 확실히 잡을 수 있는 건 기계에게.

## 함정
- 영어가 한국어보다 글자 수는 많고 폭은 비슷하거나 넓다. 한국어 기준으로 맞춘 고정 칸(이름 열 52px 등)이 영어에서 겹친다.
- 데이터 표에 글을 그대로 두면(예: 무브셋 이름) 두 곳에 같은 이름이 생기고 하나만 번역된다. 이름은 한 곳(장비 표 → 문자열 표)에서.
- 디버그 화면까지 번역하려 들지 않는다. 범위를 "플레이어가 보는 글"로 정한다.
- 기기 언어 감지는 "처음 한 번"이다. 설정 저장이 없으면 바꾼 언어가 다음 실행에 돌아간다.

## 관련 노트
- [WASM 빌드와 JS 번들](../reference/macroquad/wasm-build.md) — `--import-undefined`, 플러그인 버전 계약
- [그림 못 그려도 도트 게임 만들기](pixel-art-without-an-artist.md) — 한글 픽셀 폰트 서브셋
- [게임패드와 Android 입력 현황](../reference/macroquad/gamepad-and-android-input.md) — 커서 없는 메뉴 탐색
