#!/usr/bin/env python3
"""KB 유지 도구. 의존성 없음(표준 라이브러리만).

  python3 tools/kb.py check   # frontmatter·폴더·링크·지도 수록 검증 (CI용, 실패 시 exit 1)
  python3 tools/kb.py index   # README.md의 인덱스 섹션을 frontmatter로 재생성
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPE_DIRS = {"guide": "guides", "reference": "reference", "concept": "concepts",
             "decision": "decisions", "map": "maps"}
REQUIRED = ["title", "type", "tags", "status", "created", "updated"]
STATUSES = {"draft", "verified", "stale"}
SKIP_DIRS = ("_templates/", ".git/", "tools/", ".github/")
INDEX_START, INDEX_END = "<!-- index:start -->", "<!-- index:end -->"


def notes():
    for p in sorted(glob.glob("**/*.md", recursive=True, root_dir=ROOT)):
        if p.startswith(SKIP_DIRS) or p in ("README.md", "CLAUDE.md"):
            continue
        yield p


def frontmatter(path):
    text = open(os.path.join(ROOT, path), encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fm, cur = {}, None
    for line in m.group(1).splitlines():
        if cur and (line.startswith("  ") or line.strip() == ""):
            fm[cur] += "\n" + line.strip()
            continue
        k, _, v = line.partition(":")
        cur, v = k.strip(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [t.strip().strip('"') for t in v[1:-1].split(",") if t.strip()]
        elif v == "|":
            v = ""
        else:
            v = v.strip('"')
        fm[cur] = v
    return fm, text


def links(path, text):
    d = os.path.dirname(path)
    for m in re.finditer(r"\]\(([^)#\s]+)(#[^)]*)?\)", text):
        t = m.group(1)
        if t.startswith(("http://", "https://")):
            continue
        yield os.path.normpath(os.path.join(d, t))


def check():
    errors, warns = [], []
    all_notes = {}
    for p in notes():
        fm, text = frontmatter(p)
        if fm is None:
            errors.append(f"{p}: frontmatter 없음")
            continue
        all_notes[p] = fm
        for k in REQUIRED:
            if k not in fm or fm[k] in ("", []):
                errors.append(f"{p}: frontmatter `{k}` 누락")
        t = fm.get("type")
        if t not in TYPE_DIRS:
            errors.append(f"{p}: type `{t}` 는 {sorted(TYPE_DIRS)} 중 하나여야 함")
        elif not p.startswith(TYPE_DIRS[t] + "/"):
            errors.append(f"{p}: type `{t}` 인데 `{TYPE_DIRS[t]}/` 아래에 없음")
        if fm.get("status") not in STATUSES:
            errors.append(f"{p}: status `{fm.get('status')}` 는 {sorted(STATUSES)} 중 하나여야 함")
        if t in ("guide", "reference", "concept", "decision") and "verified" not in fm:
            errors.append(f"{p}: `verified` 항목 없음 (1차/2차 출처 구분 필수)")
        if t == "decision" and not re.match(r"decisions/\d{4}-", p):
            errors.append(f"{p}: decision 파일명은 NNNN- 로 시작")
        for target in links(p, text):
            if not os.path.exists(os.path.join(ROOT, target)):
                errors.append(f"{p}: 끊어진 링크 -> {target}")
    # 모든 비-지도 노트는 최소 한 지도에 실려야 한다 (경고)
    mapped = set()
    for p, fm in all_notes.items():
        if fm.get("type") == "map":
            mapped |= set(links(p, frontmatter(p)[1]))
    for p, fm in all_notes.items():
        if fm.get("type") != "map" and p not in mapped:
            warns.append(f"{p}: 어느 지도(maps/)에도 실려 있지 않음")
    # 태그 목록 미스매치(오타) 힌트: 단 한 노트에만 쓰인 태그
    count = {}
    for fm in all_notes.values():
        for tag in fm.get("tags", []):
            count[tag] = count.get(tag, 0) + 1
    for tag, n in sorted(count.items()):
        if n == 1:
            warns.append(f"태그 `{tag}` 는 노트 1개에만 쓰임 (오타 또는 새 도메인?)")
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(all_notes)} notes, {len(errors)} errors, {len(warns)} warnings")
    return 1 if errors else 0


def build_index():
    by_type = {k: [] for k in TYPE_DIRS}
    by_tag = {}
    for p in notes():
        fm, _ = frontmatter(p)
        if not fm or fm.get("type") not in TYPE_DIRS:
            continue
        by_type[fm["type"]].append((p, fm))
        for tag in fm.get("tags", []):
            by_tag.setdefault(tag, []).append((p, fm))
    out = [INDEX_START, "", "_`python3 tools/kb.py index` 로 생성. 손으로 고치지 말 것._", ""]
    out += ["### 지도 (도메인별 입구)"]
    out += [f"- [{fm['title']}]({p})" for p, fm in by_type["map"]] or ["- (없음)"]
    labels = [("guide", "guides"), ("reference", "reference"), ("concept", "concepts"), ("decision", "decisions")]
    for t, label in labels:
        out += ["", f"### {label}"]
        if t == "reference":
            groups = {}
            for p, fm in by_type[t]:
                groups.setdefault(p.split("/")[1], []).append((p, fm))
            for tool, items in sorted(groups.items()):
                out.append(f"- {tool}")
                out += [f"  - [{fm['title']}]({p})" for p, fm in items]
        else:
            out += [f"- [{fm['title']}]({p})" for p, fm in by_type[t]] or ["- (없음)"]
    out += ["", "### 태그"]
    out += [f"- `{tag}`: " + ", ".join(f"[{fm['title']}]({p})" for p, fm in items)
            for tag, items in sorted(by_tag.items())]
    out += ["", INDEX_END]
    readme_path = os.path.join(ROOT, "README.md")
    readme = open(readme_path, encoding="utf-8").read()
    if INDEX_START not in readme or INDEX_END not in readme:
        sys.exit("README.md 에 index:start / index:end 마커가 없음")
    pre, rest = readme.split(INDEX_START, 1)
    _, post = rest.split(INDEX_END, 1)
    open(readme_path, "w", encoding="utf-8").write(pre + "\n".join(out) + post)
    print(f"README.md 인덱스 갱신: {sum(len(v) for v in by_type.values())} notes, {len(by_tag)} tags")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        sys.exit(check())
    elif cmd == "index":
        build_index()
    else:
        sys.exit(__doc__)
