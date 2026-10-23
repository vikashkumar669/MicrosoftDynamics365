# Manuscript sources

Markdown sources for *Azure Functions for Microsoft Dynamics 365 & Power Platform* (© 2026 Vikash Kumar, self-published).

| Path | Contents |
| --- | --- |
| `chapters/` | One Markdown file per chapter (`ch01-introduction.md` …) |
| `figures/` | Diagrams (Mermaid / draw.io sources and rendered SVG) and screenshots |
| `capture-plan.csv` | Every screenshot to capture, with path, annotations and caption |
| `out/` | Build output (DOCX, PDF) – git-ignored |

| `templates/chapter-template.md` | The 21-section template every chapter starts from |
| `STYLE.md` | Writing, code, figure and accessibility rules |
| `build/` | Print CSS, Pandoc filter, Word reference document, fonts, build script |

## Building

```bash
# Needs pandoc 3.x, WeasyPrint, cairosvg, and Mermaid CLI (mmdc) for .mmd figures
book/build/build.sh book/chapters/ch06-sample.md
# -> book/out/ch06-sample.pdf (print layout) and .docx (editable manuscript)
```

Code listings are not typed into chapters by hand: they are pulled from the compiled projects in `../src` by `// <listing id>` region markers, so the printed code always matches code that CI has built.

All companies, products, people and data in the book are fictional.
