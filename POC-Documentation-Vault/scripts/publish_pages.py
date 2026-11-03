#!/usr/bin/env python3
"""Build a styled GitHub Pages site from the public wiki and project Markdown."""

from __future__ import annotations

import html
import os
import re
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlsplit

import markdown


VAULT = Path(__file__).resolve().parents[1]
OUTPUT = VAULT / "_site"
LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\]\(([^)\s]+\.md(?:#[^)\s]*)?)", re.IGNORECASE)
FRONT_MATTER_PATTERN = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n?", re.DOTALL)
FENCE_PATTERN = re.compile(r"^\s*(```|~~~)")

STYLE = """
:root {
  color-scheme: dark;
  --bg: #0a0a0f;
  --surface: #12121a;
  --surface2: #1a1a25;
  --border: #2a2a3a;
  --text: #e8e8f0;
  --text-dim: #a0a0b5;
  --accent: #818cf8;
  --accent2: #a78bfa;
  --code-bg: #1e1e2e;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font: 16px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
a { color: var(--accent); text-decoration: none; }
a:hover { color: var(--accent2); text-decoration: underline; }
.layout { min-height: 100vh; display: grid; grid-template-columns: 280px minmax(0, 1fr); }
aside {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  padding: 1.5rem 1rem;
  background: var(--surface);
  border-right: 1px solid var(--border);
}
.brand { display: block; margin: 0 0 1.5rem; color: var(--text); }
.brand strong {
  display: block;
  font-size: 1.25rem;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.brand span { color: var(--text-dim); font-size: .85rem; }
.nav-group { margin: 1.25rem 0; }
.nav-group h2 {
  margin: 0 0 .45rem;
  color: var(--text-dim);
  font-size: .72rem;
  font-weight: 700;
  letter-spacing: .1em;
  text-transform: uppercase;
}
.nav-group ul { list-style: none; margin: 0; padding: 0; }
.nav-group li { margin: .15rem 0; }
.nav-group a {
  display: block;
  padding: .35rem .55rem;
  border-radius: .4rem;
  color: var(--text-dim);
  font-size: .9rem;
}
.nav-group a:hover, .nav-group a.active {
  background: var(--surface2);
  color: var(--text);
  text-decoration: none;
}
main { min-width: 0; padding: 2rem clamp(1rem, 5vw, 4rem); }
.page { width: min(100%, 1000px); margin: 0 auto; }
.page-header { margin: 0 0 1.5rem; }
.page-header h1 {
  margin: 0;
  font-size: clamp(1.8rem, 4vw, 2.5rem);
  line-height: 1.2;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.card {
  padding: clamp(1rem, 3vw, 2rem);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: .75rem;
  overflow-wrap: anywhere;
}
.card h1 { margin-top: 0; }
h2, h3, h4 { line-height: 1.3; color: var(--text); }
h2 { margin-top: 2rem; }
h3, h4 { margin-top: 1.5rem; color: var(--accent); }
p, li, blockquote { color: var(--text-dim); }
li { margin: .25rem 0; }
blockquote {
  margin: 1rem 0;
  padding: .25rem 1rem;
  background: var(--surface2);
  border-left: 3px solid var(--accent);
}
table { width: 100%; margin: 1rem 0; border-collapse: collapse; font-size: .92rem; }
th, td { padding: .7rem; border-bottom: 1px solid var(--border); text-align: left; vertical-align: top; }
th { background: var(--surface2); color: var(--text); }
tr:hover { background: var(--surface2); }
pre {
  overflow-x: auto;
  padding: 1rem;
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: .5rem;
  font-size: .88rem;
  line-height: 1.5;
}
code { color: var(--accent); font-family: "SF Mono", Consolas, monospace; }
pre code { color: var(--text); }
hr { border: 0; border-top: 1px solid var(--border); }
img { max-width: 100%; height: auto; }
footer { margin: 1.5rem auto 0; color: var(--text-dim); font-size: .8rem; }
@media (max-width: 760px) {
  .layout { display: block; }
  aside { position: static; height: auto; max-height: 40vh; border-right: 0; border-bottom: 1px solid var(--border); }
  main { padding: 1.25rem .75rem; }
}
"""


def page_title(path: Path, text: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*#*\s*$", line)
        if match:
            return re.sub(r"[`*_]", "", match.group(1)).strip()
    if path.name.casefold() == "readme.md":
        return "Overview"
    return path.stem.replace("-", " ").replace("_", " ").title()


def source_pages() -> list[Path]:
    pages = [VAULT / "README.md"]
    for folder in ("wiki", "projects"):
        pages.extend((VAULT / folder).rglob("*.md"))
    return sorted((path for path in pages if path.is_file()), key=lambda path: path.relative_to(VAULT).as_posix().casefold())


def output_path(source: Path) -> Path:
    relative = source.relative_to(VAULT)
    if relative.as_posix().casefold() == "readme.md":
        return OUTPUT / "index.html"
    return (OUTPUT / relative).with_suffix(".html")


def page_lookup(pages: list[Path]) -> tuple[dict[str, Path], dict[str, list[Path]]]:
    by_path: dict[str, Path] = {}
    by_stem: dict[str, list[Path]] = {}
    for page in pages:
        key = page.relative_to(VAULT).with_suffix("").as_posix().casefold()
        by_path[key] = page
        by_stem.setdefault(page.stem.casefold(), []).append(page)
    return by_path, by_stem


def resolve_page(target: str, current: Path, by_path: dict[str, Path], by_stem: dict[str, list[Path]]) -> Path | None:
    target = unquote(target.replace("\\", "/").strip())
    target_path = PurePosixPath(target)
    if target_path.suffix.casefold() == ".md":
        target_path = target_path.with_suffix("")

    candidates = []
    if not target_path.is_absolute():
        candidates.append((current.relative_to(VAULT).parent / target_path).as_posix().casefold())
    candidates.append(target_path.as_posix().lstrip("./").casefold())
    for key in candidates:
        if key in by_path:
            return by_path[key]

    matches = by_stem.get(target_path.name.casefold(), [])
    return matches[0] if len(matches) == 1 else None


def page_url(source: Path, destination: Path, anchor: str = "") -> str:
    current_output = output_path(source)
    url = os.path.relpath(destination, current_output.parent).replace(os.sep, "/")
    url = quote(url, safe="/.-_")
    if anchor:
        slug = re.sub(r"[^\w-]", "", anchor.casefold().replace(" ", "-"))
        url += f"#{quote(slug, safe='-_')}"
    return url


def rewrite_links(text: str, current: Path, by_path: dict[str, Path], by_stem: dict[str, list[Path]]) -> str:
    def replace_wikilink(match: re.Match[str]) -> str:
        target_and_label = match.group(1)
        target, separator, label = target_and_label.partition("|")
        target, hashmark, anchor = target.partition("#")
        resolved = resolve_page(target, current, by_path, by_stem)
        if resolved is None:
            return label.strip() if separator else target.strip()
        title = label.strip() if separator else Path(target).stem.replace("-", " ").replace("_", " ")
        href = page_url(current, output_path(resolved), anchor if hashmark else "")
        return f"[{title}]({href})"

    def replace_markdown_link(match: re.Match[str]) -> str:
        destination = match.group(1)
        parsed = urlsplit(destination)
        resolved = resolve_page(parsed.path, current, by_path, by_stem)
        if resolved is None:
            return match.group(0)
        href = page_url(current, output_path(resolved), parsed.fragment)
        return f"]({href}"

    lines = []
    fence_character = None
    for line in text.splitlines(keepends=True):
        fence = FENCE_PATTERN.match(line)
        if fence:
            character = fence.group(1)[0]
            if fence_character is None:
                fence_character = character
            elif fence_character == character:
                fence_character = None
            lines.append(line)
            continue
        if fence_character is None:
            line = LINK_PATTERN.sub(replace_wikilink, line)
            line = MARKDOWN_LINK_PATTERN.sub(replace_markdown_link, line)
        lines.append(line)
    return "".join(lines)


def navigation(pages: list[Path], current: Path) -> str:
    groups: dict[str, list[Path]] = {"Overview": [], "Wiki": [], "Projects": []}
    for page in pages:
        relative = page.relative_to(VAULT)
        group = "Overview" if relative.as_posix().casefold() == "readme.md" else relative.parts[0].title()
        if group in groups:
            groups[group].append(page)

    sections = []
    for name, members in groups.items():
        if not members:
            continue
        links = []
        for page in members:
            label = page_title(page, page.read_text(encoding="utf-8-sig"))
            active = " class=\"active\"" if page == current else ""
            href = page_url(current, output_path(page))
            links.append(f'<li><a{active} href="{html.escape(href, quote=True)}">{html.escape(label)}</a></li>')
        sections.append(f'<section class="nav-group"><h2>{html.escape(name)}</h2><ul>{"".join(links)}</ul></section>')
    return "".join(sections)


def render_page(source: Path, pages: list[Path], by_path: dict[str, Path], by_stem: dict[str, list[Path]]) -> str:
    text = source.read_text(encoding="utf-8-sig")
    text = FRONT_MATTER_PATTERN.sub("", text, count=1)
    title = page_title(source, text)
    text = re.sub(r"^#\s+.+?\s*#*\s*(?:\r?\n|$)", "", text, count=1)
    text = rewrite_links(text, source, by_path, by_stem)
    content = markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "sane_lists"],
        output_format="html5",
    )
    nav = navigation(pages, source)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(title, quote=True)} — POC Documentation">
  <title>{html.escape(title)} — POC Documentation</title>
  <style>{STYLE}</style>
</head>
<body>
  <div class="layout">
    <aside>
      <a class="brand" href="{html.escape(page_url(source, OUTPUT / 'index.html'), quote=True)}">
        <strong>POC Documentation</strong><span>Project research and decisions</span>
      </a>
      {nav}
    </aside>
    <main>
      <div class="page">
        <header class="page-header"><h1>{html.escape(title)}</h1></header>
        <article class="card">{content}</article>
        <footer>Generated from the POC-Documentation Markdown vault.</footer>
      </div>
    </main>
  </div>
</body>
</html>
"""


def main() -> None:
    pages = source_pages()
    if not pages:
        raise RuntimeError("No README.md, wiki/*.md, or projects/*.md pages were found.")

    by_path, by_stem = page_lookup(pages)
    for source in pages:
        destination = output_path(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render_page(source, pages, by_path, by_stem), encoding="utf-8")

    print(f"Published {len(pages)} Markdown pages to {OUTPUT}")


if __name__ == "__main__":
    main()
