from pathlib import Path
import html
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = ROOT / "articles"
ARTICLES.mkdir(exist_ok=True)

# First look for articles inside scheduled/
scheduled = ROOT / "scheduled"
files = sorted(scheduled.glob("*.html")) if scheduled.exists() else []

# If scheduled/ is empty, use numbered articles from repository root
if not files:
    files = sorted(ROOT.glob("[0-9][0-9]-*.html"))

if not files:
    raise SystemExit("No articles remaining to publish.")

# Publish the first available article
source = files[0]
destination = ARTICLES / source.name
shutil.move(str(source), str(destination))

# Get all published articles
published = sorted(
    [
        p for p in ARTICLES.glob("*.html")
        if p.name != "index.html"
    ],
    reverse=True
)

# Build article listing
cards = []

for article in published:
    text = article.read_text(encoding="utf-8")

    match = re.search(
        r"<h1[^>]*>(.*?)</h1>",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        title = re.sub(r"<.*?>", "", match.group(1))
    else:
        title = article.stem.replace("-", " ").title()

    cards.append(
        f"""
        <article class="post">
            <div class="post-body">
                <span>GUIDE</span>
                <h3>{html.escape(title)}</h3>
                <a href="{html.escape(article.name)}">
                    Read guide →
                </a>
            </div>
        </article>
        """
    )

# Create articles index page
page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

<title>Digital Marketing Articles | Learning Digital Marketing</title>

<meta name="description"
content="Practical digital marketing guides covering SEO, AI, social media, affiliate marketing, dropshipping and online business.">

<link rel="canonical"
href="https://learningdigitalmarketing.online/articles/">

<link rel="stylesheet" href="../style.css">
</head>

<body>

<header class="site-header">
<div class="container nav-wrap">

<a class="logo" href="../index.html">
<span class="logo-mark">LD</span>
Learning<span>DigitalMarketing</span>
</a>

<nav class="nav">
<a href="../index.html">Home</a>
<a href="../index.html#learn">Learn</a>
<a href="index.html">Articles</a>
<a href="../index.html#contact">Contact</a>
</nav>

</div>
</header>

<main>

<section class="section">

<div class="container">

<p class="eyebrow">LATEST GUIDES</p>

<h1>Practical Digital Marketing Articles</h1>

<p class="hero-text">
New digital marketing guides published regularly.
Learn SEO, affiliate marketing, AI, social media and online business.
</p>

<div class="blog-grid">

{''.join(cards)}

</div>

</div>

</section>

</main>

<footer class="footer">

<div class="container footer-wrap">

<p>
Copyright 2026 Learning Digital Marketing.
</p>

<div>
<a href="../privacy.html">Privacy</a>
<a href="../affiliate-disclosure.html">Affiliate Disclosure</a>
<a href="../terms.html">Terms</a>
</div>

</div>

</footer>

</body>
</html>
"""

(ARTICLES / "index.html").write_text(
    page,
    encoding="utf-8"
)

# Update sitemap
urls = [
    "https://learningdigitalmarketing.online/",
    "https://learningdigitalmarketing.online/articles/",
    "https://learningdigitalmarketing.online/privacy.html",
    "https://learningdigitalmarketing.online/affiliate-disclosure.html",
    "https://learningdigitalmarketing.online/terms.html",
]

urls += [
    f"https://learningdigitalmarketing.online/articles/{p.name}"
    for p in published
]

xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
"""

for url in urls:
    xml += f"  <url><loc>{html.escape(url)}</loc></url>\n"

xml += "</urlset>\n"

(ROOT / "sitemap.xml").write_text(
    xml,
    encoding="utf-8"
)

print(f"Published: {source.name}")
print(f"Total published articles: {len(published)}")
