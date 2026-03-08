#!/usr/bin/env python3
"""
MiaLux Realty â Master Build Script v3
URL Structure:
  /new-developments/                               â Category hub (EN)
  /new-developments/brickell/                      â Neighborhood (EN)
  /new-developments/brickell/cipriani-residences/  â Listing (EN)
  /es/new-developments/brickell/cipriani-residences/ â Listing (ES)

Future categories:
  /villas/brickell/casa-bella/
  /penthouses/brickell/cipriani-penthouse/
  /es/villas/brickell/

Root stays CLEAN â only index.html + config files.
"""

import json, os, re
from datetime import date
from pathlib import Path
from collections import defaultdict

BASE_URL   = "https://mialuxrealty.com"
AGENT_ID   = f"{BASE_URL}/#agent"
WEBSITE_ID = f"{BASE_URL}/#website"
SITE_NAME  = "MiaLux Realty"
PHONE      = "+1-305-000-0000"
LOGO_URL   = f"{BASE_URL}/images/logo.png"

#──Load listings ââââââââââââââââââââââââââââââââââââââââââââââ
with open('listings.json') as f:
    LISTINGS = json.load(f)

HOOD_SLUG_MAP = {
    'Brickell':'brickell','Brickell Key':'brickell-key',
    'Miami Beach':'miami-beach','South Beach':'miami-beach',
    'Sunny Isles Beach':'sunny-isles-beach','Edgewater':'edgewater',
    'Wynwood':'wynwood','Downtown Miami':'downtown-miami',
    'Coconut Grove':'coconut-grove','Coral Gables':'coral-gables',
    'Design District':'design-district','Aventura':'aventura',
    'Bal Harbour':'bal-harbour','Fisher Island':'fisher-island',
}
for l in LISTINGS:
    hood = l.get('neighborhood','')
    l['_hood_slug']       = l.get('_hood_slug') or HOOD_SLUG_MAP.get(hood, hood.lower().replace(' ','-'))
    l['category']         = l.get('category','new-developments')
    l['page_slug']        = l.get('page_slug') or l.get('slug') or l.get('id')
    l['_canonical_path']  = f"{l['category']}/{l['_hood_slug']}/{l['page_slug']}"

by_cat_hood = defaultdict(lambda: defaultdict(list))
for l in LISTINGS:
    by_cat_hood[l['category']][l['_hood_slug']].append(l)

ALL_CATEGORIES = list(by_cat_hood.keys())

