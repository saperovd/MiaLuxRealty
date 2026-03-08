#!/usr/bin/env python3
"""
MiaLux Realty â Master Build Script v3
URL Structure:
  /new-developments/                               â Category hub (EN)
  /new-developments/brickell/                      â Neighborhood (EN)
  /new-developments/brickell/cipriani-residences/  â Listing (EN)
  /es/new-developments/brickell/cipriani-residences/ â Listing (ES)

Future categories:
  /villas/brickell/casa-bella/
  /penthouses/brickell/cipriani-penthouse/
  /es/villas/brickell/

Root stays CLEAN â only index.html + config files.
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

#──Load listings ââââââââââââââââââââââââââââââââââââââââââââââ
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

#──Neighborhood metadata ââââââââââââââââââââââââââââââââââââââ
HOOD_META = {
    'brickell': {
        'name':'Brickell','tagline':"Miami's Financial Capital & Luxury Living Hub",
        'geo':{'lat':25.7617,'lng':-80.1918},
        'highlights':['Bay & City Views','Walk Score 95+','World-Class Dining','Top Investment Returns'],
        'descriptions':{
            'en':"Brickell is Miami's undisputed financial capital â a gleaming vertical neighborhood of luxury towers, world-class restaurants, and bayfront parks. Known as the \"Manhattan of the South,\" it attracts global investors and urban professionals seeking walkable luxury living steps from the bay.",
            'es':"Brickell es la indiscutible capital financiera de Miami â un resplandeciente barrio vertical de torres de lujo, restaurantes de clase mundial y parques frente a la bahÃ­a.",
            'pt':"Brickell Ã© a capital financeira indiscutÃ­vel de Miami â um bairro vertical repleto de torres de luxo, restaurantes de classe mundial e parques Ã  beira da baÃ­a.",
            'ru':"ÐÑÐ¸ÐºÐµÐ»Ð» â Ð±ÐµÑÑÐ¿Ð¾ÑÐ½Ð°Ñ ÑÐ¸Ð½Ð°Ð½ÑÐ¾Ð²Ð°Ñ ÑÑÐ¾Ð»Ð¸ÑÐ° ÐÐ°Ð¹Ð°Ð¼Ð¸ â ÑÐ¸ÑÑÑÐ¸Ð¹ Ð²ÐµÑÑÐ¸ÐºÐ°Ð»ÑÐ½ÑÐ¹ ÑÐ°Ð¹Ð¾Ð½ ÑÐ¾ÑÐºÐ¾ÑÐ½ÑÑ Ð±Ð°ÑÐµÐ½, ÑÐµÑÑÐ¾ÑÐ°Ð½Ð¾Ð² Ð¼Ð¸ÑÐ¾Ð²Ð¾Ð³Ð¾ ÐºÐ»Ð°ÑÑÐ° Ð¸ Ð¿Ð°ÑÐºÐ¾Ð² Ð½Ð° Ð±ÐµÑÐµÐ³Ñ Ð·Ð°Ð»Ð¸Ð²Ð°.",
        },
    },
    'sunny-isles-beach': {
        'name':'Sunny Isles Beach','tagline':"The Riviera of the Americas â Oceanfront Ultra-Luxury",
        'geo':{'lat':25.9386,'lng':-80.1222},
        'highlights':['Direct Ocean Access','Ultra-Luxury Brand Towers','Private Beach','International Community'],
        'descriptions':{
            'en':"Sunny Isles Beach â nicknamed the \"Riviera of the Americas\" â is a pristine barrier island between the Atlantic Ocean and the Intracoastal Waterway. Home to iconic ultra-luxury towers by Porsche, Armani and Bentley.",
            'es':"Sunny Isles Beach â apodada la \"Riviera de las AmÃ©ricas\" â es una prÃ­stina isla barrera entre el OcÃ©ano AtlÃ¡ntico y la VÃ­a Intracostera.",
            'pt':"Sunny Isles Beach â apelidada de \"Riviera das AmÃ©ricas\" â Ã© uma ilha barreira pristina entre o Oceano AtlÃ¢ntico e a Hidrovia Intracoastal.",
            'ru':"Ð¡Ð°Ð½Ð½Ð¸-ÐÐ¹Ð»Ñ-ÐÐ¸Ñ â Ð¿ÑÐ¾Ð·Ð²Ð°Ð½Ð½ÑÐ¹ Â«Ð Ð¸Ð²ÑÐµÑÐ¾Ð¹ ÐÐ¼ÐµÑÐ¸ÐºÐ¸Â» â Ð½ÐµÑÑÐ¾Ð½ÑÑÑÐ¹ Ð±Ð°ÑÑÐµÑÐ½ÑÐ¹ Ð¾ÑÑÑÐ¾Ð² Ð¼ÐµÐ¶Ð´Ñ ÐÑÐ»Ð°Ð½ÑÐ¸ÑÐµÑÐºÐ¸Ð¼ Ð¾ÐºÐµÐ°Ð½Ð¾Ð¼ Ð¸ ÐÐ½ÑÑÑÐ¸Ð±ÐµÑÐµÐ³Ð¾Ð²ÑÐ¼ Ð²Ð¾Ð´Ð½ÑÐ¼ Ð¿ÑÑÐµÐ¼.",
        },
    },
    'miami-beach': {
        'name':'Miami Beach','tagline':"The World's Most Iconic Beach Address",
        'geo':{'lat':25.7907,'lng':-80.1300},
        'highlights':['Atlantic Oceanfront','Art Deco Historic District','World-Class Nightlife','Celebrity Enclave'],
        'descriptions':{
            'en':"Miami Beach is the world's most iconic beach destination â a vibrant island city combining Art Deco architecture, world-famous nightlife, and pristine Atlantic beaches.",
            'es':"Miami Beach es el destino de playa mÃ¡s icÃ³nico del mundo â una vibrante ciudad isleÃ±a que combina arquitectura Art Deco, vida nocturna de fama mundial y playas atlÃ¡nticas prÃ­stinas.",
            'pt':"Miami Beach Ã© o destino de praia mais icÃ´nico do mundo â uma cidade insular vibrante que combina arquitetura Art Deco, vida noturna mundialmente famosa e praias atlÃ¢nticas prÃ­stinas.",
            'ru':"ÐÐ°Ð¹Ð°Ð¼Ð¸-ÐÐ¸Ñ â ÑÐ°Ð¼ÑÐ¹ Ð·Ð½Ð°ÐºÐ¾Ð²ÑÐ¹ Ð¿Ð»ÑÐ¶Ð½ÑÐ¹ ÐºÑÑÐ¾ÑÑ Ð¼Ð¸ÑÐ° â Ð¶Ð¸Ð²Ð¾Ð¹ Ð¾ÑÑÑÐ¾Ð²Ð½Ð¾Ð¹ Ð³Ð¾ÑÐ¾Ð´ Ñ Ð°ÑÑÐ¸ÑÐµÐºÑÑÑÐ¾Ð¹ ÐÑÑ-Ð´ÐµÐºÐ¾, Ð²ÑÐµÐ¼Ð¸ÑÐ½Ð¾ Ð¸Ð·Ð²ÐµÑÑÐ½Ð¾Ð¹ Ð½Ð¾ÑÐ½Ð¾Ð¹ Ð¶Ð¸Ð·Ð½ÑÑ Ð¸ Ð½ÐµÑÑÐ¾Ð½ÑÑÑÐ¼Ð¸ Ð¿Ð»ÑÐ¶Ð°Ð¼Ð¸.",
        },
    },
    'edgewater': {
        'name':'Edgewater','tagline':"Bay Views, Arts Culture & Miami's Fastest Growth",
        'geo':{'lat':25.7936,'lng':-80.1878},
        'highlights':['Biscayne Bay Views','Near Wynwood Arts','Emerging Luxury Hub','High Growth Potential'],
        'descriptions':{
            'en':"Edgewater is Miami's fastest-growing luxury neighborhood â a waterfront district between the energy of Wynwood and the sophistication of Brickell, with unobstructed Biscayne Bay views.",
            'es':"Edgewater es el vecindario de lujo de mÃ¡s rÃ¡pido crecimiento en Miami â un distrito frente al mar entre la energÃ­a de Wynwood y la sofisticaciÃ³n de Brickell.",
            'pt':"Edgewater Ã© o bairro de luxo de crescimento mais rÃ¡pido de Miami â um distrito Ã  beira-mar entre a energia do Wynwood e a sofisticaÃ§Ã£o do Brickell.",
            'ru':"Ð­Ð´Ð¶ÑÐ¾ÑÐµÑ â ÑÐ°Ð¼ÑÐ¹ Ð±ÑÑÑÑÐ¾ÑÐ°ÑÑÑÑÐ¸Ð¹ ÑÐ¾ÑÐºÐ¾ÑÐ½ÑÐ¹ ÑÐ°Ð¹Ð¾Ð½ ÐÐ°Ð¹Ð°Ð¼Ð¸ â Ð¿ÑÐ¸Ð±ÑÐµÐ¶Ð½ÑÐ¹ ÑÐ°Ð¹Ð¾Ð½ Ð¼ÐµÐ¶Ð´Ñ ÑÐ½ÐµÑÐ³Ð¸ÐµÐ¹ ÐÐ°Ð¹Ð½Ð²ÑÐ´Ð° Ð¸ Ð¸Ð·ÑÑÐºÐ°Ð½Ð½Ð¾ÑÑÑÑ ÐÑÐ¸ÐºÐµÐ»Ð»Ð°.",
        },
    },
    'downtown-miami': {
        'name':'Downtown Miami','tagline':"Miami's Urban Heart â Culture, Bay Views & Connectivity",
        'geo':{'lat':25.7751,'lng':-80.1951},
        'highlights':['Bay & Ocean Views','Brightline Rail Access','Cultural District','Urban Walkability'],
        'descriptions':{
            'en':"Downtown Miami is the beating heart of the Magic City â a dynamic urban core with stunning bay views, world-class museums, and direct Brightline rail access to Fort Lauderdale and Orlando.",
            'es':"Downtown Miami es el corazÃ³n palpitante de la Ciudad MÃ¡gica â un nÃºcleo urbano dinÃ¡mico con impresionantes vistas a la bahÃ­a y acceso directo al tren Brightline.",
            'pt':"Downtown Miami Ã© o coraÃ§Ã£o pulsante da Cidade MÃ¡gica â um nÃºcleo urbano dinÃ¢mico com vistas deslumbrantes da baÃ­a e acesso direto ao trem Brightline.",
            'ru':"Ð¦ÐµÐ½ÑÑ ÐÐ°Ð¹Ð°Ð¼Ð¸ â Ð±ÑÑÑÐµÐµÑÑ ÑÐµÑÐ´ÑÐµ ÐÐ¾Ð»ÑÐµÐ±Ð½Ð¾Ð³Ð¾ Ð³Ð¾ÑÐ¾Ð´Ð° â Ð´Ð¸Ð½Ð°Ð¼Ð¸ÑÐ½ÑÐ¹ Ð³Ð¾ÑÐ¾Ð´ÑÐºÐ¾Ð¹ ÑÐµÐ½ÑÑ Ñ Ð²Ð¸Ð´Ð°Ð¼Ð¸ Ð½Ð° Ð·Ð°Ð»Ð¸Ð² Ð¸ Ð¶ÐµÐ»ÐµÐ·Ð½Ð¾Ð´Ð¾ÑÐ¾Ð¶Ð½ÑÐ¼ ÑÐ¾Ð¾Ð±ÑÐµÐ½Ð¸ÐµÐ¼ Brightline.",
        },
    },
    'brickell-key': {
        'name':'Brickell Key','tagline':"Miami's Most Exclusive Private Island Address",
        'geo':{'lat':25.7676,'lng':-80.1875},
        'highlights':['360Â° Water Views','Private Island','Ultra-Exclusive','Steps from Brickell'],
        'descriptions':{
            'en':"Brickell Key is Miami's most exclusive private island â a manicured oasis in Biscayne Bay just steps from the Brickell financial district, with 360Â° water views and complete privacy.",
            'es':"Brickell Key es la isla privada mÃ¡s exclusiva de Miami â un oasis cuidado en la BahÃ­a de Biscayne a pasos del distrito financiero de Brickell.",
            'pt':"Brickell Key Ã© a ilha privada mais exclusiva de Miami â um oÃ¡sis bem cuidado na BaÃ­a Biscayne a passos do distrito financeiro de Brickell.",
            'ru':"ÐÑÐ¸ÐºÐµÐ»Ð»-ÐÐ¸ â ÑÐ°Ð¼ÑÐ¹ ÑÐºÑÐºÐ»ÑÐ·Ð¸Ð²Ð½ÑÐ¹ ÑÐ°ÑÑÐ½ÑÐ¹ Ð¾ÑÑÑÐ¾Ð² ÐÐ°Ð¹Ð°Ð¼Ð¸ â ÑÑÐ¾Ð¶ÐµÐ½Ð½ÑÐ¹ Ð¾Ð°Ð·Ð¸Ñ Ð² Ð±ÑÑÑÐµ ÐÐ¸ÑÐºÐ°Ð¹Ð½ Ð² ÑÐ°Ð³Ðµ Ð¾Ñ ÑÐ¸Ð½Ð°Ð½ÑÐ¾Ð²Ð¾Ð³Ð¾ ÑÐ°Ð¹Ð¾Ð½Ð°.",
        },
    },
    'wynwood': {
        'name':'Wynwood','tagline':"Miami's Arts Capital â Culture Meets Luxury Living",
        'geo':{'lat':25.8006,'lng':-80.1993},
        'highlights':['World-Famous Street Art','Top Restaurant Scene','Creative Community','High Appreciation'],
        'descriptions':{
            'en':"Wynwood is Miami's creative capital â a vibrant arts district famed for world-renowned murals, cutting-edge galleries, and the city's best restaurant scene, now transforming into a luxury residential destination.",
            'es':"Wynwood es la capital creativa de Miami â un vibrante distrito artÃ­stico famoso por sus murales de renombre mundial, galerÃ­as de vanguardia y la mejor escena gastronÃ³mica de la ciudad.",
            'pt':"Wynwood Ã© a capital criativa de Miami â um vibrante distrito artÃ­stico famoso por murais de renome mundial, galerias de vanguarda e a melhor cena gastronÃ´mica da cidade.",
            'ru':"ÐÐ°Ð¹Ð½Ð²ÑÐ´ â ÑÐ²Ð¾ÑÑÐµÑÐºÐ°Ñ ÑÑÐ¾Ð»Ð¸ÑÐ° ÐÐ°Ð¹Ð°Ð¼Ð¸ â ÑÑÐºÐ¸Ð¹ ÑÑÐ´Ð¾Ð¶ÐµÑÑÐ²ÐµÐ½Ð½ÑÐ¹ ÑÐ°Ð¹Ð¾Ð½ Ñ Ð²ÑÐµÐ¼Ð¸ÑÐ½Ð¾ Ð¸Ð·Ð²ÐµÑÑÐ½ÑÐ¼Ð¸ Ð¼ÑÑÐ°Ð»Ð°Ð¼Ð¸, Ð¿ÐµÑÐµÐ´Ð¾Ð²ÑÐ¼Ð¸ Ð³Ð°Ð»ÐµÑÐµÑÐ¼Ð¸ Ð¸ Ð»ÑÑÑÐµÐ¹ ÑÐµÑÑÐ¾ÑÐ°Ð½Ð½Ð¾Ð¹ ÑÑÐµÐ½Ð¾Ð¹ Ð³Ð¾ÑÐ¾Ð´Ð°.",
        },
    },
}

CAT_NAMES = {
    'new-developments':{'en':'New Developments','es':'Nuevos Desarrollos','pt':'Novos Empreendimentos','ru':'ÐÐ¾Ð²Ð¾ÑÑÑÐ¾Ð¹ÐºÐ¸'},
    'villas':          {'en':'Luxury Villas',   'es':'Villas de Lujo',    'pt':'Vilas de Luxo',        'ru':'ÐÐ¸Ð»Ð»Ñ'},
    'penthouses':      {'en':'Penthouses',       'es':'Penthouses',        'pt':'Coberturas',           'ru':'ÐÐµÐ½ÑÑÐ°ÑÑÑ'},
}

#──Language configs âââââââââââââââââââââââââââââââââââââââââââ
LANGS = {
    'en':{'code':'en','dir':'','hreflang':'en','og_locale':'en_US','T':{
        'nav_all':'New Developments','nav_contact':'Contact','nav_vip':'Get VIP Access',
        'hub_label':'New Developments','hub_title':'New Pre-Construction Condos in Miami',
        'hub_subtitle':"Explore the most exclusive pre-construction residences across Miami's most sought-after neighborhoods. Zero buyer commission â we work exclusively for you.",
        'hub_browse':'Browse by Neighborhood','hub_all':'All Projects',
        'hood_label':'Pre-Construction Condos','hood_other':'Other Miami Neighborhoods','hood_all_miami':'â All Miami Developments',
        'card_from':'From','card_floors':'Floors','card_units':'Residences','card_delivery':'Delivery','card_view':'View Details â',
        'cta_title':'Get Exclusive Access','cta_subtitle':'Floor plans, pricing & developer brochures â sent to your inbox.',
        'cta_name':'Full Name','cta_email':'Email Address','cta_submit':'Request Information â',
        'hub_meta_title':'New Pre-Construction Condos Miami 2025 | MiaLux Realty',
        'hub_meta_desc':'Browse all new pre-construction condos in Miami. Brickell, Miami Beach, Edgewater, Sunny Isles & more. VIP pricing, no buyer fees.',
        'hood_meta_title':'New Pre-Construction Condos in {hood} Miami 2025 | MiaLux Realty',
        'hood_meta_desc':'Discover new pre-construction condos in {hood}, Miami. Exclusive VIP pricing, full floor plans & developer info. Zero buyer commission.',
    }},
    'es':{'code':'es','dir':'es','hreflang':'es','og_locale':'es_LA','T':{
        'nav_all':'Nuevos Desarrollos','nav_contact':'Contacto','nav_vip':'Acceso VIP',
        'hub_label':'Nuevos Desarrollos','hub_title':'Nuevos Condominios en Preventa en Miami',
        'hub_subtitle':"Descubra las residencias en preventa mÃ¡s exclusivas en los vecindarios mÃ¡s codiciados de Miami. Sin comisiÃ³n para el comprador.",
        'hub_browse':'Explorar por Vecindario','hub_all':'Todos los Proyectos',
        'hood_label':'Condominios en Preventa','hood_other':'Otros Vecindarios de Miami','hood_all_miami':'â Todos los Desarrollos en Miami',
        'card_from':'Desde','card_floors':'Pisos','card_units':'Residencias','card_delivery':'Entrega','card_view':'Ver Detalles â',
        'cta_title':'Obtenga Acceso Exclusivo','cta_subtitle':'Planos, precios y brochures del desarrollador â enviados a su correo.',
        'cta_name':'Nombre Completo','cta_email':'Correo ElectrÃ³nico','cta_submit':'Solicitar InformaciÃ³n â',
        'hub_meta_title':'Nuevos Condominios en Preventa Miami 2025 | MiaLux Realty',
        'hub_meta_desc':'Explore todos los nuevos condominios en preventa en Miami. Brickell, Miami Beach, Edgewater, Sunny Isles. Precios VIP, sin comisiÃ³n.',
        'hood_meta_title':'Nuevos Condominios en Preventa en {hood} Miami | MiaLux Realty',
        'hood_meta_desc':'Descubra nuevos condominios en preventa en {hood}, Miami. Precios VIP exclusivos, planos completos. Sin comisiÃ³n.',
    }},
    'pt':{'code':'pt','dir':'pt','hreflang':'pt','og_locale':'pt_BR','T':{
        'nav_all':'Novos Empreendimentos','nav_contact':'Contato','nav_vip':'Acesso VIP',
        'hub_label':'Novos Empreendimentos','hub_title':'Novos Apartamentos na Planta em Miami',
        'hub_subtitle':"Descubra os empreendimentos mais exclusivos nos bairros mais cobiÃ§ados de Miami. Sem comissÃ£o para o comprador.",
        'hub_browse':'Explorar por Bairro','hub_all':'Todos os Projetos',
        'hood_label':'Apartamentos na Planta','hood_other':'Outros Bairros de Miami','hood_all_miami':'â Todos os Empreendimentos',
        'card_from':'A partir de','card_floors':'Andares','card_units':'ResidÃªncias','card_delivery':'Entrega','card_view':'Ver Detalhes â',
        'cta_title':'Obtenha Acesso Exclusivo','cta_subtitle':'Plantas, preÃ§os e brochures do incorporador â enviados para seu e-mail.',
        'cta_name':'Nome Completo','cta_email':'E-mail','cta_submit':'Solicitar InformaÃ§Ãµes â',
        'hub_meta_title':'Novos Apartamentos na Planta Miami 2025 | MiaLux Realty',
        'hub_meta_desc':'Explore novos apartamentos na planta em Miami. Brickell, Miami Beach, Edgewater, Sunny Isles. PreÃ§os VIP, sem comissÃ£o.',
        'hood_meta_title':'Novos Apartamentos na Planta em {hood} Miami | MiaLux Realty',
        'hood_meta_desc':'Descubra novos apartamentos na planta em {hood}, Miami. PreÃ§os VIP exclusivos, plantas completas. Sem comissÃ£o.',
    }},
    'ru':{'code':'ru','dir':'ru','hreflang':'ru','og_locale':'ru_RU','T':{
        'nav_all':'ÐÑÐµ ÐÑÐ¾ÐµÐºÑÑ','nav_contact':'ÐÐ¾Ð½ÑÐ°ÐºÑÑ','nav_vip':'VIP ÐÐ¾ÑÑÑÐ¿',
        'hub_label':'ÐÐ¾Ð²Ð¾ÑÑÑÐ¾Ð¹ÐºÐ¸','hub_title':'ÐÐ¾Ð²ÑÐµ ÐÐ¾Ð½Ð´Ð¾Ð¼Ð¸Ð½Ð¸ÑÐ¼Ñ Ð² ÐÐ°Ð¹Ð°Ð¼Ð¸',
        'hub_subtitle':"ÐÑÑÐ»ÐµÐ´ÑÐ¹ÑÐµ ÑÐ°Ð¼ÑÐµ ÑÐºÑÐºÐ»ÑÐ·Ð¸Ð²Ð½ÑÐµ Ð½Ð¾Ð²Ð¾ÑÑÑÐ¾Ð¹ÐºÐ¸ Ð² ÑÐ°Ð¼ÑÑ Ð²Ð¾ÑÑÑÐµÐ±Ð¾Ð²Ð°Ð½Ð½ÑÑ ÑÐ°Ð¹Ð¾Ð½Ð°Ñ ÐÐ°Ð¹Ð°Ð¼Ð¸. ÐÐµÐ· ÐºÐ¾Ð¼Ð¸ÑÑÐ¸Ð¸ Ð´Ð»Ñ Ð¿Ð¾ÐºÑÐ¿Ð°ÑÐµÐ»Ñ.",
        'hub_browse':'ÐÐ¾Ð¸ÑÐº Ð¿Ð¾ Ð Ð°Ð¹Ð¾Ð½Ð°Ð¼','hub_all':'ÐÑÐµ ÐÑÐ¾ÐµÐºÑÑ',
        'hood_label':'ÐÐ¾Ð²Ð¾ÑÑÑÐ¾Ð¹ÐºÐ¸','hood_other':'ÐÑÑÐ³Ð¸Ðµ Ð Ð°Ð¹Ð¾Ð½Ñ ÐÐ°Ð¹Ð°Ð¼Ð¸','hood_all_miami':'â ÐÑÐµ ÐÐ¾Ð²Ð¾ÑÑÑÐ¾Ð¹ÐºÐ¸ ÐÐ°Ð¹Ð°Ð¼Ð¸',
        'card_from':'ÐÑ','card_floors':'Ð­ÑÐ°Ð¶ÐµÐ¹','card_units':'Ð ÐµÐ·Ð¸Ð´ÐµÐ½ÑÐ¸Ð¹','card_delivery':'Ð¡Ð´Ð°ÑÐ°','card_view':'ÐÐ¾Ð´ÑÐ¾Ð±Ð½ÐµÐµ â',
        'cta_title':'ÐÐ¾Ð»ÑÑÐ¸ÑÑ Ð­ÐºÑÐºÐ»ÑÐ·Ð¸Ð²Ð½ÑÐ¹ ÐÐ¾ÑÑÑÐ¿','cta_subtitle':'ÐÐ»Ð°Ð½Ð¸ÑÐ¾Ð²ÐºÐ¸, ÑÐµÐ½Ñ Ð¸ Ð±ÑÐ¾ÑÑÑÑ Ð·Ð°ÑÑÑÐ¾Ð¸ÑÐ¸ÐºÐ° â Ð½Ð° Ð²Ð°ÑÑ Ð¿Ð¾ÑÑÑ.',
        'cta_name':'ÐÐ¾Ð»Ð½Ð¾Ðµ ÐÐ¼Ñ','cta_email':'Email','cta_submit':'ÐÐ°Ð¿ÑÐ¾ÑÐ¸ÑÑ ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ â',
        'hub_meta_title':'ÐÐ¾Ð²ÑÐµ ÐÐ¾Ð½Ð´Ð¾Ð¼Ð¸Ð½Ð¸ÑÐ¼Ñ Ð² ÐÐ°Ð¹Ð°Ð¼Ð¸ 2025 | MiaLux Realty',
        'hub_meta_desc':'ÐÑÐµ Ð½Ð¾Ð²ÑÐµ ÐºÐ¾Ð½Ð´Ð¾Ð¼Ð¸Ð½Ð¸ÑÐ¼Ñ Ð² ÐÐ°Ð¹Ð°Ð¼Ð¸. ÐÑÐ¸ÐºÐµÐ»Ð», ÐÐ°Ð¹Ð°Ð¼Ð¸ ÐÐ¸Ñ, Ð­Ð´Ð¶ÑÐ¾ÑÐµÑ, Ð¡Ð°Ð½Ð½Ð¸-ÐÐ¹Ð»Ñ. VIP-ÑÐµÐ½Ñ, Ð±ÐµÐ· ÐºÐ¾Ð¼Ð¸ÑÑÐ¸Ð¸.',
        'hood_meta_title':'ÐÐ¾Ð²Ð¾ÑÑÑÐ¾Ð¹ÐºÐ¸ Ð² {hood} ÐÐ°Ð¹Ð°Ð¼Ð¸ | MiaLux Realty',
        'hood_meta_desc':'ÐÐ¾Ð²ÑÐµ ÐºÐ¾Ð½Ð´Ð¾Ð¼Ð¸Ð½Ð¸ÑÐ¼Ñ Ð² {hood}, ÐÐ°Ð¹Ð°Ð¼Ð¸. Ð­ÐºÑÐºÐ»ÑÐ·Ð¸Ð²Ð½ÑÐµ VIP-ÑÐµÐ½Ñ, Ð¿Ð¾Ð»Ð½ÑÐµ Ð¿Ð»Ð°Ð½Ð¸ÑÐ¾Ð²ÐºÐ¸. ÐÐµÐ· ÐºÐ¾Ð¼Ð¸ÑÑÐ¸Ð¸.',
    }},
}

#──Helpers ââââââââââââââââââââââââââââââââââââââââââââââââââââ
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

#──Schema generators ââââââââââââââââââââââââââââââââââââââââââ
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

#──Load templates âââââââââââââââââââââââââââââââââââââââââââââ
with open('hub-template.html')     as f: HUB_T  = f.read()
with open('hood-template.html')    as f: HOOD_T = f.read()
with open('landing-template.html') as f: LAND_T = f.read()

# All hoods per category (include all HOOD_META for new-developments)
all_hoods_by_cat = {}
for cat, hoods in by_cat_hood.items():
    all_hoods_by_cat[cat] = list(hoods.keys())
all_hoods_by_cat['new-developments'] = list(set(
    all_hoods_by_cat.get('new-developments',[]) + list(HOOD_META.keys())))

# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# HUB PAGES
# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
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
        '{{T_HUB_BROWSE}}':T['hub_browse'],'{{T_HUB_ALL_LISTINGS}}':T['hub_all'],'{{T_HUB_SEE_ALL}}':T['hub_all']+' â',
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
    print(f"  â {out}")

# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# NEIGHBORHOOD PAGES
# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
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
    print(f"  â {lc}: {len(all_hoods_by_cat.get(cat,[]))} neighborhood pages")

# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# LISTING PAGES
# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
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
    print(f"  â {lc}: {len(LISTINGS)} listing pages")

# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# SITEMAP
# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
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
with open('sitemap.xml','w') as f: f.write(sitemap)
print(f"  â sitemap.xml: {len(urls)} URLs")

# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# _REDIRECTS
# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
lines = ["# MiaLux Realty â _redirects v3","# Auto-generated â do not edit manually","",
         "#──Legacy root listing slugs â new 3-level structure (301) ââ"]

OLD_SLUGS = {
    'cipriani-residences-brickell':       ('new-developments','brickell','cipriani-residences'),
    'ora-by-casa-tua':                    ('new-developments','brickell','ora-by-casa-tua'),
    'st-regis-residences-sunny-isles':    ('new-developments','sunny-isles-beach','st-regis-residences'),
    'residences-1428-brickell':           ('new-developments','brickell','1428-residences'),
    'mandarin-oriental-residences-miami': ('new-developments','brickell-key','mandarin-oriental-residences'),
    'faena-residences-miami':             ('new-developments','downtown-miami','faena-residences'),
}
for old,(cat,hood,pslug) in OLD_SLUGS.items():
    lines += [f"/{old}  /{cat}/{hood}/{pslug}/  301",
              f"/{old}/  /{cat}/{hood}/{pslug}/  301"]

lines += ["","#──Legacy hub/catalog URLs ââ",
          "/miami-pre-construction-condos  /new-developments/  301",
          "/miami-pre-construction-condos/  /new-developments/  301",
          "/developments  /new-developments/  301",
          "/developments/  /new-developments/  301",
          "","#──Clean URL rewrites (200) ââ"]

for cat in ALL_CATEGORIES:
    for lc,l in LANGS.items():
        d = l['dir']
        p = f"/{d}/{cat}" if d else f"/{cat}"
        lines += [f"{p}  {p}/index.html  200", f"{p}/  {p}/index.html  200"]
    for hs in all_hoods_by_cat.get(cat,[]):
        for lc,l in LANGS.items():
            d = l['dir']
            p = f"/{d}/{cat}/{hs}" if d else f"/{cat}/{hs}"
            lines += [f"{p}  {p}/index.html  200", f"{p}/  {p}/index.html  200"]
    for listing in [x for x in LISTINGS if x['category']==cat]:
        hood  = listing['_hood_slug']
        pslug = listing['page_slug']
        for lc,l in LANGS.items():
            d = l['dir']
            p = f"/{d}/{cat}/{hood}/{pslug}" if d else f"/{cat}/{hood}/{pslug}"
            lines += [f"{p}  {p}/index.html  200", f"{p}/  {p}/index.html  200"]

with open('_redirects','w') as f: f.write('\n'.join(lines))
print(f"  â _redirects: {len([x for x in lines if x and not x.startswith('#')])} rules")

with open('robots.txt','w') as f:
    f.write("# âââââââââââââââââââââââââââââââââââââââââââââ\n# MiaLux Realty â robots.txt\n# STATUS: DEVELOPMENT MODE â all crawlers blocked\n# â  When going live, replace with the PRODUCTION version below\n# âââââââââââââââââââââââââââââââââââââââââââââ\n\nUser-agent: *\nDisallow: /\n\n# âââââââââââââââââââââââââââââââââââââââââââââ\n# PRODUCTION VERSION (use when ready to go live)\n# âââââââââââââââââââââââââââââââââââââââââââââ\n# User-agent: *\n# Allow: /\n# Disallow: /admin/\n#\n# Sitemap: https://mialuxrealty.com/sitemap.xml\n# âââââââââââââââââââââââââââââââââââââââââââââ\n")
print("  â robots.txt")

# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
# SUMMARY
# ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
total_hood_pages = len(LANGS)*sum(len(v) for v in all_hoods_by_cat.values())
print(f"""
âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
â  BUILD COMPLETE v3  â  Clean 3-level URL structure            â
â ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ£
â  Hub pages           {len(LANGS)*len(ALL_CATEGORIES):>4}                                    â
â  Neighborhood pages  {total_hood_pages:>4}                                    â
â  Listing pages       {len(LANGS)*len(LISTINGS):>4}                                    â
â  Sitemap URLs        {len(urls):>4}                                    â
â ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ£
â  /new-developments/brickell/cipriani-residences/   â EN       â
â  /es/new-developments/brickell/cipriani-residences/ â ES      â
â  Root folder: CLEAN                                           â
â  Legacy slugs: 301 redirected                                 â
â  Future: /villas/ /penthouses/ ready to add                   â
âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
""")
