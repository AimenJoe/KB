---
title: Rust 게임을 Steam에 붙이기 — 기능 하나로 가르기, 업적 표, 클라우드, 업로드 파이프라인, Deck
type: guide
tags: [gamedev, steam, rust, macroquad, release, github-actions, achievements]
status: draft
created: 2026-11-04
updated: 2026-11-04
verified: |
  2026-11-04 더함: app build VDF·SetLive 규칙은 Steamworks "Uploading to Steam" 원문, 재배포 파일 자리·dylib 설치 이름은 steamworks-sys 0.13 크레이트 파일에서 직접 봄. 실제 업로드는 아직(앱 번호 전).
  1차 출처로 확인(직접 실행·소스, nail-under-the-roots 0276, 2026-11-04): `steamworks` 0.13.1을 선택 의존성 + Cargo 기능 `steam`으로 PC 대상에만 붙여
  리눅스·Windows(cross clippy) 빌드와 웹·Android 빌드가 모두 통과. `steamworks-sys` 0.13.0의 build.rs가 OS별 재배포 파일(steam_api64.dll·libsteam_api.so 등)을
  크레이트 안 `lib/steam/redistributable_bin`에서 `OUT_DIR`로 복사한다는 것, `Client::init()`이 앱 번호를 Steam 실행 환경 또는 지금 폴더의 `steam_appid.txt`에서
  찾는다는 것, `init_app(id)`가 환경 변수 `SteamAppId`를 세운다는 것, 업적 `user_stats().achievement(name).set()` + `store_stats()`와 `run_callbacks()`를
  크레이트 소스에서 읽었다. 업적 표 ↔ 저널 목표 대응·한 번만 열기·숨김 표시는 단위 시험으로 확인.
  확인 못 함: 실제 Steam 클라이언트에 붙여 업적이 열리는 것(이 환경에 Steam이 없다), 클라우드 동기화, steamcmd 업로드, Deck 실기.
  Valve 원문을 직접 읽음(2026-11-04, partner.steamgames.com — 이 작업 환경에서 WebFetch는 막혔지만 curl로는 열렸다):
  업적 가이드(편집기 필드·Spoiler·아이콘 256 권장/64 최소/JPG도 됨·미검증 앱 100개 한도·지우면 딴 사람에게서도 사라짐·Bulk Import/Export CSV 꼴과 아이콘 파일 이름·게시는 Publish 탭·출시 점검표),
  언어 코드 표(koreana·latam 등), 가격(기본가는 $0.99 등급 이상, 할인 바닥은 그 50% ≈ $0.49), 상점 설명 글(바깥 링크·암시 URL 금지, 링크는 기본 정보 칸),
  Steam Deck 호환(가장 작은 글자 1280×800에서 9px 이상, 30cm에서 읽힘 · 패드면 패드 글자만 · 1280×800 권장 또는 1280×720 · 글 입력은 화면 키보드 API 또는 자체 입력),
  Cloud(세션 앞뒤로 동기화, 작은 파일·자주 바뀌는 것과 아닌 것을 나누기, 저장 경로는 Steam 사용자마다 갈리게, Auto-Cloud 루트는 Cross-Platform + OS별 Root Override, 사용자당 용량·파일 수 설정).
  검색 요약으로만 봄: SDK 계약의 재배포(우리 게임과 함께 실행 파일 꼴로만).
  2차 출처만 있음: SteamPipe 업로드 액션(game-ci/steam-deploy·remmik 포크 README — 빌더 계정, config.vdf, 기본 브랜치 대신 beta, Windows 러너에서 도커 문제),
  macOS 공증이 Steam에서 필수가 아니라는 것(2019 Steamworks 공지 댓글의 인용·개발자 블로그: Steam이 받은 파일엔 격리 표시가 없어 Gatekeeper가 보지 않는다),
  비슷한 로그라이트의 업적 수(10~130개, 상점 목록).
sources:
  - https://docs.rs/steamworks/
  - https://lib.rs/crates/steamworks-sys
  - https://partner.steamgames.com/documentation/sdk_access_agreement
  - https://partner.steamgames.com/doc/steamdeck/compat
  - https://partner.steamgames.com/doc/features/cloud
  - https://partner.steamgames.com/doc/store/pricing
  - https://www.github.com/game-ci/steam-deploy
  - https://gh.r-mj.com/Remmik/steam-deploy
  - https://steamcommunity.com/groups/steamworks/eventcomments/1742266164814599752
  - https://mattprice.pages.dev/2020/notarization-rundown
  - https://blendogames.com/news/post/2026-02-19-steamdeckverification/
  - https://gameworldobserver.com/2023/08/16/steam-minimum-price-new-thresholds-equivalent-to-0-99-usd
---