#──Neighborhood metadata ââââââââââââââââââââââââââââââââââââââ
HOOD_META = {
    'brickell': {
        'name':'Brickell','tagline':"Miami's Financial Capital & Luxury Living Hub",
        'geo':{'lat':25.7617,'lng':-80.1918},
        'highlights':['Bay & City Views','Walk Score 95+','World-Class Dining','Top Investment Returns'],
        'descriptions':{
            'en':"Brickell is Miami's undisputed financial capital — a gleaming vertical neighborhood of luxury towers, world-class restaurants, and bayfront parks. Known as the \"Manhattan of the South,\" it attracts global investors and urban professionals seeking walkable luxury living steps from the bay.",
            'es':"Brickell es la indiscutible capital financiera de Miami — un resplandeciente barrio vertical de torres de lujo, restaurantes de clase mundial y parques frente a la bahía.",
            'pt':"Brickell é a capital financeira indiscutível de Miami — um bairro vertical repleto de torres de luxo, restaurantes de classe mundial e parques à beira da baía.",
            'ru':"Брикелл — бесспорная финансовая столица Майами — сияющий вертикальный район роскошных башен, ресторанов мирового класса и парков на берегу залива.",
        },
    },
    'sunny-isles-beach': {
        'name':'Sunny Isles Beach','tagline':"The Riviera of the Americas — Oceanfront Ultra-Luxury",
        'geo':{'lat':25.9386,'lng':-80.1222},
        'highlights':['Direct Ocean Access','Ultra-Luxury Brand Towers','Private Beach','International Community'],
        'descriptions':{
            'en':"Sunny Isles Beach — nicknamed the \"Riviera of the Americas\" — is a pristine barrier island between the Atlantic Ocean and the Intracoastal Waterway. Home to iconic ultra-luxury towers by Porsche, Armani and Bentley.",
            'es':"Sunny Isles Beach — apodada la \"Riviera de las Américas\" — es una prístina isla barrera entre el Océano Atlántico y la Vía Intracostera.",
            'pt':"Sunny Isles Beach — apelidada de \"Riviera das Américas\" — é uma ilha barreira pristina entre o Oceano Atlântico e a Hidrovia Intracoastal.",
            'ru':"Санни-Айлс-Бич — прозванный «Ривьерой Америки» — нетронутый барьерный остров между Атлантическим океаном и Внутрибереговым водным путём.",
        },
    },
    'miami-beach': {
        'name':'Miami Beach','tagline':"The World's Most Iconic Beach Address",
        'geo':{'lat':25.7907,'lng':-80.1300},
        'highlights':['Atlantic Oceanfront','Art Deco Historic District','World-Class Nightlife','Celebrity Enclave'],
        'descriptions':{
            'en':"Miami Beach is the world's most iconic beach destination — a vibrant island city combining Art Deco architecture, world-famous nightlife, and pristine Atlantic beaches.",
            'es':"Miami Beach es el destino de playa más icónico del mundo — una vibrante ciudad isleña que combina arquitectura Art Deco, vida nocturna de fama mundial y playas atlánticas prístinas.",
            'pt':"Miami Beach é o destino de praia mais icônico do mundo — uma cidade insular vibrante que combina arquitetura Art Deco, vida noturna mundialmente famosa e praias atlânticas prístinas.",
            'ru':"Майами-Бич — самый знаковый пляжный курорт мира — живой островной город с архитектурой Арт-деко, всемирно известной ночной жизнью и нетронутыми пляжами.",
        },
    },
    'edgewater': {
        'name':'Edgewater','tagline':"Bay Views, Arts Culture & Miami's Fastest Growth",
        'geo':{'lat':25.7936,'lng':-80.1878},
        'highlights':['Biscayne Bay Views','Near Wynwood Arts','Emerging Luxury Hub','High Growth Potential'],
        'descriptions':{
            'en':"Edgewater is Miami's fastest-growing luxury neighborhood — a waterfront district between the energy of Wynwood and the sophistication of Brickell, with unobstructed Biscayne Bay views.",
            'es':"Edgewater es el vecindario de lujo de más rápido crecimiento en Miami — un distrito frente al mar entre la energía de Wynwood y la sofisticación de Brickell.",
            'pt':"Edgewater é o bairro de luxo de crescimento mais rápido de Miami — um distrito à beira-mar entre a energia do Wynwood e a sofisticação do Brickell.",
            'ru':"Эджуотер — самый быстрорастущий роскошный район Майами — прибрежный район между энергией Вайнвуда и изысканностью Брикелла.",
        },
    },
    'downtown-miami': {
        'name':'Downtown Miami','tagline':"Miami's Urban Heart — Culture, Bay Views & Connectivity",
        'geo':{'lat':25.7751,'lng':-80.1951},
        'highlights':['Bay & Ocean Views','Brightline Rail Access','Cultural District','Urban Walkability'],
        'descriptions':{
            'en':"Downtown Miami is the beating heart of the Magic City — a dynamic urban core with stunning bay views, world-class museums, and direct Brightline rail access to Fort Lauderdale and Orlando.",
            'es':"Downtown Miami es el corazón palpitante de la Ciudad Mágica — un núcleo urbano dinámico con impresionantes vistas a la bahía y acceso directo al tren Brightline.",
            'pt':"Downtown Miami é o coração pulsante da Cidade Mágica — um núcleo urbano dinâmico com vistas deslumbrantes da baía e acesso direto ao trem Brightline.",
            'ru':"Центр Майами — бьющееся сердце Волшебного города — динамичный городской центр с видами на залив и железнодорожным сообщением Brightline.",
        },
    },
    'brickell-key': {
        'name':'Brickell Key','tagline':"Miami's Most Exclusive Private Island Address",
        'geo':{'lat':25.7676,'lng':-80.1875},
        'highlights':['360° Water Views','Private Island','Ultra-Exclusive','Steps from Brickell'],
        'descriptions':{
            'en':"Brickell Key is Miami's most exclusive private island — a manicured oasis in Biscayne Bay just steps from the Brickell financial district, with 360° water views and complete privacy.",
            'es':"Brickell Key es la isla privada más exclusiva de Miami — un oasis cuidado en la Bahía de Biscayne a pasos del distrito financiero de Brickell.",
            'pt':"Brickell Key é a ilha privada mais exclusiva de Miami — um oásis bem cuidado na Baía Biscayne a passos do distrito financeiro de Brickell.",
            'ru':"Брикелл-Ки — самый эксклюзивный частный остров Майами — ухоженный оазис в бухте Бискайн в шаге от финансового района.",
        },
    },
    'wynwood': {
        'name':'Wynwood','tagline':"Miami's Arts Capital — Culture Meets Luxury Living",
        'geo':{'lat':25.8006,'lng':-80.1993},
        'highlights':['World-Famous Street Art','Top Restaurant Scene','Creative Community','High Appreciation'],
        'descriptions':{
            'en':"Wynwood is Miami's creative capital — a vibrant arts district famed for world-renowned murals, cutting-edge galleries, and the city's best restaurant scene, now transforming into a luxury residential destination.",
            'es':"Wynwood es la capital creativa de Miami — un vibrante distrito artístico famoso por sus murales de renombre mundial, galerías de vanguardia y la mejor escena gastronómica de la ciudad.",
            'pt':"Wynwood é a capital criativa de Miami — um vibrante distrito artístico famoso por murais de renome mundial, galerias de vanguarda e a melhor cena gastronômica da cidade.",
            'ru':"Вайнвуд — творческая столица Майами — яркий художественный район с всемирно известными муралами, передовыми галереями и лучшей ресторанной сценой города.",
        },
    },
}

