#!/usr/bin/env python3
"""Génère les pages du site du Centre des dirigeants dans ../site"""
import os, sys

OUT = sys.argv[1]
COURRIEL = "info@centredesdirigeants.ca"
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "seo.py"), encoding="utf-8").read())
FAQ = [
    ("Qu’est-ce que le Centre des dirigeants ?", "Le Centre des dirigeants est un réseau de collaborateurs experts basé à Gatineau. Il accompagne les dirigeants d’entreprises et d’organisations en stratégie, finances, ressources humaines, communications de crise, médiation, santé mentale au travail, protection des données et intelligence artificielle, à partir d’une seule prise de contact."),
    ("À qui s’adresse le Centre ?", "Aux dirigeants d’entreprises et d’organisations, surtout des PME, mais aussi des OBNL et de grandes organisations : propriétaires, directions générales, présidences de conseil d’administration et équipes de direction."),
    ("Faut-il savoir de quel expert on a besoin ?", "Non. C’est précisément le rôle du Centre. Vous décrivez la situation dans vos mots et la coordination du Centre vous oriente vers le ou les experts pertinents."),
    ("Comment accéder au Centre ?", "Le Centre est réservé aux clients de ses collaborateurs. Demandez une invitation par le formulaire du site ou à info@centredesdirigeants.ca. La coordination vous répond en 24 heures ouvrables."),
    ("Qu’est-ce que le continuum PUR ?", "PUR signifie Prévention, Urgence, Reconstruction. Le Centre intervient avant une difficulté pour l’anticiper, pendant une crise pour mobiliser rapidement les bonnes expertises, et après pour rétablir le dialogue et préparer la suite."),
    ("Le Centre peut-il intervenir en situation de crise ?", "Oui. En urgence, le Centre établit les priorités et mobilise rapidement les expertises nécessaires : communications de crise, finances, relations gouvernementales, soutien psychologique ou médiation."),
    ("Est-ce un engagement à long terme ?", "Non. L’accompagnement peut être ponctuel ou s’inscrire dans la durée, selon les besoins de l’organisation."),
    ("Qui a fondé le Centre des dirigeants ?", "France Bélisle et Nicolas Roy, cofondateurs et coprésidents de Posture Inc., ont lancé le Centre en novembre 2026 à Gatineau."),
]

NAV = [
    ("index.html", "Accueil"),
    ("continuum.html", "Le continuum PUR"),
    ("expertises.html", "Expertises"),
    ("experts.html", "Les experts"),
    ("demarche.html", "La démarche"),
]

def entete(courante):
    liens = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == courante else ""}>{t}</a>'
        for h, t in NAV if h != "index.html"
    )
    return f'''<header class="entete" id="entete">
  <div class="wrap">
    <a class="marque" href="index.html" aria-label="Centre des dirigeants, accueil"><img src="img/logo.png" alt="Centre des dirigeants" width="900" height="330"></a>
    <button class="menu-btn" aria-label="Ouvrir le menu" aria-expanded="false" onclick="var e=document.getElementById('entete');var o=e.classList.toggle('ouvert');this.setAttribute('aria-expanded',o)"><span></span></button>
    <nav class="nav" aria-label="Navigation principale">
      {liens}
      <a class="btn btn--or" href="contact.html">Nous écrire <span class="fl">→</span></a>
    </nav>
  </div>
</header>'''

