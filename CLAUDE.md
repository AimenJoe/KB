# CLAUDE.md — 이 KB를 읽고 쓰는 규칙

이 레포는 개인 지식 베이스다. 프로젝트 코드가 아니다.

## 질문을 받았을 때 (읽기)
1. `README.md`의 인덱스에서 관련 지도(`maps/`)와 노트를 먼저 찾는다.
2. 도메인 키워드로는 frontmatter 태그를 grep 한다. 본문 전체 grep은 그 다음.
   ```sh
   rg -l '^tags:.*\bnetlify\b' --glob '*.md'
   ```
3. 찾은 노트의 `verified`를 확인한다. "2차 출처만 있음"으로 표시된 사실은 답에 그 한계를 함께 말한다. `status: stale`이면 재검증 후 답한다.
4. KB에 없으면 그렇다고 말하고 외부 자료로 교차검증한 뒤, 남길 가치가 있으면 노트 추가를 제안한다.

## 노트를 쓸 때 (쓰기)
- 넣기 전에 묻는다: **이 프로젝트가 사라져도 유용한가?** 아니면 KB에 쓰지 않는다.
- `_templates/note.md`(또는 `map.md`) frontmatter를 그대로 쓴다. `type`과 폴더가 일치해야 한다.
- `verified`에 1차 출처(소스 코드, 공식 문서, 직접 실행)로 확인한 것과 포럼/블로그만 있는 것을 분리해 적는다. 확인 못 한 것은 못 했다고 적는다.
- 사실은 `reference/`에 한 번만. 가이드·지도는 링크한다.
- 새 노트는 관련 `maps/`에 링크를 추가한다. 맞는 지도가 없으면 지도를 만든다.
- 커밋 전:
  ```sh
  python3 tools/kb.py check && python3 tools/kb.py index
  ```
- 외부 자료의 원문을 통째로 복사하지 않는다. 요약 + `sources` URL.
- 언어: 한국어. 고유명사·명령·코드는 원문.

## 하지 않는 것
- 프로젝트별 TODO, 로그, 회의 메모를 여기에 쓰지 않는다.
- README 인덱스를 손으로 고치지 않는다 (`tools/kb.py index`가 생성).
- `verified` 없는 guide/reference/concept/decision 노트를 만들지 않는다.