# Rust 게임을 Steam에 붙이기 — 기능 하나로 가르기, 업적 표, 클라우드, 업로드 파이프라인, Deck

## 요약
Steam 연동은 **Cargo 기능 하나**(`steam`)로 PC 빌드에만 붙이고, 연결이 안 되면 조용히 그냥 켜지게 한다 — 웹·모바일·직접 받는 PC 판은 손대지 않는다. 업적은 따로 세지 말고 **이미 있는 목표 목록(저널)에서 골라** 이름·설명·조건을 빌린다(번역이 공짜, 어긋날 일이 없다). 저장이 작으면 클라우드는 코드 없는 Auto-Cloud로 충분하다. 업로드는 steamcmd + **업로드 전용 빌더 계정** + `beta` 브랜치까지만 자동, 공개는 사람이. Deck은 글자 크기(1280×800에서 9px 이상)와 "패드면 패드 글자만"이 핵심이다.

## 본문
### 1. 기능 하나로 가르기
```toml
[features]
steam = ["dep:steamworks"]

[target.'cfg(not(any(target_arch = "wasm32", target_os = "android", target_os = "ios")))'.dependencies]
steamworks = { version = "0.13", optional = true }
```
- 연결 모듈 하나(`steam.rs`)에 `#[cfg(feature = "steam")]`을 몰아넣고, 기능이 없으면 같은 함수가 빈 손이 되게 한다. 게임 코드는 `steam.tick()`·`steam.sync(&기록)`만 부른다.
- `Client::init()` 실패(Steam이 꺼짐·앱 번호 모름·소유하지 않음)는 오류가 아니라 "연결 없이 켠다"로 처리한다.
- 앱 번호는 코드에 박지 않는다: Steam으로 켜면 Steam이 알려 주고, 개발 중에는 실행 파일 옆(정확히는 지금 폴더) `steam_appid.txt`. 이 파일은 배포 묶음에 넣지 않는다.
- 빌드 확인은 크로스 clippy로 충분하다(`--target x86_64-pc-windows-msvc --features steam`) — 링크 없이 된다.

### 2. SDK 재배포 파일
- `steamworks-sys`가 OS별 재배포 파일을 크레이트 안에 싣고 빌드 때 `OUT_DIR`로 복사한다. 그래서 **레포에 SDK 파일을 커밋할 필요가 없다**(공개 레포라면 하지 말 것 — SDK 계약은 "우리 게임과 함께, 실행 파일 꼴로만" 나눠 주게 한다).
- 배포 묶음을 만드는 CI가 그 파일(`steam_api64.dll`·`libsteam_api.so`·`libsteam_api.dylib`)을 실행 파일 옆에 둔다.
- SDK는 카피레프트(GPL) 코드와 섞으면 문제가 된다. MIT·Apache 게임이면 괜찮다.

### 3. 업적 = 목표 목록에서 고른 표
- 표 한 줄 = (Steam API 이름, 빌려 올 목표 아이디, Spoiler). API 이름은 **한 번 올리면 바꾸지 않는다**(저장 키처럼 — 바꾸면 이미 나간 판의 호출이 조용히 빗나간다).
- API 이름 짓기: `ACH_` 접두(Valve 예제도 `ACH_WIN_ONE_GAME`) + **조건**을 말하는 영어, 진행 막대용 통계는 `STAT_`로 갈라 둔다. **숫자 기준은 넣지 않는다**(`ACH_KILLS`이지 `ACH_KILL_200`이 아니다 — 목표 수를 고쳐도 이름은 그대로). 같은 종류는 같은 꼬리(`_BACK`·`_DEEPEST`). 확정 목록을 시험에 그대로 적어 얼린다: 바꾸거나 지우면 실패, 새 것은 끝에만.
- 기록이 저장될 때마다 "이룬 것 − 이번 실행에서 이미 연 것"만 `set` → `store_stats()` 한 번. 켠 뒤 첫 프레임에 한 번 돌리면 **옛 기록으로 이미 이룬 것도** 열린다(이미 열린 업적을 다시 열어도 아무 일 없다).
- 고르는 기준: 이야기·발견이 반, 실력이 조금, 갈아 넣는 수(처치 1000)는 빼거나 둘째 단계까지. 엔딩 뒤 이야기는 **숨김**(상점 업적 목록이 스포일러가 된다).
- 파트너 사이트에 손으로 옮길 등록표(API 이름·숨김·언어별 이름과 설명)는 시험 하나가 파일로 만든다 — 손으로 쓰면 표와 어긋난다. Steam API 언어 코드: **koreana**(korean이 아니다)·english·japanese·schinese·tchinese·brazilian·french·spanish(스페인)·latam(중남미)·german·russian·polish — 중립 스페인어 하나면 spanish·latam 두 칸에 같은 글.
- 손으로 옮기지 말고 편집기의 **Bulk Import/Export**로: 정의 CSV(`api_name,setid,permission,spoiler,archived,progress_stat_name,progress_stat_min,progress_stat_max`), 번역 CSV(`api_name,field` + 언어 칸 — 업적마다 `name`·`description` 두 줄, API 이름은 대소문자 구분), 아이콘은 `<API>_ACHIEVED.png`·`<API>_UNACHIEVED.png`로 이름 지어 같이 끌어다 놓으면 이름으로 붙는다(잠김 아이콘은 "자동 생성"도 있다). 머리줄은 앱의 Export 틀과 대조하고, 언어부터 설정해야 번역 CSV에 그 칸이 생긴다. 이 CSV도 업적 표에서 시험이 만든다.
- "숨김"의 지금 이름은 **Spoiler**(이루거나 펼치기 전까지 이름·설명을 감춤, 상점 업적 칸에도 안 나온다). 업적을 **지우면 이미 딴 사람에게서도 사라진다** — 그만둘 업적은 Archive. 정의 CSV에서 빠진 업적은 "지우기"를 체크하지 않는 한 남는다. 미검증 앱은 업적 100개까지.
- 아이콘 두 장(열림·잠김): **256×256 PNG 권장**(최소 64, 정사각형, 크면 256으로 줄인다). 픽셀 그림은 64점으로 지어 4배 최근접으로 키우면 점이 그대로다. 게임에 이미 있는 그림에서 — 2배 밀도로 저장한 그림은 128을 잘라 반으로 줄이면 64점에 맞는다. 테두리 색을 목표 갈래 색과 맞추고, 잠김은 흑백·어둡게. 업적마다 아이콘 두 장이 있는지 시험이 본다.