PIED = f'''<footer class="pied">
  <div class="wrap">
    <div class="haut">
      <div>
        <img src="img/logo.png" alt="Centre des dirigeants" width="900" height="330">
        <p style="margin-top:20px;max-width:36ch">Un réseau de collaborateurs experts pour les dirigeants d’entreprises et d’organisations. Les bonnes expertises. Au bon moment.</p>
        <p class="pur">Prévention • Urgence • Reconstruction</p>
      </div>
      <div>
        <h4>Le Centre</h4>
        <ul>
          <li><a href="continuum.html">Le continuum PUR</a></li>
          <li><a href="expertises.html">Expertises et outils</a></li>
          <li><a href="experts.html">Les experts</a></li>
          <li><a href="demarche.html">La démarche</a></li>
        </ul>
      </div>
      <div>
        <h4>Nous joindre</h4>
        <ul>
          <li><a href="contact.html">Exposer votre situation</a></li>
          <li class="courriel">{COURRIEL}</li>
          <li>Gatineau, Québec</li>
        </ul>
      </div>
    </div>
    <div class="bas">
      <span>© 2026 Centre des dirigeants. Une initiative de Posture Inc.</span>
      <span>Accès confidentiel, sans engagement</span>
    </div>
  </div>
</footer>
<script>
(function(){{
  // Titres révélés mot à mot
  document.querySelectorAll('main h2, .entree h1').forEach(function(h){{
    if(h.closest('.galerie')||h.dataset.fait)return;h.dataset.fait=1;
    var w=h.innerHTML.split(/(<[^>]+>|\\s+)/).filter(Boolean),i=0;
    h.innerHTML=w.map(function(t){{if(/^<|^\\s+$/.test(t))return t;return '<span class="mo"><span style="transition-delay:'+(i++*0.05)+'s">'+t+'</span></span>'}}).join('');
    h.classList.add('decoupe');
  }});
  var ob=('IntersectionObserver' in window)?new IntersectionObserver(function(en){{en.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('montre');ob.unobserve(x.target)}}}})}},{{threshold:.2}}):null;
  document.querySelectorAll('.decoupe').forEach(function(h){{ob?ob.observe(h):h.classList.add('montre')}});
  // Curseur
  if(window.matchMedia('(pointer:fine)').matches&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches){{
    var c=document.getElementById('curseur'),d=document.getElementById('curseurPt'),x=0,y=0,cx=0,cy=0;document.body.classList.add('a-curseur');
    window.addEventListener('pointermove',function(e){{document.body.classList.add('bouge');x=e.clientX;y=e.clientY;d.style.transform='translate('+x+'px,'+y+'px)'}});
    (function boucle(){{cx+=(x-cx)*.18;cy+=(y-cy)*.18;c.style.transform='translate('+cx+'px,'+cy+'px)';requestAnimationFrame(boucle)}})();
    document.addEventListener('pointerover',function(e){{c.classList.toggle('gros',!!e.target.closest('a,button,summary,.portrait'))}});
  }}
}})();
(function(){{
  var h=document.getElementById('entete'),rs=document.querySelectorAll('.roue');
  function f(){{h.classList.toggle('plein',window.scrollY>40);rs.forEach(function(r){{r.style.transform='rotate('+(window.scrollY*0.06)+'deg)'}})}}
  f();window.addEventListener('scroll',f,{{passive:true}});
}})();
(function(){{
  try{{
    var els=document.querySelectorAll('.apparait');
    if(!('IntersectionObserver' in window)){{els.forEach(function(e){{e.classList.add('vu')}});return}}
    var io=new IntersectionObserver(function(en){{en.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('vu');io.unobserve(x.target)}}}})}},{{threshold:.12}});
    els.forEach(function(e){{io.observe(e)}});
  }}catch(e){{document.querySelectorAll('.apparait').forEach(function(x){{x.classList.add('vu')}})}}
}})();
</script>'''

INTRO = """<div class="intro" id="intro" aria-hidden="true"><span class="ig"></span><span class="id"></span></div>
<script>try{if(sessionStorage.getItem('cdd-intro')){document.getElementById('intro').remove()}else{sessionStorage.setItem('cdd-intro','1')}}catch(e){}</script>"""

def fil(fichier):
    if fichier == "index.html":
        return ""
    return f'<nav class="fil" aria-label="Fil d’Ariane"><a href="index.html">Accueil</a><span>/</span><span aria-current="page">{SEO[fichier]["nom"]}</span></nav>'

def page(fichier, titre, description, corps):
    corps = corps.replace('<div class="wrap apparait">\n    <span class="eyebrow">', '<div class="wrap apparait">\n    ' + fil(fichier) + '\n    <span class="eyebrow">', 1)
    html = f'''<!DOCTYPE html>
<html lang="fr-CA">
<head>
{tete(fichier, titre, description, EXPERTS, EXPERTISES, FAQ)}
</head>
<body class="v2">
<a class="sauter" href="#contenu">Aller au contenu</a>
{INTRO if fichier == "index.html" else ""}
<div class="curseur" id="curseur" aria-hidden="true"></div><div class="curseur-pt" id="curseurPt" aria-hidden="true"></div>
{entete(fichier)}
<main id="contenu">
{corps}
</main>
{PIED}
</body>
</html>
'''
    import re
    html = re.sub(r'(src="img/[a-z0-9-]+)\.jpg', r'\1.webp', html)
    html = html.replace('img/roue-pur.png', 'img/roue-pur.webp')
    with open(os.path.join(OUT, fichier), "w", encoding="utf-8") as f:
        f.write(html)

def cta(titre="Une seule prise de contact suffit.", texte="Décrivez votre situation en quelques lignes. Marie-Eve vous répond personnellement et vous met en relation avec la bonne expertise."):
    return f'''<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="cta apparait">
      <span class="demi demi--g" style="right:-90px;top:-50px;width:180px;height:360px;background:var(--moutarde)"></span>
      <span class="demi demi--g" style="right:120px;bottom:-120px;width:120px;height:240px;background:#183A50"></span>
      <div class="cta-int">
        <h2>{titre}</h2>
        <p>{texte}</p>
        <div class="actions">
          <a class="btn btn--or" href="contact.html">Exposer votre situation <span class="fl">→</span></a>
        </div>
        <p style="margin-top:22px;font-size:1rem">Ou directement : <span class="courriel">{COURRIEL}</span></p>
      </div>
    </div>
  </div>
</section>'''

