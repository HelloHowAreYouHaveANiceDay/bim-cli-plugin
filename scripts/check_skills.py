#!/usr/bin/env python3
"""Build/check skills/index.json and (optionally) run the Hermes skills scanner.

skills/index.json is the Agent Skills well-known index served at
https://bimcli.com/.well-known/skills/index.json (the bimcli.com Worker proxies
/.well-known/skills/* to this repo's skills/ folder on main).

Usage:
  python scripts/check_skills.py            # rewrite skills/index.json
  python scripts/check_skills.py --check    # fail if index.json is stale
  python scripts/check_skills.py --check --scan <path-to-hermes-agent-checkout>
                                            # also fail unless every skill scans SAFE
Stdlib only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
INDEX = SKILLS / "index.json"


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        raise ValueError("missing YAML frontmatter")
    out = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if km:
            val = km.group(2).strip()
            if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                val = val[1:-1]
            out[km.group(1)] = val
    return out


def build_index() -> dict:
    skills = []
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        d = skill_md.parent
        fm = frontmatter(skill_md.read_text(encoding="utf-8"))
        name, desc = fm.get("name", ""), fm.get("description", "")
        if name != d.name:
            raise ValueError(f"{skill_md}: frontmatter name {name!r} must match folder {d.name!r}")
        if not desc:
            raise ValueError(f"{skill_md}: missing description")
        files = sorted(
            p.relative_to(d).as_posix()
            for p in d.rglob("*")
            if p.is_file() and not any(part.startswith(".") for part in p.relative_to(d).parts)
        )
        files.remove("SKILL.md")
        skills.append({"name": name, "description": desc, "files": ["SKILL.md", *files]})
    return {"skills": skills}


def render(index: dict) -> str:
    return json.dumps(index, indent=2, ensure_ascii=False) + "\n"


def scan(hermes_dir: Path) -> bool:
    sys.path.insert(0, str(hermes_dir))
    from tools.skills_guard import format_scan_report, scan_skill, should_allow_install  # type: ignore

    ok = True
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        result = scan_skill(skill_md.parent, source="community")
        print(format_scan_report(result))
        allowed, _ = should_allow_install(result)
        if result.verdict != "safe" or not allowed:
            ok = False
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if skills/index.json is stale")
    ap.add_argument("--scan", metavar="HERMES_AGENT_DIR", help="run the Hermes skills scanner")
    args = ap.parse_args()

    want = render(build_index())
    if args.check:
        have = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
        if have.replace("\r\n", "\n") != want:
            print("skills/index.json is stale: run python scripts/check_skills.py", file=sys.stderr)
            return 1
        print("skills/index.json up to date")
    else:
        INDEX.write_text(want, encoding="utf-8", newline="\n")
        print(f"wrote {INDEX.relative_to(ROOT)}")

    if args.scan and not scan(Path(args.scan)):
        print("Hermes skills scan: not SAFE (community sources install only SAFE skills)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
