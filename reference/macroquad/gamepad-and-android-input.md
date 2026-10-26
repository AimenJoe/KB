---
title: macroquad 게임패드와 Android 입력 현황
type: reference
tags: [macroquad, miniquad, gamepad, android, input, touch, rust]
status: verified
created: 2026-10-24
updated: 2026-10-26
verified: |
  1차 출처로 확인: miniquad master의 java/MainActivity.java(onTouch/onKey만 구현, onGenericMotionEvent 없음),
  src/native/android.rs(surfaceOnKeyDown/Up → keycodes::translate_keycode), src/native/android/keycodes.rs(109개 매핑,
  0x60~0x6e 게임패드 버튼 미매핑); gamepads 0.1.7의 README·Cargo.toml(features: wasm-bindgen 기본, android-winit;
  gilrs는 non-android/non-wasm 전용); developer.android.com KeyEvent 상수값(BUTTON_A=96 등); gilrs docs.rs 지원표(Android ✕).
  직접 빌드·실행(2026-10-24, gamepads 0.1.7 + macroquad 0.4.16, rustc 1.99.1): Linux 데스크톱 빌드는 gilrs→libudev-sys 때문에 `libudev-dev`·`pkg-config`가
  필요하다. 웹 빌드는 `--import-undefined` 링커 플래그가 필요했다(wasm-build.md). 플러그인 JS의 `version:"0.1.7"`(문자열)과 크레이트의
  `gamepads_crate_version()`(정수 65543)이 달라 mq_js_bundle이 "version mismatch"를 찍는 것을 헤드리스 Chromium 콘솔로 확인.
  소스 확인: js/gamepads-src-0.1.js(스틱 y 부호 반전, 데드존 0.04 재매핑), src/backend_gilrs.rs(gilrs 축 그대로, 드라이버 데드존 사용),
  src/lib.rs(웹 is_just_pressed는 직전 poll과 비교).
  터치(2026-10-25): macroquad src/window.rs·src/input.rs·src/lib.rs(touches()는 물리 픽셀, screen_width()·mouse_position()은 DPI로 나눔,
  프레임 끝 위상 정리)를 읽고, Pixel 7 프로필(DPR 2.625) 헤드리스 Chromium에서 버튼 판정 실패를 재현한 뒤 DPI 나눗셈으로 해결 확인.
  실기 Android 13 브라우저에서 사용자가 같은 증상을 보고했고, DPI 나눗셈·비표준 매핑 허용 뒤 터치와 패드 모두 동작함을 확인(2026-10-25).
  2차 출처만 있음: macroquad 문서의 "gamepads soon" 문구, cargo-quad-apk 유지보수 상태(crates.io 0.1.4가 4년 이상 전,
  커뮤니티 이슈의 NDK/minSdk 패치 메모).
  메뉴 스틱 탐색(2026-10-25, nail-under-the-roots): "첫 칸은 키·D패드 눌림 에지, 스틱은 반복만" 구조에서 스틱 플릭이 무시되는 것을
  실기 사용자가 보고 → 스틱도 첫 칸을 내게 바꾸고(히스테리시스 0.5/0.3, 큰 축 하나) 가짜 Gamepad 헤드리스 Chromium에서 플릭 1회 = 1칸 확인.
  임계값 0.5/0.3 자체는 2차 출처(포럼의 "임계 통과 시 1회, 중앙 복귀 후 재무장" 패턴) + 직접 조정이며 표준값은 찾지 못했다.
  Android 버튼 패치(2026-10-26, nail-under-the-roots 0075): miniquad 0.4.11 사본을 `[patch.crates-io]`로 쓰고 keycodes.rs에
  0x60~0x6e 가운데 13개(BUTTON_C 0x62·BUTTON_Z 0x65는 뺌) → KeyCode::F13~F25 열세 줄을 넣었다(게임은 F13~F24 열둘을 읽고 MODE→F25는 안 쓴다). `cargo check --target aarch64-linux-android`·cargo-quad-apk 빌드 통과, 패치 표와
  게임 쪽 매핑이 같은지는 단위 테스트로 확인. 실기 패드에서 버튼이 다 듣는 것을 사용자가 확인했다(2026-10-26, 기기 모델·Android 버전 기록 없음).
  "패치 전에도 왼쪽 스틱은 움직였다"(실기 사용자 보고, v0.1.5) → AOSP frameworks/base ViewRootImpl.java의 SyntheticInputStage·
  SyntheticJoystickHandler를 읽고 확인: 앱이 처리하지 않은 조이스틱 MotionEvent의 AXIS_X/Y·AXIS_HAT_X/Y를 KEYCODE_DPAD_* 키
  이벤트로 바꿔 다시 넣는다(축마다 따로라 대각선도 됨, 누르고 있으면 반복).
  확인 못 함: Android MotionEvent 축 상수(AXIS_X/Y/Z/RZ/HAT_X/HAT_Y/LTRIGGER/RTRIGGER)의 정확한 숫자값 — 패치 시 공식 문서로 확인.
