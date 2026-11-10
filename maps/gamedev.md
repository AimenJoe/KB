---
title: "지도: 게임 개발"
type: map
tags: [gamedev, macroquad, rust, game-design, pixel-art, game-feel]
status: verified
created: 2026-10-24
updated: 2026-11-10
---

# 지도: 게임 개발

게임 개발 관련 노트의 입구. 저장 위치는 종류별 폴더에 있고, 여기서는 도메인 관점으로 모은다.

## 설계
- [1인 개발용 액션 로그라이트 설계 원칙](../concepts/action-roguelite-for-solo-dev.md) — 런 구조 vs 메트로배니아, 탑다운 vs 사이드뷰, 전투감 먼저, 캐릭터=반복 단위, 장기 프로젝트 단계
- [그림 못 그려도 도트 게임 만들기](../guides/pixel-art-without-an-artist.md) — 에셋 팩 하나 중심, 라이선스 확인, 공개 레포 + 비공개 에셋 레포(토큰·비용·AI 조항), 둥근 지형 굽기, 눈에 띄어야 하는 물체(더하기 빛·움직임), 16×16 공격 동작(들기·치기·거두기, 발 번갈아), 타이틀 키 아트(글 자리 먼저, 이음매 굴리기)
- [두 번째 게임 프로젝트의 첫날](../guides/second-game-project-day-one.md) — 첫 게임에서 늦게 깔아 비쌌던 규칙 15개를 첫 커밋에(입력 Actions·고정 틱·수치 한 곳·소리 큐·틱 단계·표+테스트·언어별 글·개발 시나리오·흐름 순수 함수·결정 기록·CI·라이선스·안내·이벤트 저장·KB 경계), 가져올 코드와 두고 올 코드
- [PoC와 Lab](../guides/poc-and-lab-before-content.md) — PoC = 질문·통과 기준·시간 상한·대안, Lab = 게임 안 슬라이더(커서 없이) → 프리셋 A/B → `tuning.rs`로 내보내기, 랩마다 시나리오, Hecker의 튜닝 사다리 · 값 얼리기(기본값 스냅숏 시험 — 판정 없이 바뀌지 않게)
- [게임 화면 색약 점검](../guides/color-vision-check-for-games.md) — 스크린숏을 Machado 행렬(선형 RGB)로 1·2·3형 + 흑백, 알아야 하는 것은 밝기·모양으로 남긴다
- [작곡가·음향 담당 없이 게임 소리 넣기](../guides/game-audio-without-a-composer.md) — CC0 출처(Kenney·OGA), 숫자로 거르기(길이·밝기·폭·이음매), 표 + 변환 스크립트, 변형·메뉴 소리 한 곳·덕킹, 사람이 고르는 듣기 페이지, 옛 곡·새 곡 둘 다(상황으로 가르기·런마다 번갈아), 환경음 층
- [인디 게임 공식 페이지](../guides/indie-game-landing-page.md)
- [공개 데모와 바깥 의견 받기](../concepts/public-demo-and-outside-feedback.md) — 첫 경험 먼저 시험, 로그라이트는 한 바퀴 온전히·깊이는 잠금, 기술 점검, 버전이 저절로 붙는 짧은 설문, itch.io HTML5 ZIP, 행사 전에 내기 — 첫 화면에 무엇·어디서, 싣는 칸(볼거리·해 보기·팩트시트·크레딧), 이야기를 스크롤로, CSS steps() 스프라이트 띠, 움직임 줄이기, 헤드리스 녹화는 도트를 뭉갠다
- [무료 그림·사진 구하는 곳](../reference/assets/free-image-sources.md) — Openverse·미술관 CC0·사진 사이트, PDM과 CC0, API 요령(Met v1.1, UA)
- [게임 그림 외주 맡기기](../guides/commissioning-game-art.md) — 임시 그림으로 먼저 판정, 사양서(안전 영역·색 약속), 계약: 저작재산권 + 2차적저작물작성권 특약(한국 제45조②), 공개 레포 커밋 허락
- [이미지 생성 모델로 게임 일러스트 그리기](../guides/image-model-for-game-illustrations.md) — 나노바나나: 직접 그린 참고 그림 + 생김새 글, 목적·세계 규칙·캐릭터·장면 덩어리, 장면마다 새 대화·스타일 덩어리 매번, 비율은 글로(구도 그림은 베낀다), 캐릭터 시트 먼저, 지울 때 대신 그릴 것, 칸마다 가장 흔한 색·작은 캐릭터 자리, ✦ 되돌리기

