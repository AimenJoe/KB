---
title: 정적 WASM 호스팅
type: concept
tags: [wasm, hosting, rust, macroquad]
status: verified
created: 2026-10-24
updated: 2026-10-24
verified: |
  1차 출처로 확인: mq_js_bundle.js 소스(load(), fs_load_file, 버전 체크 로직), macroquad README.
  2차 출처만 있음: Netlify의 .wasm 기본 Content-Type 동작(배포 후 curl -I로 확인 권장).
sources:
  - https://github.com/not-fl3/macroquad/blob/master/js/mq_js_bundle.js
  - https://docs.rs/crate/macroquad/0.4.16/source/README.md
---

# 정적 WASM 호스팅

## 요약
번들러(wasm-bindgen, trunk 등) 없이 동작하는 WASM 앱은 호스트에 "정적 파일을 올바른 MIME 타입으로, 상대 경로 그대로 서빙하라"는 것만 요구한다. 그래서 어떤 정적 호스팅(Netlify, GitHub Pages, S3)이든 동일하게 동작하고, 빌드 위치와 호스팅 위치를 분리할 수 있다.

## 본문

### WASM 앱이 브라우저에서 뜨기까지
1. `index.html`이 JS 글루(macroquad는 `mq_js_bundle.js`)를 로드한다.
2. 글루가 `fetch("game.wasm")` → `WebAssembly.compileStreaming` → `instantiate(importObject)`. `importObject.env`에 WebGL, 입력, 파일 로딩 등 브라우저 API를 감싼 함수가 들어간다.
3. wasm의 `main()`을 호출한다. 이후 프레임마다 `requestAnimationFrame`으로 wasm 쪽 루프를 깨운다.
4. 게임이 에셋을 읽으면 글루의 `fs_load_file`이 **페이지 기준 상대 경로로 XHR GET**을 보낸다.

### 호스트가 제공해야 하는 것
- `.wasm`을 `application/wasm`으로 서빙. `compileStreaming`은 이 MIME 타입을 요구한다.
- 빌드 결과 디렉터리의 **경로 구조와 대소문자 보존**. 에셋 로딩이 상대 경로이기 때문.
- 그 외 서버 로직은 전혀 필요 없다. 리다이렉트, 함수, SSR 모두 불필요.

### 그래서 생기는 자유
- 빌드와 호스팅을 분리할 수 있다. 무거운 Rust 컴파일은 캐시가 되는 CI에서, 호스팅은 CDN에서.
- 호스트 간 이동이 쉽다. `dist/`를 어디에 올려도 같다.

## 왜?
WASM 바이너리는 자기 혼자서는 브라우저 API를 못 부른다. 반드시 JS 글루가 import를 공급해야 한다. macroquad(miniquad)는 이 글루를 **범용 번들 하나로 고정**하고, 바이너리 쪽은 `crate_version()` 같은 export로 글루에 자기 버전을 알려주는 방식을 택했다. 그래서 프로젝트별 바인딩 생성 단계(wasm-bindgen)가 없고, 빌드 산출물이 "wasm + html + 공용 js" 세 파일로 끝난다.

## 함정
- 글루와 wasm의 버전 계약이 깨지면(글루 프로토콜 버전 ≠ `crate_version()`) 로드는 되지만 콘솔에 `Version mismatch`가 찍히고 동작이 깨질 수 있다. 글루를 외부 URL에서 핫링크하면 이 계약이 남의 손에 있게 된다. → [reference/macroquad/wasm-build.md](../reference/macroquad/wasm-build.md)
- 캐시: 파일명에 해시가 없다면 `immutable` 캐시 헤더를 주면 안 된다. 배포 후에도 옛 wasm이 계속 로드된다.

## 관련 노트
- [reference/macroquad/wasm-build.md](../reference/macroquad/wasm-build.md)
- [guides/macroquad-wasm-netlify-github-actions.md](../guides/macroquad-wasm-netlify-github-actions.md)
