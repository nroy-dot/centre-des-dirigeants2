# SEO et GEO : métadonnées, données structurées, fichiers pour robots et moteurs génératifs
import json

BASE = "https://www.centredesdirigeants.ca/"
ORG_ID = BASE + "#organisation"
OG = BASE + "img/og-centre-des-dirigeants.jpg"

def url(f):
    return BASE if f == "index.html" else BASE + f

SEO = {
    "index.html": {
        "t": "Centre des dirigeants | Experts pour dirigeants, Gatineau",
        "d": "Un réseau d’experts réunis à Gatineau pour les dirigeants d’entreprises et d’organisations : stratégie, finances, RH, crise, médiation, santé mentale, IA. Une seule prise de contact.",
        "nom": "Accueil",
    },
    "continuum.html": {
        "t": "Prévention, Urgence, Reconstruction | Centre des dirigeants",
        "d": "Le continuum PUR : comment le Centre des dirigeants accompagne les entreprises et les organisations avant, pendant et après une crise, sans oublier la personne qui dirige.",
        "nom": "Le continuum PUR",
    },
    "expertises.html": {
        "t": "Expertises pour dirigeants : stratégie, RH, finances, IA",
        "d": "Stratégie, CFO à la demande, RH, communications de crise, médiation, santé mentale, protection des données, IA, sondages et tests AtmanPro.",
        "nom": "Expertises et outils",
    },
    "experts.html": {
        "t": "Les experts du Centre des dirigeants | Gatineau",
        "d": "France Bélisle, Nicolas Roy, Yannick Beaulieu, Andréanne Thibault, Chantal Dufort, Daniel Feeny et les autres experts du Centre des dirigeants.",
        "nom": "Les experts",
    },
    "demarche.html": {
        "t": "Comment ça fonctionne et FAQ | Centre des dirigeants",
        "d": "Une seule prise de contact, une mise en relation avec les bons experts, un accompagnement ponctuel ou durable. Réponses aux questions des dirigeants.",
        "nom": "La démarche",
    },
    "contact.html": {
        "t": "Nous écrire | Centre des dirigeants, Gatineau",
        "d": "Exposez votre situation au Centre des dirigeants. Une personne lit chaque demande et vous met en relation avec les experts pertinents.",
        "nom": "Nous écrire",
    },
}