EXPERTS = [
    ("nicolas-roy", "Nicolas Roy", "Adm.A., CRHA", "Cofondateur",
     "Stratégie, gestion, ressources humaines et coaching de dirigeants.",
     ["Stratégie", "Ressources humaines", "Coaching et leadership"]),
    ("france-belisle", "France Bélisle", "", "Cofondatrice",
     "Communications stratégiques et de crise, affaires publiques, gouvernance et médiation. Journaliste de formation, première femme mairesse de Gatineau, formée en médiation.",
     ["Communications de crise", "Gouvernance", "Médiation"]),
    ("yannick-beaulieu", "Yannick Beaulieu", "CPA, MBA", "Direction financière",
     "Direction financière à la demande, analyse de rentabilité, prévisions financières et financement.",
     ["Finances", "Rentabilité", "Financement"]),
    ("andreanne-thibault", "Andréanne Thibault", "CRIA", "Stratège en expérience employé et GRH",
     "Ressources humaines, expérience employé, culture organisationnelle et marque employeur.",
     ["Expérience employé", "Culture", "Marque employeur"]),
    ("chantal-dufort", "Chantal Dufort", "", "Chantal Dufort Inc.",
     "Conférences, formations et accompagnement en santé mentale au travail et en gestion du stress.",
     ["Santé psychologique", "Gestion du stress", "Formation"]),
    ("daniel-feeny", "Daniel Feeny", "", "Feeny Corp.",
     "Affaires publiques, marketing et relations gouvernementales.",
     ["Affaires publiques", "Relations gouvernementales", "Marketing"]),
    ("sophie-ann-bellisle", "Sophie Ann Bellisle", "", "Privacense",
     "Gouvernance des données, gestion des risques, protection de la vie privée et conformité.",
     ["Protection des données", "Conformité", "Gestion des risques"]),
    ("marc-antoine-laramee", "Marc-Antoine Laramée", "", "Quartier AI",
     "Chef de la croissance. Stratégie, adoption et déploiement de l’IA agentique au niveau opérationnel, performance et optimisation.",
     ["IA agentique", "Transformation IA des PME", "Optimisation"]),
    ("marie-eve-venner", "Marie-Eve Venner", "", "Coordination du Centre",
     "Coordination administrative, soutien organisationnel et logistique, suivi des demandes et communications.",
     ["Accueil des demandes", "Coordination", "Suivis"]),
]

EXPERTISES = [
    ("Stratégie et gouvernance", "Clarifier où vous allez, qui décide quoi et comment le conseil joue son rôle.", "Nicolas Roy, France Bélisle, Daniel Feeny"),
    ("Direction financière et rentabilité", "Un CFO à la demande pour lire vos chiffres, prévoir et financer la suite.", "Yannick Beaulieu"),
    ("Ressources humaines", "Structurer, recruter, retenir. Bâtir une culture qui tient sous pression.", "Nicolas Roy, Andréanne Thibault"),
    ("Communications", "Communications stratégiques et de crise, affaires publiques, relations gouvernementales.", "France Bélisle, Daniel Feeny"),
    ("Sondages internes et externes", "Mesurer ce que pensent vraiment vos employés, clients ou partenaires avant de décider.", "Équipe du Centre"),
    ("Tests psychométriques", "Évaluations AtmanPro pour mieux recruter, développer et composer vos équipes.", "Nicolas Roy, Andréanne Thibault"),
    ("Médiation", "Dénouer un conflit avant qu’il ne coûte une équipe, un client ou un associé.", "France Bélisle"),
    ("Santé mentale au travail", "Prévenir l’épuisement, outiller les gestionnaires, accompagner après un choc.", "Chantal Dufort"),
    ("Protection des données", "Gouvernance des données, vie privée et conformité, sans paralyser l’organisation.", "Sophie Ann Bellisle"),
    ("Intelligence artificielle", "Adopter l’IA là où elle fait gagner du temps, pas là où elle fait du bruit.", "Marc-Antoine Laramée"),
]

def bandeau_experts():
    return '<div class="bandeau-experts">' + "".join(
        f'<img src="img/{s}.jpg" alt="{n}" title="{n}" width="84" height="84">' for s, n, *_ in EXPERTS
    ) + '</div>'

