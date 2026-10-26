---
title: macroquad iOS 빌드 — GitHub Actions macOS 러너로 서명 안 한 .ipa, 기기 시험·배포의 갈림길
type: reference
tags: [macroquad, ios, rust, github-actions, release]
status: draft
created: 2026-10-26
updated: 2026-10-26
verified: |
  1차 출처로 확인(2026-10-26, nail-under-the-roots 0086):
  - miniquad 0.4.11 소스: native/ios.rs(Metal·GLES), fs::load_file이 iOS에서 NSBundle mainBundle pathForResource로 읽음. README의 iOS 절(.app + Info.plist).
  - quad-snd 0.2.8: macOS·iOS에 CoreAudio.
  - gilrs-core 0.5.15에 iOS 플랫폼 없음(linux·macos·wasm·windows·default) → gamepads 크레이트가 iOS에서 빈 백엔드.
  - 리눅스에서 `cargo check --release --target aarch64-apple-ios` 통과.
  - GitHub Actions macos-latest에서 cargo build --release --target aarch64-apple-ios 성공: Mach-O 64-bit arm64, plutil -lint OK, 13.9MB .ipa(서명 안 함).
  확인 못 함: 실기에서 실행(화면·터치·소리·저장), 서명 후 설치.
  2차 출처만 있음: 서명 없는 앱은 시뮬레이터에서만, 무료 Apple ID 서명 7일·앱 3개(AltStore·SideStore), Developer Program 1년·TestFlight,
  공개 레포 macOS 러너 무료(비공개는 분당 과금·배수), CI에서 Xcode 자동 서명이 어렵다(인증서·프로필을 Secrets로 또는 fastlane match), EU 대체 마켓.
  macroquad.rs/articles/ios 문서는 세션에서 접속이 안 되어 못 읽었다.
sources:
  - https://github.com/not-fl3/miniquad
  - https://docs.github.com/en/actions/reference/github-hosted-runners-reference
  - https://github.blog/changelog/2026-02-26-macos-26-is-now-generally-available-for-github-hosted-runners/
  - https://blog.codemagic.io/why-github-actions-not-built-for-mobile-cicd
  - https://theapplewiki.com/wiki/AltStore
  - https://dev.to/1_king_0b1e1f8bfe6d1/how-ios-sideloading-actually-works-in-2025-dev-certs-altstore-and-the-eu-exception-1m2h
---

# macroquad iOS 빌드

## 요약
macroquad(miniquad)는 iOS를 지원한다. Xcode 프로젝트 없이 `cargo build --target aarch64-apple-ios`로 빌드한 실행 파일에 손으로 만든 `.app`(Info.plist·assets·아이콘)을 둘러, macOS 러너에서 **서명 안 한 .ipa**를 만든다. 실기에 올리려면 서명이 필요하다. 시험은 무료 Apple ID로(7일), 배포는 Developer Program($99/년)으로 한다. 게임패드는 gilrs에 iOS가 없어 따로 다리가 필요하다.

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

### 앱 안 저장 자리
- HOME은 샌드박스다. 쓸 수 있는 곳은 `Documents`·`Library`·`tmp` 아래뿐이다. 리눅스식 `~/.local/share`는 안 된다 → macOS와 같은 `~/Library/Application Support/<앱>`.

### 서명 갈림길(2차)
| 길 | 비용 | 기간 | 용도 |
|---|---|---|---|
| 서명 없음 | 0 | — | 시뮬레이터만 |
| 무료 Apple ID + Sideloadly·AltStore·SideStore | 0 | 7일마다 다시 서명, 앱 3개 | 내 기기 시험 |
| Apple Developer Program + CI codesign(.p12·프로필·App Store Connect API 키를 Secrets로) | $99/년 | 1년 | TestFlight·App Store |
| EU 대체 마켓 | 개발자 계정 필요 | — | EU 안에서만(규칙 재확인) |

### 게임패드
- `gamepads` → gilrs는 iOS 백엔드가 없다(빈 백엔드, 컴파일은 된다).
- Apple `GameController`(`GCController`)를 잇는 작은 다리가 필요하다. Android 패치처럼 키 코드로 넘기면 게임 쪽 입력 코드는 그대로 둘 수 있다.

## 왜?
- Xcode 프로젝트를 두지 않으면 레포에 생성물이 없고, 리눅스 개발자도 CI만으로 빌드한다. macroquad가 Objective-C 호출을 코드 안에서 다 하므로 .app은 파일 몇 개로 충분하다.
- 서명은 Apple이 정한 배포 통로라 피할 수 없다. 시험은 무료 길로 먼저 해서 "돌아가는가"를 보고, 배포 결정(연회비)은 그 뒤에 한다.

## 함정
- 무료 서명은 7일 뒤 앱이 열리지 않는다. 기록은 앱 안에 남지만, 앱을 지우고 다시 깔면 사라진다.
- 패드가 목표인 게임은 iOS에서 패드 다리 없이는 핵심 경험이 빠진다. 배포 전에 넣는다.
- 공개 레포의 Actions 아티팩트는 GitHub 로그인한 누구나 받을 수 있다. 유료 에셋 팩이 들어간 빌드라면 라이선스와 맞는지 본다.

## 관련 노트
- [WASM 빌드와 JS 번들](wasm-build.md)
- [macroquad를 GitHub Actions에서 Android APK로](../../guides/macroquad-android-apk-github-actions.md)
- [게임패드와 Android 입력](gamepad-and-android-input.md)
