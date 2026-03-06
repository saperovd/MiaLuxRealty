#!/usr/bin/env python3
"""
MiaLux Realty — Static Catalog Builder
--------------------------------------
Reads listings.json and generates miami-pre-construction-condos.html

Usage:
    python3 build_catalog.py

Run this every time you add or update a listing in listings.json.
No dependencies beyond Python 3 standard library.
"""

import json
import urllib.parse
from pathlib import Path
from collections import OrderedDict
from datetime import date

# ── LOAD DATA ────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
LISTINGS_FILE = SCRIPT_DIR / "listings.json"
OUTPUT_FILE = SCRIPT_DIR / "miami-pre-construction-condos.html"

with open(LISTINGS_FILE, encoding="utf-8") as f:
    listings = json.load(f)

# ── HELPERS ──────────────────────────────────────────────────────────────────

GRADIENT_COLORS = {
    "cipriani-residences-brickell":       ("#4a7a9b", "#1a3a55"),
    "ora-by-casa-tua":                    ("#7a9a6a", "#2a4a2a"),
    "st-regis-residences-sunny-isles":    ("#9a8a7a", "#3a2a18"),
    "residences-1428-brickell":           ("#5a7a9a", "#1a3050"),
    "mandarin-oriental-residences-miami": ("#8a7060", "#302018"),
    "faena-residences-miami":             ("#7a6a9a", "#2a1a40"),
}
DEFAULT_COLORS = ("#5a7a9a", "#1a3050")


def svg_placeholder(slug, w=600, h=450):
    c1, c2 = GRADIENT_COLORS.get(slug, DEFAULT_COLORS)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">'
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{c1}"/>'
        f'<stop offset="100%" stop-color="{c2}"/>'
        f'</linearGradient></defs>'
        f'<rect width="{w}" height="{h}" fill="url(#g)"/>'
        f'</svg>'
    )
    return f"data:image/svg+xml,{urllib.parse.quote(svg)}"


def fmt_price(n):
    if n >= 1_000_000:
        v = n / 1_000_000
        return f"${v:.1f}M" if n % 1_000_000 else f"${int(v)}M"
    return f"${n // 1000:,}K"


def badge_class(badge):
    return {
        "Hot Deal":    "badge-hot",
        "New Launch":  "badge-new",
        "VIP Pricing": "badge-vip",
        "Coming Soon": "badge-soon",
    }.get(badge, "badge-new")


# ── RENDER ONE LISTING CARD ──────────────────────────────────────────────────

def render_card(p):
    fallback = svg_placeholder(p["id"])
    img_src  = p.get("image_main") or fallback
    delivery = p["estimated_delivery"].split("-")[0]
    progress = p.get("construction_progress", 0)

    units_html = "".join(
        f'<li>'
        f'<span class="ut-type">{u["type"]}</span>'
        f'<span class="ut-size">{u["size_from"]:,}–{u["size_to"]:,} sqft</span>'
        f'<span class="ut-price">{fmt_price(u["price_from"])}</span>'
        f'</li>'
        for u in p.get("unit_types", [])[:3]
    )

    views_text     = " · ".join(p.get("views", [])[:3])
    amenities_text = ", ".join(p.get("amenities", [])[:5])
    brand_part     = f' · <strong>{p["brand_partner"]}</strong>' if p.get("brand_partner") else ""

    return f'''
<article class="listing-card" id="{p['id']}" itemscope itemtype="https://schema.org/Accommodation">
  <div class="lc-img">
    <img src="{img_src}"
         onerror="this.src='{fallback}'"
         alt="{p['name']} – Pre-Construction Luxury Condos {p['neighborhood']} Miami"
         width="600" height="450" loading="lazy">
    <div class="lc-badge {badge_class(p['badge'])}">{p['badge']}</div>
    <div class="lc-status">{p['status']}</div>
    <div class="lc-progress-bar">
      <div class="lc-progress-fill" style="width:{progress}%"></div>
    </div>
  </div>
  <div class="lc-body">
    <div class="lc-neighborhood" itemprop="address">{p['neighborhood']}, Miami</div>
    <h2 class="lc-name" itemprop="name">{p['name']}</h2>
    <p class="lc-tagline">{p['tagline']}</p>
    <p class="lc-dev">By <strong>{p['developer']}</strong>{brand_part} · Arch: {p['architect']}</p>
    <p class="lc-desc">{p['description_short']}</p>
    <div class="lc-specs">
      <div class="lc-spec"><span class="spec-n">{p['floors']}</span><span class="spec-l">Floors</span></div>
      <div class="lc-spec"><span class="spec-n">{p['total_units']}</span><span class="spec-l">Units</span></div>
      <div class="lc-spec"><span class="spec-n">{delivery}</span><span class="spec-l">Delivery</span></div>
      <div class="lc-spec"><span class="spec-n">{progress}%</span><span class="spec-l">Built</span></div>
    </div>
    <div class="lc-units">
      <div class="lc-units-label">Floor Plans &amp; Pricing</div>
      <ul class="ut-list">{units_html}</ul>
    </div>
    <div class="lc-amenities">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="9 11 12 14 22 4"/>
        <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
      </svg>
      {amenities_text}
    </div>
    <div class="lc-views">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
        <circle cx="12" cy="12" r="3"/>
      </svg>
      {views_text}
    </div>
    <div class="lc-footer">
      <div class="lc-price">
        <div class="lc-price-label">Starting from</div>
        <div class="lc-price-value" itemprop="price">{fmt_price(p['price_from'])}</div>
      </div>
      <a href="#contact" class="lc-cta">Get VIP Pricing →</a>
    </div>
  </div>
</article>'''