# ---------------------------------------------------------------- ACCUEIL
accueil = f'''
<section class="hero">
  <span class="demi demi--d" style="left:-90px;top:120px;width:120px;height:240px;background:var(--ciel)"></span>
  <div class="wrap">
    <div class="apparait">
      <span class="eyebrow">Gatineau · PME et OBNL</span>
      <h1>Les bonnes expertises. <span class="ligne2">Au bon moment.</span></h1>
      <p class="lead">Quand on dirige, les enjeux se croisent et le temps manque pour chercher de l’aide. Le Centre des dirigeants réunit neuf professionnels de confiance derrière une seule porte d’entrée.</p>
      <div class="actions">
        <a class="btn btn--or" href="contact.html">Exposer votre situation <span class="fl">→</span></a>
        <a class="btn btn--ligne" href="demarche.html">Voir comment ça fonctionne</a>
      </div>
      <div class="pur-bande"><span>Prévention</span><i></i><span>Urgence</span><i></i><span>Reconstruction</span></div>
    </div>
    <div class="hero-visuel apparait">
      <div class="pastille"></div>
      <div class="photo"><img src="img/photo-dirigeante.jpg" alt="Dirigeante à son bureau" width="1800" height="1200"></div>
      <div class="carte"><b>Une seule prise de contact</b><span>Vous expliquez. On vous oriente vers la bonne personne.</span></div>
    </div>
  </div>
</section>

<section class="section section--marine">
  <div class="wrap">
    <div class="tete">
      <div class="apparait"><span class="eyebrow">Si vous vous reconnaissez</span><h2>Vous n’avez pas besoin d’un fournisseur de plus. Vous avez besoin de savoir qui appeler.</h2></div>
    </div>
    <ul class="miroir apparait">
      <li>Votre agenda déborde et les décisions importantes attendent toujours le prochain vendredi tranquille.</li>
      <li>Un enjeu RH devient un enjeu financier, puis un enjeu d’image. Et c’est vous qui faites le lien entre les trois.</li>
      <li>Vous êtes entouré toute la journée, sans personne à qui parler de ce qui vous préoccupe vraiment.</li>
      <li>Chercher le bon expert est devenu une tâche de plus sur votre liste.</li>
    </ul>
    <p class="chute apparait">Demander un coup de main, c’est une force. Le Centre est là pour que ce soit simple.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="tete">
      <div class="apparait"><span class="eyebrow">Comment ça fonctionne</span><h2>Moins de démarches. Plus de temps pour avancer.</h2></div>
      <p class="lead apparait">Pas de formulaire à cases, pas de liste à magasiner. Vous parlez à une personne, qui vous met en relation avec les bonnes expertises.</p>
    </div>
    <div class="grille g3">
      <div class="carte-b apparait"><span class="num">1</span><h3>Vous exposez votre situation</h3><p>Quelques lignes ou un appel. Ce qui se passe, ce qui presse, ce qui vous empêche de dormir.</p></div>
      <div class="carte-b apparait"><span class="num">2</span><h3>On vous oriente</h3><p>Marie-Eve analyse votre demande et vous met en relation avec le ou les collaborateurs experts pertinents.</p></div>
      <div class="carte-b apparait"><span class="num">3</span><h3>Vous passez à l’action</h3><p>Un appui ponctuel ou un accompagnement dans la durée, selon ce que la situation demande.</p></div>
    </div>
  </div>
</section>

<section class="section section--blanc">
  <div class="wrap pur-grille">
    <img class="roue apparait" src="img/roue-pur.png" alt="Le continuum PUR : Prévention, Urgence, Reconstruction" width="700" height="700">
    <div class="apparait">
      <span class="eyebrow">Le continuum PUR</span>
      <h2>Avant, pendant ou après la tempête.</h2>
      <p class="lead" style="margin-top:20px">Le Centre intervient à trois moments de la vie d’une organisation. Et il tient compte autant de ses besoins que de la réalité de la personne qui la dirige.</p>
      <ul class="puces">
        <li><span><strong>Prévention.</strong> Clarifier les priorités, renforcer les pratiques, anticiper les enjeux.</span></li>
        <li><span><strong>Urgence.</strong> Établir les priorités et mobiliser rapidement les bonnes expertises.</span></li>
        <li><span><strong>Reconstruction.</strong> Rétablir le dialogue, consolider les équipes, préparer la suite.</span></li>
      </ul>
      <div class="actions"><a class="btn btn--ligne" href="continuum.html">Explorer le continuum <span class="fl">→</span></a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="tete">
      <div class="apparait"><span class="eyebrow">Expertises</span><h2>Des besoins différents. Un même réseau.</h2></div>
      <p class="lead apparait">Vos responsabilités touchent plusieurs domaines à la fois. Les expertises du Centre aussi.</p>
    </div>
    <div class="grille g4">
      {"".join(f'<div class="expertise apparait"><span class="ico"></span><h3>{t}</h3><p>{d}</p></div>' for t, d, _ in EXPERTISES[:8])}
    </div>
    <div class="actions"><a class="btn btn--ligne" href="expertises.html">Toutes les expertises et les outils <span class="fl">→</span></a></div>
  </div>
</section>

<section class="section section--ciel">
  <div class="wrap" style="text-align:center">
    <span class="eyebrow apparait">Un réseau de confiance</span>
    <h2 class="apparait" style="max-width:20ch;margin:0 auto 34px">Neuf professionnels. Une seule porte d’entrée.</h2>
    <div class="apparait">{bandeau_experts()}</div>
    <div class="actions apparait" style="justify-content:center"><a class="btn btn--ligne" href="experts.html">Rencontrer les experts <span class="fl">→</span></a></div>
  </div>
</section>

<section class="section">
  <div class="wrap grille g2" style="align-items:center;gap:clamp(32px,6vw,90px)">
    <div class="apparait">
      <p class="citation">On peut être entouré toute la journée et ne pas savoir à qui parler de ce qui nous préoccupe. Demander un coup de main, c’est une force.</p>
      <p class="auteur"><b>France Bélisle</b>, cofondatrice</p>
    </div>
    <div class="apparait">
      <p class="citation">Les dirigeants jonglent avec des enjeux qui se croisent. Ils ont besoin de gens de confiance pour y voir clair.</p>
      <p class="auteur"><b>Nicolas Roy</b>, Adm.A., CRHA, cofondateur</p>
    </div>
  </div>
</section>

{cta()}
'''
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "accueil_v3.py"), encoding="utf-8").read())
page("index.html", "Centre des dirigeants | Les bonnes expertises. Au bon moment.",
     "Un réseau de collaborateurs experts pour les dirigeants d’entreprises et d’organisations à Gatineau. Une seule prise de contact pour être orienté vers les bonnes expertises.",
     accueil)

