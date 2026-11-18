#!/usr/bin/env python3
"""Site multipage du Centre des dirigeants (9 pages)."""
import os, re, json, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
src = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
ns = {}
for nom in ["EXPERTS", "EXPERTISES", "FAQ"]:
    exec(re.search(rf"^{nom} = \[.*?^\]", src, re.S | re.M).group(0), ns)
EXPERTS, EXPERTISES, FAQ = ns["EXPERTS"], ns["EXPERTISES"], ns["FAQ"]
exec(open(os.path.join(HERE, "seo.py"), encoding="utf-8").read())
MAIL = "info@centredesdirigeants.ca"
EXPD = {s: dict(n=n, c=c, r=r, d=d, t=t) for s, n, c, r, d, t in EXPERTS}

# ======================================================================
# AGENDA : ajouter ici les activités. Les activités passées disparaissent
# automatiquement du site. Types : conference, formation, cercle, evenement
# Exemple :
# {"titre": "Gérer une crise médiatique en 72 heures", "type": "formation",
#  "date": "2026-12-03", "fin": "2026-12-03", "heure": "8 h 30 à 11 h 30",
#  "lieu": "Gatineau", "experts": ["france-belisle"],
#  "desc": "Atelier pratique pour dirigeants.",
#  "lien": "https://..."}
# ======================================================================
EVENTS = [
    {"titre": "Gala Excelor 2026 de la Chambre de commerce de Gatineau", "type": "evenement",
     "date": "2026-11-14", "heure": "Dès 16 h 30",
     "lieu": "Palais des congrès de Gatineau", "adresse": "50, boulevard Maisonneuve, Gatineau",
     "experts": ["france-belisle", "nicolas-roy", "marc-antoine-laramee", "sophie-ann-bellisle", "yannick-beaulieu", "marie-eve-venner"],
     "desc": "L’équipe du Centre était présente à la 30e édition du Gala Excelor, qui célèbre l’excellence des entreprises et des organisations de Gatineau et des Collines.",
     "lien": "https://ccgatineau.ca/evenement/gala-excelor"},
    {"titre": "Quand on a l’impression de ne jamais en faire assez", "type": "formation",
     "date": "2026-11-26", "heure": "12 h à 12 h 45", "lieu": "En ligne, sur Zoom", "en_ligne": True,
     "experts": ["chantal-dufort"],
     "desc": "Pourquoi certaines personnes veulent toujours en faire plus sans jamais être satisfaites, et comment fixer la ligne d’arrivée avant l’épuisement. Des stratégies simples, à essayer tout de suite.",
     "note": "Formation gratuite. 30 minutes de contenu et 15 minutes de questions. Enregistrement offert pendant 72 heures.",
     "lien": "https://chantaldufort.com/services/limpression-de-ne-jamais-en-faire-assez/"},
]

TYPES_EV = {"conference": "Conférence", "formation": "Formation", "cercle": "Cercle de pairs", "evenement": "Événement"}
MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]

CARTE = {"Stratégie et gouvernance": ["nicolas-roy", "france-belisle", "daniel-feeny"], "Direction financière et rentabilité": ["yannick-beaulieu"],
         "Ressources humaines": ["nicolas-roy", "andreanne-thibault"], "Communications": ["france-belisle", "daniel-feeny"],
         "Sondages internes et externes": ["nicolas-roy", "andreanne-thibault", "daniel-feeny"], "Tests psychométriques": ["nicolas-roy", "andreanne-thibault"],
         "Médiation": ["france-belisle"], "Santé mentale au travail": ["chantal-dufort"],
         "Protection des données": ["sophie-ann-bellisle"], "Intelligence artificielle": ["marc-antoine-laramee"]}
SITUATIONS = {
    "Stratégie et gouvernance": ["Votre plan stratégique dort dans un tiroir.", "Le rôle du conseil et celui de la direction se chevauchent.", "La croissance dépasse la structure."],
    "Direction financière et rentabilité": ["Vous manquez de visibilité sur vos liquidités.", "Un projet de financement se prépare.", "Certaines activités coûtent plus qu’elles ne rapportent."],
    "Ressources humaines": ["Un départ clé fragilise l’équipe.", "Le recrutement ne suit plus.", "La culture s’effrite avec la croissance."],
    "Communications": ["Une crise médiatique éclate.", "Un dossier exige des relations gouvernementales.", "Un changement important doit être annoncé."],
    "Sondages internes et externes": ["Vous voulez mesurer le climat avant de décider.", "Vous voulez connaître la perception de vos clients.", "Vous devez évaluer les risques psychosociaux."],
    "Tests psychométriques": ["Un poste de gestion est à combler.", "Une équipe de direction se compose ou se recompose.", "Un gestionnaire veut mieux se connaître."],
    "Médiation": ["Deux associés ne se parlent plus.", "Un conflit paralyse une équipe.", "Une plainte exige une démarche neutre."],
    "Santé mentale au travail": ["Des signes d’épuisement apparaissent.", "Les gestionnaires manquent d’outils.", "Un événement difficile a secoué l’équipe."],
    "Protection des données": ["Vos obligations de la Loi 25 restent floues.", "Un incident de confidentialité est survenu.", "Un nouveau système traite des renseignements personnels."],
    "Intelligence artificielle": ["Vous voulez gagner du temps sans risque.", "Des employés utilisent déjà l’IA sans cadre.", "Vous cherchez où l’IA peut vraiment aider."],
}
ENJJ = [{"t": t, "d": d, "e": CARTE[t]} for t, d, _ in EXPERTISES]

MARQUE = '<svg class="mq" viewBox="0 0 40 40" aria-hidden="true"><path d="M19 4a14 14 0 0 0 0 28z" fill="currentColor"/><path d="M21 8a14 14 0 0 1 0 28z" fill="#D5AC59"/></svg>'
NAV = [("fonctionnement.html", "Comment ça fonctionne"), ("expertises.html", "Expertises"), ("experts.html", "Les experts"),
       ("communaute.html", "Communauté"), ("ressources.html", "Ressources"), ("agenda.html", "Agenda")]

def url(f): return BASE if f == "index.html" else BASE + f

def img(n, alt, sizes="(max-width:820px) 92vw, 45vw", lazy=True, cls="", extra=""):
    return (f'<img src="img/{n}-1400.webp" srcset="img/{n}-800.webp 800w, img/{n}-1400.webp 1400w" sizes="{sizes}" alt="{alt}"'
            + (' loading="lazy"' if lazy else ' fetchpriority="high"') + (f' class="{cls}"' if cls else "") + extra + ">")

def faces(ss, size=44):
    return "".join(f'<img src="img/{s}.webp" alt="{EXPD[s]["n"]}" title="{EXPD[s]["n"]}" width="{size}" height="{size}">' for s in ss)

def head(f, titre, desc, ld_extra=None, typepage="WebPage", nom=None, bc=None):
    g = [org(EXPERTS, EXPERTISES)]
    if f == "index.html":
        g.append({"@type": "WebSite", "@id": BASE + "#site", "url": BASE, "name": "Centre des dirigeants", "inLanguage": "fr-CA", "publisher": {"@id": ORG_ID}})
    else:
        chemin = bc or [("Accueil", "index.html"), (nom, f)]
        g.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n_, "item": url(h_)} for i, (n_, h_) in enumerate(chemin)]})
    page = {"@type": typepage, "@id": url(f) + "#page", "url": url(f), "name": titre, "description": desc, "inLanguage": "fr-CA",
            "isPartOf": {"@id": BASE + "#site"}, "about": {"@id": ORG_ID}}
    if ld_extra: page.update(ld_extra)
    g.append(page)
    ld = json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False)
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url(f)}">
<link rel="alternate" hreflang="fr-CA" href="{url(f)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#0C283A">
<meta name="geo.region" content="CA-QC"><meta name="geo.placename" content="Gatineau">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_CA"><meta property="og:site_name" content="Centre des dirigeants">
<meta property="og:title" content="{titre}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url(f)}">
<meta property="og:image" content="{OG}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{titre}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{OG}">
<link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png"><link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preload" href="fonts/LeagueSpartan-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.css">
<script type="application/ld+json">{ld}</script>'''

def entete(f, solide=False):
    liens = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == f else ""}>{t}</a>' for h, t in NAV)
    return f'''<header class="hd{' solide' if solide else ''}"><div class="w">
  <a href="index.html" aria-label="Centre des dirigeants, accueil"><img src="img/logo.png" alt="Centre des dirigeants" width="900" height="330"></a>
  <button class="menu" type="button" aria-label="Menu" aria-expanded="false"><span></span></button>
  <nav aria-label="Navigation principale">{liens}<a class="btn" href="contact.html"{" aria-current=\"page\"" if f == "contact.html" else ""}>Demander une invitation <span class="fl">→</span></a></nav>
