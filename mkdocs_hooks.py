"""MkDocs hooks for links authored in the Obsidian vault."""

from pathlib import Path, PurePosixPath
import posixpath
import re


WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")


def on_page_markdown(markdown: str, page, config, files) -> str:
    source = PurePosixPath(page.file.src_uri)
    docs_dir = Path(config["docs_dir"])
    available_files = {
        path.relative_to(docs_dir).as_posix().casefold(): path.relative_to(docs_dir).as_posix()
        for path in docs_dir.rglob("*")
        if path.is_file()
    }

    def replace(match: re.Match[str]) -> str:
        target_and_label = match.group(1)
        target, separator, label = target_and_label.partition("|")
        target, hashmark, anchor = target.partition("#")
        target = target.strip()
        if not target and hashmark and anchor:
            return f"[{label.strip() if separator else anchor.strip()}](#{anchor.strip().lower().replace(' ', '-')})"

        candidates = []
        if target:
            relative = (source.parent / target).as_posix()
            candidates.append(relative)
            candidates.append(f"{relative}.md")
            candidates.append(target)
            candidates.append(f"{target}.md")

        resolved = next(
            (available_files[candidate.casefold()] for candidate in candidates
             if candidate.casefold() in available_files),
            None,
        )
        if resolved is None:
            return match.group(0)

        text = label.strip() if separator else Path(target).stem.replace("-", " ")
        href = posixpath.relpath(resolved, source.parent.as_posix())
        if hashmark and anchor:
            href += f"#{anchor.strip().lower().replace(' ', '-')}"
        return f"[{text}]({href})"

    return WIKILINK.sub(replace, markdown)