## 3D·카메라
- [시점 전환(쿼터뷰 ↔ 숄더뷰)과 락온 카메라](../concepts/camera-mode-switch-and-lock-on.md) — 게임 규칙 하나 + 리그 둘 + 입력 기준 둘, 기준은 즉시·카메라만 보간, 둘 다 Perspective·FOV 격차 줄이기, 어깨 너머 1/3 구도, 가림은 당기기 → 페이드, Nesky 50 실수
- [macroquad 3D 렌더링](../reference/macroquad/3d-rendering.md) — Camera3D(기본 z-up·fovy 라디안·깊이 켜짐 — 렌더 타깃엔 깊이 버퍼를 따로), Mesh u16·매 프레임 재업로드·조용히 잘림, 드로콜 갈리는 조건, 기본 셰이더는 normal을 안 읽음, 로더 없음
- [레트로 3D 모델 파이프라인 — Blockbench → glTF](../reference/assets/retro-3d-models-blockbench-gltf.md) — 상자 + 부위 강체 애니메이션(스키닝 없음), `gltf` 크레이트, 단위 16·y-up·5.0 부호, 상자 둘짜리 파일로 로더부터 (실제로는 Blockbench 대신 Blender bpy + AI 메시 부위 강체로 감 — 아래 AI 메시 가이드)
- [3D 도트 룩(t3ssel8r 풍)](../concepts/3d-pixel-art-look.md) — 낮은 해상도 + 정수배, 툰 빛, 선 둘(깊이 = 어두운 가장자리·법선 = 밝은 볼록 모서리), 카메라 픽셀 맞춤(직교에서만), 풀 빌보드, 모델링 체크리스트(면이 또렷한 로우폴리·큰 색 덩어리·볼록 모서리), 원근 카메라와의 충돌 · 소품을 이 룩으로(무늬 상자 대신 깎은 덩어리 쌓기·둥근 몸과 각진 테 가르기·빛나는 꼴은 색 띠·리뷰 표 + 게임 화면 앞·뒤)
- [작게 보이는 로우폴리 모델을 읽히게](../concepts/readable-low-poly-models.md) — 깊이 버퍼 먼저(없으면 부위가 엉킴), 외곽선·빛 단계·가장자리 빛, 실루엣·명도, AI 3D·팩의 약관(Hunyuan3D 한국 제외)
- [AI 3D 메시를 작은 게임용 강체 부위 모델로](../guides/ai-mesh-to-rigid-part-model.md) — Meshy 메시: 정점 합치기 → 줄이기 → 새 UV에 색 굽기 → 면 자리로 부위 자르기 → 기존 뼈·동작, Blender 굽기가 검게 나오는 두 원인 · 비스듬한 부위는 텍스처 색으로 자르기·텍스처에만 있는 눈·자른 뒤 부위마다 법선 재검사·그늘 굽힘 주의
- [실감나게 귀여운 캐릭터 동작](../concepts/believable-cute-character-motion.md) — 12원칙(Lasseter 1987)을 게임에: 예비는 적 길게·플레이어 짧게, 실감은 끝맺음·덧붙이는 스프링 층(암시적 오일러 식), 부피 지키는 찌그러짐, 작은 화면 과장, 반응 대 자연스러움
- [어두운 세계의 귀여운 캐릭터](../concepts/cute-characters-in-a-dark-world.md) — 2등신·눈 크고 낮게·입 없음·디테일 넷, "색 = 생명"(살아 있는 것만 파스텔, 침식은 같은 꼴인데 색을 잃음, 세계는 해 질 녘)