CAT_NAMES = {
    'new-developments':{'en':'New Developments','es':'Nuevos Desarrollos','pt':'Novos Empreendimentos','ru':'Новостройки'},
    'villas':          {'en':'Luxury Villas',   'es':'Villas de Lujo',    'pt':'Vilas de Luxo',        'ru':'Виллы'},
    'penthouses':      {'en':'Penthouses',       'es':'Penthouses',        'pt':'Coberturas',           'ru':'Пентхаусы'},
}

#──Language configs ───────────────────────────────────────────
LANGS = {
    'en':{'code':'en','dir':'','hreflang':'en','og_locale':'en_US','T':{
        'nav_all':'New Developments','nav_contact':'Contact','nav_vip':'Get VIP Access',
        'hub_label':'New Developments','hub_title':'New Pre-Construction Condos in Miami',
        'hub_subtitle':"Explore the most exclusive pre-construction residences across Miami's most sought-after neighborhoods. Zero buyer commission — we work exclusively for you.",
        'hub_browse':'Browse by Neighborhood','hub_all':'All Projects',
        'hood_label':'Pre-Construction Condos','hood_other':'Other Miami Neighborhoods','hood_all_miami':'← All Miami Developments',
        'card_from':'From','card_floors':'Floors','card_units':'Residences','card_delivery':'Delivery','card_view':'View Details →',
        'cta_title':'Get Exclusive Access','cta_subtitle':'Floor plans, pricing & developer brochures — sent to your inbox.',
        'cta_name':'Full Name','cta_email':'Email Address','cta_submit':'Request Information →',
        'hub_meta_title':'New Pre-Construction Condos Miami 2025 | MiaLux Realty',
        'hub_meta_desc':'Browse all new pre-construction condos in Miami. Brickell, Miami Beach, Edgewater, Sunny Isles & more. VIP pricing, no buyer fees.',
        'hood_meta_title':'New Pre-Construction Condos in {hood} Miami 2025 | MiaLux Realty',
        'hood_meta_desc':'Discover new pre-construction condos in {hood}, Miami. Exclusive VIP pricing, full floor plans & developer info. Zero buyer commission.',
    }},
    'es':{'code':'es','dir':'es','hreflang':'es','og_locale':'es_LA','T':{
        'nav_all':'Nuevos Desarrollos','nav_contact':'Contacto','nav_vip':'Acceso VIP',
        'hub_label':'Nuevos Desarrollos','hub_title':'Nuevos Condominios en Preventa en Miami',
        'hub_subtitle':"Descubra las residencias en preventa más exclusivas en los vecindarios más codiciados de Miami. Sin comisión para el comprador.",
        'hub_browse':'Explorar por Vecindario','hub_all':'Todos los Proyectos',
        'hood_label':'Condominios en Preventa','hood_other':'Otros Vecindarios de Miami','hood_all_miami':'← Todos los Desarrollos en Miami',
        'card_from':'Desde','card_floors':'Pisos','card_units':'Residencias','card_delivery':'Entrega','card_view':'Ver Detalles →',
        'cta_title':'Obtenga Acceso Exclusivo','cta_subtitle':'Planos, precios y brochures del desarrollador — enviados a su correo.',
        'cta_name':'Nombre Completo','cta_email':'Correo Electrónico','cta_submit':'Solicitar Información →',
        'hub_meta_title':'Nuevos Condominios en Preventa Miami 2025 | MiaLux Realty',
        'hub_meta_desc':'Explore todos los nuevos condominios en preventa en Miami. Brickell, Miami Beach, Edgewater, Sunny Isles. Precios VIP, sin comisión.',
        'hood_meta_title':'Nuevos Condominios en Preventa en {hood} Miami | MiaLux Realty',
        'hood_meta_desc':'Descubra nuevos condominios en preventa en {hood}, Miami. Precios VIP exclusivos, planos completos. Sin comisión.',
    }},
    'pt':{'code':'pt','dir':'pt','hreflang':'pt','og_locale':'pt_BR','T':{
        'nav_all':'Novos Empreendimentos','nav_contact':'Contato','nav_vip':'Acesso VIP',
        'hub_label':'Novos Empreendimentos','hub_title':'Novos Apartamentos na Planta em Miami',
        'hub_subtitle':"Descubra os empreendimentos mais exclusivos nos bairros mais cobiçados de Miami. Sem comissão para o comprador.",
        'hub_browse':'Explorar por Bairro','hub_all':'Todos os Projetos',
        'hood_label':'Apartamentos na Planta','hood_other':'Outros Bairros de Miami','hood_all_miami':'← Todos os Empreendimentos',
        'card_from':'A partir de','card_floors':'Andares','card_units':'Residências','card_delivery':'Entrega','card_view':'Ver Detalhes →',
        'cta_title':'Obtenha Acesso Exclusivo','cta_subtitle':'Plantas, preços e brochures do incorporador — enviados para seu e-mail.',
        'cta_name':'Nome Completo','cta_email':'E-mail','cta_submit':'Solicitar Informações →',
        'hub_meta_title':'Novos Apartamentos na Planta Miami 2025 | MiaLux Realty',
        'hub_meta_desc':'Explore novos apartamentos na planta em Miami. Brickell, Miami Beach, Edgewater, Sunny Isles. Preços VIP, sem comissão.',
        'hood_meta_title':'Novos Apartamentos na Planta em {hood} Miami | MiaLux Realty',
        'hood_meta_desc':'Descubra novos apartamentos na planta em {hood}, Miami. Preços VIP exclusivos, plantas completas. Sem comissão.',
    }},
    'ru':{'code':'ru','dir':'ru','hreflang':'ru','og_locale':'ru_RU','T':{
        'nav_all':'Все Проекты','nav_contact':'Контакты','nav_vip':'VIP Доступ',
        'hub_label':'Новостройки','hub_title':'Новые Кондоминиумы в Майами',
        'hub_subtitle':"Исследуйте самые эксклюзивные новостройки в самых востребованных районах Майами. Без комиссии для покупателя.",
        'hub_browse':'Поиск по Районам','hub_all':'Все Проекты',
        'hood_label':'Новостройки','hood_other':'Другие Районы Майами','hood_all_miami':'← Все Новостройки Майами',
        'card_from':'От','card_floors':'Этажей','card_units':'Резиденций','card_delivery':'Сдача','card_view':'Подробнее →',
        'cta_title':'Получить Эксклюзивный Доступ','cta_subtitle':'Планировки, цены и брошюры застройщика — на вашу почту.',
        'cta_name':'Полное Имя','cta_email':'Email','cta_submit':'Запросить Информацию →',
        'hub_meta_title':'Новые Кондоминиумы в Майами 2025 | MiaLux Realty',
        'hub_meta_desc':'Все новые кондоминиумы в Майами. Брикелл, Майами Бич, Эджуотер, Санни-Айлс. VIP-цены, без комиссии.',
        'hood_meta_title':'Новостройки в {hood} Майами | MiaLux Realty',
        'hood_meta_desc':'Новые кондоминиумы в {hood}, Майами. Эксклюзивные VIP-цены, полные планировки. Без комиссии.',
    }},
}

