# -*- coding: utf-8 -*-
"""Remove asset files not referenced by site HTML/CSS/JS."""
from __future__ import annotations

import re
import shutil
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
    removed_files = 0
    removed_dirs = 0

    # Whole folders that belong to removed sections.
    for folder in (ROOT / "assets" / "other",):
        if folder.is_dir():
            count = sum(1 for _ in folder.rglob("*") if _.is_file())
            shutil.rmtree(folder)
            removed_files += count
            removed_dirs += 1
            print(f"removed folder {folder.relative_to(ROOT)} ({count} files)")

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if should_skip(path):
            continue
        if path.suffix.lower() not in ASSET_EXT:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel not in refs:
            path.unlink()
            removed_files += 1
            print(f"removed {rel}")

    # Drop empty directories under assets.
    assets = ROOT / "assets"
    if assets.is_dir():
        for path in sorted(assets.rglob("*"), reverse=True):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
                removed_dirs += 1
                print(f"removed empty dir {path.relative_to(ROOT)}")

    print(f"done: {removed_files} files, {removed_dirs} dirs")


if __name__ == "__main__":
    main()
