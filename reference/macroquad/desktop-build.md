---
title: macroquad PC 빌드 — Windows·macOS·Linux 묶음, 에셋 경로 함정, 서명
type: reference
tags: [macroquad, rust, github-actions, release, windows, macos, linux, steam]
status: draft
created: 2026-10-29
updated: 2026-11-10
verified: |
  1차(직접 실행, 2026-11-10, knellroot 0135): 모델(build.rs)·소리 wav·글꼴을 모두 `include_bytes!`로 넣은 게임은 리눅스 운영판을 작업 폴더 `/`에서
  Xvfb로 켜도 타이틀이 뜬다(에셋 경로 찾기 없음, 묶음 = 실행 파일 하나). miniquad 0.4.11 소스: `conf.fullscreen`은 X11(`linux_x11.rs`)·Windows·macOS 모두 시작 때 반영,
  X11 전체 화면은 창 관리자가 해 줘서 창 관리자 없는 Xvfb에서는 창 크기 그대로(확인 못 함 = 실기 몫). `Conf::icon` 기본은 miniquad 로고.
  Pillow 12 `.ico` `append_images`로 크기마다 따로 그린 그림을 넣음(16·32가 큰 그림을 줄인 것보다 또렷).
  1차 출처로 확인(2026-10-29, nail-under-the-roots 0240):
  - miniquad 소스 `fs.rs` `load_file_desktop`: 데스크톱은 `File::open(path)` — 경로가 상대면 "지금 작업 폴더" 기준이다.
    macroquad `set_pc_assets_folder`는 그 앞에 접두사만 붙인다(`format!("{pc_assets}/{path}")`).
  - 리눅스(x86_64)에서 `cargo check`·`cargo clippy --target x86_64-pc-windows-msvc`·`aarch64-apple-darwin` 통과(링크 없이).
  - 리눅스 빌드를 Xvfb에서 작업 폴더 `/`로 켜서, 실행 파일 기준 에셋 경로로 타이틀이 뜨는 것을 봄(소리 장치는 없음).
  - GitHub Actions: windows-latest(MSVC)·macos-latest(arm64 + x86_64 → lipo → 임시 서명, codesign --verify 통과) 빌드 성공.
    ubuntu-22.04는 처음에 실패 — gilrs의 libudev-sys가 `libudev-dev`(pkg-config `libudev`)를 요구.
  - Pillow 12로 .ico(16~256)·.icns(16~1024) 저장(리눅스에서).
  직접 해 봄(2026-11-05): 리눅스 운영판 `cargo build --release --no-default-features` → 4.9 MB, `ldd`·`strings`로 링크·dlopen 확인. 에셋 크기는 `du`.
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

### 다른 길 — 에셋을 바이너리에 넣기
- 그림·모델·소리·글꼴을 `include_bytes!`(또는 `build.rs`가 만든 표)로 실행 파일에 넣으면 **경로 문제 자체가 없다**: 실행 중 디스크를 읽지 않으니 바로가기·Finder·Steam 어디서 켜도 같고, 묶음은 실행 파일 하나 + 고지 파일(knellroot 0135 — 5.9MB, 웹 wasm도 같은 바이너리라 따로 받을 파일이 없다).
- 대가: 에셋이 크면 실행 파일·wasm이 커지고, 에셋 하나를 바꿔도 다시 컴파일한다. 음악처럼 큰 파일이 많으면 nail처럼 폴더에 두는 편이 낫다.
- 웹용 mp3·네이티브용 ogg처럼 플랫폼마다 다른 파일이 필요 없는 형식(wav)이면 더 쉽다.

### 창 ✕
- 기록을 "바뀔 때마다 + 임시 파일에 쓰고 이름 바꾸기"로 쓰는 게임이면 ✕로 꺼도 잃는 것이 없다 — `prevent_quit`가 필요 없다(knellroot 0135). 주기·장면 경계에서만 쓰는 게임은 아래 "PC에서만 필요한 것"대로 붙잡는다.

