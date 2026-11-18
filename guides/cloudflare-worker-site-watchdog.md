---
title: Cloudflare Worker로 내 사이트 점검기와 GitHub API 캐시 만들기(무료판)
type: guide
tags: [cloudflare, ci, github-actions, hosting]
status: draft
created: 2026-11-18
updated: 2026-11-19
verified: |
  1차 출처로 확인(2026-11-18, Cloudflare·GitHub 라이브 문서를 받아 읽음):
  Email Sending Workers API(최종 수정 2026-11-17) — `env.EMAIL.send({ from, to, subject, text })`, 바인딩 `send_email`(제한 속성 `destination_address`·`allowed_destination_addresses`·`allowed_sender_addresses`,
  제한이 없으면 보내기 도메인을 등록하기 전엔 확인된 destination으로만), 확인된 내 destination으로 보내기는 모든 플랜 무료([Email Routing 노트](../reference/cloudflare/email-routing.md)).
  Cron Triggers(2026-11-12) — `scheduled(controller, env, ctx)`, UTC, 무료판 계정당 5개(Workers limits 2026-10-29). Custom Domains(2026-11-12) — `routes: [{ pattern, custom_domain: true }]`.
  Cache API(2026-10-29) — `caches.default`, `cache.put`/`match`에는 `stale-while-revalidate`·`stale-if-error`가 듣지 않는다(그래서 "마지막 값" 키를 따로 둔다).
  wrangler commands — `secret bulk <JSON>`, `deploy --dry-run --outdir`. GitHub 문서 — 익명 REST 한도는 IP당 시간 60회.
  직접 해 봄(2026-11-18, beardworks-ops): Node 22 `node --test` 18 통과, 실제 사이트·GitHub로 점검 22건 정상, wrangler 4.156.2 `deploy --dry-run`(13.8 KiB),
  `wrangler dev --test-scheduled`(workerd)에서 fetch 경로·cron·메일 바인딩 호출까지 확인. 클라우드 출구 IP에서 익명 GitHub API가 `API rate limit exceeded`(남은 횟수 0)로 막혔다.
  직접 겪음(2026-11-19): 점검 Worker에 와일드카드 route(`*.beardworks.io/*` 꼴, 언제 생겼는지 모름)가 걸려 같은 영역의 하위 도메인 페이지 전체가 그 Worker의 404가 됐는데,
  점검은 정상이라고 했다. 까닭은 1차 출처로 확인(2026-11-19): Workers Routing — "Routes cannot be the target of a same-zone fetch() call", 같은 영역의 fetch는 route의 Worker를 건너뛰고
  원본으로 간다(Custom Domain은 예외). Compatibility flags — `global_fetch_strictly_public`을 켜면 "requests to a Worker's own zone will loop back to the front door … treated like a request from the Internet".
  직접 해 봄(2026-11-19): 플래그 없이 점검이 nail `/play/`(Worker `web-game`의 route)를 GitHub Pages에서 찾아 404·503, 플래그를 켠 뒤 23건 중 그 오류 0.
  Workers 정적 파일은 HEAD 응답에 `content-length`가 없다(curl -I, 2026-11-19) — "크기 0"으로 잘못 알렸다.
  확인 못 함: 실제 배포 뒤 메일 도착·Custom Domain 인증서 시간, `secret bulk`가 배포 전 Worker에도 되는지(그래서 배포 뒤에 넣는다).
sources:
  - https://developers.cloudflare.com/email-service/api/send-emails/workers-api/
  - https://developers.cloudflare.com/email-service/configuration/send-bindings/
  - https://developers.cloudflare.com/workers/configuration/cron-triggers/
  - https://developers.cloudflare.com/workers/configuration/routing/custom-domains/
  - https://developers.cloudflare.com/workers/runtime-apis/cache/
  - https://developers.cloudflare.com/workers/wrangler/commands/workers/
  - https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
---

# Cloudflare Worker로 사이트 점검기 + GitHub API 캐시

## 요약
1인 개발로 사이트·게임 웹판이 여럿이면 "조용히 깨진 것"(배포 안 된 커밋, 빠진 에셋, 승인 잊은 운영 배포)을 아무도 모른다. Worker 하나에 **Cron 점검 + 나에게 메일**을 붙이면 무료판 안에서 매일 아침 잡힌다. 같은 Worker에 **GitHub Releases 캐시**를 두면 정적 페이지가 브라우저에서 GitHub API를 직접 부르다 익명 한도에 막히는 것도 없앤다.

## 본문

### 점검기
1. 무엇을 볼지는 표 한 곳(`config.js`): 페이지 목록, 게임 웹판(운영·개발 주소), 반드시 실려야 할 파일.
2. 배포 확인은 **"배포된 커밋 = 갈래 머리"**: 빌드 때 `build.txt`(커밋 SHA + 판)를 같이 올리고, 점검기가 GitHub 갈래 머리와 비교.
   - 다르면 머리 커밋이 **몇 시간 지났을 때만** 알린다(배포·승인 대기 중일 수 있다). 마지막 배포 워크플로 상태(실패·waiting)를 같이 적으면 "운영 배포 승인을 잊음"이 바로 보인다.
   - 개발판 갈래(`release/vX`)는 이름을 박지 말고 **가장 높은 판을 찾는다** — 마일스톤이 바뀌어도 고칠 것이 없다(숫자로 비교: `v0.10` > `v0.9`).