#──Helpers ────────────────────────────────────────────────────
def fmt_price(n):
    if not n: return 'Contact for Pricing'
    if n >= 1000000:
        v = n/1000000
        return f"${v:.1f}M".replace('.0M','M')
    return f"${n:,}"

def lp(d): return f"{d}/" if d else ""

def write_file(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path,'w',encoding='utf-8') as f: f.write(content)

def replace_all(tmpl, reps):
    html = tmpl
    for k,v in reps.items(): html = html.replace(k, str(v) if v is not None else '')
    return html

def lang_active(code, current): return 'class="active"' if code==current else ''

def abs_img(url):
    if not url: return ''
    if url.startswith('http'): return url
    if url.startswith('//'): return 'https:' + url
    if url.startswith('/'): return BASE_URL + url
    return BASE_URL + '/' + url

def purl(lang_dir, *parts):
    prefix = lp(lang_dir)
    path   = '/'.join(p.strip('/') for p in parts if p)
    return f"{BASE_URL}/{prefix}{path}/"

def hreflang(*path_parts):
    lines = []
    for lc, l in LANGS.items():
        lines.append(f'  <link rel="alternate" hreflang="{l["hreflang"]}" href="{purl(l["dir"], *path_parts)}">')
    lines.append(f'  <link rel="alternate" hreflang="x-default" href="{purl("", *path_parts)}">')
    return '\n'.join(lines)

def og(title, desc, url, image, locale):
    img = abs_img(image) if image else f"{BASE_URL}/images/og-default.jpg"
    return '\n'.join([
        f'  <meta property="og:type" content="website">',
        f'  <meta property="og:site_name" content="{SITE_NAME}">',
        f'  <meta property="og:url" content="{url}">',
        f'  <meta property="og:title" content="{title}">',
        f'  <meta property="og:description" content="{desc}">',
        f'  <meta property="og:image" content="{img}">',
        f'  <meta property="og:image:width" content="1200">',
        f'  <meta property="og:image:height" content="630">',
        f'  <meta property="og:locale" content="{locale}">',
        f'  <meta name="twitter:card" content="summary_large_image">',
        f'  <meta name="twitter:site" content="@mialuxrealty">',
        f'  <meta name="twitter:title" content="{title}">',
        f'  <meta name="twitter:description" content="{desc}">',
        f'  <meta name="twitter:image" content="{img}">',
    ])

def inject_head(html, og_block, hl_block):
    html = re.sub(r'\s*<meta (?:property|name)="(?:og:|twitter:)[^"]*"[^>]*>\n?','\n',html)
    html = re.sub(r'\s*<link rel="alternate" hreflang[^>]*>\n?','\n',html)
    html = html.replace('</title>', f'</title>\n{og_block}\n{hl_block}', 1)
    return html

