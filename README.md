# KB

개인 지식 베이스. "왜?"에 답할 수 있을 때까지 파고든 내용만 남긴다.

## 구조

노트는 **도메인이 아니라 "노트의 종류"** 로 1차 분류한다 ([Diátaxis](https://diataxis.fr/) 프레임워크 차용).

```
KB/
├── README.md          # 이 문서: 규칙 + 인덱스
├── _templates/        # 노트 템플릿
├── guides/            # How-to. "X를 하려면" — 여러 도구를 엮은 절차
├── reference/         # 사실 정리. 도구/기술 단위 하위 폴더 (reference/<tool>/)
├── concepts/          # 원리 설명. "왜 그렇게 동작하나"
└── decisions/         # 의사결정 기록(ADR). "왜 A가 아니라 B를 택했나"
```

### 왜 도메인별이 아니라 종류별인가

- 하나의 주제가 여러 도메인에 걸치는 일이 흔하다. 예: "macroquad를 Netlify에 GitHub Actions로 배포"는 게임개발·호스팅·CI 세 도메인이다. 도메인 폴더로 나누면 어디에 둘지부터 고민하게 되고 중복이 생긴다.
- 종류는 4개로 고정되어 폴더가 흔들리지 않는다. 도메인은 `tags`로 표현하고 검색한다.
- 읽는 목적이 다르다. 절차가 급할 때는 `guides/`, 사실 확인은 `reference/`, 이해가 필요하면 `concepts/`, "그때 왜 그랬지"는 `decisions/`.

### 각 폴더의 규칙

| 폴더 | 한 노트의 단위 | 파일명 |
|---|---|---|
| `guides/` | 하나의 목표(end-to-end) | `<목표-설명>.md` (kebab-case) |
| `reference/<tool>/` | 하나의 도구 × 하나의 주제 | `<주제>.md` |
| `concepts/` | 하나의 개념 | `<개념>.md` |
| `decisions/` | 하나의 결정 | `NNNN-<결정-요약>.md` (번호 순차) |

- 가이드는 reference를 **중복하지 않고 링크**한다. 사실은 reference 한 곳에만 둔다.
- 모든 노트는 `_templates/note.md`의 frontmatter를 갖는다. 특히 `verified`에 **1차 출처로 확인한 것과 포럼 수준 출처만 있는 것을 구분**해 적는다.
- `status`: `draft` → `verified` → (시간이 지나 의심되면) `stale`.
- 외부 자료는 요약만 남기고 원문 URL을 `sources`에 적는다.

## 인덱스

### guides
- [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md)

### reference
- macroquad
  - [WASM 빌드와 JS 번들](reference/macroquad/wasm-build.md)
- netlify
  - [CI에서 netlify-cli로 배포](reference/netlify/deploy-from-ci.md)
- github-actions
  - [Rust → wasm32 빌드 워크플로](reference/github-actions/rust-wasm-build.md)

### concepts
- [정적 WASM 호스팅: 번들러 없는 WASM 앱이 호스트에 요구하는 것](concepts/static-wasm-hosting.md)

### decisions
- [0001 Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md)