sources:
  - https://www.smashingmagazine.com/2012/02/finger-friendly-design-ideal-mobile-touchscreen-target-sizes/
  - https://www.uxpin.com/studio/blog/responsive-design-touch-devices-key-considerations/
  - https://uxmovement.com/?p=5043
  - https://github.com/not-fl3/miniquad/blob/master/java/MainActivity.java
  - https://github.com/not-fl3/miniquad/blob/master/src/native/android.rs
  - https://github.com/not-fl3/miniquad/blob/master/src/native/android/keycodes.rs
  - https://github.com/fornwall/gamepads/blob/main/README.md
  - https://docs.rs/crate/gilrs/^0.10.2
  - https://developer.android.com/reference/android/view/KeyEvent
  - https://github.com/aosp-mirror/platform_frameworks_base/blob/main/core/java/android/view/ViewRootImpl.java
  - https://developer.android.com/training/game-controllers/controller-input
  - https://github.com/not-fl3/cargo-quad-apk
  - https://macroquad.rs/articles/android/
  - https://github.com/BunnyEncoder20/king-tongue-2/issues/2
  - https://forum.babylonjs.com/t/how-to-use-the-gamepads-left-analog-to-navigate-a-game-menu-screen/40099
  - https://www.shawnhargreaves.com/blog/gamepads-suck.html
---

# macroquad 게임패드와 Android 입력 현황

## 요약
macroquad(0.4.16)/miniquad(0.4.11)에는 게임패드 API가 없다. 데스크톱·웹은 `gamepads` 크레이트로 메꿀 수 있지만 **Android에서는 그 크레이트도 동작하지 않고, miniquad Android 백엔드는 스틱·트리거 축을 받지 않으며 게임패드 버튼 키코드도 매핑하지 않는다.** 그래서 손대지 않은 APK에서는 D패드와 (Android가 D패드 키로 바꿔 주는) 왼쪽 스틱만 움직이고 버튼은 하나도 듣지 않는다. 버튼만이라면 `keycodes.rs` 열세 줄 패치로 된다(아래). 아날로그 스틱·오른쪽 스틱·트리거 축까지는 Java를 고쳐야 한다(약 200줄).

## 플랫폼별 현황

| 플랫폼 | 게임패드 경로 | 상태 |
|---|---|---|
| 데스크톱 | `gamepads` 크레이트 → gilrs 0.10 | 동작. 추가 설정 없음 |
| 웹 | `gamepads` 크레이트(`default-features = false`) → 브라우저 Gamepad API, JS 플러그인 로드 필요 | 동작. 플러그인 JS를 레포에 복사해 배포 |
| Android | 없음(원본) / `keycodes.rs` 패치 | 원본: **D패드 + 왼쪽 스틱(디지털, Android가 D패드 키로 바꿈)만.** 버튼 전부 버려짐. 패치: 버튼도 키로. 아날로그 축은 여전히 없음 |

## 데스크톱·웹: `gamepads` 크레이트

```toml
gamepads = { version = "0.1", default-features = false }  # macroquad는 wasm-bindgen을 안 쓰므로 끈다
```
```html
<script src="mq_js_bundle.js"></script>
<script src="macroquad-gamepads-0.1.js"></script>  <!-- fornwall.github.io 핫링크 대신 레포 복사본 -->
<script>load("game.wasm");</script>
```
- 매 프레임 `gamepads.poll()` 후 `all()`로 순회. 버튼, 좌우 스틱, 웹에서는 진동(dual rumble)까지.
- 플러그인 JS의 실제 경로는 `https://fornwall.github.io/gamepads/js/macroquad-gamepads-0.1.js`(`js/` 포함). 레포 `js/` 폴더에 minified 본과 `gamepads-src-0.1.js` 원본이 있다.

