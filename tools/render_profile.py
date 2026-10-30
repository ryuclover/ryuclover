"""Generate the profile's self-contained SVG assets using only Python's stdlib."""
from pathlib import Path
from html import escape
import random
import json
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
 .clover-drift {{ animation: clover-drift 4s ease-in-out infinite; }}
 @keyframes blink {{ 50% {{ opacity: .15; }} }}
 @keyframes breathe {{ 50% {{ opacity: .45; }} }}
 @keyframes flow {{ to {{ transform: translateX({width}px); }} }}
 @keyframes rain {{ to {{ transform: translateY(280px); }} }}
 @keyframes reveal {{ from {{ opacity: .25; }} to {{ opacity: 1; }} }}
 @keyframes clover-drift {{ 50% {{ transform: translateY(-9px); }} }}
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
    s=f'<g transform="translate({x} {y}) scale({scale})" aria-hidden="true"><g class="clover-drift">'
    # Four heart-shaped leaves: a clover built from terminal glyphs, never a bitmap.
    for angle in (0,90,180,270):
        s+=f'<g transform="rotate({angle})" class="breathe" style="animation-delay:-{angle/90*.7}s"><path d="M0 0C-74-28-75-98-35-104C-14-108 0-88 0-76C0-88 14-108 35-104C75-98 74-28 0 0Z" fill="{GREEN}" fill-opacity=".025" stroke="{GREEN}" stroke-opacity=".52" stroke-width="1" stroke-dasharray="2 4"/>'
        for row,string in enumerate(['.:::.   .:::.',':::++::::++:::','::++######++::',' ::++####++:: ','   ::++++::   ','     ::::     ']):
            s+=txt(-61,-84+row*12,string,11,GREEN,opacity='.8')
        s+='</g>'
    s+=f'<circle r="8" fill="{BG}" stroke="{GREEN}"/><path d="M0 9Q28 56 12 84" fill="none" stroke="{GREEN}" stroke-width="2"/>'
    s+=txt(-48,140,'[ ryuclover ]',12,MUTED)
    return s+'</g></g>'

def rain(width,height,seed=7):
    rng=random.Random(seed); s='<g aria-hidden="true" opacity=".11">'
    for col in range(8):
        x=width*.54+col*(width*.46/8)
        s+=f'<g class="rain" style="animation-delay:-{rng.randrange(13)}s">'
        for y in range(-280,height,22):
            s+=txt(round(x),y,rng.choice('01{}<>/.:+*'),11,GREEN)
        s+='</g>'
    return s+'</g>'

def hero(mobile=False):
    w,h=(480,330) if mobile else (1000,310)
    x=24 if mobile else 40
    s=rain(w,h)+txt(x,32,'~/ryuclover',13,GREEN)
    s+=pixel_name(x,76,7 if mobile else 10)
    s+=clover(418,110,.25) if mobile else clover(816,140,.64)
    s+=txt(x,169 if mobile else 183,'> desenvolvedor full stack',19 if mobile else 22,GREEN)
    s+=txt(x,211 if mobile else 225,'Interfaces, APIs e automação.',17 if mobile else 18)
    if mobile:
        s+=txt(x,259,'TimeSaver · Healthtech',15,MUTED)
        s+=txt(x,284,'UFRJ · Análise de Dados',15,MUTED)
    else:
        s+=txt(x,270,'TimeSaver · Healthtech  /  UFRJ · Análise de Dados',16,MUTED)
    s+=f'<rect class="blink" x="{w-38}" y="{h-42}" width="9" height="15" fill="{GREEN}"/>'
    return frame(w,h,'Gabriel Silva / ryuclover — desenvolvedor full stack na TimeSaver e graduando em Análise de Dados na UFRJ',s)

