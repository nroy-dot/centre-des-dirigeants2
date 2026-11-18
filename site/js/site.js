/* Centre des dirigeants : scripts communs */
(function(){
/* ---- Réglages à compléter avant la mise en ligne ---- */
var FORM_ENDPOINT = '';  /* service d'envoi du formulaire de contact, ex. https://formspree.io/f/xxxxxxx */
var NL_ENDPOINT   = '';  /* service d'inscription à ENTRE NOUS, ex. formulaire HubSpot ou Mailchimp */
var MAIL = 'info@centredesdirigeants.ca';

var R = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function $(s,c){return (c||document).querySelector(s)}
function $$(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}

/* En-tête et menu */
var hd=$('.hd');
function f(){if(!hd.classList.contains('solide'))hd.classList.toggle('pl',scrollY>30)}
f();addEventListener('scroll',f,{passive:true});
var mb=$('.menu');
if(mb){mb.addEventListener('click',function(){var o=hd.classList.toggle('ouvert');mb.setAttribute('aria-expanded',o?'true':'false');document.body.style.overflow=o?'hidden':''});
 $$('.hd nav a').forEach(function(a){a.addEventListener('click',function(){hd.classList.remove('ouvert');document.body.style.overflow=''})});}

/* Titres mot à mot et apparitions */
$$('.grand,.enonce').forEach(function(h){var i=0;h.innerHTML=h.innerHTML.split(/(<[^>]+>|\s+)/).filter(Boolean).map(function(t){if(/^<|^\s+$/.test(t))return t;return '<span class="mo"><span style="transition-delay:'+(i++*0.045)+'s">'+t+'</span></span>'}).join('');h.classList.add('ap')});
var io='IntersectionObserver' in window?new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){x.target.classList.add('vu');io.unobserve(x.target)}})},{threshold:.12}):null;
$$('.ap').forEach(function(e){io?io.observe(e):e.classList.add('vu')});