### 4. 클라우드
- 계정별 폴더 만들기(직접 해 봄): Steam 연결 직후 `client.user().steam_id().account_id().raw()`(= Auto-Cloud 변수 `{Steam3AccountID}`)로 `<앱 폴더>/steam-<번호>/`를 기록 폴더로 정한다 — **기록을 처음 읽기 전에**(Steam 초기화를 앱 시작 맨 앞으로). 설정(화면·소리·키)은 기기의 것이라 앱 폴더에 두고 클라우드에서 뺀다. 옛 기록(Steam 전·직접 받은 판)은 계정 폴더가 비었을 때 **첫 계정 하나만 복사**하고 바깥에 표를 남긴다 — 옮기면 직접 받은 판이 기록을 잃고, 표가 없으면 둘째 계정에게 같은 진행이 또 간다. Auto-Cloud 루트는 `WinAppDataRoaming`·`MacAppSupport`·`LinuxXdgDataHome` + 하위 `앱/steam-{Steam3AccountID}`.
- 저장이 몇 KB + 설정 한 장이면 **Auto-Cloud**(파트너 사이트에 OS별 경로만, 코드 없음). Steam은 세션 앞뒤로 동기화한다. 루트는 기본값 Cross-Platform으로 두고 다른 OS는 Root Override, 사용자당 용량·파일 수를 정해야 켜진다. **저장 경로는 Steam 사용자마다 갈려야 한다**(원문 권고 — 한 PC 두 Steam 계정이 같은 폴더면 서로의 저장을 덮는다; OS 사용자 폴더만으로는 부족할 수 있어 Steam 판은 계정 번호 하위 폴더를 고려).
- 파일은 작고 적게. 큰 파일·작은 파일 여럿은 종료·재실행을 늦춘다.

### 5. 업로드 파이프라인(SteamPipe)
- **업로드 전용 빌더 계정**(앱 메타데이터 편집·변경 게시 권한만, 그 앱만)을 만든다. 본 계정을 CI에 넣지 않는다.
- 인증은 그 계정으로 한 번 로그인해 만든 `config.vdf`를 시크릿으로(또는 TOTP 비밀). `config.vdf`는 가끔 만료된다 — 실패하면 다시 로그인해 갈아 끼운다.
- 데포는 OS마다 하나(Windows·macOS·Linux). 릴리스 태그 때 Steam 기능으로 다시 빌드해 데포 폴더에 놓고 **`beta` 브랜치까지만** 올린다. 기본(default) 브랜치로 옮기는 것은 사람이 파트너 사이트에서.
- 도커로 도는 액션은 Windows 러너에서 안 된다 — 리눅스 러너에서 세 OS 묶음을 받아 steamcmd로 한 번에 올리거나, steamcmd를 직접 부른다.

