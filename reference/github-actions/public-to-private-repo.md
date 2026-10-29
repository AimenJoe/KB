---
title: 공개 레포를 비공개로 바꿀 때 — Actions 비용·Pages·Release가 어떻게 되나
type: reference
tags: [github, github-actions, ci-cd, solo-dev]
status: draft
created: 2026-10-29
updated: 2026-10-29
verified: |
  1차 출처로 확인(2026-10-29, docs.github.com 원문을 curl로 받아 확인):
  - Actions: 공개 레포의 표준 GitHub 호스팅 러너와 self-hosted 러너는 무료이고 포함 사용량을 깎지 않는다.
    비공개 레포는 플랜의 "Included compute usage (per month)"로 잰다: GitHub Free $12, Pro $18, Team $18.
    산출물 저장 Free 500 MB·Pro 1 GB, 캐시 레포마다 10 GB. 분당 단가 Linux 2-core $0.006, Windows $0.010, macOS $0.062.
  - 공개 범위 바꾸기 문서(하위 조사가 인용, Claude는 Actions 문서만 다시 봄): Free 계정에서 비공개로 바꾸면 게시된 Pages가 자동으로 내려간다.
  - REST: 인증 없이 비공개 리소스를 요청하면 404(문서).
  직접 잰 것: 한 게임 레포(nail-under-the-roots)의 4.5일 실행 1,216건 → 그대로 비공개면 월 ≈ $175(Linux ≈11,600분 + macOS ≈1,700분).
  추정: 비공개 레포 Release 파일을 익명 사용자가 받지 못한다(404 규칙에서), 공개 범위를 바꿔도 시크릿은 남는다(문서에 삭제 언급 없음).
  확인 못 함: Pro 월 가격(pricing 페이지가 세션 프록시에 막힘).
sources:
  - https://docs.github.com/en/billing/concepts/product-billing/github-actions
  - https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility
  - https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
---

# 공개 레포를 비공개로 바꿀 때

## 요약
기술적으로는 CI가 그대로 돈다(태그·Release·워크플로 호출·시크릿은 같은 레포 안의 일). 깨지는 것은 셋: **Pages가 내려가고**(Free), **홈페이지가 읽던 Release·API가 익명에게 404**가 되고, **Actions가 돈이 된다**(Free 월 $12어치, macOS는 Linux의 약 10배). 공개일 때 무료라 아무도 안 세던 실행 양을 먼저 재고, 줄이거나 결제·예산을 건 뒤에 바꾼다.

## 본문
### 바꾸기 전에 할 일(순서)
1. **실행 양 재기**: Actions API(`/repos/{o}/{r}/actions/runs`)로 워크플로마다 1회 분(job마다 분 단위 올림)·하루 횟수 → 월 금액. 산출물 수·용량도(90일 보관이 기본).
2. **줄이기**: 무거운·드문 것(헤드리스 연기 시험, macOS 빌드)은 수동·태그 때만, 작업 브랜치 push에서는 배포 빼기, `retention-days`를 며칠로, 옛 산출물 지우기. macOS는 내 Mac에 self-hosted 러너(무료).
3. **Pages 옮기기**: 홈페이지를 새 공개 레포로 먼저(Free는 공개 레포에서만 Pages). 레포 이름이 페이지 주소(`<user>.github.io/<repo>`)라, 원래 이름을 홈페이지에 주고 코드 레포 이름을 바꾸면 주소·링크가 그대로다(대신 옛 이름 리다이렉트가 끊긴다).
4. **공개로 내보낼 파일 길 만들기**: 코드 레포 CI가 공개 레포에 Release를 만들려면 GITHUB_TOKEN으로는 안 된다(워크플로가 든 레포로 한정) → 그 레포 하나만 Contents 쓰기인 fine-grained PAT 또는 GitHub App 설치 토큰(만료 없음)을 시크릿으로.
5. 그 뒤에 비공개로.

### 그대로인 것
- 외부 배포(예: Netlify CLI로 Actions에서 배포)는 레포 공개 여부와 무관하다.
- 시크릿·태그·Release·실행 기록은 레포에 남는다(비공개 Release는 로그인한 권한자만).

## 왜?
- 공개 레포의 Actions는 무료라서 실행 양이 쉽게 커진다(세션마다·push마다 웹 배포·연기 시험·macOS 빌드). 비공개로 바꾸는 순간 같은 양이 그대로 청구 대상이 되고, Free 계정은 결제 수단이 없으면 포함량을 다 쓴 뒤 **막힌다** — 배포가 조용히 멈춘다.
- Pages가 자동으로 내려가는 것은 플랜 조건(Free = 공개 레포만)이라, 바꾸는 순서를 틀리면 홈페이지가 비는 시간이 생긴다.

## 함정
- "분"이 아니라 "돈"으로 준다(2026 기준 문서): macOS 1분 = Linux 약 10분. iOS 빌드를 push마다 돌리면 그것만으로 무료 몫을 넘는다.
- 산출물 저장도 무료 몫이 따로 작다(Free 500 MB) — APK·wasm을 push마다 90일 남기면 금방 넘는다.
- 홈페이지가 `api.github.com/repos/.../releases`를 읽던 코드는 404를 받는다 — 적어 둔 값으로 떨어지게 해 두었더라도 새 버전이 안 보인다.

## 관련 노트
- [Pages로 정적 사이트](pages-static-site.md)
- [버전 올리면 Release](release-from-version-bump.md)
- [CI에서 빌드해 Netlify CLI로 배포](../netlify/deploy-from-ci.md)