# ---------------------------------------------------------------- CONTINUUM
continuum = f'''
<section class="entree">
  <span class="demi demi--g" style="right:-40px;top:40px;width:140px;height:280px;background:var(--moutarde)"></span>
  <span class="demi demi--d" style="right:110px;top:110px;width:110px;height:220px;background:var(--marine)"></span>
  <div class="wrap apparait">
    <span class="eyebrow">Le continuum PUR</span>
    <h1>Prévention. Urgence. Reconstruction.</h1>
    <p class="lead">Le bon appui dépend du moment. Le Centre organise son accompagnement autour de trois axes complémentaires, pour l’organisation comme pour la personne qui la dirige.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="axe axe--p apparait">
      <div>
        <span class="etiquette">Axe 1</span>
        <h3>Prévention</h3>
        <p class="question">Tout va bien. C’est justement le moment.</p>
        <p style="margin-top:12px">Clarifier les priorités, renforcer les pratiques et anticiper les enjeux avant qu’ils ne deviennent des urgences.</p>
      </div>
      <div>
        <p class="signes">Vous êtes ici si…</p>
        <ul>
          <li>Votre organisation grandit plus vite que sa structure.</li>
          <li>Vous voulez valider votre plan stratégique ou votre gouvernance.</li>
          <li>Vous sentez une tension dans l’équipe sans pouvoir la nommer.</li>
          <li>Vos obligations en santé psychologique ou en protection des données vous semblent floues.</li>
        </ul>
      </div>
    </div>
    <div class="axe axe--u apparait">
      <div>
        <span class="etiquette">Axe 2</span>
        <h3>Urgence</h3>
        <p class="question">Ça brûle. Il faut les bonnes personnes, maintenant.</p>
        <p style="margin-top:12px">Établir les priorités et mobiliser rapidement les bonnes expertises pour traverser la situation.</p>
      </div>
      <div>
        <p class="signes">Vous êtes ici si…</p>
        <ul>
          <li>Une crise médiatique, financière ou humaine vient d’éclater.</li>
          <li>Un départ clé, un conflit ou une plainte déstabilise l’organisation.</li>
          <li>Les liquidités se resserrent et une décision ne peut plus attendre.</li>
          <li>Vous portez seul une situation que vous ne pouvez pas partager à l’interne.</li>
        </ul>
      </div>
    </div>
    <div class="axe axe--r apparait">
      <div>
        <span class="etiquette">Axe 3</span>
        <h3>Reconstruction</h3>
        <p class="question">Le pire est passé. Reste à rebâtir.</p>
        <p style="margin-top:12px">Rétablir le dialogue, consolider les équipes et préparer la suite, sans répéter ce qui a mené à la crise.</p>
      </div>
      <div>
        <p class="signes">Vous êtes ici si…</p>
        <ul>
          <li>La confiance s’est effritée entre la direction et les équipes.</li>
          <li>Vous devez restructurer après une période difficile.</li>
          <li>Vous voulez tirer les leçons d’une crise et vous en servir.</li>
          <li>Vous-même avez besoin de reprendre votre souffle.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--blanc">
  <div class="wrap pur-grille">
    <img class="roue apparait" src="img/roue-pur.png" alt="Roue du continuum PUR" width="700" height="700">
    <div class="apparait">
      <span class="eyebrow">Pourquoi un continuum</span>
      <h2>Les trois moments se touchent.</h2>
      <p class="lead" style="margin-top:20px">Une prévention négligée devient une urgence. Une urgence mal refermée revient. C’est pourquoi le même réseau vous accompagne d’un moment à l’autre, sans tout recommencer avec de nouveaux interlocuteurs.</p>
      <p style="margin-top:18px">Et parce qu’une organisation ne va jamais mieux que la personne qui la dirige, le continuum considère aussi votre réalité : votre charge, votre isolement, votre énergie.</p>
    </div>
  </div>
</section>

{cta("Vous ne savez pas dans quel axe vous êtes ?", "Pas grave. Décrivez la situation telle que vous la vivez. C’est notre travail de la situer et de trouver la bonne expertise.")}
'''
page("continuum.html", "Le continuum PUR | Centre des dirigeants",
     "Prévention, Urgence, Reconstruction : les trois axes d’accompagnement du Centre des dirigeants.", continuum)

