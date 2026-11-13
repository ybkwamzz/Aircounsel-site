import json, re, shutil
from datetime import datetime
from pathlib import Path

SITE_URL = "https://aircounsel.uk"
WORKSPACE_URL = "https://aircounsel-strata-core-production.up.railway.app/workspace"

TEMPLATE = """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | AirCounsel Institutional Research</title>
<meta name="description" content="{summary}">
<link rel="canonical" href="{site_url}/{slug}.html">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{summary}">
<meta property="og:image" content="{site_url}/og/{slug}.png">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "{title}",
  "description": "{summary}",
  "author": {{"@type": "Organization", "name": "AirCounsel Institutional Research"}},
  "publisher": {{"@type": "Organization", "name": "AirCounsel", "url": "{site_url}"}},
  "datePublished": "{date_iso}"
}}
</script>
<style>
  :root {{
    --paper: #FAF8F5;
    --card: #FFFFFF;
    --navy: #161E2E;
    --body: #2C3444;
    --muted: #5A6475;
    --stone: #D8D3C8;
    --stone-bg: #F1EFEA;
    --bronze: #8C6D3F;
  }}
  * {{ box-sizing: border-box; }}
  body {{ background: var(--paper); color: var(--body); font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 0; line-height: 1.78; }}
  .topbar-inst {{ background: var(--navy); color: #F3EFE6; padding: 14px 28px; font-size: 12px; font-family: ui-monospace, monospace; letter-spacing: 0.08em; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--bronze); }}
  .topbar-inst a {{ color: #DFC288; text-decoration: none; margin-left: 18px; }}
  .wrap {{ max-width: 820px; margin: 0 auto; padding: 38px 24px 84px; }}
  .breadcrumbs {{ font-size: 13px; color: var(--muted); margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid var(--stone); }}
  .breadcrumbs a {{ color: var(--navy); text-decoration: underline; text-underline-offset: 3px; }}
  .kicker {{ font-family: ui-monospace, monospace; color: var(--bronze); font-size: 12px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; }}
  h1 {{ font-size: 33px; line-height: 1.22; margin: 10px 0 16px; color: var(--navy); letter-spacing: -0.02em; }}
  .meta {{ font-family: ui-monospace, monospace; font-size: 12px; color: var(--muted); background: var(--stone-bg); border: 1px solid var(--stone); padding: 12px 16px; margin-bottom: 32px; }}
  h2 {{ color: var(--navy); font-size: 21px; margin-top: 38px; margin-bottom: 12px; border-bottom: 1px solid var(--stone); padding-bottom: 6px; }}
  p, li {{ color: var(--body); font-size: 16px; margin-bottom: 16px; }}
  blockquote {{ margin: 24px 0; padding: 16px 20px; background: var(--card); border-left: 4px solid var(--navy); border-top: 1px solid var(--stone); border-right: 1px solid var(--stone); border-bottom: 1px solid var(--stone); font-style: italic; color: var(--navy); }}
  table {{ width: 100%; border-collapse: collapse; margin: 22px 0; background: var(--card); font-size: 14px; }}
  th, td {{ border: 1px solid var(--stone); padding: 11px 14px; text-align: left; }}
  th {{ background: var(--stone-bg); color: var(--navy); }}
  .routing-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 16px; margin-top: 44px; padding-top: 28px; border-top: 1px solid var(--stone); }}
  .route-card {{ background: var(--card); border: 1px solid var(--stone); border-top: 3px solid var(--navy); padding: 18px; }}
  .route-card h4 {{ margin: 0 0 6px; color: var(--navy); font-size: 15px; }}
  .route-card p {{ margin: 0 0 10px; font-size: 13.5px; color: var(--muted); line-height: 1.5; }}
  .route-card a {{ color: var(--navy); font-size: 13.5px; font-weight: 600; text-decoration: underline; text-underline-offset: 3px; }}
</style>
</head>
<body>
<header class="topbar-inst">
  <span>AIRCOUNSEL // INSTITUTIONAL RESEARCH &amp; PRACTICE GOVERNANCE</span>
  <div>
    <a href="/insights.html">Research Index</a>
    <a href="{workspace_url}">V5.0 Workspace</a>
    <a href="https://aircounsel-strata-core-production.up.railway.app/specsheet">Technical Specsheet</a>
  </div>
</header>
<main class="wrap">
  <nav class="breadcrumbs">
    <a href="/">Home</a> &rsaquo; <a href="/insights.html">Institutional Research</a> &rsaquo; {pillar_category}
  </nav>
  <div class="kicker">{pillar_category}</div>
  <h1>{title}</h1>
  <div class="meta">PUBLISHED: {date_iso} &nbsp;&middot;&nbsp; AUDIENCE: {audience} &nbsp;&middot;&nbsp; PAPER REF: AC-RES-2026</div>
  <article>{body_html}</article>
  <section class="routing-grid">
    <div class="route-card">
      <h4>Technical &amp; GDPR Specsheet</h4>
      <p>Examine the 3-Axis Document FSM, Golden Matrix permissions, and OpenAPI 3.1 contract.</p>
      <a href="https://aircounsel-strata-core-production.up.railway.app/specsheet">Read Specsheet &rarr;</a>
    </div>
    <div class="route-card">
      <h4>Practice Workspace (V5.0)</h4>
      <p>Inspect the synthetic Matter Register, Evidence Pipeline V2, and Sharded HMAC Audit Outbox.</p>
      <a href="{workspace_url}">Open Workspace &rarr;</a>
    </div>
    <div class="route-card">
      <h4>6-Gate Route Readiness</h4>
      <p>Structured pre-consultation verification across UK Skilled Worker and Family routes.</p>
      <a href="/intake.html">View Intake Gate &rarr;</a>
    </div>
  </section>
</main>
</body>
</html>"""

