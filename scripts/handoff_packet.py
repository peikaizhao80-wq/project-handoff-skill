#!/usr/bin/env python3
"""
Utility helpers for the project-handoff skill.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "session"


def resolve_handoff_dir(project_root: Path) -> Path:
    work_dir = project_root / "work"
    if work_dir.exists() and work_dir.is_dir():
        return work_dir / "agent-handoff"
    return project_root / ".codex-handoff"


def template_path() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "handoff-template.md"


def load_template() -> str:
    return template_path().read_text(encoding="utf-8")


def render_template(project_root: Path, snapshot_name: str, title: str) -> str:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    text = load_template()
    replacements = {
        "{{created_at}}": now,
        "{{project_root}}": str(project_root),
        "{{snapshot_name}}": snapshot_name,
        "{{title}}": title,
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def manifest_path(handoff_dir: Path) -> Path:
    return handoff_dir / "manifest.json"


def latest_path(handoff_dir: Path) -> Path:
    return handoff_dir / "LATEST.md"


def load_manifest(handoff_dir: Path) -> dict:
    path = manifest_path(handoff_dir)
    if not path.exists():
        return {"snapshots": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_manifest(handoff_dir: Path, data: dict) -> None:
    path = manifest_path(handoff_dir)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_manifest_after_snapshot(handoff_dir: Path, snapshot: Path) -> dict:
    data = load_manifest(handoff_dir)
    snapshots = [item for item in data.get("snapshots", []) if item != snapshot.name]
    snapshots.append(snapshot.name)
    data["snapshots"] = snapshots[-20:]
    data["latest_snapshot"] = snapshot.name
    data["updated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    save_manifest(handoff_dir, data)
    return data


def find_latest_snapshot(handoff_dir: Path) -> Path | None:
    pattern = sorted(handoff_dir.glob("handoff-*.md"))
    if not pattern:
        return None
    return pattern[-1]


def prepare_closeout(project_root: Path, title: str) -> dict:
    handoff_dir = resolve_handoff_dir(project_root)
    ensure_dir(handoff_dir)

    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    snapshot_name = f"handoff-{timestamp}-{slugify(title)}.md"
    snapshot_path = handoff_dir / snapshot_name

    if not snapshot_path.exists():
        snapshot_path.write_text(
            render_template(project_root, snapshot_name, title),
            encoding="utf-8",
        )

    manifest = update_manifest_after_snapshot(handoff_dir, snapshot_path)
    return {
        "mode": "closeout",
        "project_root": str(project_root),
        "handoff_dir": str(handoff_dir),
        "snapshot_path": str(snapshot_path),
        "latest_path": str(latest_path(handoff_dir)),
        "manifest_path": str(manifest_path(handoff_dir)),
        "latest_snapshot": manifest.get("latest_snapshot"),
    }


def prepare_takeover(project_root: Path) -> dict:
    handoff_dir = resolve_handoff_dir(project_root)
    ensure_dir(handoff_dir)
    latest_snapshot = find_latest_snapshot(handoff_dir)
    return {
        "mode": "takeover",
        "project_root": str(project_root),
        "handoff_dir": str(handoff_dir),
        "latest_path": str(latest_path(handoff_dir)),
        "manifest_path": str(manifest_path(handoff_dir)),
        "latest_snapshot_path": str(latest_snapshot) if latest_snapshot else None,
        "has_latest": latest_path(handoff_dir).exists(),
        "has_snapshot": latest_snapshot is not None,
    }


def publish_latest(project_root: Path, source: Path) -> dict:
    handoff_dir = resolve_handoff_dir(project_root)
    ensure_dir(handoff_dir)
    if not source.exists():
        raise FileNotFoundError(f"Snapshot does not exist: {source}")

    destination = latest_path(handoff_dir)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    manifest = update_manifest_after_snapshot(handoff_dir, source)
    return {
        "mode": "publish-latest",
        "project_root": str(project_root),
        "source": str(source),
        "latest_path": str(destination),
        "manifest_path": str(manifest_path(handoff_dir)),
        "latest_snapshot": manifest.get("latest_snapshot"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Helpers for project handoff packets.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    closeout = subparsers.add_parser("prepare-closeout")
    closeout.add_argument("--project-root", required=True)
    closeout.add_argument("--title", default="session")

    takeover = subparsers.add_parser("prepare-takeover")
    takeover.add_argument("--project-root", required=True)

    publish = subparsers.add_parser("publish-latest")
    publish.add_argument("--project-root", required=True)
    publish.add_argument("--source", required=True)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root).resolve()

    if args.command == "prepare-closeout":
        result = prepare_closeout(project_root, args.title)
    elif args.command == "prepare-takeover":
        result = prepare_takeover(project_root)
    else:
        result = publish_latest(project_root, Path(args.source).resolve())

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
