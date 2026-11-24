---
title: 캔버스 게임의 헤드리스 브라우저 시험 — 시간이 아니라 상태를 기다린다
type: guide
tags: [testing, playwright, ci, wasm, web]
status: draft
created: 2026-11-18
updated: 2026-11-24
verified: |
  1차(Playwright 공식 문서, 2026-11-18 읽음): `page.waitForTimeout`에 "Never wait for timeout in production. Tests that wait for time are inherently flaky." 경고.
  1차(직접 겪고 고침, Knellroot CI — GitHub Actions 러너 + Playwright Chromium):
  - 고정 4초 대기가 느린 러너에서 로딩 덮개가 걷히기 전에 끝나 v0.6.4 운영 배포가 깨졌다 → 덮개 요소가 사라질 때까지 기다림(커밋 4f29e51, 2026-11-15).
  - 깨어남 장면 건너뛰기를 고정 1.5초로 기다렸다가 실패 → 기록(localStorage)에 적힐 때까지 기다림, CDP CPU 스로틀로 재현(d03e3d9, 2026-11-14).
  - 세로 회전 안내가 로딩 덮개 밑(z 순서)이라 안 보였던 것을 시험이 잡음(7548746, 2026-11-15).
  - macroquad는 한 프레임에 같은 키 두 번을 한 번으로 센다 → 누른 뒤 requestAnimationFrame 둘을 기다림(5319213, 2026-11-18 — `reference/macroquad/wasm-build.md`).
  - 메뉴에 줄 하나를 더하고 CI가 도는 스크립트 하나를 안 돌려 개발판 배포가 깨졌다(Knellroot 0151) → push 전에 CI가 돌리는 스크립트를 다.
  1차(직접 잼, 2026-11-24, Knellroot 0271 — Playwright Chromium 헤드리스, WebGL은 SwiftShader 소프트웨어 GL, 4코어 컨테이너와 GitHub 러너):
  - CI 잡 22분 가운데 Rust(fmt·clippy 셋·test·wasm, 캐시 적중)는 2분 남짓, 헤드리스 스크립트 다섯이 19분(85%). 스크립트의 고정 대기 합은 1분 안쪽 —
    나머지는 프레임을 기다리는 시간(누름 하나 = 게임 프레임 둘).
  - 같은 빌드·같은 장면에서 화면만 줄이니 1280×720 3.3 fps·스크린숏 2.0초 → 640×360 8.8 fps·0.74초 → 320×180 18 fps·0.42초.
    게임 안에서 3D 타깃만 줄이는 시험 깃발(화면 크기·UI 배치는 그대로)로 3.1 → 9 fps, 스크립트 하나 173 → 78초·638 → 161초.
  - Chromium 플래그(`--use-angle=swiftshader`·`--enable-unsafe-swiftshader`·`--use-gl=angle --ignore-gpu-blocklist`)는 fps가 같고 스크린숏은 더 느렸다.
  - 4코어에서 헤드리스 스크립트 둘·셋을 겹쳐 돌리니 부하 평균 10 안팎, 같은 스크립트가 두 배 넘게 걸렸다(SwiftShader가 코어를 다 쓴다).
  1차(GitHub 문서, 2026-11-24 읽음): 공개 레포의 표준 러너 `ubuntu-latest` = 4 vCPU·16GB(비공개는 2 vCPU·8GB), 잡마다 VM 하나, 무료 계정 동시 20잡(macOS 5).
  확인 못 함: 다른 엔진(Bevy·Godot 웹)의 같은 함정. GPU가 있는 러너(유료)에서의 차이. 고친 파이프라인의 실제 CI 시간(첫 실행 뒤 적는다).
sources:
  - https://playwright.dev/docs/api/class-page#page-wait-for-timeout
  - https://docs.github.com/en/actions/reference/runners/github-hosted-runners
  - https://docs.github.com/en/actions/reference/limits
---

# 캔버스 게임의 헤드리스 브라우저 시험

## 요약
캔버스 하나뿐인 게임은 DOM 단서가 적어 `waitForTimeout`에 기대기 쉽고, 그것이 느린 CI 러너에서만 깨진다. **보이는 상태를 기다린다**:
DOM(로딩 덮개가 사라짐), 저장소(기록에 적힘), 게임 루프(rAF 두 번), 첫 프레임 신호. 재현은 CDP CPU 스로틀로 한다.

## 본문
1. **게임이 신호를 남기게**: 첫 프레임 뒤 로딩 덮개를 지운다(`#load` 요소 제거), 장면이 끝나면 기록을 쓴다. 시험은 `page.waitForFunction(() => !document.getElementById('load'))`,
   `waitForFunction(() => localStorage.getItem(k)?.includes('woke=1'))`처럼 그것을 기다린다.
2. **키 하나 = 게임 프레임 둘**: 엔진이 "한 프레임에 눌린 키 집합"으로 읽으면 빠른 연타가 한 번이 된다.
   `await page.keyboard.press(k); await page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));`
