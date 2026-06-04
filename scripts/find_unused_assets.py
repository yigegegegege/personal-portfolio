# -*- coding: utf-8 -*-
"""List asset files not referenced by HTML/CSS/JS."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_PARTS = {".git", "__pycache__", "scripts"}
ASSET_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".mp4", ".webm", ".txt"}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def collect_refs() -> set[str]:
    refs: set[str] = set()
    patterns = [
        re.compile(r"""(?:src|href|content)=["']([^"']+)["']"""),
        re.compile(r"""url\(["']?([^"')]+)["']?\)"""),
    ]
    for ext in ("html", "css", "js"):
        for path in ROOT.rglob(f"*.{ext}"):
            if should_skip(path):
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for pat in patterns:
                for m in pat.finditer(text):
                    raw = m.group(1).split("?")[0].split("#")[0]
                    if raw.startswith(("http://", "https://", "#", "tel:", "mailto:")):
                        continue
                    raw = raw.lstrip("./")
                    while raw.startswith("../"):
                        raw = raw[3:]
                    refs.add(raw.replace("\\", "/"))
    return refs


def main() -> None:
    refs = collect_refs()
    assets = [
        p
        for p in ROOT.rglob("*")
        if p.is_file() and p.suffix.lower() in ASSET_EXT and not should_skip(p)
    ]
    unused = sorted(
        p.relative_to(ROOT).as_posix()
        for p in assets
        if p.relative_to(ROOT).as_posix() not in refs
    )
    print(f"referenced paths: {len(refs)}")
    print(f"asset files: {len(assets)}")
    print(f"unused assets: {len(unused)}")
    for item in unused:
        print(item)


if __name__ == "__main__":
    main()
