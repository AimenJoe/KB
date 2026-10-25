---
title: 작은 게임 다국어(현지화) 구조 — 고정 키 표, 자리표시자, 폰트 커버리지 테스트
type: guide
tags: [gamedev, i18n, localization, fonts, rust, testing]
status: draft
created: 2026-10-25
updated: 2026-10-25
verified: |
  직접 실행(2026-10-25, 같은 프로젝트, 다섯 번째 언어 브라질 포르투갈어): DeepL 무료 초안 260줄을 검토하며 틀린 예를 기록, Galmuri cmap에 악센트 확인(fontTools),
  로캘 pt-BR 헤드리스 스크린숏으로 넘침 3곳 수정. 번역 품질은 원어민 검수 전.
  1차 출처로 확인: 직접 실행(2026-10-25, nail-under-the-roots, Rust + macroquad 0.4.16): 언어별 `static Strings` 구조체(키 누락 = 컴파일 에러),
  `{0}` 자리표시자 + 언어 간 일치 테스트, 선호 목록 고르기(navigator.languages를 ['ja-JP','ko-KR'] / ['fr-FR','de'] / ['ko-KR']로 바꿔
  각각 한국어·영어·한국어로 시작함을 헤드리스 Chromium에서 확인), TTF cmap(형식 4·12)을 직접 읽는 폰트 커버리지 테스트(fontTools 결과와 교차 확인 — 285자 모두 있음,
  가나 'あ'는 없음), 헤드리스 Chromium `locale` 옵션으로 ko-KR/en-US 화면 스크린숏을 찍어 영어에서 넘치는 곳 3군데를 찾아 고침.
  sys-locale 0.3.2 소스(src/android.rs가 `__system_property_get("persist.sys.locale")`, wasm은 wasm-bindgen 선택 기능)를 읽음.
  Galmuri11 Condensed(npm galmuri 2.40.3)의 cmap: 가나 있음(히라가나 82·가타카나 84), 한자(U+4E00–9FFF) 0, 키릴 140.
  직접 실행(2026-10-25, 같은 프로젝트, 4개 언어로 늘리며): 가짜 언어(영어 → 악센트 + 40% 늘림)로 화면을 찍어 넘침 5곳(탭 줄, 상태 값,
  저널 목록, 지도 제목, 설정 안내)을 찾고 고침. 일본어·간체(12px 한자 = 한글 8px의 1.5배 폭)에서 띄어쓰기 기준 줄바꿈이 안 되는 것을 확인하고
  글자 단위 + 금칙 줄바꿈으로 고침(단위 테스트). 브라우저 zh-TW → 번체가 없으면 영어로 넘어가는 것 확인.
  2차 출처만 있음: Steam 언어 우선순위 권고(Steam Page Analyzer 2026, GameDiscoverCo, Nimdzi 2019~20 데이터), 번역 비용 추정치.
  2차 출처만 있음: 현지화 일반 원칙(고정 ID, 텍스트 팽창 30~50%, 의사 현지화, 문장 조각 잇기 금지, 폰트 폴백) — 업체·블로그 글.
  Steam 언어 비율(영어·중국어 간체가 1·2위를 오감, 러시아어 3위)은 월별 보도이며 Valve 보정 논란이 있다.
sources:
  - https://translated.com/resources/game-localization-developer-guide
  - https://alconost.com/en/blog/game-localization-rework
  - https://bugnet.io/blog/game-localization-testing-common-bugs
  - https://www.gamingonlinux.com/2026/10/steam-survey-for-september-2026-shows-a-drop-in-linux-with-simplified-chinese-rising/
  - https://github.com/1Password/sys-locale
  - https://github.com/quiple/galmuri
  - https://www.steampageanalyzer.com/blog/steam-localization-languages
  - https://newsletter.gamediscover.co/p/how-localization-affects-game-discovery
  - https://www.nimdzi.com/steam-the-dynamic-of-games-languages/
  - https://partner.steamgames.com/doc/store/localization/languages
  - https://docs.godotengine.org/en/latest/tutorials/i18n/pseudolocalization.html
---

# 작은 게임 다국어 구조

## 요약
글 100~수백 개, 언어 2~3개인 1인 게임이면 **언어별 문자열 표 하나 + 고정 키 + 테스트 세 개**(폰트 커버리지, 자리표시자 일치, 빈 글)가 가장 싸다. 번역 크레이트·외부 파일은 언어가 늘거나 번역가가 코드 밖에서 일할 때 도입한다. 가장 흔한 사고는 "번역은 있는데 서브셋 폰트에 글자가 없음"과 "영어가 길어서 넘침"이다.

