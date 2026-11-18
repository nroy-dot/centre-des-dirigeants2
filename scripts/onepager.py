#!/usr/bin/env python3
"""Génère les fiches d'une page (format lettre) des experts, dans le gabarit du Centre."""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from experts_data import EXPERTS_FICHES
from playwright.sync_api import sync_playwright

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(RACINE, "polices")
def b64(p): return base64.b64encode(open(p, "rb").read()).decode()
PHOTO = {s: os.path.join(RACINE, "photos-fiches", s + ".jpg") for s in ["france-belisle", "marc-antoine-laramee", "chantal-dufort", "yannick-beaulieu", "sophie-ann-bellisle", "daniel-feeny", "nicolas-roy", "andreanne-thibault"]}

CSS = f"""
@font-face{{font-family:LS;src:url(data:font/ttf;base64,{b64(FONTS+'/LeagueSpartan-Regular.ttf')});font-weight:400}}
@font-face{{font-family:LS;src:url(data:font/ttf;base64,{b64(FONTS+'/LeagueSpartan-SemiBold.ttf')});font-weight:600}}
@font-face{{font-family:LS;src:url(data:font/ttf;base64,{b64(FONTS+'/LeagueSpartan-Bold.ttf')});font-weight:700}}
@page{{size:Letter;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:8.5in;height:11in}}
body{{font-family:LS,sans-serif;color:#0C283A;font-size:var(--fs,9.6pt);line-height:1.32;padding:.38in .5in .3in;display:flex;flex-direction:column;height:11in}}
.top{{display:flex;justify-content:space-between;align-items:center;padding-bottom:.12in;border-bottom:1.2px solid #D5AC59}}
.top h1{{font-size:17pt;font-weight:700;line-height:1}}
.top p{{font-size:9pt;margin-top:4px}}
.logo{{display:flex;align-items:center}}.logo i{{width:.42in;height:.42in;border-radius:50%;background:#0C283A;display:block}}.logo b{{width:.21in;height:.42in;border-radius:0 .42in .42in 0;background:#D5AC59;display:block;margin-left:.02in}}
.band{{display:flex;margin-top:.17in;background:#0C283A;color:#fff;min-height:1.4in}}
.band .t{{flex:1;padding:.18in .22in}}
.band .n{{color:#D5AC59;font-weight:700;font-size:10.5pt}}
.band h2{{font-size:19pt;line-height:1.08;margin:.05in 0 .08in;font-weight:700;max-width:4.2in}}
.band .s{{font-size:9pt;color:#DDE5EC}}
.band .ph{{width:1.5in;background-size:cover;background-position:center 25%}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:.32in;margin-top:.18in;flex:1;align-content:start}}
h3{{font-size:11.6pt;font-weight:700;margin:0 0 .06in;line-height:1.15}}
.col>*+h3{{margin-top:.14in}}
.box{{background:#F0F3F6;border-left:3px solid #D5AC59;padding:.08in .12in;margin-bottom:.08in}}
.box b{{display:block;font-size:10pt;margin-bottom:2px}}
.box .r{{margin-top:3px}}
.cr{{background:#F2EDE7;padding:.09in .13in;margin-bottom:.08in}}
.cr b{{display:block;font-size:10pt;margin-bottom:2px}}
.gr{{background:#F0F3F6;padding:.1in .13in;margin-bottom:.08in}}
.gr.c{{background:#F2EDE7}}
.gr p+p{{margin-top:4px}}
ul{{list-style:none}} li{{padding-left:9px;position:relative;margin:1px 0}} li::before{{content:"•";position:absolute;left:0}}
.foot{{margin-top:.14in;background:#F2EDE7;display:flex;gap:.18in;padding:.12in .16in;align-items:center}}
.foot .m{{width:.95in;height:.95in;border-radius:50%;background:#0C283A;flex:none;display:flex;align-items:center;justify-content:center}}.foot .m svg{{width:.55in;height:.55in}}
.foot h4{{font-size:11.5pt;margin-bottom:5px}}
.foot u{{text-decoration:underline}}
.bas{{display:flex;justify-content:space-between;font-size:8pt;margin-top:.08in}}
.ph-a-valider{{background:#FFF3C4;color:#0C283A;padding:0 2px}}
"""

