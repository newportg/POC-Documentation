# POC-Documentation

A shared knowledge vault for project research, notes, and decisions.

- [[wiki/application-project-organisation|Project structure and workflow]]
- [[wiki/projects|Project index]]

The wiki and project Markdown pages are published to GitHub Pages with MkDocs
when changes are pushed to `master`. The site includes this README, `wiki/`, and
`projects/`; Copilot conversations, skills, prompts, and archived/raw content
are excluded by the MkDocs configuration. Set the repository's Pages source to
**GitHub Actions** for the first deployment.

Architecture diagrams are maintained as PlantUML source files using the
`!include <archimate/Archimate>` library. MkDocs publishes the source files with
the site so they can be rendered or reused separately.

To build locally from the repository root, run
`py -m mkdocs build --config-file mkdocs.yml --strict`.