## OS마다
| | 빌드 | 묶음 | 함정 |
|---|---|---|---|
| Windows | windows-latest, `x86_64-pc-windows-msvc` | zip: `Game.exe` + assets | `#![windows_subsystem = "windows"]`(릴리스만) 안 하면 콘솔 창이 같이 뜬다. 아이콘은 빌드 의존성 없이 `rcedit --set-icon`. 서명 없으면 SmartScreen 경고 |
| macOS | macos-latest, `aarch64-apple-darwin` + `x86_64-apple-darwin` → `lipo -create` | `.app`(Info.plist, `Contents/Resources/assets`, `.icns`) → `ditto -c -k --keepParent` | lipo로 합치면 링커가 붙인 arm64 서명이 깨진다 → `codesign --force --deep -s -`(임시 서명)라도 다시. `Info.plist`에 `NSHighResolutionCapable`. 공증 없으면 첫 실행이 막힌다 |
| Linux | ubuntu-22.04(glibc를 낮게 → 오래된 배포판·SteamOS) | tar.gz | apt: `libx11-dev libxi-dev libgl1-mesa-dev libasound2-dev` + 패드(gilrs)를 쓰면 `libudev-dev` |

- 웹용 오디오(mp3)는 빼고 네이티브용(ogg)만 싣는다 — macroquad 네이티브(quad-snd)는 mp3를 못 푼다.
- 비공개 에셋 레포를 CI에서 체크아웃해 묶음에 넣는다면 `persist-credentials: false` + `.git` 지우기(토큰이 묶음에 남지 않게).

## 바이너리는 어떻게 생기고, 묶음 크기는 무엇이 정하나
- **C 라이브러리 없이 전부 Rust.** macroquad 아래의 miniquad가 창·입력·GL을 SDL·GLFW 없이 OS API로 직접 맡고, 글꼴(fontdue)·소리(quad-snd)·그림 디코더도 Rust 크레이트다. cargo가 전부를 **실행 파일 하나에 정적 링크**한다 — 같이 줄 DLL·런타임이 없다.
- **OS에 원래 있는 것만 쓴다.** 리눅스는 `ldd`에 libc·libm·libasound(소리)·libudev(패드 gilrs)만 보이고, X11·GL은 실행 때 `dlopen`으로 찾는다(바이너리 문자열에 `libGL.so`·`libXi.so`). Windows는 시스템 DLL, macOS는 시스템 프레임워크.
- **에셋은 바이너리에 넣지 않는 게 기본**이다. 실행 파일 옆 `assets`에서 읽고(위 "에셋 경로"), `include_bytes!`·`include_str!`로 박는 것만 바이너리에 들어간다.
- **그래서 묶음 크기는 에셋이 정한다.** OS마다 실행 파일만 다르고 에셋은 똑같이 들어가니 세 OS 묶음·APK가 거의 같은 크기가 된다. ogg·png는 이미 압축돼 있어 zip이 거의 못 줄인다. 줄이려면 코드가 아니라 음악(비트레이트·곡 수)을 본다.
  - 숫자(nail-under-the-roots v0.9.1, 2026-11-05): 리눅스 운영판 실행 파일 4.9 MB(`opt-level = "z"` + `lto = true` + `codegen-units = 1`, 직접 빌드), 묶기 전 에셋 34 MB(CI 로그 `34M stage/assets` — 음악 ogg 27곡 약 31 MB), Release 묶음 Linux 35.3 · Windows 35.0 · macOS 36.8 · APK 36.0 MB.
  - macOS가 조금 큰 것은 arm64 + x86_64 두 실행 파일을 `lipo`로 합친 겸용이라서. 웹은 같은 그림 + mp3를 따로 받는다(네이티브는 mp3를 못 푼다, 위).
  - 확인 못 함: Windows·macOS 실행 파일 자체의 크기(묶음 크기로만 미루어 봄).

## PC에서만 필요한 것
- 타이틀 "끝내기"(`miniquad::window::order_quit`), 전체 화면 토글(`set_fullscreen`, F11 — 키 배치 밖에 둔다), 다음에 켤 때 기억(설정 칸 → 시작 `conf.fullscreen`), 창 아이콘(`Conf::icon` — 안 주면 miniquad 로고) — 웹·모바일 빌드에서는 숨긴다(`cfg!(not(any(wasm32, android, ios)))`).
- 창 ✕로 닫을 때 저장: `prevent_quit()`로 닫기를 붙잡고 `is_quit_requested()`가 오면 런을 적은 뒤 `order_quit()`(nail 0264). 안 하면 ✕가 저장 없이 끝낸다.

## 비용·서명
- macOS 러너는 분당 리눅스의 약 10배 → main push마다가 아니라 개발 갈래(`release/**`) push·릴리스·손으로만([공개 레포를 비공개로](../github-actions/public-to-private-repo.md)).
- macOS 공증: Apple Developer($99/년) → Developer ID 인증서 + `notarytool`(App Store Connect API 키)를 CI 시크릿으로.
- iOS는 [macroquad iOS 빌드](ios-build.md), Android는 [게임패드·Android 입력](gamepad-and-android-input.md).
