---
title: 액션 게임 키보드·마우스 배치 — 마우스의 일은 카메라가 정하고, 왼손은 WASD 둘레에서 빈도 순
type: concept
tags: [gamedev, input, game-design, accessibility, macroquad]
status: draft
created: 2026-11-05
updated: 2026-11-05
verified: |
  1차 출처로 확인(소스 코드 읽기, 2026-11-05, miniquad 0.4.11 — Knellroot `third_party/miniquad` 패치본): 키를 받는 방식이 플랫폼마다 다르다.
  웹 `js/gl.js`는 `event.code`(위치), Windows `windows.rs`는 lParam의 스캔코드(`HIWORD(lparam) & 0x1FF` → `keycodes::translate_keycode`, 위치),
  macOS `apple_util.rs`는 `NSEvent.keyCode` 가상 키코드(ANSI 위치), Linux X11 `linux_x11/keycodes.rs`는 `XGetKeyboardMapping`의 첫 keysym,
  Wayland는 xkb keysym(둘 다 배열을 따르는 글자). 실행해서 AZERTY로 눌러 보지는 않았다 — "Linux AZERTY에서 WASD가 흐트러진다"는 코드에서 읽은 추론.
  miniquad `MouseButton`은 Left·Middle·Right·Unknown뿐(옆 버튼 M4·M5 없음), 웹 번들에 `contextmenu`를 막는 코드가 없다(grep) — 브라우저에서 오른쪽 클릭 메뉴가 실제로 뜨는지는 안 해 봤다.
  2차 출처(위키·게임 매체)만 있음 — 게임별 기본 키: 엘든 링(Shacknews, gamenguides·gamerguides 조각과 맞음), 다크 소울 3·세키로·P의 거짓(Fextralife 하나씩,
  P의 거짓 표는 Space가 두 줄), 검은 신화: 오공(Prima·Sportskeeda — 자세 키는 서로 다름), Hades II(Shacknews·Maxroll 등 여럿이 맞음),
  Diablo IV(Fextralife·Game8·MagicGameWorld — 물약 키는 엇갈림), Diablo IV 시즌 3(2025-01) WASD 프리셋(Prima·Dexerto 등 여럿),
  PoE 2 WASD(PC Gamer·Shacknews — "기본인지 옵션인지"는 출처끼리 다르다, 기술 키 기본값은 못 확인), Last Epoch 시즌 2 실험 옵션(Icy Veins).
  Hades 원작의 "커서가 있으면 커서 쪽, 숨기면 가까운 적" 조준은 Steam 유저 글 하나. 공식 매뉴얼은 어느 게임도 직접 읽지 못했다.
  스캔코드 원칙은 Factorio 개발자 포럼 글·SDL 메인테이너 글(2011)·업체 블로그(bugnet) — 서로 맞는다.
sources:
  - https://shacknews.com/article/128968/elden-ring-controls-and-pc-keybindings
  - https://darksouls3.wiki.fextralife.com/Subcontent:Controls+3+PC+Controls
  - https://sekiroshadowsdietwice.wiki.fextralife.com/Subcontent:Controls+3+PC+Controls
  - https://liesofp.wiki.fextralife.com/Subcontent:Controls+3+Pc
  - https://primagames.com/tips/black-myth-wukong-complete-controls-for-pc-controller
  - https://www.shacknews.com/article/146103/hades-2-controls-pc-keybindings
  - https://steamcommunity.com/app/1145360/discussions/0/2932364348258038169
  - https://diablo4.wiki.fextralife.com/Controls
  - https://primagames.com/news/diablo-4-season-3-finally-brings-wasd-movement-to-pc-players
  - https://pcgamer.com/games/rpg/path-of-exile-2s-developers-ended-up-reworking-the-entire-games-combat-around-a-new-control-scheme-because-of-a-single-class
  - https://www.switchbladegaming.com/path-of-exile-2/keybinds-guide-3/
  - https://wp-prod.icy-veins.com/wasd-controls-coming-to-last-epoch-with-season-2-launch/
  - https://forums.factorio.com/viewtopic.php?p=403127
  - https://discourse.libsdl.org/t/scancodes-vs-keycodes/18036
  - https://bugnet.io/blog/how-to-fix-keyboard-shortcuts-wrong-on-non-qwerty-layouts