## 보상·경제
- [회복과 화폐 드롭](../concepts/roguelite-healing-and-currency.md) — 깎인 만큼 확률 + 불운 보정, 자석·줍기 지연·오르는 소리, 메타 화폐 맡기기(쉼터 자동)·둘 중 하나 영구 기술·살 수 있을 때 쓰는 곳이 빛나기
- [능력치·장비 설계](../concepts/action-rpg-stats-and-equipment.md) — 무기는 모양·장신구는 수치·성장은 영구, 공격 속도 = 시계 배율, 큰 회복 = 목숨
- [로그라이트 저널(목표 목록)](../concepts/roguelite-journal-goals.md) — 평소 플레이를 런을 넘는 목표로, 앞 목표 뒤에 펼쳐짐, 받기 보상(재화·힘 아닌 것·옆으로), 진행은 기록에서 계산
- [영구 성장 해금을 계획할 수 있게](../concepts/meta-progression-unlock-planning.md) — 다 보이는 칸·칸마다 그림·밝기 네 단, 잠긴 칸까지의 칸 수·합계·모자람, 목표 핀(길 표시·메뉴에서도), 캐릭터 사이 같은 꼴(고유 재주 한 칸), 탭이 넘치면 창 + ◀▶
- [저장 슬롯·이어하기·런 중단 저장](../concepts/roguelite-save-slots-and-continue.md) — 기록과 런을 나누기, 슬롯은 기록 단위·설정은 밖, 시작하기/이어하기 → 슬롯 고르기, 옛 저장 = 슬롯 1, 두 번 눌러 지우기, 런 저장은 죽음이 런을 끝내나로 고르기(한 번 쓰는 중단 저장 vs 마지막 체크포인트), 저장 빈도 세 겹(사건·경계 이벤트·끄기 전 — 짧은 주기는 싸움 중을 적어 뺐다)과 같은 글이면 안 쓰기, 쓰기 실패를 알기(되읽기·한 번 알림), 끄는 순간(PC 창 닫기·웹 visibilitychange·fsync)

## 월드 구조
- [미니맵 없이 길 알려 주기](../concepts/wayfinding-without-a-minimap.md) — 갈 곳이 빛난다(같은 색 = 갈 길), 화면 밖이면 1초 뒤 가장자리 화살(카메라 뒤면 뒤집기), 목표 글은 사건이 아니라 갈 곳, 싸우는 동안은 비우기
- [놀이 칸 밖 채우기](../concepts/surroundings-beyond-the-play-area.md) — 걷는 땅 아래 높이 안개(판 겹치기 + 깊이 버퍼), 상태 없는 입자(감아 도는 상자), 하늘 띠·공기 원근 산등성이·실루엣 하나, 흔든 이십면체 잎 무더기·각진 뿌리, 화면 고정 아지랑이·먼 클립 함정
- [탑다운 모험 구조](../concepts/adventure-field-and-procedural-dungeon.md) — 격자 하나, 카메라 경계 사각형(연속 스크롤 = 큰 경계, 방 밀기 = 경계 바뀜), 방 그래프 던전·잠금, 저장 지점 부활, 보스 뒤 출구는 쓰러진 자리에서 멀리, 장소를 바꾸는 칸은 밟기보다 곁에서 확인 버튼
- [선형 진행을 갈래 길로 느끼게 하는 지도](../concepts/branching-route-map.md) — 층 + 이어진 구간(엇갈림 없음·합류), 칸 종류가 결과를 바꿈, 다음 한 걸음 + 보스만 보이기(StS 지도·Hades 문)
- [로그라이트 방이 반복되게 느껴질 때](../concepts/roguelite-room-variety.md) — 모양보다 방마다의 판단: 무리 표·세기 곡선·싸움 종류(물결·매복·버티기)·등장·곁방 보상 표지·손으로 짠 틀(시험이 규칙을 본다)
- ["깊이 내려간다"를 보이게 하기](../concepts/conveying-descent.md) — 검은 전환 대신 지층 단면(로딩 시간 활용), 깊이 숫자 표, 지역 이름 카드, 지도 기울이기, 방 안의 위(빛줄기·떨어지는 흙·물방울)