def inject_schema(html, schema_obj):
    s = json.dumps(schema_obj, ensure_ascii=False, indent=2)
    block = f'<script type="application/ld+json">\n{s}\n</script>'
    result = re.sub(r'<script type="application/ld\+json">.*?</script>', block, html, flags=re.DOTALL, count=1)
    if result == html:
        html = html.replace('</head>', f'{block}\n</head>', 1)
        return html
    return result

#──Schema generators ──────────────────────────────────────────
def s_agent(): return {"@type":"RealEstateAgent","@id":AGENT_ID}

def s_hub(cat, lang, T):
    url = purl(lang['dir'], cat)
    return {"@context":"https://schema.org","@graph":[
        {"@type":"CollectionPage","@id":url+"#page",
         "name":T['hub_meta_title'],"description":T['hub_meta_desc'],
         "url":url,"inLanguage":lang['hreflang'],"isPartOf":{"@id":WEBSITE_ID},
         "about":{"@type":"Place","name":"Miami","address":{"@type":"PostalAddress","addressLocality":"Miami","addressRegion":"FL","addressCountry":"US"}},
         "breadcrumb":{"@type":"BreadcrumbList","itemListElement":[
             {"@type":"ListItem","position":1,"name":SITE_NAME,"item":BASE_URL},
             {"@type":"ListItem","position":2,"name":T['hub_label'],"item":url}
         ]}},
        s_agent()
    ]}

def s_hood(cat, hood_slug, hood_name, geo, meta_title, meta_desc, lang, T):
    url     = purl(lang['dir'], cat, hood_slug)
    hub_url = purl(lang['dir'], cat)
    g = geo or {'lat':25.7617,'lng':-80.1918}
    return {"@context":"https://schema.org","@graph":[
        {"@type":"CollectionPage","@id":url+"#page",
         "name":meta_title,"description":meta_desc,
         "url":url,"inLanguage":lang['hreflang'],"isPartOf":{"@id":WEBSITE_ID},
         "breadcrumb":{"@type":"BreadcrumbList","itemListElement":[
             {"@type":"ListItem","position":1,"name":SITE_NAME,"item":BASE_URL},
             {"@type":"ListItem","position":2,"name":T['hub_label'],"item":hub_url},
             {"@type":"ListItem","position":3,"name":hood_name,"item":url}
         ]}},
        {"@type":["Place","AdministrativeArea"],
         "@id":f"{BASE_URL}/{cat}/{hood_slug}/#place",
         "name":f"{hood_name}, Miami",
         "address":{"@type":"PostalAddress","addressLocality":"Miami","addressRegion":"FL","addressCountry":"US"},
         "geo":{"@type":"GeoCoordinates","latitude":g['lat'],"longitude":g['lng']},
         "containedInPlace":{"@type":"City","name":"Miami","addressRegion":"FL"}},
        s_agent()
    ]}