</div></header>
<button class="pause" id="pause" type="button" aria-pressed="false"><span class="ic" aria-hidden="true"></span><span class="tx">Mettre les animations en pause</span></button>'''

NL_PIED = f'''<div class="nl-pied" id="infolettre">
      <div><span class="eb clair">{MARQUE} L’infolettre du Centre</span><h3>ENTRE <span>NOUS</span></h3><p>Une réflexion par édition, écrite pour les dirigeants.</p></div>
      <div>
        <form class="f-nl" novalidate>
          <div class="nl-ligne"><label for="nl-courriel-pied" class="sr">Courriel</label><input type="email" id="nl-courriel-pied" name="courriel" autocomplete="email" placeholder="Votre courriel" required><button class="btn or" type="submit">Je m’abonne <span class="fl">→</span></button></div>
          <div class="pot" aria-hidden="true"><input name="site_web" tabindex="-1" autocomplete="off" aria-label="site"></div>
          <label class="consent"><input type="checkbox" name="ok" value="oui"> <span>J’accepte de recevoir ENTRE NOUS par courriel. Je peux me désabonner en tout temps. <a href="politique-confidentialite.html">Confidentialité</a></span></label>
          <p class="err" role="alert"></p>
        </form>
        <p class="nl-ok" role="status">Merci. Vous recevrez la prochaine édition d’ENTRE NOUS.</p>
      </div>
    </div>'''
PIED = f'''<footer class="pied2">
  <div class="w">
    %%NL%%
    <div class="pg">
      <div><img src="img/logo.png" alt="Centre des dirigeants" width="900" height="330"><p>Un réseau d’experts et une communauté de pairs pour les dirigeants d’entreprises et d’organisations. Les bonnes expertises. Au bon moment.</p></div>
      <div><h4>Le Centre</h4><a href="fonctionnement.html">Comment ça fonctionne</a><a href="expertises.html">Expertises</a><a href="experts.html">Les experts</a><a href="communaute.html">Communauté</a></div>
      <div><h4>Rester proches</h4><a href="ressources.html">Ressources</a><a href="agenda.html">Agenda</a><a href="ressources.html#entre-nous">Infolettre ENTRE NOUS</a></div>
      <div><h4>Nous joindre</h4><a href="contact.html">Écrire au Centre</a><span>{MAIL}</span><span>Gatineau, Québec</span></div>
    </div>
    <div class="pb"><span>© 2026 Centre des dirigeants. Une initiative de Posture Inc.</span><a href="politique-confidentialite.html">Politique de confidentialité</a></div>
  </div>
</footer>'''

def page(f, titre, desc, corps, nom=None, ld_extra=None, typepage="WebPage", solide=False, scripts="", bc=None, nav_actif=None):
    html = f'''<!DOCTYPE html>
<html lang="fr-CA">
<head>
{head(f, titre, desc, ld_extra, typepage, nom, bc)}
</head>
<body>
<a class="sauter" href="#contenu">Aller au contenu</a>
{entete(nav_actif or f, solide)}
<main id="contenu">
{corps}
</main>
{PIED.replace("%%NL%%", "" if f == "ressources.html" else NL_PIED)}
{scripts}<script src="js/site.js" defer></script>
</body>
</html>
'''
    open(os.path.join(OUT, f), "w", encoding="utf-8").write(html)

def ph(f, nom, eb, h1, lead, photo, alt):
    return f'''<section class="ph">
  <picture>{img(photo, alt, "100vw", lazy=False)}</picture>
  <div class="voile" aria-hidden="true"></div>
  <div class="w">
    <nav class="fil" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span aria-hidden="true">/</span><span aria-current="page">{nom}</span></nav>
    <span class="eb clair">{MARQUE} {eb}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>'''

def cta(titre="Demandez votre invitation.", texte="Le Centre est réservé aux clients de nos collaborateurs. Présentez-vous en quelques lignes : la coordination vous répond en 24 heures ouvrables.", btn="Demander une invitation", lien="contact.html#formulaire", photo="bureau-sourire"):
    return f'''<section class="fin" aria-label="Appel à l’action">
  <div class="w g">
    <div>
      <span class="eb">{MARQUE} Accès sur invitation</span>
      <h2 class="cta-t">{titre}</h2>
      <p style="margin-top:22px">{texte}</p>
      <div style="margin-top:30px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="{lien}">{btn} <span class="fl">→</span></a></div>
    </div>
    <figure class="fin-photo ap">{img(photo, "")}</figure>
  </div>
</section>'''

def infolettre(id_=""):
    return f'''<section class="sec" {('id="'+id_+'"') if id_ else ''} style="padding-top:0">
  <div class="w">
    <div class="infolettre ap">
      <div>
        <span class="eb clair">{MARQUE} L’infolettre du Centre</span>
        <h2 style="margin-top:16px">ENTRE <span>NOUS</span></h2>
        <p>Une réflexion par édition, écrite pour les dirigeants.</p>
        <ul><li>Un seul thème, traité en profondeur</li><li>Un outil à rapporter à votre équipe</li><li>Les prochaines activités du Centre</li></ul>
      </div>
      <div>
        <form class="f-nl" novalidate>
          <label for="nl-prenom{id_}">Prénom</label><input type="text" id="nl-prenom{id_}" name="prenom" autocomplete="given-name">
          <label for="nl-courriel{id_}">Courriel</label><input type="email" id="nl-courriel{id_}" name="courriel" autocomplete="email" required>
          <div class="pot" aria-hidden="true"><input name="site_web" tabindex="-1" autocomplete="off" aria-label="site"></div>
          <label class="consent"><input type="checkbox" name="ok" value="oui"> <span>J’accepte de recevoir ENTRE NOUS par courriel. Je peux me désabonner en tout temps. <a href="politique-confidentialite.html">Confidentialité</a></span></label>
          <div><button class="btn" type="submit">Je m’abonne <span class="fl">→</span></button></div>
          <p class="err" role="alert"></p>
        </form>
        <p class="nl-ok" role="status">Merci. Vous recevrez la prochaine édition d’ENTRE NOUS.</p>
      </div>
    </div>
  </div>
</section>'''

def faq_html(items):
    return "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><p>{r}</p></details>' for q, r in items)

def faq_ld(items):
    return {"mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in items]}

PUR = [
    ("p", "01", "Prévention.", "Tout va bien. C’est justement le moment.", "Clarifier les priorités et renforcer les pratiques avant que les enjeux deviennent des urgences.",
     ["Votre organisation grandit plus vite que sa structure.", "Votre plan stratégique ou votre gouvernance mérite un regard extérieur.", "Vos obligations en santé psychologique ou en protection des données restent floues."],
     ["nicolas-roy", "sophie-ann-bellisle", "chantal-dufort", "marc-antoine-laramee"], "planification", "Planification calme entre collègues"),
    ("u", "02", "Urgence.", "Ça brûle. Il faut les bonnes personnes, maintenant.", "Mobiliser rapidement les bonnes expertises quand la situation déborde.",
     ["Une crise médiatique, financière ou humaine vient d’éclater.", "Un départ clé, un conflit ou une plainte déstabilise l’organisation.", "Une décision ne peut plus attendre et repose sur vos épaules."],
     ["france-belisle", "yannick-beaulieu", "daniel-feeny", "chantal-dufort"], "reunion-direction", "Réunion de direction mobilisée"),
    ("r", "03", "Reconstruction.", "Le pire est passé. Reste à reconstruire.", "Rétablir la confiance, consolider les équipes et préparer la suite.",
     ["La confiance s’est effritée entre la direction et les équipes.", "Vous devez restructurer après une période difficile.", "Vous-même avez besoin de reprendre votre souffle."],
     ["france-belisle", "andreanne-thibault", "nicolas-roy"], "equipe-applaudit", "Équipe qui célèbre un succès"),
]

ORG = {"france-belisle": "Posture Inc.", "nicolas-roy": "Posture Inc.", "andreanne-thibault": "Adhésion", "yannick-beaulieu": "Votre Partenaire CFO", "chantal-dufort": "Chantal Dufort Inc.", "daniel-feeny": "Feeny Corp.", "sophie-ann-bellisle": "Privacense", "marc-antoine-laramee": "Quartier AI", "marie-eve-venner": "Centre des dirigeants"}
DATA_EXP = f'<script>window.CDD_EXP={json.dumps({s: {"n": d["n"], "c": d["c"], "r": d["r"], "d": d["d"], "o": ORG.get(s, "")} for s, d in EXPD.items()}, ensure_ascii=False)};window.CDD_ENJ={json.dumps(ENJJ, ensure_ascii=False)};</script>\n'

def constellation(lien=""):
    return f'''<div class="res-t">
      <div><span class="eb clair">{MARQUE} Le réseau</span><h2 class="grand clair">Choisissez un enjeu. <em>Voyez qui s’allume.</em></h2></div>
      <div><p style="margin-bottom:16px;color:#C9D6E0">Chaque point est un expert du réseau. Survolez-le pour le découvrir, cliquez pour voir son profil.</p><div class="chips" id="chips"></div><p class="chip-d" id="chipd" aria-live="polite"></p></div>
    </div>
    <div class="ciel" id="ciel" data-lien="{lien}"><canvas aria-hidden="true"></canvas><div class="fiche" id="fiche" aria-live="polite"></div></div>'''

# =============================== ACCUEIL ===============================
def pic_d(n, cls, prio):
    return (f'<picture class="{cls}"><source media="(max-width:700px)" srcset="img/{n}-port.webp">'
            f'<img src="img/{n}-1400.webp" srcset="img/{n}-800.webp 800w, img/{n}-1400.webp 1400w, img/{n}.webp 2400w" sizes="100vw" alt=""'
            + (' fetchpriority="high"' if prio else ' loading="lazy"') + '></picture>')
ruban = "".join(f"<span>{t}</span>{MARQUE}" for t in ["Stratégie", "Gouvernance", "Finances", "Ressources humaines", "Communications de crise", "Affaires publiques", "Médiation", "Santé mentale au travail", "Protection des données", "Intelligence artificielle"])
B1 = ["conversation-cafe", "deux-collegues", "cafe-equipe", "trio-portable", "complicite", "appel"]
B2 = ["duo-portable", "collaboration", "equipe-concentree", "planification", "equipe-reseau", "bureau-sourire"]
bande = lambda L: "".join(f'<img src="img/{n}-p.webp" alt="" loading="lazy" width="640" height="427">' for n in L)
FAQ_ACC = [FAQ[0], FAQ[2], FAQ[4], FAQ[6]]

accueil = f'''
<section class="hero2" aria-label="Accueil">
  <div class="diapos" aria-hidden="true">{pic_d("dirigeant-explique","diapo on",True)}{pic_d("dirigeante-ecoute","diapo",False)}{pic_d("equipe-concentree","diapo",False)}</div>
  <div class="voile" aria-hidden="true"></div>
  <div class="w h2c">
    <span class="eb clair">{MARQUE} Réseau d’experts au service des dirigeants</span>
    <h1><span class="l"><span>Les bonnes</span></span><span class="l"><span>expertises.</span></span><span class="l"><span class="o">Au bon moment.</span></span></h1>
    <div class="bas">
      <p>Un réseau d’experts de confiance et une communauté de pairs, réservés aux clients de nos collaborateurs.</p>
      <div class="tete-bas"><div class="pile-v">{faces([s for s,*_ in EXPERTS],52)}</div><a class="btn or" href="contact.html#formulaire">Demander une invitation <span class="fl">→</span></a></div>
    </div>
  </div>
  <div class="compteur-d" aria-hidden="true"><i class="on"></i><i></i><i></i></div>
