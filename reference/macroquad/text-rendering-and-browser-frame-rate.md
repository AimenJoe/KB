---
title: macroquad 글자 그리기 비용과 브라우저 프레임레이트 — 아틀라스 통째 올리기, 레티나, WebGL 안티에일리어싱 기본값, Safari 저전력 30fps
type: reference
tags: [macroquad, wasm, performance, safari, fonts, gamedev]
status: draft
created: 2026-10-25
updated: 2026-10-25
verified: |
  1차 출처로 확인: macroquad 0.4.16 소스 — text.rs(draw_text_ex·measure_text가 `font_size × dpi_scale`로 글자를 굽고
  처음 보는 (글자, 크기)를 cache_glyph), text/atlas.rs(cache_sprite가 dirty를 켜고, texture()가 그릴 때
  `texture_update(전체 이미지)`; 자리가 모자라면 가로세로 2배로 키우고 전부 다시 담음), miniquad 0.4.11 js/gl.js(`now()` = `Date.now()/1000`).
  직접 측정(2026-10-25, nail-under-the-roots, 헤드리스 Chromium + WebGL 후킹): 한국어 대화가 한 글자씩 찍히는 동안
  texImage2D/texSubImage2D가 새 글자마다 4MB(1024² RGBA)씩, 대화 몇 장에 40번·160MB. 언어 글자를 미리 구우니 0번.
  번들의 getContext 호출에 옵션이 없어 antialias·alpha가 켜진다(getContextAttributes로 확인), 옵션을 끼우면 꺼진다.
  원래 크기(12 물리 px)로 굽고 정수배로 키운 화면이 화면 크기로 구운 것과 픽셀 단위로 같음(dpi 1·2).
  확인 못 함: 실제 Safari에서의 프레임 시간(컨테이너에 Safari·GPU 없음. 헤드리스 Chromium은 소프트웨어 GL이라 절대 시간은 의미 없다).
  2차 출처만 있음: Safari가 저전력 모드에서 requestAnimationFrame을 30fps로 낮추고 의도된 동작이라는 것, ProMotion에서
  "Prefer Page Rendering Updates Near 60fps" 설정이 켜져 있으면 60에 묶인다는 것(WebKit Bugzilla 댓글·블로그). Safari의 WebGL
  텍스처 올리기가 Chrome보다 느린 사례(WebKit 버그 294602, 캔버스→WebGL 경로).
sources:
  - https://github.com/not-fl3/macroquad/blob/master/src/text.rs
  - https://github.com/not-fl3/macroquad/blob/master/src/text/atlas.rs
  - https://bugs.webkit.org/show_bug.cgi?id=236780
  - https://motion.dev/blog/when-browsers-throttle-requestanimationframe
  - https://bugs.webkit.org/show_bug.cgi?id=294602
---

# macroquad 글자 그리기 비용과 브라우저 프레임레이트

## 요약
macroquad는 글자를 **`font_size × dpi` 크기로 구워** 아틀라스에 넣고, 새 글자가 하나라도 들어가면 **아틀라스 텍스처 전체를 GPU에 다시 올린다**. 화면 배율이 큰 UI 글자(특히 레티나·한글·타자 효과 대화창)는 프레임마다 수 MB를 올려 버벅일 수 있다. 픽셀 폰트면 **원래 크기로 굽고 `font_scale`로 정수배**, 그리고 **그 언어 글자를 시작할 때 한 번에 굽기**로 없앤다. Safari 버벅임은 이것 말고도 **저전력 모드 30fps**일 수 있다.

