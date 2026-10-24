---
title: macroquad WASM 빌드와 JS 번들
type: reference
tags: [macroquad, miniquad, rust, wasm, gamedev]
status: verified
created: 2026-10-24
updated: 2026-10-24
verified: |
  1차 출처로 확인: macroquad 0.4.16 README(빌드 명령, 산출물 경로, index.html 템플릿),
  js/mq_js_bundle.js 소스(프로토콜 version=2, 플러그인 버전, 버전 체크 로직),
  Cargo.toml(macroquad 0.4.16 → miniquad =0.4.11 고정), .github/workflows/rust.yml.
  직접 재현(2026-10-24, rustc 1.99.1 stable, macroquad 0.4.16 + audio feature + gamepads 0.1.7): wasm 링크가
  "undefined symbol: audio_init / getGamepads"로 실패하고, `-C link-arg=--import-undefined`로 해결됨. 번들 소스에서
  quad_net 플러그인의 strict 모드 ReferenceError, 플러그인 버전 비교가 `!=`(느슨한 비교)임을 확인. 헤드리스 Chromium(Playwright)
  콘솔로 위 두 가지와 AudioContext 자동재생 경고를 관찰.
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

### 크기 줄이기 (선택)
```toml
[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
```
더 줄이려면 binaryen의 `wasm-opt -Oz`를 한 단계 추가. 필수는 아니다.

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
- 기대하는 콘솔: `Plugin sapp_jsutils is present in JS bundle, but is not used`(정상), AudioContext 자동재생 경고(정상, 첫 클릭에 번들이 resume하며 "fix"를 찍음). `Version mismatch`·`version mismatch`·`Missed function`이 있으면 번들/플러그인/링크 문제.

## 에셋 로딩
글루의 `fs_load_file`은 페이지 기준 상대 경로로 XHR GET을 한다. 빌드 결과 디렉터리에 `assets/`를 그대로 복사하고 경로 대소문자를 맞춘다.

## 왜 async main인가 (참고)
WASM에서는 실행을 "멈추고 재개"할 수 없어 블로킹 루프를 쓸 수 없다. macroquad는 외부 런타임 없이 Rust `async/await`로 `main`의 스택을 보존해 프레임마다 재개한다. (README "Why async" 절)

## 관련 노트
- [concepts/static-wasm-hosting.md](../../concepts/static-wasm-hosting.md)
- [reference/github-actions/rust-wasm-build.md](../github-actions/rust-wasm-build.md)