---

# 액션 게임 키보드·마우스 배치

## 요약
PC 액션 게임의 키보드 배치는 장르마다 놀랄 만큼 같다. 왼손은 **WASD + 엄지 Space(회피) + 검지 E(상호작용)·R(회복)·Q·F + 새끼 Shift·Ctrl**, 오른손은 마우스다. 갈리는 것은 **마우스가 무슨 일을 하느냐**이고, 그것은 카메라가 정한다: 3인칭은 카메라 돌리기, 탑다운은 조준 커서, 정통 ARPG는 이동·대상 고르기. 그래서 패드 배치를 키보드로 옮길 때는 "패드 버튼 → 키"가 아니라 "이 카메라에서 마우스가 맡을 일 → 남는 동작을 왼손 빈도 순"으로 짠다. 키는 글자가 아니라 **물리 위치**로 받는다.

## 본문

### 장르별 기본 배치(2차 출처, 2026-11 조사)
3인칭 소울라이크 — 마우스 = 카메라:

| 동작 | 엘든 링 | 다크 소울 3 | 세키로 | P의 거짓 | 검은 신화: 오공 |
|---|---|---|---|---|---|
| 회피(꾹 = 달리기) | Space | Space | **L-Shift** | Space | Space |
| 점프 | F | Space | **Space** | ? | Ctrl |
| 공격 | 왼쪽 클릭 | 왼쪽 클릭 | 왼쪽 클릭 | 왼쪽 클릭 | 왼쪽 클릭 |
| 강공격 | **Shift + 왼쪽** | Shift + 왼쪽 | — | 오른쪽 클릭 | 오른쪽 클릭 |
| 방어·패링 | 오른쪽 클릭 | 오른쪽 클릭 | 오른쪽 클릭 | **Shift** | — |
| 락온 | 휠 클릭 / Q | 휠 클릭 | 휠 클릭 | 휠 클릭 | 휠 클릭 |
| 상호작용 | E | E | E | E | E |
| 회복·아이템 | R | R | R | R | R |
| 장비 바꾸기 | 화살표 | 화살표 | Z·X·C | Tab·T·G | — |

- 공통: WASD, 왼쪽 클릭 공격, **휠 클릭 락온, E 상호작용, R 회복**, Esc 메뉴, Alt 걷기(프롬).
- 회피는 Space가 대세. 세키로만 Shift — 점프가 핵심 동작이라 엄지 자리를 점프에 줬다. **점프는 합의가 없다**(F·Space·Ctrl).

탑다운 액션 로그라이트 — 마우스 = 조준 커서:
- Hades II: WASD, 왼쪽 클릭 공격, 오른쪽 클릭 특수, **Space 대시**, Q 캐스트, E 상호작용, F 헥스. 왼손 묶음이 소울라이크와 같다.
- Hades(원작): 활·총은 커서 쪽, 커서를 숨기면 가까운 적을 겨눈다(유저 보고). 이 게임들의 기본 표에 **카메라를 돌리는 키는 없다** — 카메라가 고정이다.

정통 ARPG — 마우스 = 이동 + 대상:
- Diablo IV: 왼쪽 클릭 이동·기본 공격, 오른쪽 클릭 + 숫자 1~4 기술, Space 회피, T 귀환. 2023년 출시 땐 WASD가 없었고 **2025-01 시즌 3에 프리셋**으로 넣었다("키보드 이동" — 마우스는 공격만, "키보드만").
- PoE 2: WASD를 넣고 전투를 거기에 맞춰 다시 짰다(석궁 직업에서 시작). 오래 쓰던 기술 줄 QWERT의 **W가 이동과 겹친다**는 비판.
- Last Epoch: 시즌 2에 실험 옵션, 기본은 여전히 클릭 이동.

### 원리
- **마우스의 일 = 카메라가 정한다.**
  - 3인칭(카메라가 캐릭터 뒤에서 자유롭게 돈다) → 마우스 움직임 = 카메라. 공격·방어는 마우스 버튼(패드의 R1·L1 자리).
  - 탑다운·쿼터뷰(카메라 고정) → 마우스 = **땅 위의 조준점**. 커서 쪽으로 쏘고, 커서가 쉬면 자동 조준.
  - 락온 중(3인칭) → 카메라는 대상이 정하므로 마우스 움직임은 대상 바꾸기로 쓰인다(소울라이크 관례).