def org(EXPERTS, EXPERTISES):
    fondateurs = [{"@type": "Person", "@id": BASE + "experts.html#nicolas-roy", "name": "Nicolas Roy"},
                  {"@type": "Person", "@id": BASE + "experts.html#france-belisle", "name": "France Bélisle"}]
    return {
        "@type": ["Organization", "ProfessionalService"],
        "@id": ORG_ID,
        "name": "Centre des dirigeants",
        "url": BASE,
        "logo": BASE + "img/icone-512.png",
        "image": OG,
        "slogan": "Les bonnes expertises. Au bon moment.",
        "description": "Réseau de collaborateurs experts qui accompagne les dirigeants d’entreprises et d’organisations en prévention, en situation d’urgence et en reconstruction, à partir d’une seule prise de contact.",
        "email": "info@centredesdirigeants.ca",
        "foundingDate": "2026-11",
        "founder": fondateurs,
        "parentOrganization": {"@type": "Organization", "name": "Posture Inc.", "url": "https://www.postureinc.ca/"},
        "address": {"@type": "PostalAddress", "addressLocality": "Gatineau", "addressRegion": "QC", "addressCountry": "CA"},
        "areaServed": [{"@type": "City", "name": "Gatineau"}, {"@type": "AdministrativeArea", "name": "Outaouais"}, {"@type": "AdministrativeArea", "name": "Québec"}],
        "audience": {"@type": "BusinessAudience", "audienceType": "Dirigeants d’entreprises et d’organisations"},
        "knowsLanguage": "fr-CA",
        "knowsAbout": [t for t, *_ in EXPERTISES] + ["Gestion de crise", "Gouvernance", "Coaching de dirigeants", "Planification stratégique"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Expertises du Centre des dirigeants",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d}} for t, d, _ in EXPERTISES]},
    }

def personnes(EXPERTS):
    out = []
    for s, n, cred, role, desc, tags in EXPERTS:
        p = {"@type": "Person", "@id": BASE + "experts.html#" + s, "name": n,
             "image": BASE + "img/" + s + ".webp", "description": desc,
             "jobTitle": role, "knowsAbout": tags, "memberOf": {"@id": ORG_ID}}
        if cred:
            p["honorificSuffix"] = cred
        out.append(p)
    return out

def jsonld(fichier, titre, description, EXPERTS, EXPERTISES, FAQ):
    g = [org(EXPERTS, EXPERTISES)]
    page = {"@type": "WebPage", "@id": url(fichier) + "#page", "url": url(fichier), "name": titre,
            "description": description, "inLanguage": "fr-CA", "isPartOf": {"@id": BASE + "#site"},
            "about": {"@id": ORG_ID}, "primaryImageOfPage": OG}
    if fichier == "index.html":
        g.append({"@type": "WebSite", "@id": BASE + "#site", "url": BASE, "name": "Centre des dirigeants",
                  "inLanguage": "fr-CA", "publisher": {"@id": ORG_ID}})
    else:
        g.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": SEO[fichier]["nom"], "item": url(fichier)}]})
    if fichier == "experts.html":
        page["@type"] = "CollectionPage"
        page["mainEntity"] = {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": p} for i, p in enumerate(personnes(EXPERTS))]}
    if fichier == "demarche.html":
        page["@type"] = ["WebPage", "FAQPage"]
        page["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ]
    if fichier == "contact.html":
        page["@type"] = "ContactPage"
    g.append(page)
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, indent=1)

def tete(fichier, titre, description, EXPERTS, EXPERTISES, FAQ):
    s = SEO[fichier]; t = s["t"]; d = s["d"]; u = url(fichier)
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{u}">
<link rel="alternate" hreflang="fr-CA" href="{u}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#0C283A">
<meta name="author" content="Centre des dirigeants">
<meta name="geo.region" content="CA-QC">
<meta name="geo.placename" content="Gatineau">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_CA">
<meta property="og:site_name" content="Centre des dirigeants">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{OG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Centre des dirigeants : Les bonnes expertises. Au bon moment.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{OG}">
<link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preload" href="fonts/LeagueSpartan-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/LeagueSpartan-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/style.css">
<script type="application/ld+json">
{jsonld(fichier, t, d, EXPERTS, EXPERTISES, FAQ)}
</script>'''

def fichiers_robots(out, pages, EXPERTS, EXPERTISES, FAQ):
    import os, datetime
    j = datetime.date(2026, 11, 7).isoformat()
    prio = {"index.html": "1.0", "experts.html": "0.9", "expertises.html": "0.9", "continuum.html": "0.8", "demarche.html": "0.8", "contact.html": "0.7"}
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{url(p)}</loc><lastmod>{j}</lastmod><priority>{prio[p]}</priority></url>\n" for p in pages) + "</urlset>\n"
    open(os.path.join(out, "sitemap.xml"), "w", encoding="utf-8").write(sm)
    robots = f"""# Centre des dirigeants
User-agent: *
Allow: /

# Moteurs génératifs et assistants : bienvenus
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /

Sitemap: {BASE}sitemap.xml
"""
    open(os.path.join(out, "robots.txt"), "w", encoding="utf-8").write(robots)
    ex = "\n".join(f"- {n}{', ' + c if c else ''} ({r}) : {d}" for s, n, c, r, d, t in EXPERTS)
    exp = "\n".join(f"- {t} : {d} Experts : {q}." for t, d, q in EXPERTISES)
    faq = "\n\n".join(f"### {q}\n{r}" for q, r in FAQ)
    llms = f"""# Centre des dirigeants

> Réseau de neuf collaborateurs experts, basé à Gatineau (Québec), qui accompagne les dirigeants d’entreprises et d’organisations. Une seule prise de contact permet d’exposer sa situation et d’être orienté vers les bonnes expertises. Slogan : « Les bonnes expertises. Au bon moment. »

## Faits essentiels
- Nom : Centre des dirigeants
- Lancement : novembre 2026, à Gatineau, Québec, Canada
- Cofondateurs : France Bélisle et Nicolas Roy (Adm.A., CRHA), coprésidents de Posture Inc.
- Clientèle : dirigeants d’entreprises et d’organisations, surtout des PME, mais aussi des OBNL et de grandes organisations
- Territoire : Gatineau, Outaouais et Québec
- Accès : une seule prise de contact auprès de la coordination du Centre, à info@centredesdirigeants.ca
- Modèle : accompagnement ponctuel ou dans la durée, selon les besoins
- Approche : le continuum PUR (Prévention, Urgence, Reconstruction)

## Le continuum PUR
- Prévention : clarifier les priorités, renforcer les pratiques et anticiper les enjeux.
- Urgence : établir les priorités et mobiliser rapidement les bonnes expertises.
- Reconstruction : rétablir le dialogue, consolider les équipes et préparer la suite.
Le continuum tient compte autant des besoins de l’organisation que de la réalité de la personne qui la dirige.

## Expertises
{exp}

## Outils
- Tests psychométriques AtmanPro
- Sondages internes et externes conçus sur mesure
- Adhésion (marque employeur)
- Planification stratégique, coaching de gestion, médiation

## Experts
{ex}

## Questions fréquentes
{faq}

## Pages
- [Accueil]({BASE})
- [Le continuum PUR]({BASE}continuum.html)
- [Expertises et outils]({BASE}expertises.html)
- [Les experts]({BASE}experts.html)
- [La démarche et FAQ]({BASE}demarche.html)
- [Nous écrire]({BASE}contact.html)
"""
    open(os.path.join(out, "llms.txt"), "w", encoding="utf-8").write(llms)