def html(e):
    def hl(t): return t.replace("[", '<span class="ph-a-valider">[').replace("]", "]</span>")
    exp = "".join(f'<div class="box"><b>{t}</b>{hl(d)}<div class="r"><b style="display:inline">{e["lab"]} :</b> {hl(r)}</div></div>' for t, d, r in e["exp"])
    fac = "".join(f'<div class="cr"><b>{t}</b>{hl(d)}</div>' for t, d in e["facons"])
    pq = ("<ul>" + "".join(f"<li>{hl(x)}</li>" for x in e["pourquoi"]) + "</ul>") if e["pourquoi_liste"] else "".join(f"<p>{hl(x)}</p>" for x in e["pourquoi"])
    qd = "<ul>" + "".join(f"<li>{x}</li>" for x in e["quand"]) + "</ul>" + (f'<p style="margin-top:5px">{e["fin"]}</p>' if e["fin"] else "")
    nom = e["nom"] + (", " + e["cred"] if e["cred"] else "")
    titre = e["titre"]
    return f"""<!DOCTYPE html><html lang="fr-CA"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="top"><div><h1>Centre des dirigeants</h1><p>{e['genre']}</p></div><div class="logo"><i></i><b></b></div></div>
<div class="band"><div class="t"><div class="n">{nom}</div><h2>{titre}</h2><div class="s">{hl(e['sous'])}</div></div><div class="ph" style="background-image:url(data:image/png;base64,{b64(PHOTO[e['slug']])})"></div></div>
<div class="cols">
 <div class="col"><h3>{e['intro_t']}</h3>{''.join(f'<p>{hl(p)}</p>' for p in e['intro'])}<h3>{e['exp_t']}</h3>{exp}<h3>{e['milieux_t']}</h3><p>{hl(e['milieux'])}</p></div>
 <div class="col"><h3>Deux façons de travailler ensemble</h3>{fac}<div class="gr"><h3>Pourquoi collaborer avec moi</h3>{pq}</div><div class="gr c"><h3>{e['quand_t']}</h3>{qd}</div></div>
</div>
<div class="foot"><div class="m"><svg viewBox="0 0 40 40" aria-hidden="true"><path d="M19 4a14 14 0 0 0 0 28z" fill="#fff"/><path d="M21 8a14 14 0 0 1 0 28z" fill="#D5AC59"/></svg></div><div><h4>Planifier une rencontre exploratoire, sans engagement</h4><b>Communiquer avec la coordination du Centre</b><br>Accueil des demandes, coordination et suivis<br><u>info@centredesdirigeants.ca</u></div></div>
<div class="bas"><span>Centre des dirigeants</span><span>Prévention · Urgence · Reconstruction</span></div>
</body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width": 816, "height": 1056})
    for e in EXPERTS_FICHES:
        h = html(e)
        open(os.path.join(OUT, f"fiche-{e['slug']}.html"), "w", encoding="utf-8").write(h)
        pg.set_content(h); pg.wait_for_timeout(300)
        # ajuste la taille du texte pour tenir sur une page
        fs = 9.8
        while fs > 7.4:
            over = pg.evaluate(f"(()=>{{document.body.style.setProperty('--fs','{fs}pt');var c=document.querySelector('.cols');var f=document.querySelector('.foot');return c.scrollHeight>c.clientHeight+1 || document.body.scrollHeight>document.body.clientHeight+1}})()")
            if not over: break
            fs -= 0.2
        pg.pdf(path=os.path.join(OUT, f"fiche-{e['slug']}.pdf"), format="Letter", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        print(e["slug"], round(fs, 1))
    b.close()
