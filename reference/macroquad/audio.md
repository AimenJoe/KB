---
title: macroquad 소리(quad-snd) — 형식·메모리·음악 재생의 제약
type: reference
tags: [macroquad, audio, rust, wasm, android]
status: verified
created: 2026-10-26
updated: 2026-10-26
verified: |
  1차 출처로 확인(2026-10-26): quad-snd 0.2.8 소스(Cargo.toml: 네이티브는 audrey `wav`·`ogg_vorbis`만,
  mixer.rs load_samples_from_file: 통째로 f32 스테레오로 풀고 44100이 아니면 nearest-neighbor 리샘플),
  macroquad 0.4.16 audio.rs(PlaySoundParams = looped·volume, set_sound_volume·stop_sound).
  직접 실행: 헤드리스 Chromium에서 mp3 시험음을 load_file → load_sound_from_bytes로 받아 오류 없음(nail-under-the-roots 0081).
  확인 못 함: 네이티브(Android·데스크톱) ogg 실제 재생, 소리가 실제로 들리는지(컨테이너에 소리 장치 없음).
  2차 출처만 있음: Safari decodeAudioData의 Ogg Vorbis 지원 — WebKit 버그·MDN PR이 버전마다 엇갈린다(Safari 18.4+ 지원 제안).
sources:
  - https://github.com/not-fl3/quad-snd
  - https://docs.rs/macroquad/0.4.16/macroquad/audio/index.html
  - https://bugs.webkit.org/show_bug.cgi?id=226922
  - https://en.wikipedia.org/wiki/HTML_audio
---

# macroquad 소리(quad-snd) — 형식·메모리·음악 재생의 제약

## 요약
macroquad 0.4의 `audio` feature는 quad-snd 0.2를 쓴다.
- 네이티브(데스크톱·Android)는 **wav·ogg만** 풀 수 있다. 파일을 **통째로 44.1kHz f32 스테레오로** 메모리에 둔다.
- 웹은 브라우저 `decodeAudioData`에 맡긴다.
- 재생 인자는 **크기와 반복뿐**이다(음높이·팬 없음).

그래서 음악은 짧은 고리로 하고, 원본을 44.1kHz로 맞춘다. 웹과 네이티브는 형식을 나눠 싣는다(웹 mp3, 네이티브 ogg).

## 본문
| 항목 | 네이티브(audrey) | 웹(브라우저) |
|---|---|---|
| 형식 | wav, ogg vorbis | 브라우저가 푸는 것(mp3는 어디서나, ogg는 Safari가 버전마다 다름) |
| 메모리 | f32 스테레오 44.1kHz로 다 풀어 둔다. **1분 ≈ 21MB**(44100 × 2ch × 4B × 60) | 브라우저 AudioBuffer(대개 f32) |
| 샘플레이트 | 44100이 아니면 **nearest-neighbor 리샘플** → 거칠어진다 | 브라우저 리샘플 |
| 채널 | 1·2채널만(그 밖은 assert로 멈춘다) | — |

- API: `load_sound_from_bytes(&[u8])`, `play_sound(&s, PlaySoundParams { looped, volume })`, `set_sound_volume(&s, v)`, `stop_sound(&s)`. 같은 `Sound`를 여러 번 play하면 겹쳐 난다.
- 교차(crossfade)는 직접 한다. 새 곡을 크기 0으로 반복 재생하고 프레임마다 `set_sound_volume`으로 올린다. 옛 곡은 내려서 0이 되면 `stop_sound`.
- 음높이 변형(같은 소리를 조금씩 다르게)은 재생 인자로 못 한다 → 변형을 미리 만들어 둔다(합성음이면 시작할 때 몇 벌).
- 같은 소리가 한 틱에 여러 번 나는 것(한 번에 여럿 맞을 때)은 소리마다 마지막 재생 시각을 두고 짧은 간격(예: 30ms) 안이면 건너뛴다.
- 없는 파일을 `load_file`로 찾으면 웹 콘솔에 404가 남는다 → 실을 곡을 코드의 표로 두고 그것만 읽는다.
- 웹의 AudioContext는 사용자 제스처 뒤에야 시작한다(번들이 첫 클릭에서 resume, [고정 타임스텝 노트](../../concepts/fixed-timestep-and-hitstop.md)).

## 왜?
- quad-snd는 스트리밍이 없다. 작고 단순한 믹서다. 곡이 길수록 메모리가 그만큼 든다. Android 핸드헬드에서 곡 여섯 개를 1분씩 다 올리면 120MB를 넘는다 → 장소가 바뀔 때만 필요한 곡을 올리거나, 고리를 30~60초로 줄인다.
- 브라우저와 네이티브의 디코더가 다르니 "한 형식으로 다 된다"는 가정이 깨진다. mp3는 네이티브에서 안 되고, ogg는 일부 Safari에서 안 된다.

## 함정
- 22.05kHz로 줄여 용량을 아끼면 네이티브에서 리샘플이 거칠어진다. 용량은 길이로 줄인다.
- 크기 0으로 시작한 반복 재생은 끄지 않으면 계속 섞인다(조용해도 믹서 비용). 내려간 곡은 `stop_sound`.

## 관련 노트
- [WASM 빌드와 JS 번들](wasm-build.md) — `audio` feature, 링크 플래그, 번들 버전
- [필살기의 임팩트](../../concepts/special-move-impact.md) — 소리 하나로 잇기