def s_listing(listing, lang):
    cat   = listing['category']
    hood  = listing['_hood_slug']
    pslug = listing['page_slug']
    url    = purl(lang['dir'], cat, hood, pslug)
    en_url = purl('', cat, hood, pslug)
    hub_url  = purl(lang['dir'], cat)
    hood_url = purl(lang['dir'], cat, hood)
    hood_name = HOOD_META.get(hood,{}).get('name', hood.replace('-',' ').title())
    cat_name  = CAT_NAMES.get(cat,{}).get(lang['code'], cat)

    images = []
    if listing.get('image_main'): images.append(abs_img(listing['image_main']))
    for i in (listing.get('images_gallery') or []):
        a = abs_img(i)
        if a and a not in images: images.append(a)

    status = listing.get('status','')
    avail = 'https://schema.org/PreOrder' if any(x in status.lower() for x in ['selling','coming','pre']) else 'https://schema.org/InStock'

    unit_types = listing.get('unit_types') or []
    max_sqft = max((u.get('size_to') or u.get('size_from',0) for u in unit_types), default=None)
    max_beds = max((u.get('bathrooms',1) for u in unit_types), default=1)

    acc = {
        "@type":"Apartment","@id":en_url+"#accommodation",
        "name":listing.get('name',''),
        "description":listing.get('description_short',''),
        "address":{"@type":"PostalAddress",
            "streetAddress":(listing.get('address') or '').split(',')[0].strip(),
            "addressLocality":"Miami","addressRegion":"FL",
            "postalCode":listing.get('postal_code','33130'),"addressCountry":"US"},
        "geo":{"@type":"GeoCoordinates",
            "latitude":(listing.get('geo') or {}).get('lat',25.7617),
            "longitude":(listing.get('geo') or {}).get('lng',-80.1918)},
        "numberOfBathroomsTotal":max_beds,
        "numberOfRoomsTotal":listing.get('total_units'),
        "numberOfFloors":listing.get('floors'),
    }
    if max_sqft: acc["floorSize"]={"@type":"QuantitativeValue","value":max_sqft,"unitCode":"FTK"}
    if images:   acc["image"]=images[:5]

    offer = {"@type":"Offer","priceCurrency":"USD","availability":avail,
             "seller":{"@type":"RealEstateAgent","@id":AGENT_ID}}
    if listing.get('price_from'):
        offer["price"]=str(listing['price_from'])
        offer["priceSpecification"]={"@type":"PriceSpecification",
            "price":listing['price_from'],"priceCurrency":"USD",
            "minPrice":listing['price_from'],"maxPrice":listing.get('price_to',listing['price_from'])}

    lst = {
        "@type":"RealEstateListing","@id":en_url+"#listing",
        "name":listing.get('name',''),"description":listing.get('description_short',''),
        "url":url,"image":images[:5],"datePosted":date.today().isoformat(),
        "accommodation":{"@id":en_url+"#accommodation"},
        "offers":offer,
        "broker":{"@type":"RealEstateAgent","@id":AGENT_ID},
        "inLanguage":lang['hreflang'],"isPartOf":{"@id":WEBSITE_ID},
        "breadcrumb":{"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":SITE_NAME,"item":BASE_URL},
            {"@type":"ListItem","position":2,"name":cat_name,"item":hub_url},
            {"@type":"ListItem","position":3,"name":hood_name,"item":hood_url},
            {"@type":"ListItem","position":4,"name":listing.get('name',''),"item":en_url}
        ]}
    }

    if listing.get('rating_value') and listing.get('review_count',0)>0:
        lst["aggregateRating"]={"@type":"AggregateRating",
            "ratingValue":str(listing['rating_value']),"reviewCount":str(listing['review_count']),
            "bestRating":"5","worstRating":"1"}

    reviews = listing.get('reviews') or []
    if reviews:
        lst["review"]=[{"@type":"Review",
            "author":{"@type":"Person","name":r.get('author','Anonymous')},
            "reviewBody":r.get('body',''),
            "reviewRating":{"@type":"Rating","ratingValue":str(r.get('rating',5)),"bestRating":"5","worstRating":"1"},
            "datePublished":r.get('date',date.today().isoformat())} for r in reviews]

    return {"@context":"https://schema.org","@graph":[acc, lst, s_agent()]}

#──Load templates ─────────────────────────────────────────────
with open('hub-template.html', encoding='utf-8')     as f: HUB_T  = f.read()
with open('hood-template.html', encoding='utf-8')    as f: HOOD_T = f.read()
with open('landing-template.html', encoding='utf-8') as f: LAND_T = f.read()

# All hoods per category (include all HOOD_META for new-developments)
all_hoods_by_cat = {}
for cat, hoods in by_cat_hood.items():
    all_hoods_by_cat[cat] = list(hoods.keys())
all_hoods_by_cat['new-developments'] = list(set(
    all_hoods_by_cat.get('new-developments',[]) + list(HOOD_META.keys())))

# ─────────────────────────────────────────────────────────────
# HUB PAGES
# ─────────────────────────────────────────────────────────────
print("Building Hub pages...")
for lc, lang in LANGS.items():
    T, d = lang['T'], lang['dir']
    cat  = 'new-developments'
    url  = purl(d, cat)
    html = replace_all(HUB_T, {
        '{{LANG_CODE}}':lc,'{{LANG_CODE_UPPER}}':lc.upper(),'{{LANG_DIR}}':d,'{{LANG_DIR_PREFIX}}':lp(d),
        '{{CANONICAL_PATH}}':f"{lp(d)}{cat}/",
        '{{META_TITLE}}':T['hub_meta_title'],'{{META_DESC}}':T['hub_meta_desc'],
        '{{T_NAV_ALL_PROJECTS}}':T['nav_all'],'{{T_NAV_CONTACT}}':T['nav_contact'],'{{T_NAV_VIP}}':T['nav_vip'],
        '{{T_HUB_LABEL}}':T['hub_label'],'{{T_HUB_TITLE}}':T['hub_title'],'{{T_HUB_SUBTITLE}}':T['hub_subtitle'],
        '{{T_HUB_BROWSE}}':T['hub_browse'],'{{T_HUB_ALL_LISTINGS}}':T['hub_all'],'{{T_HUB_SEE_ALL}}':T['hub_all']+' →',
        '{{T_CARD_FROM}}':T['card_from'],'{{T_CARD_FLOORS}}':T['card_floors'],'{{T_CARD_UNITS}}':T['card_units'],
        '{{T_CARD_DELIVERY}}':T['card_delivery'],'{{T_CARD_VIEW}}':T['card_view'],
        '{{T_CTA_TITLE}}':T['cta_title'],'{{T_CTA_SUBTITLE}}':T['cta_subtitle'],
        '{{T_CTA_NAME}}':T['cta_name'],'{{T_CTA_EMAIL}}':T['cta_email'],'{{T_CTA_SUBMIT}}':T['cta_submit'],
        '{{EN_ACTIVE}}':lang_active('en',lc),'{{ES_ACTIVE}}':lang_active('es',lc),
        '{{PT_ACTIVE}}':lang_active('pt',lc),'{{RU_ACTIVE}}':lang_active('ru',lc),
        '{{LISTINGS_JSON}}':json.dumps(LISTINGS,ensure_ascii=False),
        '{{HOODS_META_JSON}}':json.dumps(HOOD_META,ensure_ascii=False),
    })
    html = inject_schema(html, s_hub(cat, lang, T))
    html = inject_head(html, og(T['hub_meta_title'],T['hub_meta_desc'],url,f"{BASE_URL}/images/miami-skyline.jpg",lang['og_locale']), hreflang(cat))
    out  = f"{d}/{cat}/index.html" if d else f"{cat}/index.html"
    write_file(out, html)
    print(f"  ✓ {out}")

