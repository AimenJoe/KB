---
title: macroquad 게임을 GitHub Actions에서 Android APK로 빌드하기 (cargo-quad-apk)
type: guide
tags: [macroquad, miniquad, android, apk, github-actions, ci-cd, rust]
status: verified
created: 2026-10-24
updated: 2026-10-24
verified: |
  1차 출처로 확인: cargo-quad-apk git master(커밋 d411c8f, 2026-07-28) 소스 — src/config.rs(NDK_HOME 필수, ANDROID_SDK_HOME→ANDROID_HOME,
  build-tools 중 가장 높은 버전 자동 선택, android_version 기본 36, min_sdk 기본 18), src/ops/build.rs(aapt2·d8·zipalign·javac -source/-target 1.8,
  ~/.android/debug.keystore를 keytool로 생성, apksigner 서명, `--nosign`), 산출물 경로 target/android-artifacts/<profile>/apk/<bin>.apk,
  miniquad 크레이트 소스의 java/MainActivity.java·QuadNative.java를 가져와 컴파일; Dockerfile(JDK17, cmdline-tools, platforms;android-36, NDK r25).
  actions/runner-images Ubuntu2404-Readme(build-tools 34~37, platforms android-34~37, NDK 27.3(기본)/29/30, JDK 17 기본, ANDROID_HOME·ANDROID_NDK_HOME 환경 변수).
  gamepads 0.1.7 소스: Android에서 android-winit feature 없이는 `poll_android_winit` 미정의로 컴파일 실패(`cargo check --target aarch64-linux-android`로 재현).
  CI 실행(2026-10-24, 러너 ubuntu-latest): 위 절차 그대로 첫 실행에 성공. 상세는 "확인 결과" 절.
  2차 출처만 있음: macroquad 공식 Android 글(macroquad.rs/articles/android, 이 세션에서 접속 불가)의 Docker 절차.
  확인 못 함: 실기 설치·실행. 디버그 키 서명 APK가 Android 14+ 기기에서 사이드로드되는지.
sources:
  - https://github.com/not-fl3/cargo-quad-apk
  - https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md
  - https://github.com/not-fl3/miniquad/tree/master/java
  - https://github.com/fornwall/gamepads
  - https://macroquad.rs/articles/android/
---

# macroquad 게임을 GitHub Actions에서 Android APK로 빌드하기

## 요약
macroquad(miniquad) 게임의 APK는 Gradle 없이 `cargo-quad-apk`로 만든다. 이 도구는 **crates.io 0.1.4는 오래됐지만 git master는 2025~2026에 갱신**되어(aapt2·d8, API 36, 명령줄 도구, NDK 29) 현재 SDK로 돌아간다. GitHub `ubuntu-latest` 러너에는 Android SDK·NDK·JDK가 전부 깔려 있으므로 **설치 단계 없이** `NDK_HOME`만 넘기면 된다. 로컬에 SDK/NDK를 두지 않고 CI에서만 빌드하는 쪽이 1인 개발에 맞다.

## 절차

### 1. Cargo.toml 메타데이터
```toml
[package.metadata.android]
package_name = "io.github.<user>.<game>"   # 기본값 rust.<bin>은 쓰지 말 것
label = "게임 이름"
android_version = 36        # compileSdk. 러너의 platforms/android-36/android.jar 필요
target_sdk_version = 36
min_sdk_version = 26
build_targets = ["aarch64-linux-android"]  # 기본은 armv7·aarch64·i686 세 개. 실기만이면 arm64로 줄여 시간 절약
fullscreen = true
version_code = 1            # 배포마다 증가

[package.metadata.android.activity_attributes]
"android:screenOrientation" = "sensorLandscape"
```