## 게임 루프·전투감
- [고정 타임스텝 게임 루프와 히트스톱](../concepts/fixed-timestep-and-hitstop.md) — 누적기 루프, 입력 래치, 보간, 히트스톱은 로직 시계만, trauma² 흔들림, 피해와 맞은 반응 가르기(독구름·장판은 넉백·히트스톱 없이)
- [공격 타이밍 패링](../concepts/timing-parry.md) — 버튼 없이 스윙 첫 창 + 앞쪽, 회피 = 안전·패링 = 이득, 거울(막는 보스: 튕기고 반격, 아래·필살기로 뚫기)
- [모든 행동에 재사용 대기](../concepts/action-reuse-gating.md) — 동작 시간·대기·게이지·쓰는 시간을 행동마다 고르기, 회복 = 먹는 시간 + 시작부터 대기, 패링 창 = 열린 순간부터 대기·성공하면 해제
- [필살기의 임팩트](../concepts/special-move-impact.md) — 시동 정지(슈퍼 플래시), 화면 한 폭 거리, 넉백 > 속도로 끌고 가기, 소리 하나, 빠른 돌진 겨누기(시동 동안만 콘 안의 적 쪽으로 + 점선)
- [근접 평타·모으기 공격의 손맛](../concepts/melee-light-and-charged-attack-feel.md) — 평타는 누르는 순간(모으기 때문에 떼는 순간에 묶지 않기), 작은 타격의 층(히트스톱 사다리·피격자 진동·카메라 킥·공격자 확인, trauma²는 작은 타격을 0으로), 모으기는 같은 시간의 콤보보다 세야(자세 깨기·벽 쿵), 박자 콤보는 반응 시간 밖의 템포 + 몸에서 닫히는 고리 + 창 전 입력은 박자에 스냅
- [도트 액션의 손맛 효과](../concepts/game-feel-particles-and-light.md) — 입자 세 무리(타격·몸짓·분위기), 흙덩이 높이·중력, 맞은 쪽 불똥, 상태 없는 환경 입자(자리는 월드 칸에서 — 화면에서 뽑으면 카메라를 따라간다), 더하기 빛 겹
- [액션 게임 적의 쫓기 길찾기](../concepts/enemy-chase-pathfinding-for-action-games.md) — 거리 지도는 땅 + 부딪힘 상자(기둥·문)를 같이, 몸 폭(가운데 + 양옆) 끈 당기기, 처음·끝 반지름은 빼고, 옆으로만 퍼지기, 돌진 띠 = 맞는 곳(폭·끝·쓸고 간 선분·벽에서 멈춤)
- [근접 주인공의 원거리 보스](../concepts/ranged-boss-for-melee-player.md) — 부채꼴 탄 + 되받아치기, 바닥 위험은 발밑 + 둘레·고리 둘(어디·언제)·파내기·무적 굴, 표시 끝 = 판정, 위험물은 적이 아니라 별도 목록
- [적 공격의 박자](../concepts/enemy-attack-rhythm.md) — 정박이 생기는 곳(예고 길이 하나·바닥 타이머·한 방), 엇박 넷(지연·빠름·연속·페인트), 몸 + 소리 신호, 잡몹 조금·보스 많이, 예고 "언제"는 설정, 고리 간격 ≥ 점프 주기, 성공률 봇으로 재기

