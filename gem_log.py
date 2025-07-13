# gem_log.py
import os, re, random
import markdown, frontmatter
from bs4 import BeautifulSoup, NavigableString, Tag

# Constants and config
INDEX_ASTRO = "src/pages/index.astro"
ABOUT_ASTRO = "src/pages/about/index.astro"
BLOG_DIR = "src/content/blog/"
OUTPUT_DIR = "gemlog"
RELATED_COUNT = 5


def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)


def clean_html_to_gemtext(html):
    soup = BeautifulSoup(html, "html.parser")
    out = []

    def rec(n):
        if isinstance(n, NavigableString):
            out.append(str(n))
        elif isinstance(n, Tag):
            name = n.name
            if name in ("br",):
                out.append("\n")
            elif name in ("p", "div"):
                out.append("\n\n")
                [rec(c) for c in n.children]
                out.append("\n\n")
            elif name in ("em", "i"):
                out.append("*")
                [rec(c) for c in n.children]
                out.append("*")
            elif name in ("strong", "b"):
                out.append("**")
                [rec(c) for c in n.children]
                out.append("**")
            elif name == "code":
                out.append("`" + n.get_text() + "`")
            else:
                [rec(c) for c in n.children]

    rec(soup)
    text = "".join(out)
    text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)
    text = re.sub(r" +", " ", text)
    return text.strip()


def parse_astro_intro(path):
    try:
        raw = open(path, "r", encoding="utf-8").read()
        s, e = raw.find("<p"), raw.find("</p>", raw.find("<p"))
        sect = raw[s : e + 4]
        return clean_html_to_gemtext(sect)
    except Exception as e:
        return f"(Failed to parse intro: {e})"


def convert_blog(filepath, blog_list):
    post = frontmatter.load(filepath)
    html = markdown.markdown(post.content, extensions=["extra"])
    body = clean_html_to_gemtext(html)

    slug = os.path.splitext(os.path.basename(filepath))[0]
    fname = f"{slug}.gmi"
    outp = os.path.join(OUTPUT_DIR, fname)

    # Related posts
    others = [b for b in blog_list if b[0] != fname]
    random.shuffle(others)
    related = others[:RELATED_COUNT]

    with open(outp, "w", encoding="utf-8") as f:
        f.write(f"# {post['title']}\n\n")
        if "pubDate" in post:
            f.write(f"**Date:** {post['pubDate']}\n\n")
        if "description" in post:
            f.write(f"**Summary:** {post['description']}\n\n")
        f.write(body + "\n\n")
        f.write("=> index.gmi ⬅ Back to Index\n\n")
        if related:
            f.write("### Explore more posts:\n")
            for p, t in related:
                f.write(f"=> {p} {t}\n")
    return fname, post["title"]


def write_index(intro, blogs):
    with open(os.path.join(OUTPUT_DIR, "index.gmi"), "w", encoding="utf-8") as f:
        f.write("# eejdev Index\n\n")
        f.write(intro + "\n\n")
        f.write("### Blog Posts\n")
        for p, t in blogs:
            f.write(f"=> {p} {t}\n")


def convert_about():
    # similar to intro
    sect = parse_astro_intro(ABOUT_ASTRO)
    with open(os.path.join(OUTPUT_DIR, "about.gmi"), "w", encoding="utf-8") as f:
        f.write("# About\n\n")
        f.write(sect + "\n")


def main():
    ensure_output_dir(OUTPUT_DIR)
    intro = parse_astro_intro(INDEX_ASTRO)
    files = sorted(f for f in os.listdir(BLOG_DIR) if f.endswith(".md"))
    blogs = []
    for fn in files:
        meta = frontmatter.load(os.path.join(BLOG_DIR, fn))
        slug = os.path.splitext(fn)[0]
        blogs.append((f"{slug}.gmi", meta["title"]))
    # generate
    for fn in files:
        convert_blog(os.path.join(BLOG_DIR, fn), blogs)
    write_index(intro, blogs)
    convert_about()
    print("✅ Gemini export complete.")


if __name__ == "__main__":
    main()
