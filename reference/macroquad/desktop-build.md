---
title: macroquad PC 빌드 — Windows·macOS·Linux 묶음, 에셋 경로 함정, 서명
type: reference
tags: [macroquad, rust, github-actions, release, windows, macos, linux, steam]
status: draft
created: 2026-10-29
updated: 2026-10-29
verified: |
  1차 출처로 확인(2026-10-29, nail-under-the-roots 0240):
  - miniquad 소스 `fs.rs` `load_file_desktop`: 데스크톱은 `File::open(path)` — 경로가 상대면 "지금 작업 폴더" 기준이다.
    macroquad `set_pc_assets_folder`는 그 앞에 접두사만 붙인다(`format!("{pc_assets}/{path}")`).
  - 리눅스(x86_64)에서 `cargo check`·`cargo clippy --target x86_64-pc-windows-msvc`·`aarch64-apple-darwin` 통과(링크 없이).
  - 리눅스 빌드를 Xvfb에서 작업 폴더 `/`로 켜서, 실행 파일 기준 에셋 경로로 타이틀이 뜨는 것을 봄(소리 장치는 없음).
  - GitHub Actions: windows-latest(MSVC)·macos-latest(arm64 + x86_64 → lipo → 임시 서명, codesign --verify 통과) 빌드 성공.
    ubuntu-22.04는 처음에 실패 — gilrs의 libudev-sys가 `libudev-dev`(pkg-config `libudev`)를 요구.
  - Pillow 12로 .ico(16~256)·.icns(16~1024) 저장(리눅스에서).
  확인 못 함: Windows·Mac 실기에서 실행(화면·소리·패드·전체 화면), Steam 경유 설치의 격리(quarantine) 여부, Steam의 공증 요구.
  2차 출처만 있음: macOS 15(Sequoia)는 격리 표시가 붙은 공증 없는 앱의 첫 실행을 막고 "개인정보 보호 및 보안 → 그래도 열기"로 연다(Eclectic Light).
  Apple 문서: Developer ID 배포는 공증을 받아야 한다(1차, 다만 Steam 경유 규칙은 Valve 문서를 못 찾음).
sources:
  - https://github.com/not-fl3/miniquad
  - https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution
  - https://eclecticlight.co/2024/08/10/gatekeeper-and-notarization-in-sequoia/
  - https://github.com/electron/rcedit
---

# macroquad PC 빌드

## 요약
macroquad(miniquad)는 Windows·macOS·Linux를 원래 지원해 코드 변경은 거의 없다. 막히는 곳은 **에셋 경로**(데스크톱은 작업 폴더 기준으로 읽는다)와 **묶음·서명**(macOS `.app`, 겸용 바이너리, 공증)이다. CI에서 세 OS 러너로 하루 안에 묶음까지 나온다.

## 에셋 경로 — 가장 먼저 고칠 것
- `set_pc_assets_folder("assets")`는 **상대 경로**다. 터미널에서 레포 폴더로 `cargo run` 할 때만 맞는다.
  바로가기·Finder·Steam으로 켜면 작업 폴더가 실행 파일 자리가 아니라(macOS Finder는 `/`) 그림·소리를 못 찾는다.
- 고치기: 시작할 때 `std::env::current_exe()`의 폴더에서 찾아 **절대 경로**를 넘긴다.
  - Windows·Linux 묶음: `<exe 폴더>/assets`
  - macOS `.app`: `<exe 폴더>/../Resources/assets`(`Contents/MacOS/게임` → `Contents/Resources`)
  - 둘 다 없으면 `assets`(개발 중 `cargo run`).
- 저장 자리는 따로: `%APPDATA%`, `~/Library/Application Support`, `$XDG_DATA_HOME` 또는 `~/.local/share`.

## OS마다
| | 빌드 | 묶음 | 함정 |
|---|---|---|---|
| Windows | windows-latest, `x86_64-pc-windows-msvc` | zip: `Game.exe` + assets | `#![windows_subsystem = "windows"]`(릴리스만) 안 하면 콘솔 창이 같이 뜬다. 아이콘은 빌드 의존성 없이 `rcedit --set-icon`. 서명 없으면 SmartScreen 경고 |
| macOS | macos-latest, `aarch64-apple-darwin` + `x86_64-apple-darwin` → `lipo -create` | `.app`(Info.plist, `Contents/Resources/assets`, `.icns`) → `ditto -c -k --keepParent` | lipo로 합치면 링커가 붙인 arm64 서명이 깨진다 → `codesign --force --deep -s -`(임시 서명)라도 다시. `Info.plist`에 `NSHighResolutionCapable`. 공증 없으면 첫 실행이 막힌다 |
| Linux | ubuntu-22.04(glibc를 낮게 → 오래된 배포판·SteamOS) | tar.gz | apt: `libx11-dev libxi-dev libgl1-mesa-dev libasound2-dev` + 패드(gilrs)를 쓰면 `libudev-dev` |

- 웹용 오디오(mp3)는 빼고 네이티브용(ogg)만 싣는다 — macroquad 네이티브(quad-snd)는 mp3를 못 푼다.
- 비공개 에셋 레포를 CI에서 체크아웃해 묶음에 넣는다면 `persist-credentials: false` + `.git` 지우기(토큰이 묶음에 남지 않게).

## PC에서만 필요한 것
- 타이틀 "끝내기"(`miniquad::window::order_quit`), 전체 화면 토글(`set_fullscreen`, F11) — 웹·모바일 빌드에서는 숨긴다(`cfg!(not(any(wasm32, android, ios)))`).

## 비용·서명
- macOS 러너는 분당 리눅스의 약 10배 → main push마다가 아니라 릴리스·손으로만([공개 레포를 비공개로](../github-actions/public-to-private-repo.md)).
- macOS 공증: Apple Developer($99/년) → Developer ID 인증서 + `notarytool`(App Store Connect API 키)를 CI 시크릿으로.
- iOS는 [macroquad iOS 빌드](ios-build.md), Android는 [게임패드·Android 입력](gamepad-and-android-input.md).