3. 반드시 실려야 할 파일(비공개 에셋 등)은 **HEAD + 크기 > 0**. 빌드의 "시크릿이 있나" 검사는 파일이 실제로 있는지는 못 본다.
4. 메일: 문제가 있을 때만 + **매주 하루는 이상 없어도 "살아 있음"** — 점검기 자체가 죽은 것을 알려면.
5. 받는 주소는 레포가 아니라 Worker 비밀 값(`ALERT_TO`). `destination_address`를 설정 파일에 쓰면 공개 레포에 메일 주소가 남는다.

### GitHub API 캐시
- `/releases/<repo>`(허용 목록만) → GitHub를 **토큰으로** 부르고 짧게(10분) 캐시, 실패하면 **마지막 값 키**(길게, 7일)를 내준다. `cache.put`/`match`는 `stale-if-error`를 안 들으니 키를 둘로.
- 페이지는 캐시 → GitHub 직접 → HTML에 적어 둔 값 차례로 — 캐시가 죽어도 나빠지지 않는다.
- 공개 데이터면 CORS `*`. 응답은 원래 꼴 그대로(쓰는 칸만 남김)라 페이지 코드는 주소만 바꾼다.

### 시험과 배포
- 의존성 없이 `node --test`: fetch·cache·GitHub를 주입(가짜)해서 hit/miss/stale/502, 배포 비교·대기, 메일 조건을 시험.
- **실제 대상에 한 번 돌리는 도구**(메일은 안 보냄)로 설정이 현실과 맞는지 본다 — 가짜만으로는 주소·경로 오타를 못 잡는다.
- `wrangler dev --test-scheduled` + `curl "localhost:8787/__scheduled?cron=…"`로 workerd에서 cron까지.
- CI: 시험 → `wrangler deploy` → `wrangler secret bulk`(배포 뒤) → `/health`. 시크릿은 Environment(배포 갈래만)에.

## 왜?
- 점검을 사람이 하면 "배포가 끝났겠지"로 넘어간다. 실패는 조용하다: 에셋이 빠진 빌드도, 승인 대기에 걸린 배포도 CI는 초록이거나 노랑이다. 결과물(사이트가 실제로 내주는 것)을 밖에서 보는 것만이 그것을 잡는다.
- GitHub 익명 한도는 **IP**에 붙는다. 방문자 브라우저든 클라우드 함수든, 그 IP를 나눠 쓰는 누군가가 이미 다 써 버렸을 수 있다 — 그래서 서버 쪽에서 토큰으로, 캐시해서 부른다.

## 함정
- 클라우드(Workers 포함)의 출구 IP에서 익명 GitHub API는 처음부터 막혀 있을 수 있다 — 토큰 없이 "되겠지" 하지 않는다.
- Cron은 UTC. 한국 아침 7시 = 전날 22시 UTC. 요일 판단도 한국 시간으로 바꿔서.
- 메일을 "매일 보고"로 만들면 읽지 않게 된다 — 문제 + 주간 살아 있음만.
- 점검 대상 갈래 이름을 박아 두면 마일스톤이 바뀔 때 조용히 옛 갈래를 본다.
- 무료판 Cron은 계정당 5개 — 점검을 Worker마다 따로 만들지 말고 하나에 모은다.
- **점검 Worker가 같은 영역의 페이지를 부르면 "밖에서 보이는 것"과 다르다 — `compatibility_flags: ["global_fetch_strictly_public"]`을 켠다.** 기본은 같은 영역(같은 도메인 아래)으로의 `fetch()`가 다른 Worker의 **route**를 건너뛰고 원본으로 간다. 그래서 다른 Worker가 route로 내는 경로(예: `/play/`)는 404로 보이고, 반대로 와일드카드 route가 하위 도메인 전체를 가로챘을 때(방문자는 404) 점검은 원본(GitHub Pages)을 받아 정상이라고 했다. 플래그를 켜면 점검 요청이 인터넷에서 온 것처럼 정문으로 들어가 방문자와 같은 것을 본다(보안 설정·봇 차단도 그대로 받는다 — Bot Fight Mode가 켜져 있으면 막힐 수 있다). Worker에 route를 손으로 더하지 말고(설정 파일에 있는 것만 — wrangler는 대시보드에서 더한 route를 지워 주지 않는다), 영역의 **Workers Routes** 목록을 때때로 본다. 중요한 페이지는 다른 출처(예: CI 러너)에서도 한 번 본다.
- 파일 크기를 HEAD의 `content-length`로 보면 Cloudflare Workers 정적 파일에서는 늘 0이다(헤더를 안 준다) — 길이가 없으면 GET으로 받아 잰다.

## 관련 노트
- [Cloudflare Email Routing](../reference/cloudflare/email-routing.md)
- [Cloudflare를 정적 사이트 운영에 쓰기](../reference/cloudflare/static-site-extras.md)
- [운영판과 개발판을 갈라 내보내기](dev-and-release-flavors.md)
- [공개 레포에서 배포 파이프라인 지키기](protect-deploy-pipeline-in-public-repo.md)
