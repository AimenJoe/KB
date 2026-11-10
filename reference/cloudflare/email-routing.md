---
title: Cloudflare Email Routing — 도메인 메일 받기와 "550 5.1.1 Address does not exist"
type: reference
tags: [cloudflare, email, dns]
status: verified
created: 2026-11-10
updated: 2026-11-10
verified: |
  1차 출처로 확인(2026-11-10, Cloudflare 공식 문서 — 검색 색인으로 찾고 라이브 페이지 `…/index.md`를 받아 아래 숫자·문장을 대조함.
  페이지 최종 수정: email-lifecycle 2026-09-16, email-routing-addresses 2026-10-15, pricing 2026-06-09, send-emails 2026-06-25, Email Service 첫 쪽 2026-10-15): 받은 메일의 처리 순서(SMTP 받기 → SPF·DKIM·DMARC·ARC 검사 → 받는 주소를 라우팅 규칙과 맞춤,
  맞는 규칙이 없으면 catch-all이 켜져 있을 때만 적용 → 동작: 메일로 전달·Worker·버림), 전달은 확인된 destination address로만 가고
  확인 전에는 그 주소를 가리키는 규칙이 꺼져 있다, Email Routing(받기)은 Workers Free·Paid 둘 다 무제한,
  Email Sending(보내기)은 2026-04-16 공개 베타 — 아무 주소로 보내려면 Workers Paid(월 3,000통 포함, 이후 1,000통당 $0.35),
  확인된 내 destination으로 보내는 것은 모든 플랜에서 무료·할당량 밖, Email Service는 Cloudflare DNS를 써야 한다.
  직접 겪음(2026-11-10, beardworks.io): MX(route1~3.mx.cloudflare.net)·SPF(include:_spf.mx.cloudflare.net)·DMARC가 다 있는데도
  support@로 보낸 메일이 `550 5.1.1 Address does not exist (in reply to RCPT TO)`로 반송 → Custom address 규칙(support@·business@ → 확인된 메일함)을
  만든 뒤 같은 테스트가 도착. DNS는 dns.google DoH로 조회했다.
  확인 못 함: 같은 메일함에서 보내 같은 메일함으로 전달될 때 받은편지함에 안 보일 수 있다는 것(일반적으로 알려진 현상 — 이번에 재현하지 않음).
sources:
  - https://developers.cloudflare.com/email-service/concepts/email-lifecycle/
  - https://developers.cloudflare.com/email-service/configuration/email-routing-addresses/
  - https://developers.cloudflare.com/email-service/platform/pricing/
  - https://developers.cloudflare.com/email-service/get-started/send-emails/
---

# Cloudflare Email Routing — 도메인 메일 받기

## 요약
Cloudflare에 DNS를 둔 도메인은 메일함 없이 `이름@도메인`을 **받아서 내 메일함으로 전달**할 수 있다(무료). DNS 레코드(MX·SPF)만 있다고 끝이 아니다: **주소마다 라우팅 규칙**(또는 catch-all)과 **확인된 받을 메일함**이 있어야 한다. 둘 중 하나라도 없으면 보내는 쪽은 `550 5.1.1 Address does not exist`를 받는다. 보내기(그 주소 이름으로 발송)는 별개 기능이다.

## 본문

### 설정 순서(대시보드 → 도메인 → Email Routing)
1. Email Routing을 켜면 MX 셋(`route1~3.mx.cloudflare.net`)과 SPF(`v=spf1 include:_spf.mx.cloudflare.net ~all`) TXT가 들어간다.
2. **Destination addresses**에 실제 메일함을 넣고, 그 메일함에 온 확인 메일의 링크를 누른다. 확인 전에는 그 주소를 가리키는 규칙이 꺼져 있다.
3. **Routing rules → Custom addresses**에 받을 주소마다 한 줄(`support@` → 메일함). 페이지·개인정보처리방침에 적은 주소는 **전부** 만든다.
4. (선택) **Catch-all**: 규칙에 없는 주소를 한 메일함으로(스팸도 같이 온다) 또는 버림.

### 받은 메일이 처리되는 차례
SMTP 받기 → SPF·DKIM·DMARC·ARC 검사(DMARC 정책상 실패면 거절) → 받는 주소를 규칙과 맞춤 → 없으면 catch-all(켜져 있을 때만) → 동작(메일로 전달·Worker·버림) → 전달은 ARC 서명 + SRS로 봉투 발신자를 바꿔 보낸다.

### 반송 문구 읽기
| 반송 | 뜻 | 할 일 |
|---|---|---|
| `550 5.1.1 Address does not exist` (RCPT TO 단계) | 그 주소에 맞는 규칙이 없고 catch-all도 없음 | Custom address 추가 또는 catch-all |
| DMARC·SPF 관련 거절 | 보내는 쪽 인증 실패 | 보내는 도메인 설정 문제(받는 쪽 아님) |

RCPT TO 단계 거절은 본문을 보기도 전이라 인증·스팸 문제가 아니라 **주소 문제**다.

### 보내기는 따로
- Email Routing은 받기만 한다. 그 주소 이름으로 답장하려면 보낼 SMTP가 따로 있어야 한다.
- Cloudflare Email Sending(2026-04 공개 베타)은 Workers 바인딩·REST API·SMTP로 보낸다. 아무 주소로 보내려면 Workers Paid(월 3,000통 포함), **확인된 내 destination으로 보내는 알림은 무료**라 "사이트 → 나에게 알림" 용도는 무료 플랜으로 된다.

## 왜?
MX는 "이 도메인의 메일은 Cloudflare가 받는다"까지만 말한다. Cloudflare는 메일함을 주지 않고 **전달만** 하므로, 어느 주소를 어디로 보낼지 모르는 메일은 받을 곳이 없다 — 그래서 받는 서버가 RCPT 단계에서 "없는 주소"로 거절한다(받아 놓고 버리는 것보다 보낸 사람에게 즉시 알린다). 받을 메일함을 확인 메일로 묶는 것은 남의 주소로 메일을 퍼붓는 데 쓰이지 않게 하려는 것.

## 함정
- DNS(MX·SPF·DMARC)가 다 초록이어도 **규칙이 없으면 반송**된다 — DNS 조회로는 규칙 유무를 알 수 없다. 테스트 메일을 실제로 보내 본다.
- 공개 문서(개인정보처리방침·상점 브랜드 설정·연락처)에 적은 주소를 하나라도 빼먹으면 그 주소만 반송된다. 주소 목록과 규칙 목록을 맞춘다.
- 받을 메일함과 같은 주소에서 테스트하면 결과가 헷갈릴 수 있다 — 다른 메일함에서 보낸다(확인 못 함, 위 verified).
- 받기를 켰다고 그 이름으로 보낼 수 있는 게 아니다(보내기는 별도 SMTP 또는 Email Sending).

## 관련 노트
- [Cloudflare를 정적 사이트 운영에 쓰기](static-site-extras.md)
- [GitHub Pages에 정적 페이지](../github-actions/pages-static-site.md)