3. **느린 기계를 흉내**: `const cdp = await ctx.newCDPSession(page); await cdp.send('Emulation.setCPUThrottlingRate', { rate: 5 });` —
   CI에서만 나던 실패가 로컬에서 몇 번에 한 번꼴로 난다. 고친 뒤 5배·8배에서 다시 돈다.
4. **저장을 심을 때**는 게임이 도는 탭이 아니라 같은 출처의 빈 페이지에서(게임이 끝날 때 제 기록으로 덮는다) 심고 다시 연다.
5. **겹치는 안내의 z 순서**도 시험이 본다: "안내가 보인다"는 요소가 있다가 아니라 맨 위에 있다(`elementFromPoint`).
6. **push 전에 CI가 돌리는 스크립트를 다 돌린다**: 메뉴 줄·탭 차례를 바꾸면 스크립트의 메뉴 길이 어긋난다. 바꾼 화면만 보는 스크립트로는 못 잡는다.
7. 고정 대기를 남겨야 하면(애니메이션을 찍는 사이 등) 그 값이 "판정"에 쓰이지 않게 — 스크린숏 간격은 되지만 "이만큼 기다리면 됐겠지"는 안 된다.

## 속도 — 헤드리스의 3D는 화소 수가 곧 시간
헤드리스 Chromium에는 GPU가 없어 WebGL을 CPU(SwiftShader)로 그린다. 그래서 시험 시간은 "기다린 시간"이 아니라 **그린 화소 수 × 프레임 수**다.
1. **먼저 잰다**: 단계별 시간(CI 로그의 타임스탬프)과 스크립트의 고정 대기 합을 견준다. 대기 합이 작으면 프레임이 병목이다 —
   `requestAnimationFrame`을 몇 초 세어 fps를 본다(1280×720에서 3 fps면 누름 하나가 0.7초).
2. **흐름만 보는 스크립트는 싸게 그린다**: 화면(뷰포트)을 줄이면 UI 배치·터치 자리가 바뀌니, 게임에 시험 깃발을 두어 **3D 타깃의 해상도만** 내린다
   (내부 해상도·슈퍼샘플링 끔). 그림을 사람이 보는 스크립트만 제 화질로 남긴다. 깃발은 개발 빌드에만.
3. **나란히 돌릴 때는 기계를 나눈다**: 소프트웨어 GL은 코어를 다 쓴다 — 한 기계에서 스크립트 둘을 겹치면 둘 다 느려지고, 시간으로 기다리는 곳이 깨진다.
   CI는 스크립트마다 잡(= VM)을 나누고(빌드 산출물은 아티팩트로 넘긴다), 필수 검사 이름을 지키려면 끝에 문지기 잡 하나가 앞 잡들의 결과를 본다
   (`if: !cancelled()` — 건너뛴 필수 검사는 통과로 읽힌다). 로컬에서는 차례로.
4. **배포 갈래에서는 나가는 것을 띄운다**: 개발 기능이 든 빌드로만 연기 시험을 돌면 실제 배포물(개발 기능을 뺀 빌드)은 한 번도 안 뜬 채 나간다.
   배포 직전에는 그 빌드를 타이틀까지 띄우고 "개발 메뉴가 없다"까지 보는 짧은 스크립트 하나면 된다 — 긴 시나리오는 PR 검사의 몫.
Rust 쪽(캐시가 맞으면 fmt·clippy·test·wasm 합쳐 2분)을 sccache·nextest로 더 줄이는 것은 이 경우 병목이 아니었다.

## 왜?
고정 대기는 "이 기계에서 이만큼이면 된다"는 가정이다. 러너는 기계마다·시간마다 빠르기가 달라, 가정이 깨지는 날에만 빨간불이 나고(운영 배포 날일 수도 있다)
재현이 어렵다. 상태를 기다리면 빠른 기계에선 빨리, 느린 기계에선 늦게 지나간다.

## 함정
- 첫 프레임 전 키는 버려진다 — 게임이 뜨기 전에 누른 키가 아무 일도 안 한 것처럼 보인다.
- 로컬에서 늘 통과하는 시험 = 안전하다가 아니다. 스로틀로 돌려 본다.
- 게임이 쓰는 저장소에 시험이 같은 탭에서 쓰면 게임이 덮는다.
- 로컬에서 시험을 겹쳐 돌리며 "CI보다 느리네"를 재면 틀린다 — 부하가 다른 측정은 서로 견주지 않는다(앞·뒤를 같은 부하에서).
- 싸게 그리는 깃발을 건 스크립트의 스크린숏은 판정용이 아니다(도트가 굵다). 제 화질로 볼 길(환경 변수)을 남긴다.

## 관련 노트
- [macroquad WASM 빌드](../reference/macroquad/wasm-build.md) — 키 누른 뒤 rAF 둘
- [개발용 시나리오 진입점](../concepts/dev-scenarios-and-scripted-cutscenes.md) — 고친 뒤 확인 세 겹
