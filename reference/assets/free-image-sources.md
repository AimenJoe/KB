---
title: 무료(CC0·퍼블릭 도메인) 그림·사진 구하는 곳과 API 요령
type: reference
tags: [assets, licensing, pixel-art, gamedev]
status: draft
created: 2026-10-26
updated: 2026-10-26
verified: |
  1차 출처로 확인(2026-10-26, nail-under-the-roots 세션에서 직접 호출):
  - Openverse API `api.openverse.org/v1/images/?q=..&license=cc0,pdm`가 인증 없이 응답했다.
    썸네일 `/v1/images/<id>/thumb/`(최대 약 600px)도 같은 도메인에서 받았다. 원본 주소(staticflickr·rawpixel)는 다른 도메인이다.
    일부 썸네일은 424(원본 쪽 실패)였다.
  - Met 컬렉션 API: `/public/collection/v1/search`가 410으로 응답했다. 응답 본문에 "2026-10-01 폐지, `/v1.1/search`(offset·limit 페이지)"라고 적혀 있다.
    `/v1.1/search?q=..&hasImages=true&isPublicDomain=true&limit=N`과 `/v1/objects/<id>`(isPublicDomain, primaryImage(Small))가 됐다.
    `images.metmuseum.org/CRDImages/<부서>/web-large/<파일>`로 중간 크기를 받았다.
  - Wikimedia API: 한 번 429였고, User-Agent를 붙여 다시 하니 200이었다. 원인이 UA인지 일시 제한인지는 가리지 못했다.
  - Art Institute of Chicago API: Cloudflare 확인 화면(403) 때문에 스크립트로 못 받았다.
  2차/확인 못 함: Unsplash·Pexels·Pixabay 라이선스 조건은 블로그 요약만 봤다(원문 미확인).
  미술관 Open Access 이미지가 CC0라는 것은 Met API의 isPublicDomain 필드와 Openverse 표기로만 확인했다.
sources:
  - https://api.openverse.org/v1/
  - https://metmuseum.github.io/
  - https://www.mediawiki.org/wiki/API:Etiquette
  - https://licenseorg.com/blog/free-stock-photos-licensing-traps
---

# 무료 그림·사진 구하는 곳

## 요약
게임 배경·일러스트의 바탕으로 쓸 그림을 찾을 때 고르는 순서는 이렇다.
1. **Openverse**(CC0·PDM 거르기)로 넓게 찾는다.
2. **미술관 Open Access**(Met 등, CC0)에서 그림을 고른다.
3. 사진은 Unsplash·Pexels·Pixabay(각자 자체 라이선스)에서 고른다.
4. 질감은 Poly Haven·ambientCG(CC0)에서 고른다.

도트화하려면 사진보다 **붓 자국이 큰 그림**이 낫다(→ [도트 가이드](../../guides/pixel-art-without-an-artist.md) "그림·사진을 도트로").

## 본문
| 곳 | 무엇 | 라이선스 | 스크립트로 받기 |
|---|---|---|---|
| Openverse | 여러 곳(Flickr·Wikimedia·rawpixel·미술관) 검색 | 거르기: `license=cc0,pdm`, 상업용 `license_type=commercial` | 키 없이 됨. 썸네일은 같은 도메인 |
| Wikimedia Commons | 자연 사진·옛 그림 | 파일마다 다름 → 파일 쪽 라이선스 확인 | User-Agent 붙일 것(API 예절) |
| The Met Open Access | 풍경화·판화·소묘 | 퍼블릭 도메인 표시 작품은 CC0 | v1.1 search + objects. 이미지 `web-large` |
| Rijksmuseum, Smithsonian, NGA | 그림 | CC0(공개 소장품) | 이번엔 시험 안 함 |
| Art Institute of Chicago | 그림 | CC0(공개 소장품) | Cloudflare 확인 화면에 막힘 |
| Biodiversity Heritage Library | 옛 박물학 도감(동물·식물) | 대부분 퍼블릭 도메인, 항목 확인 | 시험 안 함 |
| Unsplash, Pexels | 사진 | 자체 라이선스: 상업 사용·출처 표시 없음. 원본 되팔기·경쟁 서비스 금지(2차) | API 키 필요 |
| Pixabay | 사진·일러스트 | 자체 라이선스(2019~). 사람·상표 사진은 따로 조건(2차) | API 키 필요 |
| Poly Haven, ambientCG | 질감·HDRI | CC0 | 시험 안 함 |
| NASA | 하늘·별 | 대부분 퍼블릭 도메인(로고·사람 예외) | 시험 안 함 |

## 왜?
- **PDM ≠ CC0**: Public Domain Mark는 "저작권이 없다고 알려졌다"는 표시이고, CC0는 권리자가 권리를 포기한 것이다. 오래된 그림의 복제 사진에 PDM이 많다. 원작이 오래돼 퍼블릭 도메인인지(작가 사망 연도) 함께 본다.
- **도트로 바꿔도 2차 저작물**이다. 원본 라이선스를 지켜야 하니, 출처 주소·라이선스를 에셋 기록에 남긴다.
- 자체 라이선스(Unsplash 등)는 CC가 아니라 조건이 바뀔 수 있다. 쓴 날짜의 원문을 확인한다.

## 함정
- Met의 옛 `/v1/search`는 2026-10-01에 폐지됐다(410). 옛 예제 코드가 많다.
- Openverse 썸네일은 600px쯤이다. 320×180 도트화에는 충분하지만, 더 크게 쓰려면 원본 도메인을 따로 열어야 한다.
- 검색어가 흔하면 사람·트랙터·마스코트 사진이 섞인다. 사람·상표가 보이면 뺀다.
- 에셋 팩 그림을 "참조"로 넣지 않는다(팩 라이선스의 AI·파생 조항).

## 관련 노트
- [그림 못 그려도 도트 게임 만들기](../../guides/pixel-art-without-an-artist.md)
