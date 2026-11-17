---
title: Netlify 무료판의 한도 — 옛 요금제(Legacy)와 크레딧제, Cloudflare Pages와 비교
type: reference
tags: [netlify, cloudflare, hosting]
status: verified
created: 2026-11-10
updated: 2026-11-10
verified: |
  1차 출처로 확인(2026-11-10, 라이브 문서를 받아 읽음):
  Netlify "Credit-based pricing plans"(최종 수정 2026-10-30) — Free = 월 300크레딧·hard limit·자동 충전 없음, Web Bandwidth 1 GB = 20크레딧,
  Web Requests 1만 = 2크레딧, Production deploy 1회 = 15크레딧. "How credits work" — 2025-09-04 이전에 만든 Free·Starter·Pro 계정은 Legacy 요금제(그대로 둘 수 있음),
  크레딧제로 바꾸면 되돌릴 수 없다, 크레딧을 다 쓰면 모든 사이트가 멈추고 "Site not available", Deploy Previews·branch deploys = 0크레딧.
  "Legacy pricing plans" — Free: 대역폭 월 100 GB(hard limit), 빌드 300분(hard limit).
  Cloudflare(같은 날, 라이브 문서): Pages 정적 파일 요청은 무료·무제한, 파일 하나 25 MiB, 사이트당 2만 파일(Free). Pages 첫 쪽(2026-08-25)은 "새 프로젝트는 Workers로 시작"을 권한다.
  Workers Static Assets "Billing and Limitations"(2026-11-03) — 정적 파일 요청 무료·무제한, 저장 비용 없음, Range 요청에도 206이 아니라 200 + 파일 전체.
  Pages Direct Upload(2026-09-18) — CI에서 `wrangler pages deploy <폴더>`로 지은 폴더를 올린다. 자세한 것은 [정적 사이트 운영](../cloudflare/static-site-extras.md) 노트.
  직접 확인(2026-11-10): Netlify 팀 API의 플랜 이름은 Legacy·크레딧제 모두 "Free"로 보여 둘을 가를 수 없었다(대시보드 Billing에서 본다).
  게임 웹 빌드의 가장 큰 파일 = wasm 2.9 MB(2D)·4.4 MB(3D, 에셋을 바이너리에 넣음), 음악 한 곡 ≤ 2.6 MB — 25 MiB 한도와 거리가 멀다(운영 사이트 HEAD).
  확인 못 함: CLI 별칭 배포(`--alias`)가 크레딧 표의 "branch deploy"로 세어지는지(문서는 Deploy Previews·branch deploys만 명시), Pages 무료판의 월 빌드 수 한도(직접 업로드는 해당 없음으로 봄 — 이번에 읽지 않음).
sources:
  - https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/
  - https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/
  - https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-legacy-plans/legacy-pricing-plans/
  - https://developers.cloudflare.com/pages/platform/limits/
  - https://developers.cloudflare.com/pages/functions/pricing/
---

# Netlify 무료판의 한도 — Legacy와 크레딧제

## 요약
Netlify 무료판은 **계정을 언제 만들었나**로 둘로 갈린다. 2025-09-04 전 계정은 Legacy(대역폭 월 100 GB에서 멈춤), 그 뒤 계정이나 바꾼 계정은 크레딧제(월 300크레딧 — 대역폭만 쓰면 ≈ 15 GB, 운영 배포 1회 15크레딧, 다 쓰면 **모든 사이트가 멈춤**). 정적 게임 웹판처럼 첫 방문에 수 MB~수십 MB를 받는 사이트는 크레딧제에서 빨리 닿는다. Cloudflare(Workers 정적 파일 — 지금 Cloudflare가 새 프로젝트에 권하는 것, 또는 Pages)는 정적 요청이 무료·무제한이라 갑자기 몰리는 트래픽에 안전하지만 파일 하나 25 MiB 한도가 있다.

## 본문

| | Netlify Free — Legacy | Netlify Free — 크레딧제 | Cloudflare Workers 정적 파일 / Pages (Free) |
|---|---|---|---|
| 해당 | 2025-09-04 전 계정(그대로 두면) | 그 뒤 계정, 또는 바꾼 계정(되돌릴 수 없음) | — |
| 대역폭 | 월 100 GB, 넘으면 멈춤 | 1 GB = 20크레딧 → 다른 것 안 쓰면 ≈ 15 GB | 정적 요청 무료·무제한 |
| 요청 | — | 1만 = 2크레딧 | 무료 |
| 운영 배포 | CLI 업로드는 빌드 분 안 씀 | 1회 15크레딧(월 20회면 다 씀) | 제한 없음 |
| 미리 보기·갈래 배포 | — | 0크레딧 | 무료 |
| 한도 도달 | 멈춤 | 모든 사이트 "Site not available" | — |
| 파일 하나 | 제한 없음 | 제한 없음 | 25 MiB(넘는 것은 R2) |

### 셈해 보기
- 크레딧제: 300 − (운영 배포 n × 15) 남은 크레딧 ÷ 20 = 월 GB. 운영 배포 6번이면 210크레딧 ≈ 10.5 GB.
- 게임 한 번 첫 방문 = wasm + 처음 받는 그림·소리. 10 MB로 잡으면 Legacy 100 GB ≈ 1만 방문, 크레딧제 ≈ 1천 방문.

## 왜?
크레딧제는 "기능을 쓴 만큼" 한 통화로 세는 구조라, 함수·AI를 안 쓰는 정적 사이트에게는 대역폭과 배포가 그대로 크레딧이 된다. Legacy는 대역폭 한 줄만 보던 옛 구조라 정적 사이트에 후하다. Cloudflare는 정적 파일을 같은 CDN에서 내보내는 것을 돈을 받는 대상으로 두지 않고 함수(Workers) 호출만 센다 — 그래서 정적 게임은 트래픽이 커져도 비용·멈춤이 없다.

## 함정
- 팀 API·화면의 플랜 이름은 둘 다 "Free"로 보일 수 있다 — Legacy인지는 대시보드 **Billing**에서 본다.
- Legacy에서 크레딧제로 바꾸는 단추는 되돌릴 수 없다. 정적 사이트면 바꿀 이유가 거의 없다.
- 무료판 한도에 닿으면 **팀의 모든 사이트**가 함께 내려간다(크레딧제) — 게임 둘을 한 팀에 두면 하나가 몰려도 둘 다 멈춘다.
- 출시·홍보로 트래픽이 갑자기 오를 때가 위험하다. 그 전에 한도를 확인하거나 옮긴다.
- Cloudflare로 옮길 때는 파일 하나 25 MiB를 먼저 잰다. 넘는 파일(긴 음악·영상)은 R2.
- 새로 옮긴다면 Pages보다 **Workers 정적 파일**이 Cloudflare의 권장이다(Pages 문서 첫 쪽). 정적 파일 요청은 둘 다 무료.
- Workers 정적 파일은 Range 요청에도 파일 전체(200)를 준다 — 잘라 받는 클라이언트(Safari 영상 재생 등)가 있으면 그 경로만 Worker로 처리해야 한다.

## 관련 노트
- [CI에서 netlify-cli로 배포](deploy-from-ci.md)
- [Cloudflare를 정적 사이트 운영에 쓰기](../cloudflare/static-site-extras.md)
- [정적 WASM 호스팅](../../concepts/static-wasm-hosting.md)
- [0001 빌드는 CI에서, 호스팅은 CLI 업로드로](../../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md)
