---
title: macroquad WASM 빌드와 JS 번들
type: reference
tags: [macroquad, miniquad, rust, wasm, gamedev]
status: verified
created: 2026-10-24
updated: 2026-11-19
verified: |
  1차(직접 실행, 2026-11-19, knellroot 0258): opt-level z → 3 — 웹 wasm 8,306,419 → 9,213,702 바이트(gzip -9 4,322,135 → 4,556,689), PC 네이티브(llvmpipe 가상 화면)에서 틱 0.60 → 0.38ms·방랑자 그리기 0.71 → 0.49ms·소품 0.42 → 0.13ms(부하 80마리 장면). 웹 브라우저·실기기에서의 비는 재지 않았다.
  1차(직접 실행, 2026-11-19, knellroot touch.js — 시간 기다림 옛 스크립트를 그대로 다시 돌려 멈춤 창이 안 열린 채 통과하는 것을 봤다, 시험 깃발을 켠 새 스크립트는 통과).
  1차(직접 실행, 2026-11-19, knellroot save.js): 장면 이름을 적는 가져오기 함수 + waitForFunction으로 바꾼 뒤, CPU 10배 느리게 한 실행에서 옛 스크립트가 숨기던 자리(새 판이 열림)를 새 스크립트가 바로 잡았고, 전제(플레이 시간이 적힌 기록)를 기다리게 고친 뒤 보통·10배 두 번 모두 통과.
  1차 출처로 확인: macroquad 0.4.16 README(빌드 명령, 산출물 경로, index.html 템플릿),
  js/mq_js_bundle.js 소스(프로토콜 version=2, 플러그인 버전, 버전 체크 로직),
  Cargo.toml(macroquad 0.4.16 → miniquad =0.4.11 고정), .github/workflows/rust.yml.
  소스 확인 + 직접 재현(2026-11-18, knellroot): macroquad 0.4.16 `src/lib.rs`의 `keys_pressed: HashSet`(key_down_event가 넣고 프레임 끝에 비움).
  CI 실패 두 번(같은 시험·같은 자리)을 CDP CPU 스로틀 5배로 로컬에서 재현(네 번에 한 번꼴), 누를 때마다 rAF 둘을 기다리게 고친 뒤 5배·8배에서 각 두 번 통과(8배에서 고치기 전 것은 첫 판에 같은 FAIL), 고친 뒤 CI 한 번 통과. 확인 못 함: CI에서 여러 번 돌려 본 결과.
  직접 재현(2026-10-24, rustc 1.99.1 stable, macroquad 0.4.16 + audio feature + gamepads 0.1.7): wasm 링크가
  "undefined symbol: audio_init / getGamepads"로 실패하고, `-C link-arg=--import-undefined`로 해결됨. 번들 소스에서
  quad_net 플러그인의 strict 모드 ReferenceError, 전역 wasm_memory로 문자열 바이트 주고받기(2026-10-25 직접 실행), 플러그인 버전 비교가 `!=`(느슨한 비교)임을 확인. 헤드리스 Chromium(Playwright)
  콘솔로 위 두 가지와 AudioContext 자동재생 경고를 관찰. 로딩 덮개의 흘려 보내는 fetch 감싸기·실패 표시(2026-11-05 knellroot, 헤드리스 직접 실행).
  2차 출처만 있음: 번들 버전 불일치로 게임이 깨진 사례(itch.io devlog), 버전 체계 변경 배경(TWiQ #2).
  Rust 블로그 2026-04-04 "Changes to WebAssembly targets and handling undefined symbols"(wasm 타깃에서 `--allow-undefined` 제거,
  rust-lang/rust#149868; 권장 해법 `#[link(wasm_import_module = "env")]`)는 **이 세션에서 원문 접속이 막혀 검색 결과 요약으로만 봤다.**
  "1.94.1은 되고 1.98은 실패"는 GitHub 이슈(dusk-network/forge#44) 한 건의 보고다.
sources:
  - https://docs.rs/crate/macroquad/0.4.16/source/README.md
  - https://blog.rust-lang.org/2026/04/04/changes-to-webassembly-targets-and-handling-undefined-symbols/
  - https://github.com/dusk-network/forge/issues/44
  - https://lld.llvm.org/WebAssembly.html
  - https://github.com/not-fl3/macroquad/blob/master/Cargo.toml
  - https://github.com/not-fl3/macroquad/blob/master/js/mq_js_bundle.js
  - https://github.com/not-fl3/macroquad/blob/master/.github/workflows/rust.yml
  - https://macroquad.rs/twiq/week2/
  - https://psteinhaus.itch.io/komisches-projekt/devlog/769436/fixed-macroquad-bundle-version
---

# macroquad WASM 빌드와 JS 번들

## 요약
macroquad는 wasm-bindgen 없이 `wasm32-unknown-unknown` 타깃으로 바로 빌드한다. 산출물은 `.wasm` 하나이고, 실행에는 `index.html`과 공용 글루 `mq_js_bundle.js`가 필요하다. 글루는 wasm과 버전 계약을 맺고 있으므로 **레포에 복사해서 함께 배포**해야 한다.

## 빌드

```sh
rustup target add wasm32-unknown-unknown
cargo build --release --target wasm32-unknown-unknown
# → target/wasm32-unknown-unknown/release/<crate>.wasm
```

- `--release`가 없으면 `debug/` 아래에 생긴다. (0.3 시절 문서는 `target/debug/wasm32-unknown-unknown/`처럼 경로가 달랐다. 버전에 맞춰 읽을 것.)
- 추가 도구 없음. trunk, wasm-pack, wasm-bindgen 모두 불필요.
- macroquad 자체 CI(`rust.yml`)도 `actions-rs/toolchain`에 `target: wasm32-unknown-unknown`을 주고 `cargo build --target=...`만 한다.

### 최신 rustc에서 링크 실패: `undefined symbol: audio_init`
2026년 stable(확인: 1.99.1)부터 wasm 타깃의 rust-lld가 미정의 심볼을 에러로 처리한다(이전에는 `--allow-undefined`가 기본이어서 JS 쪽 import로 조용히 넘어갔다).
- miniquad 자신은 `#[link(wasm_import_module = "env")] extern "C" { ... }`로 선언해 영향이 없다.
- **quad-snd(macroquad `audio` feature)와 `gamepads` 크레이트는 맨 `extern "C"`**라 `audio_init`, `audio_add_buffer`, `getGamepads` 등이 미정의 심볼로 떨어진다.
- 해결: 레포의 `.cargo/config.toml`
  ```toml
  [target.wasm32-unknown-unknown]
  rustflags = ["-C", "link-arg=--import-undefined"]
  ```
  lld의 `--import-undefined`는 미정의 심볼을 wasm import로 만든다. 상류가 `wasm_import_module`을 붙이면 플래그는 잉여가 되고 해롭지 않다.
- 부작용: 오타로 생긴 미정의 심볼도 import가 되어 런타임에 글루의 `add_missing_functions_stabs`가 "Missed function" 경고를 찍는 것으로만 드러난다. 배포 후 콘솔을 본다.

### `audio`는 기본 feature가 아니다
macroquad 0.4.16의 `[features] default = []`. 소리를 쓰려면 `macroquad = { version = "0.4.16", features = ["audio"] }`. Linux 데스크톱 링크에 `libasound2-dev`가 필요하고, 디코더는 audrey(wav/ogg, 모노·스테레오, 임의 샘플레이트 → 44.1kHz 스테레오로 리샘플). `load_sound_from_bytes()`가 있어서 **런타임에 합성한 WAV 바이트**도 로드된다(에셋 없이 임시 효과음을 만들 때 유용).

### 크기 줄이기 (선택) — 3D 게임이면 속도와 바꾸는 것이다
```toml
[profile.release]
opt-level = "z"   # 크기 우선. 계산이 많은 게임은 3을 먼저 재 본다(아래)
lto = true
codegen-units = 1
```
더 줄이려면 binaryen의 `wasm-opt -Oz`를 한 단계 추가. 필수는 아니다.
- **"z"는 계산을 느리게 한다.** CPU에서 정점 빛·자세·충돌을 셈하는 3D 게임(Knellroot)에서 `3`으로 바꾸니 같은 장면의 우리 코드 구간이
  30~60% 빨라졌고(PC 네이티브 재기), wasm은 8.31 → 9.21MB, **gzip으로는 4.32 → 4.56MB(+5%)** — 에셋을 바이너리에 넣은 게임은 코드 몫이
  작아 차이가 더 작다. 크기를 고르기 전에 gzip 크기와 프레임 시간을 같이 잰다. 같은 프로필이 Android·데스크톱에도 걸린다는 것도 잊지 말 것.

## index.html (README 템플릿 요지)

```html
<canvas id="glcanvas" tabindex='1'></canvas>
<script src="mq_js_bundle.js"></script>   <!-- 레포에 복사한 파일 -->
<script>load("mygame.wasm");</script>
```

README 원문은 `https://not-fl3.github.io/miniquad-samples/mq_js_bundle.js`를 핫링크하지만, 아래 이유로 복사본을 권장한다. `canvas` id는 글루가 `document.querySelector("#glcanvas")`로 찾으므로 바꾸면 안 된다.

## JS 번들의 버전 계약

`mq_js_bundle.js`(2026-10 기준, 약 37KB minified)는 로드 시 다음을 검사한다.

| 검사 대상 | JS 쪽 값 | wasm 쪽 export | 불일치 시 |
|---|---|---|---|
| gl.js 프로토콜 | `version = 2` | `crate_version()` | `console.error("Version mismatch: gl.js version is: …")` |
| 플러그인 `macroquad_audio` | `version: 1` | `macroquad_audio_crate_version()` | `console.error("Plugin … version mismatch")` |
| 플러그인 `sapp_jsutils` | `version: 1` | `sapp_jsutils_crate_version()` | 같음 |
| 플러그인 `quad_net` | `version: 1` | `quad_net_crate_version()` | 같음 |

- 불일치는 **에러 로그만 내고 `main()`은 호출**한다. 그래서 "뜨긴 뜨는데 이상하게 동작"하는 형태로 나타난다.
- wasm이 import하는데 글루에 없는 함수는 `add_missing_functions_stabs`가 경고용 스텁으로 채운다. 역시 조용히 깨진다.
- 플러그인 버전 비교는 `e[t].version != s`(JS 느슨한 비교)다. 크레이트가 정수를 export하는데 JS가 문자열이면(`gamepads` 0.1.7: `"0.1.7"` vs 65543) 항상 mismatch가 찍힌다. 복사본의 값을 맞춰 두면 된다.
- 번들의 `quad_net` 플러그인 코드가 strict 모드에서 선언 없는 전역(`register_plugin=function...`)을 써서 로드 시 `ReferenceError: register_plugin is not defined`가 한 번 찍힌다(2026-10 master 기준, 상류 결함). quad_net을 쓰지 않으면 무해.
- 과거(0.3 → 0.4 전환기)에는 JS 파일이 크레이트 버전과 정확히 일치해야 했고, 이후 "Rust 쪽이 필요한 JS 버전을 선언"하는 방식으로 바뀌었다(TWiQ #2). 그래도 핫링크된 번들이 상류에서 바뀌면 깨질 수 있어 실제 사고 사례가 있다.

### 따라서
1. `Cargo.lock`의 macroquad 버전과 같은 git 태그에서 `js/mq_js_bundle.js`를 받아 `web/mq_js_bundle.js`로 커밋한다.
2. macroquad를 올릴 때 번들도 같이 갱신한다. (체크리스트에 넣을 것)
3. 배포 후 브라우저 콘솔에서 `Version mismatch`가 없는지 확인한다.

## 내 JS 플러그인: 정수로만 주고받기 (언어 읽기·설정 저장)

wasm-bindgen 없이 브라우저 기능(선호 언어, localStorage)을 쓰려면 `index.html`에서 번들 다음에 플러그인을 하나 등록한다.

```js
miniquad_add_plugin({
  name: "nail_prefs", version: 1,
  register_plugin: function (importObject) {
    importObject.env.nail_pref_get = function (i) { try { var v = parseInt(localStorage.getItem("nail.pref." + i), 10); return isNaN(v) ? 0 : (v >>> 0); } catch (e) { return 0; } };
    importObject.env.nail_pref_set = function (i, v) { try { localStorage.setItem("nail.pref." + i, String(v >>> 0)); } catch (e) {} };
  }
});
load("nail.wasm");
```

Rust 쪽은 `extern "C" { fn nail_pref_get(i: u32) -> u32; fn nail_pref_set(i: u32, v: u32); }`(wasm32에서만)와 버전 함수 `#[no_mangle] pub extern "C" fn nail_prefs_crate_version() -> u32 { 1 }`.

- **문자열 대신 정수 칸**: 문자열은 wasm 메모리 포인터·길이를 다뤄야 한다. 설정(소리·언어·키 번호)은 정수 칸 십여 개면 충분하고, 언어 태그는 "칸 i의 k번째 네 글자를 u32 하나로"(빅엔디언 ASCII) 접어 넘긴다.
- **0 = 없음**으로 정하고 값은 +1 해서 저장한다. 플러그인이 없을 때 번들이 끼워 넣는 스텁은 `undefined`를 돌려주는데, JS → wasm i32 변환(ToInt32)에서 0이 된다 → "저장 없음"과 같아진다.
- 첫 칸에 **형식 표식**(예: `0x4E410001`)을 두고 다르면 통째로 무시한다(형식을 바꿀 때 올린다).
- `localStorage`는 사생활 보호 모드·차단 정책에서 예외를 던질 수 있어 try/catch로 감싼다.
- 확인(2026-10-25, nail-under-the-roots): 헤드리스 Chromium에서 키를 다시 붙이고 새로고침 → 그대로 복원, `localStorage`에 `nail.pref.0..17`(그 뒤 0081에서 음악 칸이 붙어 0..18).

## 문자열 주고받기: wasm 메모리를 직접 (기록 저장)
정수 칸으로 모자라는 것(런을 넘는 기록처럼 키가 늘어나는 것)은 글 한 칸으로 저장한다. 번들의 전역 `wasm_memory`(`var`로 선언돼 다른 `<script>`에서 보인다)로 Rust가 잡은 버퍼를 JS가 직접 읽고 쓴다.

```js
importObject.env.nail_save_len  = function ()         { return new TextEncoder().encode(get()).length; };
importObject.env.nail_save_read = function (ptr, len) { new Uint8Array(wasm_memory.buffer, ptr, len).set(new TextEncoder().encode(get()).subarray(0, len)); };
importObject.env.nail_save_write= function (ptr, len) { set(new TextDecoder().decode(new Uint8Array(wasm_memory.buffer, ptr, len))); };
```
```rust
let n = unsafe { nail_save_len() } as usize;          // 0이면 저장 없음(플러그인이 없어도 0)
let mut buf = vec![0u8; n];
unsafe { nail_save_read(buf.as_mut_ptr(), n as u32) };  // JS가 이 버퍼에 쓴다
unsafe { nail_save_write(s.as_ptr(), s.len() as u32) }; // JS가 이 범위를 읽는다
```
- 길이는 **UTF-8 바이트 수**로 센다. JS 문자열 `.length`는 UTF-16 단위라 한글이 섞이면 어긋난다.
- `wasm_memory.buffer`는 메모리가 자라면 새 객체가 된다. 뷰(`Uint8Array`)는 **부를 때마다 새로** 만든다(전역에 잡아 두지 않는다).
- 확인(2026-10-25, nail-under-the-roots): 헤드리스 Chromium에서 `addInitScript`로 localStorage에 기록을 넣고 시작 → 읽힘. 게임이 쓴 기록이 `localStorage.getItem`에 그대로 나옴.
- 저장 칸이 여럿이면(저장 슬롯) 함수마다 첫 인자로 **칸 번호**를 받는다: `nail_save_len(cell)`, `nail_save_read(cell, ptr, len)`, `nail_save_write(cell, ptr, len)`. JS가 번호를 열쇠 이름으로 바꾼다. 예전 한 칸 저장의 열쇠를 슬롯 1에 그대로 쓰면 업데이트해도 기록이 남는다. 함수 모양을 바꾸면 플러그인 `version`과 Rust의 `<이름>_crate_version()`을 함께 올린다(다르면 번들이 콘솔에 "version mismatch"를 찍는다). 확인(2026-10-26, nail-under-the-roots 0078): 헤드리스 Chromium에서 슬롯 1(옛 열쇠)·3에 기록을 넣고 슬롯 창 → 요약 표시, 슬롯 3 지우기·슬롯 2 새로 시작 → `nail.slot`=2, 슬롯 2·3 열쇠가 바뀐 것을 `localStorage`로 확인.

## 로딩 화면 (번들을 고치지 않고)

첫 프레임 전까지 macroquad는 아무것도 그리지 않는다(wasm 받기·컴파일 + main의 `load_*().await` 동안 검은 화면).
- **HTML 덮개**: 캔버스 위 `div`(z-index), 게임 배경색, 스프라이트 시트 한 줄을 CSS `steps()` 애니메이션 + `image-rendering: pixelated`로. 이 시점엔 게임의 언어·폰트가 없으니 **글 없이** 그림과 막대만.
- **wasm 진행**: 번들 `load()`는 `fetch(path)` → `compileStreaming`. 번들보다 먼저 `window.fetch`를 감싸 `*.wasm`이면 `body.getReader()`로 바이트를 세고, 모은 조각으로 `new Response(new Blob(chunks, {type:"application/wasm"}), {headers:{"Content-Type":"application/wasm"}})`를 돌려준다(compileStreaming은 MIME을 본다).
  - 흘려 보내는 꼴도 된다(2026-11-05, knellroot 0062, 직접 실행): 조각을 모으지 않고 `new ReadableStream({pull})`이 읽은 조각을 그대로 `enqueue`하며 세고, 원래 헤더를 복사해 `Content-Length`만 지운 `new Response(stream, {status, headers})`를 돌려주면 `compileStreaming`이 받는 동안 컴파일을 그대로 한다(Content-Type이 원래 `application/wasm`이어야 한다). 헤드리스 Chromium에서 64 KB씩 15 ms 간격으로 흘린 2.6 MB에 막대 값 24개가 중간을 지나고 거꾸로 가지 않음.
- **압축 전송 주의**: gzip/br이면 `Content-Length`(압축 크기)가 읽은 바이트(푼 크기)보다 작다 → `max(Content-Length, 받은 양 × 1.05)`로 나누고 95%에서 멈춘다.
- **게임 안 준비**: 정수 플러그인(`nail_load_step(done, total)`, `nail_load_ready()`)으로 main이 폰트·그림·소리마다 알린다. `ready`는 **첫 `next_frame().await` 뒤**에 — 그 전에 덮개를 걷으면 검은 화면이 한 번 보인다.
- 확인(2026-10-25, nail-under-the-roots): Playwright `page.route`로 응답마다 지연을 넣어 느린 회선을 흉내, 막대가 0 → 60 → 68 … 100%로 차고 덮개가 걷힘.
- **시작 파일은 한꺼번에 받는다**(2026-10-26, nail 0092, 직접 측정): `load_texture(..).await`를 파일마다 차례로 하면 웹에서 파일 수 × 왕복 지연이 쌓인다(44개, 지연 70ms·9Mbps 흉내에서 wasm 뒤 6.1초). 각 `macroquad::file::load_file` 퓨처를 `Box::pin`해 한 `std::future::poll_fn`에서 같이 돌리면(macroquad 실행기는 프레임마다 메인 퓨처를 폴링하므로 깨우개 없이도 돈다) 동시에 요청되어 2.7초. 받은 바이트는 `Texture2D::from_file_with_format`·`Image::from_file_with_format`·`load_ttf_font_from_bytes`·`load_sound_from_bytes`로 만든다. 막대는 받은 파일마다 한 칸(단계 수를 상수로 박으면 한 단계에서 몇 초씩 멈춘다).
- **실패를 보이게**(2026-11-05, knellroot 0062, 번들 소스 확인 + 직접 실행): 번들 `load()`는 컴파일·`main()` 실패를 `.catch(e => console.error(e))`로만 삼킨다 — 덮개가 90%에서 영원히 멈춘 것처럼 보인다. `console.error`를 감싸 `Error` 인스턴스가 오면 막대를 붉게, 첫 프레임 전 패닉(requestAnimationFrame 안)은 `window` `error` 이벤트로 잡는다. **함정: `error` 듣기를 번들 `<script>`보다 먼저 걸면** 번들이 읽힐 때 나는 quad_net의 strict 모드 `ReferenceError: register_plugin`(무해한 잡음)에 걸려 늘 실패로 보인다 → 번들을 읽은 뒤(`load()` 바로 앞)에 건다.
- **함정 — 시트 크기를 CSS에 박지 말 것**: `background-size: 384px 384px`처럼 시트 전체 크기를 숫자로 적으면, 게임 쪽에서 시트에 칸을 더할 때(nail: 6칸 → 9칸) 로딩 그림만 가로로 찌그러지고 칸이 어긋난다. 게임 화면은 멀쩡해서 늦게 알아챈다. `background-size: auto <줄 수 × 칸 × 배율>px`처럼 **높이만 정하고 폭은 auto**로 두면 비율이 지켜진다(2026-10-26, 헤드리스로 고치기 전·후 프레임을 찍어 확인).

## 헤드리스로 웹 빌드 확인 (Playwright)
배포 전에 콘솔 에러·입력·렌더를 자동으로 본다. `python3 -m http.server --directory dist`로 띄우고:
```js
const { chromium } = require('playwright');
const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
page.on('console', m => console.log(m.type(), m.text()));
page.on('pageerror', e => console.log('pageerror', e.message));
await page.goto('http://127.0.0.1:8000/'); await page.waitForTimeout(2000);
await page.focus('#glcanvas'); await page.keyboard.press('j');   // 입력도 들어간다
await page.screenshot({ path: 'web.png' });
```
- CI에서 돌릴 때 설치가 느리면(`--with-deps`가 받는 apt 글꼴, 같은 커밋 두 번 시험): [연기 시험이 느려질 때](../github-actions/playwright-smoke-test-ci-time.md).
- **키를 누른 뒤에는 시간이 아니라 프레임을 기다린다**(2026-11-18, knellroot 0233 뒤 CI): macroquad의 "이번 프레임에 눌림"은 `HashSet`이고
  프레임 끝에 비운다(0.4.16 `src/lib.rs` `keys_pressed` — `key_down_event`가 넣고 `end_frame`이 비운다) → **한 프레임에 같은 키가 두 번 오면
  한 번**, 서로 다른 키의 순서도 남지 않는다. `keyboard.press(k)` + `waitForTimeout(80)`은 로컬에서는 늘 통과하지만 느린 CI 러너에서는
  가끔 두 누름이 한 프레임에 들어간다 — 메뉴에서 ↑ 두 번이 한 번이 되어 다른 칸을 고르고, 시험이 엉뚱한 곳에서 실패한다(같은 자리에서
  두 번, 하루 걸러). CDP `Emulation.setCPUThrottlingRate` 5~8배로 로컬에서 재현된다. 누를 때마다
  `await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))))`로 게임 루프(rAF)가 두 번 돌기를 기다린다.
- **장면이 바뀌는 누름 뒤에는 시간이 아니라 상태를 기다린다**(2026-11-19, knellroot `save.js` — 같은 자리 네 번째 실패 뒤): CI 소프트웨어 GL은
  10 fps 안팎이라 `waitForTimeout(300)`이 몇 프레임인지 정해지지 않는다. 게임이 맨 위 장면이 바뀐 프레임에 JS 가져오기 함수 하나로
  `window.knellScene = "<Scene의 Debug>"`를 적게 하고(`importObject.env`에 함수를 더하면 wasm이 부를 수 있다 — 글은 `wasm_memory`에서 읽는다),
  시험은 `page.waitForFunction(w => window.knellScene.startsWith(w))`로 기다린다. 못 오면 **지금 장면을 말하며** 멈추게 하면 실패가 진단이 된다:
  느린 CPU(`setCPUThrottlingRate` 10배)에서 "덮어쓰기 묻는 창 대신 새 판"으로 바로 잡혔고, 원인은 키 처리가 아니라 **시험의 전제**였다 —
  슬롯 창은 플레이 시간 1초 이상인 슬롯만 기록으로 보는데, 벽시계 2~3초로는 느린 러너에서 게임 시간이 1초를 못 채워 그 슬롯이 빈 슬롯이 되고
  커서 셈(↑↑)이 엉뚱한 칸에 닿았다. 게임 시간에 기대는 전제(쌓인 시간·저장된 기록)는 저장소를 폴링해 확인한 뒤 다음 걸음으로.
- **시간으로 기다리는 헤드리스 시험은 틀린 화면을 찍고도 통과한다**(2026-11-19, knellroot 스크립트 열 개를 장면 기다림으로 옮기며): 스크린숏만 남기는
  스크립트는 기대한 화면이 아니어도 실패하지 않는다. 옮기자마자 둘이 드러났다 — (1) 긴 터치 시험 도중 주인공이 곁의 적에게 쓰러져, 멈춤·장비
  창 대신 결과 화면을 찍고 있었다(옛 스크립트로 다시 돌려도 같은 자리에서 창이 안 열렸다), (2) UI가 바뀌어(새 판에는 바꿀 장비가 없음) 기대한
  목록이 더는 뜨지 않았다. 고친 길: 개발 빌드에만 있는 시험 깃발(페이지 `window.<게임>TestFlags` → 가져오기 함수 → 월드의 "맞지 않음")을
  `addInitScript`로 켜고, 기대 자체를 지금 규칙에 맞게 고쳤다. 장면 이름을 기다리는 길은 이런 조용한 틀림을 바로 실패로 바꾼다. 화면 안 탭
  넘기기처럼 이름 대신 "바뀌었다"만 알면 될 때는 누르기 전 이름을 적어 두고 다른 이름이 올 때까지 기다린다.
- 기대하는 콘솔: `Plugin sapp_jsutils is present in JS bundle, but is not used`(정상), AudioContext 자동재생 경고(정상, 첫 클릭에 번들이 resume하며 "fix"를 찍음). `ReferenceError: register_plugin is not defined`(mq_js_bundle.js 안, 2026-10-26 확인)도 원래 난다: 번들에 든 quad-net 웹소켓 플러그인이 엄격 모드에서 선언 없이 전역 `register_plugin`에 대입한다. 그 플러그인을 안 쓰면 무해하다. `Version mismatch`·`version mismatch`·`Missed function`이 있으면 번들/플러그인/링크 문제.

## 에셋 로딩
글루의 `fs_load_file`은 페이지 기준 상대 경로로 XHR GET을 한다. 빌드 결과 디렉터리에 `assets/`를 그대로 복사하고 경로 대소문자를 맞춘다.

## 왜 async main인가 (참고)
WASM에서는 실행을 "멈추고 재개"할 수 없어 블로킹 루프를 쓸 수 없다. macroquad는 외부 런타임 없이 Rust `async/await`로 `main`의 스택을 보존해 프레임마다 재개한다. (README "Why async" 절)

## 관련 노트
- [concepts/static-wasm-hosting.md](../../concepts/static-wasm-hosting.md)
- [reference/github-actions/rust-wasm-build.md](../github-actions/rust-wasm-build.md)
