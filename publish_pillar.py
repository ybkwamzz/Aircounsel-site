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
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "{title}",
  "description": "{summary}",
  "author": {{"@type": "Organization", "name": "AirCounsel STRATA Research"}},
  "publisher": {{"@type": "Organization", "name": "AirCounsel", "url": "{site_url}"}},
  "datePublished": "{date_iso}"
}}
</script>
<style>
  body {{ background:#07070F; color:#F3EFE6; font-family:ui-sans-serif,system-ui,sans-serif; margin:0; padding:48px 24px; line-height:1.75; }}
  .wrap {{ max-width:820px; margin:0 auto; }}
  .kicker {{ font-family:monospace; color:#C6A86A; font-size:12px; letter-spacing:0.14em; text-transform:uppercase; }}
  h1 {{ font-size:32px; line-height:1.25; margin:10px 0 16px; color:#FFFFFF; }}
  .meta {{ font-family:monospace; font-size:12px; color:#9AA3B5; border-bottom:1px solid #1E293B; padding-bottom:18px; margin-bottom:28px; }}
  h2 {{ color:#DFC288; font-size:21px; margin-top:34px; }}
  p, li {{ color:#CBD5E1; font-size:16px; }}
  .cta-box {{ background:#101520; border:1px solid rgba(198,168,106,0.35); border-radius:10px; padding:24px; margin-top:40px; }}
  .btn {{ display:inline-block; background:#C6A86A; color:#07080E; font-weight:700; text-decoration:none; padding:11px 18px; border-radius:6px; font-size:13px; margin-right:10px; margin-top:10px; }}
  .btn-sec {{ display:inline-block; border:1px solid #C6A86A; color:#DFC288; text-decoration:none; padding:11px 18px; border-radius:6px; font-size:13px; margin-top:10px; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="kicker">{pillar_category} // INSTITUTIONAL BRIEFING</div>
  <h1>{title}</h1>
  <div class="meta">PUBLISHED: {date_iso} &nbsp;·&nbsp; AUDIENCE: {audience} &nbsp;·&nbsp; VERIFIED BY AIRCOUNSEL STRATA™</div>
  <article>{body_html}</article>
  <div class="cta-box">
    <div class="kicker">DETERMINISTIC QUALIFICATION &amp; EVIDENCE INFRASTRUCTURE</div>
    <h3 style="margin:6px 0 8px;color:#FFF">Explore the Live STRATA V5.0 System</h3>
    <p style="margin:0 0 12px;font-size:14px">Whether you are a UK legal practice auditing case readiness or an applicant verifying route eligibility across 6 deterministic gates:</p>
    <a class="btn" href="/intake.html">Applicants: Run 6-Gate Eligibility Check →</a>
    <a class="btn-sec" href="{workspace_url}">Solicitors: Open V5.0 Operator Workspace →</a>
    <a class="btn-sec" href="/insights.html">All Research Briefings →</a>
  </div>
</div>
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
        <div style="background:#101520;border:1px solid rgba(198,168,106,0.25);border-radius:10px;padding:22px;margin-bottom:18px">
          <div style="font-family:monospace;color:#C6A86A;font-size:11px">{item['pillar_category']} · {item['date_iso']} · {item['audience']}</div>
          <h2 style="margin:6px 0 8px;font-size:20px"><a href="/{item['slug']}.html" style="color:#FFF;text-decoration:none">{item['title']}</a></h2>
          <p style="margin:0 0 12px;color:#9AA3B5;font-size:14px">{item['summary']}</p>
          <a href="/{item['slug']}.html" style="color:#DFC288;font-family:monospace;font-size:12px;text-decoration:none">Read Full Briefing →</a>
        </div>"""
    insights_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>AirCounsel // Institutional Research &amp; Immigration Briefings</title>
    <style>body{{background:#07070F;color:#F3EFE6;font-family:sans-serif;padding:48px 24px;max-width:880px;margin:0 auto}}</style></head>
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