## 이야기
- [로그라이트 다회차의 세 축](../concepts/roguelite-replay-axes.md) — 실력(단계식·골라 묶기 난이도)·다양성(캐릭터·결)·궁금함(엔딩 뒤 이야기·도감·허브), 일일 시드·보스 다시, 도움 모드, 옆으로 넓히기
- [로그라이트에서 이야기를 전하는 방법](../concepts/roguelite-narrative-delivery.md) — 죽음에 세계 안의 이유, 귀환 대사 = 조건 + 가장 구체적인 것 + 대비책 + 한 번만, 지는 사람도 이야기를 본다, 환경·허브 변화
- [다시 만나는 보스](../concepts/recurring-boss.md) — 만날 때마다 한 수·말 한 줄·눈에 보이는 흔적, 지면 길을 비킨다, 숨는 상태는 hittable 하나로, 같은 시드 = 같은 굴, HUD가 싸움을 가리는 함정, 다시 싸우기 모드(이긴 보스만·기록만·러시)
- [보스 2단계](../concepts/boss-second-phase.md) — 수치가 아니라 읽을 것을 바꾼다: 맞지 않는 짧은 전환(튕김 검사 재사용·터지며 밀쳐냄), 모양 규칙 안의 새 수 하나, 돌진 뒤 잇기, 봇으로 "다름 vs 어려움" 재기
- [두 번째 플레이어 캐릭터](../concepts/second-playable-character.md) — 같은 버튼 자리에 다른 동사(회피·특기·무기 종류), 기록·난이도·엔딩은 캐릭터마다, 보스였던 캐릭터는 그 런 보스를 끄기, 둘째 경로 대사 검수(말하는 이·듣는 이·공유된 진행·UI 글), 선물은 본인 것·이웃 말은 표 하나
- [캐릭터 설정에 쓰는 실제 동물·생태 사실](../reference/nature/animal-behavior-for-character-design.md) — 두더지 독립·침의 독, 라쿤 "손 씻기"는 씻기가 아님, 땅강아지 수렴 진화, 뽕나무버섯, 균근 공생, 다람쥐 저장

## 테스트·연출
- [1인 게임 코드의 건강 신호](../concepts/solo-game-codebase-health-signals.md) — 표로 넓히는 축 vs 틱 함수가 깊어지는 축, 재는 신호(틱 함수 줄 수·구조체 필드 수·부작용 핸들·복붙·테스트 분포), 소리 큐가 테스트 문을 연다, 리팩터링 순서, 다시 짜기는 안 한다
- [개발용 시나리오 진입점과 스텝 스크립트 컷씬](../concepts/dev-scenarios-and-scripted-cutscenes.md) — 시나리오 목록 → 월드 구성, JRPG식 대화창, 길게 눌러 건너뛰기, 배우 좌표계·싸움 끝 연타 함정, 일러스트 장면(2배 밀도 한 장 그림·패닝·입자·내레이션, 홀수 배율), 컷씬이 보간을 얼려 플레이어가 미끄러지는 함정, 고친 뒤 확인 세 겹(수정 전 실패하는 시험·헤드리스·실기)

