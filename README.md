# June Hong

## Introduction

June Hong is a software architect, technical leader, and innovator focused on
the convergence of **Physical AI, Edge AI, Digital Twins, and LLM systems**.
With more than 20 years of experience across embedded systems, cloud-native
platforms, mobile devices, and AI-driven cyber-physical systems, he designs
reliable software that connects intelligent models with real-world operations.

His current work includes cognitive layers for industrial assets, stateful
Digital Twin models, LangChain and LangGraph agent workflows, retrieval-
augmented generation (RAG), and quantized AI models running on edge hardware.
His career includes engineering and leadership work with organizations such as
Samsung, NTT, NEC, and VTech.

This repository contains June's personal portfolio, technical projects, blog,
marketing materials, and supporting resources. The site is built with plain
HTML, CSS, Markdown, and Python build scripts.

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

## Homepage Hosting

The homepage is deployed to GitHub Pages by
`.github/workflows/deploy-pages.yml` whenever changes are pushed to `main`.
To enable the first deployment, open the repository's **Settings > Pages** and
set **Source** to **GitHub Actions**. The workflow can also be started manually
from the **Actions** tab.
