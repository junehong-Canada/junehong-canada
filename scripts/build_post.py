import argparse
from pathlib import Path
from con_md_to_html import convert_md_to_html
from update_blog_index import main as update_blog_index

def main():
    parser = argparse.ArgumentParser(description="Build blog posts.")
    parser.add_argument("input", nargs="?", help="Specific Markdown file to build. If omitted, builds all in ../posts")
    args = parser.parse_args()

    if args.input:
        # Build specific file
        convert_md_to_html(args.input)
    else:
        # Build all files in posts directory
        script_dir = Path(__file__).parent
        posts_dir = script_dir / "../posts"
        
        if not posts_dir.exists():
            print(f"Error: Posts directory not found at {posts_dir}")
            return

        print(f"Building all posts in {posts_dir}...")
        for md_file in posts_dir.glob("*.md"):
            convert_md_to_html(md_file)
            
        print("Updating blog index...")
        update_blog_index()

if __name__ == "__main__":
    main()
