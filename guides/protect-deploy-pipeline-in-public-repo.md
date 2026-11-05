---
title: 공개 레포에서 배포 파이프라인 지키기 — Environment·브랜치 규칙·CODEOWNERS
type: guide
tags: [github, github-actions, ci-cd, security, solo-dev]
status: draft
created: 2026-11-04
updated: 2026-11-05
verified: |
  1차 출처로 확인(2026-11-04, docs.github.com 원문을 curl로 받아 읽음):
  - Deployments and environments: Environment 시크릿은 그 환경을 쓰는 잡만 읽고, 승인이 걸려 있으면 승인 전에는 못 읽는다.
    Deployment branches/tags는 모든 공개 레포에서, Free·Pro·Team 플랜의 required reviewers·wait timer·관리자 우회·사용자 지정 보호 규칙은 공개 레포에서만.
    포크의 같은 이름 갈래·같은 이름 태그로는 그 환경에 배포할 수 없다. "prevent self-review" 선택지가 있다.
  - Available rules for rulesets: Restrict creations·updates·deletions(우회 권한자만), Block force pushes(기본 켬), PR 필수 + 코드 주인 검토,
    우회 목록에 역할·팀·GitHub App. push ruleset(파일 경로로 막기)은 Team 플랜의 internal·private 레포용.
  직접 해 봄(nail-under-the-roots, 2026-11-04): 웹 배포 워크플로를 build(시크릿 없음)·publish(Environment) 두 잡으로 가름 →
  ① 환경이 없을 때 첫 실행이 보호 없는 환경을 저절로 만들고 레포 시크릿으로 배포 성공, ② 같은 이름 시크릿을 환경에 넣자 환경 값으로 배포 성공
  (환경 시크릿이 레포 시크릿보다 앞선다), ③ 레포 시크릿을 지운 뒤에도 배포 성공. 브랜치 규칙을 켠 뒤 우회 목록의 GitHub App으로 push하면
  원격이 "Bypassed rule violations for refs/heads/…"(때로 "Cannot update this protected ref" 한 줄 뒤 통과)를 찍는다.
  공개 API `GET /repos/{o}/{r}/rules/branches/{b}`·`/rulesets/{id}`로 규칙·우회 목록·`current_user_can_bypass`를 읽어 설정을 확인할 수 있다.
  확인 못 함: 자동화 봇(사용자 권한으로 붙는 앱)이 "관리자만 우회"인 규칙을 우회하는지 — API는 우회 가능이라 답했으나 운영 갈래라 push로 시험하지 않음.
  1차 출처로 확인(2026-11-05, github/docs 원문 markdown을 curl로): Restrict updates = "우회 권한자만 그 갈래에 push할 수 있다",
  Require a pull request = "PR에 묶이기만 하면 되고 승인은 꼭 아니다", Required approvals는 0~10, "PR 작성자는 자기 PR을 승인할 수 없다"
  (reusables/repositories/request-changes-tips.md), Environment Required reviewers는 사람·팀 여섯까지·레포 읽기 권한 이상, prevent self-review를 켜면
  배포를 일으킨 사람은 승인할 수 없다.
  직접 해 봄(nail-under-the-roots PR #12, 2026-11-05): main에 Restrict updates가 켜진 채 본인이 연 PR은 "병합할 수 없음" + "요구사항을 충족하지 않고 병합"
  (우회)만 보였다 → Restrict updates를 끄고 PR 필수(승인 0) + 상태 검사 `build`로 바꾸자 우회 없이 Merge됐고, Merge 커밋의 운영 배포 잡이
  Environment 승인 대기(waiting)로 멈추는 것까지 봤다. 화면의 Merge 단추가 규칙을 바꾼 때와 Copilot 검토가 끝난 때 중 어느 쪽에서 살아났는지는 가르지 못했다.
  확인 못 함: Required reviewers 검색 칸에 레포 주인 본인이 안 나온다는 사용자 보고 — 결국 승인 대기가 걸렸으니 넣어진 것으로 보이나 어떻게 넣었는지는 모른다.
  직접 겪음(2026-11-05, 사용자 보고): 승인 대기 run 링크를 폰의 GitHub 앱으로 열면 Review deployments 단추가 안 보였고, 같은 링크를 브라우저로 열자 승인됐다.
  2차 출처만 있음: GitHub Mobile은 2021-04 changelog에서 배포 승인·거절과 알림 탭의 승인 요청을 지원한다고 했다 — 그래서 "앱에 기능이 없다"가 아니라
  "링크로 연 화면에 안 나온다"일 수 있다(알림 탭으로 들어가 보지는 않았다).
  2차 출처만 있음: 포크 PR 워크플로에 레포 시크릿이 가지 않는다(GitHub 문서의 일반 설명으로 알려진 것 — 이번에 해당 쪽 원문은 다시 읽지 않음).
sources:
  - https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
  - https://github.com/github/docs/blob/main/data/reusables/repositories/request-changes-tips.md
  - https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/review-deployments
  - https://github.blog/changelog/2021-04-01-reviewing-deployments-on-github-mobile
---

# 공개 레포에서 배포 파이프라인 지키기

## 요약
공개 레포는 누구나 보고 포크·PR을 할 수 있지만 **쓰기는 권한자만** 된다. 지켜야 할 것은 셋 — 배포 갈래에 쓰기, 배포 시크릿 읽기, 워크플로를 고쳐 시크릿 빼돌리기. 무료 플랜 공개 레포에서도 다 막힌다: **배포 시크릿은 Environment에(정한 갈래에서만 열림)**, **배포 갈래는 브랜치 규칙으로 — 바로 push하는 갈래는 우회 목록(본인 + 쓰는 봇)만, 운영 갈래는 PR(승인 0) + 빌드 검사로만**, **워크플로 파일엔 CODEOWNERS**.

## 본문
1. **배포 잡을 따로 뗀다.** 빌드·시험 잡에는 배포 시크릿을 두지 않고, 산출물을 아티팩트로 넘겨 `publish` 잡만 `environment:`에 들어간다. 갈래마다 환경을 고르려면 `environment: ${{ github.ref == 'refs/heads/main' && 'prod' || 'dev' }}`.
2. **Environment**(Settings → Environments): Deployment branches = Selected → `main`(운영)·`release/**`(개발판). 운영에는 Required reviewers(본인)를 걸면 배포마다 승인 버튼이 생긴다. 시크릿을 환경에 넣고 **레포 시크릿의 같은 이름은 지운다** — 남겨 두면 다른 갈래·PR 워크플로가 여전히 읽는다(순서: 환경에 넣기 → 한 번 배포 확인 → 레포 것 지우기).
3. **브랜치 규칙**(Rulesets): 갈래가 어떻게 바뀌는지에 따라 둘 중 하나.
   - **바로 push하는 갈래**(개발판 `release/**`): Restrict **creations**·updates·deletions·Block force pushes, 우회 목록 = Repository admin + 쓰는 GitHub App(자동화 봇). 필수 상태 검사는 걸지 않는다(검사는 push 뒤에 돈다) — 배포 잡이 빌드 잡을 `needs:`로 기다리면 빨간 커밋은 안 나간다.
     - **creations가 빠지면 환경이 뚫린다**: 환경의 Deployment branches가 `release/**` 같은 패턴이면, 그 이름으로 새 갈래를 만들 수 있는 사람은 그 갈래의 워크플로로 환경 시크릿을 읽는다. 운영과 개발에 같은 토큰을 넣었다면 운영 권한까지 — 그래서 패턴 갈래의 "만들기"를 막는 것이 이 규칙의 핵심이다.
   - **PR로만 바뀌는 갈래**(운영 `main`, 혼자 하는 레포): **Require a pull request(Required approvals = 0) + Require status checks(빌드 잡) + Restrict deletions + Block force pushes**, Restrict updates는 **끈다**. 직접 push는 PR 필수가, 빨간 빌드의 Merge는 상태 검사가, 배포는 Environment 승인(2)이 막는다. Merge할 수 있는 사람은 Write 이상뿐이라 협업자가 없으면 본인 혼자다(6).
4. **CODEOWNERS**: `/.github/ @본인` — PR이 워크플로를 고치면 본인 검토가 걸린다(규칙에서 코드 주인 검토를 켰을 때만 막는 힘이 있다).
5. **Actions 설정**: 포크 PR 워크플로는 외부 기여자 승인 필요, `GITHUB_TOKEN` 기본 권한은 읽기만(쓰기가 필요한 잡은 `permissions:`에 적는다), Actions의 PR 만들기·승인 끔.
6. 협업자에게 Write를 주지 않고 기여는 포크 PR로. 계정 2단계 인증.

## 왜?
GitHub는 **워크플로를 실행하는 갈래의 워크플로 파일**을 쓴다. 같은 레포에 push할 수 있는 사람은 자기 갈래에서 워크플로를 고쳐 레포 시크릿을 출력할 수 있다 — 레포 시크릿은 "레포에 쓸 수 있는 모든 사람의 것"이다. Environment 시크릿은 환경의 갈래 규칙을 통과한 잡만 받으니, 고친 워크플로가 다른 갈래에서 돌면 시크릿이 비어 있다. 그 갈래(main·release)에 쓰는 것 자체는 브랜치 규칙이 막는다. 둘이 같이 있어야 닫힌다.

## 함정
- **Restrict updates는 PR Merge도 막는다.** Merge도 그 갈래를 바꾸는 일이라 우회 목록 밖이면(직접 겪음) "병합할 수 없음"이 뜨고, 주인에게는 "요구사항을 충족하지 않고 병합"(우회 단추)만 남는다 — 매번 우회하면 규칙이 기록상 매번 깨진다. PR로 들이는 갈래에는 Restrict updates 대신 PR 필수를.
- **혼자 하는 레포에서 승인 1 이상을 걸면 우회 없이는 Merge하지 못한다**: PR 작성자는 자기 PR을 승인할 수 없다(GitHub 문서). 봇이 주인 계정으로 PR을 열어도 작성자는 주인이다. 승인 수는 0으로 두고, 사람의 확인은 Environment Required reviewers(배포 승인)에 건다. 이쪽도 **prevent self-review는 끈다** — 켜면 Merge한 본인이 그 배포를 승인할 수 없다.
- **승인 단추가 안 보이면 브라우저로**: 승인은 워크플로 실행(run) 첫 화면 위 노란 알림의 Review deployments에 있다 — 잡 로그 화면·PR 화면엔 없다. 폰의 GitHub 앱으로 연 링크에서는 안 보였고 브라우저에서는 됐다(앱은 알림 탭에서 승인한다고 changelog에 나온다).
- **봇이 사장 권한으로 붙으면 "관리자만 우회"가 봇도 통과시킬 수 있다.** 그래서 운영 갈래는 규칙만 믿지 말고 운영 환경에 **Required reviewers**(사람 승인)를 겹친다 — 누가 넣어도 배포는 사람이 누를 때만.
- **Dependabot의 `target-branch`가 Restrict updates 갈래면** 그 PR의 Merge도 update라 우회 단추로만 들어간다(main에서 겪은 것과 같은 원리 — 개발 갈래는 아직 직접 겪지 않음). 개발 갈래면 우회 Merge로 두거나, 운영 갈래 쪽으로 받아 PR 흐름에 태운다.
- 운영 갈래 반영을 "봇이 PR → 사람이 Merge"로 바꾸면 문서(작업 규칙)도 같이 고친다 — 안 그러면 봇이 습관대로 직접 push하려다 막힌다.
- 시크릿을 환경으로 옮기고 레포 시크릿을 지우지 않으면 아무것도 안 바뀐다.
- 하나의 잡이 PR에서도 돌고 배포도 하면 환경 갈래 규칙에 PR 실행이 막힌다 — 그래서 잡을 나눈다(PR 미리 보기 배포는 포기하거나 별도 환경).
- 아직 없는 환경 이름을 워크플로에 쓰면 첫 실행 때 보호 없는 환경이 저절로 생긴다 — 규칙은 사람이 따로 건다.
- 파일 경로로 push를 막는 push ruleset은 무료 공개 레포에 없다.
- 읽기 전용 토큰(예: 비공개 에셋 레포 읽기)이라도 레포 시크릿이면 쓰기 권한자는 읽는다 — 협업자를 들이면 그것도 환경으로.

## 관련 노트
- [공개 레포를 비공개로 바꿀 때](../reference/github-actions/public-to-private-repo.md)
- [macroquad WASM → Netlify 배포](macroquad-wasm-netlify-github-actions.md)
