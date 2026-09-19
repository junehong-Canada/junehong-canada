import html
import math
import re
import sys
from pathlib import Path

import markdown
import yaml


def parse_front_matter(content):
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1]) or {}, parts[2]
    return {}, content


def render_post_template(title, description, author, date, tags, html_content, template_path):
    template = template_path.read_text(encoding="utf-8")
    title = html.escape(str(title), quote=True)
    description = html.escape(str(description), quote=True)
    author = html.escape(str(author), quote=True)
    date = html.escape(str(date), quote=True)

    word_count = len(re.findall(r"\S+", html_content))
    read_time = max(1, math.ceil(word_count / 200))

    tags_html = ""
    if tags:
        tags_html = "".join(
            f'<span class="tag">{html.escape(str(tag), quote=True)}</span>' for tag in tags
        )
        tags_html = f'<div class="tags-container">{tags_html}</div>'

    replacements = {
        "{{ title }}": title,
        "{{ description }}": description,
        "{{ author }}": author,
        "{{ date }}": date,
        "{{ read_time }}": str(read_time),
        "{{ tags_html }}": tags_html,
        "{{ article_content }}": html_content,
    }

    for old, new in replacements.items():
        template = template.replace(old, new)

    return template


def convert_md_to_html(md_file_path):
    md_path = Path(md_file_path)
    if not md_path.exists():
        print(f"File not found: {md_path}")
        return

    print(f"Converting {md_path.name}...")
    content = md_path.read_text(encoding="utf-8")
    meta, md_content = parse_front_matter(content)

    html_content = markdown.markdown(md_content, extensions=["fenced_code", "tables"])

    title = meta.get("title", "Blog Post")
    description = meta.get("description", "")
    author = meta.get("author", "June Hong")
    date = meta.get("date", "")
    tags = meta.get("tags", [])

    template_path = Path(__file__).resolve().parent.parent / "templates" / "post.html"
    template = render_post_template(title, description, author, date, tags, html_content, template_path)

    output_path = md_path.with_suffix(".html")
    output_path.write_text(template, encoding="utf-8")
    print(f"Generated {output_path.name}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        convert_md_to_html(sys.argv[1])
    else:
        print("Usage: con_md_to_html.py <markdown-file>")