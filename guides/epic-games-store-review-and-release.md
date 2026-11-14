---
title: Epic Games Store 검토 통과와 출시 — 반려 사유별 고치기, Dev → Stage → Live, "출시 예정"과 판매
type: guide
tags: [gamedev, epic, release, business, localization]
status: draft
created: 2026-11-14
updated: 2026-11-14
verified: |
  1차 출처로 확인:
  - 실제 검토 반려 글 두 번(Naïl: Under the Roots, 2026-11-11·11-13 — Epic 검토팀이 보낸 원문): 법적 정보 푸터 영어로만, 지원 링크에 GitHub 금지(지원 이메일이 있으면 비워도 됨),
    EAS를 쓰면 로그인 요건에 Epic ID(정해진 출시일 전에는 막지 않음), 캐러셀 그림의 영어 아닌 글, 상품 주소(slug)는 상품 이름과 맞아야 하고 바꾸는 것은 파트너 지원만,
    EAS 어플리케이션을 오퍼 Artifact Settings → EAS Integration에 연결, 업적은 따로 Push To Live, 새 계정으로 로그인·업적 확인.
  - EAS 브랜드 검토 반려(2026-11-13, 사유 "개인정보처리방침에서는 에픽의 정책에 대해 설명합니다")와 Brand Review Intro 원문(사용자가 붙여 준 한국어판): 평가 기준 목록.
  - 포털 화면(사용자가 직접 봄, 2026-11-11~14): 반려 뒤 Live로 보내기 버튼이 꺼져 있음, EAS 어플리케이션 카드(브랜드 설정 퍼블리싱됨·권한·연동된 클라이언트), Push to Live 뒤에도 상점이 "출시 예정"으로 보임.
  공식 문서의 검색 요약으로만 확인(dev.epicgames.com 직접 접속은 세션 네트워크에서 막힘): Release Management(반려 뒤 Dev에서 고쳐 Stage → 다시 검토,
    Queued for Review 동안 Stage로 못 보냄), Release Your Product(승인 + Stage가 Ready for Live여야 Push to Live, 미래 게시 시각이면 그때까지 안 보임),
    Publish Your Product Page(날짜를 모르면 "Coming Soon"), Recent Updates(지난 예상 날짜는 지워지고 Coming Soon으로 — 정해진 날짜를 넣고 다시 검토).
  2차 출처(포럼)만 있음: slug 끝 꼬리(-e118b5 같은 것)는 자동으로 붙고 지울 수 없다(Epic 직원, 2022 — 지금도 그런지 모름), 이름 부분만 바꿔 달라는 요청 사례,
    비공개 토론 답이 며칠~일주일 걸린 사례, 예상 날짜로 승인받아 Live로 보내면 Coming Soon 페이지가 된 사례.
  확인 못 함: slug 변경 요청의 실제 결과(답 대기 중), 이미지와 상품 이름 불일치가 반려 사유가 되는지, 꼬리 없는 주소가 넘겨주기인지 별칭인지.
sources:
  - https://dev.epicgames.com/docs/epic-games-store/requirements-guidelines/content-ratings/content-guidelines
  - https://dev.epicgames.com/docs/epic-games-store/publishing-tools/store-presence/store-config
  - https://dev.epicgames.com/docs/epic-games-store/publishing-tools/publishing-process/release-management
  - https://dev.epicgames.com/docs/epic-games-store/get-started/get-started-steps/release-your-product
  - https://dev.epicgames.com/docs/epic-games-store/get-started/get-started-steps/publish-your-product-page
  - https://dev.epicgames.com/docs/epic-games-store/whats-new/recent-updates
  - https://dev.epicgames.com/docs/epic-games-store/publishing-tools/store-presence/manage-offers
  - https://dev.epicgames.com/docs/epic-games-store/services/epic-achievements/achievements-setup
  - https://dev.epicgames.com/docs/epic-online-services/accounts-and-social/eos-epic-account-services/brand-review/brand-review-intro
  - https://dev.epicgames.com/docs/epic-account-services/brand-review/domain-verification
  - https://forums.unrealengine.com/t/incorrect-store-page-url-aka-slug/791829
  - https://forums.unrealengine.com/t/egs-product-url-change-request/2837423
  - https://forums.unrealengine.com/t/why-isnt-my-game-pursable-in-egs-when-it-says-released-still-says-coming-soon/2530454
