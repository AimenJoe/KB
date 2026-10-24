---
title: macroquad 픽셀 퍼펙트 렌더링 (내부 해상도 고정 + 정수 배율)
type: reference
tags: [macroquad, pixel-art, rendering, rust, gamedev]
status: verified
created: 2026-10-24
updated: 2026-10-24
verified: |
  1차 출처로 확인: macroquad 0.4.16 src/texture.rs(render_target(), Texture2D::set_filter 문서 주석
  "Use Nearest if you need integer-ratio scaling for pixel art", draw_texture_ex의 flip_y 처리), src/camera.rs(from_display_rect가
  zoom.y를 음수로 두고, matrix()가 render_target이 있으면 invert_y = 1.0, 없으면 -1.0을 곱함), miniquad 0.4.11 src/conf.rs(high_dpi 기본 false).
  직접 실행(2026-10-24, Linux Xvfb + Mesa llvmpipe, macroquad 0.4.16): 아래 스케치 그대로 돌리면 **렌더 타깃 결과가 상하 반전**되어 나온다.
  월드 (2,2)에 그린 표식이 화면 아래쪽에, 글자는 거울상으로 찍혔다. X 서버 캡처(ImageMagick import)와 get_screen_data() 결과가 일치.
  `DrawTextureParams { flip_y: true }`로 올리면 정상. 수정 후 캡처로 재확인.
  2차 출처만 있음: 없음.
  확인 못 함: 웹(WebGL)·macOS·Windows에서도 같은 방향인지는 데스크톱 GL과 동일한 코드 경로라 같다고 추정만 했다. 웹 빌드는 헤드리스 Chromium에서 flip_y 적용본이 바르게 나오는 것만 확인.
sources:
  - https://github.com/not-fl3/macroquad/blob/master/src/texture.rs
  - https://github.com/not-fl3/macroquad/blob/master/src/camera.rs
  - https://github.com/not-fl3/miniquad/blob/master/src/conf.rs
---

# macroquad 픽셀 퍼펙트 렌더링

## 요약
도트 게임은 **작은 내부 해상도의 렌더 타깃에 그리고, 화면에는 정수 배율로 확대**해야 픽셀이 균일하다. macroquad에서는 `render_target` + `Camera2D { render_target: Some(..) }` + `set_filter(FilterMode::Nearest)` 조합으로 한다.

## 왜 내부 해상도를 고정하는가
- 화면 해상도에 직접 그리면 스프라이트마다 확대 비율이 달라져 픽셀 크기가 들쭉날쭉해진다("레트로 느낌"이 깨지는 가장 흔한 원인).
- 비정수 배율(예: 2.37배)은 픽셀 행이 어떤 건 2줄, 어떤 건 3줄로 찍혀 흔들림(shimmering)이 생긴다.
- 내부 해상도를 고정하면 게임 로직 좌표계도 고정되어 UI 배치·히트박스가 단순해진다.

## 해상도 선택 (16:9 기준)

| 내부 해상도 | 720p | 1080p | 1440p | 4K |
|---|---|---|---|---|
| 320×180 | ×4 | ×6 | ×8 | ×12 |
| 384×216 | — | ×5 | — | ×10 |
| 480×270 | — | ×4 | — | ×8 |
| 640×360 | ×2 | ×3 | ×4 | ×6 |

320×180은 모든 흔한 해상도에서 정수 배율이 나와 핸드헬드(720p/1080p)와 데스크톱 모두에 안전하다. 타일 16×16이면 20×11.25 타일, 화면이 작게 느껴지면 384×216.

## 구현 스케치

```rust
use macroquad::prelude::*;

const W: u32 = 320; const H: u32 = 180;

#[macroquad::main("game")]
async fn main() {
    let rt = render_target(W, H);
    rt.texture.set_filter(FilterMode::Nearest);          // 확대 시 보간 금지
    let mut cam = Camera2D::from_display_rect(Rect::new(0., 0., W as f32, H as f32));
    cam.render_target = Some(rt.clone());

    loop {
        // 1) 내부 해상도로 월드 그리기
        set_camera(&cam);
        clear_background(BLACK);
        // draw_texture / draw_rectangle ... (좌표계 0..320, 0..180)

        // 2) 화면에 정수 배율로 올리기 (레터박스)
        set_default_camera();
        clear_background(BLACK);
        let scale = (screen_width() / W as f32).min(screen_height() / H as f32).floor().max(1.0);
        let dw = W as f32 * scale; let dh = H as f32 * scale;
        let x = ((screen_width() - dw) / 2.0).floor();
        let y = ((screen_height() - dh) / 2.0).floor();
        draw_texture_ex(&rt.texture, x, y, WHITE, DrawTextureParams {
            dest_size: Some(vec2(dw, dh)),
            flip_y: true, // 0.4.16: from_display_rect + render_target 조합은 뒤집혀 나온다 (아래 함정)
            ..Default::default()
        });
        next_frame().await
    }
}
```

