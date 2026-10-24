# KB

개인 지식 베이스. "왜?"에 답할 수 있을 때까지 파고든 내용만 남긴다.

## 구조

노트는 **도메인이 아니라 "노트의 종류"** 로 저장하고([Diátaxis](https://diataxis.fr/) 차용), **도메인별 탐색은 `maps/`의 지도 노트**로 한다.

```
KB/
├── README.md          # 규칙 + 자동 생성 인덱스
├── CLAUDE.md          # Claude Code가 이 KB를 읽고 쓰는 규칙
├── _templates/        # 노트 템플릿 (note.md, map.md)
├── maps/              # 도메인별 입구(Map of Content). 링크만 모은다
├── guides/            # How-to. "X를 하려면" — 여러 도구를 엮은 절차
├── reference/<tool>/  # 사실 정리. 도구/기술 단위 하위 폴더
├── concepts/          # 원리 설명. "왜 그렇게 동작하나"
├── decisions/         # 의사결정 기록(ADR). "왜 A가 아니라 B를 택했나"
└── tools/kb.py        # check(검증) / index(인덱스 생성)
```

### 왜 저장은 종류별, 탐색은 지도로 하는가

- 하나의 주제가 여러 도메인에 걸치는 일이 흔하다. 예: "macroquad를 Netlify에 GitHub Actions로 배포"는 게임개발·Rust·CI 세 도메인이다. 폴더는 한 곳에만 둘 수 있지만 지도에는 여러 곳에 실을 수 있다.
- 종류는 5개로 고정되어 폴더가 흔들리지 않는다. 도메인은 `tags`와 `maps/`로 표현하므로 새 도메인이 생겨도 폴더를 옮길 일이 없다.
- 읽는 목적이 다르다. 절차가 급할 때는 `guides/`, 사실 확인은 `reference/`, 이해가 필요하면 `concepts/`, "그때 왜 그랬지"는 `decisions/`, "이 분야에 뭐가 있지"는 `maps/`.

### 무엇을 넣고 무엇을 넣지 않는가

판별 기준은 하나다. **"이 프로젝트가 사라져도 유용한가?"**
- 예 → KB. (Netlify CLI 동작 방식, Rust 캐시가 중요한 이유)
- 아니오 → 그 프로젝트 레포. (특정 게임의 TODO, 오늘 깨진 빌드 로그, 회의 메모)

프로젝트 기록이 섞이면 검색 결과가 썩는다. 지식만 둔다.

### 각 폴더의 규칙

| 폴더 | 한 노트의 단위 | 파일명 |
|---|---|---|
| `maps/` | 하나의 도메인 | `<도메인>.md` |
| `guides/` | 하나의 목표(end-to-end) | `<목표-설명>.md` (kebab-case) |
| `reference/<tool>/` | 하나의 도구 × 하나의 주제 | `<주제>.md` |
| `concepts/` | 하나의 개념 | `<개념>.md` |
| `decisions/` | 하나의 결정 | `NNNN-<결정-요약>.md` (번호 순차) |

- 가이드는 reference를 **중복하지 않고 링크**한다. 사실은 reference 한 곳에만 둔다.
- 모든 노트는 `_templates/`의 frontmatter를 갖는다. 특히 `verified`에 **1차 출처로 확인한 것과 포럼 수준 출처만 있는 것을 구분**해 적는다.
- `status`: `draft` → `verified` → (시간이 지나 의심되면) `stale`.
- 외부 자료는 요약만 남기고 원문 URL을 `sources`에 적는다.
- 새 노트는 **최소 한 지도에 실어야 한다.** 실을 지도가 없으면 새 도메인이니 `_templates/map.md`로 지도를 만든다.

### 도구

```sh
python3 tools/kb.py check   # frontmatter·폴더 일치·끊어진 링크·지도 수록 여부 검증
python3 tools/kb.py index   # 아래 인덱스 섹션 재생성
```
GitHub Actions(`kb-check`)가 push/PR마다 둘을 실행한다. 인덱스가 오래되면 실패한다.

## 인덱스

<!-- index:start -->

_`python3 tools/kb.py index` 로 생성. 손으로 고치지 말 것._

### 지도 (도메인별 입구)
- [지도: CI/CD와 호스팅](maps/ci-cd-hosting.md)
- [지도: 게임 개발](maps/gamedev.md)
- [지도: Rust](maps/rust.md)

### guides
- [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md)
- [그림 못 그려도 도트 게임 만들기 (에셋 전략)](guides/pixel-art-without-an-artist.md)

### reference
- github-actions
  - [GitHub Actions에서 Rust → wasm32 빌드](reference/github-actions/rust-wasm-build.md)
- macroquad
  - [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md)
  - [macroquad 픽셀 퍼펙트 렌더링 (내부 해상도 고정 + 정수 배율)](reference/macroquad/pixel-perfect-rendering.md)
  - [macroquad WASM 빌드와 JS 번들](reference/macroquad/wasm-build.md)
- netlify
  - [CI에서 netlify-cli로 배포](reference/netlify/deploy-from-ci.md)
- rust-game-engines
  - [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)

### concepts
- [1인 개발용 액션 로그라이트 설계 원칙](concepts/action-roguelite-for-solo-dev.md)
- [정적 WASM 호스팅](concepts/static-wasm-hosting.md)

### decisions
- [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md)

### 태그
- `android`: [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md), [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- `assets`: [그림 못 그려도 도트 게임 만들기 (에셋 전략)](guides/pixel-art-without-an-artist.md)
- `bevy`: [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- `ci`: [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [지도: CI/CD와 호스팅](maps/ci-cd-hosting.md), [GitHub Actions에서 Rust → wasm32 빌드](reference/github-actions/rust-wasm-build.md), [CI에서 netlify-cli로 배포](reference/netlify/deploy-from-ci.md)
- `combat`: [1인 개발용 액션 로그라이트 설계 원칙](concepts/action-roguelite-for-solo-dev.md)
- `deploy`: [지도: CI/CD와 호스팅](maps/ci-cd-hosting.md), [CI에서 netlify-cli로 배포](reference/netlify/deploy-from-ci.md)
- `game-design`: [1인 개발용 액션 로그라이트 설계 원칙](concepts/action-roguelite-for-solo-dev.md), [지도: 게임 개발](maps/gamedev.md)
- `gamedev`: [1인 개발용 액션 로그라이트 설계 원칙](concepts/action-roguelite-for-solo-dev.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [그림 못 그려도 도트 게임 만들기 (에셋 전략)](guides/pixel-art-without-an-artist.md), [지도: 게임 개발](maps/gamedev.md), [지도: Rust](maps/rust.md), [macroquad 픽셀 퍼펙트 렌더링 (내부 해상도 고정 + 정수 배율)](reference/macroquad/pixel-perfect-rendering.md), [macroquad WASM 빌드와 JS 번들](reference/macroquad/wasm-build.md), [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- `gamepad`: [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md), [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- `github-actions`: [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [지도: CI/CD와 호스팅](maps/ci-cd-hosting.md), [GitHub Actions에서 Rust → wasm32 빌드](reference/github-actions/rust-wasm-build.md)
- `godot`: [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- `hosting`: [정적 WASM 호스팅](concepts/static-wasm-hosting.md), [지도: CI/CD와 호스팅](maps/ci-cd-hosting.md), [CI에서 netlify-cli로 배포](reference/netlify/deploy-from-ci.md)
- `input`: [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md)
- `licensing`: [그림 못 그려도 도트 게임 만들기 (에셋 전략)](guides/pixel-art-without-an-artist.md)
- `macroquad`: [정적 WASM 호스팅](concepts/static-wasm-hosting.md), [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [지도: 게임 개발](maps/gamedev.md), [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md), [macroquad 픽셀 퍼펙트 렌더링 (내부 해상도 고정 + 정수 배율)](reference/macroquad/pixel-perfect-rendering.md), [macroquad WASM 빌드와 JS 번들](reference/macroquad/wasm-build.md), [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- `miniquad`: [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md), [macroquad WASM 빌드와 JS 번들](reference/macroquad/wasm-build.md)
- `netlify`: [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [지도: CI/CD와 호스팅](maps/ci-cd-hosting.md), [CI에서 netlify-cli로 배포](reference/netlify/deploy-from-ci.md)
- `pixel-art`: [그림 못 그려도 도트 게임 만들기 (에셋 전략)](guides/pixel-art-without-an-artist.md), [지도: 게임 개발](maps/gamedev.md), [macroquad 픽셀 퍼펙트 렌더링 (내부 해상도 고정 + 정수 배율)](reference/macroquad/pixel-perfect-rendering.md)
- `rendering`: [macroquad 픽셀 퍼펙트 렌더링 (내부 해상도 고정 + 정수 배율)](reference/macroquad/pixel-perfect-rendering.md)
- `roguelite`: [1인 개발용 액션 로그라이트 설계 원칙](concepts/action-roguelite-for-solo-dev.md)
- `rust`: [정적 WASM 호스팅](concepts/static-wasm-hosting.md), [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [지도: 게임 개발](maps/gamedev.md), [지도: Rust](maps/rust.md), [GitHub Actions에서 Rust → wasm32 빌드](reference/github-actions/rust-wasm-build.md), [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md), [macroquad 픽셀 퍼펙트 렌더링 (내부 해상도 고정 + 정수 배율)](reference/macroquad/pixel-perfect-rendering.md), [macroquad WASM 빌드와 JS 번들](reference/macroquad/wasm-build.md), [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- `solo-dev`: [1인 개발용 액션 로그라이트 설계 원칙](concepts/action-roguelite-for-solo-dev.md), [그림 못 그려도 도트 게임 만들기 (에셋 전략)](guides/pixel-art-without-an-artist.md)
- `wasm`: [정적 WASM 호스팅](concepts/static-wasm-hosting.md), [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [지도: Rust](maps/rust.md), [GitHub Actions에서 Rust → wasm32 빌드](reference/github-actions/rust-wasm-build.md), [macroquad WASM 빌드와 JS 번들](reference/macroquad/wasm-build.md), [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)

<!-- index:end -->