### 2. 워크플로
```yaml
on:
  push: { branches: ['**'], tags: ['v*'], paths: ['src/**', 'Cargo.toml', 'Cargo.lock', '.cargo/**', '.github/workflows/build-android.yml'] }
  workflow_dispatch:
env:
  CARGO_QUAD_APK_REV: d411c8fe1c08339e46d7dc6b40ac04ea5e3a01b6   # 커밋 고정
jobs:
  apk:
    runs-on: ubuntu-latest
    permissions: { contents: write }      # 태그 Release용
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with: { targets: aarch64-linux-android }
      - uses: Swatinem/rust-cache@v2
      - uses: actions/cache@v4             # cargo 크레이트를 컴파일하므로 첫 설치가 몇 분. 바이너리를 커밋 해시로 캐시
        id: cqa
        with: { path: ~/.cargo/bin/cargo-quad-apk, key: cargo-quad-apk-${{ runner.os }}-${{ env.CARGO_QUAD_APK_REV }} }
      - if: steps.cqa.outputs.cache-hit != 'true'
        run: cargo install --locked --git https://github.com/not-fl3/cargo-quad-apk --rev "$CARGO_QUAD_APK_REV"
      - run: |
          export NDK_HOME="$ANDROID_NDK_HOME"      # cargo-quad-apk는 NDK_HOME만 본다. ANDROID_HOME은 러너가 이미 설정
          cargo quad-apk build --release
      - uses: actions/upload-artifact@v4
        with: { name: apk, path: target/android-artifacts/release/apk/*.apk, if-no-files-found: error }
      - if: startsWith(github.ref, 'refs/tags/v')
        uses: softprops/action-gh-release@v2
        with: { files: target/android-artifacts/release/apk/*.apk }
```
- 태그 push에는 `paths` 필터가 적용되지 않으므로 `v*` 태그는 항상 빌드된다.
- 산출 APK는 `~/.android/debug.keystore`(없으면 keytool로 생성)로 서명된다. `adb install`·사이드로드용. 스토어 배포는 릴리스 키로 `apksigner`를 한 번 더 돌리거나 `--nosign` 뒤 직접 서명.

### 3. 커밋 전 로컬 검사
NDK 없이도 `rustup target add aarch64-linux-android && cargo check --target aarch64-linux-android`는 된다. Android에서만 깨지는 의존성을 CI 전에 잡는다.

## 왜?
- **Gradle 없이**: miniquad는 NativeActivity가 아니라 자체 `MainActivity.java`(+`QuadNative`)를 쓴다. cargo-quad-apk가 그 Java를 miniquad 크레이트 소스에서 찾아 `javac → d8 → aapt2 link → zipalign → apksigner` 순서로 묶는다. 일반 `cargo-apk`/`xbuild`는 NativeActivity 전제라 맞지 않는다.
- **CI에서만 빌드**: 러너 이미지가 SDK·NDK·JDK 버전을 관리해 준다. 로컬은 `cargo check`만.
- **커밋 고정**: 상류 master가 바뀌어 조용히 깨지는 것을 막는다. 올릴 때 CI 한 번 보고 올린다.

## 함정
- `gamepads` 크레이트(0.1.7)는 Android에서 `android-winit` feature 없이 **컴파일되지 않는다**. 그 feature는 winit 전용이라 miniquad에 못 쓴다. `[target.'cfg(not(target_os = "android"))'.dependencies]`로 옮기고 코드에 `cfg`를 둔다. Android 게임패드 자체는 miniquad 백엔드 공백([gamepad-and-android-input.md](../reference/macroquad/gamepad-and-android-input.md)).
- `NDK_HOME`을 안 넘기면 "Please set the path to the Android NDK with the $NDK_HOME environment variable". 러너 변수 이름은 `ANDROID_NDK_HOME`이다.
- build-tools는 **가장 높은 버전 디렉터리**를 고른다. 러너에 rc 버전이 있으면 그걸 집는다.
- `javac -source 1.8 -target 1.8 -bootclasspath android.jar`: JDK 17에서는 경고만, JDK 21+에서도 아직 허용. 러너 기본 JDK 17.
- 첫 `cargo install`은 `cargo` 크레이트 0.87을 통째로 컴파일한다. 캐시 없이는 매번 수 분.

## 확인 결과 (2026-10-24, nail-under-the-roots 첫 실행)
- 러너 `ubuntu-latest`, rustc 1.99.1, 캐시 없는 첫 실행: 전체 4분 46초(cargo-quad-apk 컴파일 포함). 바이너리 캐시 9.6MB 저장.
- `MainActivity.java` 컴파일에 deprecation 경고 9개(`setSystemUiVisibility` 등). 에러 없음.
- 산출물 `nail.apk` 455KB(`classes.dex` + `lib/arm64-v8a/libnail.so`), `zipalign` 검증 통과, `~/.android/debug.keystore`를 keytool로 새로 만들어 apksigner 서명(`nail.apk.idsig` 동봉). 아티팩트 zip 449KB.
- Android 전용 코드 경로 없이 `cargo check --target aarch64-linux-android`만 통과시킨 상태에서 바로 성공했다. 즉 macroquad 0.4.16 + audio feature는 Android에서 추가 설정 없이 링크된다(quad-snd는 OpenSL ES 백엔드).

## 관련 노트
- [reference/macroquad/gamepad-and-android-input.md](../reference/macroquad/gamepad-and-android-input.md)
- [guides/macroquad-wasm-netlify-github-actions.md](macroquad-wasm-netlify-github-actions.md)
- [reference/github-actions/rust-wasm-build.md](../reference/github-actions/rust-wasm-build.md)