---

# Epic Games Store 검토 통과와 출시

## 요약
Epic 검토는 **영어로 읽히는가·링크가 우리 사이트인가·이름이 어디서나 같은가·EAS가 끝났는가**를 본다. 반려되면 Dev 샌드박스에서 고쳐 Stage로 올리고 다시 검토를 받는다(Live 버튼은 승인 전엔 꺼져 있다). 승인 뒤 Live로 보내도 오퍼에 **정해진 출시일**이 없으면 상점은 "출시 예정(Coming Soon)"으로만 뜬다. 상품 주소(slug)는 처음 이름으로 굳어 직접 못 바꾸니, 상품을 만들 때 최종 이름으로 만든다.

## 반려 사유와 고치기 (실제 받은 것)
| 반려 | 고치기 | 왜 |
|---|---|---|
| 법적 정보 푸터가 영어로 안 읽힘 | 푸터는 영어만. 한글 상호 `(털보네공업사)` 하나로도 걸렸다 | 출판 도구가 영어로 읽히지 않는 상품 페이지를 받지 않는다(Localization policies). 다른 언어는 현지화 메뉴에 |
| 캐러셀 그림에 영어 아닌 글 | **게임 화면을 영어로 다시 찍는다**(HUD·보스 이름·알림까지). 다른 언어 스크린숏은 그 언어 현지화 페이지에만 | 영어를 지원 언어로 적었으면 기본 페이지는 영어로 읽혀야 한다 |
| 지원 페이지가 GitHub | 지원 링크를 **비운다**(지원 이메일이 있으면 허용) 또는 우리 게임 사이트 안의 지원·연락처 페이지 | 제3자 저장소 사이트 링크 금지(Linked-to content). 링크 하나 때문에 서버(Worker 등)를 새로 둘 필요는 없다 |
| 로그인 요건에 Epic ID 없음 | Store Settings → Product Details → Login Requirements에 **Epic ID** | EAS(Epic 계정 로그인)를 쓰면 손님에게 계정이 필요하다고 알려야 한다. 정해진 출시일 전에는 막지 않는다 |
| 상품 주소가 상품 이름과 다름 | eoshelp에서 **비공개 토론(Create Private Discussion)**, 주제 Epic Games Store, 상품 이름·ID와 원하는 이름 부분을 적는다(꼬리는 Epic에 맡김) | slug는 상품을 만들 때의 이름으로 정해지고 이름을 바꿔도 안 따라온다. 포털에 고치는 칸이 없다 |
| EAS 미확인·클라이언트 없음 | 아래 "EAS" 순서 | 확인 전엔 조직 구성원만 로그인 — 손님은 업적을 못 연다 |
| 업적이 Dev에만 있음 | Epic Online Services → Player & Game Data → Achievements → Epic Games Store 탭 → Stage 배포 → **Push To Live** | 업적은 상품 출시 흐름과 따로 Live로 보낸다 |
| (같은 검토) 새 계정으로 확인 | 조직에 속하지 않은 Epic 계정으로 로그인·업적 하나 열기 | 조직 계정은 미확인 앱도 로그인되어 문제를 못 본다 |

## EAS(Epic Account Services)
어플리케이션 = 상품 하나의 EAS 설정 묶음: **브랜드 설정**(이름·로고·웹사이트·개인정보처리방침, 로그인 동의 창에 보인다) + **권한**(Basic Profile) + **연동된 클라이언트**(게임 빌드에 넣은 클라이언트). 브랜드 검토는 브랜드 설정만 본다.
1. 조직 설정 → Domains에 **최상위 도메인**(`example.io`, www 없이) → DNS TXT → 확인. 최상위가 승인되면 하위 도메인도 승인.
2. 브랜드 설정: 이름은 **게임 이름**(회사는 조직 이름으로 따로 보인다), 웹사이트는 확인한 도메인과 **같은 꼴**, 개인정보처리방침은 영어판 직접 URL.
3. 권한 Basic Profile, 연동 클라이언트 → 브랜드 검토 제출.
4. 승인되면 **오퍼 → Artifact Settings → EAS Integration**에서 그 어플리케이션을 고른다(빼먹기 쉽다).