## 절차
1. **글을 코드에서 빼서 표로**: 키 = 의미 있는 고정 이름(`gift_title`), 값 = 언어별 글. Rust라면 `struct Strings { gift_title: &'static str, … }`와 언어마다 `static KO/EN: Strings` — 한 언어라도 필드가 빠지면 컴파일이 안 된다. 키 목록은 매크로 한 번으로 구조체와 `all()`(테스트용 열거)을 같이 만든다.
2. **데이터 표는 글 대신 "글을 고르는 함수"를 든다**: `type Tr = fn(&Strings) -> &'static str;` 무기·퀘스트·대사 표에 `name: |s| s.w_mole`. 게임 로직은 언어를 모르고, 그릴 때만 지금 언어로 꺼낸다.
3. **숫자는 자리표시자**: `"{0}연타 · 마지막 타 피해 {1}"` / `"{0}-hit combo · finisher damage {1}"`. 위치 번호라 어순이 달라도 된다. 문장을 조각으로 이어 붙이지 않는다.
4. **시작 언어 = 기기 언어, 설정에서 바꿈**: 번체 지역(zh-TW·HK·MO, zh-Hant)을 간체로 바꾸지 않는다 — 번체가 없으면 다음 선호 언어로 넘긴다. 첫 선호 언어만 보지 말고 **선호 목록을 앞에서부터 보고 가진 첫 언어**, 하나도 없으면 영어. 일본어·한국어 순으로 둔 사람은 한국어를, 프랑스어·독일어만 둔 사람은 영어를 받는다. 웹은 `navigator.languages`, 네이티브는 OS 선호 목록(`sys_locale::get_locales()`). 언어 이름은 그 언어로 쓴다("한국어", "English").
5. **테스트 세 개**(CI): (a) 모든 언어의 모든 글자가 쓰는 폰트의 cmap에 있는가 (b) 같은 키의 자리표시자 집합이 언어끼리 같은가 (c) 빈 글이 없는가.
6. **두 언어로 화면을 찍어 본다**: 헤드리스 브라우저의 로캘 옵션(Playwright `newContext({ locale })`)으로 언어별 스크린숏. 고정 폭 칸·한 줄 안내가 넘친다. 칸 폭은 가장 긴 글에 맞추고 긴 안내는 줄바꿈한다.

## 어떤 언어를, 언제 (PC/Steam 인디, 2026 기준 — 2차 출처)
- 흔한 권고 순서: 영어 → **중국어 간체·일본어·한국어** → **러시아어·브라질 포르투갈어·스페인어**(·터키어) → 독일어·프랑스어·번체·폴란드어. 예전 표준 EFIGS(영·프·이·독·스) 우선은 PC에선 낡았다는 평이 많고, 이탈리아어가 가장 자주 빠진다.
- 비용 감: 상점 페이지만 번역은 언어당 수백 달러, 게임 전체는 중간 규모 인디 기준 수천 달러(한 블로그 추정). 상점 페이지 먼저가 싸다.
- Steam 정식 지원 언어는 29~30개(문서와 제3자 표가 다름). API 코드는 Web API(zh-CN)와 Steamworks API(schinese)가 다르다.
- **구조(국제화)는 처음부터, 번역(현지화)은 글이 굳은 뒤.** 글이 매주 바뀌는 시기에 10개 언어를 번역하면 바뀔 때마다 10배로 고친다. 대신 구조가 언어를 견디는지는 매번 확인한다(아래 "처음부터 넣어 둘 것").
- 지금 구조로 안 되는 언어를 미리 적어 둔다: 오른쪽→왼쪽(아랍어·히브리어), 글자 조합 셰이핑(태국어·힌디어). 간단한 엔진의 글자 그리기는 셰이핑을 안 한다.

