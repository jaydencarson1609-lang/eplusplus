"""Build websites from plain English E++ code."""

from __future__ import annotations

import html
import webbrowser
from pathlib import Path


COLORS = {
    "white": "#ffffff",
    "black": "#111111",
    "red": "#ef4444",
    "blue": "#3b82f6",
    "green": "#22c55e",
    "yellow": "#eab308",
    "purple": "#a855f7",
    "pink": "#ec4899",
    "orange": "#f97316",
    "gray": "#6b7280",
    "grey": "#6b7280",
    "skyblue": "#38bdf8",
    "sky blue": "#38bdf8",
    "lightblue": "#93c5fd",
    "darkblue": "#1e3a8a",
    "coral": "#fb7185",
    "mint": "#6ee7b7",
    "lavender": "#c4b5fd",
}


def css_color(value: str) -> str:
    lower = value.strip().lower()
    if lower in COLORS:
        return COLORS[lower]
    if value.startswith("#") or value.startswith("rgb"):
        return value
    return value


class WebBuilder:
    def __init__(self) -> None:
        self.title = "My E++ Website"
        self.background = "#f0f9ff"
        self.text_color = "#1e293b"
        self.font = "system-ui, sans-serif"
        self.blocks: list[str] = []
        self.saved_path: Path | None = None

    def start(self, title: str) -> None:
        self.title = title
        self.blocks.clear()
        self.saved_path = None

    def set_background(self, color: str) -> None:
        self.background = css_color(color)

    def set_text_color(self, color: str) -> None:
        self.text_color = css_color(color)

    def set_font(self, font_name: str) -> None:
        fonts = {
            "comic": "Comic Sans MS, cursive",
            "arial": "Arial, sans-serif",
            "times": "Times New Roman, serif",
            "mono": "ui-monospace, monospace",
            "system": "system-ui, sans-serif",
        }
        self.font = fonts.get(font_name.lower(), font_name)

    def add_heading(self, text: str, level: int = 1) -> None:
        level = max(1, min(3, level))
        tag = f"h{level}"
        self.blocks.append(f"<{tag}>{html.escape(text)}</{tag}>")

    def add_paragraph(self, text: str) -> None:
        self.blocks.append(f"<p>{html.escape(text)}</p>")

    def add_button(self, label: str, url: str | None = None) -> None:
        if url:
            self.blocks.append(
                f'<a class="btn" href="{html.escape(url, quote=True)}">{html.escape(label)}</a>'
            )
        else:
            self.blocks.append(f'<button class="btn" type="button">{html.escape(label)}</button>')

    def add_link(self, text: str, url: str) -> None:
        self.blocks.append(
            f'<p><a href="{html.escape(url, quote=True)}">{html.escape(text)}</a></p>'
        )

    def add_image(self, src: str, alt: str = "picture") -> None:
        self.blocks.append(
            f'<img src="{html.escape(src, quote=True)}" alt="{html.escape(alt)}" />'
        )

    def add_list(self, items: list[object]) -> None:
        parts = "".join(f"<li>{html.escape(str(item))}</li>" for item in items)
        self.blocks.append(f"<ul>{parts}</ul>")

    def add_input(self, label: str, placeholder: str = "") -> None:
        ph = html.escape(placeholder or label)
        self.blocks.append(
            f'<label class="field">{html.escape(label)}'
            f'<input type="text" placeholder="{ph}" /></label>'
        )

    def add_divider(self) -> None:
        self.blocks.append("<hr />")

    def add_html(self, raw: str) -> None:
        self.blocks.append(raw)

    def render(self) -> str:
        body = "\n        ".join(self.blocks) if self.blocks else "<p>Your website is ready!</p>"
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(self.title)}</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      font-family: {self.font};
      background: {self.background};
      color: {self.text_color};
      max-width: 720px;
      margin: 0 auto;
      padding: 2rem 1.25rem 3rem;
      line-height: 1.6;
    }}
    h1 {{ font-size: 2.2rem; margin-bottom: 0.5rem; }}
    h2 {{ font-size: 1.6rem; }}
    h3 {{ font-size: 1.25rem; }}
    p {{ margin: 0.75rem 0; }}
    a {{ color: #2563eb; }}
    img {{
      max-width: 100%;
      border-radius: 12px;
      margin: 1rem 0;
      box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }}
    ul {{ padding-left: 1.25rem; }}
    li {{ margin: 0.35rem 0; }}
    .btn {{
      display: inline-block;
      background: #2563eb;
      color: white !important;
      text-decoration: none;
      border: none;
      padding: 0.75rem 1.25rem;
      border-radius: 10px;
      font-size: 1rem;
      margin: 0.75rem 0;
      cursor: pointer;
    }}
    .field {{
      display: block;
      margin: 1rem 0;
      font-weight: 600;
    }}
    .field input {{
      display: block;
      width: 100%;
      margin-top: 0.35rem;
      padding: 0.65rem 0.75rem;
      border: 2px solid #cbd5e1;
      border-radius: 8px;
      font-size: 1rem;
    }}
    hr {{
      border: none;
      border-top: 2px dashed #cbd5e1;
      margin: 1.5rem 0;
    }}
    footer {{
      margin-top: 2rem;
      font-size: 0.9rem;
      opacity: 0.7;
    }}
  </style>
</head>
<body>
        {body}
        <footer>Made with E++ (English++)</footer>
</body>
</html>
"""

    def save(self, path: Path) -> Path:
        path = path if path.suffix else path.with_suffix(".html")
        path.write_text(self.render(), encoding="utf-8")
        self.saved_path = path.resolve()
        return self.saved_path

    def open_in_browser(self) -> None:
        if not self.saved_path:
            raise RuntimeError("Save the website first with: save website to \"my_site.html\"")
        webbrowser.open(self.saved_path.as_uri())