/* Compteurs */
$$('[data-c]').forEach(function(el){if(!('IntersectionObserver' in window))return;var fin=+el.dataset.c;var o=new IntersectionObserver(function(e){if(e[0].isIntersecting){o.disconnect();if(R){el.textContent=fin;return}var t0=null;(function p(t){if(!t0)t0=t;var k=Math.min((t-t0)/1500,1);el.textContent=Math.round(fin*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(p)})(performance.now())}},{threshold:.6});o.observe(el)});

/* Pause des animations */
var bp=$('#pause');
function fige(v){R=v;document.body.classList.toggle('fige',v);if(bp){bp.setAttribute('aria-pressed',v?'true':'false');$('.tx',bp).textContent=v?'Relancer les animations':'Mettre les animations en pause'}try{localStorage.setItem('cdd-fige',v?'1':'0')}catch(e){}}
if(bp)bp.addEventListener('click',function(){fige(!document.body.classList.contains('fige'))});
try{if(localStorage.getItem('cdd-fige')==='1')fige(true)}catch(e){}
if(R)fige(true);

/* Diaporama de l'accueil */
var ds=$$('.diapo'),cd=$$('.compteur-d i'),di=0;
if(ds.length>1){setInterval(function(){if(R)return;ds[di].classList.remove('on');if(cd[di])cd[di].classList.remove('on');di=(di+1)%ds.length;void ds[di].offsetWidth;ds[di].classList.add('on');if(cd[di]){void cd[di].offsetWidth;cd[di].classList.add('on')}},6000)}

/* Parallaxe */
var par=$$('[data-par]'),pbg=$('[data-parbg]');
function px(){if(R)return;var h=innerHeight;par.forEach(function(im){var r=im.parentNode.getBoundingClientRect();if(r.bottom<0||r.top>h)return;var k=parseFloat(im.dataset.par);im.style.transform='translateY('+((r.top+r.height/2-h/2)*k-r.height*.08)+'px)'});
 if(pbg){var r=pbg.parentNode.getBoundingClientRect();pbg.style.transform='translateY('+(r.top*-.12)+'px)'}}
addEventListener('scroll',function(){requestAnimationFrame(px)},{passive:true});px();

/* Constellation des experts */
var ciel=$('#ciel');
if(ciel&&window.CDD_EXP){
 var EXP=window.CDD_EXP,ENJ=window.CDD_ENJ||[],cv=$('canvas',ciel),cx=cv.getContext('2d'),fiche=$('#fiche');
 var base=[[.5,.5],[.2,.3],[.8,.26],[.1,.7],[.35,.82],[.63,.84],[.9,.64],[.3,.1],[.68,.08]];
 var ordre=['marie-eve-venner','nicolas-roy','france-belisle','chantal-dufort','andreanne-thibault','yannick-beaulieu','sophie-ann-bellisle','daniel-feeny','marc-antoine-laramee'];
 var noeuds=[],actif=null,filtre=null,lien=ciel.dataset.lien;
 function montre(s){actif=s;var e=EXP[s],url=lien==='pages'?(s==='marie-eve-venner'?'contact.html':'expert-'+s+'.html'):lien+'#'+s,txt=s==='marie-eve-venner'?'Nous joindre':'Voir le profil complet';
  fiche.innerHTML='<div class="f-tete"><img src="img/'+s+'.webp" alt=""><div><span class="r">'+esc(e.o||e.r)+'</span><h3>'+esc(e.n)+(e.c?'<small>'+esc(e.c)+'</small>':'')+'</h3></div></div><p>'+esc(e.d)+'</p>'+(lien?'<a class="f-lien" href="'+url+'">'+txt+' <span aria-hidden="true">→</span></a>':'');
  fiche.classList.add('vu');ciel.classList.add('focus');place();noeuds.forEach(function(n){n.el.classList.toggle('on',n.s===s)})}
 function place(){if(!actif)return;var n=null;noeuds.forEach(function(m){if(m.s===actif)n=m});if(!n||n.x==null)return;
  var W=ciel.clientWidth,H=ciel.clientHeight,cw=fiche.offsetWidth,ch=fiche.offsetHeight,rad=n.el.offsetWidth/2+20,g=n.x>W/2;
  var l=g?n.x-rad-cw:n.x+rad;l=Math.max(0,Math.min(W-cw,l));var t=Math.max(8,Math.min(H-ch-8,n.y-ch/2));
  fiche.style.left=l+'px';fiche.style.top=t+'px';fiche.classList.toggle('g',g);fiche.style.setProperty('--ay',Math.max(24,Math.min(ch-24,n.y-t))+'px')}
 ordre.forEach(function(s,i){var d=document.createElement('button');d.className='etoile';d.type='button';d.setAttribute('aria-label',EXP[s].n+', '+EXP[s].r);
  d.innerHTML='<img src="img/'+s+'.webp" alt=""><b>'+esc(EXP[s].n.split(' ')[0])+'</b>';ciel.appendChild(d);
  noeuds.push({s:s,el:d,bx:base[i][0],by:base[i][1],ph:Math.random()*6.28,sp:.35+Math.random()*.4});
  d.addEventListener('mouseenter',function(){montre(s)});d.addEventListener('focus',function(){montre(s)});d.addEventListener('click',function(){if(lien==='pages'&&s!=='marie-eve-venner'){location.href='expert-'+s+'.html'}else{montre(s)}})});
 ciel.addEventListener('mouseleave',function(){ciel.classList.remove('focus');if(filtre){actif=null;fiche.classList.remove('vu')}if(!filtre){actif=null;fiche.classList.remove('vu');noeuds.forEach(function(n){n.el.classList.remove('on')})}});
 function taille(){var r=ciel.getBoundingClientRect(),d=devicePixelRatio||1;cv.width=r.width*d;cv.height=r.height*d;cx.setTransform(d,0,0,d,0,0)}
 taille();addEventListener('resize',taille);
 var t0=performance.now();
 (function anime(t){var r=ciel.getBoundingClientRect(),W=r.width,H=r.height,tt=((t||t0)-t0)/1000;
  if(r.bottom>0&&r.top<innerHeight&&W>0){
  noeuds.forEach(function(n){var a=R?0:1;n.x=(n.bx+Math.sin(tt*n.sp+n.ph)*.018*a)*W;n.y=(n.by+Math.cos(tt*n.sp*.8+n.ph)*.03*a)*H;n.el.style.left=n.x+'px';n.el.style.top=n.y+'px'});if(actif)place();
  cx.clearRect(0,0,W,H);
  noeuds.forEach(function(n,i){noeuds.forEach(function(m,j){if(j<=i)return;var lie=(i===0)||(Math.hypot(n.bx-m.bx,n.by-m.by)<.34);if(!lie)return;
   var fort=(actif&&(n.s===actif||m.s===actif))||(filtre&&filtre.indexOf(n.s)>-1&&filtre.indexOf(m.s)>-1);
   cx.strokeStyle=fort?'rgba(213,172,89,.95)':'rgba(198,222,244,'+(i===0?.18:.1)+')';cx.lineWidth=fort?2:1;cx.beginPath();cx.moveTo(n.x,n.y);cx.lineTo(m.x,m.y);cx.stroke();
   if(fort&&!R){var fr=(tt*.6)%1;cx.fillStyle='#D5AC59';cx.beginPath();cx.arc(n.x+(m.x-n.x)*fr,n.y+(m.y-n.y)*fr,3,0,6.3);cx.fill()}})});}
  requestAnimationFrame(anime)})();
 var chips=$('#chips'),cartes=$$('[data-expert]');
 if(chips)ENJ.forEach(function(e){var b=document.createElement('button');b.className='chip';b.type='button';b.textContent=e.t;b.setAttribute('aria-pressed','false');
  b.onclick=function(){var deja=b.getAttribute('aria-pressed')==='true';$$('.chip',chips).forEach(function(c){c.setAttribute('aria-pressed','false')});
   if(deja){filtre=null;noeuds.forEach(function(n){n.el.classList.remove('off','on')});cartes.forEach(function(c){c.classList.remove('off')});fiche.classList.remove('vu');var cd=$('#chipd');if(cd)cd.textContent='';return}
   b.setAttribute('aria-pressed','true');filtre=['marie-eve-venner'].concat(e.e);
   noeuds.forEach(function(n){n.el.classList.toggle('off',filtre.indexOf(n.s)<0);n.el.classList.toggle('on',e.e.indexOf(n.s)>-1)});
   cartes.forEach(function(c){c.classList.toggle('off',filtre.indexOf(c.dataset.expert)<0)});
   actif=null;fiche.classList.remove('vu');var cd=$('#chipd');if(cd)cd.innerHTML='<b>'+e.e.map(function(s){return esc(EXP[s].n)}).join(', ')+'</b> · '+esc(e.d)};
  chips.appendChild(b)});
}

/* Formulaire de contact */
var fm=$('#form');
if(fm){
 var ret=$('#ret'),merci=$('#merci'),err=$('#err'),corps='';
 var p=new URLSearchParams(location.search),t=p.get('type');
 if(t){var r=fm.querySelector('input[name=type][value="'+t+'"]');if(r)r.checked=true}
 try{var h=location.hash.replace('#','');if(h.indexOf('type-')===0){var r2=fm.querySelector('input[name=type][value="'+h.slice(5)+'"]');if(r2)r2.checked=true}}catch(e){}
 function repli(n,ty){$('pre',ret).textContent=corps;
  $('#ouvrir').href='mailto:'+MAIL+'?subject='+encodeURIComponent(ty+' : '+n)+'&body='+encodeURIComponent(corps);
  fm.style.display='none';ret.classList.add('vu')}
 fm.addEventListener('submit',function(ev){ev.preventDefault();err.textContent='';
  if(fm.site_web.value)return;
  var n=fm.nom.value.trim(),o=fm.org.value.trim(),m=fm.mail.value.trim(),x=fm.msg.value.trim(),ty=(fm.querySelector('input[name=type]:checked')||{}).dataset;ty=ty&&ty.l?ty.l:'Demande au Centre des dirigeants';
  var manque=[];[fm.nom,fm.mail,fm.msg].forEach(function(c){var v=c.value.trim();c.style.borderColor=v?'':'#9B2C1A';if(!v)manque.push(c)});
  if(manque.length){err.textContent='Merci de remplir votre nom, votre courriel et votre message.';manque[0].focus();return}
  if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(m)){err.textContent='Ce courriel ne semble pas valide.';fm.mail.focus();return}
  if(!fm.ok.checked){err.textContent='Merci de cocher la case de consentement.';fm.ok.focus();return}
  corps=ty+'\n\n'+x+'\n\n'+n+(o?'\n'+o:'')+'\n'+m;
  if(!FORM_ENDPOINT){repli(n,ty);return}
  var b=$('#envoyer');b.disabled=true;
  fetch(FORM_ENDPOINT,{method:'POST',headers:{'Accept':'application/json'},body:new FormData(fm)}).then(function(r){if(!r.ok)throw 0;fm.style.display='none';merci.classList.add('vu')}).catch(function(){repli(n,ty)});
 });
 var cp=$('#copier');if(cp)cp.addEventListener('click',function(){var b=this;try{navigator.clipboard.writeText(corps).then(function(){b.textContent='Message copié'},function(){b.textContent='Sélectionnez le texte'})}catch(e){b.textContent='Sélectionnez le texte'}});
}