## 처음부터 넣어 둘 것 (체크리스트)
1. 문자열 표(위 절차) + 폰트 커버리지·자리표시자 테스트.
2. **가짜 언어**(개발 빌드에서만 고를 수 있게): 영어를 악센트 글자로 바꾸고 30~50% 늘린다. 자리표시자 `{0}`은 그대로. 넘치는 칸과, 악센트가 없는 글(표를 거치지 않은 글)이 바로 보인다. 엔진 기능으로도 있다(Godot pseudolocalization).
3. **폭이 다른 문자 하나**(일본어나 중국어)를 일찍 넣는다. 한자·가나는 정사각 칸이라 같은 px 폰트의 한글·라틴보다 넓다(12px 한자 = 한글 Condensed 8px의 1.5배).
4. **줄바꿈 두 가지**: 띄어쓰기 단위(한국어·영어) + 글자 단위(일본어·중국어). 글자 단위엔 금칙 — 。、！？）」·작은 가나·ー는 줄 맨 앞에 오지 않게 앞 줄에 붙이고, （「는 줄 끝에 남기지 않는다. 한 단어가 줄보다 길면(독일어 합성어) 쪼갠다. 측정 함수를 받는 순수 함수로 만들면 단위 테스트가 쉽다.
5. **고정 칸의 마지막 안전장치**: 넘치면 뒤를 잘라 "…"(`fit`). 탭 줄은 전체 폭 안에서 여백을 줄이고, 그래도 넘치면 같은 몫으로 자른다. 이름·값 표는 이름 칸을 가장 긴 이름에 맞추되 상한을 둔다.
6. 한 줄 안내는 두 줄로 자랄 자리를 둔다. 같은 줄에 두 요소(탭 + 안내 문구)를 놓지 않는다.
7. 번역하지 않는 개발 화면은 언어와 상관없이 기본 폰트로 찍는다(다른 언어 폰트엔 그 글자가 없다).
8. 복수형이 필요한 문장은 피해서 쓴다("1 / 15 칸"). 러시아어·폴란드어를 넣을 때 다시 본다.

## macroquad(wasm-bindgen 없음)에서 브라우저 언어 읽기
- `sys-locale`은 웹에서 wasm-bindgen 선택 기능을 쓴다. macroquad는 wasm-bindgen을 쓰지 않으므로 **wasm에서는 빼고** 작은 miniquad 플러그인으로 읽는다: `index.html`에서 `miniquad_add_plugin({ name, version, register_plugin(io) { io.env.nail_locale = () => … } })`, Rust는 `extern "C" { fn nail_locale(i: u32, k: u32) -> u32; }` — i번째 선호 언어 태그의 k번째 네 글자를 빅엔디언 u32로 받고 0이면 끝(태그 전체가 필요하다: zh-CN과 zh-TW를 갈라야 하므로 주 언어 두 글자로는 모자란다). 문자열을 넘기지 않고, 지원 언어 목록은 Rust 쪽(`Lang::from_tag`) 한 곳에만 둔다. 링크는 `--import-undefined`(wasm-build 노트).
- 플러그인에 `name`·`version`을 주면 번들이 `<name>_crate_version` 내보내기를 찾는다. 없으면 콘솔 로그만 남지만, 같은 값을 돌려주는 `#[no_mangle] extern "C" fn` 하나를 두면 깔끔하다.
- 옛 `index.html`(플러그인 없음)에서는 번들이 빈 함수를 끼워 넣어 `undefined` → 0이 된다. 0을 "모름"으로 두면 안전하다.
- 데스크톱·Android는 `sys-locale`(Android는 시스템 속성 `persist.sys.locale`).

## 폰트
- 중국어·일본어는 폰트가 따로다(한자 통합·일본식 약자). 후보와 범위: [중국어·일본어 픽셀 폰트](../reference/fonts/cjk-pixel-fonts.md).
- 서브셋 폰트는 언어를 늘릴 때마다 다시 만든다. 일본어는 가나만으로도 쓸 수 있지만(어린이용 게임의 히라가나 모드처럼) 한자가 필요하면 한자 있는 픽셀 폰트를 따로 들여야 한다. 라이선스부터 확인.
- 예: Galmuri11 Condensed는 한글 11,172자·가나·키릴은 있고 한자는 없다(npm galmuri 2.40.3 기준).

## 기계 번역 초안 + 사람 검토 (브라질 포르투갈어 사례, 2026-10-25)
- 순서: 기존 표에서 용어(장소·기술·이름)를 먼저 찾는다 → 직접 번역 → 한 줄씩 원문(한국어·영어)과 대조 → 자리표시자 일치 테스트 → 로캘로 화면 찍기.
- 기계 번역(DeepL) 초안은 이 프로젝트에서 쓰지 않기로 했다(2026-10-25, 사장 결정). 게임 용어 오독이 줄마다 나와 고치는 품이 직접 쓰는 것보다 컸다.
  - 오독 예: 굴 → oyster·牡蠣, 보리(이름) → barley, 털빛 → feather color·羽色, 굴파기 → "Oyster Harvesting", 끼기 → stuck·挟む, 실 → path.
  - 무료 요금제는 문맥·사용자 지침을 무시한다. 짧은 UI 글일수록 문맥이 없어 더 틀린다.
