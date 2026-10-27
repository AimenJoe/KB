---
title: GitHub Pages에 정적 페이지 올리기 — Actions 배포, 처음 켜기, 릴리스에서 읽는 값
type: reference
tags: [github-actions, ci-cd, hosting, static-site, fonts]
status: verified
created: 2026-10-25
updated: 2026-10-27
verified: |
  1차 출처로 확인(2026-10-25):
  - 각 액션 레포의 태그와 action.yml(git fetch로 읽음): configure-pages v6.0.0(2026-03-24, node24, `enablement` 입력은 "GITHUB_TOKEN 말고 다른 토큰이 필요"),
    upload-pages-artifact v5.0.0(2026-04-08, composite, `path` 필수·기본 `_site/`, `include-hidden-files` 기본 false로 점 파일 제외, .git·.github는 늘 제외, 보관 1일),
    deploy-pages v5.0.1(2026-09-01, node24).
  - 직접 실행(nail-under-the-roots pages.yml): Pages를 켜기 전 첫 실행이 configure-pages에서 "Get Pages site failed … Not Found"로 실패.
  - fontTools 4.67(subset, woff2 + brotli)로 픽셀 한글 글꼴 452KB → 9KB(페이지 글자만, 그때 게임 서브셋 기준. 지금 게임 서브셋은 344KB).
  - 헤드리스 Chromium에서 api.github.com/repos/<repo>/releases 읽기, 요청 제한(403)일 때 적어 둔 값이 남는 것.
  직접 실행(2026-10-27): 페이지를 다시 짠 뒤 사람 브라우저에서 새 HTML + 캐시된 옛 style.css가 만나 깨져 보였다
    (새 HTML에 옛 CSS를 붙여 헤드리스로 똑같이 재현). CSS·JS·글꼴 주소에 내용 해시(?v=sha1 8자)를 붙여 해결.
  2차/확인 못 함: 비인증 API 요청 제한 "IP당 시간 60회"는 기억에 의존(이 세션에서 docs.github.com 접속이 막혀 원문 미확인).
  GitHub Free에서 공개 레포 Pages가 무료라는 것은 요금 문서 원본(github/docs plans)으로 본 범위까지.
sources:
  - https://github.com/actions/configure-pages
  - https://github.com/actions/upload-pages-artifact
  - https://github.com/actions/deploy-pages
  - https://fonttools.readthedocs.io/en/latest/subset/index.html
---

# GitHub Pages에 정적 페이지 올리기

## 요약
빌드 도구 없는 한 장짜리 페이지(HTML·CSS·이미지)는 레포의 폴더 하나(`site/`)를 **Actions로 Pages에 올리는** 게 가장 단순하다. 걸리는 곳은 하나다. **Pages는 처음 한 번 사람이 켜야 한다.** `GITHUB_TOKEN`으로는 켤 수 없어서, 켜기 전 첫 실행은 실패한다.

## 본문

### 워크플로
```yaml
on:
  push: { branches: [main], paths: ['site/**', '.github/workflows/pages.yml'] }
  workflow_dispatch:
permissions: { contents: read, pages: write, id-token: write }
concurrency: { group: pages, cancel-in-progress: false }
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: { name: github-pages, url: ${{ steps.deploy.outputs.page_url }} }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v6
      - uses: actions/upload-pages-artifact@v5
        with: { path: site }
      - id: deploy
        uses: actions/deploy-pages@v5
```
- `pages: write` + `id-token: write`가 없으면 deploy-pages가 실패한다(OIDC로 배포 권한을 받는다).
- `environment: github-pages`는 Pages가 만드는 환경이다. 기본 보호 규칙상 기본 브랜치에서만 배포된다.
- 점으로 시작하는 파일(`.nojekyll` 등)은 기본으로 빠진다. 필요하면 `include-hidden-files: true`.
- Actions 배포는 Jekyll을 돌리지 않으니 `.nojekyll`도 필요 없다.

