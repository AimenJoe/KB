---
title: 골든 트레이스와 플랫폼 수학 — sin·atan2의 끝자리는 기계마다 다르다
type: concept
tags: [gamedev, rust, testing, determinism, ci, floating-point]
status: draft
created: 2026-11-26
updated: 2026-11-26
verified: |
  1차(직접 겪음, knellroot 0278·0279, 2026-11-26): 같은 누름으로 15초를 돌린 판의 사건 해시 65개 가운데 넷, 이펙트 해시 429개 가운데
  열하나가 CI(Ubuntu 26.04)에서만 달랐다. 세션 컨테이너(Ubuntu 24.04, glibc 2.39)에서는 늘 같았다. CI 두 실행의 해시는 서로 같았다.
  검사 잡의 러너만 ubuntu-24.04로 고정하자 통과했고(원인 = 시스템 libm의 판), 초월 함수 520곳쯤을 `libm` 크레이트로 옮긴 뒤에는
  ubuntu-latest(26.04)에서 고정값을 다시 쓰지 않고 통과했다(골든 102 · 시나리오 65는 그대로, 이펙트 일곱 줄만 다시 씀).
  clippy `disallowed-methods`가 `f32::sin` · `f32::atan2`를 실제로 잡는 것도 한 줄 넣어 확인했다.
  1차(공식 문서): glibc 2.41 NEWS — acosf · asinf · atan2f · atanf · tanf 등을 CORE-MATH의 올바르게 반올림되는 구현으로 바꿨다.
  sinf · cosf는 그 목록에 없다(갈린 것이 atan2 · asin · acos를 쓰는 긴 판뿐이던 관찰과 맞는다 — 어느 함수가 갈렸는지 함수별로 재지는 않았다).
  Rust RFC 3514 — 초월 함수의 정확한 결과는 타깃 · 버전 · 플래그에 따라 달라질 수 있다.
  2차 출처만 있음: `libm` 크레이트로 Linux · macOS에서 같은 결과를 얻었다는 포럼 글. Windows · macOS · Android 실기기에서 우리 해시가
  같은지는 재지 않았다(CI의 Linux 둘과 wasm 빌드만).
  확인 못 함: 함정의 "컴파일러 상수 접기가 호스트 libm을 쓴다"는 rust-lang/rust 이슈 109118(opt-level에 따라 sin의 비트가 달랐다는 보고)에서
  짐작한 것 — 직접 재현하지 않았다.
  못 잰 것: 네이티브에서 `libm` 크레이트가 glibc보다 얼마나 느린지(한 프레임의 호출이 수천 아래라 재지 않았다).
sources:
  - https://gcc.gnu.org/pipermail/libc-alpha/2025-January/164378.html
  - https://rust-lang.github.io/rfcs/3514-float-semantics.html
  - https://docs.rs/bevy_math/latest/src/bevy_math/ops.rs.html
  - https://users.rust-lang.org/t/f64-ln-1p-platform-specific-behavior/77113
  - https://docs.rs/libm
  - https://github.com/rust-lang/rust/issues/109118
---

# 골든 트레이스와 플랫폼 수학

## 요약
로직을 고정 입력으로 돌려 해시를 적어 두는 시험(골든 트레이스)은 리팩터링의 가장 값싼 증명이다. 그런데 `f32::sin` · `atan2` 같은 초월
함수는 네이티브에서 **시스템의 libm**을 부르고, 그 끝자리는 libc 판마다 다르다. 짧은 판은 우연히 같고, 적 수십이 서로 미는 긴 판은
끝자리 하나로 갈린다 — 내 기계에서는 초록, CI에서는 빨강. 고치는 법은 초월 함수를 순수 Rust 구현(`libm` 크레이트)으로 지나게 하고
std의 것을 린트로 막는 것이다.

## 본문

### 무엇이 같고 무엇이 다른가
| 연산 | 플랫폼마다 |
|---|---|
| `+ - * /` · `sqrt` · `abs` · `floor` · `round` · `mul_add` | 같다(IEEE 754가 결과를 정한다) |
| `to_radians` · `powi`(곱셈으로 풀린다) | 같다 |
| `sin` · `cos` · `tan` · `atan2` · `asin` · `acos` · `exp` · `ln` · `powf` · `hypot` | **다를 수 있다** — 네이티브는 시스템 libm, wasm은 Rust std 안의 libm |
| 수학 크레이트의 각도 함수(glam `Quat::from_rotation_y` · `Vec2::from_angle` · `angle_between` · `slerp`) | 안에서 std를 부른다 — 같이 다르다 |