### 실제로 붙여 보니 (0.1.7)
- **버전 표기 불일치**: JS 플러그인은 `version:"0.1.7"`, 크레이트는 `(major<<24)+(minor<<16)+patch` = 65543을 export. mq_js_bundle은 `!=`로 비교해 매 로드마다 `Plugin gamepads version mismatch` 에러를 찍는다(동작에는 영향 없음). 복사본의 숫자를 65543으로 고치면 사라진다.
- **스틱 y 부호**: 두 백엔드 모두 **위가 +**다. 브라우저 Gamepad API는 위가 −인데 플러그인 JS가 축 1·3의 부호를 뒤집고, gilrs도 위가 +. 화면 좌표(아래가 +)로 쓰려면 `-y`.
- **데드존**: 웹 플러그인이 0.04 데드존을 빼고 0..1로 다시 편다. 데스크톱은 gilrs가 드라이버 데드존을 쓴다. 게임 쪽에서 반지름 데드존(0.2 정도)을 한 번 더 두는 편이 안전하다.
- **눌림(edge)**: 웹의 `is_just_pressed`는 "직전 `poll()` 때 안 눌렸고 지금 눌림"이므로 `poll()`은 프레임당 정확히 한 번. 고정 타임스텝이면 눌림을 래치에 모아 틱이 소비한다([concepts/fixed-timestep-and-hitstop.md](../../concepts/fixed-timestep-and-hitstop.md)).
- **비표준 매핑 패드는 통째로 무시된다**: 플러그인 JS는 `gamepad.mapping !== "standard"`이면 그 패드를 연결 안 된 것으로 기록한다. Android Chrome의 블루투스 패드·핸드헬드 내장 패드는 `mapping`이 `""`인 경우가 많아 "컨트롤러가 전혀 안 먹는" 증상이 된다(2026-10-25, 가짜 `navigator.getGamepads`로 재현: standard면 인식, ""면 pads 0). 복사본에서 그 조건을 빼면 표준 인덱스 가정으로 받는다. 어떤 패드가 어떻게 잡히는지는 https://hardwaretester.com/gamepad 로 본다.
- **브라우저는 버튼을 한 번 눌러야 패드를 노출한다**: Gamepad API는 사용자 제스처 전까지 `getGamepads()`에 패드를 넣지 않는다. 페이지를 연 뒤 아무 버튼이나 눌러야 한다.
- **Standard Gamepad 매핑 인덱스**: `Button` enum 순서 = W3C 표준 인덱스. ActionDown(0, A/×) ActionRight(1, B/○) ActionLeft(2, X/□) ActionUp(3, Y/△) FrontLeftUpper(4, L1) FrontRightUpper(5, R1) FrontLeftLower(6, L2) FrontRightLower(7, R2) LeftCenterCluster(8, Select) RightCenterCluster(9, Start) LeftStick(10) RightStick(11) DPad Up/Down/Left/Right(12~15) Mode(16). 웹은 `mapping === "standard"`인 패드만 보고한다.
- **Linux 데스크톱 빌드 의존성**: gilrs → libudev-sys → `libudev-dev`, `pkg-config`. 없으면 build.rs가 "Package libudev was not found"로 실패.
- Cargo.toml의 `android-winit` feature는 winit 0.30 + `android-native-activity` 전용이다. miniquad는 winit을 쓰지 않으므로 **macroquad Android 빌드에서는 쓸 수 없다.** gilrs 자체도 Android 미지원.

## Android: miniquad 백엔드가 받는 것

- `MainActivity.java`는 `View.OnTouchListener`, `View.OnKeyListener`만 구현한다. `onKey`는 `ACTION_DOWN/UP`의 `keyCode`를 `QuadNative.surfaceOnKeyDown/Up(keyCode)`로 넘기고 `true`를 돌려준다(시스템이 먹지 않는다). **`onGenericMotionEvent`가 없어 조이스틱 축 값은 앱에 오지 않는다.**
- 대신 Android 프레임워크가 처리되지 않은 조이스틱 `MotionEvent`를 D패드 키로 바꿔 준다. `ViewRootImpl`의 `SyntheticInputStage` → `SyntheticJoystickHandler`가 `AXIS_X/Y`(왼쪽 스틱)와 `AXIS_HAT_X/Y`를 `KEYCODE_DPAD_LEFT/RIGHT/UP/DOWN` 키 이벤트로 만든다(AOSP 소스 확인). 그래서 원본 miniquad에서도 왼쪽 스틱이 화살표 키처럼 움직인다. 축마다 따로라 대각선도 되지만, 세기가 없는 디지털 8방향이다. 오른쪽 스틱(`AXIS_Z/RZ`)과 트리거 축은 바뀌지 않는다.
- `android.rs`의 JNI 진입점은 `keycodes::translate_keycode`로 변환해 `Message::KeyDown/KeyUp`을 보낸다.
- `keycodes.rs` 매핑(109개) 중 게임패드 관련: `0x13~0x16 DPAD_UP/DOWN/LEFT/RIGHT → KeyCode::Up/Down/Left/Right`, `0x17 DPAD_CENTER → Enter`. **`0x60~0x6e`(BUTTON_A~BUTTON_MODE)는 없음** → 미지의 키로 떨어진다.

