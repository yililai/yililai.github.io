# Academic blog maintenance

- Preserve existing articles and permanent URLs. Do not replace a completed article with a summary. Never delete existing files without explicit user confirmation.
- Read `docs/BLOG_WORKFLOW.md` before adding or editing a post. Use primary paper / publisher / author sources; distinguish published, accepted, and preprint status.
- Edit generated article sources in `content/`, metadata in `data/posts.json`, and shared markup in `templates/article.html`. Run `python scripts/build_blog.py` and commit generated outputs together.
- Keep legacy FCN and U-Net pages unchanged until a deliberate, reviewed migration is authorized. The generator must not write legacy pages or rebuild homepage content outside its marked area.
- Store article figures in `assets/figures/<slug>/`, with source and permission records in `assets/figures/sources.json`. Use independently composed diagrams if reuse permission is unconfirmed. Code license does not imply paper-figure permission.
- Clearly label original-paper results, independent interpretation, and untested research proposals. Never invent metrics, citations or a successful publication / deployment.
- Check `python scripts/build_blog.py --check`, `python scripts/check_site.py`, `git diff --check`, and mobile / desktop layout after meaningful changes. The link checker documents one pre-existing U-Net navigation issue; do not silently expand its exception list.
- Use ordinary fast-forward Git operations. Review remote changes before pushing; do not force push or modify GitHub Pages settings as a side effect of content maintenance.
