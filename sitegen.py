import pypandoc
from pathlib import Path
import os
import sys
import shutil
from typing import List


def get_blog_dir() -> Path:
    BLOG_MD_DIR = os.getenv("BLOG_MD_DIR")
    if BLOG_MD_DIR:
        return Path(os.path.expanduser(BLOG_MD_DIR))

    OBSIDIAN_HOME = os.getenv("OBSIDIAN_HOME")
    if not OBSIDIAN_HOME:
        print("Path to Obsidian vault not found. Set env variable OBSIDIAN_HOME")
        sys.exit(1)

    obsidian_blog_path = (
        Path(os.path.expanduser(OBSIDIAN_HOME)) / "hacker-book" / "Blog"
    )

    return obsidian_blog_path


BLOG_MD_DIR = get_blog_dir()
TARGET_DIR = Path("./docs")

print(f"Using blog dir at: ", str(BLOG_MD_DIR))


def gen_html(md: Path, append=None):
    html_file = TARGET_DIR / md.with_suffix(".html").relative_to(BLOG_MD_DIR)
    print(f"Converting {md} to {html_file}")

    with open(md, "r") as f:
        contents = f.read()

        if append:
            contents += append

    output = pypandoc.convert_text(
        contents, to="html", format="markdown", extra_args=["--ascii"]
    )

    html_file.parent.mkdir(parents=True, exist_ok=True)

    with open(html_file, "w") as f:
        f.write(output)


def generate_posts(posts_dir: Path):
    for file in posts_dir.rglob("*"):
        if file.is_dir():
            continue

        if file.suffix == ".md":
            gen_html(file)
        else:
            target = TARGET_DIR / file.relative_to(BLOG_MD_DIR)
            target.parent.mkdir(exist_ok=True, parents=True)
            shutil.copy(file, target)


shutil.rmtree(TARGET_DIR, ignore_errors=True)
TARGET_DIR.mkdir(exist_ok=False)

posts_section = "\n"

for d in BLOG_MD_DIR.iterdir():
    if d.is_dir():
        generate_posts(d)


for d in TARGET_DIR.iterdir():
    if not d.is_dir():
        continue

    # Generate posts subsection
    heading = f"### {d.name}\n"
    for file in d.iterdir():
        if file.is_file() and file.suffix == ".html":
            p = f"- [{file.with_suffix('').name}]({file.relative_to(TARGET_DIR)})\n"
            heading += p

    heading += "\n\n"
    posts_section += heading

home_md = BLOG_MD_DIR / "Home.md"
gen_html(home_md, append=posts_section)

home_html = TARGET_DIR / "Home.html"
home_html.rename(TARGET_DIR / "index.html")
