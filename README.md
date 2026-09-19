# junehong.github.io

Personal portfolio and blog website for June Hong.

## Project Structure

```text
├── index.html              # Main landing page
├── projects.html           # Projects portfolio
├── blog.html               # Blog index page
├── style.css               # Shared styles
├── templates/
│   └── post.html           # HTML template for blog posts
├── posts/                  # Markdown source files for blog posts
│   ├── *.md
│   └── *.html              # Generated HTML files
└── scripts/                # Build scripts
    ├── build_post.py       # Converts MD to HTML (all or single)
    ├── update_blog_index.py# Updates blog.html with latest posts
    └── run_build.bat/.sh   # One-click build scripts
```

## How to Add a New Blog Post

1.  Create a new Markdown file in the `posts/` directory (e.g., `posts/my-new-post.md`).
2.  Add the required Front Matter at the top of the file:

    ```markdown
    ---
    title: "My New Post Title"
    description: "A short summary of the post for the card view."
    date: "2026-01-15"
    author: "June Hong"
    ---

    # Content starts here...
    ```

3.  Run the build script to generate the HTML and update the index.

## How to Build

### Windows
Run the batch file:
```cmd
scripts\run_build.bat
```

### Linux / macOS
Run the shell script:
```bash
./scripts/run_build.sh
```

This will:
1.  Install Python dependencies (`markdown`, `pyyaml`).
2.  Convert all `.md` files in `posts/` to `.html` using the `templates/post.html` template.
3.  Update `blog.html` with the list of posts, sorted by date.
