#!/usr/bin/env python3
"""Build the workshop site.

Reads every people/*.md file, turns each one into a card, and drops the cards
into site/template.html at the {{CARDS}} placeholder. Output goes to _site/.

Standard library only. No pip installs, no build tooling.

Design rule: ONE broken participant file must NEVER fail the build. Every file
is parsed inside its own try/except; anything unparseable is skipped with a
warning on stderr and the build carries on.
"""

from __future__ import annotations

import html
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PEOPLE_DIR = ROOT / "people"
SITE_DIR = ROOT / "site"
OUT_DIR = ROOT / "_site"

TEMPLATE = SITE_DIR / "template.html"
STYLESHEET = SITE_DIR / "style.css"

PLACEHOLDER = "{{CARDS}}"
COUNT_PLACEHOLDER = "{{COUNT}}"
LABEL_PLACEHOLDER = "{{PEOPLE_LABEL}}"


class PersonError(Exception):
    """Raised when a people/*.md file cannot be turned into a card."""


def warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


def parse_person(path: Path) -> dict[str, str]:
    """Parse one people/*.md file into {username, name, fact}.

    Format:
        # Display Name
        A fun fact about them, one or more lines.
    """
    username = path.stem.strip()
    if not username:
        raise PersonError("empty filename stem")

    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    # First non-empty line is the display name; "#" markers are decoration.
    name = ""
    rest_start = len(lines)
    for i, line in enumerate(lines):
        if line.strip():
            name = line.lstrip("#").strip()
            rest_start = i + 1
            break

    if not name:
        raise PersonError("no display name found (file is empty or blank)")

    fact = "\n".join(lines[rest_start:]).strip()
    if not fact:
        fact = "No fun fact yet — ask them in person."

    return {"username": username, "name": name, "fact": fact}


def render_card(person: dict[str, str]) -> str:
    """Render one card. Every field is HTML-escaped: this is user content."""
    username = html.escape(person["username"])
    name = html.escape(person["name"])

    # Preserve the participant's line breaks without trusting their markup.
    fact_lines = [html.escape(line) for line in person["fact"].splitlines()]
    fact = "<br>".join(line if line.strip() else "" for line in fact_lines)

    initial = html.escape(person["name"][:1].upper() or "?")

    return f"""      <article class="card">
        <div class="card-head">
          <span class="avatar" aria-hidden="true">{initial}</span>
          <div class="card-id">
            <h2 class="card-name">{name}</h2>
            <a class="card-user" href="https://github.com/{username}">@{username}</a>
          </div>
        </div>
        <p class="card-fact">{fact}</p>
      </article>"""


def collect_people() -> list[dict[str, str]]:
    if not PEOPLE_DIR.is_dir():
        warn(f"no people/ directory at {PEOPLE_DIR}; rendering an empty site")
        return []

    people: list[dict[str, str]] = []
    for path in sorted(PEOPLE_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue  # _EXAMPLE.md and friends are docs, not participants.
        try:
            people.append(parse_person(path))
        except Exception as exc:  # noqa: BLE001 - one bad file must not stop the build
            warn(f"skipping people/{path.name}: {exc}")

    people.sort(key=lambda p: p["username"].lower())
    return people


def main() -> int:
    try:
        template = TEMPLATE.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot read {TEMPLATE}: {exc}", file=sys.stderr)
        return 1

    if PLACEHOLDER not in template:
        print(f"error: {TEMPLATE} has no {PLACEHOLDER} placeholder", file=sys.stderr)
        return 1

    people = collect_people()
    cards = "\n".join(render_card(p) for p in people)
    if not cards:
        cards = '      <p class="empty">No one has been added yet. Be the first!</p>'

    page = (
        template.replace(PLACEHOLDER, cards)
        .replace(COUNT_PLACEHOLDER, str(len(people)))
        .replace(LABEL_PLACEHOLDER, "person" if len(people) == 1 else "people")
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "index.html").write_text(page, encoding="utf-8")

    try:
        shutil.copyfile(STYLESHEET, OUT_DIR / "style.css")
    except OSError as exc:
        warn(f"could not copy stylesheet: {exc}")

    print(f"Rendered {len(people)} people -> {OUT_DIR / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