</section>
<div class="ruban" aria-hidden="true"><div class="p">{ruban}{ruban}</div></div>

<section class="reseau" id="experts">
  <div class="w">{constellation("pages")}
    <div class="ap" style="margin-top:30px"><a class="btn or" href="experts.html">Rencontrer les experts <span class="fl">→</span></a></div>
  </div>
</section>


<section class="sec">
  <div class="w">
    <span class="eb ap">{MARQUE} Ce qu’on fait</span>
    <h2 class="grand">Vous n’avez plus à <em>tout porter.</em></h2>
    <div class="deux ap">
      <p>Un enjeu RH devient financier, puis médiatique. Le Centre réunit les bonnes expertises, au moment où vous en avez besoin.</p>
      <p style="font-weight:600"><a href="expertises.html" style="color:var(--of)">Voir les expertises →</a></p>
    </div>
    <div class="duo-photo ap">
      <figure class="demi-photo g">{img("dirigeante-ecoute","Dirigeante à l’écoute pendant une rencontre",extra=' data-par=".06"')}</figure>
      <figure class="demi-photo d">{img("conversation-cafe","Conversation entre dirigeants autour d’un café",extra=' data-par="-.06"')}</figure>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:2vh">
  <div class="w">
    <div class="pur-tete petit"><div>
    <span class="eb ap">{MARQUE} Comment on le fait</span>
    <h2 class="grand">Avant, pendant <em>et après</em> la tempête.</h2>
    <p class="int ap">Le continuum PUR : trois moments qui s’emboîtent, un même réseau.</p>
    </div><img class="roue ap" src="img/roue-pur.webp" srcset="img/roue-pur-500.webp 500w, img/roue-pur.webp 900w" sizes="(max-width:820px) 70vw, 300px" alt="Le continuum PUR : Prévention, Urgence et Reconstruction, trois pièces d’un même casse-tête" width="900" height="900" loading="lazy"></div>
    <div class="verbes">
      {"".join(f'<article class="verbe ap" style="transition-delay:{i*.1}s"><span class="k">{k}</span><h3>{v}</h3><div class="vph">{img(ph_, alt)}</div><p>{x}</p></article>' for i,(c,k,v,q,x,sig,ex,ph_,alt) in enumerate(PUR))}
    </div>
    <div class="ap" style="margin-top:34px"><a class="btn" href="fonctionnement.html">Comprendre la démarche <span class="fl">→</span></a></div>
  </div>
</section>

<section class="preuve"><div class="preuve-fond" aria-hidden="true" style="background-image:url(img/equipe-reseau-1400.webp)" data-parbg></div>
  <span class="deco" aria-hidden="true"></span>
  <div class="w">
    <span class="eb ap">{MARQUE} Le réseau en chiffres</span>
    <div class="chiff">
      <div class="ap"><div class="v" data-c="8">8</div><p>experts collaborateurs, choisis pour leur façon de travailler</p></div>
      <div class="ap"><div class="v o" data-c="10">10</div><p>domaines d’expertise qui se parlent entre eux</p></div>
      <div class="ap"><div class="v">1</div><p>seule prise de contact pour tout mettre en mouvement</p></div>
    </div>
    <p class="note ap">Près de <span>70 organisations</span> accompagnées par l’équipe fondatrice en deux ans. Le Centre met ce réseau à votre portée.</p>
  </div>
</section>

<div class="bandeau-photos" aria-hidden="true"><div class="rang r1">{bande(B1)}{bande(B1)}</div><div class="rang r2">{bande(B2)}{bande(B2)}</div></div>

<section class="sec">
  <div class="w">
    <p class="enonce">Subir l’imprévu coûte cher. Savoir <mark>qui appeler</mark> change tout.</p>
    <h2 class="eb ap" style="margin-top:7vh">{MARQUE} Ce que vous obtenez</h2>
    <div class="benef">
      <div class="bn ap"><span class="n">01</span><h3>Des décisions qui avancent.</h3><p>Moins de dossiers en suspens, plus de choix assumés et suivis.</p></div>
      <div class="bn ap" style="transition-delay:.08s"><span class="n">02</span><h3>Des équipes qui restent.</h3><p>Un climat plus sain, moins d’épuisement, une culture durable.</p></div>
      <div class="bn ap" style="transition-delay:.16s"><span class="n">03</span><h3>Une organisation qui tient.</h3><p>Des pratiques solides en finances, conformité et gouvernance.</p></div>
      <div class="bn ap" style="transition-delay:.24s"><span class="n">04</span><h3>Une direction moins isolée.</h3><p>Des pairs et des experts de confiance, à portée de main.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <span class="eb ap">{MARQUE} Rester proches</span>
    <h2 class="grand">Plus qu’un réseau. <em>Un centre.</em></h2>
    <div class="portes">
      <a class="porte ap" href="communaute.html">{img("cafe-equipe","Dirigeants en discussion")}<span class="k">Communauté</span><h3>Penser à voix haute, entre pairs.</h3><p>Des cercles de dirigeants, sur invitation, où la parole reste dans la salle.</p><span class="fl2">Découvrir →</span></a>
      <a class="porte ap" style="transition-delay:.1s" href="ressources.html">{img("collaboration","Deux personnes qui collaborent")}<span class="k">Ressources</span><h3>Des outils pour décider mieux.</h3><p>Réflexions, outils, diagnostics et l’infolettre ENTRE NOUS.</p><span class="fl2">Explorer →</span></a>
      <a class="porte ap" style="transition-delay:.2s" href="agenda.html">{img("equipe-applaudit","Équipe réunie lors d’une activité")}<span class="k">Agenda</span><h3>Où croiser nos experts.</h3><p>Conférences, formations et activités du Centre et de ses experts.</p><span class="fl2">Voir l’agenda →</span></a>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="w sv">
    <div class="ap">
      <span class="eb">{MARQUE} En bref</span>
      <h2 class="grand" style="font-size:clamp(2.2rem,4.4vw,3.8rem)">Le Centre, en une minute.</h2>
      <p class="def">Le Centre des dirigeants est un réseau de collaborateurs experts et une communauté de pairs, lancé en novembre 2026 à Gatineau par France Bélisle et Nicolas Roy, qui accompagne les dirigeants d’entreprises et d’organisations à partir d’une seule prise de contact.</p>
      <dl>
        <dt>Pour qui</dt><dd>Dirigeants d’entreprises et d’organisations (surtout des PME, mais aussi des OBNL et de grandes organisations), conseils d’administration</dd>
        <dt>Où</dt><dd>Gatineau, Outaouais et ailleurs au Québec</dd>
        <dt>Approche</dt><dd>Continuum PUR : Prévention, Urgence, Reconstruction</dd>
        <dt>Accès</dt><dd>Sur invitation, pour les clients de nos collaborateurs · {MAIL}</dd>
      </dl>
    </div>
    <div class="faq ap"><h3 class="eb" style="margin-bottom:8px">{MARQUE} Questions fréquentes</h3>{faq_html(FAQ_ACC)}<p style="margin-top:18px"><a href="contact.html#faq" style="font-weight:700">Toutes les questions →</a></p></div>
  </div>
