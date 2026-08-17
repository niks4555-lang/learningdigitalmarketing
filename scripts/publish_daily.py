from pathlib import Path
import html, re, shutil

ROOT = Path(__file__).resolve().parents[1]
scheduled = ROOT / "scheduled"
articles = ROOT / "articles"
articles.mkdir(exist_ok=True)

files = sorted(scheduled.glob("*.html"))
if not files:
    raise SystemExit("No scheduled articles remaining.")

source = files[0]
shutil.move(str(source), str(articles / source.name))

published = sorted(
    [p for p in articles.glob("*.html") if p.name != "index.html"],
    reverse=True
)

cards = []
for p in published:
    text = p.read_text(encoding="utf-8")
    m = re.search(r"<h1>(.*?)</h1>", text, re.S)
    title = re.sub(r"<.*?>", "", m.group(1)) if m else p.stem
    cards.append(
        '<article class="post"><div class="post-body"><span>GUIDE</span>'
        f'<h3>{html.escape(title)}</h3><a href="{html.escape(p.name)}">Read guide →</a>'
        '</div></article>'
    )

page = (
    '<!doctype html><html lang="en"><head>'
    '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Latest Digital Marketing Articles | Learning Digital Marketing</title>'
    '<meta name="description" content="Latest practical guides on SEO, digital marketing, AI, affiliate marketing, social media and online business.">'
    '<link rel="canonical" href="https://learningdigitalmarketing.online/articles/">'
    '<link rel="stylesheet" href="../style.css"></head><body>'
    '<header class="site-header"><div class="container nav-wrap">'
    '<a class="logo" href="../index.html"><span class="logo-mark">LD</span>Learning<span>DigitalMarketing</span></a>'
    '<nav class="nav"><a href="../index.html">Home</a><a href="../index.html#learn">Learn</a><a href="index.html">Articles</a><a href="../index.html#contact">Contact</a></nav>'
    '</div></header><main><section class="section"><div class="container">'
    '<p class="eyebrow">LATEST GUIDES</p><h1>Practical Digital Marketing Articles</h1>'
    '<p class="hero-text">New guides are published regularly. Read, apply and come back for the next step.</p>'
    '<div class="blog-grid">' + ''.join(cards) + '</div>'
    '</div></section></main><footer class="footer"><div class="container footer-wrap">'
    '<p>Copyright 2026 Learning Digital Marketing.</p><div><a href="../privacy.html">Privacy</a>'
    '<a href="../affiliate-disclosure.html">Affiliate Disclosure</a><a href="../terms.html">Terms</a></div>'
    '</div></footer></body></html>'
)
(articles/"index.html").write_text(page, encoding="utf-8")

urls = [
    "https://learningdigitalmarketing.online/",
    "https://learningdigitalmarketing.online/privacy.html",
    "https://learningdigitalmarketing.online/affiliate-disclosure.html",
    "https://learningdigitalmarketing.online/terms.html",
    "https://learningdigitalmarketing.online/articles/"
]
urls += [f"https://learningdigitalmarketing.online/articles/{p.name}" for p in published]
xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
xml += ''.join(f'  <url><loc>{html.escape(u)}</loc></url>\n' for u in urls)
xml += '</urlset>\n'
(ROOT/"sitemap.xml").write_text(xml, encoding="utf-8")
