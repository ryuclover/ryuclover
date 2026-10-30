"""Generate the profile's self-contained SVG assets using only Python's stdlib."""
from pathlib import Path
from html import escape
import random
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'terminal'
OUT.mkdir(parents=True, exist_ok=True)
BG, PANEL, LINE = '#090e0c', '#0c1310', '#24382e'
WHITE, GREEN, MUTED, AMBER = '#e4f0e8', '#9dffb0', '#789184', '#d9bd84'
FONT = 'ui-monospace, SFMono-Regular, Consolas, Liberation Mono, monospace'

PROJECTS = [
    ('olympus', 'Olympus Painel', 'PROSPECÇÃO / CRM', 'DESKTOP + WEB',
     ['Da descoberta de empresas à gestão comercial.', 'Leads, mapa, Kanban, reuniões e contratos.'],
     'React · Electron · Python / Flask · SQLite', 'https://github.com/ryuclover/Olympus-painel'),
    ('wide', 'Wide Studio', 'FERRAMENTAS CRIATIVAS', 'EXTENSÃO',
     ['Um novo fluxo de edição para o wide.video.', 'Drive público, importações e clipes vinculados.'],
     'TypeScript · Browser Extension · wide.video', 'https://github.com/ryuclover/wide-studio'),
    ('photopea', 'Photopea AI Studio', 'IMAGEM / IA', 'EXPERIMENTAL',
     ['Da seleção do canvas a uma nova camada.', 'Edição com IA, prévia e ajustes de borda.'],
     'React · TypeScript · SDXL · Hugging Face', 'https://github.com/ryuclover/photopea-ai-studio'),
    ('beehost', 'BeeHost', 'CLOUD / GAMES', 'FULL STACK',
     ['Do checkout PIX ao servidor Minecraft.', 'Vitrine, provisionamento e painel do cliente.'],
     'React · Node.js · Asaas · Daytona · PaperMC', 'https://github.com/ryuclover/BeeHost'),
    ('fast', 'Fast-Travel', 'MOBILIDADE', 'WEB APP',
     ['Menos abas. Mais caminhos para viajar.', 'Comparação de passagens e busca ID Jovem.'],
     'Next.js · TypeScript · APIs · Web Scraping', 'https://github.com/ryuclover/Fast-Travel'),
    ('serapeu', 'Serapeu', 'CONHECIMENTO', 'COLABORATIVO',
     ['Conhecimento que vira passo a passo.', 'Tutoriais, comunidade e controle de acesso.'],
     'Next.js · Supabase · PostgreSQL · Vitest', 'https://github.com/ryuclover/Serapeu'),
    ('masquerada', 'Masquerada', 'COMUNICAÇÃO / P2P', 'DESKTOP',
     ['Conexões entre pessoas, de ponto a ponto.', 'Mensagens, voz, tela e histórico local.'],
     'Electron · React · WebRTC · SQLite', 'https://github.com/ryuclover/Masquerada'),
]

def txt(x, y, value, size=16, color=WHITE, **attrs):
    extras=' '.join(f'{k.replace("_", "-")}="{escape(str(v))}"' for k,v in attrs.items())
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extras}>{escape(value)}</text>'

def line(x1,y1,x2,y2,color=LINE):
    return f'<path d="M{x1} {y1}H{x2}" stroke="{color}"/>' if y1==y2 else f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}"/>'

