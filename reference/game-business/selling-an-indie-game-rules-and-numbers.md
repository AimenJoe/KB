---
title: 인디 게임을 팔 때의 규칙과 숫자 — Steam·Play·Apple·itch, AI 공개, 위시리스트, 한국 세금·등급
type: reference
tags: [gamedev, marketing, steam, business, legal, ai-image, itch-io]
status: draft
created: 2026-10-29
updated: 2026-10-29
verified: |
  1차 출처로 확인(2026-10-29, 원문을 직접 받아 읽음): Steamworks 문서(Content Survey의 AI 절, Steam Direct, Coming Soon, Next Fest와 2027-02판, 오픈소스 배포, 세금 FAQ),
  IRS 조세조약 표 1(2023-05판, 한국 줄), Google Play Console 도움말(서비스 수수료·12명 시험), Android Developers(target SDK·개발자 확인)·Developer Console 도움말,
  Apple Developer(회비 면제·Small Business Program), itch.io FAQ와 오픈 수익 배분 공지, Gemini API 추가 약관(2026-03-23판), 문체부 보도자료(2019 시행령).
  데이터 회사·분석가의 원문(1차 데이터지만 추정치): Gamalytic 위시리스트 전환(2024-04-29), GameDiscoverCo EA 졸업작(2026), Sulka Haro의 Steam AI 표시 전수 조사(2023-07~2026-07).
  2차 출처만 있음: 매출 중앙값($249·$1,136), Boxleiter 배수(리뷰×20~60), Next Fest 위시리스트 중앙값(설문), 플레이어 AI 반감 설문(8% "절대 안 산다"), 캡슐 외주 시세.
  확인 못 함: Valve의 한국 자체등급분류사업자 지정 여부(2024 "관심" 보도 뒤 소식 없음), 게임위 등급분류 수수료표, STOVE 수수료.
sources:
  - https://partner.steamgames.com/doc/gettingstarted/contentsurvey
  - https://partner.steamgames.com/steamdirect
  - https://partner.steamgames.com/doc/store/coming_soon
  - https://partner.steamgames.com/doc/marketing/upcoming_events/nextfest
  - https://partner.steamgames.com/doc/marketing/upcoming_events/nextfest/feb_2027
  - https://partner.steamgames.com/doc/sdk/uploading/distributing_opensource
  - https://partner.steamgames.com/doc/finance/taxfaq
  - https://www.irs.gov/pub/irs-lbi/tax-treaty-table-1.pdf
  - https://support.google.com/googleplay/android-developer/answer/112622
  - https://support.google.com/googleplay/android-developer/answer/14151465
  - https://developer.android.com/google/play/requirements/target-sdk
  - https://developer.android.com/developer-verification
  - https://support.google.com/android-developer-console/answer/16561738
  - https://developer.apple.com/app-store/small-business-program/
  - https://itch.io/developers/faq
  - https://itch.io/updates/introducing-open-revenue-sharing
  - https://ai.google.dev/gemini-api/terms
  - https://www.mcst.go.kr/site/s_notice/press/pressView.jsp?pSeq=17434
  - https://gamalytic.com/blog/exploring-steam-wishlist-sale-ratio
  - https://newsletter.gamediscover.co/p/what-happened-to-early-access-graduates
  - https://fragwyz.substack.com/p/three-years-of-ai-on-steam
---

# 인디 게임을 팔 때의 규칙과 숫자

## 요약
1인 인디 게임을 유료로 낼 때 막히는 규칙(스토어 가입·심사 기간·행사 조건·AI 공개·수수료·세금·등급)과 기대치를 정하는 숫자(위시리스트 전환·AI 표시 게임의 성과)를 원문 기준으로 모았다. 결론은 셋이다. **위시리스트가 판매를 정한다**, **Next Fest는 게임당 한 번이다**, **AI 그림 공개는 피할 수 없고 성과가 눈에 띄게 낮다.**

## 본문

### Steam
| 항목 | 내용(2026-10 원문) |
|---|---|
| 가입 | Steam Direct 앱당 $100, 조정 총매출 $1,000을 넘은 뒤 정산 때 돌려준다. 은행·세금·신원 서류 15~30일, 결제 뒤 **출시까지 30일 대기** |
| 상점 페이지 | 새 게임은 Coming Soon을 **최소 2주** 공개해야 출시. 검토 요청은 공개 7영업일 전. Valve: 2년 전에 찜한 사람도 2주 전에 찜한 사람만큼 산다 — 일찍 열어도 손해가 거의 없다 |
| Next Fest | **게임당 한 번만**. 조건: 상점 페이지 공개, 행사 시작 때 공개 데모, 행사 끝까지 미출시. 데모 길이·독점 조건 없음. 데모 빌드 검토는 약 3주 전. 2027-02판: 02-22~03-01, 등록 마감 01-10 |
| AI 공개 | Content Survey의 생성형 AI 절. **Pre-Generated**(개발 중 AI로 만들어 게임과 함께 나가 플레이어가 보는 것: 그림·소리·서사·현지화)와 **Live-Generated**(실행 중 생성, 불법 생성물 가드레일 설명 추가). 효율을 위한 개발 도구(코드 도우미 등)는 대상이 아니라고 문서가 밝힌다. 마케팅 자료가 대상인지는 문서에 없다 |
| 오픈소스 | Steamworks SDK는 카피레프트(GPL)와 문제가 된다. MIT·BSD·Apache 2.0은 괜찮다 |
| 세금(미국 원천징수) | 조약이 없으면 30%. W-8BEN으로 조약 세율. **한국: 저작권 사용료 10%**(IRS 표 1, 2023-05판; 특허·노하우 15%). 게임 판매에는 "royalty copyright" 세율. TIN을 나중에 넣어도 이미 뗀 것은 돌려주지 않는다 |

