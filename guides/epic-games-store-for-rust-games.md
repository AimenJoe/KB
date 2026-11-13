---
title: Rust 게임을 Epic Games Store에 붙이기 — EOS 로그인·업적, 일괄 올리기 파일, BuildPatchTool
type: guide
tags: [gamedev, epic, rust, release, achievements, github-actions]
status: draft
created: 2026-11-04
updated: 2026-11-13
verified: |
  1차 출처로 확인(2026-11-04, dev.epicgames.com 원문을 헤드리스 브라우저로 읽음 — store.epicgames.com은 봇 확인 창에 막힘):
  - EOS "Log In with an Epic Games Account"(Connect): Auth 로그인 → EOS_Auth_CopyIdToken → EOS_Connect_Login(EOS_ECT_EPIC_ID_TOKEN) →
    EOS_InvalidUser면 EOS_Connect_CreateUser(ContinuanceToken), 완료 안 됐으면(EOS_EResult_IsOperationComplete 거짓) 기다림.
  - "Integrate a third-party launcher": Epic 런처가 교환 코드를 명령줄로 넘기고 EOS_LCT_ExchangeCode로 로그인한다(코드는 짧게 만료).
  - 업적: EGS 업적은 EOS 업적에 잇는다, XP 합 정확히 1,000·하나 5~200·5의 배수, 다른 PC 상점에 업적이 있으면 의무, 웹·macOS 판은 면제,
    올린 뒤 XP 수정·삭제 불가. EOS 업적 아이디에 % 금지, 아이콘 256 권장.
  - Bulk Import 템플릿(BulkTemplate.zip을 받아 열어 봄): achievementDefinitions.csv `name,hidden,statThresholds`,
    achievementLocalizations.csv `name,locale,lockedTitle,lockedDescription,unlockedTitle,unlockedDescription,flavorText,lockedIcon,unlockedIcon`
    (빈 locale = 기본, 아이콘 칸 = zip 맨 위의 파일 이름), stats.csv `name,aggregationType`.
  - BuildPatchTool 1.8 지침: `-mode=UploadBinary -OrganizationId -ProductId -ArtifactId -ClientId -ClientSecretEnvVar -BuildRoot -BuildVersion -AppLaunch -AppArgs -CloudDir`,
    비밀은 `ClientSecretEnvVar` 권장, CloudDir은 실행마다 다른 임시 폴더, Windows·macOS·Linux판.
  크레이트 소스로 확인: eos-sys 0.1.1(MIT/Apache)은 미리 만든 바인딩을 싣고(libclang 불필요) Windows에서만 `EOS_SDK_DIR/Lib`로 링크 지시를 낸다 —
  SDK 없이도 `cargo clippy --target x86_64-pc-windows-msvc`는 된다. wrapper.h가 eos_achievements.h의 함수를 빼서 업적 함수는 직접 extern으로 선언해야 한다(타입은 있다).
  직접 해 봄: 위 흐름으로 짠 코드가 Windows 대상 clippy -D warnings 통과(nail-under-the-roots src/epic.rs). 실제 로그인·업적 열기는 포털·SDK 뒤라 확인 못 함.
  2026-11-05 더함(dev.epicgames.com 원문, 헤드리스 브라우저): 클라이언트 정책 종류(Client & Client Policy Reference·Guide),
    EAS 신청 단계(Get Started with Epic Account Services), 브랜드 검토의 도메인 확인(Brand Review Process·Domain Verification), Epic Games ID 제공자는 설정 불필요(Identity Provider Management).
    직접 봄: 포털의 제품 설정 화면(제품·Live 샌드박스·Live 배포 아이디가 상품을 만들면 바로 생기고, 클라이언트는 따로 만든다).
  2026-11-13 바로잡음(Domain Verification 원문을 검색 요약으로 읽음 — dev.epicgames.com 직접 접속은 세션에서 막힘): 최상위 도메인 승인 = 하위 도메인 자동 승인(전엔 반대로 적었다),
    도메인 확인과 브랜드 검토의 주소 꼴을 맞춘다, 메일용 하위 도메인은 따로 확인.
  2차 출처만 있음: 런처 인자 이름 `-AUTH_PASSWORD=<교환 코드>`(포럼·gist — 원문 참조 문서 "Auth Interface Reference > Epic Games Launcher"는 못 읽음).
  확인 못 함: EOS 로컬 언어 코드 꼴(zh-Hans·pt-BR 등), EGS 업적(XP) 일괄 올리기 템플릿, BuildPatchTool의 macOS 앱 실행 경로 꼴.