/* Infolettre ENTRE NOUS */
$$('.f-nl').forEach(function(nf){
 nf.addEventListener('submit',function(ev){ev.preventDefault();var e=$('.err',nf),ok=nf.parentNode.querySelector('.nl-ok');e.textContent='';
  if(nf.site_web&&nf.site_web.value)return;
  var m=nf.courriel.value.trim(),pr=(nf.prenom?nf.prenom.value.trim():'');
  if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(m)){e.textContent='Merci d’inscrire un courriel valide.';nf.courriel.focus();return}
  if(!nf.ok.checked){e.textContent='Merci de confirmer votre consentement à recevoir ENTRE NOUS.';nf.ok.focus();return}
  function fini(){nf.style.display='none';ok.classList.add('vu')}
  if(!NL_ENDPOINT){location.href='mailto:'+MAIL+'?subject='+encodeURIComponent('Inscription à ENTRE NOUS')+'&body='+encodeURIComponent('Je souhaite recevoir ENTRE NOUS.\n\n'+(pr?pr+'\n':'')+m);fini();return}
  fetch(NL_ENDPOINT,{method:'POST',headers:{'Accept':'application/json'},body:new FormData(nf)}).then(function(r){if(!r.ok)throw 0;fini()}).catch(function(){e.textContent='Un problème est survenu. Écrivez-nous à '+MAIL+'.'});
 });
});