- **왼손은 WASD에서 손을 떼지 않는 거리 = 빈도 순**: 엄지 Space(가장 급한 방어 동작), 검지 E·R·F·Q(W에서 한 칸), 새끼 Shift·Ctrl(쥐고 있는 동작 — 달리기·방어), 1~4는 손을 뻗는다 → 가끔 쓰는 주문·아이템.
- **패드를 키보드로 직역하면 조합키가 생긴다**: 프롬의 `Shift + 클릭` = 패드 R2·L2를 옮긴 흔적. 뒤의 게임(P의 거짓·오공)은 강공격을 오른쪽 클릭에 따로 뒀다. 동시에 누르기는 접근성 비용이다.
- **프리셋으로 덧붙이기**: Diablo IV처럼 "키보드+마우스 / 키보드만"을 프리셋으로 두면 기존 배치를 깨지 않고 마우스 쪽을 더할 수 있다. 프리셋 안에서 다시 붙이기는 그대로.
- **키는 물리 위치로(스캔코드), 안내는 그 자판의 글자로.** 프랑스 AZERTY의 WASD 자리는 ZQSD — 위치로 받으면 손 모양이 같다. 글자 입력(이름 짓기)만 글자 기준. 다시 붙이기는 그래도 필요한 마지막 안전망.

## 왜?
- 양손이 하는 일이 다르다. 오른손은 마우스로 **연속값**(방향·카메라)을 다루는 데 쓰고, 이산 동작은 마우스 버튼 둘·셋에 가장 급한 것(공격·방어)만 둔다. 나머지 이산 동작은 왼손이 이동을 멈추지 않고 닿는 키에 빈도대로 깔린다 — 장르가 달라도 손이 같으니 배치가 수렴한다.
- 마우스 움직임은 하나의 연속값이라 **한 가지 일**만 맡을 수 있다. 3인칭은 카메라가 그 일이고, 탑다운은 카메라가 고정이라 그 자리를 조준이 쓴다. 그래서 탑다운에서 마우스로 카메라를 돌리게 하면 조준을 잃는다.
- 스캔코드: 플레이어가 바꾸는 것은 "자판에 찍힌 글자"지 손의 모양이 아니다. 글자로 받으면 배열이 다른 나라에서 기본 배치가 흩어진다.

## 함정
- **카메라 돌리기가 게임 규칙의 일부일 때** 마우스 카메라로 대신하면 장치마다 규칙이 갈린다. 예: 돌리기가 몸을 돌리고 적을 휘청이게 하는 동작이면, 마우스로 자유롭게 도는 플레이어는 그 동작을 잃는다. 시점과 동작을 함께 하는 키는 마우스 프리셋에서도 남긴다.
- 키보드로 해도 패드 안내가 뜨는 게임(엘든 링 기본값이 Xbox 안내라는 지적, 2차) — 안내는 마지막으로 만진 장치를 따라야 한다([컨트롤러 배치](controller-layout-and-remapping.md)).
- miniquad: 웹·Windows·macOS는 위치, **Linux X11·Wayland는 글자**(위 verified). Linux 묶음을 내면 AZERTY에서 WASD가 흩어질 수 있다. 마우스 옆 버튼(M4·M5)은 받지 못한다.
- 웹: 오른쪽 클릭은 브라우저 메뉴, 휠 클릭은 Windows 브라우저의 자동 스크롤과 부딪힐 수 있다 — 캔버스에서 `contextmenu`·`mousedown`(button 1)을 막아야 할 수 있다(코드에서 막는 곳이 없음만 확인).
- PoE 2의 교훈: 이동을 WASD로 옮기면 그 자리에 있던 기능 키(W)가 밀려난다. 키 배치는 이동 방식과 함께 바꾼다.

## 관련 노트
- [컨트롤러 버튼 배치와 다시 붙이기](controller-layout-and-remapping.md) — 배치표·맞바꾸기·고정 키·장치를 따르는 안내
- [시점 전환과 락온 카메라](camera-mode-switch-and-lock-on.md) — 입력 기준과 카메라 리그
- [게임패드와 Android 입력 현황](../reference/macroquad/gamepad-and-android-input.md)
- [액션 게임 터치 배치](touch-action-layout.md)