### 처음 켜기
- 레포 **Settings → Pages → Build and deployment → Source = GitHub Actions**.
- 켜기 전에는 `configure-pages`가 `Get Pages site failed. Please verify that the repository has Pages enabled …`로 멈춘다.
- 자동으로 켜려면 `enablement: true` + 관리 권한이 있는 토큰(PAT `repo` 또는 Pages 쓰기)이 필요하다. 한 번뿐이라 손으로 켜는 편이 토큰을 하나 덜 둔다.
- 주소: 사용자 `<owner>.github.io/<repo>/`. 그래서 페이지 안 경로는 **상대 경로**로 쓴다(`/img/…`는 레포 이름이 빠진다).

### 릴리스에서 읽는 값
- 최신 버전·날짜·APK 직접 주소·소식 목록을 페이지에 박으면 릴리스마다 페이지를 고쳐야 한다. 페이지 스크립트가 `https://api.github.com/repos/<owner>/<repo>/releases?per_page=4`를 읽어 채운다(CORS 허용, 인증 없음).
- 비인증 요청은 IP마다 제한이 있다. 막히면(403) **HTML에 적어 둔 값과 릴리스 목록 링크가 그대로 보이게** 만든다. 스크립트는 덮어쓰기만 한다.
- 에셋 직접 주소는 `assets[].browser_download_url`. 못 읽었을 때 링크는 `/releases/latest`로 둔다.

### 큰 글꼴 줄이기
- 한글 픽셀 글꼴(2,350자 서브셋도 450KB)을 제목에만 쓴다면, 페이지에 나오는 글자만 남겨 woff2로 줄인다. `fontTools.subset`으로 HTML 글자를 모으고(태그 제거·엔티티 풀기), 스크립트가 채울 숫자·영문을 더한다.
- OFL 글꼴은 줄여도 된다. 다만 **예약 글꼴 이름(Reserved Font Name)**이 있으면 바꾼 판에 그 이름을 쓸 수 없다. 라이선스 첫 줄을 확인한다. OFL 원문을 글꼴 곁에 둔다.
- 글을 바꿀 때마다 다시 줄여야 한다(빠진 글자는 대체 글꼴로 나온다). 줄이는 스크립트를 레포에 둔다.

## 왜?
- Pages 배포 권한은 저장소 쓰기와 다르다. 워크플로가 저장소 설정(Pages 켜기)을 바꾸려면 관리 권한이 필요하다. `GITHUB_TOKEN`에는 그 권한이 없다. 그래서 "켜기"는 사람 몫이고 "올리기"는 워크플로 몫이다.
- 정적 페이지에 빌드 단계를 두지 않으면 고칠 것이 HTML 한 곳뿐이다. 한 장짜리 소개 페이지는 템플릿 엔진이 더 많은 것을 고장 낸다.

## 함정
- **새 HTML + 캐시된 옛 CSS.** Pages는 정적 파일에 짧은 캐시를 준다(몇 분, 정확한 값은 원문 미확인). 페이지 구조를 크게 바꾸면 그동안 새 HTML이 옛 CSS로 그려져, 숨긴 요소(본문 건너뛰기 링크·고정 장식 목록)가 드러나고 배치가 깨진다. 빌드 스크립트가 `style.css?v=<내용 해시>`처럼 CSS·JS(그리고 CSS 안의 글꼴) 주소에 해시를 붙이면, 내용이 바뀔 때 주소도 바뀐다. 글꼴 해시를 CSS에 먼저 넣고 그 CSS로 해시를 잰다.
- 첫 실행 실패를 고장으로 보지 말 것. 켠 뒤 `workflow_dispatch`로 다시 돌린다.
- 도트 그림은 `image-rendering: pixelated`를 주지 않으면 브라우저가 흐리게 키운다.
- 스크린숏에 제3자 에셋 팩 그림이 들어가면, 원본 파일이 아니라도 라이선스 기록과 페이지 크레딧을 남긴다.

## 관련 노트
- [버전 올리기 = 릴리스](release-from-version-bump.md) — 페이지가 읽는 Release를 만드는 쪽
- [CI에서 netlify-cli로 배포](../netlify/deploy-from-ci.md) — 게임(WASM)은 Netlify, 소개 페이지는 Pages로 나눈 경우
- [정적 WASM 호스팅](../../concepts/static-wasm-hosting.md)
