import argparse
import re
import yaml
from pathlib import Path
from con_md_to_html import convert_md_to_html

def update_project_index():
    script_dir = Path(__file__).parent
    projects_dir = script_dir / "../projects"
    projects_html = script_dir / "../projects.html"

    print(f"Updating project index in {projects_html}...")
    
    projects = []
    if projects_dir.exists():
        for md_file in projects_dir.glob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        meta = yaml.safe_load(parts[1])
                        projects.append({
                            "title": meta.get("title", "Untitled"),
                            "description": meta.get("description", ""),
                            "date": str(meta.get("date", "")),
                            "link": f"projects/{md_file.stem}.html",
                            "image": meta.get("image", "")
                        })
            except Exception as e:
                print(f"Skipping {md_file.name}: {e}")

    # Sort by date (newest first)
    projects.sort(key=lambda x: x["date"], reverse=True)

    cards = []
    for p in projects:
        img_html = ""
        if p.get("image"):
            img_html = f'<img src="{p["image"]}" alt="{p["title"]}" />'

        card = f"""
        <div class="project-card">
          {img_html}
          <h3>{p['title']}</h3>
          <p>{p['description']}</p>
          <a class="project-link" href="{p['link']}">View details →</a>
        </div>"""
        cards.append(card)

    html_cards = "\n".join(cards)

    if projects_html.exists():
        content = projects_html.read_text(encoding="utf-8")
        start_marker = "<!-- PROJECT_LIST_START -->"
        end_marker = "<!-- PROJECT_LIST_END -->"

        if start_marker in content and end_marker in content:
            pattern = re.compile(f"({re.escape(start_marker)}).*?({re.escape(end_marker)})", re.DOTALL)
            new_content = pattern.sub(f"\\1\n{html_cards}\n\\2", content)
            projects_html.write_text(new_content, encoding="utf-8")
            print(f"Project index updated with {len(projects)} projects.")
        else:
            print("Markers not found in projects.html.")
    else:
        print("projects.html not found.")

def main():
    parser = argparse.ArgumentParser(description="Build project pages.")
    parser.add_argument("input", nargs="?", help="Specific Markdown file to build. If omitted, builds all in ../projects")
    args = parser.parse_args()

    if args.input:
        # Build specific file
        convert_md_to_html(args.input)
    else:
        # Build all files in projects directory
        script_dir = Path(__file__).parent
        projects_dir = script_dir / "../projects"
        
        if not projects_dir.exists():
            print(f"Error: Projects directory not found at {projects_dir}")
            return

        print(f"Building all projects in {projects_dir}...")
        for md_file in projects_dir.glob("*.md"):
            convert_md_to_html(md_file)

        update_project_index()

if __name__ == "__main__":
    main()
