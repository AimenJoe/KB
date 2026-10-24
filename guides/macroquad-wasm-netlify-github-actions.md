---
title: macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포
type: guide
tags: [macroquad, rust, wasm, netlify, github-actions, gamedev, ci]
status: verified
created: 2026-10-24
updated: 2026-10-24
verified: |
  각 단계의 근거는 링크된 reference 노트의 verified 항목을 따른다.
  이 가이드의 워크플로 YAML 자체는 실제 레포에서 아직 실행 검증하지 않았다(초안). 첫 실행 후 updated/status 갱신할 것.
sources:
  - reference/macroquad/wasm-build.md
  - reference/netlify/deploy-from-ci.md
  - reference/github-actions/rust-wasm-build.md
---

# macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포

## 요약
GitHub Actions에서 `wasm32-unknown-unknown`으로 빌드 → `dist/` 조립 → 공식 `netlify-cli`로 업로드. Netlify 사이트에는 Git 연동을 걸지 않는다. 결정 배경은 [decisions/0001](../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md).

## 사전 준비 (1회)

1. **Netlify 사이트 생성 — Git 연동 없이.**
   `netlify init --manual` 또는 UI에서 "Deploy manually". 레포를 연결하면 CLI 배포가 다음 push에 덮어써진다. ([왜](../reference/netlify/deploy-from-ci.md#둘을-섞으면-안-되는-이유))
2. **GitHub Secrets 두 개.**
   - `NETLIFY_AUTH_TOKEN`: Netlify → User settings → Applications → Personal access token
   - `NETLIFY_SITE_ID`: Site configuration → General → Site ID
3. **JS 번들을 레포에 복사.**
   `Cargo.lock`의 macroquad 버전과 같은 태그에서 `js/mq_js_bundle.js`를 받아 `web/mq_js_bundle.js`로 커밋. 핫링크 금지. ([왜](../reference/macroquad/wasm-build.md#js-번들의-버전-계약))
4. **`web/index.html`** — README 템플릿에서 스크립트 src만 로컬 파일로 바꾼 것.
   ```html
   <!doctype html>
   <html lang="ko">
   <head>
     <meta charset="utf-8">
     <title>mygame</title>
     <style>html,body,canvas{margin:0;padding:0;width:100%;height:100%;overflow:hidden;position:absolute;background:black;z-index:0}</style>
   </head>
   <body>
     <canvas id="glcanvas" tabindex="1"></canvas>
     <script src="mq_js_bundle.js"></script>
     <script>load("mygame.wasm");</script>
   </body>
   </html>
   ```
5. **`.gitignore`에 `.netlify/`, `dist/` 추가.**
6. (선택) `Cargo.toml` release 프로파일로 wasm 크기 축소.
   ```toml
   [profile.release]
   opt-level = "z"
   lto = true
   codegen-units = 1
   ```

## 워크플로

`.github/workflows/deploy-web.yml`

```yaml
name: deploy-web
on:
  push:
    branches: [main]
  pull_request:

concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: dtolnay/rust-toolchain@stable
        with:
          targets: wasm32-unknown-unknown
      - uses: Swatinem/rust-cache@v2

      - run: cargo build --release --target wasm32-unknown-unknown

      - name: Assemble publish dir
        run: |
          mkdir -p dist
          cp web/index.html web/mq_js_bundle.js dist/
          cp target/wasm32-unknown-unknown/release/mygame.wasm dist/
          [ -d assets ] && cp -r assets dist/assets

      - uses: actions/setup-node@v4
        with:
          node-version: 22

      - name: Deploy production
        if: github.event_name == 'push'
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
        run: npx netlify-cli@23 deploy --dir=dist --prod --message="${{ github.sha }}"

      - name: Deploy PR preview
        if: github.event_name == 'pull_request' && github.event.pull_request.head.repo.fork == false
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
        run: npx netlify-cli@23 deploy --dir=dist --alias="pr-${{ github.event.number }}"
```

`mygame`은 크레이트 이름으로 바꾼다. 미리보기 URL은 `pr-<번호>--<site>.netlify.app`.

## 배포 후 확인

```sh
curl -sI https://<site>.netlify.app/mygame.wasm | grep -i content-type   # application/wasm
```
- 브라우저 콘솔에 `Version mismatch`, `Missed function` 경고가 없어야 한다.
- 에셋 404가 있으면 `dist/assets` 경로와 대소문자를 확인한다.

## 유지보수 체크리스트
- macroquad 버전 올릴 때: `web/mq_js_bundle.js`도 같은 태그로 갱신.
- `netlify-cli` 메이저 올릴 때: 워크플로의 `@23` 갱신.
- 토큰 로테이션: Netlify 개인 토큰은 계정 단위다. 유출 시 Applications에서 revoke.

## 함정 요약
| 증상 | 원인 | 해결 |
|---|---|---|
| 배포 성공인데 사이트가 옛 버전 | Git CD가 연결돼 Netlify가 덮어씀 | 레포 연결 해제 |
| 콘솔 `Version mismatch` | 번들과 크레이트 버전 불일치 | 같은 태그의 번들로 교체 |
| 포크 PR에서 배포 실패 | 시크릿 미전달 | `fork == false` 조건 (이미 포함) |
| `--site` 줬는데 아무것도 안 올라감 | 폴더 경로를 ID 자리에 넣음 | `--dir`로 폴더, `--site`는 ID |
| 배포 후에도 옛 wasm 로드 | `immutable` 캐시를 해시 없는 파일명에 적용 | 기본 캐시 유지 |

## 대안 비교
- **GitHub Pages**: 같은 빌드 job에 `actions/deploy-pages`만 붙이면 되고 토큰이 필요 없다. 커스텀 헤더·PR 미리보기가 필요 없으면 더 단순.
- **Netlify Git CD로 Rust 직접 빌드**: 가능하지만 기본 툴체인 없음, cargo 캐시 없음, 빌드 분 소모. ([decisions/0001](../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md))
- **itch.io (butler)**: 게임 배포 목적이면 같은 `dist/`를 추가 step으로 올린다.

## 관련 노트
- [concepts/static-wasm-hosting.md](../concepts/static-wasm-hosting.md)
- [reference/macroquad/wasm-build.md](../reference/macroquad/wasm-build.md)
- [reference/netlify/deploy-from-ci.md](../reference/netlify/deploy-from-ci.md)
- [reference/github-actions/rust-wasm-build.md](../reference/github-actions/rust-wasm-build.md)
