---
title: Cloudflare를 정적 사이트 운영에 쓰기 — 프록시 뒤에서 무료로 되는 것과 한도
type: reference
tags: [cloudflare, hosting, analytics, dns]
status: draft
created: 2026-11-10
updated: 2026-11-10
verified: |
  1차 출처로 확인(2026-11-10, Cloudflare 공식 문서 검색):
  Web Analytics — 쿠키 없이 브라우저 비컨으로 Core Web Vitals·방문을 잰다, 프록시(주황 구름)된 사이트는 응답에 자동 주입(Free 플랜은 규칙 0개라 그 영역의 모든 하위 도메인에),
  DNS만(회색 구름)이면 손으로 스크립트, `Cache-Control: no-transform`이면 자동 주입이 안 된다, 비컨은 광고 차단기에 막힐 수 있고 엣지 통계(대시보드 Analytics)는 막히지 않는다.
  Workers/Pages 정적 파일 — 파일 하나 25 MiB, 버전당 파일 2만(Free)·10만(Paid), 정적 파일 요청은 무료·무제한, Workers Free 하루 10만 요청·CPU 10ms.
  R2 — 내려받기(egress) 요금 없음, 무료 매달 10 GB-month·Class A 100만·Class B 1,000만(Standard만), 이후 $0.015/GB-month.
  Email Sending — 아무 주소로 보내기는 Workers Paid($5/월, 3,000통 포함).
  직접 확인(2026-11-10): GitHub Pages에 붙인 루트·하위 도메인 셋이 프록시되어 응답 헤더에 `server: cloudflare`·`cf-ray`가 있다(curl -I).
  확인 못 함: GitHub Pages 원본 앞의 프록시가 Pages의 HTTPS 인증서 갱신과 충돌하는지(이번에는 문제 없었음), Web Analytics를 실제로 켠 결과.
sources:
  - https://developers.cloudflare.com/web-analytics/faq/
  - https://developers.cloudflare.com/web-analytics/limits/
  - https://developers.cloudflare.com/workers/platform/limits/
  - https://developers.cloudflare.com/pages/platform/limits/
  - https://developers.cloudflare.com/pages/functions/pricing/
  - https://developers.cloudflare.com/r2/pricing/
  - https://developers.cloudflare.com/email-service/platform/pricing/
---

# Cloudflare를 정적 사이트 운영에 쓰기

## 요약
도메인 DNS를 Cloudflare에 두고 정적 페이지(GitHub Pages·Netlify 등)를 프록시하면, 돈을 안 내고도 **엣지 통계·쿠키 없는 방문 분석·리디렉트·메일 받기**가 붙는다. 큰 파일 배포는 **R2**(내려받기 무료)가 맞고, 호스팅 자체를 Pages/Workers로 옮길 때는 **파일 하나 25 MiB** 한도부터 잰다. 분석을 켜는 것은 "무엇을 모으는가"가 바뀌는 일이라 개인정보처리방침을 먼저 고친다.

## 본문

| 기능 | 무료로 되는 것 | 한도·조건 | 맞는 쓰임 |
|---|---|---|---|
| 대시보드 Analytics(엣지) | 프록시된 요청 수·국가 | 스크립트 없음 → 차단기에 안 막힘 | 아무것도 안 해도 기본 트래픽 보기 |
| Web Analytics | 쿠키 없는 방문·페이지·Core Web Vitals | 프록시면 자동 주입(Free = 영역 전체 하위 도메인), `no-transform`이면 안 됨, 비컨은 차단기에 막힐 수 있음 | 소개 페이지 유입·속도 |
| 리디렉트 규칙 | `www` → 루트, 짧은 주소 → 상점 페이지 | — | 출시 링크 |
| Email Routing | 주소별 받기 → 내 메일함 전달 | 주소마다 규칙 + 확인된 메일함 | 연락처 메일([노트](email-routing.md)) |
| R2 | 매달 10 GB-month·읽기 1,000만 회, **내려받기 무료** | 넘으면 $0.015/GB-month | 큰 바이너리·보도자료 묶음 배포 |
| Pages / Workers 정적 파일 | 정적 요청 무료·무제한 | **파일 하나 25 MiB**, 버전당 2만 파일(Free) | 사이트 호스팅 옮기기 |
| Workers | 하루 10만 요청 | CPU 10 ms(Free) | 폼·웹훅·알림 |
| Email Sending | 내 메일함으로 보내는 알림 | 아무 주소로는 Workers Paid | 거래 메일 |

## 왜?
프록시(주황 구름)면 모든 요청이 Cloudflare 엣지를 지난다 — 그래서 원본(GitHub Pages)이 무엇이든 통계를 엣지에서 세고, HTML 응답에 비컨을 끼워 넣고(자동 주입), 규칙으로 리디렉트할 수 있다. 같은 이유로 원본이 `no-transform`을 보내면 응답을 고칠 수 없어 자동 주입이 안 된다. R2의 내려받기 무료는 같은 네트워크 안에서 나가기 때문에 가능한 가격 구조라, 많이 받아 가는 큰 파일일수록 차이가 커진다.

## 함정
- 분석을 켜면 수집 항목이 늘어난다 — 사이트에 개인정보처리방침이 있으면 **먼저** 고친다. 쿠키가 없다고 수집이 없는 것은 아니다.
- Free 플랜은 Web Analytics 규칙이 0개라 자동 주입이 **같은 영역의 모든 하위 도메인**에 들어간다(게임 웹판 하위 도메인까지). 원치 않으면 손으로 넣는 방식(manual)으로.
- 게임 웹 빌드를 Pages/Workers로 옮기기 전에 wasm·음악 같은 큰 파일이 25 MiB를 넘는지 잰다. 넘으면 그 파일만 R2로.
- 이미 Netlify 등 다른 호스트로 CI 배포를 쓰고 있으면 옮기는 것은 배포 파이프라인(시크릿·승인) 전체를 바꾸는 일이다 — 기능 하나 때문에 옮기지 않는다.

## 관련 노트
- [Cloudflare Email Routing](email-routing.md)
- [정적 WASM 호스팅](../../concepts/static-wasm-hosting.md)
- [CI에서 netlify-cli로 배포](../netlify/deploy-from-ci.md)
- [GitHub Pages에 정적 페이지](../github-actions/pages-static-site.md)
