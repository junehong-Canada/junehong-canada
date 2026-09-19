import re
import yaml
from pathlib import Path

def main():
    script_dir = Path(__file__).parent
    posts_dir = script_dir / "../posts"
    blog_html = script_dir / "../blog.html"

    print(f"Updating blog index in {blog_html}...")

    posts = []
    if posts_dir.exists():
        for md_file in posts_dir.glob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        meta = yaml.safe_load(parts[1])
                        # Determine output filename (md -> html)
                        html_filename = md_file.with_suffix(".html").name
                        
                        posts.append({
                            "title": meta.get("title", "Untitled"),
                            "description": meta.get("description", ""),
                            "date": str(meta.get("date", "")),
                            "link": f"posts/{html_filename}",
                            "author": meta.get("author", ""),
                            "tags": meta.get("tags", [])
                        })
            except Exception as e:
                print(f"Skipping {md_file.name}: {e}")

    # Sort by date (newest first)
    posts.sort(key=lambda x: x["date"], reverse=True)

    cards = []
    for p in posts:
        tags_html = ""
        if p.get("tags"):
            # Show only first 3 tags to keep card clean
            tags_html = '<div class="tags-container" style="margin-bottom: 0.5rem;">' + "".join([f'<span class="tag">{t}</span>' for t in p['tags'][:3]]) + '</div>'

        card = f"""
        <div class="blog-card">
          <h3>{p['title']}</h3>
          {tags_html}
          <p>{p['description']}</p>
          <div class="blog-meta">
            <span>{p['date']}</span>
            <a class="read-more" href="{p['link']}">Read more →</a>
          </div>
        </div>"""
        cards.append(card)

    html_cards = "\n".join(cards)

    if blog_html.exists():
        content = blog_html.read_text(encoding="utf-8")
        start_marker = "<!-- BLOG_LIST_START -->"
        end_marker = "<!-- BLOG_LIST_END -->"

        if start_marker in content and end_marker in content:
            pattern = re.compile(f"({re.escape(start_marker)}).*?({re.escape(end_marker)})", re.DOTALL)
            new_content = pattern.sub(f"\\1\n{html_cards}\n\\2", content)
            blog_html.write_text(new_content, encoding="utf-8")
            print(f"Blog index updated with {len(posts)} posts.")
        else:
            print("Markers not found in blog.html.")
    else:
        print("blog.html not found.")

if __name__ == "__main__":
    main()