# ---------------------------------------------------------------- EXPERTISES
expertises = f'''
<section class="entree">
  <span class="demi demi--d" style="right:-30px;top:60px;width:130px;height:260px;background:var(--ciel)"></span>
  <div class="wrap apparait">
    <span class="eyebrow">Expertises et outils</span>
    <h1>Des expertises complémentaires, facilement accessibles.</h1>
    <p class="lead">Stratégie, finances, ressources humaines, communications, santé mentale, données, intelligence artificielle. Vos enjeux se croisent. Nos expertises aussi.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="grille g3">
      {"".join(f'<div class="expertise apparait"><span class="ico"></span><h3>{t}</h3><p>{d}</p><span class="qui">{q}</span></div>' for t, d, q in EXPERTISES)}
      <div class="expertise apparait" style="background:var(--marine);border-color:var(--marine)"><h3 style="color:#fff">Votre enjeu n’est pas dans la liste ?</h3><p style="color:#D9E3EA">Écrivez-nous quand même. Le réseau sait vers qui vous orienter.</p><a class="btn btn--or" href="contact.html" style="margin-top:auto;align-self:flex-start">Nous écrire <span class="fl">→</span></a></div>
    </div>
  </div>
</section>

<section class="section section--marine">
  <div class="wrap">
    <div class="tete">
      <div class="apparait"><span class="eyebrow">Des outils pour aller plus loin</span><h2>Décider sur des faits, pas sur des impressions.</h2></div>
      <p class="lead apparait">Le Centre met aussi à votre disposition des outils de mesure et de diagnostic pour éclairer vos décisions.</p>
    </div>
    <div class="grille g3">
      <div class="carte-b apparait"><span class="num">A</span><h3>Tests psychométriques AtmanPro</h3><p>Mieux comprendre les profils pour recruter juste, développer vos gestionnaires et composer des équipes qui fonctionnent.</p></div>
      <div class="carte-b apparait"><span class="num">S</span><h3>Sondages internes et externes</h3><p>Conçus sur mesure pour recueillir les perceptions de vos employés, clients ou partenaires et établir un diagnostic.</p></div>
      <div class="carte-b apparait"><span class="num">M</span><h3>Adhésion, marque employeur</h3><p>Mesurer et renforcer ce qui donne envie de rester et de joindre votre organisation.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="tete">
      <div class="apparait"><span class="eyebrow">L’offre comprend aussi</span><h2>Des accompagnements de fond.</h2></div>
    </div>
    <div class="grille g3">
      <div class="carte-b apparait"><h3>Planification stratégique</h3><p>Une démarche structurée pour choisir ses priorités, aligner son équipe de direction et s’y tenir.</p></div>
      <div class="carte-b apparait"><h3>Coaching de gestion</h3><p>Un espace pour prendre du recul sur votre rôle, vos décisions et votre façon de diriger.</p></div>
      <div class="carte-b apparait"><h3>Médiation</h3><p>Rétablir le dialogue entre associés, gestionnaires ou équipes quand le conflit bloque l’organisation.</p></div>
    </div>
    <p class="apparait" style="margin-top:34px;max-width:70ch">À venir : des outils en ligne et des activités de formation en lien avec les expertises des collaborateurs. Les clients des collaborateurs experts bénéficient d’un accès privilégié au Centre.</p>
  </div>
</section>

{cta()}
'''
page("expertises.html", "Expertises et outils | Centre des dirigeants",
     "Les expertises et outils offerts par le Centre des dirigeants : stratégie, finances, RH, communications, médiation, santé mentale, données, IA.", expertises)

# ---------------------------------------------------------------- EXPERTS
def carte_expert(s, n, cred, role, desc, tags):
    nom = n + (f'<span style="font-weight:400;color:var(--doux);font-size:.95rem">, {cred}</span>' if cred else "")
    return f'''<article class="expert apparait" id="{s}">
  <div class="ph"><img src="img/{s}.jpg" alt="{n}" width="172" height="172"></div>
  <div class="bio">
    <span class="role">{role}</span>
    <h3>{nom}</h3>
    <p>{desc}</p>
    <div class="tags">{"".join(f'<span class="tag">{t}</span>' for t in tags)}</div>
  </div>
</article>'''