</section>
{cta()}
'''
page("index.html", "Centre des dirigeants | Experts pour dirigeants, Gatineau",
     "Un réseau d’experts et une communauté de pairs pour les dirigeants d’entreprises et d’organisations à Gatineau : stratégie, finances, RH, crise, médiation, santé mentale, IA.",
     accueil, ld_extra=faq_ld(FAQ_ACC), typepage=["WebPage", "FAQPage"], scripts=DATA_EXP)

# =========================== FONCTIONNEMENT ===========================
FAQ_F = [FAQ[2], FAQ[4], FAQ[5], FAQ[6], FAQ[7]]
SITU = [
    ("Une direction générale part du jour au lendemain.", "Un OBNL de 40 employés perd sa direction générale sans préavis. Le conseil doit rassurer l’équipe, assurer l’intérim et préparer un recrutement.", ["Gouvernance", "Communications", "Ressources humaines", "Tests psychométriques"]),
    ("Une crise médiatique éclate un vendredi soir.", "Une PME se retrouve à la une pour un incident. Il faut une ligne de communication claire, des appuis politiques et un regard sur l’impact financier.", ["Communications de crise", "Relations gouvernementales", "Finances"]),
    ("L’équipe s’épuise en pleine croissance.", "Une entreprise double ses ventes en deux ans. Les gestionnaires sont débordés, les départs se multiplient et la culture s’effrite.", ["Santé mentale au travail", "Ressources humaines", "Stratégie", "IA pour alléger les tâches"]),
]
fonct = ph("fonctionnement.html", "Comment ça fonctionne", "Comment ça fonctionne", "Une seule porte. <em>Les bons experts.</em>",
           "Quand tout semble urgent, chercher de l’aide devient une tâche de plus. Le Centre réduit cette démarche à une seule prise de contact.", "planification", "Rencontre de planification") + f'''
<section class="sec">
  <div class="w">
    <span class="eb ap">{MARQUE} La démarche</span>
    <h2 class="grand">Trois gestes. <em>Zéro détour.</em></h2>
    <div class="etapes ap">
      <div><span class="num-g">01</span><h3>Vous écrivez</h3><p>Quelques lignes, dans vos mots. Ce qui presse, ce qui accroche, ce que vous avez déjà essayé.</p></div>
      <div><span class="num-g">02</span><h3>On vous oriente</h3><p>La coordination du Centre lit votre demande, prend le temps de comprendre et vous met en relation avec le ou les experts pertinents.</p></div>
      <div><span class="num-g">03</span><h3>Vous avancez</h3><p>Un appui ponctuel ou dans la durée. Si plusieurs expertises sont en jeu, l’équipe se coordonne pour vous.</p></div>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0" id="pur">
  <div class="w">
    <div class="pur-tete"><div>
    <span class="eb ap">{MARQUE} Le continuum PUR</span>
    <h2 class="grand">Prévention. Urgence. <em>Reconstruction.</em></h2>
    <p class="int ap">Le bon appui dépend du moment. Le continuum tient compte autant des besoins de l’organisation que de la réalité de la personne qui la dirige. Trois moments, trois pièces d’un même casse-tête : chacune s’emboîte dans la suivante.</p>
    </div><img class="roue ap" src="img/roue-pur.webp" srcset="img/roue-pur-500.webp 500w, img/roue-pur.webp 900w" sizes="(max-width:820px) 70vw, 380px" alt="Le continuum PUR : Prévention, Urgence et Reconstruction, trois pièces d’un même casse-tête" width="900" height="900" loading="lazy"></div>
    {"".join(f'<article class="axe {c} ap"><div class="ph2">{img(ph_,alt)}</div><div class="tx"><span class="k">{k}</span><h3>{v}</h3><p class="q">{q}</p><p>{x}</p><span class="sous">Vous êtes ici si…</span><ul>{"".join(f"<li>{s_}</li>" for s_ in sig)}</ul></div></article>' for (c,k,v,q,x,sig,ex,ph_,alt) in PUR)}
  </div>
</section>

<section class="sec creme">
  <div class="w">
    <span class="eb ap">{MARQUE} Situations types</span>
    <h2 class="grand">À quoi ça ressemble, <em>concrètement.</em></h2>
    <p class="int ap">Des situations illustratives, inspirées de ce que vivent les dirigeants. Les noms et détails sont fictifs.</p>
    <div class="g3c">{"".join(f'<div class="situ ap"><h3>{t}</h3><p>{d}</p><div class="mob">{"".join(f"<span>{m}</span>" for m in ms)}</div></div>' for t,d,ms in SITU)}</div>
  </div>
</section>

<section class="sec">
  <div class="w g2c" style="margin-top:0;align-items:start">
    <div class="carte ap"><span class="tag or">Notre engagement</span><h3>Le bon expert, pas le plus proche.</h3><p>Nous vous orientons selon votre situation, vers l’expertise qui y répond le mieux. Si la bonne personne n’est pas dans le réseau, nous vous le dirons.</p></div>
    <div class="carte ap" style="transition-delay:.1s"><span class="tag">Confidentialité</span><h3>Votre situation reste entre nous.</h3><p>Votre demande est traitée avec discrétion et partagée seulement avec les experts concernés, avec votre accord. <a href="politique-confidentialite.html" style="font-weight:700">Notre politique</a></p></div>
  </div>
</section>

{cta()}
'''
page("fonctionnement.html", "Comment ça fonctionne | Centre des dirigeants, Gatineau",
     "Une seule prise de contact, une mise en relation avec les bons experts et le continuum PUR : Prévention, Urgence, Reconstruction.",
     fonct, nom="Comment ça fonctionne", ld_extra=faq_ld(FAQ_F), typepage=["WebPage", "FAQPage"])

# ============================= EXPERTISES =============================
xp_html = "".join(f'''<article class="xp ap" id="{re.sub(r"[^a-z]+","-",t.lower().translate(str.maketrans("éèêàâîôûç’","eeeaaiouc ")) ).strip("-")}">
  <div><span class="n">{i+1:02d}</span><h3>{t}</h3></div>
  <div><p>{d}</p><ul>{"".join(f"<li>{s_}</li>" for s_ in SITUATIONS[t])}</ul></div>
</article>''' for i, (t, d, _) in enumerate(EXPERTISES))
expert_ld = {"mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Service", "name": t, "description": d, "provider": {"@id": ORG_ID}, "areaServed": "Outaouais"}} for i, (t, d, _) in enumerate(EXPERTISES)]}}
expertises = ph("expertises.html", "Expertises", "Expertises et outils", "Vos enjeux se croisent. <em>Nos expertises aussi.</em>",
                "Dix domaines complémentaires, réunis pour les dirigeants d’entreprises et d’organisations. Reconnaissez votre situation, on s’occupe du reste.", "reunion-direction", "Réunion de direction") + f'''
<section class="sec">
  <div class="w">
    <span class="eb ap">{MARQUE} Dix domaines</span>
    <h2 class="grand">Des besoins différents. <em>Un même réseau.</em></h2>
    <div style="margin-top:6vh">{xp_html}</div>
  </div>
</section>

<section class="sec marine">
  <div class="w">
    <span class="eb ap">{MARQUE} Des outils pour aller plus loin</span>
    <h2 class="grand">Décider sur des faits, <em>pas sur des impressions.</em></h2>
    <div class="g3c">
      <div class="carte ap"><span class="tag or">Évaluation</span><h3>Tests psychométriques AtmanPro</h3><p>Mieux comprendre les profils pour recruter juste, développer vos gestionnaires et composer des équipes qui fonctionnent.</p></div>
      <div class="carte ap" style="transition-delay:.1s"><span class="tag or">Mesure</span><h3>Sondages internes et externes</h3><p>Conçus sur mesure pour recueillir les perceptions de vos employés, clients ou partenaires et établir un diagnostic.</p></div>
      <div class="carte ap" style="transition-delay:.2s"><span class="tag or">Marque employeur</span><h3>Adhésion</h3><p>Mesurer et renforcer ce qui donne envie de rester dans votre organisation, et d’y entrer.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <span class="eb ap">{MARQUE} Accompagnements de fond</span>
    <h2 class="grand">Quand il faut <em>prendre le temps.</em></h2>
    <div class="g3c">
      <div class="carte ap"><h3>Planification stratégique</h3><p>Choisir ses priorités, aligner son équipe de direction et s’y tenir.</p></div>
      <div class="carte ap" style="transition-delay:.1s"><h3>Coaching de gestion</h3><p>Un espace pour prendre du recul sur votre rôle, vos décisions et votre façon de diriger.</p></div>
      <div class="carte ap" style="transition-delay:.2s"><h3>Médiation</h3><p>Rétablir le dialogue entre associés, gestionnaires ou équipes quand le conflit bloque tout.</p></div>
    </div>
  </div>
