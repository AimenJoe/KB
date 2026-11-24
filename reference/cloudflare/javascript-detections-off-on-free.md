---
title: Cloudflare 무료 플랜에서 JavaScript Detections(jsd/main.js·cf_clearance 쿠키) 끄기
type: reference
tags: [cloudflare, privacy, cookies, bots, hosting]
status: draft
created: 2026-11-24
updated: 2026-11-24
verified: |
  직접 실행(2026-11-24, Free 영역 하나): Bot Fight Mode를 대시보드에서 끈 뒤에도 프록시된 모든 HTML 응답에
  `/cdn-cgi/challenge-platform/scripts/jsd/main.js`가 주입됐다(curl로 확인). `GET /zones/{id}/bot_management`가 `fight_mode: false, enable_js: true`를 돌려줬다.
  `PUT /zones/{id}/bot_management`에 `{"fight_mode": false, "enable_js": false}`를 보내자 성공했고, 20초 뒤 다섯 호스트·경로의 HTML에서 주입이 사라졌다.
  헤드리스 Chromium으로 세 페이지를 연 뒤 쿠키가 0개였고, Turnstile(explicit render)은 그대로 떴다.
  1차 출처로 확인(Cloudflare 공식 문서, 2026-11-24): "Bot Fight Mode 고객은 JavaScript Detections가 자동으로 켜지고 끌 수 없다",
  주입은 HTML 응답에만, `cf_clearance` 쿠키에 결과를 담는다, 원본 응답에 `Cache-Control: no-transform`이 있으면 주입하지 않는다, API의 `enable_js` 필드.
  2차 출처(포럼)만 있음: Bot Fight Mode를 꺼도 주입이 남는다는 다른 사람의 보고(본문은 403으로 읽지 못함, 검색 요약만).
  확인 못 함: Bot Fight Mode를 다시 켜면 `enable_js`가 다시 켜지는지, `no-transform`을 Cloudflare 규칙으로 덧붙여도 통하는지, ePrivacy에서 이 쿠키가 "꼭 필요한 쿠키" 예외에 드는지(규제 기관의 언급 없음).
sources:
  - https://developers.cloudflare.com/cloudflare-challenges/challenge-types/javascript-detections/
  - https://developers.cloudflare.com/bots/get-started/bot-fight-mode/
  - https://developers.cloudflare.com/api/resources/bot_management/methods/update/
  - https://community.cloudflare.com/t/bot-fight-mode-off-but-javascript-detections-still-injected-and-blocked-by-our-csp/974584
---

# Cloudflare 무료 플랜에서 JavaScript Detections 끄기

## 요약
무료 플랜 대시보드에는 JavaScript Detections만 끄는 스위치가 없고, Bot Fight Mode를 꺼도 주입이 남는다. API의 `enable_js`를 `false`로 보내면 꺼진다 — 그러면 모든 페이지에 붙던 스크립트와 `cf_clearance` 쿠키가 사라져, "쿠키를 쓰지 않는다"고 말할 수 있다.

## 본문
증상: 프록시(주황 구름) 뒤의 모든 HTML 끝에 `/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray=…`가 붙고, 브라우저에 `cf_clearance` 쿠키(영역 전체, 최대 1년)가 생긴다.

```sh
# 토큰 권한: 영역 → Bot Management → 편집
curl -s "https://api.cloudflare.com/client/v4/zones/$ZONE/bot_management" -H "Authorization: Bearer $TOKEN"   # enable_js 확인
curl -s -X PUT "https://api.cloudflare.com/client/v4/zones/$ZONE/bot_management" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"fight_mode": false, "enable_js": false}'
curl -s https://example.com/ | grep -c challenge-platform    # 0이어야 한다(수십 초 뒤)
```

확인은 curl의 문자열 세기 + 실제 브라우저의 쿠키 목록 둘 다로 한다. 문의 양식의 Turnstile은 별개라 그대로 돈다.

다른 길: 원본이 `Cache-Control: no-transform`을 보내면 그 응답에는 주입하지 않는다(문서). Workers 정적 파일은 `_headers`로 넣을 수 있지만 GitHub Pages 원본은 헤더를 못 바꾼다.

## 왜?
Bot Fight Mode는 켜는 순간 영역 설정의 `enable_js`를 같이 켜는데, 대시보드에서 Bot Fight Mode를 꺼도 그 값은 되돌리지 않는다(관찰). 유료 플랜(Super Bot Fight Mode)에는 그 값의 스위치가 있고 무료에는 없어서, 무료에서는 API가 유일한 손잡이다. 끌 이유는 개인정보 처리방침이다 — 광고·분석을 안 해도 이 쿠키 하나 때문에 쿠키 고지·거부 방법(한국 법 제30조제1항제7호)과 유럽 ePrivacy의 동의 예외를 따져야 한다.

## 함정
- 대시보드의 "Bot Fight Mode 꺼짐"만 보고 꺼졌다고 믿지 않는다 — HTML을 받아 본다.
- Bot Fight Mode를 다시 켜면 주입도 돌아온다고 보고(문서: 켜진 동안은 끌 수 없다) 방침의 쿠키 문장을 같이 되돌린다.
- 봇 방어가 하나 줄어든다. 양식은 Turnstile·전송 제한으로 따로 막는다.

## 관련 노트
- [Cloudflare를 정적 사이트 운영에 쓰기](static-site-extras.md)
- [Worker로 사이트 점검기](../../guides/cloudflare-worker-site-watchdog.md)
