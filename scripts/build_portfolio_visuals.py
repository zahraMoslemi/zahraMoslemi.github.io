"""Original schematic illustrations for Zahra's research portfolio.

These are explanatory diagrams, not experimental results or borrowed paper figures.
Run before build_portfolio.py after changing these illustrations.
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parents[1] / 'images' / 'research'
OUT.mkdir(parents=True, exist_ok=True)
COLORS = {'uncertainty': '#803750', 'science': '#256b68', 'agents': '#8c602e'}


def text(x, y, value, size=18, color='#44505a', anchor='start', weight=400):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>'


def line(x1, y1, x2, y2, color='#bac3ca', dashed=False):
    return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="2.5"'+(' stroke-dasharray="6 6"' if dashed else '')+'/>'


def circle(x, y, r=7, color='#803750'):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'


def box(x, y, w, h, label, color, fill='#fff', size=18):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{color}" stroke-width="1.5"/>'+text(x+w/2, y+h/2+6, label, size, color, 'middle', 500)


def arrow(x1, y1, x2, y2, color='#9aa6af'):
    return line(x1,y1,x2,y2,color)+f'<path d="M{x2-7} {y2-5}L{x2} {y2}L{x2-7} {y2+5}" fill="none" stroke="{color}" stroke-width="2"/>'


def save(name, title, topic, body, subtitle):
    color=COLORS[topic]
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">Conceptual illustration: {escape(subtitle)}.</desc><rect width="640" height="360" fill="#f7f8fa"/><g font-family="Arial, Helvetica, sans-serif">{text(32,40,title,19,color,weight=600)}{text(608,40,'SCHEMATIC',11,'#75808a','end')}{body}{text(32,333,subtitle,16,'#626d76')}</g></svg>'''
    (OUT / f'{name}.svg').write_text(svg+'\n')


def uncertainty():
    c=COLORS['uncertainty']
    body=line(65,272,575,272)+line(65,272,65,79)
    body+='<path d="M80 212 C155 118 230 237 298 172 S425 60 559 104 L559 224 C430 182 374 143 298 232 S160 225 80 269Z" fill="#ead8e0"/>'
    body+=f'<path d="M80 241 C160 174 224 247 298 202 S430 110 559 164" fill="none" stroke="{c}" stroke-width="3"/>'
    for x,y in [(91,237),(130,207),(177,220),(220,228),(273,207),(321,174),(364,157),(414,146),(462,158),(504,159),(549,161)]:body+=circle(x,y,4.5,c)
    body+=text(100,101,'Calibrated prediction regions',18,c)+text(492,294,'Input',15)
    return body
save('uncertainty','Learning with uncertainty','uncertainty',uncertainty(),'Bayesian inference + conformal prediction')
save('scope','Conformal-guided inference','uncertainty',uncertainty(),'Posterior exploration → calibrated predictions')

c=COLORS['uncertainty']
body=''
for x1,ys1,x2,ys2 in [(90,[130,190,250],210,[110,160,210,260]),(210,[110,160,210,260],330,[130,190,250])]:
    for y1 in ys1:
        for y2 in ys2:body+=line(x1,y1,x2,y2,'#d7c6d0')
for x,ys in [(90,[130,190,250]),(210,[110,160,210,260]),(330,[130,190,250])]:
    for y in ys:body+=circle(x,y,11,c)
body+=arrow(353,190,409,190,c)+line(426,255,597,255)
body+='<path d="M430 250 C474 250 459 106 507 106 S540 250 589 250" fill="#ead8e0" stroke="#803750" stroke-width="3"/>'
body+=text(204,297,'Emulate',18,c,'middle')+text(507,297,'Sample',18,c,'middle')
save('fbnn','Scalable Bayesian learning','uncertainty',body,'Calibration → emulation → sampling')


def graph(cx,cy,scale=1,color='#256b68'):
    nodes=[(-55,-30),(-15,-62),(44,-36),(53,30),(0,54),(-51,26),(2,-2)]
    body=''
    for i,j in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,6),(1,6),(2,6),(3,6),(4,6),(5,6)]:
        a,b=nodes[i],nodes[j];body+=line(cx+a[0]*scale,cy+a[1]*scale,cx+b[0]*scale,cy+b[1]*scale,'#92b7b5')
    for i,(x,y) in enumerate(nodes):body+=circle(cx+x*scale,cy+y*scale,7*scale,color if i!=6 else '#b68d45')
    return body
c=COLORS['science']
body=graph(116,182,.95)+graph(320,182,1.25)+graph(524,182,.95)
body+=arrow(188,182,222,182,c)+arrow(418,182,452,182,c)
body+=text(116,278,'Biological data',17,c,'middle')+text(320,294,'Shared structure',17,c,'middle')+text(524,278,'Interpretation',17,c,'middle')
save('science','Connecting data to discovery','science',body,'Graph representations for health and science')
save('mgmt','Heterogeneous graph alignment','science',body,'Align graphs through a shared representation')
body=''
for i in range(3):
    y=114+i*50
    body+=f'<path d="M40 {y}h25l8 -20 8 39 8 -29 8 10h20l7 -29 8 46 8 -17h25" stroke="#61948e" stroke-width="2" fill="none"/>'
body+=arrow(184,180,227,180,c)+graph(321,180,1.1)+arrow(410,180,453,180,c)
body+=box(467,138,132,84,'Decode',c, '#eaf3f1',20)
body+=text(107,283,'Neural activity',18,c,'middle')+text(321,283,'Align',18,c,'middle')+text(532,283,'Interpret',18,c,'middle')
save('crossgraph','Interpretable neural decoding','science',body,'Relating neural recordings across subjects')

c=COLORS['agents']
body=box(35,141,134,66,'Plan',c)+arrow(172,174,217,174,c)+box(222,141,164,66,'Execute',c)+arrow(390,174,434,174,c)+box(440,141,165,66,'Evaluate',c)
body+=f'<path d="M522 211V260H104V211" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="6 6"/>'
body+=text(319,292,'Feedback + human oversight',18,c,'middle')
body+=text(320,98,'Reliable agent workflows',21,c,'middle')
save('agents','LLM agents in real workflows','agents',body,'Structured planning, execution, and evaluation')
body=box(32,130,154,80,'Typed plan',c)+arrow(190,170,231,170,c)+box(237,130,171,80,'Policy checks',c)+arrow(411,170,451,170,c)+box(457,130,150,80,'Execution',c)
body+=f'<path d="M533 216V267H112V216" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="6 6"/>'+text(320,294,'Bounded repair · traceable decisions',18,c,'middle')
save('polaris','Governed agent execution','agents',body,'From a typed plan to a verifiable workflow')
body=box(40,120,152,110,'Workflow',c)+arrow(196,175,240,175,c)
body+='<rect x="248" y="88" width="187" height="185" rx="9" fill="white" stroke="#8c602e" stroke-width="1.5"/>'
body+=text(342,121,'Evaluation rubric',19,c,'middle')
for y,label in [(160,'Correctness'),(199,'Policy checks'),(238,'Human review')]:
    body+=f'<path d="M269 {y-8}l6 6 10 -14" fill="none" stroke="{c}" stroke-width="2"/>'+text(296,y,label,16,c)
body+=arrow(439,175,475,175,c)+box(481,120,122,110,'Audit trail',c,size=17)
save('aema','Verifiable agent evaluation','agents',body,'Reproducible evaluation with human oversight')
body=box(40,129,150,91,'Genetics','#256b68')
body+=arrow(194,175,241,175,'#256b68')+box(248,129,150,91,'Analysis','#256b68')+arrow(402,175,449,175,'#256b68')+box(456,129,150,91,'Recovery','#256b68')
save('strong','Genetics and stroke recovery','science',body,'Statistical analysis of clinical outcomes')
body='<rect x="42" y="107" width="157" height="141" rx="7" fill="#e3e9ec"/>'
for i in range(5):body+=f'<path d="M50 {128+i*20}Q120 {150+i*14}190 {125+i*18}" fill="none" stroke="#7e979e" stroke-width="3"/>'
body+=arrow(206,177,249,177,'#256b68')+box(256,132,157,90,'Embedding','#256b68')+arrow(417,177,453,177,'#256b68')
for i,(x,y) in enumerate([(491,125),(512,139),(486,152),(550,203),(573,218),(544,228)]):body+=circle(x,y,9,'#256b68' if i<3 else '#ab7754')
save('oct','Learning from limited images','science',body,'Metric learning for retinal classification')
print('Created 11 original conceptual SVG illustrations.')