평가 기준(Brand Review Intro): 웹사이트는 공개·**조직 이름 + 상품 이름과 개요**·PEGI 12 이하. 개인정보처리방침은 직접 URL·공개·데이터 보호 연락처·무엇을 누구와·보관과 열람·삭제 방법, 그리고 **Epic이 하는 일과 하지 않는 일을 주장하지 않는다** — "Epic이 계정 식별자를 처리한다"·"처리 주체: Epic"으로 반려됐다. 게임이 하는 일(무엇을 받아 어디에 두는지)만 적고 Epic 계정은 Epic 방침 링크로.

## 출시 흐름
1. 고치는 곳은 늘 **Dev 샌드박스**.
2. Release Management → **Push to Stage** → Stage에서 **Submit for Review**(2일 이상). 검토 대기(Queued for Review) 중엔 Stage로 못 보낸다.
3. 승인되고 Stage의 설정·오퍼·페이지·빌드가 Ready for Live면 **Push to Live**가 켜진다. 반려 상태에선 꺼져 있는 게 정상.
4. Live로 보내도 **Offers → Offer Dates**가 날짜 모름·예상 날짜면 상점은 "출시 예정"(찜하기만). 예상 날짜는 빌드 없이도 승인되어 페이지 먼저 열기에 쓴다. 팔려면 **정해진 날짜**를 넣고 다시 검토 → Live. 미래 시각으로 Live에 보내면 그 시각까지 안 보인다. 지난 예상 날짜는 지워져 Coming Soon으로 돌아간다.

## 왜?
Epic 검토는 상품이 아니라 **손님이 보는 겉면**을 본다: 영어로 읽히는가(기본 언어), 링크가 퍼블리셔 자신의 것인가(피싱·제3자 파일 방지), 이름·주소·브랜드가 같은 정체를 가리키는가(사칭 방지), 계정 정보를 누가 책임지는가(Epic 몫은 Epic 방침이 진다). 반려 사유 하나하나가 이 넷 중 하나로 읽히면, 다음 게임에선 제출 전에 미리 고칠 수 있다.

## 함정
- **상품을 임시 이름으로 만들지 않는다.** slug가 그 이름으로 굳고, 고치려면 지원 케이스(답이 며칠~일주일)를 기다려야 한다. 포털 이름 칸이 `ï` 같은 글자를 안 받으면 처음부터 `Nail Under the Roots`처럼 최종 이름의 영문으로.
- 반려 하나 고칠 때마다 제출하면 왕복이 길다 — 위 표를 제출 전 점검표로 한 번에.
- 스크린숏을 공식 페이지(자국어)와 같이 쓰지 않는다. 상점용은 영어 화면으로 따로 찍는 스크립트를 둔다.
- 개인정보처리방침에 상점이 하는 일을 친절하게 설명하면 오히려 반려된다(Steam 줄도 같은 꼴로 고쳐 두면 다음 상점에서 덜 걸린다).
- 빌드에 박힌 클라이언트 아이디가 EAS에 연동한 클라이언트와 다르면 손님 로그인이 실패한다 — 클라이언트를 바꿨으면 빌드를 다시 올린다.
- 비공개 토론은 공개 게시판에 "게시"되지 않는다(Pending = 답 대기로 보임). 답이 늦어도 새로 만들지 말고 같은 케이스에 덧붙인다.

## 관련 노트
- [Rust 게임을 Epic Games Store에 붙이기](epic-games-store-for-rust-games.md) — 코드·SDK·업적 표·BuildPatchTool
- [인디 게임을 팔 때의 규칙과 숫자 — Epic 표](../reference/game-business/selling-an-indie-game-rules-and-numbers.md)
- [작은 게임 다국어 구조](small-game-localization.md)
- [인디 게임 소개 페이지](indie-game-landing-page.md)