Android 게임패드 버튼 키코드(공식 문서 확인값): `BUTTON_A 96(0x60)`, `BUTTON_B 97`, `BUTTON_X 99`, `BUTTON_Y 100`, `BUTTON_L1 102`, `BUTTON_R1 103`, `BUTTON_START 108`, `BUTTON_SELECT 109`, `DPAD_UP 19(0x13)`.

## Android 컨트롤러를 지원하려면 (패치 범위)

1. **버튼**(해 봄, 2026-10-26): `keycodes.rs`에 `0x60~0x6e` 가운데 C·Z를 뺀 13개 매핑 추가. miniquad `KeyCode`에 게임패드 버튼 variant가 없으므로 데스크톱 키보드에 없는 `F13~F25`에 대응시켰다(가장 작은 패치, 열세 줄). 방법:
   - crates.io 원본을 레포(`third_party/miniquad`)에 복사하고 루트 `Cargo.toml`에 `[patch.crates-io] miniquad = { path = "third_party/miniquad" }`. 버전 번호가 같아야 patch가 먹는다.
   - cargo-quad-apk는 miniquad 패키지 폴더에서 `java/MainActivity.java`를 가져가므로, patch를 쓰면 사본의 Java가 들어간다(Java를 고칠 때도 같은 자리).
   - 경로 의존성은 `--cap-lints`가 안 걸려 원본의 경고가 clippy 출력에 섞인다 → 사본 `lib.rs` 맨 위 `#![allow(warnings)]`.
   - 게임 쪽은 Android에서만 `is_key_pressed(KeyCode::F13)` 등을 패드 버튼으로 읽는다. 패치 표와 게임 쪽 표가 어긋나지 않게 `include_str!`로 패치 파일을 읽는 단위 테스트를 둔다.
   - Android에서는 화살표 키도 "패드"로 세야 화면 안내 글이 키보드 글자로 바뀌지 않는다. 기기 뒤로 키는 `KEYCODE_BACK`(0x04) → `KeyCode::Back`.
2. **축**: `MainActivity.java`에 `onGenericMotionEvent` 추가 → `SOURCE_JOYSTICK`이면 `AXIS_X/Y`(좌 스틱), `AXIS_Z/RZ`(우 스틱), `AXIS_HAT_X/Y`(D-pad 아날로그), `AXIS_LTRIGGER/RTRIGGER`를 JNI로 전달 → `android.rs`에 진입점과 새 `Message` → `EventHandler`에 콜백.
3. **빌드**: `cargo-quad-apk`는 crates.io 0.1.4가 4년 이상 전 릴리스지만 **git master는 2025~2026에 갱신**됐다(API 36, aapt2·d8, NDK 29). 커밋을 고정해 설치하면 GitHub 러너 내장 SDK/NDK로 바로 빌드된다 → [guides/macroquad-android-apk-github-actions.md](../../guides/macroquad-android-apk-github-actions.md).
4. **`gamepads` 크레이트는 Android 빌드에서 빼야 한다**: 0.1.7은 `android-winit` feature 없이 `poll_android_winit` 미정의로 컴파일 실패(2026-10-24 `cargo check --target aarch64-linux-android`로 재현). non-Android 전용 의존성으로 두고 코드에 `cfg(not(target_os = "android"))`.

합쳐서 Java·Rust 200줄 안팎이지만 **miniquad 포크를 유지**하게 된다. 버튼(1)만 먼저 하고, 아날로그가 필요하다고 느낄 때 축(2)을 하는 순서가 싸다. 왼쪽 스틱은 프레임워크가 D패드 키로 바꿔 주므로 메뉴·이동은 버튼 패치만으로 된다.