# ── GROUP BY NEIGHBORHOOD ─────────────────────────────────────────────────────

neighborhoods: OrderedDict = OrderedDict()
for p in listings:
    nb = p["neighborhood"]
    neighborhoods.setdefault(nb, []).append(p)


# ── RENDER NEIGHBORHOOD SECTIONS ─────────────────────────────────────────────

def render_sections():
    html = ""
    for nb, projects in neighborhoods.items():
        anchor = nb.lower().replace(" ", "-")
        count  = len(projects)
        cards  = "\n".join(render_card(p) for p in projects)
        plural = "s" if count > 1 else ""
        html += f'''
<section class="nb-section" id="neighborhood-{anchor}">
  <div class="nb-section-header">
    <div>
      <div class="sec-label">{count} Project{plural} Available</div>
      <h2>Pre-Construction Condos in <em>{nb}</em></h2>
    </div>
  </div>
  <div class="listings-grid">
    {cards}
  </div>
</section>'''
    return html


# ── NEIGHBORHOOD NAV PILLS ────────────────────────────────────────────────────

def render_nb_nav():
    return "".join(
        f'<a href="#neighborhood-{nb.lower().replace(" ","-")}" class="nb-pill">'
        f'{nb} <span>({len(ps)})</span></a>'
        for nb, ps in neighborhoods.items()
    )


# ── SCHEMA.ORG JSON-LD ────────────────────────────────────────────────────────

def render_schema():
    items = [
        {
            "@type": "Accommodation",
            "name": p["name"],
            "description": p["description_short"],
            "address": {
                "@type": "PostalAddress",
                "streetAddress": p["address"],
                "addressLocality": "Miami",
                "addressRegion": "FL",
                "addressCountry": "US",
            },
            "offers": {
                "@type": "Offer",
                "priceCurrency": "USD",
                "price": p["price_from"],
                "availability": "https://schema.org/InStock",
            },
        }
        for p in listings
    ]
    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Miami Pre-Construction Luxury Condos",
        "description": "Complete catalog of luxury pre-construction condos in Miami",
        "numberOfItems": len(listings),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": s}
            for i, s in enumerate(items)
        ],
    }
    return json.dumps(schema, indent=2)


# ── FULL HTML PAGE ────────────────────────────────────────────────────────────

