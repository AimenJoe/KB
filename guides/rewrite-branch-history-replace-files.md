---
title: 브랜치 히스토리의 파일을 고친 판으로 바꿔 쓰기(force push 전후)
type: guide
tags: [git, github]
status: draft
created: 2026-10-26
updated: 2026-10-26
verified: |
  1차 출처로 확인(2026-10-26, GitHub 공식 문서 원문 github/docs "Removing sensitive data from a repository"를 직접 읽음): 권장 도구는 git-filter-repo(2.47+의 --sensitive-data-removal),
  다시 쓴 뒤에도 남는 곳(다른 사람의 클론·포크, GitHub의 캐시된 화면에서 SHA로 직접, 그 커밋을 가리키는 PR), 부작용(해시가 모두 바뀜, 닫힌 PR의 diff가 깨짐, 열린 PR의 댓글이 사라질 수 있음, 서명이 사라짐, 옛 클론이 pull 후 push하면 되살아남),
  GitHub Support는 "민감하지 않은 데이터는 지우지 않고", 자격 증명을 바꿔서 막을 수 없는 경우에만 돕는다.
  직접 실행으로 확인(nail-under-the-roots 0133 후속, 2026-10-26): `git filter-branch --index-filter`로 범위(main..브랜치)의 이미지 blob을 고친 blob으로 바꿈(48커밋, 87개 중 43개),
  끝 커밋 트리가 다시 쓰기 전과 같음, 범위 밖(main·태그)은 그대로, `--force-with-lease=<브랜치>:<옛 SHA>` push.
  확인 못 함: git-filter-repo의 blob 콜백으로 같은 일을 하는 방법(이번에는 filter-branch를 썼다), GitHub가 참조 없는 옛 커밋을 실제로 언제 지우는지.
sources:
  - https://github.com/github/docs/blob/main/content/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository.md
  - https://github.com/newren/git-filter-repo
---

# 브랜치 히스토리의 파일을 고친 판으로 바꿔 쓰기(force push 전후)

## 요약
지금 파일만 고치면 옛 커밋에는 고치기 전 판이 남는다(공개 레포면 누구나 본다). 히스토리까지 바꾸려면 **먼저 범위를 잰다**(어느 브랜치·태그가 그 파일의 옛 판을 품는가). 범위가 작업 브랜치뿐이면 그 브랜치만 다시 쓴다. 지우지 않고 **옛 판마다 고친 판을 만들어 바꿔 끼우면** 히스토리의 모양(커밋 수·메시지·순서)은 그대로다. 끝 커밋의 트리가 다시 쓰기 전과 같은지로 확인하고 `--force-with-lease`로 push한다. GitHub에는 옛 커밋이 SHA로 한동안 남고, Support는 민감한 데이터만 지워 준다.

## 본문
### 1. 범위 재기
```sh
git rev-list --count origin/main -- <경로>            # main에 그 경로를 건드린 커밋이 있나
git rev-list --count origin/main..HEAD -- <경로>      # 브랜치에만 있는 커밋
git tag --contains <그 경로를 처음 넣은 커밋>          # 태그(릴리스)가 품나
```
main·태그에 없으면 main(배포된 히스토리)과 릴리스는 건드리지 않아도 된다.

### 2. 옛 판 → 고친 판 지도 만들기
```sh
for c in $(git rev-list origin/main..HEAD); do git ls-tree -r $c <경로>; done | awk '{print $3, $4}' | sort -u
```
blob마다 `git cat-file blob <sha>`로 꺼내 고치고 `git hash-object -w <파일>`로 새 blob을 쓴다. "옛 sha 새 sha" 줄의 표를 남긴다. 이미 고친 판(지금 파일)은 그대로 둔다.

### 3. 인덱스만 바꿔 다시 쓰기
```sh
# idx.sh: 표에 있는 blob만 바꾼다
git ls-files -s -- <경로> | while read mode blob stage path; do
  new=$(grep "^$blob " map.txt | cut -d' ' -f2)
  [ -n "$new" ] && git update-index --cacheinfo "$mode,$new,$path"
done
```
```sh
git filter-branch --index-filter ./idx.sh -- origin/main..<브랜치>
```
작업 트리를 꺼내지 않아(`--index-filter`) 빠르다(48커밋 7초).

### 4. 확인 → push
- 끝 커밋 트리가 같다: `git rev-parse <옛 HEAD>^{tree}` = `git rev-parse HEAD^{tree}`(지금 파일이 이미 고친 판이었다면).
- 커밋 수가 같고 밑(`git merge-base HEAD origin/main`)이 그대로다.
- 범위의 모든 커밋에서 옛 blob이 하나도 안 보인다.
- `git push --force-with-lease=<브랜치>:<옛 HEAD> origin HEAD:<브랜치>`: 그 사이 다른 사람이 push했으면 거절된다.

## 왜?
- git 커밋 해시는 트리(곧 파일 내용)에서 나온다. 옛 커밋의 파일을 바꾸면 그 커밋과 뒤의 모든 커밋이 새 해시가 된다. 그래서 "히스토리를 다시 쓴다"이고 force push가 필요하다.
- 지우기(`--invert-paths`) 대신 바꿔 끼우면 옛 커밋도 그때의 작업(그 파일이 있다는 것, 생성 결과와 짝)이 그대로 맞는다.

## 함정
- **GitHub에 남는다**: 다시 쓴 뒤에도 옛 커밋은 GitHub의 캐시된 화면에서 SHA로 직접 열리고, 그 커밋을 가리키는 PR·포크·다른 사람의 클론에도 남는다. Support는 **민감한 데이터(자격 증명처럼 바꿔서 막을 수 없는 것)만** 지워 준다. 그림 같은 일반 파일은 "브랜치에서 보이지 않게"까지가 할 수 있는 끝이다.
- **옛 클론이 되살린다**: 다시 쓰기 전 클론에서 `git pull` 뒤 `git push`하면 옛 커밋이 돌아온다. 다른 기기는 `git fetch` + `git reset --hard origin/<브랜치>`(또는 새로 클론).
- 해시를 기억하는 것(문서의 커밋 링크, CI 캐시 키, 서명)이 모두 바뀐다. 커밋 메시지·문서에 짧은 해시를 적어 두었다면 낡는다.
- 열린 PR이 있으면 diff·댓글이 흐트러진다. 닫거나 합친 뒤에 한다.
- `filter-branch`는 `refs/original/`에 옛 참조를 남긴다(로컬 되돌리기용). 확인이 끝나면 지워도 된다.

## 관련 노트
- [버전 올리기 = 릴리스](../reference/github-actions/release-from-version-bump.md)
- [이미지 생성 모델로 게임 일러스트 그리기](image-model-for-game-illustrations.md) — 이 방법을 쓴 까닭(원본의 ✦ 로고)
