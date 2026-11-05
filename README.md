# KB

개인 지식 베이스. "왜?"에 답할 수 있을 때까지 파고든 내용만 남긴다.

## 구조

노트는 **도메인이 아니라 "노트의 종류"** 로 저장하고([Diátaxis](https://diataxis.fr/) 차용), **도메인별 탐색은 `maps/`의 지도 노트**로 한다.

```
KB/
├── README.md          # 규칙 + 자동 생성 인덱스
├── CLAUDE.md          # Claude Code가 이 KB를 읽고 쓰는 규칙
├── _templates/        # 노트 템플릿 (note.md, map.md)
├── maps/              # 도메인별 입구(Map of Content). 링크만 모은다
├── guides/            # How-to. "X를 하려면" — 여러 도구를 엮은 절차
├── reference/<tool>/  # 사실 정리. 도구/기술 단위 하위 폴더
├── concepts/          # 원리 설명. "왜 그렇게 동작하나"
├── decisions/         # 의사결정 기록(ADR). "왜 A가 아니라 B를 택했나"
└── tools/kb.py        # check(검증) / index(인덱스 생성)
```

### 왜 저장은 종류별, 탐색은 지도로 하는가

- 하나의 주제가 여러 도메인에 걸치는 일이 흔하다. 예: "macroquad를 Netlify에 GitHub Actions로 배포"는 게임개발·Rust·CI 세 도메인이다. 폴더는 한 곳에만 둘 수 있지만 지도에는 여러 곳에 실을 수 있다.
- 종류는 5개로 고정되어 폴더가 흔들리지 않는다. 도메인은 `tags`와 `maps/`로 표현하므로 새 도메인이 생겨도 폴더를 옮길 일이 없다.
- 읽는 목적이 다르다. 절차가 급할 때는 `guides/`, 사실 확인은 `reference/`, 이해가 필요하면 `concepts/`, "그때 왜 그랬지"는 `decisions/`, "이 분야에 뭐가 있지"는 `maps/`.

### 무엇을 넣고 무엇을 넣지 않는가

판별 기준은 하나다. **"이 프로젝트가 사라져도 유용한가?"**
- 예 → KB. (Netlify CLI 동작 방식, Rust 캐시가 중요한 이유)
- 아니오 → 그 프로젝트 레포. (특정 게임의 TODO, 오늘 깨진 빌드 로그, 회의 메모)

프로젝트 기록이 섞이면 검색 결과가 썩는다. 지식만 둔다.

### 각 폴더의 규칙

| 폴더 | 한 노트의 단위 | 파일명 |
|---|---|---|
| `maps/` | 하나의 도메인 | `<도메인>.md` |
| `guides/` | 하나의 목표(end-to-end) | `<목표-설명>.md` (kebab-case) |
| `reference/<tool>/` | 하나의 도구 × 하나의 주제 | `<주제>.md` |
| `concepts/` | 하나의 개념 | `<개념>.md` |
| `decisions/` | 하나의 결정 | `NNNN-<결정-요약>.md` (번호 순차) |

- 가이드는 reference를 **중복하지 않고 링크**한다. 사실은 reference 한 곳에만 둔다.
- 모든 노트는 `_templates/`의 frontmatter를 갖는다. 특히 `verified`에 **1차 출처로 확인한 것과 포럼 수준 출처만 있는 것을 구분**해 적는다.
- `status`: `draft` → `verified` → (시간이 지나 의심되면) `stale`.
- 외부 자료는 요약만 남기고 원문 URL을 `sources`에 적는다.
- 새 노트는 **최소 한 지도에 실어야 한다.** 실을 지도가 없으면 새 도메인이니 `_templates/map.md`로 지도를 만든다.

### 도구

```sh
python3 tools/kb.py check   # frontmatter·폴더 일치·끊어진 링크·지도 수록 여부 검증
python3 tools/kb.py index   # 아래 인덱스 섹션 재생성
```
GitHub Actions(`kb-check`)가 push/PR마다 둘을 실행한다. 인덱스가 오래되면 실패한다.

## 인덱스

<!-- index:start -->

_`python3 tools/kb.py index` 로 생성. 손으로 고치지 말 것._

### 지도 (도메인별 입구)
- [지도: CI/CD와 호스팅](maps/ci-cd-hosting.md)
- [지도: 게임 개발](maps/gamedev.md)
- [지도: Rust](maps/rust.md)

### guides
- [AI 3D 메시(Meshy 등)를 작은 게임용 강체 부위 모델로 — 줄이기·색 굽기·부위 자르기](guides/ai-mesh-to-rigid-part-model.md)
- [게임 화면 색약 점검 — 시뮬레이션 행렬로 스크린숏을 돌려 보기](guides/color-vision-check-for-games.md)
- [게임 그림 외주 맡기기 — 사양서와 계약 체크리스트(한국 저작권법 기준)](guides/commissioning-game-art.md)
- [운영판과 개발판을 갈라 내보내기 — 마일스톤 갈래, Cargo 기능, 따로 열고 따로 깔기](guides/dev-and-release-flavors.md)
- [Rust 게임을 Epic Games Store에 붙이기 — EOS 로그인·업적, 일괄 올리기 파일, BuildPatchTool](guides/epic-games-store-for-rust-games.md)
- [작곡가·음향 담당 없이 게임 소리 넣기 (CC0 출처·숫자로 고르기·섞기)](guides/game-audio-without-a-composer.md)
- [이미지 생성 모델(나노바나나)로 게임 일러스트 그리기 — 참고 그림·프롬프트·격자](guides/image-model-for-game-illustrations.md)
- [인디 게임 공식 페이지 — 무엇을 싣고, 도트 게임답게 움직이기](guides/indie-game-landing-page.md)
- [macroquad 게임을 GitHub Actions에서 Android APK로 빌드하기 (cargo-quad-apk)](guides/macroquad-android-apk-github-actions.md)
- [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md)
- [그림 못 그려도 도트 게임 만들기 (에셋 전략)](guides/pixel-art-without-an-artist.md)
- [PoC와 Lab — 콘텐츠보다 먼저, 수치는 사람이 화면에서 정한다](guides/poc-and-lab-before-content.md)
- [공개 레포에서 배포 파이프라인 지키기 — Environment·브랜치 규칙·CODEOWNERS](guides/protect-deploy-pipeline-in-public-repo.md)
- [브랜치 히스토리의 파일을 고친 판으로 바꿔 쓰기(force push 전후)](guides/rewrite-branch-history-replace-files.md)
- [두 번째 게임 프로젝트의 첫날 — 첫 게임에서 배운 것을 처음부터 깔기](guides/second-game-project-day-one.md)
- [작은 게임 다국어(현지화) 구조 — 고정 키 표, 자리표시자, 폰트 커버리지 테스트](guides/small-game-localization.md)
- [Rust 게임을 Steam에 붙이기 — 기능 하나로 가르기, 업적 표, 클라우드, 업로드 파이프라인, Deck](guides/steam-release-for-rust-games.md)

### reference
- assets
  - [무료(CC0·퍼블릭 도메인) 그림·사진 구하는 곳과 API 요령](reference/assets/free-image-sources.md)
  - [레트로 3D 모델 파이프라인 — Blockbench 상자 모델 → glTF(부위 강체 애니메이션) → 직접 로더](reference/assets/retro-3d-models-blockbench-gltf.md)
- fonts
  - [중국어·일본어 픽셀 폰트 — 한자 통합, 글자 범위, 12px 후보](reference/fonts/cjk-pixel-fonts.md)
  - [게임 UI용 한글 명조 — 고운바탕 vs 함렛, 가변 글꼴과 macroquad, 서브셋 크기](reference/fonts/korean-serif-ui-fonts.md)
- game-business
  - [인디 게임을 팔 때의 규칙과 숫자 — Steam·Epic·Play·Apple·itch, AI 공개, 위시리스트, 한국 세금·등급](reference/game-business/selling-an-indie-game-rules-and-numbers.md)
- github-actions
  - [GitHub Actions의 Node 20 폐기 — 액션을 node24 판으로 올리기](reference/github-actions/node24-action-runtime.md)
  - [GitHub Pages에 정적 페이지 올리기 — Actions 배포, 처음 켜기, 릴리스에서 읽는 값](reference/github-actions/pages-static-site.md)
  - [GitHub Actions의 액션과 Rust 버전 고정하기 — SHA 고정·Dependabot·잠금 파일, dtolnay/rust-toolchain을 SHA로 쓸 때](reference/github-actions/pin-actions-and-rust-toolchain.md)
  - [GitHub Actions에서 Playwright 연기 시험이 느려질 때 — `--with-deps`의 apt 글꼴과 같은 커밋 두 번 돌리기](reference/github-actions/playwright-smoke-test-ci-time.md)
  - [공개 레포를 비공개로 바꿀 때 — Actions 비용·Pages·Release가 어떻게 되나](reference/github-actions/public-to-private-repo.md)
  - [버전 올리기 = 릴리스 — CI가 태그를 만들고 빌드를 직접 부르기](reference/github-actions/release-from-version-bump.md)
  - [GitHub Actions에서 Rust → wasm32 빌드](reference/github-actions/rust-wasm-build.md)
- macroquad
  - [macroquad 3D 렌더링 — Camera3D·Mesh·배치·조명 없음·모델 로더 없음](reference/macroquad/3d-rendering.md)
  - [macroquad 소리(quad-snd) — 형식·메모리·음악 재생의 제약](reference/macroquad/audio.md)
  - [macroquad PC 빌드 — Windows·macOS·Linux 묶음, 에셋 경로 함정, 서명](reference/macroquad/desktop-build.md)
  - [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md)
  - [macroquad 앱이 오래 켜면 죽을 때 — GPU 메모리가 자라는 두 원인과 재는 법](reference/macroquad/gpu-memory-growth.md)
  - [macroquad iOS 빌드 — GitHub Actions macOS 러너로 서명 안 한 .ipa, 기기 시험·배포의 갈림길](reference/macroquad/ios-build.md)
  - [macroquad 픽셀 퍼펙트 렌더링 (내부 해상도 고정 + 정수 배율)](reference/macroquad/pixel-perfect-rendering.md)
  - [macroquad 글자 그리기 비용과 브라우저 프레임레이트 — 아틀라스 통째 올리기, 레티나, WebGL 안티에일리어싱 기본값, Safari 저전력 30fps](reference/macroquad/text-rendering-and-browser-frame-rate.md)
  - [macroquad WASM 빌드와 JS 번들](reference/macroquad/wasm-build.md)
- nature
  - [캐릭터 설정에 쓰는 실제 동물·생태 사실](reference/nature/animal-behavior-for-character-design.md)
- netlify
  - [CI에서 netlify-cli로 배포](reference/netlify/deploy-from-ci.md)
- rust-game-engines
  - [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- web
  - [웹 게임을 PWA로: 설치·오프라인·전체 화면·가로 잠금(Chrome·Android·iPhone)](reference/web/pwa-install-fullscreen-orientation.md)

### concepts
- [3D 도트 룩(t3ssel8r 풍) — 낮은 해상도·툰 빛·선 둘(어두운 가장자리 + 밝은 볼록 모서리)·카메라 픽셀 맞춤](concepts/3d-pixel-art-look.md)
- [모든 행동에 재사용 대기 — 동작 시간·대기·게이지·먹는 시간](concepts/action-reuse-gating.md)
- [1인 개발용 액션 로그라이트 설계 원칙](concepts/action-roguelite-for-solo-dev.md)
- [액션 RPG의 능력치·장비 설계 — 무기는 모양, 장신구는 수치, 성장은 영구](concepts/action-rpg-stats-and-equipment.md)
- [탑다운 모험 구조 — 격자 하나, 카메라 경계 사각형, 방 그래프 던전](concepts/adventure-field-and-procedural-dungeon.md)
- [실감나게 귀여운 캐릭터 동작 — 애니메이션 원칙을 게임 반응성과 작은 화면에 맞추기](concepts/believable-cute-character-motion.md)
- [선형 진행을 갈래 길로 느끼게 하는 지도](concepts/branching-route-map.md)
- [시점 전환(쿼터뷰 ↔ 숄더뷰)과 락온 카메라 — 하나의 전투, 두 개의 구도](concepts/camera-mode-switch-and-lock-on.md)
- [컨트롤러 버튼 배치와 다시 붙이기 — 오른쪽 넷은 자주 쓰는 넷, 메뉴 키는 고정, 안내는 배치를 따라](concepts/controller-layout-and-remapping.md)
- [깊이 내려간다"를 보이게 하기 — 전환·깊이 숫자·지도 방향·방 안의 위](concepts/conveying-descent.md)
- [어두운 세계의 귀여운 캐릭터 — 2등신 문법과 "색 = 생명](concepts/cute-characters-in-a-dark-world.md)
- [개발용 시나리오 진입점과 스텝 스크립트 컷씬](concepts/dev-scenarios-and-scripted-cutscenes.md)
- [고정 타임스텝 게임 루프와 히트스톱](concepts/fixed-timestep-and-hitstop.md)
- [도트 액션의 손맛 효과 — 입자·빛·환경 입자·그림자](concepts/game-feel-particles-and-light.md)
- [작은 픽셀 HUD 읽히게 하기 — 바탕판·테두리 글자, 퀵 슬롯 고정 자리와 저절로 바꾸기](concepts/hud-readability-and-quick-slots.md)
- [액션 게임 키보드·마우스 배치 — 마우스의 일은 카메라가 정하고, 왼손은 WASD 둘레에서 빈도 순](concepts/keyboard-and-mouse-layout-for-action-games.md)
- [근접 평타·모으기 공격의 손맛 — 누르는 순간, 작은 타격의 피드백 층, 모으기의 보상](concepts/melee-light-and-charged-attack-feel.md)
- [영구 성장(재주 나무) 해금을 계획할 수 있게 — 다 보이는 칸, 그림, 거기까지의 값, 목표 핀](concepts/meta-progression-unlock-planning.md)
- [인디 게임 공개 데모와 바깥 의견 받기](concepts/public-demo-and-outside-feedback.md)
- [근접 주인공의 원거리 보스 — 되받아치는 탄, 비키거나 파내는 바닥 위험](concepts/ranged-boss-for-melee-player.md)
- [작게 보이는 로우폴리 모델을 읽히게 — 깊이·외곽선·빛 단계·실루엣, 그리고 하지 말 것](concepts/readable-low-poly-models.md)
- [다시 만나는 보스 — 만날 때마다 한 수, 지면 길을 비킨다](concepts/recurring-boss.md)
- [액션 로그라이트의 회복과 화폐 드롭 — 깎인 만큼·불운 보정·자석](concepts/roguelite-healing-and-currency.md)
- [로그라이트 저널(목표 목록) — 평소 플레이를 장기 목표로, 받기로 보상](concepts/roguelite-journal-goals.md)
- [로그라이트에서 이야기를 전하는 방법](concepts/roguelite-narrative-delivery.md)
- [로그라이트 다회차의 세 축 — 실력·다양성·궁금함](concepts/roguelite-replay-axes.md)
- [로그라이트 방이 반복되게 느껴질 때 — 모양보다 방마다의 판단을 바꾼다](concepts/roguelite-room-variety.md)
- [로그라이트의 저장 슬롯·이어하기·런 중단 저장](concepts/roguelite-save-slots-and-continue.md)
- [두 번째 플레이어 캐릭터 — 같은 버튼, 다른 동사](concepts/second-playable-character.md)
- [1인 게임 코드의 건강 신호 — 표로 넓히는 축, 틱 함수가 깊어지는 축, 소리 때문에 못 돌리는 테스트](concepts/solo-game-codebase-health-signals.md)
- [필살기의 임팩트 — 시동 정지, 거리, 끌고 가기, 소리 하나](concepts/special-move-impact.md)
- [정적 WASM 호스팅](concepts/static-wasm-hosting.md)
- [놀이 칸 밖 채우기 — 높이 안개·떠다니는 것·원경·식생(작은 3D 도트 게임)](concepts/surroundings-beyond-the-play-area.md)
- [공격 타이밍 패링 — 버튼 없이 맞받기, 굴/회피와 역할 나누기](concepts/timing-parry.md)
- [액션 게임 터치 배치 — 공격 둘레 호, 상황 버튼은 제 자리에만, 버튼 수가 복잡도](concepts/touch-action-layout.md)
- [미니맵 없이 길 알려 주기 — 환경 빛 + 화면 밖 화살 + 목표 글, 같은 규칙을 끝까지](concepts/wayfinding-without-a-minimap.md)

### decisions
- [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md)

### 태그
- `3d`: [3D 도트 룩(t3ssel8r 풍) — 낮은 해상도·툰 빛·선 둘(어두운 가장자리 + 밝은 볼록 모서리)·카메라 픽셀 맞춤](concepts/3d-pixel-art-look.md), [실감나게 귀여운 캐릭터 동작 — 애니메이션 원칙을 게임 반응성과 작은 화면에 맞추기](concepts/believable-cute-character-motion.md), [시점 전환(쿼터뷰 ↔ 숄더뷰)과 락온 카메라 — 하나의 전투, 두 개의 구도](concepts/camera-mode-switch-and-lock-on.md), [어두운 세계의 귀여운 캐릭터 — 2등신 문법과 "색 = 생명](concepts/cute-characters-in-a-dark-world.md), [작게 보이는 로우폴리 모델을 읽히게 — 깊이·외곽선·빛 단계·실루엣, 그리고 하지 말 것](concepts/readable-low-poly-models.md), [AI 3D 메시(Meshy 등)를 작은 게임용 강체 부위 모델로 — 줄이기·색 굽기·부위 자르기](guides/ai-mesh-to-rigid-part-model.md), [레트로 3D 모델 파이프라인 — Blockbench 상자 모델 → glTF(부위 강체 애니메이션) → 직접 로더](reference/assets/retro-3d-models-blockbench-gltf.md), [macroquad 3D 렌더링 — Camera3D·Mesh·배치·조명 없음·모델 로더 없음](reference/macroquad/3d-rendering.md)
- `accessibility`: [컨트롤러 버튼 배치와 다시 붙이기 — 오른쪽 넷은 자주 쓰는 넷, 메뉴 키는 고정, 안내는 배치를 따라](concepts/controller-layout-and-remapping.md), [액션 게임 키보드·마우스 배치 — 마우스의 일은 카메라가 정하고, 왼손은 WASD 둘레에서 빈도 순](concepts/keyboard-and-mouse-layout-for-action-games.md), [액션 게임 터치 배치 — 공격 둘레 호, 상황 버튼은 제 자리에만, 버튼 수가 복잡도](concepts/touch-action-layout.md), [미니맵 없이 길 알려 주기 — 환경 빛 + 화면 밖 화살 + 목표 글, 같은 규칙을 끝까지](concepts/wayfinding-without-a-minimap.md), [게임 화면 색약 점검 — 시뮬레이션 행렬로 스크린숏을 돌려 보기](guides/color-vision-check-for-games.md)
- `achievements`: [Rust 게임을 Epic Games Store에 붙이기 — EOS 로그인·업적, 일괄 올리기 파일, BuildPatchTool](guides/epic-games-store-for-rust-games.md), [Rust 게임을 Steam에 붙이기 — 기능 하나로 가르기, 업적 표, 클라우드, 업로드 파이프라인, Deck](guides/steam-release-for-rust-games.md)
- `ai-assets`: [작게 보이는 로우폴리 모델을 읽히게 — 깊이·외곽선·빛 단계·실루엣, 그리고 하지 말 것](concepts/readable-low-poly-models.md), [AI 3D 메시(Meshy 등)를 작은 게임용 강체 부위 모델로 — 줄이기·색 굽기·부위 자르기](guides/ai-mesh-to-rigid-part-model.md)
- `ai-image`: [이미지 생성 모델(나노바나나)로 게임 일러스트 그리기 — 참고 그림·프롬프트·격자](guides/image-model-for-game-illustrations.md), [인디 게임을 팔 때의 규칙과 숫자 — Steam·Epic·Play·Apple·itch, AI 공개, 위시리스트, 한국 세금·등급](reference/game-business/selling-an-indie-game-rules-and-numbers.md)
- `android`: [운영판과 개발판을 갈라 내보내기 — 마일스톤 갈래, Cargo 기능, 따로 열고 따로 깔기](guides/dev-and-release-flavors.md), [macroquad 게임을 GitHub Actions에서 Android APK로 빌드하기 (cargo-quad-apk)](guides/macroquad-android-apk-github-actions.md), [버전 올리기 = 릴리스 — CI가 태그를 만들고 빌드를 직접 부르기](reference/github-actions/release-from-version-bump.md), [macroquad 소리(quad-snd) — 형식·메모리·음악 재생의 제약](reference/macroquad/audio.md), [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md), [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md), [웹 게임을 PWA로: 설치·오프라인·전체 화면·가로 잠금(Chrome·Android·iPhone)](reference/web/pwa-install-fullscreen-orientation.md)
- `animals`: [캐릭터 설정에 쓰는 실제 동물·생태 사실](reference/nature/animal-behavior-for-character-design.md)
- `animation`: [실감나게 귀여운 캐릭터 동작 — 애니메이션 원칙을 게임 반응성과 작은 화면에 맞추기](concepts/believable-cute-character-motion.md), [AI 3D 메시(Meshy 등)를 작은 게임용 강체 부위 모델로 — 줄이기·색 굽기·부위 자르기](guides/ai-mesh-to-rigid-part-model.md), [레트로 3D 모델 파이프라인 — Blockbench 상자 모델 → glTF(부위 강체 애니메이션) → 직접 로더](reference/assets/retro-3d-models-blockbench-gltf.md)
- `apk`: [macroquad 게임을 GitHub Actions에서 Android APK로 빌드하기 (cargo-quad-apk)](guides/macroquad-android-apk-github-actions.md)
- `architecture`: [1인 게임 코드의 건강 신호 — 표로 넓히는 축, 틱 함수가 깊어지는 축, 소리 때문에 못 돌리는 테스트](concepts/solo-game-codebase-health-signals.md), [두 번째 게임 프로젝트의 첫날 — 첫 게임에서 배운 것을 처음부터 깔기](guides/second-game-project-day-one.md)
- `art`: [어두운 세계의 귀여운 캐릭터 — 2등신 문법과 "색 = 생명](concepts/cute-characters-in-a-dark-world.md), [작게 보이는 로우폴리 모델을 읽히게 — 깊이·외곽선·빛 단계·실루엣, 그리고 하지 말 것](concepts/readable-low-poly-models.md), [게임 화면 색약 점검 — 시뮬레이션 행렬로 스크린숏을 돌려 보기](guides/color-vision-check-for-games.md)
- `art-direction`: [3D 도트 룩(t3ssel8r 풍) — 낮은 해상도·툰 빛·선 둘(어두운 가장자리 + 밝은 볼록 모서리)·카메라 픽셀 맞춤](concepts/3d-pixel-art-look.md), [놀이 칸 밖 채우기 — 높이 안개·떠다니는 것·원경·식생(작은 3D 도트 게임)](concepts/surroundings-beyond-the-play-area.md)
- `art-pipeline`: [AI 3D 메시(Meshy 등)를 작은 게임용 강체 부위 모델로 — 줄이기·색 굽기·부위 자르기](guides/ai-mesh-to-rigid-part-model.md), [이미지 생성 모델(나노바나나)로 게임 일러스트 그리기 — 참고 그림·프롬프트·격자](guides/image-model-for-game-illustrations.md)
- `assets`: [게임 그림 외주 맡기기 — 사양서와 계약 체크리스트(한국 저작권법 기준)](guides/commissioning-game-art.md), [작곡가·음향 담당 없이 게임 소리 넣기 (CC0 출처·숫자로 고르기·섞기)](guides/game-audio-without-a-composer.md), [그림 못 그려도 도트 게임 만들기 (에셋 전략)](guides/pixel-art-without-an-artist.md), [무료(CC0·퍼블릭 도메인) 그림·사진 구하는 곳과 API 요령](reference/assets/free-image-sources.md), [레트로 3D 모델 파이프라인 — Blockbench 상자 모델 → glTF(부위 강체 애니메이션) → 직접 로더](reference/assets/retro-3d-models-blockbench-gltf.md)
- `audio`: [작곡가·음향 담당 없이 게임 소리 넣기 (CC0 출처·숫자로 고르기·섞기)](guides/game-audio-without-a-composer.md), [macroquad 소리(quad-snd) — 형식·메모리·음악 재생의 제약](reference/macroquad/audio.md)
- `bevy`: [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- `blender`: [AI 3D 메시(Meshy 등)를 작은 게임용 강체 부위 모델로 — 줄이기·색 굽기·부위 자르기](guides/ai-mesh-to-rigid-part-model.md), [레트로 3D 모델 파이프라인 — Blockbench 상자 모델 → glTF(부위 강체 애니메이션) → 직접 로더](reference/assets/retro-3d-models-blockbench-gltf.md)
- `blockbench`: [레트로 3D 모델 파이프라인 — Blockbench 상자 모델 → glTF(부위 강체 애니메이션) → 직접 로더](reference/assets/retro-3d-models-blockbench-gltf.md)
- `boss`: [근접 주인공의 원거리 보스 — 되받아치는 탄, 비키거나 파내는 바닥 위험](concepts/ranged-boss-for-melee-player.md), [다시 만나는 보스 — 만날 때마다 한 수, 지면 길을 비킨다](concepts/recurring-boss.md)
- `business`: [인디 게임을 팔 때의 규칙과 숫자 — Steam·Epic·Play·Apple·itch, AI 공개, 위시리스트, 한국 세금·등급](reference/game-business/selling-an-indie-game-rules-and-numbers.md)
- `camera`: [탑다운 모험 구조 — 격자 하나, 카메라 경계 사각형, 방 그래프 던전](concepts/adventure-field-and-procedural-dungeon.md), [시점 전환(쿼터뷰 ↔ 숄더뷰)과 락온 카메라 — 하나의 전투, 두 개의 구도](concepts/camera-mode-switch-and-lock-on.md), [macroquad 3D 렌더링 — Camera3D·Mesh·배치·조명 없음·모델 로더 없음](reference/macroquad/3d-rendering.md)
- `ci`: [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md), [운영판과 개발판을 갈라 내보내기 — 마일스톤 갈래, Cargo 기능, 따로 열고 따로 깔기](guides/dev-and-release-flavors.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [지도: CI/CD와 호스팅](maps/ci-cd-hosting.md), [GitHub Actions에서 Rust → wasm32 빌드](reference/github-actions/rust-wasm-build.md), [CI에서 netlify-cli로 배포](reference/netlify/deploy-from-ci.md)
- `ci-cd`: [macroquad 게임을 GitHub Actions에서 Android APK로 빌드하기 (cargo-quad-apk)](guides/macroquad-android-apk-github-actions.md), [공개 레포에서 배포 파이프라인 지키기 — Environment·브랜치 규칙·CODEOWNERS](guides/protect-deploy-pipeline-in-public-repo.md), [두 번째 게임 프로젝트의 첫날 — 첫 게임에서 배운 것을 처음부터 깔기](guides/second-game-project-day-one.md), [GitHub Actions의 Node 20 폐기 — 액션을 node24 판으로 올리기](reference/github-actions/node24-action-runtime.md), [GitHub Pages에 정적 페이지 올리기 — Actions 배포, 처음 켜기, 릴리스에서 읽는 값](reference/github-actions/pages-static-site.md), [GitHub Actions의 액션과 Rust 버전 고정하기 — SHA 고정·Dependabot·잠금 파일, dtolnay/rust-toolchain을 SHA로 쓸 때](reference/github-actions/pin-actions-and-rust-toolchain.md), [GitHub Actions에서 Playwright 연기 시험이 느려질 때 — `--with-deps`의 apt 글꼴과 같은 커밋 두 번 돌리기](reference/github-actions/playwright-smoke-test-ci-time.md), [공개 레포를 비공개로 바꿀 때 — Actions 비용·Pages·Release가 어떻게 되나](reference/github-actions/public-to-private-repo.md), [버전 올리기 = 릴리스 — CI가 태그를 만들고 빌드를 직접 부르기](reference/github-actions/release-from-version-bump.md)
- `cjk`: [중국어·일본어 픽셀 폰트 — 한자 통합, 글자 범위, 12px 후보](reference/fonts/cjk-pixel-fonts.md)
- `combat`: [모든 행동에 재사용 대기 — 동작 시간·대기·게이지·먹는 시간](concepts/action-reuse-gating.md), [1인 개발용 액션 로그라이트 설계 원칙](concepts/action-roguelite-for-solo-dev.md), [액션 RPG의 능력치·장비 설계 — 무기는 모양, 장신구는 수치, 성장은 영구](concepts/action-rpg-stats-and-equipment.md), [근접 평타·모으기 공격의 손맛 — 누르는 순간, 작은 타격의 피드백 층, 모으기의 보상](concepts/melee-light-and-charged-attack-feel.md), [근접 주인공의 원거리 보스 — 되받아치는 탄, 비키거나 파내는 바닥 위험](concepts/ranged-boss-for-melee-player.md), [필살기의 임팩트 — 시동 정지, 거리, 끌고 가기, 소리 하나](concepts/special-move-impact.md), [공격 타이밍 패링 — 버튼 없이 맞받기, 굴/회피와 역할 나누기](concepts/timing-parry.md)
- `controller`: [시점 전환(쿼터뷰 ↔ 숄더뷰)과 락온 카메라 — 하나의 전투, 두 개의 구도](concepts/camera-mode-switch-and-lock-on.md)
- `css`: [인디 게임 공식 페이지 — 무엇을 싣고, 도트 게임답게 움직이기](guides/indie-game-landing-page.md)
- `cute`: [실감나게 귀여운 캐릭터 동작 — 애니메이션 원칙을 게임 반응성과 작은 화면에 맞추기](concepts/believable-cute-character-motion.md), [어두운 세계의 귀여운 캐릭터 — 2등신 문법과 "색 = 생명](concepts/cute-characters-in-a-dark-world.md)
- `cutscene`: [개발용 시나리오 진입점과 스텝 스크립트 컷씬](concepts/dev-scenarios-and-scripted-cutscenes.md)
- `debugging`: [macroquad 앱이 오래 켜면 죽을 때 — GPU 메모리가 자라는 두 원인과 재는 법](reference/macroquad/gpu-memory-growth.md)
- `demo`: [인디 게임 공개 데모와 바깥 의견 받기](concepts/public-demo-and-outside-feedback.md)
- `deploy`: [운영판과 개발판을 갈라 내보내기 — 마일스톤 갈래, Cargo 기능, 따로 열고 따로 깔기](guides/dev-and-release-flavors.md), [지도: CI/CD와 호스팅](maps/ci-cd-hosting.md), [CI에서 netlify-cli로 배포](reference/netlify/deploy-from-ci.md)
- `dialogue`: [로그라이트에서 이야기를 전하는 방법](concepts/roguelite-narrative-delivery.md)
- `ecology`: [캐릭터 설정에 쓰는 실제 동물·생태 사실](reference/nature/animal-behavior-for-character-design.md)
- `epic`: [Rust 게임을 Epic Games Store에 붙이기 — EOS 로그인·업적, 일괄 올리기 파일, BuildPatchTool](guides/epic-games-store-for-rust-games.md), [인디 게임을 팔 때의 규칙과 숫자 — Steam·Epic·Play·Apple·itch, AI 공개, 위시리스트, 한국 세금·등급](reference/game-business/selling-an-indie-game-rules-and-numbers.md)
- `fog`: [놀이 칸 밖 채우기 — 높이 안개·떠다니는 것·원경·식생(작은 3D 도트 게임)](concepts/surroundings-beyond-the-play-area.md)
- `fonts`: [작은 게임 다국어(현지화) 구조 — 고정 키 표, 자리표시자, 폰트 커버리지 테스트](guides/small-game-localization.md), [중국어·일본어 픽셀 폰트 — 한자 통합, 글자 범위, 12px 후보](reference/fonts/cjk-pixel-fonts.md), [게임 UI용 한글 명조 — 고운바탕 vs 함렛, 가변 글꼴과 macroquad, 서브셋 크기](reference/fonts/korean-serif-ui-fonts.md), [GitHub Pages에 정적 페이지 올리기 — Actions 배포, 처음 켜기, 릴리스에서 읽는 값](reference/github-actions/pages-static-site.md), [macroquad 글자 그리기 비용과 브라우저 프레임레이트 — 아틀라스 통째 올리기, 레티나, WebGL 안티에일리어싱 기본값, Safari 저전력 30fps](reference/macroquad/text-rendering-and-browser-frame-rate.md)
- `fullscreen`: [웹 게임을 PWA로: 설치·오프라인·전체 화면·가로 잠금(Chrome·Android·iPhone)](reference/web/pwa-install-fullscreen-orientation.md)
- `game-design`: [모든 행동에 재사용 대기 — 동작 시간·대기·게이지·먹는 시간](concepts/action-reuse-gating.md), [1인 개발용 액션 로그라이트 설계 원칙](concepts/action-roguelite-for-solo-dev.md), [액션 RPG의 능력치·장비 설계 — 무기는 모양, 장신구는 수치, 성장은 영구](concepts/action-rpg-stats-and-equipment.md), [탑다운 모험 구조 — 격자 하나, 카메라 경계 사각형, 방 그래프 던전](concepts/adventure-field-and-procedural-dungeon.md), [선형 진행을 갈래 길로 느끼게 하는 지도](concepts/branching-route-map.md), [시점 전환(쿼터뷰 ↔ 숄더뷰)과 락온 카메라 — 하나의 전투, 두 개의 구도](concepts/camera-mode-switch-and-lock-on.md), [컨트롤러 버튼 배치와 다시 붙이기 — 오른쪽 넷은 자주 쓰는 넷, 메뉴 키는 고정, 안내는 배치를 따라](concepts/controller-layout-and-remapping.md), [깊이 내려간다"를 보이게 하기 — 전환·깊이 숫자·지도 방향·방 안의 위](concepts/conveying-descent.md), [어두운 세계의 귀여운 캐릭터 — 2등신 문법과 "색 = 생명](concepts/cute-characters-in-a-dark-world.md), [액션 게임 키보드·마우스 배치 — 마우스의 일은 카메라가 정하고, 왼손은 WASD 둘레에서 빈도 순](concepts/keyboard-and-mouse-layout-for-action-games.md), [근접 평타·모으기 공격의 손맛 — 누르는 순간, 작은 타격의 피드백 층, 모으기의 보상](concepts/melee-light-and-charged-attack-feel.md), [영구 성장(재주 나무) 해금을 계획할 수 있게 — 다 보이는 칸, 그림, 거기까지의 값, 목표 핀](concepts/meta-progression-unlock-planning.md), [근접 주인공의 원거리 보스 — 되받아치는 탄, 비키거나 파내는 바닥 위험](concepts/ranged-boss-for-melee-player.md), [다시 만나는 보스 — 만날 때마다 한 수, 지면 길을 비킨다](concepts/recurring-boss.md), [액션 로그라이트의 회복과 화폐 드롭 — 깎인 만큼·불운 보정·자석](concepts/roguelite-healing-and-currency.md), [로그라이트 저널(목표 목록) — 평소 플레이를 장기 목표로, 받기로 보상](concepts/roguelite-journal-goals.md), [로그라이트에서 이야기를 전하는 방법](concepts/roguelite-narrative-delivery.md), [로그라이트 다회차의 세 축 — 실력·다양성·궁금함](concepts/roguelite-replay-axes.md), [로그라이트 방이 반복되게 느껴질 때 — 모양보다 방마다의 판단을 바꾼다](concepts/roguelite-room-variety.md), [두 번째 플레이어 캐릭터 — 같은 버튼, 다른 동사](concepts/second-playable-character.md), [1인 게임 코드의 건강 신호 — 표로 넓히는 축, 틱 함수가 깊어지는 축, 소리 때문에 못 돌리는 테스트](concepts/solo-game-codebase-health-signals.md), [필살기의 임팩트 — 시동 정지, 거리, 끌고 가기, 소리 하나](concepts/special-move-impact.md), [공격 타이밍 패링 — 버튼 없이 맞받기, 굴/회피와 역할 나누기](concepts/timing-parry.md), [액션 게임 터치 배치 — 공격 둘레 호, 상황 버튼은 제 자리에만, 버튼 수가 복잡도](concepts/touch-action-layout.md), [미니맵 없이 길 알려 주기 — 환경 빛 + 화면 밖 화살 + 목표 글, 같은 규칙을 끝까지](concepts/wayfinding-without-a-minimap.md), [지도: 게임 개발](maps/gamedev.md), [캐릭터 설정에 쓰는 실제 동물·생태 사실](reference/nature/animal-behavior-for-character-design.md)
- `game-feel`: [모든 행동에 재사용 대기 — 동작 시간·대기·게이지·먹는 시간](concepts/action-reuse-gating.md), [실감나게 귀여운 캐릭터 동작 — 애니메이션 원칙을 게임 반응성과 작은 화면에 맞추기](concepts/believable-cute-character-motion.md), [시점 전환(쿼터뷰 ↔ 숄더뷰)과 락온 카메라 — 하나의 전투, 두 개의 구도](concepts/camera-mode-switch-and-lock-on.md), [개발용 시나리오 진입점과 스텝 스크립트 컷씬](concepts/dev-scenarios-and-scripted-cutscenes.md), [고정 타임스텝 게임 루프와 히트스톱](concepts/fixed-timestep-and-hitstop.md), [도트 액션의 손맛 효과 — 입자·빛·환경 입자·그림자](concepts/game-feel-particles-and-light.md), [작은 픽셀 HUD 읽히게 하기 — 바탕판·테두리 글자, 퀵 슬롯 고정 자리와 저절로 바꾸기](concepts/hud-readability-and-quick-slots.md), [근접 평타·모으기 공격의 손맛 — 누르는 순간, 작은 타격의 피드백 층, 모으기의 보상](concepts/melee-light-and-charged-attack-feel.md), [액션 로그라이트의 회복과 화폐 드롭 — 깎인 만큼·불운 보정·자석](concepts/roguelite-healing-and-currency.md), [필살기의 임팩트 — 시동 정지, 거리, 끌고 가기, 소리 하나](concepts/special-move-impact.md), [공격 타이밍 패링 — 버튼 없이 맞받기, 굴/회피와 역할 나누기](concepts/timing-parry.md), [게임 화면 색약 점검 — 시뮬레이션 행렬로 스크린숏을 돌려 보기](guides/color-vision-check-for-games.md), [PoC와 Lab — 콘텐츠보다 먼저, 수치는 사람이 화면에서 정한다](guides/poc-and-lab-before-content.md), [지도: 게임 개발](maps/gamedev.md)
- `gamedev`: [3D 도트 룩(t3ssel8r 풍) — 낮은 해상도·툰 빛·선 둘(어두운 가장자리 + 밝은 볼록 모서리)·카메라 픽셀 맞춤](concepts/3d-pixel-art-look.md), [모든 행동에 재사용 대기 — 동작 시간·대기·게이지·먹는 시간](concepts/action-reuse-gating.md), [1인 개발용 액션 로그라이트 설계 원칙](concepts/action-roguelite-for-solo-dev.md), [액션 RPG의 능력치·장비 설계 — 무기는 모양, 장신구는 수치, 성장은 영구](concepts/action-rpg-stats-and-equipment.md), [탑다운 모험 구조 — 격자 하나, 카메라 경계 사각형, 방 그래프 던전](concepts/adventure-field-and-procedural-dungeon.md), [실감나게 귀여운 캐릭터 동작 — 애니메이션 원칙을 게임 반응성과 작은 화면에 맞추기](concepts/believable-cute-character-motion.md), [선형 진행을 갈래 길로 느끼게 하는 지도](concepts/branching-route-map.md), [시점 전환(쿼터뷰 ↔ 숄더뷰)과 락온 카메라 — 하나의 전투, 두 개의 구도](concepts/camera-mode-switch-and-lock-on.md), [컨트롤러 버튼 배치와 다시 붙이기 — 오른쪽 넷은 자주 쓰는 넷, 메뉴 키는 고정, 안내는 배치를 따라](concepts/controller-layout-and-remapping.md), [깊이 내려간다"를 보이게 하기 — 전환·깊이 숫자·지도 방향·방 안의 위](concepts/conveying-descent.md), [어두운 세계의 귀여운 캐릭터 — 2등신 문법과 "색 = 생명](concepts/cute-characters-in-a-dark-world.md), [개발용 시나리오 진입점과 스텝 스크립트 컷씬](concepts/dev-scenarios-and-scripted-cutscenes.md), [고정 타임스텝 게임 루프와 히트스톱](concepts/fixed-timestep-and-hitstop.md), [도트 액션의 손맛 효과 — 입자·빛·환경 입자·그림자](concepts/game-feel-particles-and-light.md), [작은 픽셀 HUD 읽히게 하기 — 바탕판·테두리 글자, 퀵 슬롯 고정 자리와 저절로 바꾸기](concepts/hud-readability-and-quick-slots.md), [액션 게임 키보드·마우스 배치 — 마우스의 일은 카메라가 정하고, 왼손은 WASD 둘레에서 빈도 순](concepts/keyboard-and-mouse-layout-for-action-games.md), [근접 평타·모으기 공격의 손맛 — 누르는 순간, 작은 타격의 피드백 층, 모으기의 보상](concepts/melee-light-and-charged-attack-feel.md), [영구 성장(재주 나무) 해금을 계획할 수 있게 — 다 보이는 칸, 그림, 거기까지의 값, 목표 핀](concepts/meta-progression-unlock-planning.md), [인디 게임 공개 데모와 바깥 의견 받기](concepts/public-demo-and-outside-feedback.md), [근접 주인공의 원거리 보스 — 되받아치는 탄, 비키거나 파내는 바닥 위험](concepts/ranged-boss-for-melee-player.md), [작게 보이는 로우폴리 모델을 읽히게 — 깊이·외곽선·빛 단계·실루엣, 그리고 하지 말 것](concepts/readable-low-poly-models.md), [다시 만나는 보스 — 만날 때마다 한 수, 지면 길을 비킨다](concepts/recurring-boss.md), [액션 로그라이트의 회복과 화폐 드롭 — 깎인 만큼·불운 보정·자석](concepts/roguelite-healing-and-currency.md), [로그라이트 저널(목표 목록) — 평소 플레이를 장기 목표로, 받기로 보상](concepts/roguelite-journal-goals.md), [로그라이트에서 이야기를 전하는 방법](concepts/roguelite-narrative-delivery.md), [로그라이트 다회차의 세 축 — 실력·다양성·궁금함](concepts/roguelite-replay-axes.md), [로그라이트 방이 반복되게 느껴질 때 — 모양보다 방마다의 판단을 바꾼다](concepts/roguelite-room-variety.md), [로그라이트의 저장 슬롯·이어하기·런 중단 저장](concepts/roguelite-save-slots-and-continue.md), [두 번째 플레이어 캐릭터 — 같은 버튼, 다른 동사](concepts/second-playable-character.md), [1인 게임 코드의 건강 신호 — 표로 넓히는 축, 틱 함수가 깊어지는 축, 소리 때문에 못 돌리는 테스트](concepts/solo-game-codebase-health-signals.md), [필살기의 임팩트 — 시동 정지, 거리, 끌고 가기, 소리 하나](concepts/special-move-impact.md), [놀이 칸 밖 채우기 — 높이 안개·떠다니는 것·원경·식생(작은 3D 도트 게임)](concepts/surroundings-beyond-the-play-area.md), [공격 타이밍 패링 — 버튼 없이 맞받기, 굴/회피와 역할 나누기](concepts/timing-parry.md), [액션 게임 터치 배치 — 공격 둘레 호, 상황 버튼은 제 자리에만, 버튼 수가 복잡도](concepts/touch-action-layout.md), [미니맵 없이 길 알려 주기 — 환경 빛 + 화면 밖 화살 + 목표 글, 같은 규칙을 끝까지](concepts/wayfinding-without-a-minimap.md), [AI 3D 메시(Meshy 등)를 작은 게임용 강체 부위 모델로 — 줄이기·색 굽기·부위 자르기](guides/ai-mesh-to-rigid-part-model.md), [게임 화면 색약 점검 — 시뮬레이션 행렬로 스크린숏을 돌려 보기](guides/color-vision-check-for-games.md), [게임 그림 외주 맡기기 — 사양서와 계약 체크리스트(한국 저작권법 기준)](guides/commissioning-game-art.md), [운영판과 개발판을 갈라 내보내기 — 마일스톤 갈래, Cargo 기능, 따로 열고 따로 깔기](guides/dev-and-release-flavors.md), [Rust 게임을 Epic Games Store에 붙이기 — EOS 로그인·업적, 일괄 올리기 파일, BuildPatchTool](guides/epic-games-store-for-rust-games.md), [작곡가·음향 담당 없이 게임 소리 넣기 (CC0 출처·숫자로 고르기·섞기)](guides/game-audio-without-a-composer.md), [이미지 생성 모델(나노바나나)로 게임 일러스트 그리기 — 참고 그림·프롬프트·격자](guides/image-model-for-game-illustrations.md), [인디 게임 공식 페이지 — 무엇을 싣고, 도트 게임답게 움직이기](guides/indie-game-landing-page.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [그림 못 그려도 도트 게임 만들기 (에셋 전략)](guides/pixel-art-without-an-artist.md), [PoC와 Lab — 콘텐츠보다 먼저, 수치는 사람이 화면에서 정한다](guides/poc-and-lab-before-content.md), [두 번째 게임 프로젝트의 첫날 — 첫 게임에서 배운 것을 처음부터 깔기](guides/second-game-project-day-one.md), [작은 게임 다국어(현지화) 구조 — 고정 키 표, 자리표시자, 폰트 커버리지 테스트](guides/small-game-localization.md), [Rust 게임을 Steam에 붙이기 — 기능 하나로 가르기, 업적 표, 클라우드, 업로드 파이프라인, Deck](guides/steam-release-for-rust-games.md), [지도: 게임 개발](maps/gamedev.md), [지도: Rust](maps/rust.md), [무료(CC0·퍼블릭 도메인) 그림·사진 구하는 곳과 API 요령](reference/assets/free-image-sources.md), [레트로 3D 모델 파이프라인 — Blockbench 상자 모델 → glTF(부위 강체 애니메이션) → 직접 로더](reference/assets/retro-3d-models-blockbench-gltf.md), [인디 게임을 팔 때의 규칙과 숫자 — Steam·Epic·Play·Apple·itch, AI 공개, 위시리스트, 한국 세금·등급](reference/game-business/selling-an-indie-game-rules-and-numbers.md), [macroquad 3D 렌더링 — Camera3D·Mesh·배치·조명 없음·모델 로더 없음](reference/macroquad/3d-rendering.md), [macroquad 픽셀 퍼펙트 렌더링 (내부 해상도 고정 + 정수 배율)](reference/macroquad/pixel-perfect-rendering.md), [macroquad 글자 그리기 비용과 브라우저 프레임레이트 — 아틀라스 통째 올리기, 레티나, WebGL 안티에일리어싱 기본값, Safari 저전력 30fps](reference/macroquad/text-rendering-and-browser-frame-rate.md), [macroquad WASM 빌드와 JS 번들](reference/macroquad/wasm-build.md), [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- `gamepad`: [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md), [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- `git`: [브랜치 히스토리의 파일을 고친 판으로 바꿔 쓰기(force push 전후)](guides/rewrite-branch-history-replace-files.md)
- `github`: [공개 레포에서 배포 파이프라인 지키기 — Environment·브랜치 규칙·CODEOWNERS](guides/protect-deploy-pipeline-in-public-repo.md), [브랜치 히스토리의 파일을 고친 판으로 바꿔 쓰기(force push 전후)](guides/rewrite-branch-history-replace-files.md), [공개 레포를 비공개로 바꿀 때 — Actions 비용·Pages·Release가 어떻게 되나](reference/github-actions/public-to-private-repo.md)
- `github-actions`: [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md), [운영판과 개발판을 갈라 내보내기 — 마일스톤 갈래, Cargo 기능, 따로 열고 따로 깔기](guides/dev-and-release-flavors.md), [Rust 게임을 Epic Games Store에 붙이기 — EOS 로그인·업적, 일괄 올리기 파일, BuildPatchTool](guides/epic-games-store-for-rust-games.md), [macroquad 게임을 GitHub Actions에서 Android APK로 빌드하기 (cargo-quad-apk)](guides/macroquad-android-apk-github-actions.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [공개 레포에서 배포 파이프라인 지키기 — Environment·브랜치 규칙·CODEOWNERS](guides/protect-deploy-pipeline-in-public-repo.md), [Rust 게임을 Steam에 붙이기 — 기능 하나로 가르기, 업적 표, 클라우드, 업로드 파이프라인, Deck](guides/steam-release-for-rust-games.md), [지도: CI/CD와 호스팅](maps/ci-cd-hosting.md), [GitHub Actions의 Node 20 폐기 — 액션을 node24 판으로 올리기](reference/github-actions/node24-action-runtime.md), [GitHub Pages에 정적 페이지 올리기 — Actions 배포, 처음 켜기, 릴리스에서 읽는 값](reference/github-actions/pages-static-site.md), [GitHub Actions의 액션과 Rust 버전 고정하기 — SHA 고정·Dependabot·잠금 파일, dtolnay/rust-toolchain을 SHA로 쓸 때](reference/github-actions/pin-actions-and-rust-toolchain.md), [GitHub Actions에서 Playwright 연기 시험이 느려질 때 — `--with-deps`의 apt 글꼴과 같은 커밋 두 번 돌리기](reference/github-actions/playwright-smoke-test-ci-time.md), [공개 레포를 비공개로 바꿀 때 — Actions 비용·Pages·Release가 어떻게 되나](reference/github-actions/public-to-private-repo.md), [버전 올리기 = 릴리스 — CI가 태그를 만들고 빌드를 직접 부르기](reference/github-actions/release-from-version-bump.md), [GitHub Actions에서 Rust → wasm32 빌드](reference/github-actions/rust-wasm-build.md), [macroquad PC 빌드 — Windows·macOS·Linux 묶음, 에셋 경로 함정, 서명](reference/macroquad/desktop-build.md), [macroquad iOS 빌드 — GitHub Actions macOS 러너로 서명 안 한 .ipa, 기기 시험·배포의 갈림길](reference/macroquad/ios-build.md)
- `gltf`: [AI 3D 메시(Meshy 등)를 작은 게임용 강체 부위 모델로 — 줄이기·색 굽기·부위 자르기](guides/ai-mesh-to-rigid-part-model.md), [레트로 3D 모델 파이프라인 — Blockbench 상자 모델 → glTF(부위 강체 애니메이션) → 직접 로더](reference/assets/retro-3d-models-blockbench-gltf.md)
- `godot`: [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- `hosting`: [정적 WASM 호스팅](concepts/static-wasm-hosting.md), [지도: CI/CD와 호스팅](maps/ci-cd-hosting.md), [GitHub Pages에 정적 페이지 올리기 — Actions 배포, 처음 켜기, 릴리스에서 읽는 값](reference/github-actions/pages-static-site.md), [CI에서 netlify-cli로 배포](reference/netlify/deploy-from-ci.md)
- `hud`: [작은 픽셀 HUD 읽히게 하기 — 바탕판·테두리 글자, 퀵 슬롯 고정 자리와 저절로 바꾸기](concepts/hud-readability-and-quick-slots.md), [게임 UI용 한글 명조 — 고운바탕 vs 함렛, 가변 글꼴과 macroquad, 서브셋 크기](reference/fonts/korean-serif-ui-fonts.md)
- `i18n`: [작은 게임 다국어(현지화) 구조 — 고정 키 표, 자리표시자, 폰트 커버리지 테스트](guides/small-game-localization.md), [중국어·일본어 픽셀 폰트 — 한자 통합, 글자 범위, 12px 후보](reference/fonts/cjk-pixel-fonts.md), [게임 UI용 한글 명조 — 고운바탕 vs 함렛, 가변 글꼴과 macroquad, 서브셋 크기](reference/fonts/korean-serif-ui-fonts.md)
- `input`: [컨트롤러 버튼 배치와 다시 붙이기 — 오른쪽 넷은 자주 쓰는 넷, 메뉴 키는 고정, 안내는 배치를 따라](concepts/controller-layout-and-remapping.md), [고정 타임스텝 게임 루프와 히트스톱](concepts/fixed-timestep-and-hitstop.md), [액션 게임 키보드·마우스 배치 — 마우스의 일은 카메라가 정하고, 왼손은 WASD 둘레에서 빈도 순](concepts/keyboard-and-mouse-layout-for-action-games.md), [액션 게임 터치 배치 — 공격 둘레 호, 상황 버튼은 제 자리에만, 버튼 수가 복잡도](concepts/touch-action-layout.md), [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md)
- `ios`: [macroquad iOS 빌드 — GitHub Actions macOS 러너로 서명 안 한 .ipa, 기기 시험·배포의 갈림길](reference/macroquad/ios-build.md), [웹 게임을 PWA로: 설치·오프라인·전체 화면·가로 잠금(Chrome·Android·iPhone)](reference/web/pwa-install-fullscreen-orientation.md)
- `itch-io`: [인디 게임 공개 데모와 바깥 의견 받기](concepts/public-demo-and-outside-feedback.md), [인디 게임을 팔 때의 규칙과 숫자 — Steam·Epic·Play·Apple·itch, AI 공개, 위시리스트, 한국 세금·등급](reference/game-business/selling-an-indie-game-rules-and-numbers.md)
- `legal`: [인디 게임을 팔 때의 규칙과 숫자 — Steam·Epic·Play·Apple·itch, AI 공개, 위시리스트, 한국 세금·등급](reference/game-business/selling-an-indie-game-rules-and-numbers.md)
- `level-design`: [선형 진행을 갈래 길로 느끼게 하는 지도](concepts/branching-route-map.md), [깊이 내려간다"를 보이게 하기 — 전환·깊이 숫자·지도 방향·방 안의 위](concepts/conveying-descent.md), [로그라이트 방이 반복되게 느껴질 때 — 모양보다 방마다의 판단을 바꾼다](concepts/roguelite-room-variety.md), [미니맵 없이 길 알려 주기 — 환경 빛 + 화면 밖 화살 + 목표 글, 같은 규칙을 끝까지](concepts/wayfinding-without-a-minimap.md)
- `licensing`: [게임 그림 외주 맡기기 — 사양서와 계약 체크리스트(한국 저작권법 기준)](guides/commissioning-game-art.md), [작곡가·음향 담당 없이 게임 소리 넣기 (CC0 출처·숫자로 고르기·섞기)](guides/game-audio-without-a-composer.md), [그림 못 그려도 도트 게임 만들기 (에셋 전략)](guides/pixel-art-without-an-artist.md), [무료(CC0·퍼블릭 도메인) 그림·사진 구하는 곳과 API 요령](reference/assets/free-image-sources.md), [중국어·일본어 픽셀 폰트 — 한자 통합, 글자 범위, 12px 후보](reference/fonts/cjk-pixel-fonts.md), [게임 UI용 한글 명조 — 고운바탕 vs 함렛, 가변 글꼴과 macroquad, 서브셋 크기](reference/fonts/korean-serif-ui-fonts.md)
- `linux`: [macroquad PC 빌드 — Windows·macOS·Linux 묶음, 에셋 경로 함정, 서명](reference/macroquad/desktop-build.md)
- `localization`: [두 번째 게임 프로젝트의 첫날 — 첫 게임에서 배운 것을 처음부터 깔기](guides/second-game-project-day-one.md), [작은 게임 다국어(현지화) 구조 — 고정 키 표, 자리표시자, 폰트 커버리지 테스트](guides/small-game-localization.md), [중국어·일본어 픽셀 폰트 — 한자 통합, 글자 범위, 12px 후보](reference/fonts/cjk-pixel-fonts.md)
- `lock-on`: [시점 전환(쿼터뷰 ↔ 숄더뷰)과 락온 카메라 — 하나의 전투, 두 개의 구도](concepts/camera-mode-switch-and-lock-on.md)
- `loot`: [액션 RPG의 능력치·장비 설계 — 무기는 모양, 장신구는 수치, 성장은 영구](concepts/action-rpg-stats-and-equipment.md), [액션 로그라이트의 회복과 화폐 드롭 — 깎인 만큼·불운 보정·자석](concepts/roguelite-healing-and-currency.md)
- `low-poly`: [어두운 세계의 귀여운 캐릭터 — 2등신 문법과 "색 = 생명](concepts/cute-characters-in-a-dark-world.md), [작게 보이는 로우폴리 모델을 읽히게 — 깊이·외곽선·빛 단계·실루엣, 그리고 하지 말 것](concepts/readable-low-poly-models.md)
- `macos`: [macroquad PC 빌드 — Windows·macOS·Linux 묶음, 에셋 경로 함정, 서명](reference/macroquad/desktop-build.md)
- `macroquad`: [3D 도트 룩(t3ssel8r 풍) — 낮은 해상도·툰 빛·선 둘(어두운 가장자리 + 밝은 볼록 모서리)·카메라 픽셀 맞춤](concepts/3d-pixel-art-look.md), [탑다운 모험 구조 — 격자 하나, 카메라 경계 사각형, 방 그래프 던전](concepts/adventure-field-and-procedural-dungeon.md), [컨트롤러 버튼 배치와 다시 붙이기 — 오른쪽 넷은 자주 쓰는 넷, 메뉴 키는 고정, 안내는 배치를 따라](concepts/controller-layout-and-remapping.md), [도트 액션의 손맛 효과 — 입자·빛·환경 입자·그림자](concepts/game-feel-particles-and-light.md), [액션 게임 키보드·마우스 배치 — 마우스의 일은 카메라가 정하고, 왼손은 WASD 둘레에서 빈도 순](concepts/keyboard-and-mouse-layout-for-action-games.md), [작게 보이는 로우폴리 모델을 읽히게 — 깊이·외곽선·빛 단계·실루엣, 그리고 하지 말 것](concepts/readable-low-poly-models.md), [정적 WASM 호스팅](concepts/static-wasm-hosting.md), [놀이 칸 밖 채우기 — 높이 안개·떠다니는 것·원경·식생(작은 3D 도트 게임)](concepts/surroundings-beyond-the-play-area.md), [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md), [macroquad 게임을 GitHub Actions에서 Android APK로 빌드하기 (cargo-quad-apk)](guides/macroquad-android-apk-github-actions.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [Rust 게임을 Steam에 붙이기 — 기능 하나로 가르기, 업적 표, 클라우드, 업로드 파이프라인, Deck](guides/steam-release-for-rust-games.md), [지도: 게임 개발](maps/gamedev.md), [게임 UI용 한글 명조 — 고운바탕 vs 함렛, 가변 글꼴과 macroquad, 서브셋 크기](reference/fonts/korean-serif-ui-fonts.md), [macroquad 3D 렌더링 — Camera3D·Mesh·배치·조명 없음·모델 로더 없음](reference/macroquad/3d-rendering.md), [macroquad 소리(quad-snd) — 형식·메모리·음악 재생의 제약](reference/macroquad/audio.md), [macroquad PC 빌드 — Windows·macOS·Linux 묶음, 에셋 경로 함정, 서명](reference/macroquad/desktop-build.md), [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md), [macroquad 앱이 오래 켜면 죽을 때 — GPU 메모리가 자라는 두 원인과 재는 법](reference/macroquad/gpu-memory-growth.md), [macroquad iOS 빌드 — GitHub Actions macOS 러너로 서명 안 한 .ipa, 기기 시험·배포의 갈림길](reference/macroquad/ios-build.md), [macroquad 픽셀 퍼펙트 렌더링 (내부 해상도 고정 + 정수 배율)](reference/macroquad/pixel-perfect-rendering.md), [macroquad 글자 그리기 비용과 브라우저 프레임레이트 — 아틀라스 통째 올리기, 레티나, WebGL 안티에일리어싱 기본값, Safari 저전력 30fps](reference/macroquad/text-rendering-and-browser-frame-rate.md), [macroquad WASM 빌드와 JS 번들](reference/macroquad/wasm-build.md), [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- `manifest`: [웹 게임을 PWA로: 설치·오프라인·전체 화면·가로 잠금(Chrome·Android·iPhone)](reference/web/pwa-install-fullscreen-orientation.md)
- `marketing`: [인디 게임 공식 페이지 — 무엇을 싣고, 도트 게임답게 움직이기](guides/indie-game-landing-page.md), [인디 게임을 팔 때의 규칙과 숫자 — Steam·Epic·Play·Apple·itch, AI 공개, 위시리스트, 한국 세금·등급](reference/game-business/selling-an-indie-game-rules-and-numbers.md)
- `memory`: [macroquad 앱이 오래 켜면 죽을 때 — GPU 메모리가 자라는 두 원인과 재는 법](reference/macroquad/gpu-memory-growth.md)
- `meta-progression`: [영구 성장(재주 나무) 해금을 계획할 수 있게 — 다 보이는 칸, 그림, 거기까지의 값, 목표 핀](concepts/meta-progression-unlock-planning.md), [로그라이트 저널(목표 목록) — 평소 플레이를 장기 목표로, 받기로 보상](concepts/roguelite-journal-goals.md), [두 번째 플레이어 캐릭터 — 같은 버튼, 다른 동사](concepts/second-playable-character.md)
- `miniquad`: [macroquad 게임을 GitHub Actions에서 Android APK로 빌드하기 (cargo-quad-apk)](guides/macroquad-android-apk-github-actions.md), [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md), [macroquad WASM 빌드와 JS 번들](reference/macroquad/wasm-build.md)
- `mobile`: [액션 게임 터치 배치 — 공격 둘레 호, 상황 버튼은 제 자리에만, 버튼 수가 복잡도](concepts/touch-action-layout.md)
- `narrative`: [개발용 시나리오 진입점과 스텝 스크립트 컷씬](concepts/dev-scenarios-and-scripted-cutscenes.md), [다시 만나는 보스 — 만날 때마다 한 수, 지면 길을 비킨다](concepts/recurring-boss.md), [로그라이트에서 이야기를 전하는 방법](concepts/roguelite-narrative-delivery.md), [로그라이트 다회차의 세 축 — 실력·다양성·궁금함](concepts/roguelite-replay-axes.md), [캐릭터 설정에 쓰는 실제 동물·생태 사실](reference/nature/animal-behavior-for-character-design.md)
- `nature`: [캐릭터 설정에 쓰는 실제 동물·생태 사실](reference/nature/animal-behavior-for-character-design.md)
- `netlify`: [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md), [운영판과 개발판을 갈라 내보내기 — 마일스톤 갈래, Cargo 기능, 따로 열고 따로 깔기](guides/dev-and-release-flavors.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [지도: CI/CD와 호스팅](maps/ci-cd-hosting.md), [CI에서 netlify-cli로 배포](reference/netlify/deploy-from-ci.md), [웹 게임을 PWA로: 설치·오프라인·전체 화면·가로 잠금(Chrome·Android·iPhone)](reference/web/pwa-install-fullscreen-orientation.md)
- `node`: [GitHub Actions의 Node 20 폐기 — 액션을 node24 판으로 올리기](reference/github-actions/node24-action-runtime.md)
- `orientation`: [웹 게임을 PWA로: 설치·오프라인·전체 화면·가로 잠금(Chrome·Android·iPhone)](reference/web/pwa-install-fullscreen-orientation.md)
- `particles`: [놀이 칸 밖 채우기 — 높이 안개·떠다니는 것·원경·식생(작은 3D 도트 게임)](concepts/surroundings-beyond-the-play-area.md)
- `performance`: [macroquad 앱이 오래 켜면 죽을 때 — GPU 메모리가 자라는 두 원인과 재는 법](reference/macroquad/gpu-memory-growth.md), [macroquad 글자 그리기 비용과 브라우저 프레임레이트 — 아틀라스 통째 올리기, 레티나, WebGL 안티에일리어싱 기본값, Safari 저전력 30fps](reference/macroquad/text-rendering-and-browser-frame-rate.md)
- `pixel-art`: [3D 도트 룩(t3ssel8r 풍) — 낮은 해상도·툰 빛·선 둘(어두운 가장자리 + 밝은 볼록 모서리)·카메라 픽셀 맞춤](concepts/3d-pixel-art-look.md), [깊이 내려간다"를 보이게 하기 — 전환·깊이 숫자·지도 방향·방 안의 위](concepts/conveying-descent.md), [도트 액션의 손맛 효과 — 입자·빛·환경 입자·그림자](concepts/game-feel-particles-and-light.md), [작은 픽셀 HUD 읽히게 하기 — 바탕판·테두리 글자, 퀵 슬롯 고정 자리와 저절로 바꾸기](concepts/hud-readability-and-quick-slots.md), [게임 그림 외주 맡기기 — 사양서와 계약 체크리스트(한국 저작권법 기준)](guides/commissioning-game-art.md), [이미지 생성 모델(나노바나나)로 게임 일러스트 그리기 — 참고 그림·프롬프트·격자](guides/image-model-for-game-illustrations.md), [인디 게임 공식 페이지 — 무엇을 싣고, 도트 게임답게 움직이기](guides/indie-game-landing-page.md), [그림 못 그려도 도트 게임 만들기 (에셋 전략)](guides/pixel-art-without-an-artist.md), [지도: 게임 개발](maps/gamedev.md), [무료(CC0·퍼블릭 도메인) 그림·사진 구하는 곳과 API 요령](reference/assets/free-image-sources.md), [레트로 3D 모델 파이프라인 — Blockbench 상자 모델 → glTF(부위 강체 애니메이션) → 직접 로더](reference/assets/retro-3d-models-blockbench-gltf.md), [중국어·일본어 픽셀 폰트 — 한자 통합, 글자 범위, 12px 후보](reference/fonts/cjk-pixel-fonts.md), [macroquad 픽셀 퍼펙트 렌더링 (내부 해상도 고정 + 정수 배율)](reference/macroquad/pixel-perfect-rendering.md)
- `playtest`: [인디 게임 공개 데모와 바깥 의견 받기](concepts/public-demo-and-outside-feedback.md)
- `playwright`: [GitHub Actions에서 Playwright 연기 시험이 느려질 때 — `--with-deps`의 apt 글꼴과 같은 커밋 두 번 돌리기](reference/github-actions/playwright-smoke-test-ci-time.md)
- `procedural`: [실감나게 귀여운 캐릭터 동작 — 애니메이션 원칙을 게임 반응성과 작은 화면에 맞추기](concepts/believable-cute-character-motion.md)
- `procedural-generation`: [탑다운 모험 구조 — 격자 하나, 카메라 경계 사각형, 방 그래프 던전](concepts/adventure-field-and-procedural-dungeon.md), [선형 진행을 갈래 길로 느끼게 하는 지도](concepts/branching-route-map.md)
- `process`: [두 번째 게임 프로젝트의 첫날 — 첫 게임에서 배운 것을 처음부터 깔기](guides/second-game-project-day-one.md)
- `procgen`: [로그라이트 방이 반복되게 느껴질 때 — 모양보다 방마다의 판단을 바꾼다](concepts/roguelite-room-variety.md)
- `prototyping`: [PoC와 Lab — 콘텐츠보다 먼저, 수치는 사람이 화면에서 정한다](guides/poc-and-lab-before-content.md)
- `pwa`: [웹 게임을 PWA로: 설치·오프라인·전체 화면·가로 잠금(Chrome·Android·iPhone)](reference/web/pwa-install-fullscreen-orientation.md)
- `release`: [Rust 게임을 Epic Games Store에 붙이기 — EOS 로그인·업적, 일괄 올리기 파일, BuildPatchTool](guides/epic-games-store-for-rust-games.md), [Rust 게임을 Steam에 붙이기 — 기능 하나로 가르기, 업적 표, 클라우드, 업로드 파이프라인, Deck](guides/steam-release-for-rust-games.md), [버전 올리기 = 릴리스 — CI가 태그를 만들고 빌드를 직접 부르기](reference/github-actions/release-from-version-bump.md), [macroquad PC 빌드 — Windows·macOS·Linux 묶음, 에셋 경로 함정, 서명](reference/macroquad/desktop-build.md), [macroquad iOS 빌드 — GitHub Actions macOS 러너로 서명 안 한 .ipa, 기기 시험·배포의 갈림길](reference/macroquad/ios-build.md)
- `rendering`: [3D 도트 룩(t3ssel8r 풍) — 낮은 해상도·툰 빛·선 둘(어두운 가장자리 + 밝은 볼록 모서리)·카메라 픽셀 맞춤](concepts/3d-pixel-art-look.md), [작게 보이는 로우폴리 모델을 읽히게 — 깊이·외곽선·빛 단계·실루엣, 그리고 하지 말 것](concepts/readable-low-poly-models.md), [놀이 칸 밖 채우기 — 높이 안개·떠다니는 것·원경·식생(작은 3D 도트 게임)](concepts/surroundings-beyond-the-play-area.md), [macroquad 3D 렌더링 — Camera3D·Mesh·배치·조명 없음·모델 로더 없음](reference/macroquad/3d-rendering.md), [macroquad 픽셀 퍼펙트 렌더링 (내부 해상도 고정 + 정수 배율)](reference/macroquad/pixel-perfect-rendering.md)
- `roguelite`: [1인 개발용 액션 로그라이트 설계 원칙](concepts/action-roguelite-for-solo-dev.md), [액션 RPG의 능력치·장비 설계 — 무기는 모양, 장신구는 수치, 성장은 영구](concepts/action-rpg-stats-and-equipment.md), [탑다운 모험 구조 — 격자 하나, 카메라 경계 사각형, 방 그래프 던전](concepts/adventure-field-and-procedural-dungeon.md), [선형 진행을 갈래 길로 느끼게 하는 지도](concepts/branching-route-map.md), [영구 성장(재주 나무) 해금을 계획할 수 있게 — 다 보이는 칸, 그림, 거기까지의 값, 목표 핀](concepts/meta-progression-unlock-planning.md), [인디 게임 공개 데모와 바깥 의견 받기](concepts/public-demo-and-outside-feedback.md), [근접 주인공의 원거리 보스 — 되받아치는 탄, 비키거나 파내는 바닥 위험](concepts/ranged-boss-for-melee-player.md), [다시 만나는 보스 — 만날 때마다 한 수, 지면 길을 비킨다](concepts/recurring-boss.md), [액션 로그라이트의 회복과 화폐 드롭 — 깎인 만큼·불운 보정·자석](concepts/roguelite-healing-and-currency.md), [로그라이트 저널(목표 목록) — 평소 플레이를 장기 목표로, 받기로 보상](concepts/roguelite-journal-goals.md), [로그라이트에서 이야기를 전하는 방법](concepts/roguelite-narrative-delivery.md), [로그라이트 다회차의 세 축 — 실력·다양성·궁금함](concepts/roguelite-replay-axes.md), [로그라이트 방이 반복되게 느껴질 때 — 모양보다 방마다의 판단을 바꾼다](concepts/roguelite-room-variety.md), [로그라이트의 저장 슬롯·이어하기·런 중단 저장](concepts/roguelite-save-slots-and-continue.md), [두 번째 플레이어 캐릭터 — 같은 버튼, 다른 동사](concepts/second-playable-character.md)
- `rust`: [고정 타임스텝 게임 루프와 히트스톱](concepts/fixed-timestep-and-hitstop.md), [1인 게임 코드의 건강 신호 — 표로 넓히는 축, 틱 함수가 깊어지는 축, 소리 때문에 못 돌리는 테스트](concepts/solo-game-codebase-health-signals.md), [정적 WASM 호스팅](concepts/static-wasm-hosting.md), [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md), [운영판과 개발판을 갈라 내보내기 — 마일스톤 갈래, Cargo 기능, 따로 열고 따로 깔기](guides/dev-and-release-flavors.md), [Rust 게임을 Epic Games Store에 붙이기 — EOS 로그인·업적, 일괄 올리기 파일, BuildPatchTool](guides/epic-games-store-for-rust-games.md), [macroquad 게임을 GitHub Actions에서 Android APK로 빌드하기 (cargo-quad-apk)](guides/macroquad-android-apk-github-actions.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [PoC와 Lab — 콘텐츠보다 먼저, 수치는 사람이 화면에서 정한다](guides/poc-and-lab-before-content.md), [두 번째 게임 프로젝트의 첫날 — 첫 게임에서 배운 것을 처음부터 깔기](guides/second-game-project-day-one.md), [작은 게임 다국어(현지화) 구조 — 고정 키 표, 자리표시자, 폰트 커버리지 테스트](guides/small-game-localization.md), [Rust 게임을 Steam에 붙이기 — 기능 하나로 가르기, 업적 표, 클라우드, 업로드 파이프라인, Deck](guides/steam-release-for-rust-games.md), [지도: 게임 개발](maps/gamedev.md), [지도: Rust](maps/rust.md), [GitHub Actions의 액션과 Rust 버전 고정하기 — SHA 고정·Dependabot·잠금 파일, dtolnay/rust-toolchain을 SHA로 쓸 때](reference/github-actions/pin-actions-and-rust-toolchain.md), [버전 올리기 = 릴리스 — CI가 태그를 만들고 빌드를 직접 부르기](reference/github-actions/release-from-version-bump.md), [GitHub Actions에서 Rust → wasm32 빌드](reference/github-actions/rust-wasm-build.md), [macroquad 3D 렌더링 — Camera3D·Mesh·배치·조명 없음·모델 로더 없음](reference/macroquad/3d-rendering.md), [macroquad 소리(quad-snd) — 형식·메모리·음악 재생의 제약](reference/macroquad/audio.md), [macroquad PC 빌드 — Windows·macOS·Linux 묶음, 에셋 경로 함정, 서명](reference/macroquad/desktop-build.md), [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md), [macroquad 앱이 오래 켜면 죽을 때 — GPU 메모리가 자라는 두 원인과 재는 법](reference/macroquad/gpu-memory-growth.md), [macroquad iOS 빌드 — GitHub Actions macOS 러너로 서명 안 한 .ipa, 기기 시험·배포의 갈림길](reference/macroquad/ios-build.md), [macroquad 픽셀 퍼펙트 렌더링 (내부 해상도 고정 + 정수 배율)](reference/macroquad/pixel-perfect-rendering.md), [macroquad WASM 빌드와 JS 번들](reference/macroquad/wasm-build.md), [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md)
- `safari`: [macroquad 글자 그리기 비용과 브라우저 프레임레이트 — 아틀라스 통째 올리기, 레티나, WebGL 안티에일리어싱 기본값, Safari 저전력 30fps](reference/macroquad/text-rendering-and-browser-frame-rate.md)
- `save`: [로그라이트의 저장 슬롯·이어하기·런 중단 저장](concepts/roguelite-save-slots-and-continue.md)
- `security`: [공개 레포에서 배포 파이프라인 지키기 — Environment·브랜치 규칙·CODEOWNERS](guides/protect-deploy-pipeline-in-public-repo.md), [GitHub Actions의 액션과 Rust 버전 고정하기 — SHA 고정·Dependabot·잠금 파일, dtolnay/rust-toolchain을 SHA로 쓸 때](reference/github-actions/pin-actions-and-rust-toolchain.md)
- `service-worker`: [웹 게임을 PWA로: 설치·오프라인·전체 화면·가로 잠금(Chrome·Android·iPhone)](reference/web/pwa-install-fullscreen-orientation.md)
- `solo-dev`: [1인 개발용 액션 로그라이트 설계 원칙](concepts/action-roguelite-for-solo-dev.md), [인디 게임 공개 데모와 바깥 의견 받기](concepts/public-demo-and-outside-feedback.md), [다시 만나는 보스 — 만날 때마다 한 수, 지면 길을 비킨다](concepts/recurring-boss.md), [로그라이트 다회차의 세 축 — 실력·다양성·궁금함](concepts/roguelite-replay-axes.md), [로그라이트의 저장 슬롯·이어하기·런 중단 저장](concepts/roguelite-save-slots-and-continue.md), [두 번째 플레이어 캐릭터 — 같은 버튼, 다른 동사](concepts/second-playable-character.md), [게임 그림 외주 맡기기 — 사양서와 계약 체크리스트(한국 저작권법 기준)](guides/commissioning-game-art.md), [작곡가·음향 담당 없이 게임 소리 넣기 (CC0 출처·숫자로 고르기·섞기)](guides/game-audio-without-a-composer.md), [그림 못 그려도 도트 게임 만들기 (에셋 전략)](guides/pixel-art-without-an-artist.md), [PoC와 Lab — 콘텐츠보다 먼저, 수치는 사람이 화면에서 정한다](guides/poc-and-lab-before-content.md), [공개 레포에서 배포 파이프라인 지키기 — Environment·브랜치 규칙·CODEOWNERS](guides/protect-deploy-pipeline-in-public-repo.md), [두 번째 게임 프로젝트의 첫날 — 첫 게임에서 배운 것을 처음부터 깔기](guides/second-game-project-day-one.md), [공개 레포를 비공개로 바꿀 때 — Actions 비용·Pages·Release가 어떻게 되나](reference/github-actions/public-to-private-repo.md)
- `static-site`: [인디 게임 공식 페이지 — 무엇을 싣고, 도트 게임답게 움직이기](guides/indie-game-landing-page.md), [GitHub Pages에 정적 페이지 올리기 — Actions 배포, 처음 켜기, 릴리스에서 읽는 값](reference/github-actions/pages-static-site.md)
- `steam`: [Rust 게임을 Steam에 붙이기 — 기능 하나로 가르기, 업적 표, 클라우드, 업로드 파이프라인, Deck](guides/steam-release-for-rust-games.md), [인디 게임을 팔 때의 규칙과 숫자 — Steam·Epic·Play·Apple·itch, AI 공개, 위시리스트, 한국 세금·등급](reference/game-business/selling-an-indie-game-rules-and-numbers.md), [macroquad PC 빌드 — Windows·macOS·Linux 묶음, 에셋 경로 함정, 서명](reference/macroquad/desktop-build.md)
- `supply-chain`: [GitHub Actions의 액션과 Rust 버전 고정하기 — SHA 고정·Dependabot·잠금 파일, dtolnay/rust-toolchain을 SHA로 쓸 때](reference/github-actions/pin-actions-and-rust-toolchain.md)
- `testing`: [개발용 시나리오 진입점과 스텝 스크립트 컷씬](concepts/dev-scenarios-and-scripted-cutscenes.md), [1인 게임 코드의 건강 신호 — 표로 넓히는 축, 틱 함수가 깊어지는 축, 소리 때문에 못 돌리는 테스트](concepts/solo-game-codebase-health-signals.md), [PoC와 Lab — 콘텐츠보다 먼저, 수치는 사람이 화면에서 정한다](guides/poc-and-lab-before-content.md), [두 번째 게임 프로젝트의 첫날 — 첫 게임에서 배운 것을 처음부터 깔기](guides/second-game-project-day-one.md), [작은 게임 다국어(현지화) 구조 — 고정 키 표, 자리표시자, 폰트 커버리지 테스트](guides/small-game-localization.md), [GitHub Actions에서 Playwright 연기 시험이 느려질 때 — `--with-deps`의 apt 글꼴과 같은 커밋 두 번 돌리기](reference/github-actions/playwright-smoke-test-ci-time.md)
- `touch`: [액션 게임 터치 배치 — 공격 둘레 호, 상황 버튼은 제 자리에만, 버튼 수가 복잡도](concepts/touch-action-layout.md), [macroquad 게임패드와 Android 입력 현황](reference/macroquad/gamepad-and-android-input.md)
- `tuning`: [PoC와 Lab — 콘텐츠보다 먼저, 수치는 사람이 화면에서 정한다](guides/poc-and-lab-before-content.md)
- `ui`: [개발용 시나리오 진입점과 스텝 스크립트 컷씬](concepts/dev-scenarios-and-scripted-cutscenes.md), [작은 픽셀 HUD 읽히게 하기 — 바탕판·테두리 글자, 퀵 슬롯 고정 자리와 저절로 바꾸기](concepts/hud-readability-and-quick-slots.md), [영구 성장(재주 나무) 해금을 계획할 수 있게 — 다 보이는 칸, 그림, 거기까지의 값, 목표 핀](concepts/meta-progression-unlock-planning.md), [로그라이트 저널(목표 목록) — 평소 플레이를 장기 목표로, 받기로 보상](concepts/roguelite-journal-goals.md), [로그라이트의 저장 슬롯·이어하기·런 중단 저장](concepts/roguelite-save-slots-and-continue.md), [미니맵 없이 길 알려 주기 — 환경 빛 + 화면 밖 화살 + 목표 글, 같은 규칙을 끝까지](concepts/wayfinding-without-a-minimap.md)
- `vegetation`: [놀이 칸 밖 채우기 — 높이 안개·떠다니는 것·원경·식생(작은 3D 도트 게임)](concepts/surroundings-beyond-the-play-area.md)
- `vfx`: [깊이 내려간다"를 보이게 하기 — 전환·깊이 숫자·지도 방향·방 안의 위](concepts/conveying-descent.md), [도트 액션의 손맛 효과 — 입자·빛·환경 입자·그림자](concepts/game-feel-particles-and-light.md)
- `wasm`: [정적 WASM 호스팅](concepts/static-wasm-hosting.md), [0001: Rust WASM은 GitHub Actions에서 빌드하고 Netlify에는 CLI로 올린다](decisions/0001-build-rust-wasm-in-github-actions-deploy-via-netlify-cli.md), [macroquad WASM을 GitHub Actions로 빌드해 Netlify에 배포](guides/macroquad-wasm-netlify-github-actions.md), [지도: Rust](maps/rust.md), [GitHub Actions에서 Rust → wasm32 빌드](reference/github-actions/rust-wasm-build.md), [macroquad 소리(quad-snd) — 형식·메모리·음악 재생의 제약](reference/macroquad/audio.md), [macroquad 앱이 오래 켜면 죽을 때 — GPU 메모리가 자라는 두 원인과 재는 법](reference/macroquad/gpu-memory-growth.md), [macroquad 글자 그리기 비용과 브라우저 프레임레이트 — 아틀라스 통째 올리기, 레티나, WebGL 안티에일리어싱 기본값, Safari 저전력 30fps](reference/macroquad/text-rendering-and-browser-frame-rate.md), [macroquad WASM 빌드와 JS 번들](reference/macroquad/wasm-build.md), [Rust 게임 엔진 비교 — 웹 + Android 핸드헬드 + 컨트롤러 요구사항 기준](reference/rust-game-engines/web-android-gamepad-support.md), [웹 게임을 PWA로: 설치·오프라인·전체 화면·가로 잠금(Chrome·Android·iPhone)](reference/web/pwa-install-fullscreen-orientation.md)
- `web`: [GitHub Actions에서 Playwright 연기 시험이 느려질 때 — `--with-deps`의 apt 글꼴과 같은 커밋 두 번 돌리기](reference/github-actions/playwright-smoke-test-ci-time.md), [웹 게임을 PWA로: 설치·오프라인·전체 화면·가로 잠금(Chrome·Android·iPhone)](reference/web/pwa-install-fullscreen-orientation.md)
- `webgl`: [macroquad 앱이 오래 켜면 죽을 때 — GPU 메모리가 자라는 두 원인과 재는 법](reference/macroquad/gpu-memory-growth.md)
- `windows`: [macroquad PC 빌드 — Windows·macOS·Linux 묶음, 에셋 경로 함정, 서명](reference/macroquad/desktop-build.md)

<!-- index:end -->