- **짧은 UI 조각일수록 틀린다.** 문맥이 없어서다: Resume → "Currículo"(이력서), On → "Em"(~에), Spring(샘) → "Primavera"(봄), Back closes → "Fechamento das vendas"(판매 마감), 게임 용어(Burrow)를 영어 그대로 둠. 긴 대사는 대체로 쓸 만했다.
- **성별 굴절 언어**(포르투갈어·스페인어·프랑스어…)는 플레이어 성별을 정하지 않으려면 형용사를 피한다: "Bem-vindo"(남성) → "Boas-vindas", "você está machucado" → "você se machucou". 이름 모르는 인물은 문법 성이 고정된 일반 명사로("aquela criaturinha").
- 길이: 포르투갈어는 영어보다 길다. 고정 칸(메뉴·능력치 이름)은 짧은 동의어로("Configurações" → "Opções", "Velocidade de ataque" → "Vel. ataque").
- 라틴 악센트(ã õ ç …)는 한국어 픽셀 폰트(Galmuri)에도 다 있었다 — 폰트 cmap을 먼저 확인하면 서브셋을 새로 만들 필요가 없다.
- 지역 변이: pt-PT를 pt-BR로 보내는 건 괜찮다(같은 글자, 낱말 차이). 번체 → 간체는 안 된다(글자 체계가 다름).

## 왜?
- **고정 키 vs 원문 키(gettext)**: 원문을 키로 쓰면 원문을 고칠 때 번역이 끊긴다. 고정 키 + 컴파일 검사는 "빠진 번역"을 실행 전에 없앤다. 대신 키를 짓는 수고가 든다.
- **표 vs 크레이트(fluent 등)**: 복수형·성별 굴절·런타임 파일 로드가 필요 없으면 크레이트는 의존성과 런타임 실패(키 오타)만 늘린다. 러시아어처럼 복수형이 복잡한 언어를 넣을 때 다시 본다.
- **폰트 테스트가 먼저인 이유**: 빠진 글자는 원어민이 아니면 리뷰에서 못 본다. 기계가 확실히 잡을 수 있는 건 기계에게.

## 함정
- **가는 픽셀 폰트 + 바쁜 배경**: 1px 획 폰트(예: Galmuri Condensed)는 뒤로 지나가는 선과 겹치면 획이 끊긴 것처럼 읽혀 "글자가 깨졌다"는 말을 듣는다. 획이 빽빽한 폰트(Ark Pixel 한자·가나)는 덜 드러나서 "일본어·중국어만 멀쩡하다"로 보인다. 그리기 순서 문제와 구별하려면 배경 선을 원색(초록)으로 바꿔 찍어 글자 위에 그 색이 있는지 본다. 고침: 1게임 px 어두운 테두리(상하좌우 4번 먼저 찍기)나 글 뒤 어두운 띠.
- 영어가 한국어보다 글자 수는 많고 폭은 비슷하거나 넓다. 한국어 기준으로 맞춘 고정 칸(이름 열 52px 등)이 영어에서 겹친다.
- 데이터 표에 글을 그대로 두면(예: 무브셋 이름) 두 곳에 같은 이름이 생기고 하나만 번역된다. 이름은 한 곳(장비 표 → 문자열 표)에서.
- 디버그 화면까지 번역하려 들지 않는다. 범위를 "플레이어가 보는 글"로 정한다.
- 기기 언어 감지는 "처음 한 번"이다. 설정 저장이 없으면 바꾼 언어가 다음 실행에 돌아간다.

## 관련 노트
- [중국어·일본어 픽셀 폰트](../reference/fonts/cjk-pixel-fonts.md) — 한자 통합, 12px 후보, PNG 원본에서 언어별 서브셋
- [WASM 빌드와 JS 번들](../reference/macroquad/wasm-build.md) — `--import-undefined`, 플러그인 버전 계약
- [그림 못 그려도 도트 게임 만들기](pixel-art-without-an-artist.md) — 한글 픽셀 폰트 서브셋
- [게임패드와 Android 입력 현황](../reference/macroquad/gamepad-and-android-input.md) — 커서 없는 메뉴 탐색