experts = f'''
<section class="entree">
  <span class="demi demi--g" style="right:-40px;top:50px;width:130px;height:260px;background:var(--marine)"></span>
  <span class="demi demi--d" style="right:96px;top:120px;width:100px;height:200px;background:var(--moutarde)"></span>
  <div class="wrap apparait">
    <span class="eyebrow">Les experts du Centre</span>
    <h1>Un réseau de confiance.</h1>
    <p class="lead">Neuf professionnels qui partagent une même volonté : offrir aux dirigeants un accompagnement concret, au moment où ils en ont besoin.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="grille g3">
      {"".join(carte_expert(*e) for e in EXPERTS)}
    </div>
  </div>
</section>

<section class="section section--marine">
  <div class="wrap grille g2" style="align-items:center;gap:clamp(32px,6vw,90px)">
    <div class="apparait">
      <span class="eyebrow">Notre engagement</span>
      <h2>Vos ambitions nous inspirent. Notre réseau vous propulse.</h2>
    </div>
    <div class="apparait">
      <ul class="puces" style="margin-top:0">
        <li><span><strong style="color:#fff">Une seule porte d’entrée.</strong> Vous n’avez pas à identifier vous-même le bon expert.</span></li>
        <li><span><strong style="color:#fff">Des gens de confiance.</strong> Chaque collaborateur a été choisi pour son expertise et sa façon de travailler.</span></li>
        <li><span><strong style="color:#fff">De la discrétion.</strong> Votre situation reste entre vous et les personnes qui vous accompagnent.</span></li>
      </ul>
    </div>
  </div>
</section>

{cta("Pas besoin de choisir qui contacter.", "Décrivez votre situation. On s’occupe de trouver la bonne combinaison d’expertises.")}
'''
page("experts.html", "Les experts | Centre des dirigeants",
     "Les neuf collaborateurs experts du Centre des dirigeants.", experts)

# ---------------------------------------------------------------- DÉMARCHE
demarche = f'''
<section class="entree">
  <span class="demi demi--d" style="right:-30px;top:60px;width:130px;height:260px;background:var(--moutarde)"></span>
  <div class="wrap apparait">
    <span class="eyebrow">La démarche</span>
    <h1>Par où commencer ? Par ici.</h1>
    <p class="lead">Quand tout semble urgent, chercher de l’aide peut devenir une tâche de plus. Le Centre réduit cette démarche à une seule prise de contact.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="etapes">
      <div class="etape apparait"><span class="n">01</span><div><h3>Vous nous écrivez</h3><p>Par courriel ou par le formulaire. Pas besoin de bien formuler le problème : décrivez ce que vous vivez, dans vos mots. Ce qui presse, ce qui accroche, ce que vous avez déjà essayé.</p></div></div>
      <div class="etape apparait"><span class="n">02</span><div><h3>Marie-Eve recueille votre demande</h3><p>Elle prend le temps de comprendre votre situation et vos besoins. Vous parlez à une personne, pas à un système.</p></div></div>
      <div class="etape apparait"><span class="n">03</span><div><h3>Mise en relation avec les bons experts</h3><p>Selon vos besoins, vous êtes orienté vers un ou plusieurs collaborateurs. Si votre enjeu touche plusieurs domaines, l’équipe se coordonne pour vous.</p></div></div>
      <div class="etape apparait"><span class="n">04</span><div><h3>Un accompagnement à votre mesure</h3><p>Ponctuel ou dans la durée. Marie-Eve assure la coordination, l’organisation des rencontres et le suivi de votre demande.</p></div></div>
    </div>
  </div>
</section>

<section class="section section--blanc">
  <div class="wrap grille g2" style="align-items:center;gap:clamp(32px,6vw,90px)">
    <div class="apparait">
      <span class="eyebrow">Votre point de contact</span>
      <h2>Une personne. Pas un répondeur.</h2>
      <p class="lead" style="margin-top:18px">Marie-Eve Venner accueille chaque demande, fait les liens avec les experts et s’assure que rien ne tombe entre deux chaises.</p>
    </div>
    <div class="apparait">
      <div class="personne">
        <img src="img/marie-eve-venner.jpg" alt="Marie-Eve Venner" width="96" height="96">
        <div><b>Marie-Eve Venner</b><span>Coordination et accueil des demandes</span><br><span class="courriel">{COURRIEL}</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="tete"><div class="apparait"><span class="eyebrow">Questions fréquentes</span><h2>Ce qu’on nous demande souvent.</h2></div></div>
    <div class="faq">
      {"".join(f'<details class="apparait"{" open" if i==0 else ""}><summary><h3>{q}</h3><span class="plus" aria-hidden="true"></span></summary><p>{r}</p></details>' for i,(q,r) in enumerate(FAQ))}
    </div>
  </div>
</section>

{cta()}
'''
page("demarche.html", "La démarche | Centre des dirigeants",
     "Comment fonctionne le Centre des dirigeants : une seule prise de contact pour être orienté vers les bonnes expertises.", demarche)