- 오프셋 `x, y`를 `floor()`로 정수화해야 반 픽셀 번짐이 없다.
- 월드 안에서도 스프라이트 위치를 정수로 반올림해 그리면 더 깨끗하다(카메라 스크롤 포함).
- 마우스 좌표는 `(mouse_x - x) / scale`로 내부 좌표계로 되돌린다.

## 함정
- **상하 반전 (0.4.16에서 실행 확인)**: `Camera2D::from_display_rect`는 y가 아래로 가는 좌표계를 만들려고 `zoom.y`를 **음수**로 둔다. `matrix()`는 `render_target`이 있으면 `invert_y = 1.0`, 없으면 `-1.0`을 `zoom.y`에 곱한다. 화면에 직접 그릴 때는 둘이 상쇄되지만, 렌더 타깃에 그릴 때는 월드 y=0이 클립 공간 +1(텍스처의 마지막 행)로 가고, `draw_texture_ex`는 텍스처 첫 행을 위에 그리므로 **결과가 뒤집힌다**. 해결은 둘 중 하나: (a) 올릴 때 `flip_y: true`(위 스케치), (b) `from_display_rect` 대신 `zoom: vec2(2./w, 2./h)`(양수)로 카메라를 직접 만든다. 어느 쪽도 macroquad가 `invert_y` 논리를 바꾸면 다시 뒤집히므로, 버전을 올릴 때 **표식을 그려 실행 확인**한다(아래 "확인 방법").
- **HiDPI**: miniquad `Conf::high_dpi`는 기본 `false`. false면 `screen_width()`가 논리 픽셀을 돌려주고 OS가 확대하므로 Retina/고배율 화면에서 흐려질 수 있다. 선명함이 중요하면 `high_dpi: true`로 물리 픽셀 기준으로 배율을 계산한다.
- **텍스처 아틀라스 bleeding**: Nearest라도 타일 경계에서 인접 픽셀이 새어 들어올 수 있다. 타일 사이 1px 패딩 또는 UV를 반 픽셀 안쪽으로.
- **텍스트**: 내장 폰트는 내부 해상도에서 작게 렌더되면 깨진다. 픽셀 폰트를 쓰거나 UI만 바깥(실제 해상도) 패스에서 그린다.

## 확인 방법 (헤드리스 Linux)
표식(왼쪽 위에 색 사각형 + 글자)을 월드에 그리고 캡처한다. 디스플레이가 없는 컨테이너/CI에서도 된다.

```sh
# Xvfb + Mesa 소프트웨어 GL. 창이 뜰 때까지 xdotool이 기다리고, ImageMagick으로 루트 창을 찍는다.
xvfb-run -a -s "-screen 0 1280x720x24" bash -c '
  LIBGL_ALWAYS_SOFTWARE=1 ./target/debug/game & 
  xdotool search --sync --name "창 제목" >/dev/null
  timeout 1.5 tail -f /dev/null          # sleep 대용
  import -window root shot.png; kill %1'
```
- 필요한 패키지(Ubuntu): `xvfb x11-utils xdotool imagemagick libgl1-mesa-dri`. 소리 장치가 없으면 quad-snd가 "Audio thread died"를 찍지만 렌더에는 영향 없다.
- `xdotool key j`로 키 입력도 넣을 수 있다(창에 `windowfocus` 먼저). miniquad X11 백엔드는 XTEST 입력을 받는다.
- `get_screen_data().export_png()`로 앱 안에서 찍은 결과는 X 서버 캡처와 방향이 같았다(0.4.16).

## 관련 노트
- [reference/macroquad/wasm-build.md](wasm-build.md) — 웹 빌드도 헤드리스로 확인하는 법
- [guides/pixel-art-without-an-artist.md](../../guides/pixel-art-without-an-artist.md)
