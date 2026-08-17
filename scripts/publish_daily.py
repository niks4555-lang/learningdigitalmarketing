from pathlib import Path
import html
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = ROOT / "articles"
SCHEDULED = ROOT / "scheduled"

ARTICLES.mkdir(exist_ok=True)

# ==============================
# GOOGLE ADSENSE CONFIGURATION
# ==============================

ADSENSE_CLIENT = "ca-pub-3382058697049306"
ADSENSE_SLOT = "3761462206"

ADSENSE_SCRIPT = f"""
<script async
src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}"
crossorigin="anonymous"></script>
"""

ADSENSE_UNIT = f"""
<div class="ad-container" style="margin:30px 0;text-align:center;">
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="{ADSENSE_CLIENT}"
     data-ad-slot="{ADSENSE_SLOT}"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({{}});
</script>
</div>
"""

# ==============================
# ADD ADSENSE TO HTML
# ==============================

def add_adsense(content, include_unit=True):

    # Add AdSense script only if it doesn't already exist
    if "pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" not in content:

        if "</head>" in content.lower():

            content = re.sub(
                r"</head>",
                ADSENSE_SCRIPT + "\n</head>",
                content,
                count=1,
                flags=re.IGNORECASE
            )

    # Add ad unit only if the slot is not already present
    if include_unit and ADSENSE_SLOT not in content:

        # Prefer placing the ad before footer
        if re.search(r"</main>", content, re.IGNORECASE):

            content = re.sub(
                r"</main>",
                ADSENSE_UNIT + "\n</main>",
                content,
                count=1,
                flags=re.IGNORECASE
            )

        elif re.search(r"</body>", content, re.IGNORECASE):

            content = re.sub(
                r"</body>",
                ADSENSE_UNIT + "\n</body>",
                content,
                count=1,
                flags=re.IGNORECASE
            )

    return content


# ==============================
# FIND SCHEDULED ARTICLE
# ==============================

files = sorted(
    SCHEDULED.glob("*.html")
) if SCHEDULED.exists() else []

# If scheduled folder is empty,
# use numbered articles from repository root
if not files:

    files = sorted(
        ROOT.glob("[0-9][0-9]-*.html")
    )

if not files:

    raise SystemExit("No articles remaining to publish.")


# ==============================
# PUBLISH FIRST ARTICLE
# ==============================

source = files[0]

destination = ARTICLES / source.name

shutil.move(
    str(source),
    str(destination)
)

print(f"Publishing: {source.name}")


# ==============================
# ADD ADSENSE TO NEW ARTICLE
# ==============================

article_text = destination.read_text(
    encoding="utf-8"
)

article_text = add_adsense(
    article_text,
    include_unit=True
)

destination.write_text(
    article_text,
    encoding="utf-8"
)


# ==============================
# UPDATE ADSENSE ON ALL ARTICLES
# ==============================

published = sorted(
    [
        p for p in ARTICLES.glob("*.html")
        if p.name != "index.html"
    ],
    reverse=True
)

for article in published:

    text = article.read_text(
        encoding="utf-8"
    )

    updated = add_adsense(
        text,
        include_unit=True
    )

    if updated != text:

        article.write_text(
            updated,
            encoding="utf-8"
        )

        print(
            f"AdSense updated: {article.name}"
        )


# ==============================
# BUILD ARTICLE LISTING
# ==============================

cards = []

for article in published:

    text = article.read_text(
        encoding="utf-8"
    )

    match = re.search(
        r"<h1[^>]*>(.*?)</h1>",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:

        title = re.sub(
            r"<.*?>",
            "",
            match.group(1)
        )

    else:

        title = article.stem.replace(
            "-",
            " "
        ).title()

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


# ==============================
# CREATE ARTICLES INDEX
# ==============================

page = f"""<!doctype html>

<html lang="en">

<head>

<meta charset="utf-8">

<meta name="viewport"
content="width=device-width,initial-scale=1">

<title>
Digital Marketing Articles | Learning Digital Marketing
</title>

<meta name="description"
content="Practical digital marketing guides covering SEO, AI, affiliate marketing, social media, dropshipping and online business.">

<link rel="canonical"
href="https://learningdigitalmarketing.online/articles/">

<link rel="stylesheet"
href="../style.css">

{ADSENSE_SCRIPT}

</head>

<body>

<header class="site-header">

<div class="container nav-wrap">

<a class="logo"
href="../index.html">

<span class="logo-mark">
LD
</span>

Learning<span>
DigitalMarketing
</span>

</a>

<nav class="nav">

<a href="../index.html">
Home
</a>

<a href="../index.html#learn">
Learn
</a>

<a href="index.html">
Articles
</a>

<a href="../index.html#contact">
Contact
</a>

</nav>

</div>

</header>


<main>

<section class="section">

<div class="container">

<p class="eyebrow">
LATEST GUIDES
</p>

<h1>
Practical Digital Marketing Articles
</h1>

<p class="hero-text">

New digital marketing guides published regularly.

Learn SEO, affiliate marketing, AI,
social media and online business.

</p>

{ADSENSE_UNIT}

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

<a href="../privacy.html">
Privacy
</a>

<a href="../affiliate-disclosure.html">
Affiliate Disclosure
</a>

<a href="../terms.html">
Terms
</a>

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


# ==============================
# UPDATE SITEMAP
# ==============================

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

<urlset
xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

"""


for url in urls:

    xml += (
        f"  <url>"
        f"<loc>{html.escape(url)}</loc>"
        f"</url>\n"
    )


xml += "</urlset>\n"


(ROOT / "sitemap.xml").write_text(
    xml,
    encoding="utf-8"
)


# ==============================
# FINAL STATUS
# ==============================

print("--------------------------------")
print("Daily publishing completed.")
print(f"Published article: {source.name}")
print(f"Total published articles: {len(published)}")
print("AdSense: Enabled")
print(f"AdSense Client: {ADSENSE_CLIENT}")
print(f"AdSense Slot: {ADSENSE_SLOT}")
print("--------------------------------")