# ─────────────────────────────────────────────────────────────
# NEIGHBORHOOD PAGES
# ─────────────────────────────────────────────────────────────
print("\nBuilding Neighborhood pages...")
for lc, lang in LANGS.items():
    T, d = lang['T'], lang['dir']
    cat  = 'new-developments'
    for hood_slug in all_hoods_by_cat.get(cat,[]):
        meta       = HOOD_META.get(hood_slug,{})
        hood_name  = meta.get('name', hood_slug.replace('-',' ').title())
        hood_desc  = meta.get('descriptions',{}).get(lc, meta.get('descriptions',{}).get('en',''))
        url        = purl(d, cat, hood_slug)
        meta_title = T['hood_meta_title'].replace('{hood}', hood_name)
        meta_desc  = T['hood_meta_desc'].replace('{hood}', hood_name)
        hood_img   = (by_cat_hood.get(cat,{}).get(hood_slug,[{}])[0]).get('image_main','')

        html = replace_all(HOOD_T, {
            '{{LANG_CODE}}':lc,'{{LANG_DIR}}':d,'{{LANG_DIR_PREFIX}}':lp(d),
            '{{CANONICAL_PATH}}':f"{lp(d)}{cat}/{hood_slug}/",
            '{{META_TITLE}}':meta_title,'{{META_DESC}}':meta_desc,
            '{{HOOD_SLUG}}':hood_slug,'{{HOOD_NAME}}':hood_name,
            '{{HOOD_TAGLINE}}':meta.get('tagline',''),'{{HOOD_DESCRIPTION}}':hood_desc,
            '{{T_HUB_LABEL}}':T['hub_label'],'{{T_HOOD_LABEL}}':T['hood_label'],
            '{{T_HOOD_OTHER}}':T['hood_other'],'{{T_HUB_ALL_MIAMI}}':T['hood_all_miami'],
            '{{T_NAV_ALL_PROJECTS}}':T['nav_all'],'{{T_NAV_CONTACT}}':T['nav_contact'],'{{T_NAV_VIP}}':T['nav_vip'],
            '{{T_CARD_FROM}}':T['card_from'],'{{T_CARD_FLOORS}}':T['card_floors'],'{{T_CARD_UNITS}}':T['card_units'],
            '{{T_CARD_DELIVERY}}':T['card_delivery'],'{{T_CARD_VIEW}}':T['card_view'],
            '{{T_CTA_TITLE}}':T['cta_title'],'{{T_CTA_SUBTITLE}}':T['cta_subtitle'],
            '{{T_CTA_NAME}}':T['cta_name'],'{{T_CTA_EMAIL}}':T['cta_email'],'{{T_CTA_SUBMIT}}':T['cta_submit'],
            '{{EN_ACTIVE}}':lang_active('en',lc),'{{ES_ACTIVE}}':lang_active('es',lc),
            '{{PT_ACTIVE}}':lang_active('pt',lc),'{{RU_ACTIVE}}':lang_active('ru',lc),
            '{{LISTINGS_JSON}}':json.dumps(LISTINGS,ensure_ascii=False),
            '{{ALL_HOODS_META_JSON}}':json.dumps(HOOD_META,ensure_ascii=False),
        })
        html = inject_schema(html, s_hood(cat, hood_slug, hood_name, meta.get('geo'), meta_title, meta_desc, lang, T))
        html = inject_head(html, og(meta_title,meta_desc,url,hood_img or f"{BASE_URL}/images/miami-{hood_slug}.jpg",lang['og_locale']), hreflang(cat, hood_slug))
        out  = f"{d}/{cat}/{hood_slug}/index.html" if d else f"{cat}/{hood_slug}/index.html"
        write_file(out, html)
    print(f"  ✓ {lc}: {len(all_hoods_by_cat.get(cat,[]))} neighborhood pages")

