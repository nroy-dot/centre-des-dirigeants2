from PIL import Image, ImageDraw, ImageFilter, ImageChops
import os
S=['nicolas-roy','france-belisle','yannick-beaulieu','andreanne-thibault','chantal-dufort','daniel-feeny','sophie-ann-bellisle','marc-antoine-laramee','marie-eve-venner']
def make(s,W):
    hr=f'/home/claude/portraits/hr/{s}-detoure.png'
    cut=Image.open(hr if os.path.exists(hr) else f'/home/claude/portraits/{s}-detoure.png').convert('RGBA')
    a=cut.split()[3]
    k=max(1,round(cut.width/600))
    a=a.filter(ImageFilter.MinFilter(3 if k<2 else 5)).filter(ImageFilter.GaussianBlur(1.2*k))
    a=a.point(lambda v:0 if v<20 else v);cut.putalpha(a)
    bb=a.getbbox();top=bb[1];h=cut.height-top
    # pour les photos en pied (Yannick, Marie-Eve, Marcan), on recadre au buste
    head=a.crop((0,top,cut.width,top+int(h*.30))).getbbox()
    headw=(head[2]-head[0]) if head else cut.width*.4
    hs=(W*0.34)/headw; fs=(W*0.905)/h
    scale=max(hs,min(fs,hs*1.5))
    if fs>scale:  # buste trop court : fondu vers le bas
        from PIL import ImageDraw as _D
        g=Image.new('L',cut.size,255);dd=_D.Draw(g);n=int(cut.height*.16)
        for i in range(n):dd.line([(0,cut.height-n+i),(cut.width,cut.height-n+i)],fill=int(255*(1-i/n)))
        a=Image.composite(a,Image.new('L',cut.size,0),g) if False else ImageChops.multiply(a,g);cut.putalpha(a)
    cw=int(cut.width*scale);ch=int(cut.height*scale)
    c2=cut.resize((cw,ch),Image.LANCZOS)
    hx=(head[0]+head[2])/2*scale
    x=int(W/2-hx);y=int(W*0.10-top*scale)
    bg=Image.new('RGBA',(W,W),(12,40,58,255));d=ImageDraw.Draw(bg)
    d.pieslice((int(W*.24),int(W*.12),int(W*1.02),int(W*.9)),270,90,fill=(213,172,89,255))
    bg.alpha_composite(c2,(x,y))
    return bg.convert('RGB')
sheet=Image.new('RGB',(9*160,170),'white')
for i,s in enumerate(S):
    m=make(s,600);m.save(f'/home/claude/site8/img/{s}.webp',quality=86,method=6)
    g=make(s,1100);g.save(f'/home/claude/site8/img/{s}-grand.webp',quality=84,method=6);g.save(f'/home/claude/portraits/{s}-final.png')
    sheet.paste(m.resize((150,150),Image.LANCZOS),(i*160,10))
sheet.save('/home/claude/shots/portraits-hr.jpg',quality=85)
z=Image.new('RGB',(4*300,300))
for k,s in enumerate(['yannick-beaulieu','marc-antoine-laramee','sophie-ann-bellisle','daniel-feeny']):z.paste(Image.open(f'/home/claude/portraits/{s}-final.png').resize((300,300)),(k*300,0))
z.save('/home/claude/shots/portraits-hr-zoom.jpg',quality=85)