</section>
{cta("Votre enjeu n’est pas dans la liste ?", "Écrivez-nous quand même. Le réseau sait vers qui vous orienter.", photo="appel")}
'''
page("expertises.html", "Expertises : stratégie, RH, finances, IA | Centre des dirigeants",
     "Stratégie, CFO à la demande, RH, communications de crise, médiation, santé mentale, protection des données, IA, sondages et tests AtmanPro, en Outaouais.",
     expertises, nom="Expertises", ld_extra=expert_ld)

# =============================== EXPERTS ===============================
AVEC_PAGE = {"france-belisle","yannick-beaulieu","chantal-dufort","daniel-feeny","sophie-ann-bellisle","marc-antoine-laramee","nicolas-roy","andreanne-thibault"}
exec(open(os.path.join(HERE, "bios.py"), encoding="utf-8").read())
PRENOM = {"sophie-ann-bellisle": "Sophie Ann"}
def bio_html(s, d):
    b = BIOS.get(s)
    if not b: return f"<p>{d}</p>"
    reste = "".join(f"<p>{x}</p>" for x in b[1:])
    return f'<div class="bio"><p>{b[0]}</p>' + (f'<details><summary><span class="ouvrir">Lire la suite</span><span class="fermer">Réduire</span></summary>{reste}</details>' if reste else "") + "</div>"
fiches = "".join(f'''<article class="fiche-x ap" id="{s}" data-expert="{s}">
  <div class="haut"><img src="img/{s}.webp" alt="{n}" width="96" height="96" loading="lazy"><div><h3>{n}{f"<small>{c}</small>" if c else ""}</h3></div></div>
  <div class="corps">{bio_html(s, d)}<div class="tags">{"".join(f"<span>{x}</span>" for x in t)}</div>{f'<a class="lien-x" href="expert-{s}.html">Voir le profil complet →</a>' if s in AVEC_PAGE else '<span class="lien-x" style="opacity:.7">Coordination du Centre</span>'}</div>
</article>''' for s, n, c, r, d, t in EXPERTS)
pers = personnes(EXPERTS)
for p in pers: p["@id"] = BASE + "experts.html#" + p["@id"].split("#")[1]
experts = ph("experts.html", "Les experts", "Les experts du Centre", "Un réseau <em>de confiance.</em>",
             "Des professionnels qui partagent une même volonté : offrir aux dirigeants un accompagnement concret, au moment où ils en ont besoin.", "equipe-reseau", "Équipe du réseau") + f'''
<section class="reseau" style="margin-top:clamp(10px,2vw,24px)">
  <div class="w">{constellation("pages")}</div>
</section>
<section class="sec">
  <div class="w">
    <span class="eb ap">{MARQUE} Les fiches</span>
    <h2 class="grand">Qui fait <em>quoi.</em></h2>
    <div class="fiches">{fiches}</div>
    <p class="ap" style="margin-top:30px;color:var(--d)">Les experts du réseau sont des professionnels et des entreprises indépendants. Les cercles de la communauté restent réservés aux dirigeants.</p>
  </div>
</section>
{cta("Pas besoin de choisir qui contacter.", "Décrivez votre situation. On s’occupe de trouver la bonne combinaison d’expertises.", photo="trio-portable")}
'''
page("experts.html", "Les experts du Centre des dirigeants | Gatineau",
     "France Bélisle, Nicolas Roy, Yannick Beaulieu, Andréanne Thibault, Chantal Dufort, Daniel Feeny et les autres experts du Centre des dirigeants.",
     experts, nom="Les experts", typepage="CollectionPage",
     ld_extra={"mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": p} for i, p in enumerate(pers)]}}, scripts=DATA_EXP)

# ============================ PAGES EXPERT ============================
sys.path.insert(0, HERE)
from experts_data import EXPERTS_FICHES
def hl(t): return t.replace("[", '<mark class="avalider">[').replace("]", "]</mark>")
ORDRE = [e["slug"] for e in EXPERTS_FICHES]
for e in EXPERTS_FICHES:
    s_ = e["slug"]; nomc = e["nom"] + (", " + e["cred"] if e["cred"] else "")
    nom_court = e["nom"].replace(" (Marcan)", "")
    exp_html = "".join(f'<article class="xcarte ap" style="transition-delay:{i*.06:.2f}s"><span class="num-g" style="font-size:2.4rem">{i+1:02d}</span><h3>{t}</h3><p>{hl(d)}</p><p class="obj"><b>{e["lab"]} :</b> {hl(r)}</p></article>' for i, (t, d, r) in enumerate(e["exp"]))
    fac_html = "".join(f'<div class="facon ap {"f1" if i==0 else "f2"}"><span class="k">0{i+1}</span><h3>{t}</h3><p>{hl(d)}</p></div>' for i, (t, d) in enumerate(e["facons"]))
    pq = ("<ul class=\"puces-x\">" + "".join(f"<li>{hl(x)}</li>" for x in e["pourquoi"]) + "</ul>") if e["pourquoi_liste"] else "".join(f"<p>{hl(x)}</p>" for x in e["pourquoi"])
    qd = "<ul class=\"puces-x\">" + "".join(f"<li>{x}</li>" for x in e["quand"]) + "</ul>" + (f'<p style="margin-top:16px">{e["fin"]}</p>' if e["fin"] else "")
    autres = "".join(f'<a class="autre" href="expert-{o["slug"]}.html"><img src="img/{o["slug"]}.webp" alt="" width="72" height="72" loading="lazy"><span><b>{o["nom"].replace(" (Marcan)","")}</b><small>{o["titre"]}</small></span></a>' for o in EXPERTS_FICHES if o["slug"] != s_)
    corps = f'''<section class="xhero">
  <div class="w xh">
    <div>
      <nav class="fil" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span aria-hidden="true">/</span><a href="experts.html">Les experts</a><span aria-hidden="true">/</span><span aria-current="page">{nom_court}</span></nav>
      <span class="eb clair">{MARQUE} {e["genre"]} du Centre</span>
      <h1>{e["nom"]}{f'<small>{e["cred"]}</small>' if e["cred"] else ''}</h1>
      <p class="xt">{e["titre"]}</p>
      <p class="xs">{hl(e["sous"])}</p>
      <div class="actions" style="margin-top:28px"><a class="btn or" href="contact.html?type=situation#formulaire">Planifier une rencontre <span class="fl">→</span></a><a class="btn cl2" href="docs/fiche-{s_}.pdf" download>Télécharger la fiche (PDF)</a></div>
    </div>
    <figure class="xportrait"><img src="img/{s_}-grand.webp" alt="{nom_court}" width="1100" height="1100" fetchpriority="high"></figure>
  </div>
</section>

<section class="sec">
  <div class="w split" style="align-items:start">
    <div><span class="eb ap">{MARQUE} En quelques mots</span><h2 class="grand" style="font-size:clamp(2.2rem,4.6vw,4.2rem)">{e["intro_t"]}</h2></div>
    <div class="ap">{"".join(f'<p class="int" style="margin-top:0">{hl(x)}</p>' for x in e["intro"])}</div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="w">
    <span class="eb ap">{MARQUE} {e["exp_t"]}</span>
    <div class="xgrille">{exp_html}</div>
  </div>
</section>

<section class="sec creme">
  <div class="w">
    <span class="eb ap">{MARQUE} Travailler ensemble</span>
    <h2 class="grand">Deux façons <em>de travailler ensemble.</em></h2>
    <div class="facons">{fac_html}</div>
  </div>
</section>

<section class="sec marine">
  <div class="w g2c" style="margin-top:0;gap:5vw;align-items:start">
    <div class="ap"><span class="eb">{MARQUE} Pourquoi collaborer avec {"moi" if True else ""}</span><div class="pq">{pq}</div></div>
    <div class="ap"><span class="eb">{MARQUE} {e["quand_t"].replace(" ?","")}</span><h2 class="grand" style="font-size:clamp(2rem,3.6vw,3.2rem);margin-bottom:18px">{e["quand_t"].replace(" ?", "\u00a0?")}</h2>{qd}</div>
  </div>
</section>

<section class="sec" style="padding-bottom:0">
  <div class="w"><div class="milieux ap"><span class="eb">{MARQUE} {e["milieux_t"]}</span><p>{hl(e["milieux"])}</p></div></div>
</section>
{f'''<section class="sec" id="bio">
  <div class="w split" style="align-items:start">
    <div><span class="eb ap">{MARQUE} Biographie</span><h2 class="grand" style="font-size:clamp(2.2rem,4.6vw,4.2rem)">Le parcours <em>de {PRENOM.get(s_, nom_court.split(" ")[0])}.</em></h2></div>
    <div class="ap bio-x">{"".join(f"<p>{x}</p>" for x in BIOS[s_])}</div>
  </div>
</section>''' if s_ in BIOS else ""}
{cta(f"Travailler avec {PRENOM.get(s_, nom_court.split(' ')[0])} ?", f"L’accès au Centre se fait sur invitation. Présentez-vous à la coordination, qui organise un premier échange avec {PRENOM.get(s_, nom_court.split(' ')[0])}, ou avec l’expert le mieux placé pour votre situation.", "Planifier une rencontre", "contact.html?type=situation#formulaire", "bureau-sourire")}
<section class="sec" style="padding-top:0">
  <div class="w"><span class="eb ap">{MARQUE} Les autres experts du Centre</span><div class="autres ap">{autres}</div></div>