## 입력·접근성
- [게임 메뉴의 뼈대 — 장면 스택·줄 표·포커스·누를 자리](../concepts/game-menu-scene-stack-and-focus.md) — 창은 얹고 뒤로 = 꺼내기(닫으면 연 줄로), 목록 화면 = 줄 표 하나(입력·그림 공용, 이름 … 값·◀ 값 ▶·→), 포커스 규칙 표(Xbox 112·Microsoft), `(칸, 뜻)` 목록(먼저 넣은 칸이 이긴다·창 밖 = 닫기·▲▼는 제목 줄), 헤드리스 길이 커서 0을 가정하던 함정
- [작은 픽셀 HUD 읽히게 하기](../concepts/hud-readability-and-quick-slots.md) — 바탕판·테두리 글자, 게이지 굵게·가득 신호, 퀵 슬롯 자리 고정·저절로 바꾸기 + 깜빡임, 창 밑 HUD 숨기기
- [컨트롤러 버튼 배치와 다시 붙이기](../concepts/controller-layout-and-remapping.md) — 오른쪽 넷 = 자주 쓰는 넷, 키보드 기본값은 장르 관례로(쿼터뷰 액션 = WASD + 오른손 J·K·L, 플랫포머 = 방향키 + Z·X·C, 메뉴 뒤로는 회피 키 — 키 두 벌은 거둠), 겹치면 맞바꿈, 메뉴 키 고정, 안내는 배치를 따라, 격자 끝에서 옆 탭으로, 되돌릴 수 없는 메뉴 항목은 묻는 창(단추 = 하는 일 이름, 커서는 취소에서)
- [액션 게임 키보드·마우스 배치](../concepts/keyboard-and-mouse-layout-for-action-games.md) — 소울라이크·Hades·Diablo·PoE 2 기본 키, 마우스의 일은 카메라가 정한다(3인칭 = 카메라·탑다운 = 조준·ARPG = 이동), 왼손은 WASD 둘레에서 빈도 순, 조합키는 패드 직역의 흔적, 프리셋으로 덧붙이기, 스캔코드(miniquad Linux는 글자)
- [액션 게임 터치 배치](../concepts/touch-action-layout.md) — 공격 둘레 호(자주 쓰는 넷), 상황 버튼은 제 자리에만(쓸 수 없으면 숨김), 합칠 수 있으면 합치기(점프 = 상호작용), 짝 버튼은 캡슐, 배치는 순수 함수 + 시험

## 판매·비즈니스
- [Rust 게임을 Steam에 붙이기](../guides/steam-release-for-rust-games.md) — Cargo 기능 하나로 PC만·연결 없으면 그냥 켜기, SDK 재배포 파일은 크레이트가 복사(커밋 안 함), 업적 = 목표 목록에서 고른 표(API 이름 고정·숨김·등록표는 시험이 만든다·아이콘은 있는 그림에서), Auto-Cloud, 빌더 계정 + config.vdf + beta까지만 자동, macOS 공증은 필수 아님(2차), 가격 바닥 $0.99, Deck 글자 9px·패드 글자만
- [Rust 게임을 Epic Games Store에 붙이기](../guides/epic-games-store-for-rust-games.md) — Cargo 기능 epic(Windows만), 런처 교환 코드 → Epic 계정 → ID 토큰 → EOS Connect(처음이면 사용자 만들기) → 업적, eos-sys 바인딩에 업적 함수가 없어 직접 extern, EOS 일괄 CSV 두 장 + 아이콘 zip, Epic 상점 XP 합 1,000(5~200·5의 배수, 올린 뒤 못 바꿈), BuildPatchTool UploadBinary
- [인디 게임을 팔 때의 규칙과 숫자](../reference/game-business/selling-an-indie-game-rules-and-numbers.md) — Steam Direct·Coming Soon 2주·Next Fest 게임당 한 번·AI 공개(Pre/Live-Generated)·원천징수(한국 저작권 10%), 위시리스트 전환·AI 표시 게임의 성과, Play(한국 15%)·Android 개발자 확인·Apple·itch, Gemini 약관, 한국 비영리 등급 면제

## 다국어
- [작은 게임 다국어 구조](../guides/small-game-localization.md) — 고정 키 표, 자리표시자, 폰트 커버리지 테스트, 브라우저 언어 읽기
- [중국어·일본어 픽셀 폰트](../reference/fonts/cjk-pixel-fonts.md) — 중국어 폰트 ≠ 일본어 폰트, Ark Pixel·Fusion·Galmuri 범위와 라이선스
- [게임 UI용 한글 명조](../reference/fonts/korean-serif-ui-fonts.md) — 고운바탕(11,172자·정적 굵기) vs 함렛(2,788자·가변 — fontdue는 축을 못 고름), 표 글자 서브셋 크기

## 엔진·플랫폼 선택
- [Rust 게임 엔진 비교: 웹 + Android 핸드헬드 + 컨트롤러](../reference/rust-game-engines/web-android-gamepad-support.md) — macroquad / Bevy / Godot, Android 게임패드가 공통 공백(macroquad는 버튼만 패치로 해결)