def card(project,index,mobile=False):
    slug,name,domain,status,description,stack,url=project
    w,h=(480,166) if mobile else (1000,132)
    x=24 if mobile else 32
    concise={
        'olympus':['Prospecção e gestão de leads.','Mapa, Kanban, reuniões e contratos.'],
        'wide':['Extensão para editar no wide.video.','Drive, importações e clipes vinculados.'],
        'photopea':['Edição por seleção com IA no Photopea.','Resultado em uma nova camada.'],
        'beehost':['Hospedagem de servidores Minecraft.','Checkout PIX e provisionamento em nuvem.'],
        'fast':['Comparador de passagens de ônibus.','Busca por datas e benefícios ID Jovem.'],
        'serapeu':['Tutoriais colaborativos passo a passo.','Comunidade e controle de acesso.'],
        'masquerada':['Comunicação desktop de ponto a ponto.','Mensagens, voz e compartilhamento de tela.'],
    }
    s=txt(x,41,name,24 if mobile else 27,WHITE,font_weight='700')
    s+=txt(w-x,41,'↗',21,GREEN,text_anchor='end')
    if mobile:
        s+=txt(x,78,concise[slug][0],15)+txt(x,101,concise[slug][1],15,MUTED)
        short={'olympus':'React · Electron · Flask','wide':'TypeScript · Browser Extension','photopea':'React · TypeScript · SDXL','beehost':'React · Node.js · Daytona','fast':'Next.js · TypeScript · APIs','serapeu':'Next.js · Supabase · Vitest','masquerada':'Electron · WebRTC · SQLite'}
        s+=txt(x,141,short[slug],12,MUTED)
    else:
        s+=txt(x,76,' '.join(concise[slug]),16)
        s+=txt(x,107,stack,12,MUTED)
    return frame(w,h,name+' — '+' '.join(concise[slug]),s)

def button(label,hint,mobile=False):
    w,h=(150,50) if mobile else (320,57)
    label='PROJETOS' if mobile and label=='GUIA DE PROJETOS' else label
    s=txt(14 if mobile else 22,30 if mobile else 33,label,13 if mobile else 16,GREEN,font_weight='600')+txt(w-14 if mobile else 294,30 if mobile else 33,'↗',15 if mobile else 19,MUTED,text_anchor='end')
    return frame(w,h,label+' — '+hint,s)

def guide_card(mobile=False):
    w,h=(480,156) if mobile else (1000,133)
    x=24 if mobile else 32
    s=txt(x,31,'$ open projetos/',12,AMBER)
    s+=txt(x,71,'Guia dos Meus Projetos',24 if mobile else 28,WHITE,font_weight='700')
    s+=txt(w-x,71,'↗',22,GREEN,text_anchor='end')
    if mobile:
        s+=txt(x,107,'O mapa completo do meu portfólio.',15,MUTED)
        s+=txt(x,132,'Arquitetura, tecnologias e como executar.',14,MUTED)
    else:
        s+=txt(x,106,'O portfólio completo: arquitetura, tecnologias e guias de execução.',17,MUTED)
    return frame(w,h,'Guia dos Meus Projetos — catálogo completo, arquitetura, tecnologias e guias de execução',s)

def stats_card(mobile=False):
    data=json.loads((ROOT/'tools/profile_stats.json').read_text(encoding='utf-8'))
    w,h=(480,265) if mobile else (1000,282)
    x=24 if mobile else 32
    s=txt(x,33,'Estatísticas do GitHub',22 if mobile else 26,WHITE,font_weight='700')
    values=[(data['public_repos'],'repos públicos'),(data['followers'],'seguidores'),(data['calendar']['totalContributions'],'contribuições / 12 meses')]
    for i,(value,label) in enumerate(values):
        xx=x+i*(144 if mobile else 310)
        s+=txt(xx,88,str(value),29 if mobile else 34,GREEN,font_weight='700')
        if mobile and i==2:
            s+=txt(xx,109,'contribuições',11,MUTED)+txt(xx,125,'últimos 12 meses',10,MUTED)
        else: s+=txt(xx,115,label,11 if mobile else 13,MUTED)
    step,side=(8,6) if mobile else (16,12)
    colors=['#15231b','#254c31','#3b7748','#62b874',GREEN]
    s+='<g aria-hidden="true">'
    for col,week in enumerate(data['calendar']['weeks']):
        for day in week['contributionDays']:
            n=day['contributionCount']
            level=0 if n==0 else 1 if n<3 else 2 if n<7 else 3 if n<15 else 4
            s+=f'<rect x="{x+col*step}" y="{148+day["weekday"]*step}" width="{side}" height="{side}" rx="1.5" fill="{colors[level]}"/>'
    s+='</g>'
    date='/'.join(reversed(data['updated_at'].split('-')))
    s+=txt(x,244 if mobile else 267,f'Dados consultados em {date}',11,MUTED)
    return frame(w,h,f'Estatísticas do GitHub: {values[0][0]} repositórios públicos, {values[1][0]} seguidores e {values[2][0]} contribuições nos últimos 12 meses. Consulta em {date}.',s)

