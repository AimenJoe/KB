---
title: 액션 게임 터치 배치 — 공격 둘레 호, 상황 버튼은 제 자리에만, 버튼 수가 복잡도
type: concept
tags: [touch, input, mobile, accessibility, game-design, gamedev]
status: draft
created: 2026-11-04
updated: 2026-11-04
verified: |
  1차 출처로 확인(2026-11-04, 원문 읽음):
  - Apple HIG "Game controls"(2025-06 개정): 자주 쓰는 컨트롤 최소 44×44pt·덜 중요한 것 28×28pt, safe area 피하기, "쓸 수 없거나 상관없을 때는 숨겨 어수선함을 줄여라",
    탭/길게 누르기로 한 컨트롤에 변형 동작, 여러 동작은 한 컨트롤로, 이동 스틱은 엄지 댄 자리에, 눌림 상태는 손가락에 가려도 보이게, 버튼 그림은 글자 대신 기호.
  - Apple HIG "Accessibility": 테두리 있는 요소 둘레 약 12pt, 제스처에는 버튼 대안.
  - Android 접근성 도움말: 터치 대상 48×48dp(약 9mm), 간격 8dp 이상.
  - Activision 블로그(2019, CoD Mobile): 커스텀 레이아웃(옮기기·크기·불투명도), 상황 버튼(문 앞 문 열기·장애물 앞 넘기 등).
  - 직접 구현·시험(Knellroot 0053, 2026-11-04): 공격 + 둘레 호 넷 + 돌리기 캡슐 + 상황 버튼 둘, 겹침 없음·화면 안·상황 버튼이 켜져도 다른 버튼 자리 그대로를
    단위 시험(폰·작은 폰·태블릿·데스크톱·세로 폰)과 헤드리스 Chromium 터치(DPR 3) 스크린숏으로 확인. 실제 폰에서 엄지가 닿는지는 사람 판정 전.
  2차 출처만 있음: Diablo Immortal(공격이 가장 크고 둘레에 스킬, 끌어 조준), Wild Rift(스킬 넷, 끌면 조준 스틱, 버튼마다 크기·자리 바꾸기),
  Brawl Stars(탭 = 자동 조준, 끌기 = 조준), Dead Cells 모바일(버튼 자리·크기, 쓸어 회피, 자동 공격), Fez(Vita, 쓸어 세계 돌리기),
  Hoober 2013(한 손 쥠 49% — 관찰 연구, 가로 게임 쥠에는 바로 못 씀). "버튼 수가 복잡도"라는 개발자 말은 출처 미확인.
  확인 못 함: iPhone 가로 safe-area 값과 macroquad 웹에서 `env(safe-area-inset-*)` 읽기, 엄지 크기의 1차 연구.
sources:
  - https://developer.apple.com/design/human-interface-guidelines/game-controls
  - https://developer.apple.com/design/human-interface-guidelines/accessibility
  - https://support.google.com/accessibility/android/answer/7101858
  - https://blog.activision.com/call-of-duty/2019-10/Getting-a-Grip-on-the-Call-of-Duty-Mobile-Controls
  - https://diabloimmortal.wiki.fextralife.com/Controls
  - https://playerassist.com/league-legends-wild-rift-change-hud-layout/
  - https://www.siliconera.com/dead-cells-heads-to-smartphones-with-a-new-mobile-friendly-interface/
---

# 액션 게임 터치 배치

## 요약
가로 폰 액션 게임의 터치 오버레이는 **공격을 가장 크게 오른쪽 아래에 두고, 자주 쓰는 동작 넷을 그 둘레 호에** 놓는다. 가끔 쓰는 것은 바깥 호에 둔다. **쓸 수 있을 때만 필요한 버튼(락온·회복·상호작용)은 상황 버튼**으로 만든다. 상황 버튼은 정해 둔 제 자리에만 뜨고 다른 버튼을 밀지 않는다. 기능을 하나씩 더하다 보면 버튼이 10개를 넘어 난잡해진다. 그러니 동작을 더할 때마다 "합칠 수 있나(점프 = 상호작용), 숨길 수 있나(쓸 수 없을 때)"를 먼저 묻는다.

## 본문
- **기준 길이 u = 짧은 변**(가로 폰의 높이). 크기·거리를 u 비율로 정하고, 태블릿에서 너무 커지지 않게 u에 상한(예: 520 논리 px)을 둔다.
- **공격**: 지름 약 0.27u, 오른쪽·아래 여백 약 0.21~0.24u. 탭 = 콤보, 꾹 = 강타처럼 한 버튼에 변형을 싣는다(HIG).
- **첫째 호**(공격 가운데에서 약 0.26u): 회피·패링·원거리·점프처럼 타이밍이 중요하고 자주 쓰는 것. 각도를 고르게 벌리면(예: 188°·146°·104°·62°) 엄지를 굴리기만 해도 닿는다. 지름 약 0.15~0.17u.
- **둘째 호**(약 0.44u): 덜 쓰는 것, 그리고 상황 버튼.
- **상황 버튼**: 쉼터 곁에서만 쉬기, 적이 가까울 때만 락온, 마실 수 있을 때만 회복. 쓸 수 없을 때는 숨기고, 자리는 늘 비워 둔다.
- **합치기**: 연타하지 않는 동작끼리 합친다(점프 + 상호작용). 그림은 지금 하는 일로 바꾼다(모닥불).
- **짝 버튼**(왼쪽·오른쪽 돌리기)은 캡슐 하나로 묶어 버튼 하나처럼 읽히게 한다.
- **시험**: 배치를 순수 함수로 두고 다음을 단위 시험한다 — 겹침 없음, 화면 안(세로 폰·태블릿 포함), 공격이 가장 큼, 최소 크기, 상황 버튼이 켜져도 나머지 자리가 그대로. 헤드리스 터치 시험의 좌표 표도 같은 식으로 맞춘다.

## 왜?
- 엄지 하나가 오른쪽 버튼을 다 맡는다. 공격 둘레 호에 두면 "공격 → 회피"가 엄지를 굴리는 것 하나로 된다. 자리가 바뀌면 손이 외운 자리가 틀어진다. 그래서 상황 버튼이 다른 버튼을 밀면 안 된다.
- 화면은 게임을 보는 곳이다. 쓸 수 없는 버튼까지 늘 그려 두면 플레이어가 화면을 덜 보게 된다(HIG "숨겨 어수선함을 줄여라").

## 함정
- 개발용 버튼(랩·시나리오)도 버튼이다. 작은 폰에서는 개발 줄이 바깥 호와 겹쳤다 → 시험에 "개발 버튼까지 켠 경우"를 넣는다.
- 상호작용을 연타하는 버튼(공격·회피)과 합치면 싸울 때 문·상자를 못 연다([컨트롤러 배치](controller-layout-and-remapping.md)).
- 터치에는 조준 스틱이 없다. 원거리는 자동 조준으로 두고, 끌어 조준은 나중에 붙인다.

## 관련 노트
- [컨트롤러 버튼 배치와 다시 붙이기](controller-layout-and-remapping.md)
- [macroquad 게임패드·Android·터치 입력](../reference/macroquad/gamepad-and-android-input.md)
- [HUD 읽기와 퀵 슬롯](hud-readability-and-quick-slots.md)