### 고치는 꼴(Rust)
1. 확장 트레이트 하나: `trait Det { fn sin_d(self) -> Self; fn atan2_d(self, x: Self) -> Self; … }`를 `f32` · `f64`에 `libm::sinf` …로 구현.
   메서드 이름을 다르게(`_d`) 두면 `sed`로 옮길 수 있다(타입의 제 메서드가 트레이트 메서드보다 앞서므로 같은 이름으로는 못 가린다).
2. `clippy.toml`의 `disallowed-methods`에 `f32::sin` · `f32::cos` · `f32::atan2` …를 적는다(`-D warnings`인 CI가 막는다). 원시 타입의
   경로(`f32::sin`)가 그대로 먹는다.
3. 로직이 쓰는 수학 크레이트의 각도 함수는 손으로 바꾼다(회전 = 반각의 `sin_cos`로 쿼터니언을 직접 만든다) + 로직 폴더를 훑는 시험.
   그림 쪽(렌더 · 카메라)은 트레이스 밖이면 그대로 둬도 된다.
4. 러너를 옛 판으로 고정하는 것은 임시 방편이다 — 고정값을 쓴 기계의 판이 오르면 다시 깨진다.

### 경합과 플랫폼 차이 가르기
- 같은 곳에서 두 번 돌려 해시가 **다르면** 경합 · 전역 상태 · 해시맵 순서.
- 같은 곳에서는 **같고** 다른 곳과만 다르면 플랫폼(libm · CPU 갈래 · 컴파일 플래그).
- 갈린 경우가 "긴 판 · 물체가 많은 판"에 몰려 있으면 끝자리가 혼돈으로 커진 것이다.

## 왜?
- IEEE 754는 초월 함수의 올바른 반올림을 **권고**할 뿐 요구하지 않는다. libm마다 "1 ULP 안"의 다른 값을 내도 규격 안이다. glibc는
  2.41에서 여러 binary32 함수를 올바르게 반올림되는 구현으로 바꿨다 — 더 정확해졌고, 그래서 옛 판과 끝자리가 달라졌다.
- Rust std는 이 함수들의 결과를 약속하지 않는다(RFC 3514). 웹(wasm32-unknown-unknown)의 std는 처음부터 Rust로 옮긴 libm을 쓴다 —
  `libm` 크레이트로 맞추면 네이티브 시험이 웹 빌드와 같은 셈을 한다는 덤이 있다.
- 게임 로직은 되먹임 계다. 끝자리 하나가 충돌 차례 하나를 바꾸고, 그 뒤는 다른 판이다. 그래서 "얼마나 다른가"가 아니라 "비트가
  같은가"가 기준이 된다.

## 함정
- **안전망을 넣은 push의 CI를 안 봤다**: 로컬에서 초록인 것만 보고 네 번을 올렸고, 개발판 배포가 그동안 멈춰 있었다. 고정값을 넣거나
  다시 쓴 push는 CI 결과까지 본다.
- 짧은 골든(6초 · 서 있는 적)은 두 플랫폼에서 같았다 — "CI에서 한 번 통과했다"가 결정론의 증명은 아니다.
- 해시에 접는 값을 1e-3으로 양자화해도 소용없다: 끝자리가 경계를 넘거나 사건의 차례를 바꾸면 그대로 갈린다.
- 컴파일러의 상수 접기(컴파일 때 `sin(상수)`를 미리 셈)도 std 함수에서는 변수일 수 있다(확인 못 함 — `verified`). 순수 Rust 구현은 접히든 아니든 같은 코드의 결과다.
- `libm` 크레이트의 `sqrt`까지 쓸 필요는 없다(std의 `sqrt`는 IEEE가 정한다) — 수학 크레이트의 `libm` 기능을 통째로 켜면 `sqrt`도
  그리로 가서 느려질 수 있다.
- 리플레이 · 록스텝 네트워킹을 하려면 이것만으로는 모자란다(FMA 융합 · x87 · 스레드 차례). 여기서 다룬 것은 "같은 바이너리 꼴,
  다른 libc"까지다.

## 관련 노트
- [1인 게임 코드의 건강 신호](solo-game-codebase-health-signals.md) — 골든 트레이스를 안전망으로 쓰는 리팩터링 차례
- [고정 타임스텝 게임 루프와 히트스톱](fixed-timestep-and-hitstop.md) — 고정 틱이라야 트레이스가 선다