def tools_card(mobile=False):
    w,h=(480,314) if mobile else (1000,224)
    x=24 if mobile else 32
    s=txt(x,34,'Tecnologias e ferramentas',22 if mobile else 26,WHITE,font_weight='700')
    rows=[('FRONTEND','TypeScript · React · Next.js · Vite'),('BACKEND','Node.js · Python / Flask · Go'),('DADOS','PostgreSQL · Supabase · SQLite'),('INFRA / QUALIDADE','Docker · Git · Vitest · Grafana')]
    for n,(name,items) in enumerate(rows):
        y=76+n*60 if mobile else 79+n*38
        s+=txt(x,y,name,10 if mobile else 11,GREEN,letter_spacing='.7')
        s+=txt(x if mobile else 240,y+23 if mobile else y,items,14 if mobile else 16,WHITE)
    return frame(w,h,'Tecnologias e ferramentas: TypeScript, React, Next.js, Vite, Node.js, Python, Flask, Go, PostgreSQL, Supabase, SQLite, Docker, Git, Vitest e Grafana.',s)

def save(name,text):
    ET.fromstring(text)
    assert '<script' not in text and '<foreignObject' not in text
    (OUT/name).write_text(text,encoding='utf-8',newline='\n')

def picture(slug,alt):
    return f'<picture>\n  <source media="(max-width: 560px)" srcset="./assets/terminal/{slug}-mobile.svg?v=4">\n  <img src="./assets/terminal/{slug}.svg?v=4" width="100%" alt="{escape(alt)}">\n</picture>'

def main():
    for mobile in (False,True):
        suffix='-mobile' if mobile else ''
        save(f'hero{suffix}.svg',hero(mobile))
        save(f'guide{suffix}.svg',guide_card(mobile))
        save(f'stats{suffix}.svg',stats_card(mobile))
        save(f'tools{suffix}.svg',tools_card(mobile))
        for i,p in enumerate(PROJECTS,1): save(f'project-{p[0]}{suffix}.svg',card(p,i,mobile))
    for slug,label in [('portfolio','PORTFÓLIO'),('linkedin','LINKEDIN'),('guide','GUIA DE PROJETOS')]:
        save(f'button-{slug}.svg',button(label,label))
        save(f'button-{slug}-mobile.svg',button(label,label,True))
    readme='<!-- Assets generated by tools/render_profile.py. -->\n\n'
    readme+=picture('hero','Gabriel Silva / ryuclover. Desenvolvedor Full Stack na TimeSaver e graduando em Análise de Dados na UFRJ. TypeScript, Python e Go.')+'\n\n'
    readme+='''<p align="center">
  <a href="https://site-six-gules-60.vercel.app"><picture><source media="(max-width: 560px)" srcset="./assets/terminal/button-portfolio-mobile.svg"><img src="./assets/terminal/button-portfolio.svg" width="49%" alt="Visitar meu portfólio"></picture></a>
  <a href="https://www.linkedin.com/in/gabrielmsas/"><picture><source media="(max-width: 560px)" srcset="./assets/terminal/button-linkedin-mobile.svg"><img src="./assets/terminal/button-linkedin.svg" width="49%" alt="Conversar no LinkedIn"></picture></a>
</p>

'''
    readme+='<a href="https://github.com/ryuclover/Guia-dos-meus-projetos">\n'+picture('guide','Guia dos Meus Projetos — catálogo completo, arquitetura, tecnologias e guias de execução.')+'\n</a>\n\n## Projetos em destaque\n\n'
    for p in PROJECTS:
        slug,name,domain,status,description,tools,url=p
        readme+=f'<a href="{url}">\n'+picture('project-'+slug,name+' — '+' '.join(description)+' '+tools)+'\n</a>\n\n'
    readme+='<p>\n'+picture('stats','Estatísticas do GitHub: repositórios públicos, seguidores e contribuições nos últimos 12 meses. A data da consulta consta no card.')+'\n</p>\n\n'
    readme+='<p>\n'+picture('tools','Tecnologias e ferramentas — frontend, backend, dados, infraestrutura e qualidade.')+'\n</p>\n'
    (ROOT/'README.md').write_text(readme,encoding='utf-8',newline='\n')
    print(f'Generated {len(list(OUT.glob("*.svg")))} SVG assets and README.md')

if __name__=='__main__': main()