- app build 스크립트(원문 "Uploading to Steam"): `"AppBuild" { "AppID" … "Desc" … "SetLive" "<베타 갈래>" "ContentRoot" … "BuildOutput" … "Depots" { "<데포>" { "FileMapping" { "LocalPath" "windows/*" "DepotPath" "." "recursive" "1" } } … } }` → `steamcmd +login <빌더> +run_app_build <vdf> +quit`. **`SetLive`는 베타 갈래만 — 기본 갈래는 자동으로 못 건다**(원문). 실패하면 콘솔이 아니라 BuildOutput의 `*.log`를 본다.
- 재배포 파일 놓기(steamworks-sys 0.13 소스에서 확인): Windows `steam_api64.dll`, macOS `libsteam_api.dylib`(겸용 x86_64+arm64, 설치 이름 `@loader_path/libsteam_api.dylib` → `.app/Contents/MacOS/`에 실행 파일과 같이), Linux `libsteam_api.so`(실행 파일을 rpath `$ORIGIN`으로 빌드 — Steam이 게임 폴더를 라이브러리 경로에 넣어 준다는 보장을 못 찾음). 모두 빌드 때 `target/**/steamworks-sys-*/out/`에 생긴다.
- 묶기는 스크립트 하나로(직접 받는 판·Steam 판·다른 상점 판이 같은 단계를 쓰게) — 상점 판만 재배포 파일·rpath를 더한다.

### 6. 플랫폼·가격
- **macOS**: Mac App Store와 무관하게 Steam이 macOS 데포를 받는다. 공증(Apple $99/년)은 Valve가 "권장, 필수 아님"이라 했고, Steam 클라이언트가 내려받은 파일엔 격리 표시가 없어 Gatekeeper가 공증을 보지 않는다는 보고가 여럿이다(2차) — 공증 없이 먼저 내고 실기에서 막히면 그때 가입해도 된다. 직접 내려받는 zip은 격리 표시가 붙으니 공증 없으면 "그래도 열기"를 안내한다.
- **Linux**: 낮은 glibc(오래된 우분투 러너)로 빌드하면 오래된 배포판·SteamOS에서 돈다.
- **가격**: 기본 가격의 바닥은 $0.99 등급(다른 통화는 그 등급에 맞춘 값), 할인은 그 절반까지.

### 7. Steam Deck 점검표
- 가장 작은 글자 1280×800에서 **9px 이상**(12px 권장) — 가장 흔한 탈락 이유. 320×180 × 4 = 1280×720 화면이면 위아래 띠가 생기고, 11px 글꼴이 44px라 넉넉하다.
- 패드로 놀면 **패드 글자만**(키보드 글자를 숨긴다), 버튼 이름은 Deck 또는 Xbox 이름.
- 글 입력이 있으면 패드로 되게(Steam 화면 키보드 API 또는 게임 안 입력).
- Proton으로 Windows 판을 돌리기보다 리눅스 판을 내면 확인할 것이 줄어든다.

## 왜?
- 기능 하나로 가르면 Steam이 없는 판(웹·모바일·직접 받는 PC)과 같은 코드가 그대로 남는다. Steam이 꺼졌다고 게임이 안 켜지면 리뷰가 망가진다.
- 업적을 목표 목록에서 빌리면 조건을 두 번 세지 않고(버그 두 배), 열한 언어 번역을 다시 하지 않는다. 게임 안 목표와 Steam 업적이 같은 말을 해서 플레이어도 헷갈리지 않는다.
- 업로드를 beta까지만 자동으로 하는 것은 되돌리기 어려운 공개를 사람 손에 두기 위해서다.

## 함정
- API 이름을 바꾸면 이미 연 사람의 업적이 사라진 것처럼 보인다 — 바꾸지 않는다.
- 업적 조건을 게임 쪽에 따로 두면 목표 목록과 어긋난다(목표는 이뤘는데 업적은 안 열림).
- 공개 레포에 SDK 재배포 파일·`steam_appid.txt`·`config.vdf`를 커밋하지 않는다.
- 기본 브랜치로 바로 올리면 시험하지 않은 빌드가 곧장 플레이어에게 간다.
- 개발 중 Valve 시험 앱(480, Spacewar)으로 붙이면 연결·콜백은 시험되지만 우리 업적 이름은 없다 — 업적 시험은 앱이 생긴 뒤.

## 관련 노트
- [Rust 게임을 Epic Games Store에 붙이기](epic-games-store-for-rust-games.md)
- [인디 게임을 팔 때의 규칙과 숫자](../reference/game-business/selling-an-indie-game-rules-and-numbers.md)
- [macroquad PC 빌드](../reference/macroquad/desktop-build.md)
- [운영판과 개발판을 갈라 내보내기](dev-and-release-flavors.md)
- [로그라이트 저널(목표 목록)](../concepts/roguelite-journal-goals.md)
