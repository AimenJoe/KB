---
title: "지도: CI/CD와 호스팅"
type: map
tags: [ci, deploy, hosting, github-actions, netlify, cloudflare]
status: verified
created: 2026-10-24
updated: 2026-11-10
---

# 지도: CI/CD와 호스팅

## GitHub Actions
- [Rust → wasm32 빌드 워크플로](../reference/github-actions/rust-wasm-build.md) — 툴체인 액션 비교, 캐시, concurrency
- [GitHub Pages에 정적 페이지](../reference/github-actions/pages-static-site.md) — Actions 배포, 처음 한 번 사람이 켜기(GITHUB_TOKEN 불가), 릴리스 API로 버전·소식 채우기, 글꼴 줄이기
- [버전 올리기 = 릴리스](../reference/github-actions/release-from-version-bump.md) — CI가 태그를 만들고(GITHUB_TOKEN 태그는 다른 워크플로를 안 깨움) 빌드를 `workflow_call`로 부르기, 앱에 버전·커밋 찍기
- [공개 레포를 비공개로 바꿀 때](../reference/github-actions/public-to-private-repo.md) — Actions가 돈이 된다(Free 월 $12어치, macOS ≈10배)·Pages 자동 내림·Release 익명 404, 바꾸기 전 실행 양 재기·줄이기·홈페이지 먼저 옮기기
- [공개 레포에서 배포 파이프라인 지키기](../guides/protect-deploy-pipeline-in-public-repo.md) — 배포 잡을 떼고 시크릿은 Environment(정한 갈래만), 배포 갈래는 브랜치 규칙 우회 목록만, CODEOWNERS·Actions 권한, 레포 시크릿을 지우지 않으면 소용없다
- [Node 20 폐기 — 액션을 node24 판으로](../reference/github-actions/node24-action-runtime.md) — `runs.using`이 정한다(`node-version`과 무관), 액션마다 node24 메이저·올릴 때 깨지는 것(checkout v6 자격 증명 파일, setup-node 자동 캐시, upload-artifact는 v6부터)
- [액션·Rust 버전 고정](../reference/github-actions/pin-actions-and-rust-toolchain.md) — 시크릿 곁의 액션은 커밋 SHA + `# v태그`(Dependabot이 올림, 잠금 파일이 더 강함), `rust-toolchain.toml`은 숫자로, dtolnay를 SHA로 쓰면 `toolchain` 입력(master 역사의 SHA), 필수 상태 검사까지 켜야 막는다
- [Playwright 연기 시험이 느려질 때](../reference/github-actions/playwright-smoke-test-ci-time.md) — ubuntu-latest에서 `--with-deps`가 새로 받는 건 글꼴 apt뿐(미러가 느리면 몇 분), 브라우저 캐시는 공식 비권장, 같은 SHA를 운영 갈래에서 다시 시험하지 않기 · 콘솔 error만 모으면 엔진 경고(잘라 냄)를 놓친다 · 운영 빌드도 따로 띄운다
- [Android APK 빌드](../guides/macroquad-android-apk-github-actions.md) — 덮어 설치 = 같은 키 + 큰 versionCode, 키를 캐시에만 두면 7일 뒤 사라짐
- [공개 레포 + 비공개 에셋 레포](../guides/pixel-art-without-an-artist.md#공개-레포에서-유료-팩-다루기) — 두 번째 checkout, fine-grained 토큰, Actions 비용은 도는 레포 기준

## Git·GitHub
- [브랜치 히스토리의 파일을 고친 판으로 바꿔 쓰기](../guides/rewrite-branch-history-replace-files.md) — 범위부터 재기(main·태그), 옛 blob → 고친 blob 표 + `--index-filter`, 끝 트리가 같은지 확인, force-with-lease, GitHub에 SHA로 남고 Support는 민감한 데이터만

## Netlify
- [CI에서 netlify-cli로 배포](../reference/netlify/deploy-from-ci.md) — Git CD vs CLI 업로드, 섞으면 덮어쓰기, 헤더/캐시
- [정적 WASM 호스팅](../concepts/static-wasm-hosting.md) — 정적 호스트가 제공해야 하는 것

## Cloudflare
- [Email Routing — 도메인 메일 받기](../reference/cloudflare/email-routing.md) — MX·SPF만으론 부족, 주소마다 규칙 + 확인된 메일함, `550 5.1.1 Address does not exist`(RCPT 단계) = 규칙 없음, 보내기는 따로(Email Sending은 Workers Paid)
- [정적 사이트 운영에 쓰기](../reference/cloudflare/static-site-extras.md) — 프록시 뒤 엣지 통계·쿠키 없는 Web Analytics(Free는 하위 도메인 전체에 주입)·리디렉트, R2 내려받기 무료, Pages/Workers 파일 25 MiB

## 웹 앱(PWA)
- [웹 게임을 PWA로](../reference/web/pwa-install-fullscreen-orientation.md) — 매니페스트·빌드 SHA 캐시 서비스 워커(skipWaiting 없음)·no-cache 헤더, 전체 화면·가로 잠금은 Android/데스크톱만, iPhone 홈 화면 앱은 저장소가 따로

## 엮은 절차
- [운영판과 개발판을 갈라 내보내기](../guides/dev-and-release-flavors.md) — 마일스톤 갈래, 운영판 `--no-default-features`, Netlify 별칭 + build.txt 확인, Android 개발판 패키지(`….dev.<게임>` — 마지막 조각 = 라이브러리 이름)·기록 폴더, 운영판도 따로 띄워 보기, 미리 보기 Release 갈아 끼우기
- [macroquad WASM → GitHub Actions → Netlify](../guides/macroquad-wasm-netlify-github-actions.md)
- [0001 빌드는 CI에서, 호스팅은 CLI 업로드로](../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md)

## 다른 지도
- [게임 개발](gamedev.md) · [Rust](rust.md)