sources:
  - https://dev.epicgames.com/docs/epic-online-services/eos-fundamentals/connect-interface/connect-guide/log-in-with-an-epic-games-account
  - https://dev.epicgames.com/docs/epic-online-services/accounts-and-social/eos-epic-account-services/auth-interface/integrate-a-third-party-launcher-with-egs
  - https://dev.epicgames.com/docs/epic-games-store/services/epic-achievements/achievements-setup
  - https://dev.epicgames.com/docs/epic-online-services/player-and-game-data/achievements-interface/achievements-guide/set-up-achievements
  - https://dev.epicgames.com/docs/epic-online-services/eos-fundamentals/tools/bulk-importer-exporter-tool
  - https://dev.epicgames.com/docs/epic-games-store/publishing-tools/uploading-binaries/bpt-instructions-180
  - https://crates.io/crates/eos-sys
  - https://dev.epicgames.com/docs/epic-games-store/store-presence/manage-artifacts
  - https://dev.epicgames.com/docs/epic-online-services/eos-fundamentals/client-and-client-policy/client-policy-reference
  - https://dev.epicgames.com/docs/epic-online-services/eos-fundamentals/client-and-client-policy/client-policy-guide
  - https://dev.epicgames.com/docs/epic-account-services/getting-started
  - https://dev.epicgames.com/docs/epic-online-services/accounts-and-social/eos-epic-account-services/brand-review/domain-verification
  - https://dev.epicgames.com/docs/epic-online-services/eos-fundamentals/identity-provider-management
  - https://forums.unrealengine.com/t/how-to-test-eos-lct-exchangecode/886227
---

# Rust 게임을 Epic Games Store에 붙이기

## 요약
Steam처럼 **Cargo 기능 하나**(`epic`, Windows만)로 가르고, 없으면 조용히 그냥 켜지게 한다. 업적은 **EOS 업적**을 열면 되고 Epic 상점 업적은 포털에서 그 EOS 업적에 이어 **XP(합 1,000)** 만 준다 — 같은 업적 표에 XP 칸 하나. 로그인은 "런처의 교환 코드 → Epic 계정 → ID 토큰 → EOS Connect(처음이면 사용자 만들기) → ProductUserId". SDK·BuildPatchTool은 포털에서 받는 파일이라 공개 레포에 넣지 않고 비공개 저장소 + CI 환경 변수로.

## 본문
### 1. 바인딩
- `eos-sys`(미리 만든 바인딩) — SDK 없이 Windows 대상 검사가 된다. 링크·실행에는 `EOS_SDK_DIR`(Include·Lib·Bin)과 실행 파일 옆 `EOSSDK-Win64-Shipping.dll`.
- 업적 함수(`EOS_Achievements_UnlockAchievements`)는 바인딩에 없다 → 서명 그대로 `extern "C"` 하나 직접(옵션 구조체·콜백 타입은 있다).

### 2. 로그인과 업적(콜백은 `EOS_Platform_Tick` 안에서)
1. `EOS_Initialize`(제품 이름·버전) → `EOS_Platform_Create`(ProductId·SandboxId·DeploymentId·ClientId/Secret).
2. 명령줄 교환 코드로 `EOS_Auth_Login(EOS_LCT_ExchangeCode)`. 개발 중에는 Developer Authentication Tool + `EOS_LCT_Developer`(Id = host:port, Token = 자격 이름).
3. 성공 → `EOS_Auth_CopyIdToken` → `EOS_Connect_Login(EOS_ECT_EPIC_ID_TOKEN, JsonWebToken)` → 토큰 해제.
4. `EOS_InvalidUser`면 `EOS_Connect_CreateUser(ContinuanceToken)`. 완료되지 않은 결과면 기다린다.
5. ProductUserId로 `EOS_Achievements_UnlockAchievements(아이디 배열)`. 로그인 전에 이룬 것은 로그인 뒤 한꺼번에(매번 다시 열어도 된다 — 원문, 재시도 간격만 지킨다).
- 콜백 상태는 상자에 담아 주소를 고정하고 그 주소를 ClientData로.
- 아이디는 빌드 때 환경 변수(`option_env!`)로 — 공개 레포에 적지 않는다.

### 3. 업적 자료
- EOS 일괄 올리기 zip = `achievementDefinitions.csv` + `achievementLocalizations.csv`(언어마다 한 줄, 빈 locale = 기본) + 아이콘(이름으로 붙는다). 같은 업적 표에서 시험이 CSV를 만들고 작은 스크립트가 아이콘과 묶는다.
- Epic 상점 업적은 따로: EOS 업적에 이어 XP만. **합 1,000, 5~200, 5의 배수** — 표에 칸을 두고 시험으로 지킨다. 올린 뒤 못 바꾼다.
- 잠김 아이콘은 Epic 상점이 쓰지 않는다(반투명 + 자물쇠).

### 4. 업로드
- BuildPatchTool `-mode=UploadBinary`(조직·제품·아티팩트·클라이언트 아이디, 비밀은 `-ClientSecretEnvVar`, `-BuildVersion`은 겹치지 않게, `-CloudDir`은 임시 폴더). 라벨 붙이기·출시는 포털에서 사람이.
- **아티팩트**는 오퍼(기본 게임)를 만들면 자동으로 하나 생기는 "내려받는 것 하나"다. 플랫폼마다·샌드박스마다 따로 만들지 않는다 — Windows·macOS 바이너리를 같은 아티팩트에 올리고 바이너리마다 Manage Platforms로 플랫폼을 고른다. 올리는 곳은 늘 Dev 샌드박스, Stage·Live로는 Release Management로 올린다. `-BuildVersion`은 아티팩트 안에서 플랫폼까지 겹치면 안 된다(`1.0.0-windows`·`1.0.0-macos`). 아티팩트에 배포(deployment) ID를 걸어 두면 런처가 `-epicdeploymentid`·`-epicsandboxid`를 넘긴다(선택). [원문: Manage Artifacts·BPT 1.8]
- 리눅스 러너에서 Linux판 BuildPatchTool로 Windows·macOS 빌드를 올릴 수 있다(빌드 폴더만 있으면 된다 — 원문이 플랫폼별 도구가 같다고 함).