## 터치 (웹·모바일 브라우저)
macroquad 0.4.16의 `touches()`는 `Touch { id, phase, position }`를 돌려준다. 실제로 붙여 보고 확인한 함정 두 가지(2026-10-25, Pixel 7 프로필 헤드리스 Chromium과 실기 Android 13 브라우저):
- **좌표 단위 불일치**: `screen_width()`·`mouse_position()`은 `miniquad::window::dpi_scale()`로 나눈 논리 픽셀을 주지만, `touches()`의 `position`은 **물리 픽셀 그대로**다(src/window.rs, src/input.rs 확인). `high_dpi: true`인 고해상도 폰(DPR 2~3)에서는 터치 좌표가 화면 크기의 2~3배로 들어와 버튼 판정이 전부 빗나간다. `t.position / screen_dpi_scale()`로 맞춘다. DPR 1인 데스크톱·헤드리스에서는 재현되지 않으므로 테스트할 때 `deviceScaleFactor`를 올려야 한다.
- **위상(phase)에 기대지 말 것**: macroquad는 터치를 id별로 하나만 보관하고 프레임 끝에 Started/Moved→Stationary, Ended→삭제로 정리한다. 실제 손가락은 touchstart 직후 같은 프레임에 touchmove가 와서 Started가 Moved로 덮이고, 짧은 탭은 start·end가 한 프레임에 들어와 Ended만 보인다. "눌림"은 **지난 프레임까지 본 id 목록에 없는 새 id**로 판정하고, 새 id가 Ended여도 눌림으로 센다.
- 웹 글루는 `touchstart/move/end/cancel`을 `canvas`에 걸고 `e.changedTouches`의 `identifier`를 id로 넘긴다. `simulate_mouse_with_touch`(기본 true)라 마우스 이벤트도 같이 생긴다.
- **버튼 크기**: 플랫폼 최소 터치 크기(Apple 44pt, Material 48dp)는 바닥일 뿐이다. 게임은 엄지로 누르고(성인 엄지 폭 약 1인치), 가장 자주 누르는 버튼(공격)은 다른 버튼보다 확실히 크게 — 짧은 변 기준 비율로 정하면 기기마다 맞는다(예: 공격 지름 ≈ 짧은 변의 27%, 가로 폰에서 약 100pt). 나머지는 엄지가 쉬는 오른쪽 아래 둘레 호에. 배치는 순수 함수(폭, 높이) → 버튼 목록으로 빼서 "겹치지 않음·화면 안·공격이 가장 큼"을 여러 화면 크기로 테스트한다. 엄지 크기 출처는 2차(UX 글), 게임 버튼 크기 표준 문서는 못 찾았다.
- `index.html`에 `touch-action: none; overscroll-behavior: none; user-select: none`과 `user-scalable=no` viewport를 두지 않으면 스크롤·확대·길게 누르기 메뉴가 끼어든다.

## 메뉴 탐색: 스틱을 한 칸 눌림으로
게임플레이는 스틱 벡터를 그대로 쓰지만, 메뉴는 "한 칸" 눌림이 필요하다. 키·D패드는 눌림 에지(`is_key_pressed`, `is_just_pressed`)가 있고 **아날로그 스틱에는 없다.**
- 함정: "첫 칸은 버튼 에지, 반복은 이동 벡터"로 짜면 스틱은 반복 지연(예 0.35초)만큼 누르고 있어야 겨우 움직인다. 사용자는 "왼쪽 스틱이 무시된다"고 느낀다.
- 패턴: 이동 벡터(키·D패드·스틱 합친 것)에서 방향을 만들고, **방향이 새로 잡히는 순간 한 칸**, 누르고 있으면 지연 뒤 일정 간격으로 반복. 키 에지와 같은 프레임에 겹치면 OR이라 한 칸이다.
- 스틱은 **큰 축 하나**만 본다(대각선 = 큰 쪽). 메뉴 축은 서로 독립이다(Hargreaves의 축별 데드존 논의).
- **히스테리시스**: 잡는 임계(0.5)와 푸는 임계(0.3)를 다르게. 경계에서 손이 떨려도 한 칸만 나간다. 중앙(0.3 밑)으로 돌아와야 다시 잡힌다.
- 데드존을 뺀(0..1로 다시 편) 값에 임계를 건다. 데드존 없이 메뉴 경로를 짜면 스틱 드리프트로 커서가 저절로 움직인다(RetroPie·UE 보고).

## 설계 함의
- 코드가 `KeyCode`를 직접 보지 않고 **액션(`Attack`, `Dodge`, `Move(Vec2)`)** 을 보게 입력 레이어를 처음부터 둔다. 키보드·`gamepads`·Android 패치가 전부 이 뒤에 들어간다.
- UI는 커서 없이 동작하게(좌우 이동 + 확인) 처음부터 설계한다.

## 관련 노트
- [reference/rust-game-engines/web-android-gamepad-support.md](../rust-game-engines/web-android-gamepad-support.md)
- [reference/macroquad/wasm-build.md](wasm-build.md)