## macroquad
- 입력
  - [게임패드와 Android 입력 현황](../reference/macroquad/gamepad-and-android-input.md) — `gamepads` 크레이트, miniquad Android 백엔드의 공백과 패치 범위, 메뉴 스틱 탐색(히스테리시스), 모바일 웹 실제 키보드(번들은 캔버스·`e.code`만 — 포커스 밖·빈 code를 창 capture에서 채워 넘기기, iPad 웹앱은 touchstart preventDefault가 키를 죽인다), 키는 자리로·이름은 배열 글자로(플랫폼별 표·얻는 API, Linux는 evdev 패치, Xvfb 배열 시험 요령)
- 렌더링
  - [픽셀 퍼펙트 렌더링](../reference/macroquad/pixel-perfect-rendering.md) — 내부 해상도 320×180, render target, Nearest, 정수 배율
  - [오래 켜면 죽을 때: GPU 메모리가 자라는 원인과 재는 법](../reference/macroquad/gpu-memory-growth.md) — `telemetry::capture_frame`이 텍스처를 흘림, 호출 칸 버퍼는 최댓값을 쥠, WebGL 탐침, Rust 힙 도구
  - [글자 그리기 비용과 브라우저 프레임레이트](../reference/macroquad/text-rendering-and-browser-frame-rate.md) — 아틀라스 통째 올리기, 픽셀 폰트는 원래 크기로 굽고 정수배, 미리 굽기, WebGL 안티에일리어싱 끄기, Safari 저전력 30fps
- 빌드·배포
  - [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](../guides/macroquad-wasm-netlify-github-actions.md) — 전체 절차
  - [macroquad를 GitHub Actions에서 Android APK로](../guides/macroquad-android-apk-github-actions.md) — cargo-quad-apk git 고정, 러너 내장 SDK/NDK, gamepads 제외, 서명 키는 Secret에
  - [macroquad iOS 빌드](../reference/macroquad/ios-build.md) — macOS 러너로 서명 안 한 .ipa, Info.plist 최소 키, 샌드박스 저장 자리, 서명 갈림길(무료 7일 / $99 TestFlight), 패드는 gilrs에 iOS 없음
  - [macroquad PC 빌드](../reference/macroquad/desktop-build.md) — Windows·macOS(겸용 .app, lipo 뒤 임시 서명)·Linux(libudev-dev) 묶음, 에셋 경로를 실행 파일 기준으로(데스크톱은 작업 폴더 기준이라 바로가기로 켜면 못 찾는다), 공증
  - [버전 올리기 = 릴리스](../reference/github-actions/release-from-version-bump.md) — 본문 파일이 스위치, CI가 태그·APK·Release
  - [WASM 빌드와 JS 번들](../reference/macroquad/wasm-build.md) — 번들 버전 계약, 에셋 로딩, 정수로 주고받는 내 플러그인(localStorage 설정 저장), 번들을 고치지 않는 로딩 화면
  - [소리(quad-snd)](../reference/macroquad/audio.md) — 네이티브 wav·ogg만·통째로 f32 44.1kHz(1분 ≈ 21MB)·가까운 점 리샘플·음높이 없음, 웹 mp3/네이티브 ogg, 교차는 직접, 들을 때 읽고 놓기(네이티브는 푸는 동안 멈칫)
  - [정적 WASM 호스팅](../concepts/static-wasm-hosting.md) — 왜 번들러가 없어도 되는가
  - [0001 빌드는 CI, 호스팅은 Netlify](../decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md)

## 아직 없는 것
- 컷씬·전환을 포함한 장면 상태 관리(메뉴 쪽은 위 "게임 메뉴의 뼈대") — 노트가 생기면 추가

## 다른 지도
- [Rust](rust.md) · [CI/CD와 호스팅](ci-cd-hosting.md)
