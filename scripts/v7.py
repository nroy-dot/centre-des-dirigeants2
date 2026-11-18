#!/usr/bin/env python3
"""Version 3 : éditoriale et affirmée, inspirée de l'approche de theready.com, aux couleurs du Centre."""
import os, re, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
src = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
ns = {}
for nom in ["EXPERTS", "EXPERTISES", "FAQ"]:
    exec(re.search(rf"^{nom} = \[.*?^\]", src, re.S | re.M).group(0), ns)
EXPERTS, EXPERTISES, FAQ = ns["EXPERTS"], ns["EXPERTISES"], ns["FAQ"]
exec(open(os.path.join(HERE, "seo.py"), encoding="utf-8").read())
MAIL = "centredesdirigeants@postureinc.ca"

head = tete("index.html", "", "", EXPERTS, EXPERTISES, FAQ)
ld = json.loads(re.search(r'<script type="application/ld\+json">\n(.*)\n</script>', head, re.S).group(1))
for g in ld["@graph"]:
    if g.get("@type") == "WebPage":
        g["@type"] = ["WebPage", "FAQPage"]
        g["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in FAQ]
    if "founder" in g:
        for f in g["founder"]:
            f["@id"] = BASE + "#" + f["@id"].split("#")[1]
for p in personnes(EXPERTS):
    k = p["@id"].split("#")[1]; p["@id"] = BASE + "#" + k; ld["@graph"].append(p)
head = re.sub(r'<script type="application/ld\+json">\n.*\n</script>',
              '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False) + '\n</script>', head, flags=re.S)
head = head.replace('<link rel="stylesheet" href="css/style.css">', '').replace('content="#0C283A"', 'content="#0C283A"')

MARQUE = '<svg class="mq" viewBox="0 0 40 40" aria-hidden="true"><path d="M19 4a14 14 0 0 0 0 28z" fill="currentColor"/><path d="M21 8a14 14 0 0 1 0 28z" fill="#D5AC59"/></svg>'
ruban = "".join(f"<span>{t}</span>{MARQUE}" for t in ["Un réseau d’experts", "Prévention", "Urgence", "Reconstruction", "Une seule porte d’entrée", "PME et OBNL", "Gatineau"])

ILLU = {
 "p": '''<svg viewBox="0 0 220 200" class="illu"><circle cx="110" cy="150" r="22" fill="#F2EDE7"/><g class="bal"><path d="M30 120a80 80 0 0 1 160 0z" fill="#0C283A"/><rect x="108" y="118" width="4" height="40" fill="#0C283A"/></g><circle cx="60" cy="40" r="6" fill="#0C283A" class="gout"/><circle cx="150" cy="24" r="6" fill="#0C283A" class="gout g2"/><circle cx="104" cy="12" r="6" fill="#0C283A" class="gout g3"/></svg>''',
 "u": '''<svg viewBox="0 0 220 200" class="illu"><path d="M20 160 Q 80 40 200 60" stroke="#0C283A" stroke-width="4" fill="none" stroke-dasharray="8 10" class="trace"/><g class="fus"><path d="M170 40a26 26 0 0 0 0 52z" fill="#0C283A"/><path d="M174 46a26 26 0 0 1 0 52z" fill="#D5AC59"/></g><circle cx="24" cy="160" r="12" fill="#C6DEF4" stroke="#0C283A" stroke-width="3"/></svg>''',
 "r": '''<svg viewBox="0 0 220 200" class="illu"><g class="pile3"><path d="M40 180a40 40 0 0 1 80 0z" fill="#0C283A"/><path d="M100 180a40 40 0 0 1 80 0z" fill="#D5AC59" class="b2"/><path d="M70 140a40 40 0 0 1 80 0z" fill="#C6DEF4" stroke="#0C283A" stroke-width="3" class="b3"/><path d="M90 100a20 20 0 0 1 40 0z" fill="#0C283A" class="b4"/></g></svg>''',
}

visages = "".join(f'<img src="img/{s}.webp" alt="{n}" title="{n}" width="64" height="64">' for s, n, *_ in EXPERTS)
experts_html = "".join(
    f'''<article class="ex" id="{s}"><div class="exi"><img src="img/{s}.webp" alt="{n}" width="172" height="172" loading="lazy"></div>
<div><span class="exr">{r}</span><h3>{n}<small>{", " + c if c else ""}</small></h3><p>{d}</p></div></article>''' for s, n, c, r, d, t in EXPERTS)
faq_html = "".join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><p>{r}</p></details>' for q, r in FAQ)
expertises_html = "".join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d, _ in EXPERTISES)

CSS = r"""
@font-face{font-family:LS;src:url(fonts/LeagueSpartan-Light.woff2) format("woff2");font-weight:300;font-display:swap}
@font-face{font-family:LS;src:url(fonts/LeagueSpartan-Regular.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:LS;src:url(fonts/LeagueSpartan-SemiBold.woff2) format("woff2");font-weight:600;font-display:swap}
@font-face{font-family:LS;src:url(fonts/LeagueSpartan-Bold.woff2) format("woff2");font-weight:700;font-display:swap}
:root{--m:#0C283A;--o:#D5AC59;--of:#86651F;--c:#C6DEF4;--s:#F2EDE7;--d:#4C6577;--l:rgba(12,40,58,.14)}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:LS,system-ui,sans-serif;background:var(--s);color:var(--m);font-size:19px;line-height:1.5;overflow-x:hidden}
a{color:inherit}img{display:block;max-width:100%}
.w{width:min(1280px,100% - 48px);margin-inline:auto}
.eb{display:inline-flex;align-items:center;gap:10px;font-size:.95rem;font-weight:600;color:var(--m)}
.eb .mq{width:22px;height:22px;color:var(--m)}
.mq{width:26px;height:26px;flex:none}
.btn{display:inline-flex;align-items:center;gap:12px;font:700 1.05rem/1 LS,sans-serif;padding:20px 30px 17px;border-radius:999px;background:var(--m);color:#fff;text-decoration:none;border:0;cursor:pointer;transition:transform .2s,background .2s,color .2s}
.btn:hover{transform:translateY(-3px) rotate(-1deg);background:var(--o);color:var(--m)}
.btn .fl{transition:transform .2s}.btn:hover .fl{transform:translateX(4px)}
.btn.or{background:var(--o);color:var(--m)}.btn.or:hover{background:#fff}
.sep{display:flex;justify-content:center;gap:18px;padding:0;color:var(--m)}
.sep .mq{width:22px;height:22px}

/* En-tête */
.hd{position:fixed;inset:0 0 auto;z-index:40;transition:background .3s,box-shadow .3s}
.hd.pl{background:rgba(242,237,231,.9);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);box-shadow:0 1px 0 var(--l)}
.hd .w{display:flex;justify-content:space-between;align-items:center;height:86px}
.hd img{height:46px;width:auto}
.hd nav{display:flex;gap:30px;align-items:center}
.hd nav a{text-decoration:none;font-weight:600}
.hd nav a:not(.btn):hover{color:var(--o)}
.hd .btn{padding:14px 22px 12px;font-size:.95rem}
@media(max-width:900px){.hd nav a:not(.btn){display:none}}

/* Héros */
.hero{padding:150px 0 70px;position:relative}
.hero .petit{font-size:clamp(1.4rem,2.6vw,2.2rem);font-weight:600;display:block;margin-bottom:.25em;letter-spacing:0;line-height:1.2}
.hero h1{font-size:clamp(3.6rem,11.2vw,11.5rem);line-height:.84;letter-spacing:-.055em;font-weight:700}
.hero h1 .l{display:block;overflow:hidden;padding-bottom:.05em}
.hero h1 .l>span{display:inline-block;transform:translateY(105%);animation:mt 1.1s cubic-bezier(.16,1,.3,1) forwards}
.hero h1 .l:nth-child(3)>span{animation-delay:.12s}
.hero h1 .l:nth-child(4)>span{animation-delay:.24s}
@keyframes mt{to{transform:none}}
.hero h1 .o{color:var(--o)}
.hero .bas{display:grid;grid-template-columns:1.2fr .8fr;gap:5vw;align-items:end;margin-top:6vh}
.hero .bas p{font-size:clamp(1.2rem,2vw,1.6rem);line-height:1.35;max-width:30ch}
.tete-bas{display:flex;gap:22px;align-items:center;flex-wrap:wrap;justify-content:flex-end}
.pile-v{display:flex}.pile-v img{width:52px;height:52px;border-radius:50%;object-fit:cover;border:3px solid var(--s);margin-left:-14px}.pile-v img:first-child{margin-left:0}
.balance{position:absolute;right:4vw;top:118px;width:clamp(120px,16vw,240px);aspect-ratio:1;animation:bal 7s ease-in-out infinite}
.balance .a{position:absolute;left:0;top:0;width:48%;height:100%;background:var(--m);border-radius:999px 0 0 999px}
.balance .b{position:absolute;right:0;top:16%;width:48%;height:100%;background:var(--o);border-radius:0 999px 999px 0}
@keyframes bal{0%,100%{transform:rotate(-6deg)}50%{transform:rotate(6deg)}}
@media(max-width:820px){.hero .bas{grid-template-columns:1fr}.tete-bas{justify-content:flex-start}.balance{width:90px;top:100px;right:20px}}

/* Ruban */
.ruban{background:var(--m);color:#fff;overflow:hidden;padding:22px 0 18px;transform:rotate(-1.4deg);margin:30px -10px;width:calc(100% + 20px)}
.ruban .p{display:inline-flex;align-items:center;gap:30px;white-space:nowrap;animation:rb 40s linear infinite;font-weight:700;font-size:clamp(1.3rem,2.4vw,2rem)}
.ruban .mq{color:#F2EDE7}
@keyframes rb{to{transform:translateX(-50%)}}

/* Sections */
.sec{padding:clamp(80px,12vw,160px) 0}
.grand{font-size:clamp(2.6rem,6.4vw,6rem);line-height:.95;letter-spacing:-.04em;font-weight:700;max-width:17ch;margin-top:22px}
.grand em{font-style:normal;color:var(--of)}.grand.clair em,.reseau .grand em{color:var(--o)}
.deux{display:grid;grid-template-columns:1fr 1fr;gap:6vw;align-items:end;margin-top:6vh}
.deux p{font-size:1.25rem;max-width:42ch}
@media(max-width:820px){.deux{grid-template-columns:1fr}}

/* Expertises en liste éditoriale */
.liste{list-style:none;margin-top:7vh;border-top:2px solid var(--m)}
.liste li{display:grid;grid-template-columns:1fr 1.2fr auto;gap:30px;align-items:center;padding:24px 0;border-bottom:1px solid var(--l);transition:padding .3s,background .3s;position:relative}
.liste li::after{content:"→";font-weight:700;font-size:1.4rem;opacity:0;transform:translateX(-10px);transition:all .3s}
.liste li:hover{padding-left:18px;background:var(--c)}
.liste li:hover::after{opacity:1;transform:none;margin-right:18px}
.liste b{font-size:clamp(1.3rem,2.3vw,2rem);letter-spacing:-.02em;line-height:1.1}
.liste span{color:var(--d);font-size:1.02rem}
@media(max-width:820px){.liste li{grid-template-columns:1fr;gap:6px}.liste li::after{display:none}}

/* Comment : 3 verbes */
.verbes{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:7vh}
.verbe{border-radius:32px;padding:34px 30px 36px;min-height:520px;display:flex;flex-direction:column;transition:transform .35s cubic-bezier(.2,.8,.2,1)}
.verbe:hover{transform:translateY(-10px) rotate(-.6deg)}
.verbe:nth-child(1){background:var(--o)}
.verbe:nth-child(2){background:var(--c)}
.verbe:nth-child(3){background:var(--m);color:#C9D6E0}
.verbe:nth-child(3) h3{color:#fff}
.verbe .k{font-weight:600;font-size:.95rem;opacity:.75}
.verbe h3{font-size:clamp(2.4rem,4vw,3.6rem);letter-spacing:-.04em;line-height:.95;margin:10px 0 14px}
.verbe .illu{width:100%;height:190px;margin:auto 0 20px}
.verbe p{font-size:1.05rem}
.verbe .qui{display:flex;margin-top:20px}.verbe .qui img{width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid currentColor;margin-left:-8px}.verbe .qui img:first-child{margin-left:0}
.bal{transform-origin:110px 120px;animation:bal 5s ease-in-out infinite}
.gout{animation:gt 2.2s linear infinite}.g2{animation-delay:.7s}.g3{animation-delay:1.4s}
@keyframes gt{0%{transform:translateY(-10px);opacity:0}20%{opacity:1}70%{transform:translateY(70px);opacity:1}80%,100%{transform:translateY(70px);opacity:0}}
.trace{animation:tr 1.6s linear infinite}@keyframes tr{to{stroke-dashoffset:-36}}
.fus{animation:fu 3s ease-in-out infinite}@keyframes fu{0%,100%{transform:translate(0,0)}50%{transform:translate(-10px,-8px)}}
.pile3 path{transform-box:fill-box;transform-origin:bottom;animation:pl 3.6s ease-in-out infinite}
.pile3 .b2{animation-delay:.2s}.pile3 .b3{animation-delay:.4s}.pile3 .b4{animation-delay:.6s}
@keyframes pl{0%,100%{transform:scaleY(1)}12%{transform:scaleY(.82)}24%{transform:scaleY(1)}}
@media(max-width:900px){.verbes{grid-template-columns:1fr}.verbe{min-height:auto}}

/* Preuve : chiffres en graphique */
.preuve{background:var(--m);color:#C9D6E0;border-radius:40px;margin:0 clamp(10px,2vw,24px);padding:clamp(60px,9vw,120px) 0;position:relative;overflow:hidden}
.preuve .eb,.preuve .eb .mq{color:#fff}
.chiff{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-top:6vh}
.chiff>div{border-left:1px solid rgba(255,255,255,.15);padding:0 3vw}
.chiff>div:first-child{border-left:0;padding-left:0}
.chiff .v{font-size:clamp(5rem,13vw,12rem);font-weight:700;line-height:.8;letter-spacing:-.06em;color:#fff}
.chiff .v.o{color:var(--o)}
.chiff p{font-size:1.2rem;margin-top:14px;max-width:18ch}
.preuve .note{margin-top:7vh;font-size:clamp(1.4rem,2.6vw,2.2rem);color:#fff;font-weight:600;max-width:32ch;line-height:1.25}
.preuve .note span{color:var(--o)}
.preuve .deco{position:absolute;right:-60px;bottom:-60px;width:260px;height:260px;border-radius:50%;border:2px dashed rgba(213,172,89,.35);animation:rt 40s linear infinite}
@keyframes rt{to{transform:rotate(360deg)}}
@media(max-width:820px){.chiff{grid-template-columns:1fr;gap:34px}.chiff>div{border:0;padding:0}}

/* Voix */
.voix{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:6vh}
.vx{background:#fff;border-radius:32px;padding:clamp(28px,4vw,48px);display:flex;flex-direction:column;gap:26px;justify-content:space-between}
.vx q{font-size:clamp(1.4rem,2.3vw,1.95rem);line-height:1.25;font-weight:600;quotes:"« " " »"}
.vx q::before,.vx q::after{color:var(--o)}
.vx .qui{display:flex;gap:14px;align-items:center}
.vx .qui img{width:58px;height:58px;border-radius:50%;object-fit:cover}
.vx .qui b{display:block}.vx .qui span{color:var(--d);font-size:.95rem}
@media(max-width:820px){.voix{grid-template-columns:1fr}}

/* Énoncé */
.enonce{font-size:clamp(2.2rem,5.4vw,5rem);line-height:1.02;letter-spacing:-.035em;font-weight:700;max-width:20ch}
.enonce mark{background:linear-gradient(transparent 62%,var(--o) 62%);color:inherit;padding:0 .04em}

/* Bénéfices */
.benef{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:6vh}
.bn{border-top:3px solid var(--m);padding-top:22px}
.bn .n{font-weight:700;color:var(--of)}
.bn h3{font-size:1.65rem;line-height:1.05;letter-spacing:-.02em;margin:10px 0}
.bn p{color:var(--d);font-size:1.02rem}
@media(max-width:900px){.benef{grid-template-columns:1fr 1fr}}@media(max-width:560px){.benef{grid-template-columns:1fr}}

/* Experts */
.exg{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:6vh}
.ex{background:#fff;border-radius:28px;padding:20px;display:grid;grid-template-columns:96px 1fr;gap:18px;align-items:start;transition:transform .3s,box-shadow .3s}
.ex:hover{transform:translateY(-6px);box-shadow:0 22px 40px rgba(12,40,58,.12)}
.exi{width:96px;height:96px;border-radius:50% 50% 50% 8px;overflow:hidden;background:var(--c)}
.exi img{width:100%;height:100%;object-fit:cover}
.exr{font-size:.8rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--of)}
.ex h3{font-size:1.3rem;line-height:1.1;margin:4px 0 6px}.ex h3 small{font-size:.8rem;font-weight:400;color:var(--d)}
.ex p{font-size:.95rem;color:var(--d)}
@media(max-width:1000px){.exg{grid-template-columns:1fr 1fr}}@media(max-width:640px){.exg{grid-template-columns:1fr}}

/* En bref + FAQ */
.sv{display:grid;grid-template-columns:.9fr 1.1fr;gap:6vw}
.sv .def{font-size:1.3rem;line-height:1.45;font-weight:600;margin-top:20px}
.sv dl{display:grid;grid-template-columns:auto 1fr;margin-top:26px;border-top:1px solid var(--l)}
.sv dt,.sv dd{padding:13px 0;border-bottom:1px solid var(--l);font-size:1rem}
.sv dt{padding-right:22px;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--d);padding-top:15px}
.sv dd{font-weight:600}
.faq details{border-bottom:1px solid var(--l)}
.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:20px;padding:22px 0;font-weight:700;font-size:1.2rem}
.faq summary::-webkit-details-marker{display:none}
.faq summary i{flex:none;width:34px;height:34px;border-radius:50%;background:var(--m);position:relative;transition:background .2s}
.faq summary i::before,.faq summary i::after{content:"";position:absolute;left:50%;top:50%;width:13px;height:2px;background:#fff;transform:translate(-50%,-50%)}
.faq summary i::after{transform:translate(-50%,-50%) rotate(90deg);transition:transform .3s}
.faq details[open] summary i{background:var(--o)}
.faq details[open] summary i::after{transform:translate(-50%,-50%)}
.faq details p{padding:0 50px 22px 0;color:var(--d)}
@media(max-width:820px){.sv{grid-template-columns:1fr}}

/* Finale */
.fin{background:var(--o);border-radius:40px;margin:0 clamp(10px,2vw,24px) clamp(10px,2vw,24px);padding:clamp(70px,10vw,140px) 0;position:relative;overflow:hidden}
.fin h2{font-size:clamp(4rem,13vw,12.5rem);line-height:.84;letter-spacing:-.06em}
.fin h2 span{color:transparent;-webkit-text-stroke:2.5px var(--m)}
.fin .g{display:grid;grid-template-columns:1fr 1fr;gap:6vw;margin-top:6vh;align-items:start}
.fin .g p{font-size:1.3rem;max-width:30ch}
.fin form{display:grid;gap:12px;background:var(--s);border-radius:28px;padding:28px}
.fin label{font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--d)}
.fin input,.fin textarea{width:100%;border:0;border-bottom:1.5px solid var(--l);background:transparent;font:400 1.15rem/1.4 LS,sans-serif;color:var(--m);padding:8px 0 10px}
.fin textarea{min-height:120px;resize:vertical}
.fin input:focus,.fin textarea:focus{outline:none;border-color:var(--m)}
.pot{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.consent{display:grid!important;grid-template-columns:auto 1fr;gap:12px;align-items:start;text-transform:none!important;letter-spacing:0!important;font-size:.9rem!important;font-weight:400!important;color:var(--d)!important;margin-top:8px}
.consent input{width:20px;height:20px;margin-top:2px;accent-color:var(--m)}
.consent a{color:var(--m);font-weight:600}
.delai{font-size:.92rem;color:var(--d)}.err{color:#9B2C1A;font-weight:600;font-size:.95rem;min-height:1em}
.ret{display:none;background:var(--s);border-radius:28px;padding:28px}.ret.vu{display:block}
.ret pre{white-space:pre-wrap;font:inherit;background:#fff;border-radius:12px;padding:14px;margin:14px 0;font-size:.95rem}
.marie{display:flex;gap:14px;align-items:center;margin-top:28px}.marie img{width:64px;height:64px;border-radius:50%;object-fit:cover}
@media(max-width:820px){.fin .g{grid-template-columns:1fr}}
footer{padding:40px 0 50px;font-size:.92rem;color:var(--d)}
footer .w{display:flex;justify-content:space-between;flex-wrap:wrap;gap:14px;align-items:center}
footer img{height:40px;width:auto}

/* Apparition */
.ap{opacity:0;transform:translateY(30px);transition:opacity .8s ease,transform .8s cubic-bezier(.16,1,.3,1)}
.ap.vu{opacity:1;transform:none}
.mo{display:inline-block;overflow:hidden;vertical-align:bottom;padding-bottom:.06em;margin-bottom:-.06em}
.mo>span{display:inline-block;transform:translateY(110%);transition:transform .9s cubic-bezier(.16,1,.3,1)}
.vu .mo>span,.mo.vu>span{transform:none}

/* ===== Vivant : photos ===== */
.eb.clair,.eb.clair .mq{color:#fff}
.grand.clair{color:#fff}
.hero2{position:relative;min-height:100vh;min-height:100svh;display:flex;align-items:flex-end;color:#fff;overflow:hidden;background:var(--m)}
.diapos,.diapo,.voile{position:absolute;inset:0}
.diapo img{width:100%;height:100%;object-fit:cover;object-position:center 35%}.diapo{display:block;opacity:0;transform:scale(1.12);transition:opacity 1.6s ease}
.diapo.on{opacity:1;animation:kb 9s linear forwards}
@keyframes kb{from{transform:scale(1.14) translate(1.5%,1%)}to{transform:scale(1.02) translate(-1%,-1%)}}
.voile{background:linear-gradient(90deg,rgba(12,40,58,.92) 0%,rgba(12,40,58,.72) 42%,rgba(12,40,58,.15) 75%),linear-gradient(0deg,rgba(12,40,58,.85),transparent 45%)}
.h2c{position:relative;z-index:2;padding:150px 0 9vh}
.hero2 h1{font-size:clamp(3.4rem,9.4vw,9.6rem);line-height:.86;letter-spacing:-.05em;color:#fff;margin-top:18px}
.hero2 h1 .l{display:block;overflow:hidden;padding-bottom:.05em}
.hero2 h1 .l>span{display:inline-block;transform:translateY(105%);animation:mt 1.1s cubic-bezier(.16,1,.3,1) forwards}
.hero2 h1 .l:nth-child(2)>span{animation-delay:.12s}.hero2 h1 .l:nth-child(3)>span{animation-delay:.24s}
.hero2 h1 .o{color:var(--o)}
.hero2 .bas{display:grid;grid-template-columns:1.2fr .8fr;gap:5vw;align-items:end;margin-top:5vh}
.hero2 .bas p{font-size:clamp(1.15rem,1.8vw,1.45rem);line-height:1.4;max-width:34ch;color:#E3EAF0}
.hero2 .pile-v img{border-color:var(--m)}
.compteur-d{position:absolute;right:clamp(20px,4vw,48px);bottom:9vh;z-index:2;display:grid;gap:10px}
.compteur-d i{display:block;width:3px;height:28px;background:rgba(255,255,255,.3);border-radius:3px;overflow:hidden;position:relative}
.compteur-d i.on::after{content:"";position:absolute;inset:0;background:var(--o);animation:rempl 6s linear forwards;transform-origin:top}
@keyframes rempl{from{transform:scaleY(0)}to{transform:scaleY(1)}}
.hd{color:#fff}.hd img{filter:brightness(0) invert(1);transition:filter .3s}
.hd.pl{color:var(--m)}.hd.pl img{filter:none}
.hd .btn{background:var(--o);color:var(--m)}.hd.pl .btn{background:var(--m);color:#fff}
@media(max-width:820px){.hero2 .bas{grid-template-columns:1fr}.voile{background:linear-gradient(0deg,rgba(12,40,58,.95) 30%,rgba(12,40,58,.45))}.compteur-d{display:none}}

.duo-photo{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:3vw;margin-top:9vh;align-items:center}
.demi-photo{overflow:hidden;aspect-ratio:1/1.15;position:relative}
.demi-photo.g{border-radius:999px 0 0 999px;clip-path:inset(0 0 0 100%);transition:clip-path 1.4s cubic-bezier(.16,1,.3,1)}
.demi-photo.d{border-radius:0 999px 999px 0;margin-top:14vh;clip-path:inset(0 100% 0 0);transition:clip-path 1.4s .15s cubic-bezier(.16,1,.3,1)}
.duo-photo.ap{opacity:1;transform:none}.duo-photo.vu .demi-photo{clip-path:inset(0 0 0 0)}
.demi-photo.ap{opacity:1;transform:none}
.demi-photo img{width:100%;height:118%;object-fit:cover;will-change:transform}
.demi-photo.d::after{content:"";position:absolute;inset:0;background:rgba(213,172,89,.12);mix-blend-mode:multiply}
.legende{position:absolute;left:50%;bottom:-2vh;transform:translateX(-50%);background:var(--m);color:#fff;border-radius:999px;padding:16px 26px 13px;font-size:1.05rem;white-space:nowrap;box-shadow:0 20px 40px rgba(12,40,58,.25)}
.legende.ap{transform:translate(-50%,30px)}.legende.ap.vu{transform:translate(-50%,0)}
.legende b{color:var(--o)}
@media(max-width:820px){.legende{white-space:normal;width:90%;text-align:center;border-radius:20px}.demi-photo.d{margin-top:8vh}}

.vph{border-radius:22px;overflow:hidden;aspect-ratio:4/3;margin:14px 0 22px}
.vph img{width:100%;height:100%;object-fit:cover;transform:scale(1.08);transition:transform 1.2s cubic-bezier(.16,1,.3,1)}
.verbe:hover .vph img{transform:scale(1.15)}
.verbe.vu .vph img{transform:scale(1)}
.verbe{min-height:auto}

.preuve{isolation:isolate}
.preuve-fond{position:absolute;inset:-10% 0;background-size:cover;background-position:center;opacity:.22;z-index:-1;filter:grayscale(.4)}
.preuve::before{content:"";position:absolute;inset:0;background:linear-gradient(120deg,rgba(12,40,58,.96) 35%,rgba(12,40,58,.7));z-index:-1}

.bandeau-photos{padding:10vh 0 2vh;overflow:hidden;display:grid;gap:16px}
.rang{display:flex;gap:16px;width:max-content}
.rang img{height:clamp(150px,19vw,260px);width:auto;aspect-ratio:3/2;object-fit:cover;border-radius:22px}
.rang img:nth-child(3n+2){border-radius:999px 22px 22px 999px}
.rang img:nth-child(4n){border-radius:22px 999px 999px 22px}
.r1{animation:rb 60s linear infinite}
.r2{animation:rb2 60s linear infinite}
@keyframes rb2{from{transform:translateX(-50%)}to{transform:translateX(0)}}
.bandeau-photos:hover .rang{animation-play-state:paused}

.fin-photo{border-radius:999px 999px 28px 28px;overflow:hidden;aspect-ratio:4/3.3;margin-bottom:26px;max-width:460px}
.fin-photo img{width:100%;height:100%;object-fit:cover}

/* Pause */
.pause{position:fixed;left:18px;bottom:18px;z-index:45;display:flex;align-items:center;gap:10px;border:0;cursor:pointer;background:rgba(12,40,58,.9);color:#fff;border-radius:999px;padding:10px 16px 8px 10px;font:600 .82rem/1 LS,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.2)}
.pause .ic{width:24px;height:24px;border-radius:50%;background:var(--o);position:relative;flex:none}
.pause .ic::before,.pause .ic::after{content:"";position:absolute;top:7px;width:3px;height:10px;background:var(--m);left:8px}
.pause .ic::after{left:13px}
.pause[aria-pressed=true] .ic::before{left:9px;width:0;height:0;background:none;border-left:9px solid var(--m);border-top:5px solid transparent;border-bottom:5px solid transparent}
.pause[aria-pressed=true] .ic::after{display:none}
.pause:focus-visible{outline:3px solid var(--o);outline-offset:3px}
@media(max-width:600px){.pause .tx{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}.pause{padding:8px}}
body.fige *,body.fige *::before,body.fige *::after{animation-play-state:paused!important}
/* Constellation */
.reseau{background:var(--m);color:#C9D6E0;padding:clamp(80px,12vw,160px) 0;border-radius:40px;margin:0 clamp(10px,2vw,24px)}
.res-t{display:grid;grid-template-columns:1.1fr .9fr;gap:4vw;align-items:end;margin-bottom:4vh}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{all:unset;cursor:pointer;padding:10px 15px 8px;border-radius:999px;font-weight:600;font-size:.9rem;color:#fff;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.25);transition:all .2s}
.chip:hover{box-shadow:inset 0 0 0 1.5px var(--o)}
.chip[aria-pressed=true]{background:var(--o);color:var(--m);box-shadow:none}
.chip:focus-visible{outline:2px solid var(--o);outline-offset:2px}
.ciel{position:relative;height:min(76vh,740px)}
.ciel canvas{position:absolute;inset:0;width:100%;height:100%}
.etoile{all:unset;position:absolute;width:clamp(66px,7.4vw,104px);aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;cursor:pointer;transition:opacity .35s,width .35s}
.etoile img{width:100%;height:100%;border-radius:50%;object-fit:cover;box-shadow:0 0 0 3px var(--m),0 0 0 4.5px rgba(213,172,89,.65),0 18px 40px rgba(0,0,0,.45);filter:grayscale(.75);transition:filter .35s}
.etoile:hover img,.etoile.on img{filter:none}
.etoile.on{width:clamp(82px,9vw,126px)}
.etoile.off{opacity:.22}
.etoile b{position:absolute;left:50%;top:calc(100% + 10px);transform:translateX(-50%);white-space:nowrap;color:#fff;font-size:.9rem;font-weight:600;opacity:.8}
.etoile:focus-visible img{box-shadow:0 0 0 3px var(--m),0 0 0 6px var(--o)}
.fiche{position:absolute;right:0;bottom:0;width:min(400px,92%);background:var(--s);color:var(--m);border-radius:22px;padding:22px 24px;box-shadow:0 30px 60px rgba(0,0,0,.4);transform:translateY(20px);opacity:0;transition:all .35s;pointer-events:none}
.fiche.vu{transform:none;opacity:1}
.fiche .r{font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;color:var(--of);font-weight:600}
.fiche h3{font-size:1.45rem;margin:4px 0 8px;line-height:1.1}
.fiche p{font-size:.98rem;color:var(--d)}
.reseau .exg{display:none}
@media(max-width:820px){.res-t{grid-template-columns:1fr}.ciel{display:none}.reseau .exg{display:grid}.reseau .ex.off{opacity:.3}}

@media(prefers-reduced-motion:reduce){*{animation:none!important}.demi-photo{clip-path:none!important}.diapo.on{transform:none}.ap,.mo>span,.hero h1 .l>span{opacity:1!important;transform:none!important}}
"""

JS = r"""
(function(){
var hd=document.querySelector('.hd');function f(){hd.classList.toggle('pl',scrollY>30)}f();addEventListener('scroll',f,{passive:true});
document.querySelectorAll('.grand,.enonce').forEach(function(h){var i=0;h.innerHTML=h.innerHTML.split(/(<[^>]+>|\s+)/).filter(Boolean).map(function(t){if(/^<|^\s+$/.test(t))return t;return '<span class="mo"><span style="transition-delay:'+(i++*0.045)+'s">'+t+'</span></span>'}).join('');h.classList.add('ap')});
var io='IntersectionObserver' in window?new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){x.target.classList.add('vu');io.unobserve(x.target)}})},{threshold:.15}):null;
document.querySelectorAll('.ap').forEach(function(e){io?io.observe(e):e.classList.add('vu')});
document.querySelectorAll('[data-c]').forEach(function(el){var fin=+el.dataset.c;var o=new IntersectionObserver(function(e){if(e[0].isIntersecting){o.disconnect();var t0=null;(function p(t){if(!t0)t0=t;var k=Math.min((t-t0)/1500,1);el.textContent=Math.round(fin*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(p)})(performance.now())}},{threshold:.6});o.observe(el)});

var R=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var bp=document.getElementById('pause');
function fige(v){R=v;document.body.classList.toggle('fige',v);bp.setAttribute('aria-pressed',v?'true':'false');bp.querySelector('.tx').textContent=v?'Relancer les animations':'Mettre les animations en pause';try{localStorage.setItem('cdd-fige',v?'1':'0')}catch(e){}}
bp.addEventListener('click',function(){fige(!document.body.classList.contains('fige'))});
try{if(localStorage.getItem('cdd-fige')==='1')fige(true)}catch(e){}
if(R)fige(true);
/* Diaporama du héros */
var ds=document.querySelectorAll('.diapo'),cd=document.querySelectorAll('.compteur-d i'),di=0;
if(ds.length){setInterval(function(){if(R)return;ds[di].classList.remove('on');cd[di].classList.remove('on');di=(di+1)%ds.length;void ds[di].offsetWidth;ds[di].classList.add('on');void cd[di].offsetWidth;cd[di].classList.add('on')},6000)}
/* Parallaxe */
var par=document.querySelectorAll('[data-par]'),pbg=document.querySelector('[data-parbg]');
function px(){if(R)return;var h=innerHeight;par.forEach(function(im){var r=im.parentNode.getBoundingClientRect();if(r.bottom<0||r.top>h)return;var k=parseFloat(im.dataset.par);im.style.transform='translateY('+((r.top+r.height/2-h/2)*k-r.height*.08)+'px)'});
 if(pbg){var r=pbg.parentNode.getBoundingClientRect();pbg.style.transform='translateY('+(r.top*-.12)+'px)'}}
addEventListener('scroll',function(){requestAnimationFrame(px)},{passive:true});px();
/* Constellation */
var EXP=__EXP__,ENJ=__ENJ__;
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
var ciel=document.getElementById('ciel'),cv=ciel.querySelector('canvas'),cx=cv.getContext('2d'),fiche=document.getElementById('fiche');
var base=[[.5,.5],[.2,.3],[.8,.26],[.1,.7],[.35,.82],[.63,.84],[.9,.64],[.3,.1],[.68,.08]];
var ordre=['marie-eve-venner','nicolas-roy','france-belisle','chantal-dufort','andreanne-thibault','yannick-beaulieu','sophie-ann-bellisle','daniel-feeny','marc-antoine-laramee'];
var noeuds=[],actif=null,filtre=null;
function montre(s){actif=s;var e=EXP[s];fiche.innerHTML='<span class="r">'+esc(e.r)+'</span><h3>'+esc(e.n)+(e.c?', '+esc(e.c):'')+'</h3><p>'+esc(e.d)+'</p>';fiche.classList.add('vu');noeuds.forEach(function(n){n.el.classList.toggle('on',n.s===s)})}
ordre.forEach(function(s,i){var d=document.createElement('button');d.className='etoile';d.type='button';d.setAttribute('aria-label',EXP[s].n+', '+EXP[s].r);
 d.innerHTML='<img src="img/'+s+'.webp" alt=""><b>'+esc(EXP[s].n.split(' ')[0])+'</b>';ciel.appendChild(d);
 noeuds.push({s:s,el:d,bx:base[i][0],by:base[i][1],ph:Math.random()*6.28,sp:.35+Math.random()*.4});
 d.addEventListener('mouseenter',function(){montre(s)});d.addEventListener('focus',function(){montre(s)});d.addEventListener('click',function(){montre(s)})});
ciel.addEventListener('mouseleave',function(){if(!filtre){actif=null;fiche.classList.remove('vu');noeuds.forEach(function(n){n.el.classList.remove('on')})}});
function taille(){var r=ciel.getBoundingClientRect(),d=devicePixelRatio||1;cv.width=r.width*d;cv.height=r.height*d;cx.setTransform(d,0,0,d,0,0)}
taille();addEventListener('resize',taille);
var t0=performance.now();
(function anime(t){var r=ciel.getBoundingClientRect(),W=r.width,H=r.height,tt=((t||t0)-t0)/1000;
 if(r.bottom>0&&r.top<innerHeight){
 noeuds.forEach(function(n){var a=R?0:1;n.x=(n.bx+Math.sin(tt*n.sp+n.ph)*.018*a)*W;n.y=(n.by+Math.cos(tt*n.sp*.8+n.ph)*.03*a)*H;n.el.style.left=n.x+'px';n.el.style.top=n.y+'px'});
 cx.clearRect(0,0,W,H);
 noeuds.forEach(function(n,i){noeuds.forEach(function(m,j){if(j<=i)return;var lie=(i===0)||(Math.hypot(n.bx-m.bx,n.by-m.by)<.34);if(!lie)return;
  var fort=(actif&&(n.s===actif||m.s===actif))||(filtre&&filtre.indexOf(n.s)>-1&&filtre.indexOf(m.s)>-1);
  cx.strokeStyle=fort?'rgba(213,172,89,.95)':'rgba(198,222,244,'+(i===0?.18:.1)+')';cx.lineWidth=fort?2:1;cx.beginPath();cx.moveTo(n.x,n.y);cx.lineTo(m.x,m.y);cx.stroke();
  if(fort&&!R){var f=(tt*.6)%1;cx.fillStyle='#D5AC59';cx.beginPath();cx.arc(n.x+(m.x-n.x)*f,n.y+(m.y-n.y)*f,3,0,6.3);cx.fill()}})});}
 requestAnimationFrame(anime)})();
var chips=document.getElementById('chips'),cartes=document.querySelectorAll('.reseau .ex');
ENJ.forEach(function(e){var b=document.createElement('button');b.className='chip';b.type='button';b.textContent=e.t;b.setAttribute('aria-pressed','false');
 b.onclick=function(){var deja=b.getAttribute('aria-pressed')==='true';chips.querySelectorAll('.chip').forEach(function(c){c.setAttribute('aria-pressed','false')});
  if(deja){filtre=null;noeuds.forEach(function(n){n.el.classList.remove('off','on')});cartes.forEach(function(c){c.classList.remove('off')});fiche.classList.remove('vu');return}
  b.setAttribute('aria-pressed','true');filtre=['marie-eve-venner'].concat(e.e);
  noeuds.forEach(function(n){n.el.classList.toggle('off',filtre.indexOf(n.s)<0);n.el.classList.toggle('on',e.e.indexOf(n.s)>-1)});
  cartes.forEach(function(c){c.classList.toggle('off',filtre.indexOf(c.id)<0)});
  actif=null;fiche.innerHTML='<span class="r">'+esc(e.t)+'</span><h3>'+e.e.map(function(s){return esc(EXP[s].n)}).join(' et ')+'</h3><p>'+esc(e.d)+'</p>';fiche.classList.add('vu')};
 chips.appendChild(b)});

var FORM_ENDPOINT='';/* À remplir : adresse du service d'envoi (ex. https://formspree.io/f/xxxxxxx) */
var fm=document.getElementById('form'),ret=document.getElementById('ret'),merci=document.getElementById('merci'),err=document.getElementById('err'),corps='';
function repli(n){ret.querySelector('pre').textContent=corps;
 document.getElementById('ouvrir').href='mailto:__MAIL__?subject='+encodeURIComponent('Demande au Centre des dirigeants : '+n)+'&body='+encodeURIComponent(corps);
 fm.style.display='none';ret.classList.add('vu')}
fm.addEventListener('submit',function(ev){ev.preventDefault();err.textContent='';
 if(fm.site_web.value)return;
 var n=fm.nom.value.trim(),o=fm.org.value.trim(),m=fm.mail.value.trim(),x=fm.msg.value.trim();
 var manque=[];[fm.nom,fm.mail,fm.msg].forEach(function(c){var v=c.value.trim();c.style.borderColor=v?'':'#9B2C1A';if(!v)manque.push(c)});
 if(manque.length){err.textContent='Merci de remplir votre nom, votre courriel et votre situation.';manque[0].focus();return}
 if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(m)){err.textContent='Ce courriel ne semble pas valide.';fm.mail.focus();return}
 if(!fm.ok.checked){err.textContent='Merci de cocher la case de consentement.';fm.ok.focus();return}
 corps=x+'\n\n'+n+(o?'\n'+o:'')+'\n'+m;
 if(!FORM_ENDPOINT){repli(n);return}
 var b=document.getElementById('envoyer');b.disabled=true;b.firstChild.textContent='Envoi en cours… ';
 fetch(FORM_ENDPOINT,{method:'POST',headers:{'Accept':'application/json'},body:new FormData(fm)}).then(function(r){if(!r.ok)throw 0;fm.style.display='none';merci.classList.add('vu');merci.focus&&merci.focus()}).catch(function(){repli(n)});
});
document.getElementById('copier').addEventListener('click',function(){var b=this;try{navigator.clipboard.writeText(corps).then(function(){b.textContent='Message copié'},function(){b.textContent='Sélectionnez le texte'})}catch(e){b.textContent='Sélectionnez le texte'}});
})();
""".replace("__MAIL__", MAIL)

B1=["conversation-cafe","deux-collegues","cafe-equipe","trio-portable","complicite","appel"]
B2=["duo-portable","collaboration","equipe-concentree","planification","equipe-reseau","bureau-sourire"]
ALT={"conversation-cafe":"Conversation autour d’un café","deux-collegues":"Deux collègues au travail","cafe-equipe":"Équipe en discussion","trio-portable":"Trois collègues autour d’un portable","complicite":"Complicité au travail","appel":"Dirigeante au téléphone","duo-portable":"Duo au travail","collaboration":"Collaboration","equipe-concentree":"Équipe concentrée","planification":"Planification","equipe-reseau":"Équipe réunie","bureau-sourire":"Dirigeante souriante"}
BANDE1="".join(f'<img src="img/{n}-p.webp" alt="" loading="lazy" width="640" height="427">' for n in B1)
BANDE2="".join(f'<img src="img/{n}-p.webp" alt="" loading="lazy" width="640" height="427">' for n in B2)
CARTE={"Stratégie et gouvernance":["nicolas-roy","france-belisle"],"Direction financière et rentabilité":["yannick-beaulieu"],"Ressources humaines":["nicolas-roy","andreanne-thibault"],"Communications":["france-belisle","daniel-feeny"],"Sondages internes et externes":["nicolas-roy","andreanne-thibault"],"Tests psychométriques":["nicolas-roy"],"Médiation":["france-belisle"],"Santé mentale au travail":["chantal-dufort"],"Protection des données":["sophie-ann-bellisle"],"Intelligence artificielle":["marc-antoine-laramee"]}
EXPJ={s_:{"n":n,"c":c,"r":r,"d":d} for s_,n,c,r,d,t in EXPERTS}
ENJJ=[{"t":t,"d":d,"e":CARTE[t]} for t,d,_ in EXPERTISES]

def qui(*ss):
    return '<div class="qui">' + "".join(f'<img src="img/{s}.webp" alt="" width="40" height="40">' for s in ss) + '</div>'

JS = JS.replace("__EXP__", json.dumps(EXPJ, ensure_ascii=False)).replace("__ENJ__", json.dumps(ENJJ, ensure_ascii=False))
html = f"""<!DOCTYPE html>
<html lang="fr-CA">
<head>
{head}
<style>{CSS}</style>
</head>
<body>
<header class="hd"><div class="w">
  <a href="#haut" aria-label="Centre des dirigeants, haut de page"><img src="img/logo.png" alt="Centre des dirigeants" width="900" height="330"></a>
  <nav aria-label="Navigation"><a href="#ce-qu-on-fait">Ce qu’on fait</a><a href="#comment">Comment</a><a href="#experts">Les experts</a><a href="#en-bref">En bref</a><a class="btn" href="#parler">Parlons-en <span class="fl">→</span></a></nav>
</div></header>
<button class="pause" id="pause" type="button" aria-pressed="false"><span class="ic" aria-hidden="true"></span><span class="tx">Mettre les animations en pause</span></button>
<main id="haut">

<section class="hero2" aria-label="Accueil">
  <div class="diapos" aria-hidden="true">
    <picture class="diapo on"><source media="(max-width:700px)" srcset="img/dirigeant-explique-port.webp"><img src="img/dirigeant-explique-1400.webp" srcset="img/dirigeant-explique-800.webp 800w, img/dirigeant-explique-1400.webp 1400w, img/dirigeant-explique.webp 2400w" sizes="100vw" alt="" fetchpriority="high"></picture>
    <picture class="diapo"><source media="(max-width:700px)" srcset="img/dirigeante-ecoute-port.webp"><img src="img/dirigeante-ecoute-1400.webp" srcset="img/dirigeante-ecoute-800.webp 800w, img/dirigeante-ecoute-1400.webp 1400w, img/dirigeante-ecoute.webp 2400w" sizes="100vw" alt="" loading="lazy"></picture>
    <picture class="diapo"><source media="(max-width:700px)" srcset="img/equipe-concentree-port.webp"><img src="img/equipe-concentree-1400.webp" srcset="img/equipe-concentree-800.webp 800w, img/equipe-concentree-1400.webp 1400w, img/equipe-concentree.webp 2400w" sizes="100vw" alt="" loading="lazy"></picture>
  </div>
  <div class="voile" aria-hidden="true"></div>
  <div class="w h2c">
    <span class="eb clair">{MARQUE} Réseau d’experts · PME et OBNL · Gatineau</span>
    <h1><span class="l"><span>Les bonnes</span></span><span class="l"><span>expertises.</span></span><span class="l"><span class="o">Au bon moment.</span></span></h1>
    <div class="bas">
      <p>Neuf experts de confiance, une seule porte d’entrée. Pour les dirigeants de PME et d’OBNL qui n’ont pas le temps de chercher qui appeler.</p>
      <div class="tete-bas"><div class="pile-v">{visages}</div><a class="btn or" href="#parler">Commençons <span class="fl">→</span></a></div>
    </div>
  </div>
  <div class="compteur-d" aria-hidden="true"><i class="on"></i><i></i><i></i></div>
</section>

<div class="ruban" aria-hidden="true"><div class="p">{ruban}{ruban}</div></div>

<section class="sec" id="ce-qu-on-fait">
  <div class="w">
    <span class="eb ap">{MARQUE} Ce qu’on fait</span>
    <h2 class="grand">On aide les dirigeants à traverser <em>ce qui se croise.</em></h2>
    <div class="deux ap">
      <p>Un enjeu RH devient financier, puis médiatique. Vous faites le lien entre tout, souvent seul. Le Centre réunit les expertises dont vous avez besoin, au moment où vous en avez besoin.</p>
      <p style="font-weight:600">Vous expliquez votre situation une seule fois. On vous oriente vers les bonnes personnes. Vous avancez.</p>
    </div>
    <div class="duo-photo ap">
      <figure class="demi-photo g"><img src="img/dirigeante-ecoute-1400.webp" srcset="img/dirigeante-ecoute-800.webp 800w, img/dirigeante-ecoute-1400.webp 1400w" sizes="(max-width:820px) 92vw, 45vw" alt="Dirigeante à l’écoute pendant une rencontre" loading="lazy" data-par=".06"></figure>
      <figure class="demi-photo d"><img src="img/conversation-cafe-1400.webp" srcset="img/conversation-cafe-800.webp 800w, img/conversation-cafe-1400.webp 1400w" sizes="(max-width:820px) 92vw, 45vw" alt="Conversation entre dirigeants autour d’un café" loading="lazy" data-par="-.06"></figure>
      <p class="legende ap">Vous expliquez votre situation <b>une seule fois</b>. Le réseau fait le reste.</p>
    </div>
    <ul class="liste ap" aria-label="Expertises du Centre">{expertises_html}</ul>
  </div>
</section>

<div class="sep" aria-hidden="true">{MARQUE}{MARQUE}{MARQUE}</div>

<section class="sec" id="comment">
  <div class="w">
    <span class="eb ap">{MARQUE} Comment on le fait</span>
    <h2 class="grand">Avant, pendant <em>et après</em> la tempête.</h2>
    <div class="verbes">
      <article class="verbe ap"><span class="k">01 · Prévention</span><h3>Prévenir.</h3><div class="vph"><img src="img/planification-1400.webp" srcset="img/planification-800.webp 800w, img/planification-1400.webp 1400w" sizes="(max-width:820px) 92vw, 45vw" alt="Planification calme entre collègues" loading="lazy"></div><p>Clarifier les priorités, renforcer les pratiques et anticiper les enjeux avant qu’ils ne deviennent des urgences.</p>{qui("nicolas-roy","sophie-ann-bellisle","chantal-dufort","marc-antoine-laramee")}</article>
      <article class="verbe ap" style="transition-delay:.1s"><span class="k">02 · Urgence</span><h3>Traverser.</h3><div class="vph"><img src="img/reunion-direction-1400.webp" srcset="img/reunion-direction-800.webp 800w, img/reunion-direction-1400.webp 1400w" sizes="(max-width:820px) 92vw, 45vw" alt="Réunion de direction mobilisée autour d’un enjeu" loading="lazy"></div><p>Établir les priorités et mobiliser rapidement les bonnes expertises : crise, finances, relations gouvernementales, soutien.</p>{qui("france-belisle","yannick-beaulieu","daniel-feeny","chantal-dufort")}</article>
      <article class="verbe ap" style="transition-delay:.2s"><span class="k">03 · Reconstruction</span><h3>Rebâtir.</h3><div class="vph"><img src="img/equipe-applaudit-1400.webp" srcset="img/equipe-applaudit-800.webp 800w, img/equipe-applaudit-1400.webp 1400w" sizes="(max-width:820px) 92vw, 45vw" alt="Équipe qui célèbre un succès" loading="lazy"></div><p>Rétablir le dialogue, consolider les équipes et préparer la suite, sans répéter ce qui a mené à la crise.</p>{qui("france-belisle","andreanne-thibault","nicolas-roy")}</article>
    </div>
  </div>
</section>

<section class="preuve"><div class="preuve-fond" aria-hidden="true" style="background-image:image-set(url(img/equipe-reseau-1400.webp) 1x)" data-parbg></div>
  <span class="deco" aria-hidden="true"></span>
  <div class="w">
    <span class="eb ap">{MARQUE} Le réseau en chiffres</span>
    <div class="chiff">
      <div class="ap"><div class="v" data-c="9">9</div><p>experts collaborateurs, choisis pour leur façon de travailler</p></div>
      <div class="ap"><div class="v o" data-c="10">10</div><p>domaines d’expertise qui se parlent entre eux</p></div>
      <div class="ap"><div class="v">1</div><p>seule prise de contact pour tout mettre en mouvement</p></div>
    </div>
    <p class="note ap">Près de <span>70 organisations</span> accompagnées par l’équipe fondatrice en deux ans. Le Centre met ce réseau à votre portée.</p>
  </div>
</section>

<div class="bandeau-photos" aria-hidden="true">
  <div class="rang r1">{BANDE1}{BANDE1}</div>
  <div class="rang r2">{BANDE2}{BANDE2}</div>
</div>

<section class="sec">
  <div class="w">
    <span class="eb ap">{MARQUE} Pourquoi le Centre existe</span>
    <div class="voix">
      <figure class="vx ap"><q>On peut être entouré toute la journée et ne pas savoir à qui parler de ce qui nous préoccupe. Demander un coup de main, c’est une force.</q><figcaption class="qui"><img src="img/france-belisle.webp" alt="France Bélisle" width="58" height="58"><div><b>France Bélisle</b><span>Cofondatrice, première femme mairesse de Gatineau</span></div></figcaption></figure>
      <figure class="vx ap" style="transition-delay:.1s"><q>Les dirigeants jonglent avec des enjeux qui se croisent. Ils ont besoin de gens de confiance pour y voir clair, sans multiplier les démarches.</q><figcaption class="qui"><img src="img/nicolas-roy.webp" alt="Nicolas Roy" width="58" height="58"><div><b>Nicolas Roy</b><span>Cofondateur, Adm.A., CRHA</span></div></figcaption></figure>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="w">
    <p class="enonce">Subir l’imprévu coûte cher. Savoir <mark>qui appeler</mark> change tout.</p>
    <h2 class="eb ap" style="margin-top:7vh">{MARQUE} Ce que vous obtenez</h2>
    <div class="benef">
      <div class="bn ap"><span class="n">01</span><h3>Des décisions qui avancent.</h3><p>Moins de dossiers en suspens, plus de choix assumés et suivis.</p></div>
      <div class="bn ap" style="transition-delay:.08s"><span class="n">02</span><h3>Des équipes qui restent.</h3><p>Un climat plus sain, moins d’épuisement, une culture qui tient.</p></div>
      <div class="bn ap" style="transition-delay:.16s"><span class="n">03</span><h3>Une organisation qui tient.</h3><p>Des pratiques solides en finances, conformité et gouvernance.</p></div>
      <div class="bn ap" style="transition-delay:.24s"><span class="n">04</span><h3>Un dirigeant moins seul.</h3><p>Des gens de confiance à qui parler, au bon moment.</p></div>
    </div>
  </div>
</section>

<section id="experts" class="reseau" aria-labelledby="res-t">
  <div class="w">
    <div class="res-t">
      <div><span class="eb clair">{MARQUE} Qui nous sommes</span><h2 id="res-t" class="grand clair">Neuf experts. <em>Une constellation de confiance.</em></h2></div>
      <div><p style="margin-bottom:16px;color:#C9D6E0">Choisissez un enjeu. Voyez qui, dans le réseau, s’allume pour vous. Survolez un visage pour faire connaissance.</p><div class="chips" id="chips"></div></div>
    </div>
    <div class="ciel" id="ciel"><canvas aria-hidden="true"></canvas><div class="fiche" id="fiche" aria-live="polite"></div></div>
    <div class="exg">{experts_html}</div>
  </div>
</section>

<section class="sec" id="en-bref" style="padding-top:0">
  <div class="w sv">
    <div class="ap">
      <span class="eb">{MARQUE} En bref</span>
      <h2 class="grand" style="font-size:clamp(2.2rem,4.4vw,3.8rem)">Le Centre, en une minute.</h2>
      <p class="def">Le Centre des dirigeants est un réseau de neuf collaborateurs experts, lancé en novembre 2026 à Gatineau par France Bélisle et Nicolas Roy, qui accompagne les dirigeants de PME et d’OBNL à partir d’une seule prise de contact.</p>
      <dl>
        <dt>Pour qui</dt><dd>Dirigeants de PME et d’OBNL, conseils d’administration</dd>
        <dt>Où</dt><dd>Gatineau, Outaouais et ailleurs au Québec</dd>
        <dt>Approche</dt><dd>Continuum PUR : Prévention, Urgence, Reconstruction</dd>
        <dt>Outils</dt><dd>Tests AtmanPro, sondages sur mesure, marque employeur Adhésion</dd>
        <dt>Accès</dt><dd>{MAIL}</dd>
      </dl>
    </div>
    <div class="faq ap"><h3 class="eb" style="margin-bottom:8px">{MARQUE} Questions fréquentes</h3>{faq_html}</div>
  </div>
</section>

<section class="fin" id="parler" aria-labelledby="fin-t">
  <div class="w">
    <span class="eb">{MARQUE} Par où commencer ?</span>
    <h2 id="fin-t" class="ap">Êtes-vous <span>prêt ?</span></h2>
    <div class="g">
      <div>
        <figure class="fin-photo ap"><img src="img/bureau-sourire-1400.webp" srcset="img/bureau-sourire-800.webp 800w, img/bureau-sourire-1400.webp 1400w" sizes="(max-width:820px) 92vw, 45vw" alt="Dirigeante souriante à son bureau" loading="lazy"></figure>
        <p>Dites-nous ce qui se passe, dans vos mots. Une personne vous lit et vous répond.</p>
        <div class="marie"><img src="img/marie-eve-venner.webp" alt="Marie-Eve Venner" width="64" height="64"><div><b>Marie-Eve Venner</b><br><span>Votre point de contact · {MAIL}</span></div></div>
      </div>
      <div>
        <form id="form" novalidate>
          <label for="nom">Nom</label><input id="nom" name="nom" autocomplete="name">
          <label for="org">Organisation et rôle</label><input id="org" name="org" autocomplete="organization">
          <label for="mail">Courriel</label><input id="mail" name="mail" type="email" autocomplete="email">
          <label for="msg">Votre situation</label><textarea id="msg" name="msg" placeholder="Ce qui se passe, ce qui presse, ce que vous avez déjà essayé…"></textarea>
          <div class="pot" aria-hidden="true"><label for="site_web">Ne pas remplir</label><input id="site_web" name="site_web" tabindex="-1" autocomplete="off"></div>
          <label class="consent"><input type="checkbox" id="ok" name="consentement" value="oui"> <span>J’accepte que le Centre des dirigeants utilise ces renseignements pour répondre à ma demande et, au besoin, les transmette aux seuls experts concernés. <a href="politique-confidentialite.html">Politique de confidentialité</a></span></label>
          <div style="margin-top:8px"><button class="btn" type="submit" id="envoyer">Envoyer ma demande <span class="fl">→</span></button></div>
          <p class="delai">Réponse personnelle sous deux jours ouvrables.</p>
          <p class="err" id="err" role="alert"></p>
        </form>
        <div class="ret" id="merci" role="status" aria-live="polite"><b style="font-size:1.4rem">Merci. Votre demande est bien reçue.</b><p style="margin-top:8px">Marie-Eve vous répondra personnellement sous deux jours ouvrables.</p></div>
        <div class="ret" id="ret" role="status" aria-live="polite"><b>Votre message est prêt.</b><p>Envoyez-le à {MAIL}. Si votre messagerie ne s’ouvre pas, copiez le texte.</p><pre></pre><a class="btn" id="ouvrir" href="#">Ouvrir ma messagerie <span class="fl">→</span></a> <button class="btn or" type="button" id="copier">Copier</button></div>
      </div>
    </div>
  </div>
</section>
</main>
<footer><div class="w"><img src="img/logo.png" alt="Centre des dirigeants" width="900" height="330"><span>Gatineau, Québec · {MAIL}</span><span>© 2026 Centre des dirigeants. Une initiative de Posture Inc. · <a href="politique-confidentialite.html">Politique de confidentialité</a></span></div></footer>
<script>{JS}</script>
</body>
</html>
"""
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
fichiers_robots(OUT, ["index.html"], EXPERTS, EXPERTISES, FAQ)
p = os.path.join(OUT, "llms.txt"); s = open(p, encoding="utf-8").read()
s = s[:s.index("## Pages")] + "## Sections de la page\n- [Ce qu’on fait](" + BASE + "#ce-qu-on-fait)\n- [Comment](" + BASE + "#comment)\n- [Les experts](" + BASE + "#experts)\n- [En bref et FAQ](" + BASE + "#en-bref)\n- [Nous écrire](" + BASE + "#parler)\n"
open(p, "w", encoding="utf-8").write(s)
print("ok", len(html))

# ---------------- Politique de confidentialité (premier jet, Loi 25)
POL = f"""<!DOCTYPE html>
<html lang="fr-CA">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Politique de confidentialité | Centre des dirigeants</title>
<meta name="description" content="Comment le Centre des dirigeants recueille, utilise, communique et protège vos renseignements personnels, conformément à la Loi 25 du Québec.">
<link rel="canonical" href="{BASE}politique-confidentialite.html">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png">
<style>
@font-face{{font-family:LS;src:url(fonts/LeagueSpartan-Regular.woff2) format("woff2");font-weight:400;font-display:swap}}
@font-face{{font-family:LS;src:url(fonts/LeagueSpartan-Bold.woff2) format("woff2");font-weight:700;font-display:swap}}
body{{margin:0;font-family:LS,system-ui,sans-serif;background:#F2EDE7;color:#0C283A;font-size:18px;line-height:1.6}}
.w{{width:min(820px,100% - 48px);margin-inline:auto}}
header{{padding:28px 0;border-bottom:1px solid rgba(12,40,58,.14)}}
header img{{height:46px;width:auto}}
h1{{font-size:clamp(2.2rem,5vw,3.4rem);line-height:1;letter-spacing:-.03em;margin:60px 0 10px}}
h2{{font-size:1.4rem;margin:44px 0 10px;letter-spacing:-.01em}}
p,li{{color:#2B3E4C}} ul{{padding-left:22px}} li{{margin:6px 0}}
a{{color:#0C283A;font-weight:700}}
.maj{{color:#4C6577}}
.brouillon{{background:#fff;border-left:5px solid #86651F;border-radius:10px;padding:16px 20px;margin-top:28px;font-size:.95rem}}
.cases{{background:#fff;border-radius:16px;padding:20px 24px}}
footer{{margin-top:80px;padding:30px 0 50px;border-top:1px solid rgba(12,40,58,.14);font-size:.9rem;color:#4C6577}}
</style>
</head>
<body>
<header><div class="w"><a href="index.html"><img src="img/logo.png" alt="Centre des dirigeants, retour à l’accueil" width="900" height="330"></a></div></header>
<main class="w">

<h1>Politique de confidentialité</h1>
<p class="maj">Dernière mise à jour : 11 novembre 2026</p>
<p>Le Centre des dirigeants accorde une grande importance à la protection de vos renseignements personnels. Cette politique explique quels renseignements nous recueillons, pourquoi, avec qui nous les partageons et comment exercer vos droits, conformément à la Loi sur la protection des renseignements personnels dans le secteur privé du Québec, modifiée par la Loi 25.</p>

<h2>1. Qui nous sommes</h2>
<p>Le Centre des dirigeants est une initiative de Posture Inc. (16650473 Canada Inc.), à Gatineau, Québec. Posture Inc. est responsable des renseignements recueillis par ce site.</p>

<h2>2. Responsable de la protection des renseignements personnels</h2>
<div class="cases"><p style="margin:0"><b>Marie-Eve Venner</b>, coordonnatrice<br>Responsable de la protection des renseignements personnels<br>4, rue Dumas, bureau 101, Gatineau (Québec) J8Y 2M5<br>Courriel : <a href="mailto:confidentialite@centredesdirigeants.ca">confidentialite@centredesdirigeants.ca</a></p></div>
<p>Toute question sur cette politique ou sur vos renseignements peut lui être adressée.</p>

<h2>3. Renseignements recueillis</h2>
<p>Lorsque vous nous écrivez par le formulaire ou par courriel, nous recueillons :</p>
<ul><li>votre nom;</li><li>votre organisation et votre rôle, si vous les indiquez;</li><li>votre adresse courriel;</li><li>le contenu de votre message, qui peut décrire la situation de votre organisation.</li></ul>
<p>Nous vous invitons à ne pas inclure dans votre premier message de renseignements sensibles, comme des renseignements de santé ou des informations sur des tiers identifiables. Nous pourrons en discuter de façon plus sécuritaire par la suite.</p>

<h2>4. Pourquoi nous les utilisons</h2>
<ul><li>Répondre à votre demande.</li><li>Comprendre votre situation et vous orienter vers les experts pertinents.</li><li>Assurer le suivi et la coordination de l’accompagnement.</li></ul>
<p>Nous n’utilisons pas vos renseignements à d’autres fins sans votre consentement, et nous ne les vendons jamais.</p>

<h2>5. Avec qui nous les partageons</h2>
<p>Les experts du Centre sont des professionnels et des entreprises distincts. Avec votre consentement, nous transmettons à l’expert ou aux experts concernés uniquement les renseignements nécessaires pour vous accompagner. Chacun est tenu de les protéger et de ne les utiliser que pour cette fin.</p>
<p>Nous faisons aussi appel à des fournisseurs technologiques pour recevoir et conserver les demandes : Google Forms, notre messagerie électronique Google Workspace et, pour l’infolettre, Mailchimp. Ces fournisseurs peuvent conserver des données à l’extérieur du Québec. Avant toute communication hors Québec, nous évaluons que les renseignements y bénéficieront d’une protection adéquate, comme l’exige la loi.</p>

<h2>6. Durée de conservation</h2>
<p>Nous conservons vos renseignements pendant 24 mois après notre dernier échange, puis nous les détruisons de façon sécuritaire, sauf si une obligation légale exige une conservation plus longue.</p>

<h2>7. Sécurité</h2>
<p>L’accès à vos renseignements est limité aux personnes qui en ont besoin pour traiter votre demande. Nous utilisons des comptes protégés par authentification et des communications chiffrées.</p>

<h2>8. Vos droits</h2>
<p>Vous pouvez en tout temps :</p>
<ul><li>demander l’accès aux renseignements que nous détenons à votre sujet;</li><li>en demander la rectification;</li><li>retirer votre consentement à leur utilisation ou à leur communication;</li><li>demander qu’ils soient supprimés lorsque leur conservation n’est plus nécessaire.</li></ul>
<p>Écrivez à la personne responsable indiquée à la section 2. Nous répondons dans un délai de 30 jours. Si vous n’êtes pas satisfait de notre réponse, vous pouvez porter plainte auprès de la <a href="https://www.cai.gouv.qc.ca/">Commission d’accès à l’information du Québec</a>.</p>

<h2>9. Témoins et mesure d’audience</h2>
<p>Ce site n’utilise pas de témoins publicitaires ni d’outils de suivi. Il enregistre seulement dans votre navigateur votre préférence pour les animations (en pause ou non). Il n’utilise aucun outil de mesure d’audience.</p>

<h2>10. Modifications</h2>
<p>Nous pouvons mettre cette politique à jour. La date de la dernière mise à jour figure en haut de la page.</p>
</main>
<footer><div class="w">© 2026 Centre des dirigeants · <a href="index.html">Retour à l’accueil</a></div></footer>
</body>
</html>
"""
open(os.path.join(OUT, "politique-confidentialite.html"), "w", encoding="utf-8").write(POL)
sm = os.path.join(OUT, "sitemap.xml"); t = open(sm, encoding="utf-8").read()
t = t.replace("</urlset>", f"  <url><loc>{BASE}politique-confidentialite.html</loc><lastmod>2026-11-08</lastmod><priority>0.3</priority></url>\n</urlset>")
open(sm, "w", encoding="utf-8").write(t)
print("politique ok")