# ─────────────────────────────────────────────────────────────
# LISTING PAGES
# ─────────────────────────────────────────────────────────────
print("\nBuilding Listing pages...")
for lc, lang in LANGS.items():
    d = lang['dir']
    for listing in LISTINGS:
        cat   = listing['category']
        hood  = listing['_hood_slug']
        pslug = listing['page_slug']
        url   = purl(d, cat, hood, pslug)
        img   = listing.get('image_main','')
        meta_title = listing.get('meta_title') or f"{listing['name']} | Pre-Construction {listing.get('neighborhood','Miami')} | MiaLux Realty"
        meta_desc  = listing.get('meta_description') or listing.get('description_short','')

        html = replace_all(LAND_T, {
            '{{META_TITLE}}':meta_title,'{{META_DESCRIPTION}}':meta_desc,
            '{{IMAGE_MAIN}}':abs_img(img),'{{SLUG}}':pslug,
            '{{NAME}}':listing.get('name',''),'{{STATUS}}':listing.get('status','Coming Soon'),
            '{{NEIGHBORHOOD}}':listing.get('neighborhood','Miami'),
            '{{TAGLINE}}':listing.get('tagline',''),
            '{{FLOORS}}':str(listing.get('floors','')),
            '{{TOTAL_UNITS}}':str(listing.get('total_units','')),
            '{{ESTIMATED_DELIVERY}}':listing.get('estimated_delivery',''),
            '{{PRICE_FROM_FMT}}':fmt_price(listing.get('price_from',0)),
            '{{DESCRIPTION_FULL}}':listing.get('description_full') or listing.get('description_short',''),
            '{{DESCRIPTION_FULL_P2}}':listing.get('description_short',''),
            '{{ADDRESS}}':listing.get('address','Miami, FL'),
            '{{PRICE_FROM}}':str(listing.get('price_from',0)),
            '{{LISTING_JSON}}':json.dumps(listing,ensure_ascii=False),
            '{{LANG_CODE}}':lc,'{{LANG_CODE_UPPER}}':lc.upper(),'{{LANG_DIR}}':d,
            '/new-developments/':f"/{lp(d)}{cat}/",
        })
        html = inject_schema(html, s_listing(listing, lang))
        html = inject_head(html, og(meta_title,meta_desc,url,img,lang['og_locale']), hreflang(cat, hood, pslug))
        out  = f"{d}/{cat}/{hood}/{pslug}/index.html" if d else f"{cat}/{hood}/{pslug}/index.html"
        write_file(out, html)
    print(f"  ✓ {lc}: {len(LISTINGS)} listing pages")

# ─────────────────────────────────────────────────────────────
# SITEMAP
# ─────────────────────────────────────────────────────────────
print("\nBuilding sitemap...")
today = date.today().isoformat()
urls  = []

def add_url(u, priority, freq, img_url=None, img_title=None):
    img = f"\n    <image:image><image:loc>{abs_img(img_url)}</image:loc><image:title>{img_title or ''}</image:title></image:image>" if img_url else ""
    urls.append(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{priority}</priority>{img}\n  </url>")

add_url(BASE_URL+'/', '1.0', 'weekly')
for cat in ALL_CATEGORIES:
    for lc,l in LANGS.items(): add_url(purl(l['dir'],cat), '0.9', 'daily')
    for hs in all_hoods_by_cat.get(cat,[]):
        for lc,l in LANGS.items(): add_url(purl(l['dir'],cat,hs), '0.8', 'weekly')
    for listing in [x for x in LISTINGS if x['category']==cat]:
        for lc,l in LANGS.items():
            add_url(purl(l['dir'],cat,listing['_hood_slug'],listing['page_slug']),
                    '0.85','weekly',listing.get('image_main',''),listing.get('name',''))

sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n{chr(10).join(urls)}\n</urlset>'
with open('sitemap.xml','w', encoding='utf-8') as f: f.write(sitemap)
print(f"  ✓ sitemap.xml: {len(urls)} URLs")

# ─────────────────────────────────────────────────────────────
# _REDIRECTS
# ─────────────────────────────────────────────────────────────
with open('_redirects','w', encoding='utf-8') as f:
    f.write("# MiaLux Realty — _redirects\n# Cloudflare Pages serves index.html automatically — no rewrites needed.\n# Add 301s here only when URLs change after the site goes live.\n")
print(f"  ✓ _redirects: empty (not needed yet)")

with open('robots.txt','w', encoding='utf-8') as f:
    f.write("# MiaLux Realty — robots.txt\n# STATUS: DEVELOPMENT MODE — all crawlers blocked\n\nUser-agent: *\nDisallow: /\n\n# PRODUCTION VERSION (use when ready to go live)\n# User-agent: *\n# Allow: /\n# Disallow: /admin/\n#\n# Sitemap: https://mialuxrealty.com/sitemap.xml\n")
print("  ✓ robots.txt")

total_hood_pages = len(LANGS)*sum(len(v) for v in all_hoods_by_cat.values())
print(f"""
╔══════════════════════════════════════════════╗
║  BUILD COMPLETE v3                           ║
╠══════════════════════════════════════════════╣
║  Hub pages           {len(LANGS)*len(ALL_CATEGORIES):>4}                        ║
║  Neighborhood pages  {total_hood_pages:>4}                        ║
║  Listing pages       {len(LANGS)*len(LISTINGS):>4}                        ║
║  Sitemap URLs        {len(urls):>4}                        ║
╚══════════════════════════════════════════════╝
""")