</section>
'''
    pers = {"@type": "Person", "@id": BASE + f"expert-{s_}.html#personne", "name": nom_court, "jobTitle": e["titre"], "description": " ".join(e["intro"]),
            "image": BASE + f"img/{s_}-grand.webp", "knowsAbout": [t for t, _, _ in e["exp"]], "memberOf": {"@id": ORG_ID}, "knowsLanguage": "fr-CA"}
    if e["cred"]: pers["honorificSuffix"] = e["cred"]
    titre_p = f"{nom_court} | {e['titre']} | Centre des dirigeants"
    if len(titre_p) > 65: titre_p = f"{nom_court}, {e['titre']}"
    if len(titre_p) > 65: titre_p = f"{nom_court} | Centre des dirigeants"
    desc_p = re.sub("<[^>]+>", "", e["intro"][0])
    desc_p = (desc_p[:150].rsplit(" ", 1)[0] + "…") if len(desc_p) > 155 else desc_p
    page(f"expert-{s_}.html", titre_p, desc_p, corps, nom=nom_court, typepage="ProfilePage", ld_extra={"mainEntity": pers},
         bc=[("Accueil", "index.html"), ("Les experts", "experts.html"), (nom_court, f"expert-{s_}.html")], nav_actif="experts.html")

# ============================== COMMUNAUTÉ ==============================
SALLES = [("La Salle de réflexion", "Des textes pour prendre du recul sur votre rôle et vos décisions."),
          ("La Boîte à outils", "Des gabarits et des grilles à utiliser dès lundi avec votre équipe."),
          ("L’Espace décision", "Des cadres pour trancher plus vite et mieux, en solo ou en équipe."),
          ("Les Archives vivantes", "Les conférences et échanges marquants, à revoir quand vous en avez besoin."),
          ("Les Diagnostics", "Des auto-évaluations pour savoir où vous en êtes, sans complaisance."),
          ("La Salle de préparation", "Pour préparer une rencontre difficile, une annonce ou un conseil d’administration.")]
commu = ph("communaute.html", "Communauté", "La communauté de pairs", "Penser à voix haute, <em>entre pairs.</em>",
           "On peut être entouré toute la journée et n’avoir personne à qui parler de ce qui nous préoccupe vraiment. La communauté du Centre existe pour ça.", "cafe-equipe", "Dirigeants en discussion") + f'''
<section class="sec">
  <div class="w split">
    <div>
      <span class="eb ap">{MARQUE} Pourquoi une communauté</span>
      <h2 class="grand">La solitude du dirigeant <em>n’est pas une fatalité.</em></h2>
      <p class="int ap">Au sommet, les vraies questions se posent rarement à voix haute. Pas devant l’équipe, pas devant le conseil, pas toujours à la maison. Les cercles du Centre réunissent des dirigeants qui vivent la même réalité, dans un cadre où l’on peut tout dire.</p>
      <p class="int ap" style="font-weight:600">Pas de réseautage vide. Pas de façade. Des échanges vrais, qui aident à décider.</p>
    </div>
    <figure class="ap">{img("deux-collegues","Deux dirigeantes en conversation")}</figure>
  </div>
</section>