def publish_next_from_queue(publish_all=False):
    q_dir = Path("draft_queue")
    q_dir.mkdir(exist_ok=True)
    index_file = Path("published_pillars.json")
    published = json.loads(index_file.read_text(encoding="utf-8")) if index_file.exists() else []

    drafts = sorted(q_dir.glob("*.json"))
    if not drafts:
        print("No queued drafts in draft_queue/.")
        return

    to_process = drafts if publish_all else drafts[:1]
    for d_file in to_process:
        data = json.loads(d_file.read_text(encoding="utf-8"))
        slug = data["slug"]
        date_iso = datetime.utcnow().strftime("%Y-%m-%d")
        html = TEMPLATE.format(
            title=data["title"],
            summary=data["summary"],
            site_url=SITE_URL,
            slug=slug,
            date_iso=date_iso,
            pillar_category=data["pillar_category"],
            audience=data["audience"],
            body_html=data["body_html"],
            workspace_url=WORKSPACE_URL,
        )
        Path(f"{slug}.html").write_text(html, encoding="utf-8")
        published.insert(0, {**data, "date_iso": date_iso})
        d_file.unlink()
        print(f"[PUBLISHED LIVE] -> {SITE_URL}/{slug}.html")

    index_file.write_text(json.dumps(published, indent=2), encoding="utf-8")
    rebuild_insights_and_sitemap(published)

def rebuild_insights_and_sitemap(published):
    cards = ""
    for item in published:
        cards += f"""
        <div style="background:#FFFFFF;border:1px solid #D8D3C8;border-top:3px solid #161E2E;border-radius:10px;padding:22px;margin-bottom:18px">
          <div style="font-family:monospace;color:#C6A86A;font-size:11px">{item['pillar_category']} · {item['date_iso']} · {item['audience']}</div>
          <h2 style="margin:6px 0 8px;font-size:20px"><a href="/{item['slug']}.html" style="color:#161E2E;text-decoration:none">{item['title']}</a></h2>
          <p style="margin:0 0 12px;color:#2C3444;font-size:14.5px">{item['summary']}</p>
          <a href="/{item['slug']}.html" style="color:#161E2E;font-weight:600;font-family:monospace;font-size:12px;text-decoration:none">Read Full Briefing →</a>
        </div>"""
    insights_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>AirCounsel // Institutional Research &amp; Immigration Briefings</title>
    <style>body{{background:#FAF8F5;color:#2C3444;font-family:sans-serif;padding:48px 24px;max-width:880px;margin:0 auto}}</style></head>
    <body><div style="font-family:monospace;color:#C6A86A;font-size:12px">AIRCOUNSEL STRATA™ // RESEARCH HUB</div>
    <h1>Institutional Legal-Tech &amp; UK Immigration Briefings</h1>{cards}</body></html>"""
    Path("insights.html").write_text(insights_html, encoding="utf-8")

    # Rebuild sitemap.xml for automatic Google indexing
    urls = [f"{SITE_URL}/", f"{SITE_URL}/intake.html", f"{SITE_URL}/insights.html"] + [f"{SITE_URL}/{x['slug']}.html" for x in published]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sm += f"  <url><loc>{u}</loc></url>\n"
    sm += "</urlset>"
    Path("sitemap.xml").write_text(sm, encoding="utf-8")

if __name__ == "__main__":
    import sys
    publish_next_from_queue(publish_all=("--all" in sys.argv))
