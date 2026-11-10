---
title: macroquad iOS 빌드 — GitHub Actions macOS 러너로 서명 안 한 .ipa, 기기 시험·배포의 갈림길
type: reference
tags: [macroquad, ios, rust, github-actions, release]
status: draft
created: 2026-10-26
updated: 2026-11-10
verified: |
  1차(소스·문서, 2026-11-10, knellroot 0137): miniquad 0.4.11 `native/ios.rs`의 `draw_in_rect`(GLKView·MTKView 대리자)가 메인 스레드에서
  `update()`·`draw()`를 부른다 — 그 앞에서 GameController를 읽어 `key_down_event`·`key_up_event`로 넘기면 macroquad `is_key_pressed`가 그대로 받는다.
  miniquad는 `objc` 크레이트(`objc-rs`)의 `msg_send!`·`class!`를 이미 쓰고, 프레임워크는 `#[link(name = "GameController", kind = "framework")]`로 잇는다.
  Apple 문서(developer.apple.com): GCExtendedGamepad 요소(buttonA·B·X·Y·leftShoulder·rightShoulder·leftTrigger·rightTrigger·dpad·left/rightThumbstick·
  left/rightThumbstickButton(선택)·buttonMenu·buttonOptions(선택)·buttonHome(선택)), "Handling input events"의 폴링 권장(게임 루프에서 고정 간격),
  Xcode Game Controllers 능력 = Info.plist `GCSupportsControllerUserInteraction` true + `GCSupportedGameControllers`[{ProfileName: ExtendedGamepad}].
  리눅스에서 `cargo clippy --target aarch64-apple-ios` 통과. 확인 못 함: 실기 패드 입력, plist 키 없이도 입력이 오는지.
  1차 출처로 확인(2026-10-26, nail-under-the-roots 0086):
  - miniquad 0.4.11 소스: native/ios.rs(Metal·GLES), fs::load_file이 iOS에서 NSBundle mainBundle pathForResource로 읽음. README의 iOS 절(.app + Info.plist).
  - quad-snd 0.2.8: macOS·iOS에 CoreAudio.
  - gilrs-core 0.5.15에 iOS 플랫폼 없음(linux·macos·wasm·windows·default) → gamepads 크레이트가 iOS에서 빈 백엔드.
  - 리눅스에서 `cargo check --release --target aarch64-apple-ios` 통과.
  - GitHub Actions macos-latest에서 cargo build --release --target aarch64-apple-ios 성공: Mach-O 64-bit arm64, plutil -lint OK, 13.9MB .ipa(서명 안 함).
  게임패드(2026-11-10, nail 0288): GameController 직접 폴링을 리눅스 `cargo clippy --target aarch64-apple-ios`로 확인 — 자세한 근거는
  gamepad-and-android-input.md.
  확인 못 함: 실기에서 실행(화면·터치·소리·저장·패드), 서명 후 설치.
  2차 출처만 있음: 서명 없는 앱은 시뮬레이터에서만, 무료 Apple ID 서명 7일·앱 3개(AltStore·SideStore, Sideloadly FAQ), iOS 16+ 개발자 모드(사용 안내 글 여럿 —
  Apple 문서로는 못 봄), 무료 계정 앱 아이디 한도(10개 — "4일마다"·"한 주"로 글마다 다름), Developer Program 1년·TestFlight,
  공개 레포 macOS 러너 무료(비공개는 분당 과금·배수), CI에서 Xcode 자동 서명이 어렵다(인증서·프로필을 Secrets로 또는 fastlane match), EU 대체 마켓.
  macroquad.rs/articles/ios 문서는 세션에서 접속이 안 되어 못 읽었다.
sources:
  - https://sideloadly.io/faq
  - https://ios.cfw.guide/sideloading-apps
  - https://developer.apple.com/documentation/gamecontroller/handling-input-events
  - https://developer.apple.com/documentation/gamecontroller/gcextendedgamepad
  - https://developer.apple.com/documentation/xcode/configuring-game-controllers
  - https://github.com/not-fl3/miniquad
  - https://docs.github.com/en/actions/reference/github-hosted-runners-reference
  - https://github.blog/changelog/2026-02-26-macos-26-is-now-generally-available-for-github-hosted-runners/
  - https://blog.codemagic.io/why-github-actions-not-built-for-mobile-cicd
  - https://theapplewiki.com/wiki/AltStore
  - https://dev.to/1_king_0b1e1f8bfe6d1/how-ios-sideloading-actually-works-in-2025-dev-certs-altstore-and-the-eu-exception-1m2h