<section class="sec marine">
  <div class="w">
    <span class="eb ap">{MARQUE} Les règles du cercle</span>
    <h2 class="grand">Un cadre simple. <em>Une confiance totale.</em></h2>
    <div class="regles">
      <div class="regle ap"><span class="num-g">01</span><h3>Sur invitation</h3><p>On entre dans la communauté sur recommandation ou invitation, pour préserver la qualité des échanges.</p></div>
      <div class="regle ap" style="transition-delay:.08s"><span class="num-g">02</span><h3>Entre pairs seulement</h3><p>Les experts du réseau ne participent pas aux cercles. La parole reste entre dirigeants.</p></div>
      <div class="regle ap" style="transition-delay:.16s"><span class="num-g">03</span><h3>Ce qui se dit reste là</h3><p>Rien de ce qui est partagé dans un cercle n’en sort, même sous forme anonyme.</p></div>
      <div class="regle ap" style="transition-delay:.24s"><span class="num-g">04</span><h3>On repart avec quelque chose</h3><p>Chaque rencontre se termine par une décision, une piste ou un outil à rapporter à votre équipe.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <span class="eb ap">{MARQUE} Le portail des membres</span>
    <h2 class="grand">Un centre, <em>pas seulement des rencontres.</em></h2>
    <p class="int ap">Entre les cercles, les membres ont accès à un portail de ressources conçues pour être utilisées sans animateur, dans la vraie vie d’une organisation.</p>
    <div class="salles">{"".join(f'<div class="salle ap" style="transition-delay:{i*.06:.2f}s">{MARQUE}<h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(SALLES))}</div>
  </div>
</section>
{cta("Vous aimeriez rejoindre un cercle ?", "Dites-nous qui vous êtes et ce que vous cherchez. Nous vous recontacterons pour en parler.", "Demander une invitation", "contact.html?type=invitation#formulaire", "complicite")}
'''
page("communaute.html", "Communauté et cercles de pairs | Centre des dirigeants",
     "Des cercles de dirigeants d’entreprises et d’organisations, sur invitation, où la parole reste entre pairs. Un portail de ressources pour les membres.",
     commu, nom="Communauté")

# ============================== RESSOURCES ==============================
RES = [
    ("reflexions", "Réflexion", "Pourquoi votre stratégie ne fonctionne pas (et ce n’est pas à cause de la stratégie)", "Ce qui bloque l’exécution se trouve rarement dans le plan.", "Public", "planification"),
    ("reflexions", "Réflexion", "Le vrai problème derrière votre surcharge de gestion", "Et si le trop-plein n’était pas une question de temps ?", "Public", "equipe-concentree"),
    ("reflexions", "Réflexion", "Ce que les dirigeants ne se disent jamais entre eux", "Les conversations qui manquent, et ce qu’elles coûtent.", "Public", "conversation-cafe"),
    ("reflexions", "Essai signature", "Les 4 angles morts des dirigeants en croissance", "Une lecture longue pour ceux qui grandissent vite.", "Public", "dirigeant-explique"),
    ("outils", "Outil", "Grille d’alignement stratégique", "Vérifier en 20 minutes si votre équipe de direction tire dans le même sens.", "Membres", "trio-portable"),
    ("outils", "Outil", "Questions pour recadrer une équipe de direction", "Les bonnes questions pour une rencontre qui tourne en rond.", "Membres", "reunion-direction"),
    ("diagnostics", "Diagnostic", "Diagnostic de posture du leader", "Une auto-évaluation franche de votre façon de diriger.", "Membres", "dirigeante-ecoute"),
    ("conferences", "Archives", "Conférences du Centre", "Les interventions de nos experts, à revoir au besoin.", "Membres", "equipe-applaudit"),
]
res_html = "".join(f'''<article class="res ap" data-cat="{cat}">
  <div class="vis"><img src="img/{ph_}-p.webp" alt="" loading="lazy" width="640" height="427">{MARQUE}</div>
  <div class="c"><div class="meta"><span>{typ}</span><span class="{'membre' if acc=='Membres' else ''}">{'Réservé aux membres' if acc=='Membres' else 'Accès libre'}</span><span class="bientot">À paraître</span></div><h3>{t}</h3><p>{d}</p></div>
</article>''' for cat, typ, t, d, acc, ph_ in RES)
ressources = ph("ressources.html", "Ressources", "Ressources", "Penser mieux. <em>Décider plus vite.</em>",
                "Des réflexions pour prendre du recul, des outils pour passer à l’action. Nous publions ce qui fait réfléchir, et réservons aux membres ce qui fait agir.", "collaboration", "Collaboration au travail") + f'''
{infolettre("entre-nous").replace('style="padding-top:0"','style="padding-top:clamp(60px,8vw,110px)"')}
<section class="sec" style="padding-top:0">
  <div class="w">
    <span class="eb ap">{MARQUE} La bibliothèque</span>
    <h2 class="grand">Les premières <em>parutions.</em></h2>
    <div class="filtres" data-filtres="#biblio" role="group" aria-label="Filtrer les ressources">
      <button class="filtre" data-v="tous" aria-pressed="true">Tout</button><button class="filtre" data-v="reflexions" aria-pressed="false">Réflexions</button><button class="filtre" data-v="outils" aria-pressed="false">Outils</button><button class="filtre" data-v="diagnostics" aria-pressed="false">Diagnostics</button><button class="filtre" data-v="conferences" aria-pressed="false">Conférences</button>
    </div>
    <div class="res-g" id="biblio">{res_html}</div>
    <p class="ap" style="margin-top:28px;color:var(--d)">Abonnez-vous à ENTRE NOUS pour être averti de chaque nouvelle parution. Les ressources réservées sont accessibles aux membres de la <a href="communaute.html" style="font-weight:700">communauté</a>.</p>
  </div>
</section>
{cta("Une question précise ?", "Les ressources aident à réfléchir. Pour votre situation à vous, rien ne remplace une conversation.", photo="duo-portable")}
'''
page("ressources.html", "Ressources et infolettre | Centre des dirigeants",
     "Réflexions, outils, diagnostics et l’infolettre ENTRE NOUS pour les dirigeants d’entreprises et d’organisations. Penser mieux, décider plus vite.",
     ressources, nom="Ressources", typepage="CollectionPage")

# ================================ AGENDA ================================
def ev_html(e, passe=False):
    d = datetime.date.fromisoformat(e["date"])
    who = "".join(f'<img src="img/{s}.webp" alt="{EXPD[s]["n"]}" title="{EXPD[s]["n"]}">' for s in e.get("experts", []))
    noms = ", ".join(EXPD[s]["n"] for s in e.get("experts", []))
    if e.get("tous"): noms = "l’ensemble des experts du Centre"
    lien = f'<a href="{e["lien"]}" style="font-weight:700">{"À propos de l’événement" if passe else "Détails et inscription"} →</a>' if e.get("lien") else ""
    return f'''<article class="ev" data-cat="{e["type"]}" data-date="{e["date"]}" data-fin="{e.get("fin", e["date"])}">
  <div class="date"><b>{d.day}</b><span>{MOIS[d.month-1]} {d.year}</span></div>
  <div><span class="type">{TYPES_EV[e["type"]]}</span><h3 style="margin-top:8px">{e["titre"]}</h3><p>{e.get("desc","")}</p>{f'<p class="note-ev">{e["note"]}</p>' if e.get("note") else ""}
  <div class="infos">{f"<span>{e['heure']}</span>" if e.get("heure") else ""}{f"<span>{e['lieu']}" + (f", {e['adresse']}" if e.get("adresse") else "") + "</span>" if e.get("lieu") else ""}{f"<span>Avec {noms}</span>" if noms else ""}{lien}</div></div>
  <div class="who">{who}</div>
</article>'''
AUJ = datetime.date.today()
evs = sorted([e for e in EVENTS if datetime.date.fromisoformat(e.get("fin", e["date"])) >= AUJ], key=lambda e: e["date"])
evs_p = sorted([e for e in EVENTS if datetime.date.fromisoformat(e.get("fin", e["date"])) < AUJ], key=lambda e: e["date"], reverse=True)
ev_ld = {"mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {
    "@type": "Event", "name": e["titre"], "startDate": e["date"], "endDate": e.get("fin", e["date"]), "description": e.get("desc", ""),
    "eventAttendanceMode": "https://schema.org/" + ("OnlineEventAttendanceMode" if e.get("en_ligne") else "OfflineEventAttendanceMode"), "eventStatus": "https://schema.org/EventScheduled",
    **({"isAccessibleForFree": True} if "gratuit" in e.get("note", "").lower() else {}),
    "location": {"@type": "VirtualLocation", "url": e.get("lien", "")} if e.get("en_ligne") else {"@type": "Place", "name": e.get("lieu", "Gatineau"), "address": {"@type": "PostalAddress", **({"streetAddress": e["adresse"].split(", Gatineau")[0]} if e.get("adresse") else {}), "addressLocality": "Gatineau", "addressRegion": "QC", "addressCountry": "CA"}},
    "organizer": {"@id": ORG_ID}, "performer": [{"@type": "Person", "name": EXPD[s]["n"]} for s in e.get("experts", [])]}} for i, e in enumerate(evs + evs_p)]}} if (evs or evs_p) else None
agenda = ph("agenda.html", "Agenda", "Agenda", "Où croiser <em>nos experts.</em>",
            "Conférences, formations, cercles et événements du Centre et de ses experts. Pour apprendre, échanger et rencontrer les bonnes personnes.", "equipe-applaudit", "Équipe réunie lors d’une activité") + f'''
<section class="sec">
  <div class="w">
    <span class="eb ap">{MARQUE} À venir</span>
    <h2 class="grand">Ce qui <em>s’en vient.</em></h2>
    <div class="filtres" data-filtres="#agenda" role="group" aria-label="Filtrer les activités"{' hidden' if not evs else ''}>
      <button class="filtre" data-v="tous" aria-pressed="true">Tout</button>{"".join(f'<button class="filtre" data-v="{k}" aria-pressed="false">{v}</button>' for k,v in TYPES_EV.items())}
    </div>
    <div class="ag-liste" id="agenda">{"".join(ev_html(e) for e in evs)}</div>
    <p class="vide-filtre" hidden style="margin-top:20px;color:var(--d)">Aucune activité de ce type pour le moment.</p>
    <div class="vide ap" id="agenda-vide"{'' if not evs else ' hidden'}>
      <div class="cal" aria-hidden="true"><svg viewBox="0 0 40 40"><path d="M19 4a14 14 0 0 0 0 28z" fill="#0C283A"/><path d="M21 8a14 14 0 0 1 0 28z" fill="#F2EDE7"/></svg></div>
      <div><h3>Les premières activités seront annoncées sous peu.</h3><p>Le Centre prépare ses premières formations et rencontres avec les experts du réseau. Abonnez-vous à ENTRE NOUS pour être parmi les premiers avertis.</p><div style="margin-top:20px"><a class="btn" href="#infolettre">Être averti <span class="fl">→</span></a></div></div>
    </div>
  </div>
</section>
<section class="sec" id="passees" style="padding-top:0"{'' if evs_p else ' hidden'}>
  <div class="w">
    <span class="eb ap">{MARQUE} Activités passées</span>
    <h2 class="grand">Là où <em>on était.</em></h2>
    <div class="ag-liste passe" id="agenda-passe">{"".join(ev_html(e, True) for e in evs_p)}</div>
  </div>
</section>
<section class="sec creme">
  <div class="w g2c" style="margin-top:0">
    <div class="carte ap"><span class="tag or">Organisateurs</span><h3>Un expert du Centre pour votre événement ?</h3><p>Conférences, panels, formations en entreprise : nos experts interviennent sur la gestion de crise, la santé mentale au travail, la gouvernance, l’IA et plus encore.</p><a class="lien" href="contact.html?type=evenement#formulaire">Inviter un expert →</a></div>
    <div class="carte ap" style="transition-delay:.1s"><span class="tag">Membres</span><h3>Les cercles de pairs</h3><p>Les rencontres des cercles sont réservées aux membres de la communauté et ne sont pas publiées ici.</p><a class="lien" href="communaute.html">Découvrir la communauté →</a></div>
  </div>
</section>
'''
page("agenda.html", "Agenda : conférences et formations | Centre des dirigeants",
     "Conférences, formations et événements du Centre des dirigeants et de ses experts à Gatineau et en Outaouais.",
     agenda, nom="Agenda", ld_extra=ev_ld)

# =============================== CONTACT ===============================
TYPES = [("invitation", "Demander une invitation", "Demande d’invitation au Centre des dirigeants"), ("situation", "Exposer une situation", "Demande au Centre des dirigeants"),
         ("evenement", "Inviter un expert à un événement", "Invitation d’un expert"), ("autre", "Autre", "Message au Centre des dirigeants")]
contact = ph("contact.html", "Nous joindre", "Nous joindre", "Demandez <em>votre invitation.</em>",
             "Le Centre est réservé aux clients de nos collaborateurs. Présentez-vous en quelques lignes : la coordination vous répond en 24 heures ouvrables.", "bureau-sourire", "Dirigeante souriante à son bureau") + f'''
<section class="fin" id="formulaire" style="margin-top:clamp(10px,2vw,24px)">
  <div class="w g">
    <div>
      <span class="eb">{MARQUE} Votre point de contact</span>
      <div class="marie" style="margin-top:22px"><span class="marie-mq">{MARQUE}</span><div><b>Coordination du Centre</b><br><span>Accueil des demandes, coordination et suivis</span></div></div>
      <ol class="apres">
        <li><b class="n">1</b><span>La coordination lit votre demande et vous répond.</span></li>
        <li><b class="n">2</b><span>Un court échange pour faire connaissance et comprendre vos besoins.</span></li>
        <li><b class="n">3</b><span>Votre accès au Centre et, au besoin, la mise en relation avec les bons experts.</span></li>
      </ol>
      <p style="margin-top:26px">Par courriel : <b>{MAIL}</b></p>
    </div>
    <div>
      <form id="form" novalidate>
        <span style="font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--d)">Votre demande</span>
        <div class="types" role="radiogroup" aria-label="Type de demande">{"".join(f'<label><input type="radio" name="type" value="{v}" data-l="{l2}"{" checked" if i==0 else ""}> {l}</label>' for i,(v,l,l2) in enumerate(TYPES))}</div>
        <label for="nom">Nom</label><input id="nom" name="nom" autocomplete="name">
        <label for="org">Organisation et rôle</label><input id="org" name="org" autocomplete="organization">
        <label for="mail">Courriel</label><input id="mail" name="mail" type="email" autocomplete="email">
        <label for="msg">Votre message</label><textarea id="msg" name="msg" placeholder="Votre organisation, le collaborateur qui vous réfère et ce que vous cherchez…"></textarea>
        <div class="pot" aria-hidden="true"><input id="site_web" name="site_web" tabindex="-1" autocomplete="off" aria-label="site"></div>
        <label class="consent"><input type="checkbox" id="ok" name="consentement" value="oui"> <span>J’accepte que le Centre des dirigeants utilise ces renseignements pour répondre à ma demande et, au besoin, les transmette aux seuls experts concernés. <a href="politique-confidentialite.html">Politique de confidentialité</a></span></label>
        <div style="margin-top:8px"><button class="btn" type="submit" id="envoyer">Envoyer ma demande <span class="fl">→</span></button></div>
        <p class="delai">Réponse personnelle en 24 heures ouvrables.</p>
        <p class="err" id="err" role="alert"></p>
      </form>
      <div class="ret" id="merci" role="status"><b style="font-size:1.4rem">Merci. Votre demande est bien reçue.</b><p style="margin-top:8px">La coordination du Centre vous répondra en 24 heures ouvrables.</p></div>
      <div class="ret" id="ret" role="status"><b>Votre message est prêt.</b><p>Envoyez-le à {MAIL}. Si votre messagerie ne s’ouvre pas, copiez le texte.</p><pre></pre><a class="btn" id="ouvrir" href="#">Ouvrir ma messagerie <span class="fl">→</span></a> <button class="btn or" type="button" id="copier">Copier</button></div>
    </div>
  </div>
</section>
<section class="sec" id="faq">
  <div class="w sv">
    <div class="ap"><span class="eb">{MARQUE} Questions fréquentes</span><h2 class="grand" style="font-size:clamp(2.2rem,4.4vw,3.8rem)">Avant de nous écrire.</h2></div>
    <div class="faq ap">{faq_html(FAQ)}</div>
  </div>
</section>
'''
page("contact.html", "Nous joindre | Centre des dirigeants, Gatineau",
     "Exposez votre situation, demandez une invitation à la communauté ou invitez un expert. Réponse personnelle en 24 heures ouvrables.",
     contact, nom="Nous joindre", typepage=["ContactPage", "FAQPage"], ld_extra=faq_ld(FAQ))

# ======================= POLITIQUE DE CONFIDENTIALITÉ =======================
pol_src = open(os.path.join(HERE, "v7.py"), encoding="utf-8").read()
m = re.search(r'<main class="w">(.*?)</main>', pol_src, re.S)
pol = m.group(1)
pol = pol.replace('<h2>9. Témoins et mesure d’audience</h2>', '''<h2>9. Infolettre ENTRE NOUS</h2>
<p>Si vous vous abonnez à ENTRE NOUS, nous utilisons votre prénom et votre courriel uniquement pour vous l’envoyer, avec votre consentement exprès, conformément à la Loi canadienne anti-pourriel. Chaque envoi comprend un lien de désabonnement, et vous pouvez vous désabonner en tout temps en nous écrivant. L’infolettre est envoyée au moyen de Mailchimp, dont les serveurs sont situés à l’extérieur du Québec.</p>

<h2>10. Témoins et mesure d’audience</h2>''').replace('<h2>10. Modifications</h2>', '<h2>11. Modifications</h2>')
pol = pol.replace("{{", "{").replace("}}", "}")
politique = f'''<section class="sec pol"><div class="w" style="max-width:820px;padding-top:110px">{pol}</div></section>'''
page("politique-confidentialite.html", "Politique de confidentialité | Centre des dirigeants",
     "Comment le Centre des dirigeants recueille, utilise, communique et protège vos renseignements personnels, conformément à la Loi 25 du Québec.",
     politique, nom="Politique de confidentialité", solide=True)

# ================================ CSS =================================
base = open(os.path.join(OUT, "css", "base.css"), encoding="utf-8").read().replace("url(fonts/", "url(../fonts/")
extra = open(os.path.join(HERE, "site8_extra.css"), encoding="utf-8").read()
plus = '''
.pied2{background:var(--m);color:#B9C7D2;padding:70px 0 34px;margin-top:clamp(10px,2vw,24px)}
.pied2 .pg{display:grid;grid-template-columns:1.6fr 1fr 1fr 1.2fr;gap:40px}
.pied2 img{height:52px;width:auto;filter:brightness(0) invert(1)}
.pied2 p{margin-top:16px;max-width:36ch;font-size:.98rem}
.pied2 h4{color:#fff;font-size:1rem;margin-bottom:12px}
.pied2 a,.pied2 span{display:block;text-decoration:none;font-size:.98rem;margin:6px 0;word-break:break-word}
.pied2 a:hover{color:var(--o)}
.pied2 .pb{margin-top:50px;padding-top:22px;border-top:1px solid rgba(255,255,255,.14);display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;font-size:.88rem}
.pied2 .pb a,.pied2 .pb span{display:inline;margin:0}
@media(max-width:900px){.pied2 .pg{grid-template-columns:1fr 1fr}}@media(max-width:560px){.pied2 .pg{grid-template-columns:1fr}}
.sauter{position:absolute;left:-9999px;top:10px;z-index:200;background:var(--o);color:var(--m);padding:10px 16px;border-radius:8px;font-weight:600}.sauter:focus{left:10px}
.fin .g{display:grid;grid-template-columns:1fr 1fr;gap:6vw;align-items:center}
.cta-t{font-size:clamp(2.8rem,6.6vw,6.4rem)!important;line-height:.9!important;letter-spacing:-.05em}
.fin .fin-photo{max-width:none;margin:0;aspect-ratio:4/3.6}
#formulaire .g{align-items:start}
@media(max-width:820px){.fin .g{grid-template-columns:1fr}}
.pol h1{font-size:clamp(2.2rem,5vw,3.4rem);line-height:1;letter-spacing:-.03em;margin:30px 0 10px}
.pol h2{font-size:1.4rem;margin:40px 0 10px}.pol p,.pol li{color:#2B3E4C}.pol ul{padding-left:22px}.pol a{font-weight:700}
.pol .brouillon{background:#fff;border-left:5px solid var(--of);border-radius:10px;padding:16px 20px;font-size:.95rem}
.pol .cases{background:#fff;border-radius:16px;padding:20px 24px}.pol .maj{color:var(--d)}
'''
open(os.path.join(OUT, "css", "site.css"), "w", encoding="utf-8").write(base + extra + plus)

# ============================ 404 ============================
page("404.html", "Page introuvable | Centre des dirigeants", "Cette page n’existe pas ou a été déplacée.", f'''<section class="sec p404">
  <div class="w">
    <div class="num404 ap">404</div>
    <span class="eb ap" style="margin-top:24px">{MARQUE} Page introuvable</span>
    <h1 class="grand ap" style="margin-top:14px">Ce chemin ne mène <em>nulle part.</em></h1>
    <p class="int ap">La page que vous cherchez n’existe pas ou a été déplacée. Les bonnes expertises, elles, sont toujours au même endroit.</p>
    <div class="ap" style="display:flex;gap:14px;flex-wrap:wrap;margin-top:30px"><a class="btn" href="index.html">Retour à l’accueil <span class="fl">→</span></a><a class="btn or" href="contact.html">Écrire au Centre <span class="fl">→</span></a></div>
  </div>
</section>''', nom="Page introuvable", solide=True)
_p = os.path.join(OUT, "404.html"); _h = open(_p, encoding="utf-8").read()
_h = _h.replace("<head>", '<head>\n<base href="/">\n<meta name="robots" content="noindex">', 1)
_h = re.sub(r'<link rel="canonical"[^>]*>\n?', "", _h)
open(_p, "w", encoding="utf-8").write(_h)

# ============================ SITEMAP, ROBOTS, LLMS ============================
PAGES = ["index.html", "fonctionnement.html", "expertises.html", "experts.html"] + [f"expert-{e['slug']}.html" for e in EXPERTS_FICHES] + ["communaute.html", "ressources.html", "agenda.html", "contact.html", "politique-confidentialite.html"]
pr = {"index.html": "1.0", "politique-confidentialite.html": "0.3"}
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{url(p)}</loc><lastmod>2026-11-11</lastmod><priority>{pr.get(p,'0.8')}</priority></url>\n" for p in PAGES) + "</urlset>\n")
fichiers_robots_tmp = os.path.join(OUT, "_tmp"); os.makedirs(fichiers_robots_tmp, exist_ok=True)
fichiers_robots(fichiers_robots_tmp, ["index.html"], EXPERTS, EXPERTISES, FAQ)
os.replace(os.path.join(fichiers_robots_tmp, "robots.txt"), os.path.join(OUT, "robots.txt"))
ll = open(os.path.join(fichiers_robots_tmp, "llms.txt"), encoding="utf-8").read()
ll = ll.replace("> Réseau de neuf collaborateurs experts,", "> Réseau de neuf collaborateurs experts et communauté de pairs sur invitation,")
ll = ll[:ll.index("## Pages")] + """## Communauté
- Cercles de dirigeants sur invitation, réservés aux pairs (les experts du réseau n’y participent pas).
- Règle de confidentialité stricte : rien de ce qui se dit dans un cercle n’en sort.
- Portail des membres : Salle de réflexion, Boîte à outils, Espace décision, Archives vivantes, Diagnostics, Salle de préparation.

## Infolettre
- ENTRE NOUS : une réflexion par édition, signée par une personne.

## Pages
""" + "".join(f"- [{n}]({url(p)})\n" for p, n in [("index.html", "Accueil"), ("fonctionnement.html", "Comment ça fonctionne"), ("expertises.html", "Expertises et outils"), ("experts.html", "Les experts")] + [(f"expert-{e['slug']}.html", e["nom"].replace(" (Marcan)","") + " : " + e["titre"]) for e in EXPERTS_FICHES] + [("communaute.html", "Communauté de pairs"), ("ressources.html", "Ressources et infolettre"), ("agenda.html", "Agenda"), ("contact.html", "Nous joindre et FAQ")])
open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write(ll)
import shutil; shutil.rmtree(fichiers_robots_tmp)
print("ok", len(PAGES), "pages")