## 본문
- **굽는 크기**: `draw_text_ex`·`measure_text`는 `ceil(font_size × dpi_scale)` px로 굽는다. 그리는 크기는 `구운 크기 / dpi × font_scale`. 그래서 "화면 크기로 보이게" `font_size = 12 × 배율`로 주면 레티나(dpi 2)·배율 4에서 글자 하나가 96px이다.
- **아틀라스**: 처음 1024², 새 글자 → dirty → 다음 그리기에서 `texture_update(이미지 전체)`. 모자라면 2048², 4096²으로 키우고 전부 다시 담는다(올리는 양도 4MB → 16MB → 64MB).
- **원래 크기로 굽기**(픽셀 폰트만): 구운 크기 = 12 × m 물리 px, 키우는 배 = 12 × 배율 × dpi ÷ (12 × m)가 정수인 가장 작은 m. dpi 1·2·3·1.5는 m = 1(12px 그대로)로 된다. 결과는 화면 크기로 구운 것과 같다(폰트 픽셀이 정사각형 윤곽이라).
- **미리 굽기**: 언어 표의 모든 글자를 이어 붙인 문자열을 한 번 `measure_text` → 굽기만 하고 올리기는 다음 그리기에서 한 번. 언어·배율·dpi가 바뀌면 다시. 12px 글자면 수백 자도 1024²에 넉넉하다.
- **브라우저 프레임레이트**: Safari는 저전력 모드(맥북 배터리 기본값, iPhone 저전력)에서 rAF를 30fps로 낮춘다(의도된 동작). ProMotion 120Hz도 설정에 따라 60에 묶인다. 고정 타임스텝 + 보간이면 속도는 그대로지만 눈에는 끊겨 보인다 — 게임 쪽에서 고칠 수 없으니 "전원을 꽂고 비교"가 먼저다.
- **WebGL 컨텍스트 기본값**: 번들(`mq_js_bundle.js`)은 `canvas.getContext("webgl")`/`("webgl2")`를 옵션 없이 부른다 → 브라우저 기본값 `antialias: true`, `alpha: true`. `high_dpi: true`면 아이폰(dpr 3)에서 캔버스가 2532×1170이고 매 프레임 4배 샘플을 칠하고 합친다. 도트 게임엔 쓸모가 없으니 `index.html`에서 번들보다 먼저 `HTMLCanvasElement.prototype.getContext`를 감싸 `{antialias:false, alpha:false, powerPreference:"high-performance"}`를 끼운다(번들 복사본은 그대로). 헤드리스 Chromium(같은 조건, 3초)에서 그린 프레임 62 → 144(2026-10-25, 실제 iPhone 측정은 아님).
- **시계**: miniquad 웹의 `now()`는 `Date.now()/1000`(ms 단위, 벽시계). 프레임 시간이 1ms씩 흔들리는 정도는 누적기 + 보간이 흡수한다.

## 왜?
- 텍스처 전체 올리기는 구현이 단순하지만 글자가 자주 새로 생기는 UI(타자 효과, 숫자·시간, 다국어)에서 비용이 글자 수 × 아틀라스 크기가 된다. 브라우저마다 올리기 경로의 속도가 달라(Safari가 느린 사례가 있다) 같은 코드가 한 브라우저에서만 버벅인다.
- 픽셀 폰트는 구울 해상도를 높여도 정보가 늘지 않는다. 작게 굽고 정수배로 키우면 모양은 같고 아틀라스는 작다.

## 함정
- 헤드리스 Chromium(소프트웨어 GL)의 프레임 시간은 픽셀 수에 비례해 느려질 뿐 GPU 사정을 보여 주지 않는다. **WebGL 함수를 감싸 올린 바이트를 세는 쪽**이 원인을 가르는 데 낫다.
- 벡터(매끈한) 폰트에 같은 방법을 쓰면 흐려진다. 픽셀 폰트일 때만.
- dpi가 어중간하면(1.25 등) 정수배 조합이 없을 수 있다 → 예전처럼 화면 크기로 굽는다.

## 관련 노트
- [픽셀 퍼펙트 렌더링](pixel-perfect-rendering.md)
- [WASM 빌드와 JS 번들](wasm-build.md) — 헤드리스 확인, WebGL 후킹
- [중국어·일본어 픽셀 폰트](../fonts/cjk-pixel-fonts.md)