### 위시리스트·성과 숫자(데이터 회사 추정)
- Gamalytic(2024-04): 첫 주 판매 = 출시 위시리스트의 중앙값 22%, 첫 달 27%(첫 달 500장 미만 제외). EA는 약 20%, 정식은 약 30%. 상위 10%는 134%, 하위 10%는 6%. 출시 할인 10~15%는 전환을 크게 바꾸지 않는다.
- GameDiscoverCo(2026): EA 졸업작 91개 중 **21%만** 1.0 매출이 EA 출시보다 많았다. EA 기간 중앙값 1년 3개월.
- Sulka Haro(전수 53,597개, 2023-07~2026-07, 매출은 리뷰×30 추정): AI 표시 비율 2024 10.9% → 2025 19.9% → 2026 30.8%. AI 표시 게임의 매출 몫은 10~27%로 출시 비중(~33%)보다 낮다. 출시 시기를 맞춰도 AI 표시 게임이 **리뷰 100개(≈3천 장)에 닿는 비율은 비AI의 약 55%**. 망한 AI 게임은 그림에만 쓰고 공개 문구가 짧았고(중앙값 13단어), 성공작은 쓴 곳과 사람의 손질을 구체적으로 적었다.
- 2차(설문·블로그): Steam 신작 매출 중앙값은 수백 달러 수준, 리뷰 1개 ≈ 판매 20~60장(최근 약 30).

### 다른 스토어
| 스토어 | 내용 |
|---|---|
| Google Play | 개인 계정(2023-11-13 뒤)은 **12명 × 14일 비공개 시험** 뒤 정식 출시. 새 앱·업데이트는 **targetSdk 36**(2026-08-31~). 수수료: EEA·영국·미국(2026-06-30)·호주·일본(2026-09-30)은 새 구조(첫 $1M 10% + 결제 5% 등), **한국 등 나머지는 아직 15%(첫 $1M)/30%**, 한국은 대체 결제 시 4%p 낮음 |
| Android 직접 설치 | 개발자 확인: 2026-09-30 일부 나라, **2027년 전 세계**. 확인 안 된 앱은 고급 흐름(경고·대기)으로만. 정식 배포 계정 $25, **제한 배포 계정은 무료·신분증 없이 기기 20대까지**. ADB는 그대로 |
| App Store | 연 $99(회비 면제는 비영리·교육기관·정부만). Small Business Program 15%(전년 수익 $1M 이하·신규) |
| itch.io | 수익 배분을 개발자가 정한다(**기본 10%**), Stripe·PayPal로 바로 받는다, EU VAT 자동 |

### 그림 도구·에셋·한국 규칙
- Gemini API 추가 약관(2026-03-23): 생성물 소유권을 주장하지 않는다, 같거나 비슷한 것을 남에게도 만들 수 있다, **무료 사용분(AI Studio·무료 할당)은 입력·결과를 제품 개선에 쓰고 사람이 볼 수 있다**, 18세 이상·업무 목적. 소비자용 Gemini 앱은 이 약관이 아니라 Google 서비스 약관 — 어느 제품을 썼는지 기록해 둔다.
- 등급분류(한국): 2019-09-03 시행령으로 개인·동호회의 **비영리 단순공개** 게임은 면제(청소년이용불가 내용 제외). 판매하면 면제 밖. Google·Apple은 자체등급분류사업자, Valve는 지정 소식 없음 — 한국 판매 전 게임위 확인.

## 왜?
- 판매는 품질보다 **출시 때 찜한 사람 수**를 따라간다(전환율 분포가 넓어도 기준점은 위시리스트). 그래서 상점 페이지를 일찍 열고(손해 없음), 한 번뿐인 Next Fest를 위시리스트가 쌓인 뒤에 쓴다.
- AI 공개는 숨길 수 없는 규칙이고, 표시된 게임은 같은 시기 비AI 게임보다 중간 성공에 닿는 확률이 낮다. 원인이 AI 자체인지 품질인지는 데이터가 가르지 못하지만, 사는 사람이 보는 것은 표시다.

## 함정
- "Next Fest에 여러 번 나가면 된다" — 게임당 한 번이다.
- W-8BEN의 납세자번호를 첫 정산 뒤에 넣으면 그동안 뗀 30%는 돌려받지 못한다.
- Google Play 10% 기사는 지역 한정이다. 한국 계산은 15%.
- AI 공개 문구를 한 줄로 때우면 망한 게임들의 모양과 같아진다.
- 매출 숫자 대부분은 리뷰 수에서 거꾸로 추정한 것이다(±크다).

## 관련 노트
- [공개 데모와 바깥 의견 받기](../../concepts/public-demo-and-outside-feedback.md)
- [인디 게임 공식 페이지](../../guides/indie-game-landing-page.md)
- [게임 그림 외주 맡기기](../../guides/commissioning-game-art.md)
- [이미지 모델로 게임 일러스트 그리기](../../guides/image-model-for-game-illustrations.md)
