---
title: GitHub Actions에서 Rust → wasm32 빌드
type: reference
tags: [github-actions, rust, wasm, ci]
status: verified
created: 2026-10-24
updated: 2026-10-24
verified: |
  1차 출처로 확인: dtolnay/rust-toolchain의 `targets` 입력, actions-rust-lang/setup-rust-toolchain의 `target` 입력과 rust-cache 기본 내장,
  macroquad 자체 CI의 wasm32 매트릭스.
  2차 출처만 있음: 없음.
sources:
  - https://github.com/dtolnay/rust-toolchain
  - https://github.com/actions-rust-lang/setup-rust-toolchain
  - https://github.com/Swatinem/rust-cache
  - https://github.com/not-fl3/macroquad/blob/master/.github/workflows/rust.yml
---

# GitHub Actions에서 Rust → wasm32 빌드

## 요약
툴체인 액션에 `wasm32-unknown-unknown` 타깃을 추가하고 `Swatinem/rust-cache`를 붙이면 끝. 번들러가 없는 프로젝트(macroquad 등)는 `cargo build` 한 줄이다.

## 최소 단계

```yaml
- uses: actions/checkout@v4
- uses: dtolnay/rust-toolchain@stable
  with:
    targets: wasm32-unknown-unknown        # 쉼표로 여러 개 가능
- uses: Swatinem/rust-cache@v2
- run: cargo build --release --target wasm32-unknown-unknown
```

### 액션 선택
| 액션 | 타깃 입력 이름 | 캐시 |
|---|---|---|
| `dtolnay/rust-toolchain` | `targets` | 별도로 `Swatinem/rust-cache` |
| `actions-rust-lang/setup-rust-toolchain` | `target` | 기본 내장(`cache: true`) |
| `actions-rs/toolchain` | `target` | 없음. **아카이브됨**, 신규 사용 비권장 (macroquad 자체 CI는 아직 이걸 쓴다) |

### 툴체인 고정
`rust-toolchain.toml`을 레포에 두면 로컬과 CI가 같은 버전을 쓴다. 액션은 이 파일을 존중한다.
```toml
[toolchain]
channel = "stable"
targets = ["wasm32-unknown-unknown"]
```

### 캐시가 중요한 이유
Rust는 의존성 컴파일이 빌드 시간의 대부분이다. `rust-cache`는 `~/.cargo`와 `target/`을 `Cargo.lock` 해시 기준으로 캐시해 두 번째 빌드부터 수 분 → 수십 초로 줄인다. Netlify 같은 호스팅 빌더에는 이 캐시가 없다. → [decisions/0001](../../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md)

## 산출물 조립
빌드 산출물은 `target/wasm32-unknown-unknown/release/<crate>.wasm` 하나다. 배포 디렉터리는 직접 조립한다.
```sh
mkdir -p dist
cp web/index.html web/mq_js_bundle.js dist/
cp target/wasm32-unknown-unknown/release/mygame.wasm dist/
[ -d assets ] && cp -r assets dist/assets
```
`dist/`를 `actions/upload-artifact`로 올려두면 배포 단계를 별도 job으로 분리하거나 다른 호스트(GitHub Pages, itch.io butler)에 재사용할 수 있다.

## 동시성
같은 브랜치에 push가 연달아 오면 이전 배포 job을 취소한다.
```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: true
```

## 관련 노트
- [reference/macroquad/wasm-build.md](../macroquad/wasm-build.md)
- [reference/netlify/deploy-from-ci.md](../netlify/deploy-from-ci.md)
