---
name: md-to-html
description: Convert markdown files to styled HTML pages using ghmd-js (GitHub-flavored markdown renderer) and move them to the workspace pub/ folder. Use when the user wants to publish, preview, or share a markdown document as a web page.
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["npx"]}}}
---

# Markdown to HTML

Convert markdown files into GitHub-styled HTML pages using `ghmd-js`. Output goes to `<workspace>/pub/`.

## When to Use

- User wants to convert a `.md` file to HTML
- User wants to publish or preview a markdown document as a web page
- User asks to make a document "shareable" or "presentable"
- Chaining with other skills (e.g., x-to-markdown → md-to-html → r2-upload)

## Usage

```bash
# Convert with embedded CSS, dark mode (self-contained HTML)
npx ghmd-js --embed-css --dark <input.md>

# Output goes to same directory as input, with .html extension
# Then move to pub/:
mv <input-basename>.html <workspace>/pub/
```

### Options

| Flag | Description |
|------|-------------|
| `--embed-css` | Embed CSS inline (self-contained file) — **always use this** |
| `--dark` | Dark theme only |
| `--light` | Light theme only |
| `--no-gfm` | Plain markdown instead of GitHub Flavored Markdown |

### Workflow

1. Run `npx ghmd-js --embed-css <input.md>`
2. Move the resulting `.html` file to `<workspace>/pub/`
3. Optionally upload via R2 for sharing

### Example

```bash
npx ghmd-js --embed-css --dark exports/article.md
mv exports/article.html pub/
```

## Integration with Other Skills

Works well chained with:
- **x-to-markdown** → export tweet → convert to HTML page
- **r2-upload** → convert to HTML → upload for sharing
- **news-summary** → generate summary → publish as HTML

## Notes

- Uses GitHub's markdown styling — tables, code blocks, task lists all render properly
- `--embed-css` makes the file fully self-contained (no external stylesheets)
- Output file is placed next to the input file by default, so move to `pub/` after