---

# macroquad iOS 빌드

## 요약
macroquad(miniquad)는 iOS를 지원한다. Xcode 프로젝트 없이 `cargo build --target aarch64-apple-ios`로 빌드한 실행 파일에 손으로 만든 `.app`(Info.plist·assets·아이콘)을 둘러, macOS 러너에서 **서명 안 한 .ipa**를 만든다. 실기에 올리려면 서명이 필요하다. 시험은 무료 Apple ID로(7일), 배포는 Developer Program($99/년)으로 한다. 게임패드는 gilrs에 iOS가 없어 GameController를 직접 읽는 다리가 필요하다(miniquad는 안 고친다).

## 본문
### CI(GitHub Actions)
```yaml
runs-on: macos-latest
steps:
  - uses: dtolnay/rust-toolchain@stable
    with: { targets: aarch64-apple-ios }
  - run: cargo build --release --target aarch64-apple-ios
  - run: |
      app=Payload/Game.app; mkdir -p "$app"
      cp target/aarch64-apple-ios/release/game "$app/"
      cp -R assets "$app/assets"          # NSBundle 바로 아래(코드의 "assets/…" 경로 그대로)
      cp icons/*.png "$app/"; cp Info.plist "$app/"; plutil -lint "$app/Info.plist"
      ditto -c -k --sequesterRsrc --keepParent Payload game-unsigned.ipa
```
- Info.plist에 꼭 넣을 것:
  - CFBundleExecutable·Identifier·ShortVersionString·Version, LSRequiresIPhoneOS, MinimumOSVersion.
  - 스토리보드 없이 전체 화면이려면 `UILaunchScreen`(빈 dict, iOS 14+)을 넣는다. 없으면 옛 기기 크기로 뜬다(2차).
  - 가로 게임이면 UISupportedInterfaceOrientations(~ipad도), UIRequiresFullScreen, UIStatusBarHidden.
  - 아이콘은 에셋 카탈로그 없이 CFBundleIcons → CFBundleIconFiles(`AppIcon60x60` → @2x·@3x 파일)로 지정한다.
- 아이콘은 투명하면 안 된다(검게 채운다). 1024는 App Store용이다.

### 남에게 나눠 주기(상점 없이)
- 서명 안 한 `.ipa`를 GitHub Release에 붙이면 받는 사람이 Sideloadly·AltStore로 **자기 Apple ID로** 서명해 깐다 — 만든 쪽은 Apple 계정·비용이 없다(nail 0291). Actions 아티팩트는 로그인이 필요하고 90일 뒤 지워져서 공개 링크로는 못 쓴다.
- 받는 쪽 짐이 크다(컴퓨터·개발자 모드·7일마다 다시·앱 셋). 페이지에서는 큰 다운로드 버튼보다 안내 칸으로 보내고, 웹판이 있으면 그쪽을 쉬운 길로 먼저 말한다.
- 릴리스 워크플로가 ipa를 붙이기 전의 Release를 가리키는 링크는 404가 된다 — 페이지 스크립트가 Release의 자산 목록을 보고 없으면 Release 페이지로 보낸다.

### 앱 안 저장 자리
- HOME은 샌드박스다. 쓸 수 있는 곳은 `Documents`·`Library`·`tmp` 아래뿐이다. 리눅스식 `~/.local/share`는 안 된다 → macOS와 같은 `~/Library/Application Support/<앱>`.

### 서명 갈림길(2차)
| 길 | 비용 | 기간 | 용도 |
|---|---|---|---|
| 서명 없음 | 0 | — | 시뮬레이터만 |
| 무료 Apple ID + Sideloadly·AltStore·SideStore | 0 | 7일마다 다시 서명, 앱 3개, iOS 16+는 개발자 모드 | 내 기기 시험 · 남에게 "직접 설치"로 나눠 주기 |
| Apple Developer Program + CI codesign(.p12·프로필·App Store Connect API 키를 Secrets로) | $99/년 | 1년 | TestFlight·App Store |
| EU 대체 마켓 | 개발자 계정 필요 | — | EU 안에서만(규칙 재확인) |

