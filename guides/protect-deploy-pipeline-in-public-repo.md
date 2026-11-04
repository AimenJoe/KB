---
title: 공개 레포에서 배포 파이프라인 지키기 — Environment·브랜치 규칙·CODEOWNERS
type: guide
tags: [github, github-actions, ci-cd, security, solo-dev]
status: draft
created: 2026-11-04
updated: 2026-11-04
verified: |
  1차 출처로 확인(2026-11-04, docs.github.com 원문을 curl로 받아 읽음):
  - Deployments and environments: Environment 시크릿은 그 환경을 쓰는 잡만 읽고, 승인이 걸려 있으면 승인 전에는 못 읽는다.
    Deployment branches/tags는 모든 공개 레포에서, Free·Pro·Team 플랜의 required reviewers·wait timer·관리자 우회·사용자 지정 보호 규칙은 공개 레포에서만.
    포크의 같은 이름 갈래·같은 이름 태그로는 그 환경에 배포할 수 없다. "prevent self-review" 선택지가 있다.
  - Available rules for rulesets: Restrict creations·updates·deletions(우회 권한자만), Block force pushes(기본 켬), PR 필수 + 코드 주인 검토,
    우회 목록에 역할·팀·GitHub App. push ruleset(파일 경로로 막기)은 Team 플랜의 internal·private 레포용.
  직접 해 봄(nail-under-the-roots, 2026-11-04): 웹 배포 워크플로를 build(시크릿 없음)·publish(Environment) 두 잡으로 가름 — 실제 CI 결과는 그 레포 기록.
  2차 출처만 있음: 포크 PR 워크플로에 레포 시크릿이 가지 않는다(GitHub 문서의 일반 설명으로 알려진 것 — 이번에 해당 쪽 원문은 다시 읽지 않음),
  코드 주인은 자기 PR을 승인할 수 없어 혼자 하는 레포는 우회 목록이 필요하다(블로그).
sources:
  - https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
---

# 공개 레포에서 배포 파이프라인 지키기

## 요약
공개 레포는 누구나 보고 포크·PR을 할 수 있지만 **쓰기는 권한자만** 된다. 지켜야 할 것은 셋 — 배포 갈래에 쓰기, 배포 시크릿 읽기, 워크플로를 고쳐 시크릿 빼돌리기. 무료 플랜 공개 레포에서도 다 막힌다: **배포 시크릿은 Environment에(정한 갈래에서만 열림)**, **배포 갈래는 브랜치 규칙으로 우회 목록(본인 + 쓰는 봇)만**, **워크플로 파일엔 CODEOWNERS**.

## 본문
1. **배포 잡을 따로 뗀다.** 빌드·시험 잡에는 배포 시크릿을 두지 않고, 산출물을 아티팩트로 넘겨 `publish` 잡만 `environment:`에 들어간다. 갈래마다 환경을 고르려면 `environment: ${{ github.ref == 'refs/heads/main' && 'prod' || 'dev' }}`.
2. **Environment**(Settings → Environments): Deployment branches = Selected → `main`(운영)·`release/**`(개발판). 운영에는 Required reviewers(본인)를 걸면 배포마다 승인 버튼이 생긴다. 시크릿을 환경에 넣고 **레포 시크릿의 같은 이름은 지운다** — 남겨 두면 다른 갈래·PR 워크플로가 여전히 읽는다(순서: 환경에 넣기 → 한 번 배포 확인 → 레포 것 지우기).
3. **브랜치 규칙**(Rulesets): 대상 `main`·`release/**`, Restrict updates·Restrict deletions·Block force pushes, 우회 목록 = Repository admin + 쓰는 GitHub App(자동화 봇). "PR 필수"는 혼자 바로 push하는 흐름이면 켜지 않는다.
4. **CODEOWNERS**: `/.github/ @본인` — PR이 워크플로를 고치면 본인 검토가 걸린다(규칙에서 코드 주인 검토를 켰을 때만 막는 힘이 있다).
5. **Actions 설정**: 포크 PR 워크플로는 외부 기여자 승인 필요, `GITHUB_TOKEN` 기본 권한은 읽기만(쓰기가 필요한 잡은 `permissions:`에 적는다), Actions의 PR 만들기·승인 끔.
6. 협업자에게 Write를 주지 않고 기여는 포크 PR로. 계정 2단계 인증.

## 왜?
GitHub는 **워크플로를 실행하는 갈래의 워크플로 파일**을 쓴다. 같은 레포에 push할 수 있는 사람은 자기 갈래에서 워크플로를 고쳐 레포 시크릿을 출력할 수 있다 — 레포 시크릿은 "레포에 쓸 수 있는 모든 사람의 것"이다. Environment 시크릿은 환경의 갈래 규칙을 통과한 잡만 받으니, 고친 워크플로가 다른 갈래에서 돌면 시크릿이 비어 있다. 그 갈래(main·release)에 쓰는 것 자체는 브랜치 규칙이 막는다. 둘이 같이 있어야 닫힌다.

## 함정
- 시크릿을 환경으로 옮기고 레포 시크릿을 지우지 않으면 아무것도 안 바뀐다.
- 하나의 잡이 PR에서도 돌고 배포도 하면 환경 갈래 규칙에 PR 실행이 막힌다 — 그래서 잡을 나눈다(PR 미리 보기 배포는 포기하거나 별도 환경).
- 아직 없는 환경 이름을 워크플로에 쓰면 첫 실행 때 보호 없는 환경이 저절로 생긴다 — 규칙은 사람이 따로 건다.
- 파일 경로로 push를 막는 push ruleset은 무료 공개 레포에 없다.
- 읽기 전용 토큰(예: 비공개 에셋 레포 읽기)이라도 레포 시크릿이면 쓰기 권한자는 읽는다 — 협업자를 들이면 그것도 환경으로.

## 관련 노트
- [공개 레포를 비공개로 바꿀 때](../reference/github-actions/public-to-private-repo.md)
- [macroquad WASM → Netlify 배포](macroquad-wasm-netlify-github-actions.md)