def frame(width,height,title,body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<defs>
 <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><path d="M0 1H4" stroke="#000" stroke-opacity=".15"/></pattern>
 <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="{GREEN}" stroke-opacity=".025"/></pattern>
 <linearGradient id="sweep"><stop stop-color="{GREEN}" stop-opacity="0"/><stop offset=".5" stop-color="{GREEN}" stop-opacity=".6"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
</defs>
<style>
 text {{ font-family: {FONT}; }}
 .blink {{ animation: blink 1.5s steps(2, end) infinite; }}
 .breathe {{ animation: breathe 4s ease-in-out infinite; }}
 .flow {{ animation: flow 6s linear infinite; }}
 .rain {{ animation: rain 13s linear infinite; }}
 .reveal {{ animation: reveal 3s steps(28, end) 1 both; }}
 @keyframes blink {{ 50% {{ opacity: .15; }} }}
 @keyframes breathe {{ 50% {{ opacity: .45; }} }}
 @keyframes flow {{ to {{ transform: translateX({width}px); }} }}
 @keyframes rain {{ to {{ transform: translateY(280px); }} }}
 @keyframes reveal {{ from {{ opacity: .25; }} to {{ opacity: 1; }} }}
</style>
<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="9" fill="{BG}" stroke="{LINE}"/>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="9" fill="url(#grid)"/>
{body}
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="9" fill="url(#scan)" pointer-events="none"/>
</svg>'''

GLYPHS={
'G':['01111','10000','10000','10111','10001','10001','01110'],
'A':['01110','10001','10001','11111','10001','10001','10001'],
'B':['11110','10001','10001','11110','10001','10001','11110'],
'R':['11110','10001','10001','11110','10100','10010','10001'],
'I':['11111','00100','00100','00100','00100','00100','11111'],
'E':['11111','10000','10000','11110','10000','10000','11111'],
'L':['10000','10000','10000','10000','10000','10000','11111'],
}

def pixel_name(x,y,p):
    result='<g aria-hidden="true" class="reveal">'
    for n,char in enumerate('GABRIEL'):
        for row,bits in enumerate(GLYPHS[char]):
            for col,bit in enumerate(bits):
                if bit=='1':
                    result+=f'<rect x="{x+n*6*p+col*p}" y="{y+row*p}" width="{p-1}" height="{p-1}" fill="{WHITE}" opacity="{.78+row*.03:.2f}"/>'
    return result+'</g>'

def clover(x,y,scale=1):
    s=f'<g transform="translate({x} {y}) scale({scale})" aria-hidden="true">'
    # Four heart-shaped leaves: a clover built from terminal glyphs, never a bitmap.
    for angle in (0,90,180,270):
        s+=f'<g transform="rotate({angle})" class="breathe"><path d="M0 0C-74-28-75-98-35-104C-14-108 0-88 0-76C0-88 14-108 35-104C75-98 74-28 0 0Z" fill="{GREEN}" fill-opacity=".025" stroke="{GREEN}" stroke-opacity=".52" stroke-width="1" stroke-dasharray="2 4"/>'
        for row,string in enumerate(['.:::.   .:::.',':::++::::++:::','::++######++::',' ::++####++:: ','   ::++++::   ','     ::::     ']):
            s+=txt(-61,-84+row*12,string,11,GREEN,opacity='.8')
        s+='</g>'
    s+=f'<circle r="8" fill="{BG}" stroke="{GREEN}"/><path d="M0 9Q28 56 12 84" fill="none" stroke="{GREEN}" stroke-width="2"/>'
    s+=txt(-48,140,'[ ryuclover ]',12,MUTED)
    return s+'</g>'

def rain(width,height,seed=7):
    rng=random.Random(seed); s='<g aria-hidden="true" opacity=".10">'
    for col in range(15):
        x=width*.54+col*(width*.46/15)
        s+=f'<g class="rain" style="animation-delay:-{rng.randrange(13)}s">'
        for y in range(-280,height,22):
            s+=txt(round(x),y,rng.choice('01{}<>/.:+*'),11,GREEN)
        s+='</g>'
    return s+'</g>'

def hero(mobile=False):
    w,h=(480,530) if mobile else (1000,490)
    x=24 if mobile else 40
    s=rain(w,h)+txt(x,32,'~/ryuclover',13,GREEN)
    s+=txt(w-24,32,'FULL STACK / DATA',11,MUTED,text_anchor='end')
    s+=line(x,50,w-x,50)
    s+=pixel_name(x,96,8 if mobile else 12)
    s+=txt(x,182 if mobile else 211,'SILVA  /  @RYUCLOVER',13,MUTED,letter_spacing='2')
    if mobile:
        s+=clover(410,125,.28)
        s+=txt(x,230,'> desenvolvedor full stack',19,GREEN)
        s+=txt(x,275,'Interfaces, APIs e automação.',18)
        s+=txt(x,304,'Da ideia ao código em produção.',18)
        s+=line(x,330,w-x,330)
        s+=txt(x,364,'$ cat sobre.txt',13,AMBER)
        for yy,ss in [(396,'TypeScript, Python e Go.'),(424,'Healthtech na TimeSaver.'),(452,'Análise de Dados na UFRJ.')]: s+=txt(x,yy,ss,16)
        s+=txt(x,500,'ENGENHARIA × PRODUTO × CURIOSIDADE',11,MUTED)
        s+=f'<rect class="blink" x="{w-38}" y="486" width="11" height="17" fill="{GREEN}"/>'
    else:
        s+=txt(x,257,'> desenvolvedor full stack',24,GREEN)
        s+=txt(x,310,'Construo interfaces, APIs e automações.',19)
        s+=txt(x,339,'Da ideia ao código em produção.',19)
        s+=clover(785,190,.9)
        s+=line(x,369,w-x,369)
        s+=txt(x,402,'$ cat sobre.txt',13,AMBER)
        s+=txt(x,432,'TypeScript, Python e Go · Healthtech na TimeSaver.',17)
        s+=txt(x,460,'Análise de Dados na UFRJ. Sempre construindo o próximo projeto.',16,MUTED)
        s+=f'<rect class="blink" x="941" y="445" width="11" height="18" fill="{GREEN}"/>'
    return frame(w,h,'Gabriel Silva / ryuclover — desenvolvedor full stack na TimeSaver e graduando em Análise de Dados na UFRJ',s)

def card(project,index,mobile=False):
    slug,name,domain,status,description,stack,url=project
    w,h=(480,273) if mobile else (1000,211)
    x=24 if mobile else 32
    s=txt(x,29,f'[{index:02d}] ~/{slug}',12,GREEN)
    s+=txt(w-x,29,status,11,AMBER,text_anchor='end')+line(1,46,w-1,46)
    s+=txt(x,92,name,25 if mobile else 30,font_weight='700',letter_spacing='-.6')
    if mobile:
        # Explicit line wraps keep every card readable at narrow viewport sizes.
        wraps={
          'olympus':['Da descoberta de empresas à gestão','comercial. Leads, mapa e Kanban.'],
          'wide':['Um novo fluxo para o wide.video.','Drive, importações e clipes vinculados.'],
          'photopea':['Da seleção do canvas a uma nova camada.','Edição com IA, prévia e ajustes de borda.'],
          'beehost':['Do checkout PIX ao servidor Minecraft.','Vitrine, nuvem e painel do cliente.'],
          'fast':['Menos abas. Mais caminhos para viajar.','Passagens de ônibus e busca ID Jovem.'],
          'serapeu':['Conhecimento que vira passo a passo.','Tutoriais e controle de acesso.'],
          'masquerada':['Conexões de ponto a ponto.','Mensagens, voz, tela e histórico local.'],
        }
        s+=txt(x,129,wraps[slug][0],15)+txt(x,153,wraps[slug][1],15)
        compact={'olympus':'React · Electron · Flask · SQLite','wide':'TypeScript · Browser Extension','photopea':'React · TypeScript · SDXL','beehost':'React · Node.js · Asaas · Daytona','fast':'Next.js · TypeScript · APIs','serapeu':'Next.js · Supabase · Vitest','masquerada':'Electron · React · WebRTC · SQLite'}
        s+=txt(x,191,compact[slug],13,MUTED)
        s+=line(x,213,w-x,213)+txt(x,245,domain,10,MUTED)+txt(w-x,245,'EXPLORAR ↗',13,GREEN,text_anchor='end')
    else:
        s+=txt(x,127,description[0],17)+txt(x,153,description[1],17)
        s+=txt(x,187,stack,13,MUTED)
        s+=txt(w-38,135,f'/{index:02d}',64,LINE,text_anchor='end',font_weight='700')
        s+=txt(w-35,186,'EXPLORAR ↗',13,GREEN,text_anchor='end')
    s+=f'<rect class="flow" x="-{w}" y="{h-2}" width="{w}" height="1" fill="url(#sweep)" style="animation-delay:-{index*.8}s"/>'
    return frame(w,h,name+' — '+description[0]+' '+description[1],s)

def button(label,hint,mobile=False):
    w,h=(150,50) if mobile else (320,57)
    label='PROJETOS' if mobile and label=='GUIA DE PROJETOS' else label
    s=txt(14 if mobile else 22,30 if mobile else 33,label,13 if mobile else 16,GREEN,font_weight='600')+txt(w-14 if mobile else 294,30 if mobile else 33,'↗',15 if mobile else 19,MUTED,text_anchor='end')
    return frame(w,h,label+' — '+hint,s)

def stack(mobile=False):
    w,h=(480,365) if mobile else (1000,268)
    x=24 if mobile else 32
    s=txt(x,31,'$ ls stack/',14,AMBER)+line(1,50,w-1,50)
    rows=[('FRONTEND','React · Next.js · TypeScript · Vite'),('BACKEND','Node.js · Python / Flask · Go'),('DADOS','PostgreSQL · Supabase · SQLite · MongoDB'),('INFRA','Docker · NGINX · Prometheus · Grafana'),('ENGENHARIA','Vitest · Git · SOLID · RLS')]
    for n,(label,tools) in enumerate(rows):
        y=83+n*(55 if mobile else 37)
        s+=txt(x,y,label,11,GREEN,letter_spacing='1')
        s+=txt(x if mobile else 205,y+23 if mobile else y,tools,13 if mobile else 16,WHITE)
    return frame(w,h,'Tecnologias utilizadas nos meus projetos',s)

def footer(mobile=False):
    w,h=(480,142) if mobile else (1000,130)
    x=24 if mobile else 32
    s=txt(x,35,'$ next --conversation',13,AMBER)
    s+=txt(x,75,'Bora construir alguma coisa?',22 if mobile else 27,GREEN,font_weight='700')
    s+=txt(x,109,'Tecnologia, projetos e novas conexões. ↗',13 if mobile else 16,MUTED)
    return frame(w,h,'Vamos conversar no LinkedIn: Gabriel Silva',s)

def save(name,text):
    ET.fromstring(text)
    assert '<script' not in text and '<foreignObject' not in text
    (OUT/name).write_text(text,encoding='utf-8',newline='\n')
    if not name.startswith('button-'):
        static=text.replace('</svg>','<style>.blink,.breathe,.flow,.rain,.reveal { animation: none !important; }</style></svg>')
        (OUT/(name[:-4]+'-static.svg')).write_text(static,encoding='utf-8',newline='\n')

def picture(slug,alt):
    return f'<picture>\n  <source media="(prefers-reduced-motion: reduce) and (max-width: 560px)" srcset="./assets/terminal/{slug}-mobile-static.svg">\n  <source media="(prefers-reduced-motion: reduce)" srcset="./assets/terminal/{slug}-static.svg">\n  <source media="(max-width: 560px)" srcset="./assets/terminal/{slug}-mobile.svg">\n  <img src="./assets/terminal/{slug}.svg" width="100%" alt="{escape(alt)}">\n</picture>'

def main():
    for mobile in (False,True):
        suffix='-mobile' if mobile else ''
        save(f'hero{suffix}.svg',hero(mobile))
        save(f'stack{suffix}.svg',stack(mobile))
        save(f'contact{suffix}.svg',footer(mobile))
        for i,p in enumerate(PROJECTS,1): save(f'project-{p[0]}{suffix}.svg',card(p,i,mobile))
    for slug,label in [('portfolio','PORTFÓLIO'),('linkedin','LINKEDIN'),('guide','GUIA DE PROJETOS')]:
        save(f'button-{slug}.svg',button(label,label))
        save(f'button-{slug}-mobile.svg',button(label,label,True))
    readme='<!-- Assets generated by tools/render_profile.py. -->\n\n'
    readme+=picture('hero','Gabriel Silva / ryuclover. Desenvolvedor Full Stack na TimeSaver e graduando em Análise de Dados na UFRJ. TypeScript, Python e Go.')+'\n\n'
    readme+='''<p align="center">
  <a href="https://site-six-gules-60.vercel.app"><picture><source media="(max-width: 560px)" srcset="./assets/terminal/button-portfolio-mobile.svg"><img src="./assets/terminal/button-portfolio.svg" width="32%" alt="Visitar meu portfólio"></picture></a>
  <a href="https://www.linkedin.com/in/gabrielmsas/"><picture><source media="(max-width: 560px)" srcset="./assets/terminal/button-linkedin-mobile.svg"><img src="./assets/terminal/button-linkedin.svg" width="32%" alt="Conversar no LinkedIn"></picture></a>
  <a href="https://github.com/ryuclover/Guia-dos-meus-projetos"><picture><source media="(max-width: 560px)" srcset="./assets/terminal/button-guide-mobile.svg"><img src="./assets/terminal/button-guide.svg" width="32%" alt="Explorar o guia dos meus projetos"></picture></a>
</p>

## Projetos em destaque

'''
    for p in PROJECTS:
        slug,name,domain,status,description,tools,url=p
        readme+=f'<a href="{url}">\n'+picture('project-'+slug,name+' — '+' '.join(description)+' '+tools)+'\n</a>\n\n'
    readme+='**[Explorar todos os projetos →](https://github.com/ryuclover/Guia-dos-meus-projetos)**\n\n'
    readme+=picture('stack','Tecnologias: React, Next.js, TypeScript, Node.js, Python, Go, PostgreSQL, Supabase, SQLite, MongoDB, Docker, NGINX, Prometheus, Grafana, Vitest e Git.')+'\n\n'
    readme+='<details>\n<summary>Índice dos projetos em texto</summary>\n\n'
    for p in PROJECTS: readme+=f'- **[{p[1]}]({p[-1]})** — {" ".join(p[4])}\n'
    readme+='\nMais projetos: **Clicktube**, **Pixelboard**, **mangator**, **Cornucopia**, **Módulo Mercado Pago**, **Projeto Korp**, **HÔTE** e meu **portfólio pessoal**. [Arquitetura, tecnologias e guias de execução](https://github.com/ryuclover/Guia-dos-meus-projetos).\n\n</details>\n\n'
    readme+='<a href="https://www.linkedin.com/in/gabrielmsas/">\n'+picture('contact','Bora construir alguma coisa? Vamos conversar sobre tecnologia, projetos e novas conexões no LinkedIn.')+'\n</a>\n'
    (ROOT/'README.md').write_text(readme,encoding='utf-8',newline='\n')
    print(f'Generated {len(list(OUT.glob("*.svg")))} SVG assets and README.md')

if __name__=='__main__': main()