year  = date.today().year
total = len(listings)

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Miami Pre-Construction Luxury Condos {year} | New Developments | MiaLux Realty</title>
<meta name="description" content="Browse {total} luxury pre-construction developments in Miami. Cipriani, St. Regis, Mandarin Oriental, ORA by Casa Tua &amp; more. VIP pricing, zero buyer commission. Expert guidance for international buyers.">
<meta name="keywords" content="Miami pre-construction condos, Miami new developments {year}, Brickell pre-construction, Miami luxury condos, new condos Miami Beach, Sunny Isles pre-construction">
<link rel="canonical" href="https://mialuxrealty.com/miami-pre-construction-condos">
<meta property="og:title" content="Miami Pre-Construction Luxury Condos {year} | MiaLux Realty">
<meta property="og:description" content="VIP access to Miami's finest new developments. Zero buyer commission. Expert guidance for international investors.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://mialuxrealty.com/miami-pre-construction-condos">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<script type="application/ld+json">
{render_schema()}
</script>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --gold:#b8935a;--gold-light:#d4b483;--gold-pale:#f5ede0;
  --dark-nav:#1e1e1e;--dark-footer:#252525;
  --charcoal:#3a3a3a;--mid:#6b6b6b;--light:#9a9a9a;
  --border:#e2e2e2;--border-soft:#ececec;
  --bg:#ffffff;--bg2:#f7f7f5;--bg3:#f0efec;
  --serif:'Playfair Display',Georgia,serif;
  --sans:'Inter',system-ui,sans-serif;
  --r:8px;--rm:14px;--rl:20px;--rxl:28px;
}}
html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--charcoal);font-family:var(--sans);font-weight:300;line-height:1.6;overflow-x:hidden;-webkit-font-smoothing:antialiased}}
nav{{position:sticky;top:0;z-index:100;background:var(--dark-nav);padding:0 2.5rem;height:64px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 2px 20px rgba(0,0,0,.18)}}
.logo{{font-family:var(--serif);font-size:1.3rem;color:#fff;text-decoration:none}}
.logo span{{color:var(--gold-light)}}
.nav-links{{display:flex;gap:2rem;list-style:none}}
.nav-links a{{font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.65);text-decoration:none;transition:color .2s}}
.nav-links a:hover,.nav-links a.active{{color:var(--gold-light)}}
.nav-btn{{font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;padding:.55rem 1.3rem;background:var(--gold);color:#fff;border-radius:var(--r);text-decoration:none;font-weight:500;transition:background .2s}}
.nav-btn:hover{{background:var(--gold-light)}}
.hamburger{{display:none;flex-direction:column;gap:5px;cursor:pointer;background:none;border:none;padding:4px}}
.hamburger span{{display:block;width:22px;height:1.5px;background:rgba(255,255,255,.8)}}
.mob-menu{{display:none;position:fixed;inset:0;background:var(--dark-nav);z-index:99;flex-direction:column;align-items:center;justify-content:center;gap:2rem}}
.mob-menu.open{{display:flex}}
.mob-menu a{{font-family:var(--serif);font-size:1.8rem;color:#fff;text-decoration:none}}
.mob-close{{position:absolute;top:1.2rem;right:1.8rem;background:none;border:none;color:rgba(255,255,255,.7);font-size:1.8rem;cursor:pointer}}
.page-header{{background:var(--dark-nav);padding:3.5rem 6vw 4rem;position:relative;overflow:hidden}}
.page-header::before{{content:'';position:absolute;top:-80px;right:-80px;width:500px;height:500px;background:radial-gradient(circle,rgba(184,147,90,.1) 0%,transparent 65%);pointer-events:none}}
.ph-label{{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.8rem;display:flex;align-items:center;gap:.6rem}}
.ph-label::before{{content:'';display:block;width:24px;height:1.5px;background:var(--gold)}}
.page-header h1{{font-family:var(--serif);font-size:clamp(1.9rem,4vw,3.2rem);font-weight:400;color:#fff;line-height:1.15;margin-bottom:.9rem}}
.page-header h1 em{{font-style:italic;color:var(--gold-light)}}
.page-header p{{font-size:.9rem;color:rgba(255,255,255,.5);max-width:600px;line-height:1.7}}
.ph-stats{{display:flex;gap:3rem;margin-top:2.2rem;flex-wrap:wrap}}
.ph-stat-n{{font-family:var(--serif);font-size:1.7rem;color:#fff}}
.ph-stat-l{{font-size:.65rem;letter-spacing:.13em;text-transform:uppercase;color:rgba(255,255,255,.38);margin-top:.15rem}}
.breadcrumb{{padding:.85rem 6vw;background:var(--bg3);border-bottom:1px solid var(--border-soft);font-size:.75rem;color:var(--light)}}
.breadcrumb a{{color:var(--mid);text-decoration:none}}
.breadcrumb a:hover{{color:var(--gold)}}
.breadcrumb span{{margin:0 .5rem}}
.nb-nav{{position:sticky;top:64px;z-index:50;background:var(--bg);border-bottom:1px solid var(--border-soft);padding:.85rem 6vw;overflow-x:auto;white-space:nowrap;box-shadow:0 2px 10px rgba(0,0,0,.04)}}
.nb-nav::-webkit-scrollbar{{height:3px}}
.nb-nav::-webkit-scrollbar-thumb{{background:var(--border)}}
.nb-pill{{display:inline-flex;align-items:center;gap:.4rem;padding:.4rem 1.1rem;font-size:.73rem;letter-spacing:.06em;border:1.5px solid var(--border);border-radius:50px;color:var(--mid);text-decoration:none;margin-right:.5rem;transition:all .2s}}
.nb-pill:hover{{border-color:var(--gold);color:var(--gold)}}
.nb-pill span{{color:var(--light);font-size:.67rem}}
.seo-intro{{padding:3rem 6vw 2rem;max-width:900px}}
.seo-intro h2{{font-family:var(--serif);font-size:1.5rem;font-weight:400;margin-bottom:.8rem}}
.seo-intro h2 em{{font-style:italic;color:var(--gold)}}
.seo-intro p{{font-size:.88rem;color:var(--mid);line-height:1.8;margin-bottom:.7rem}}
.nb-section{{padding:3rem 6vw 4rem;border-top:2px solid var(--border-soft)}}
.nb-section:first-of-type{{border-top:none}}
.sec-label{{font-size:.67rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.6rem;display:flex;align-items:center;gap:.5rem}}
.sec-label::before{{content:'';display:block;width:20px;height:1.5px;background:var(--gold)}}
.nb-section-header{{margin-bottom:2rem}}
.nb-section-header h2{{font-family:var(--serif);font-size:clamp(1.6rem,2.8vw,2.2rem);font-weight:400;line-height:1.2;color:var(--charcoal)}}
.nb-section-header h2 em{{font-style:italic;color:var(--gold)}}
.listings-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem}}
.listing-card{{background:var(--bg);border:1px solid var(--border-soft);border-radius:var(--rl);overflow:hidden;display:flex;flex-direction:column;box-shadow:0 2px 16px rgba(0,0,0,.05);transition:box-shadow .3s,transform .3s,border-color .3s}}
.listing-card:hover{{box-shadow:0 12px 40px rgba(0,0,0,.1);transform:translateY(-5px);border-color:var(--gold-light)}}
.lc-img{{position:relative;aspect-ratio:4/3;overflow:hidden}}
.lc-img img{{width:100%;height:100%;object-fit:cover;transition:transform .6s;display:block}}
.listing-card:hover .lc-img img{{transform:scale(1.05)}}
.lc-badge{{position:absolute;top:.9rem;left:.9rem;padding:.28rem .75rem;font-size:.62rem;letter-spacing:.12em;text-transform:uppercase;font-weight:500;border-radius:var(--r)}}
.badge-hot{{background:var(--gold);color:#fff}}
.badge-new{{background:rgba(255,255,255,.92);color:var(--gold);border:1px solid var(--gold-light)}}
.badge-vip{{background:#1e1e1e;color:var(--gold-light)}}
.badge-soon{{background:rgba(255,255,255,.92);color:var(--charcoal)}}
.lc-status{{position:absolute;top:.9rem;right:.9rem;font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;background:rgba(255,255,255,.9);padding:.2rem .6rem;border-radius:4px;color:var(--mid)}}
.lc-progress-bar{{position:absolute;bottom:0;left:0;right:0;height:3px;background:rgba(255,255,255,.2)}}
.lc-progress-fill{{height:100%;background:linear-gradient(to right,var(--gold),var(--gold-light))}}
.lc-body{{padding:1.4rem;flex:1;display:flex;flex-direction:column;gap:.5rem}}
.lc-neighborhood{{font-size:.65rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:500}}
.lc-name{{font-family:var(--serif);font-size:1.22rem;font-weight:400;line-height:1.25;color:var(--charcoal);transition:color .2s}}
.listing-card:hover .lc-name{{color:var(--gold)}}
.lc-tagline{{font-size:.78rem;color:var(--light);font-style:italic}}
.lc-dev{{font-size:.72rem;color:var(--mid)}}
.lc-desc{{font-size:.8rem;color:var(--mid);line-height:1.65;margin:.2rem 0}}
.lc-specs{{display:flex;background:var(--bg2);border-radius:var(--r);overflow:hidden;margin:.3rem 0}}
.lc-spec{{flex:1;text-align:center;padding:.6rem .4rem;border-right:1px solid var(--border-soft)}}
.lc-spec:last-child{{border-right:none}}
.spec-n{{display:block;font-family:var(--serif);font-size:1rem;color:var(--charcoal)}}
.spec-l{{display:block;font-size:.57rem;letter-spacing:.1em;text-transform:uppercase;color:var(--light);margin-top:.12rem}}
.lc-units{{background:var(--bg2);border-radius:var(--r);padding:.8rem 1rem;margin:.2rem 0}}
.lc-units-label{{font-size:.6rem;letter-spacing:.13em;text-transform:uppercase;color:var(--light);margin-bottom:.5rem}}
.ut-list{{list-style:none;display:flex;flex-direction:column;gap:.3rem}}
.ut-list li{{display:flex;justify-content:space-between;align-items:center;font-size:.75rem;padding:.25rem 0;border-bottom:1px solid var(--border-soft)}}
.ut-list li:last-child{{border-bottom:none}}
.ut-type{{color:var(--charcoal)}}
.ut-size{{color:var(--light);font-size:.7rem}}
.ut-price{{font-family:var(--serif);color:var(--gold);font-size:.88rem}}
.lc-amenities,.lc-views{{font-size:.72rem;color:var(--mid);display:flex;align-items:flex-start;gap:.4rem;line-height:1.5}}
.lc-amenities svg,.lc-views svg{{flex-shrink:0;margin-top:2px;color:var(--gold)}}
.lc-footer{{margin-top:auto;padding-top:.9rem;border-top:1px solid var(--border-soft);display:flex;align-items:center;justify-content:space-between}}
.lc-price-label{{font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:var(--light)}}
.lc-price-value{{font-family:var(--serif);font-size:1.2rem;color:var(--gold);line-height:1.1}}
.lc-cta{{font-size:.7rem;letter-spacing:.07em;text-transform:uppercase;font-weight:500;color:var(--gold);text-decoration:none;padding:.5rem .9rem;border:1.5px solid var(--gold-light);border-radius:var(--r);transition:all .2s;white-space:nowrap}}
.lc-cta:hover{{background:var(--gold);color:#fff;border-color:var(--gold)}}
.seo-bottom{{padding:3rem 6vw 4rem;background:var(--bg2);border-top:1px solid var(--border-soft)}}
.seo-bottom-inner{{max-width:900px}}
.seo-bottom h2{{font-family:var(--serif);font-size:1.5rem;font-weight:400;margin-bottom:1rem}}
.seo-bottom h2 em{{font-style:italic;color:var(--gold)}}
.seo-bottom h3{{font-family:var(--serif);font-size:1.1rem;font-weight:400;color:var(--charcoal);margin:1.5rem 0 .5rem}}
.seo-bottom p{{font-size:.86rem;color:var(--mid);line-height:1.8;margin-bottom:.6rem}}
.cta-banner{{background:var(--dark-nav);padding:4rem 6vw;text-align:center;position:relative;overflow:hidden}}
.cta-banner::before{{content:'';position:absolute;top:-100px;left:50%;transform:translateX(-50%);width:600px;height:400px;background:radial-gradient(circle,rgba(184,147,90,.12) 0%,transparent 65%);pointer-events:none}}
.cta-banner h2{{font-family:var(--serif);font-size:clamp(1.6rem,3vw,2.5rem);color:#fff;margin-bottom:.8rem}}
.cta-banner h2 em{{font-style:italic;color:var(--gold-light)}}
.cta-banner p{{color:rgba(255,255,255,.5);font-size:.88rem;margin-bottom:2rem;max-width:500px;margin-left:auto;margin-right:auto}}
.cta-actions{{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap}}
.btn{{display:inline-flex;align-items:center;gap:.5rem;padding:.85rem 1.8rem;font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;text-decoration:none;font-weight:500;border-radius:var(--r);border:none;cursor:pointer;transition:all .2s}}
.btn-gold{{background:var(--gold);color:#fff;box-shadow:0 4px 16px rgba(184,147,90,.35)}}
.btn-gold:hover{{background:var(--gold-light);transform:translateY(-2px)}}
.btn-outline-light{{background:none;border:1.5px solid rgba(255,255,255,.3);color:rgba(255,255,255,.8)}}
.btn-outline-light:hover{{border-color:var(--gold-light);color:var(--gold-light)}}
.contact-section{{padding:4rem 6vw;background:var(--bg)}}
.contact-inner{{max-width:680px;margin:0 auto;text-align:center}}
.sec-label-center{{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.8rem;display:flex;align-items:center;justify-content:center;gap:.6rem}}
.sec-label-center::before,.sec-label-center::after{{content:'';display:block;width:24px;height:1.5px;background:var(--gold)}}
.contact-inner h2{{font-family:var(--serif);font-size:clamp(1.6rem,3vw,2.2rem);font-weight:400;margin-bottom:.7rem}}
.contact-inner h2 em{{font-style:italic;color:var(--gold)}}
.contact-inner>p{{color:var(--mid);margin-bottom:2rem;font-size:.88rem}}
.form-card{{background:var(--bg2);border:1px solid var(--border);border-radius:var(--rxl);padding:2.5rem;box-shadow:0 4px 32px rgba(0,0,0,.06);text-align:left}}
.form-grid{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}
.fg{{display:flex;flex-direction:column;gap:.35rem}}
.fg.full{{grid-column:1/-1}}
.fg label{{font-size:.68rem;letter-spacing:.09em;text-transform:uppercase;color:var(--mid);font-weight:500}}
.fg input,.fg select,.fg textarea{{background:var(--bg);border:1.5px solid var(--border);border-radius:var(--r);padding:.75rem 1rem;color:var(--charcoal);font-family:var(--sans);font-size:.9rem;font-weight:300;outline:none;transition:border-color .2s,box-shadow .2s;-webkit-appearance:none;appearance:none}}
.fg input:focus,.fg select:focus,.fg textarea:focus{{border-color:var(--gold);box-shadow:0 0 0 3px rgba(184,147,90,.1)}}
.fg textarea{{resize:vertical;min-height:80px}}
.form-submit{{grid-column:1/-1;margin-top:.3rem}}
.form-submit .btn{{width:100%;justify-content:center;padding:1rem}}
.form-note{{font-size:.68rem;color:var(--light);text-align:center;margin-top:.6rem}}
.form-success{{display:none;text-align:center;padding:2rem}}
.form-success h3{{font-family:var(--serif);font-size:1.5rem;color:var(--gold);margin-bottom:.5rem}}
footer{{background:var(--dark-footer);padding:4rem 6vw 2rem;border-radius:var(--rxl) var(--rxl) 0 0}}
.footer-grid{{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:3rem;margin-bottom:3rem}}
.f-logo{{font-family:var(--serif);font-size:1.2rem;color:#fff;text-decoration:none}}
.f-logo span{{color:var(--gold-light)}}
.f-desc{{font-size:.8rem;color:rgba(255,255,255,.4);line-height:1.72;margin-top:.9rem;max-width:270px}}
.f-head{{font-size:.65rem;letter-spacing:.15em;text-transform:uppercase;color:var(--gold-light);margin-bottom:1rem}}
.f-links{{display:flex;flex-direction:column;gap:.55rem}}
.f-links a{{font-size:.8rem;color:rgba(255,255,255,.4);text-decoration:none;transition:color .2s}}
.f-links a:hover{{color:rgba(255,255,255,.8)}}
.f-bottom{{border-top:1px solid rgba(255,255,255,.08);padding-top:1.4rem;display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}}
.f-bottom p,.f-legal a{{font-size:.7rem;color:rgba(255,255,255,.28);text-decoration:none}}
.f-legal{{display:flex;gap:1.5rem}}
.float{{position:fixed;bottom:1.5rem;right:1.5rem;z-index:50;display:flex;flex-direction:column;gap:.55rem;align-items:flex-end}}
.float-btn{{display:flex;align-items:center;gap:.6rem;padding:.72rem 1.15rem;font-size:.76rem;text-decoration:none;font-weight:500;border-radius:50px;box-shadow:0 4px 20px rgba(0,0,0,.2);transition:transform .2s;letter-spacing:.07em}}
.float-btn:hover{{transform:translateY(-2px)}}
.float-wa{{background:#25D366;color:#fff}}
.float-call{{background:var(--gold);color:#fff}}
@media(max-width:1100px){{.listings-grid{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:900px){{
  .nav-links,.nav-btn{{display:none}}
  .hamburger{{display:flex}}
  .footer-grid{{grid-template-columns:1fr 1fr}}
}}
@media(max-width:650px){{
  .listings-grid{{grid-template-columns:1fr}}
  .form-grid{{grid-template-columns:1fr}}
  .footer-grid{{grid-template-columns:1fr}}
  .float-btn span{{display:none}}
  .float-btn{{padding:.85rem;border-radius:50%;width:48px;height:48px;justify-content:center}}
}}
</style>
</head>
<body>

<nav>
  <a class="logo" href="index.html">MiaLux<span>Realty</span></a>
  <ul class="nav-links">
    <li><a href="miami-pre-construction-condos.html" class="active">Developments</a></li>
    <li><a href="index.html#neighborhoods">Neighborhoods</a></li>
    <li><a href="index.html#process">Process</a></li>
    <li><a href="index.html#faq">FAQ</a></li>
    <li><a href="index.html#news">News</a></li>
  </ul>
  <a href="#contact" class="nav-btn">Get VIP Access</a>
  <button class="hamburger" id="ham" aria-label="Menu"><span></span><span></span><span></span></button>
</nav>
<div class="mob-menu" id="mobMenu">
  <button class="mob-close" id="mobClose">&#10005;</button>
  <a href="miami-pre-construction-condos.html">Developments</a>
  <a href="index.html#neighborhoods">Neighborhoods</a>
  <a href="index.html#process">Process</a>
  <a href="index.html#faq">FAQ</a>
  <a href="#contact" style="color:var(--gold-light)">Get VIP Access &#8594;</a>
</div>

<div class="page-header">
  <div class="ph-label">Complete Catalog &middot; {total} Projects</div>
  <h1>Miami Pre-Construction <em>Luxury Condos</em> {year}</h1>
  <p>Handpicked new developments across Miami's most desirable neighborhoods. VIP developer access, best pricing guaranteed, zero buyer commission for international and domestic buyers.</p>
  <div class="ph-stats">
    <div><div class="ph-stat-n">{total}+</div><div class="ph-stat-l">Active Projects</div></div>
    <div><div class="ph-stat-n">0%</div><div class="ph-stat-l">Buyer Commission</div></div>
    <div><div class="ph-stat-n">$500K</div><div class="ph-stat-l">Starting Price</div></div>
    <div><div class="ph-stat-n">2025–2029</div><div class="ph-stat-l">Delivery Range</div></div>
  </div>
</div>

<nav class="breadcrumb" aria-label="Breadcrumb">
  <a href="index.html">Home</a>
  <span>&#8250;</span>
  <span>Miami Pre-Construction Luxury Condos</span>
</nav>

<div class="nb-nav" aria-label="Jump to neighborhood">
  {render_nb_nav()}
</div>

<div class="seo-intro">
  <h2>New <em>Pre-Construction</em> Developments in Miami</h2>
  <p>Miami's luxury pre-construction market offers international buyers and investors a rare opportunity: the ability to secure a residence in one of the world's most dynamic cities at today's prices, with delivery in 2025–2029. From the financial towers of Brickell to the oceanfront estates of Sunny Isles Beach, MiaLux Realty provides exclusive VIP access to Miami's most sought-after new developments.</p>
  <p>As a licensed Florida real estate broker, we represent buyers at <strong>zero commission</strong> — our service is paid by developers, meaning you receive expert guidance, floor plan priority, and pre-launch pricing at no cost to you.</p>
</div>

{render_sections()}

<div class="seo-bottom">
  <div class="seo-bottom-inner">
    <h2>Why Buy <em>Pre-Construction</em> in Miami?</h2>
    <p>Pre-construction condos in Miami offer buyers a compelling combination of price appreciation, flexible payment structures, and access to brand-new residences with cutting-edge amenities. By purchasing before completion, buyers typically lock in prices that are 15–25% below what comparable completed units sell for in the same building.</p>
    <h3>Understanding the Miami Pre-Construction Market</h3>
    <p>Miami's luxury new developments are driven by record demand from Latin American, European, and North American buyers seeking both lifestyle and investment returns. Neighborhoods like Brickell, Edgewater, and Sunny Isles Beach have seen consistent price appreciation of 10–20% annually over the past five years.</p>
    <h3>How Pre-Construction Payment Schedules Work</h3>
    <p>Most Miami pre-construction developments require a deposit of 20–30% spread across construction milestones — typically 20% at contract, followed by additional installments at 6, 12, or 18 months, with the balance (60–70%) due at closing. This structure allows international buyers to invest gradually over a 2–4 year period.</p>
    <h3>Can Foreigners Buy Pre-Construction in Miami?</h3>
    <p>Yes. There are no restrictions on foreign nationals purchasing real estate in the United States. Miami is one of the most popular destinations for international real estate investment, particularly from buyers in Brazil, Argentina, Colombia, Venezuela, Mexico, Europe, and Canada. Foreign national mortgage programs are also available for qualified buyers.</p>
    <h3>MiaLux Realty — Your Miami Pre-Construction Specialist</h3>
    <p>MiaLux Realty is a licensed Florida real estate brokerage specializing exclusively in luxury pre-construction developments in Miami. Our team provides complete buyer representation including project selection, contract review, payment schedule management, and closing support — at absolutely zero cost to buyers.</p>
  </div>
</div>

<div class="cta-banner">
  <h2>Ready to Find Your <em>Perfect Investment?</em></h2>
  <p>Tell us your budget and goals. We'll send you a personalized selection of projects with full pricing and floor plans within 2 hours.</p>
  <div class="cta-actions">
    <a href="#contact" class="btn btn-gold">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
      Get Free Consultation
    </a>
    <a href="https://wa.me/13050000000" class="btn btn-outline-light" target="_blank" rel="noopener">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
      WhatsApp Us Now
    </a>
  </div>
</div>

<section class="contact-section" id="contact">
  <div class="contact-inner">
    <div class="sec-label-center">Free Consultation</div>
    <h2>Get <em>VIP Access</em> to Miami's Best Projects</h2>
    <p>Tell us what you're looking for. A specialist will respond within 2 hours with curated recommendations and full pricing.</p>
    <div class="form-card">
      <div id="leadForm">
        <div class="form-grid">
          <div class="fg"><label>First Name</label><input type="text" placeholder="John" autocomplete="given-name"></div>
          <div class="fg"><label>Last Name</label><input type="text" placeholder="Smith" autocomplete="family-name"></div>
          <div class="fg"><label>Email Address</label><input type="email" id="email" placeholder="john@email.com" autocomplete="email"></div>
          <div class="fg"><label>Phone / WhatsApp</label><input type="tel" placeholder="+1 305 000 0000" autocomplete="tel"></div>
          <div class="fg"><label>Budget Range</label>
            <select><option value="" disabled selected>Select budget</option><option>$500K &#8211; $1M</option><option>$1M &#8211; $2M</option><option>$2M &#8211; $5M</option><option>$5M &#8211; $10M</option><option>$10M+</option></select>
          </div>
          <div class="fg"><label>I'm Looking To</label>
            <select><option value="" disabled selected>Select goal</option><option>Buy to live in</option><option>Buy to rent / invest</option><option>Buy for resale</option><option>Still exploring</option></select>
          </div>
          <div class="fg full"><label>Preferred Neighborhood or Project</label><input type="text" placeholder="e.g. Brickell, or Cipriani Residences&#8230;"></div>
          <div class="fg full"><label>Anything else?</label><textarea placeholder="Timeline, bedroom count, specific requirements&#8230;"></textarea></div>
          <div class="form-submit">
            <button type="button" class="btn btn-gold" onclick="submitForm()">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
              Send My Request &#8212; It&#8217;s Free
            </button>
            <div class="form-note">&#128274; Private &amp; confidential. We never share your data.</div>
          </div>
        </div>
      </div>
      <div class="form-success" id="formSuccess">
        <h3>&#10003; Thank You!</h3>
        <p>A Miami luxury specialist will contact you within 2 hours with personalized recommendations.</p>
      </div>
    </div>
  </div>
</section>

<footer>
  <div class="footer-grid">
    <div>
      <a href="index.html" class="f-logo">MiaLux<span>Realty</span></a>
      <p class="f-desc">Miami's premier pre-construction specialists. VIP access to luxury new developments. Zero buyer commission. Expert guidance for international investors.</p>
    </div>
    <div>
      <div class="f-head">Neighborhoods</div>
      <div class="f-links">
        <a href="#neighborhood-brickell">Brickell</a>
        <a href="#neighborhood-miami-beach">Miami Beach</a>
        <a href="#neighborhood-edgewater">Edgewater</a>
        <a href="#neighborhood-sunny-isles-beach">Sunny Isles Beach</a>
        <a href="#neighborhood-downtown-miami">Downtown Miami</a>
      </div>
    </div>
    <div>
      <div class="f-head">Resources</div>
      <div class="f-links">
        <a href="index.html#process">Buying Process</a>
        <a href="index.html#faq">FAQ</a>
        <a href="index.html#news">Market Reports</a>
        <a href="#contact">Free Consultation</a>
      </div>
    </div>
    <div>
      <div class="f-head">Contact</div>
      <div class="f-links">
        <a href="tel:+13050000000">+1 (305) 000-0000</a>
        <a href="mailto:hello@mialuxrealty.com">hello@mialuxrealty.com</a>
        <a href="https://wa.me/13050000000">WhatsApp Chat</a>
      </div>
    </div>
  </div>
  <div class="f-bottom">
    <p>&#169; {year} MiaLuxRealty.com &middot; All rights reserved &middot; Licensed Real Estate Broker, Florida</p>
    <div class="f-legal"><a href="#">Privacy Policy</a><a href="#">Terms of Use</a><a href="#">Sitemap</a></div>
  </div>
</footer>

<div class="float">
  <a href="https://wa.me/13050000000" class="float-btn float-wa" target="_blank" rel="noopener">
    <svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
    <span>WhatsApp</span>
  </a>
  <a href="tel:+13050000000" class="float-btn float-call">
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.68A2 2 0 012 .18h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>
    <span>Call Now</span>
  </a>
</div>

<script>
document.getElementById('ham').onclick = () => document.getElementById('mobMenu').classList.add('open');
document.getElementById('mobClose').onclick = () => document.getElementById('mobMenu').classList.remove('open');
document.querySelectorAll('.mob-menu a').forEach(a => a.onclick = () => document.getElementById('mobMenu').classList.remove('open'));
function submitForm() {{
  const email = document.getElementById('email').value;
  if (!email) {{ alert('Please enter your email address.'); return; }}
  document.getElementById('leadForm').style.display = 'none';
  document.getElementById('formSuccess').style.display = 'block';
}}
</script>
</body>
</html>'''

# ── WRITE OUTPUT ─────────────────────────────────────────────────────────────

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(HTML)

size_kb = OUTPUT_FILE.stat().st_size // 1024
print(f"✓ Built: {OUTPUT_FILE.name}  ({size_kb} KB)")
print(f"  {total} listings across {len(neighborhoods)} neighborhoods")
print(f"  Neighborhoods: {', '.join(neighborhoods.keys())}")