### 게임패드
- `gamepads` → gilrs는 iOS 백엔드가 없다(빈 백엔드, 컴파일은 된다). iOS 빌드에서는 크레이트를 뺀다.
- Apple `GameController`(`GCController`)를 잇는 작은 다리가 필요하다. Android 패치처럼 키 코드로 넘기면 게임 쪽 입력 코드는 그대로 둘 수 있다. 버튼 이름·부호·nil·시스템 버튼처럼 API 쪽 사실은 [게임패드 노트](gamepad-and-android-input.md) "iOS".
- 실제로 놓은 다리(knellroot 0137): miniquad 사본에 파일 하나(`native/ios_pad.rs`) — `draw_in_rect`가 `update()` 직전에 부른다.
  1. `[GCController controllers]`에서 `extendedGamepad`가 nil이 아닌 첫 패드.
  2. 버튼 열둘의 `isPressed`를 비트로 모아 지난 그리기와 비교 → 바뀐 비트만 `key_down_event`/`key_up_event`(Android 패치와 같은 F13~F24 — 게임은 두 플랫폼을 한 길로 읽는다).
  3. 스틱·D패드의 `xAxis`·`yAxis` `value`를 원자값 배열에(Android 패치의 `joystick_axes()`와 같은 배열·부호 — GameController는 위가 +라 뒤집는다).
  4. 패드가 빠지면 빈 마스크라 눌린 것이 모두 떼어진다.
- 게임 쪽 cfg는 `target_os` 둘을 매번 쓰지 말고 `build.rs`에서 `cargo:rustc-cfg=pad_keys`(+ `cargo::rustc-check-cfg=cfg(pad_keys)`) 하나로.
- Info.plist에 `GCSupportsControllerUserInteraction`·`GCSupportedGameControllers`(ExtendedGamepad) — Xcode 능력을 손으로.
- 폴링이라 그리기 사이(1/60초 안)의 아주 짧은 누름은 놓칠 수 있다. 문제가 되면 `valueChangedHandler` 콜백으로.
- 다른 길(nail 0288): miniquad를 고치지 않고 게임 쪽 모듈이 `objc-rs`(miniquad와 같은 판 — 새 크레이트 없음)로 같은 것을 읽어 순수한 프레임 값 → 동작 함수로 넘긴다(리눅스 시험이 짝을 본다). 입력 구조가 "플랫폼마다 동작을 돌려주는" 게임이면 이쪽, Android처럼 키로 받는 길이 이미 있으면 위 패치 쪽.
- **두 길 모두 꼭**: (1) 프레임워크 심볼(`GCControllerDidConnectNotification` 등)을 실제로 참조해 링크를 보장하고 CI에서 `otool -L … | grep GameController.framework` — objc-rs `class!`는 클래스를 못 찾으면 panic한다(소스 1차), 빈 `#[link]` 블록만으로는 장담 못 한다. (2) `Class::get`으로 찾아 없으면 패드 없음. (3) 연결·끊김 알림을 한 번 구독(Apple 권장, iOS 15+ 패드 찾기 시작 — 2차). (4) 읽기를 `autoreleasepool`로. (5) 패드 여럿은 합친다. nail 0288은 처음에 (2)를 빠뜨려 `class!(GCController)`로 썼다가 이 목록과 견주고 고쳤다.

## 왜?
- Xcode 프로젝트를 두지 않으면 레포에 생성물이 없고, 리눅스 개발자도 CI만으로 빌드한다. macroquad가 Objective-C 호출을 코드 안에서 다 하므로 .app은 파일 몇 개로 충분하다.
- 서명은 Apple이 정한 배포 통로라 피할 수 없다. 시험은 무료 길로 먼저 해서 "돌아가는가"를 보고, 배포 결정(연회비)은 그 뒤에 한다.

## 함정
- 무료 서명은 7일 뒤 앱이 열리지 않는다. 기록은 앱 안에 남지만, 앱을 지우고 다시 깔면 사라진다.
- 패드가 목표인 게임은 iOS에서 패드 다리 없이는 핵심 경험이 빠진다. 배포 전에 넣는다(위 "실제로 놓은 다리"). 넣어도 실기 확인은 서명한 앱으로만 된다.
- 공개 레포의 Actions 아티팩트는 GitHub 로그인한 누구나 받을 수 있다. 유료 에셋 팩이 들어간 빌드라면 라이선스와 맞는지 본다.

## 관련 노트
- [WASM 빌드와 JS 번들](wasm-build.md)
- [macroquad를 GitHub Actions에서 Android APK로](../../guides/macroquad-android-apk-github-actions.md)
- [게임패드와 Android 입력](gamepad-and-android-input.md)