/* Filtres (ressources et agenda) */
$$('[data-filtres]').forEach(function(box){
 var cible=$(box.dataset.filtres);
 $$('.filtre',box).forEach(function(b){b.addEventListener('click',function(){$$('.filtre',box).forEach(function(x){x.setAttribute('aria-pressed','false')});b.setAttribute('aria-pressed','true');var v=b.dataset.v;
  $$('[data-cat]',cible).forEach(function(it){it.hidden=!(v==='tous'||it.dataset.cat.split(' ').indexOf(v)>-1)});
  var vide=$('.vide-filtre',cible.parentNode);if(vide)vide.hidden=$$('[data-cat]:not([hidden])',cible).length>0})});
});

/* Agenda : déplacer les activités passées */
var ag=$('#agenda');
if(ag){var auj=new Date();auj.setHours(0,0,0,0);var reste=0;
 var pas=$('#agenda-passe');$$('.ev',ag).forEach(function(ev){var x=(ev.dataset.fin||ev.dataset.date).split('-'),d=new Date(+x[0],x[1]-1,+x[2]);if(d<auj){if(pas){var l=ev.querySelector('.infos a');if(l)l.textContent='À propos de l’événement →';pas.insertBefore(ev,pas.firstChild);var sp=$('#passees');if(sp)sp.hidden=false}else ev.remove()}else reste++});
 if(!reste){var v=$('#agenda-vide');if(v)v.hidden=false;var fl=$('[data-filtres="#agenda"]');if(fl)fl.hidden=true}}
})();