### 5. 포털 준비(사람이 하는 순서)
1. 조직·상품 만들기 → 제품 설정에 제품 ID·Live 샌드박스·Live 배포가 생긴다. 클라이언트는 없다.
2. **클라이언트 정책** → **클라이언트**. 미리 정의된 정책은 Peer2Peer·TrustedServer·GameClient·`GameClient /w UnlockAchievements`. 업적만 여는 게임이면 마지막 것, 또는 사용자 지정(Achievements의 `unlockAchievementForLocalUser`·`findAchievementDefinitions`·`findAchievementsForLocalUser` — 문서는 운영판에 사용자 지정을 권한다). 정책 없이도 인증은 되지만 업적은 `EOS_ClientPolicyMissingAction`. TrustedServer 자격은 공개 빌드에 넣지 않는다.
3. 교환 코드 로그인(`EOS_Auth_Login`)은 **Epic Account Services**라 EAS 신청이 따로 있다: 약관 → 브랜드 설정(앱 웹사이트·개인정보처리방침 URL·128px 로고) → 권한(Basic Profile은 필수) → 연결된 클라이언트 → 브랜드 검토. **검토를 통과하기 전에는 조직 밖 사용자가 로그인할 수 없다.**
4. 앱 웹사이트는 조직 설정 → Domains에서 **DNS TXT 레코드로 소유를 확인한 도메인**이어야 하고, 사이트에 조직 이름·제품 이름과 소개가 있어야 한다(PEGI 12 이하 내용). **최상위(apex) 도메인이 승인되면 하위 도메인도 자동 승인**이다(반대가 아니다 — 2026-11-13 바로잡음). 메일 알림에 하위 도메인을 쓰면 그것은 따로 확인. 도메인 확인과 브랜드 검토에는 **같은 꼴의 주소**를 넣는다(`foo.com`으로 확인했으면 브랜드 검토에도 `foo.com`). 사이트에 상품·퍼블리셔 소개가 없으면 반려된다(포럼 사례).
5. "Epic Games" ID 제공자(Connect)는 포털 설정이 필요 없다.

## 왜?
업적 자료를 상점마다 따로 손으로 만들면 이름·설명·숨김이 어긋난다. 한 표(목표·API 이름·숨김·XP)에서 Steam CSV·EOS CSV·XP 표가 같이 나오면 상점이 늘어도 고칠 곳은 한 줄이다. 로그인을 상점 기능 안에 가두면 직접 받는 판·웹·모바일은 아무것도 모른다.

## 함정
- 바인딩 크레이트가 모든 헤더를 싣지 않을 수 있다 — 필요한 함수가 있는지 먼저 grep.
- 교환 코드는 몇 분 안에 만료 — 시작하자마자 로그인한다. 런처 밖에서는 코드가 없다(개발 로그인을 따로).
- macOS 판은 EOS 오버레이가 없어 업적 의무가 면제 — 같은 기능을 macOS에서 켜도 연결 코드는 빈 손이게(cfg windows).
- 개발자 포털의 제품 이름·EAS 애플리케이션 이름 칸은 특수 문자(`ï`·`:` 같은 것)를 받지 않는다(사용자가 직접 겪음, 2026-11-05 — 허용 문자 목록은 원문에서 못 찾음). `Naïl: Under the Roots` → `Nail Under the Roots`처럼 영문·숫자·공백으로. 상점 페이지 제목은 따로 정한다.
- `<사용자>.github.io` 같은 남의 도메인은 DNS TXT를 넣을 수 없어 EAS 브랜드 검토의 도메인 확인을 못 한다 — 자체 도메인을 사서 같은 페이지를 사용자 지정 도메인으로 띄운다(확인한 사례는 없음, 문서 조건에서 따져 본 것).
- 포털 "헤더 파일의 크리덴셜 사용"은 아이디를 소스에 박는 방식 — 공개 레포면 쓰지 말고 빌드 때 환경 변수로.
- Epic 상점 페이지 문서(store.epicgames.com)는 봇 확인에 막히는 일이 있다 — dev.epicgames.com 문서가 같은 내용을 더 자세히 가진다.

## 관련 노트
- [Rust 게임을 Steam에 붙이기](steam-release-for-rust-games.md)
- [인디 게임을 팔 때의 규칙과 숫자 — Epic 표](../reference/game-business/selling-an-indie-game-rules-and-numbers.md)
- [공개 레포에서 배포 파이프라인 지키기](protect-deploy-pipeline-in-public-repo.md)