# ---------------------------------------------------------------- CONTACT
contact = f'''
<section class="entree">
  <span class="demi demi--g" style="right:-40px;top:50px;width:130px;height:260px;background:var(--marine)"></span>
  <span class="demi demi--d" style="right:96px;top:120px;width:100px;height:200px;background:var(--moutarde)"></span>
  <div class="wrap apparait">
    <span class="eyebrow">Nous écrire</span>
    <h1>Dites-nous ce qui se passe.</h1>
    <p class="lead">Dans vos mots, sans mettre de forme. Une personne vous lit et vous répond.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap grille g2" style="gap:clamp(32px,6vw,80px);align-items:start">
    <div class="apparait">
      <form class="form" id="formulaire" novalidate>
        <div class="champ"><label for="nom">Votre nom</label><input id="nom" name="nom" autocomplete="name" required></div>
        <div class="champ"><label for="org">Organisation et rôle</label><input id="org" name="org" autocomplete="organization" placeholder="Ex. : directrice générale, OBNL de 40 employés"></div>
        <div class="champ"><label for="mail">Courriel</label><input id="mail" name="mail" type="email" autocomplete="email" required></div>
        <div class="champ"><label for="msg">Votre situation</label><textarea id="msg" name="msg" required placeholder="Ce qui se passe, ce qui presse, ce que vous avez déjà essayé…"></textarea></div>
        <div><button class="btn btn--or" type="submit">Préparer mon message <span class="fl">→</span></button></div>
        <p class="note">Votre message sera adressé à {COURRIEL}. Il est traité avec discrétion et partagé seulement avec les experts concernés.</p>
      </form>
      <div class="retour" id="retour" role="status" aria-live="polite">
        <h3>Votre message est prêt.</h3>
        <p>Envoyez-le à <span class="courriel">{COURRIEL}</span> depuis votre messagerie. Le bouton ci-dessous ouvre votre logiciel de courriel; s’il ne s’ouvre pas, copiez le texte.</p>
        <div class="copie" id="apercu"></div>
        <div class="actions">
          <a class="btn btn--or" id="lienMail" href="#">Ouvrir ma messagerie <span class="fl">→</span></a>
          <button class="btn btn--ligne" type="button" id="copier">Copier le message</button>
        </div>
      </div>
    </div>
    <div class="apparait">
      <div class="personne" style="margin-bottom:22px">
        <img src="img/marie-eve-venner.jpg" alt="Marie-Eve Venner" width="96" height="96">
        <div><b>Marie-Eve Venner</b><span>Votre point de contact au Centre</span></div>
      </div>
      <div class="carte-b">
        <h3>Ce qui se passe ensuite</h3>
        <ul class="puces">
          <li><span>Marie-Eve lit votre message et vous répond personnellement.</span></li>
          <li><span>Au besoin, un court échange pour bien comprendre la situation.</span></li>
          <li><span>Mise en relation avec le ou les experts pertinents.</span></li>
        </ul>
      </div>
      <div class="carte-b" style="margin-top:22px">
        <h3>Par courriel</h3>
        <p class="courriel" style="font-size:1.05rem">{COURRIEL}</p>
        <p style="margin-top:8px">Gatineau, Québec</p>
      </div>
    </div>
  </div>
</section>
<script>
(function(){{
  var f=document.getElementById('formulaire'),r=document.getElementById('retour');
  var corps='';
  f.addEventListener('submit',function(e){{
    e.preventDefault();
    var nom=f.nom.value.trim(),org=f.org.value.trim(),mail=f.mail.value.trim(),msg=f.msg.value.trim();
    if(!nom||!mail||!msg){{
      [f.nom,f.mail,f.msg].forEach(function(c){{c.style.borderColor=c.value.trim()?'':'#C0563B'}});
      return;
    }}
    corps=msg+'\\n\\n'+nom+(org?'\\n'+org:'')+'\\n'+mail;
    document.getElementById('apercu').textContent=corps;
    document.getElementById('lienMail').href='mailto:{COURRIEL}?subject='+encodeURIComponent('Demande au Centre des dirigeants : '+nom)+'&body='+encodeURIComponent(corps);
    f.style.display='none';r.classList.add('visible');r.scrollIntoView({{behavior:'smooth',block:'start'}});
  }});
  document.getElementById('copier').addEventListener('click',function(){{
    var b=this;
    try{{navigator.clipboard.writeText(corps).then(function(){{b.textContent='Message copié'}},function(){{b.textContent='Sélectionnez le texte pour le copier'}})}}catch(err){{b.textContent='Sélectionnez le texte pour le copier'}}
  }});
}})();
</script>
'''
page("contact.html", "Nous écrire | Centre des dirigeants",
     "Exposez votre situation au Centre des dirigeants. Une personne vous lit et vous répond.", contact)

fichiers_robots(OUT, [h for h, _ in NAV] + ["contact.html"], EXPERTS, EXPERTISES, FAQ)
print("ok")
