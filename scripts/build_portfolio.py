"""Generate the portfolio's static Jekyll pages and an identical local preview.

Edit the copy below, then run: python3 scripts/build_portfolio.py
No third-party Python packages are required. The existing GitHub Pages/Jekyll
deployment serves the generated pages; it does not need to run this script.
"""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / '_portfolio_preview'
SITE = 'https://zahramoslemi.github.io'
SCHOLAR = 'https://scholar.google.com/citations?user=jbJTkg4AAAAJ&hl=en'

papers = [
dict(id='scope', year='2026', type='Preprint', topics='uncertainty',
 title='SCOPE Before You Sample: Conformal Scores Guide Posterior Exploration for Fast and Calibrated Bayesian Predictive Inference',
 authors='Zahra Moslemi, Ziyi Liang, Babak Shahbaba',
 venue='arXiv preprint · Under review at AISTATS 2027',
 summary='Conformal scores identify the posterior directions that matter for predictive regions, combining targeted MCMC with a variational approximation and calibrated coverage.',
 url='https://arxiv.org/abs/2610.17146', pdf='https://arxiv.org/pdf/2610.17146'),
dict(id='mgmt', year='2026', type='Preprint', topics='science',
 title='Heterogeneous Graph Alignment for Joint Reasoning and Interpretability',
 authors='Zahra Moslemi, Ziyi Liang, Norbert Fortin, Babak Shahbaba',
 venue='arXiv preprint · Multi-Graph Meta-Transformer (MGMT)',
 summary='A shared meta-graph aligns attention-selected supernodes across heterogeneous graphs, supporting joint prediction and interpretable scientific analysis. Related MGMT work was presented at the NeurIPS 2025 NPGML Workshop (Spotlight).',
 url='https://arxiv.org/abs/2601.22593', pdf='https://arxiv.org/pdf/2601.22593'),
dict(id='polaris', year='2026', type='Workshop', topics='agents',
 title='POLARIS: Typed Planning and Governed Execution for Agentic AI in Back-Office Automation',
 authors='Zahra Moslemi, Keerthi Koneru, Yen-Ting Lee, Sheethal Kumar, Ramesh Radhakrishnan',
 venue='AAAI 2026 · Workshop on Agentic AI Benchmarks and Applications for Enterprise Tasks',
 summary='Typed plan synthesis and validated execution bring policy checks, bounded repair, and traceable decision-making to enterprise agent workflows.',
 url='https://arxiv.org/abs/2601.11816', pdf='https://arxiv.org/pdf/2601.11816'),
dict(id='aema', year='2026', type='Workshop', topics='agents',
 title='AEMA: Verifiable Evaluation Framework for Trustworthy and Controlled Agentic LLM Systems',
 authors='Yen-Ting Lee, Keerthi Koneru, Zahra Moslemi, Sheethal Kumar, Ramesh Radhakrishnan',
 venue='AAAI 2026 · Workshop on Trust and Control in Agentic AI',
 summary='An auditable framework for planning, running, and aggregating evaluations of multi-agent workflows, with human oversight and reproducible evaluation records.',
 url='https://arxiv.org/abs/2601.11903', pdf='https://arxiv.org/pdf/2601.11903'),
dict(id='crossgraph', year='2025', type='Workshop', topics='science',
 title='Multi-Graph Meta-Transformer: An Interpretable Framework for Cross-Graph Functional Alignment in Neural Decoding',
 authors='Zahra Moslemi, Ziyi Liang, Norbert J. Fortin, Babak Shahbaba',
 venue='NeurIPS 2025 · AI4Science Workshop · Spotlight · Best Poster Runner-up',
 summary='Functional alignment across heterogeneous neural recordings connects task-relevant structures across subjects while preserving interpretable graph representations.',
 url='https://openreview.net/forum?id=CBcubwXMhA', pdf='https://openreview.net/pdf/b80baee1e96105401fdc5397af5723ebdb7054a1.pdf'),
dict(id='fbnn', year='2024', type='Journal', topics='uncertainty',
 title='Scaling Up Bayesian Neural Networks with Neural Networks',
 authors='Zahra Moslemi, Yang Meng, Shiwei Lan, Babak Shahbaba',
 venue='Transactions on Machine Learning Research (TMLR)',
 summary='A calibration–emulation–sampling strategy accelerates Bayesian neural network inference while retaining predictive accuracy and uncertainty estimation.',
 url='https://openreview.net/forum?id=cD209Ug0X7', pdf='https://arxiv.org/pdf/2312.11799'),
dict(id='strong', year='2024', type='Journal', topics='science',
 title='Genetic Variation and Stroke Recovery: The STRONG Study',
 authors='Steven C. Cramer, Livia Parodi, Zahra Moslemi, Robynne G. Braun, Chad M. Aldridge, Babak Shahbaba, Jonathan Rosand, E. Alison Holman; STRONG Study Investigators',
 venue='Stroke · 55(8):2094–2102',
 summary='A prospective study across 28 U.S. stroke centers investigating associations between genetic variation and recovery outcomes.',
 url='https://doi.org/10.1161/STROKEAHA.124.047643', pdf=''),
dict(id='oct', year='2024', type='Journal', topics='science',
 title='Deep learning-based retinal abnormality detection from OCT images with limited data',
 authors='Mohammad Talebzadeh, Abolfazl Sodagartojgi, Zahra Moslemi, Sara Sedighi, Behzad Kazemi, Faezeh Akbari',
 venue='World Journal of Advanced Research and Reviews · 21(3):690–698',
 summary='Metric learning for retinal disease classification when labeled medical imaging data are limited.',
 url='https://doi.org/10.30574/wjarr.2024.21.3.0716', pdf='https://wjarr.com/sites/default/files/fulltext_pdf/WJARR-2024-0716.pdf')
]

# Figures from the papers, prepared from the arXiv/OpenReview sources and the
# TMLR submission source (provenance in PORTFOLIO_MAINTENANCE.md). The first
# figure of each paper is its card image; every figure opens in the lightbox.
# Card images are 16:9 crops named <file>-card.<ext>; full figures keep their aspect.
FIGURES = {
 'scope': [
  dict(file='scope-figure', ext='svg', w=1700, h=900,
       alt='Three-stage diagram of SCOPE: score-guided directions, slice sampling with variational completion, conformal calibration',
       lead='How SCOPE guides, samples and calibrates',
       caption='SCOPE in three stages. (1) Score gradients on a held-out guide set, weighted toward the target coverage level, identify the few parameter directions that move the prediction-region boundary; these are generally not the directions of largest posterior variance. (2) Slice MCMC explores only that r-dimensional subspace while a projected variational approximation carries the remaining directions, giving a completed predictive distribution at a fraction of the cost of full MCMC. (3) The same guide set selects the better anchor and sets the region’s density level through a conformal quantile; SCOPE/Split uses an independent calibration set for finite-sample validity.'),
 ],
 'mgmt': [
  dict(file='mgmt-architecture', ext='png', w=2000, h=1036,
       alt='MGMT architecture diagram: encode sources, select nodes, wire sources, predict',
       lead='MGMT architecture: encode, select, wire, predict',
       caption='MGMT architecture. Source-specific graph-attention encoders combine four depths and retain selected nodes together with their induced edges. A parameter-free wiring step compares nodes through reference signatures and links similar nodes across sources into one meta-graph. Two meta-graph attention layers with mean pooling produce a single collection-level prediction. Brackets mark the two fitted stages and the construction step between them.'),
  dict(file='mgmt-layers', ext='png', w=1753, h=472,
       alt='Four hippocampal connectivity graphs with per-layer attention and confidence scores',
       lead='Layer-wise attention on one subject’s LFP graph',
       caption='Layer-wise attention patterns for the LFP data of one subject (SuperChris). Each panel shows the same connectivity graph with the learned depth-confidence score Γ of that layer, the edge-level attention scores, and node-wise summed attention weights; warmer colours indicate higher attention.'),
  dict(file='mgmt-wiring', ext='png', w=1800, h=910,
       alt='Forest plot of accuracy differences between cosine wiring and two control wirings',
       lead='Controlled wiring study against matched controls',
       caption='Controlled wiring study. Mean accuracy difference between cosine wiring and two matched controls, count-matched random wiring and degree-preserving rewiring, with pointwise 95% paired-bootstrap intervals. Source representations and edge budgets are frozen and only the final predictor is retrained. Starred tasks pass Holm correction across the 14-test family.'),
 ],
 'polaris': [
  dict(file='polaris-figure', ext='svg', w=1700, h=900,
       alt='Four-stage diagram of POLARIS: normalize input, typed plan selection, governed DAG execution with repair loop and guardrails, reconciled outputs',
       lead='Typed planning and governed execution',
       caption='POLARIS treats back-office automation as typed plan synthesis and validated execution. Inputs are normalised into one typed record; a planner proposes several type-checked DAGs and a rubric-guided reasoning agent selects a single compliant plan; execution runs a document parser and data validator inside a bounded repair loop, invokes only the processors the plan requires, and applies compiled policy guardrails that block or route side effects before they occur; reconciliation returns a decision with its rationale, a structured report and a full execution trace.'),
 ],
 'aema': [
  dict(file='aema-figure', ext='svg', w=1700, h=900,
       alt='Diagram of AEMA: human request, planning agent, prompt-refinement agent, evaluation agents scoring each workflow step, final report agent, oversight loop',
       lead='Process-aware, auditable evaluation',
       caption='AEMA evaluates agentic workflows as a process rather than a single response. From a human evaluator’s business context and specification, a planning agent builds an executable evaluation plan, a prompt-refinement agent prepares exemplars and settings for each step, evaluation agents score every intermediate action of the workflow under test with feedback and evidence, and a final report agent aggregates everything into an auditable, reproducible report. Human oversight closes the loop, and final scores vary far less across repeated runs than with a single LLM-as-a-judge.'),
 ],
 'crossgraph': [
  dict(file='crossgraph-figure', ext='svg', w=1700, h=900,
       alt='Three-stage diagram: graphs from five rats’ CA1 recordings, attention-based node selection, meta-graph alignment and odor decoding',
       lead='From five animals’ recordings to one decoded odor',
       caption='Cross-graph functional alignment for neural decoding. Local field potentials from hippocampal CA1 of five rats, recorded during an odor-sequence memory task, become one functional-connectivity graph per animal with different electrode sets. A depth-aware graph transformer scores and keeps the informative electrodes of each animal with their induced edges; similarity links join the selected nodes across animals into a meta-graph that a shared transformer decodes into the odor label. Selection frequencies over fitted models show which electrodes matter, with distal CA1 recurring across animals.'),
 ],
 'fbnn': [
  dict(file='fbnn-figure', ext='svg', w=1700, h=900,
       alt='Three-stage diagram of FBNN: calibration run, neural-network emulator of the log-posterior, pCN sampling with the emulator',
       lead='Calibration, emulation, sampling',
       caption='The calibration–emulation–sampling strategy behind FBNN. A short SGHMC run collects a few hundred weight samples with their log-posterior values; a neural-network emulator is trained on these pairs to approximate the map from weights to log-posterior; the dimension-robust pCN sampler then draws posterior samples using the emulator instead of a full pass over the data, keeping the predictive accuracy and uncertainty of the full BNN at much lower cost.'),
 ],
 'strong': [
  dict(file='strong-figure', ext='svg', w=1700, h=900,
       alt='Three-stage diagram of the STRONG study: enrollment and follow-up timeline, candidate variants and outcomes, association findings',
       lead='A one-year multicenter genetic study of recovery',
       caption='Design of the STRONG study. Adults with stroke were enrolled at 28 U.S. stroke centers (763 enrollees) and followed at 3, 6 and 12 months. Candidate variants were tested for association with motor and functional recovery (ApoE ε4, BDNF, a dopamine polygenic score) and with stress-related outcomes (seven variants, examined against post-stroke stress), using regression models adjusted for stroke severity, age, sex and ancestry with Holm–Bonferroni correction. BDNF rs6265 was associated with poorer 12-month cognition; ACE, FAAH and COMT variants modified how post-stroke stress related to depression and PTSD; and the GISCOME rs1842681 association with 3-month mRS replicated.'),
 ],
 'oct': [
  dict(file='oct-figure', ext='svg', w=1700, h=900,
       alt='Three-stage diagram: few labeled OCT scans, deep triplet network with shared encoder and embedding space, nearest-class detection',
       lead='Metric learning for OCT with few labels',
       caption='Retinal abnormality detection from few labeled OCT scans. Instead of training a classifier directly on scarce images, a deep triplet network with a shared VGG16-based encoder learns an embedding in which scans of the same class (normal, drusen, CNV, DME) are pulled together and other classes pushed apart, using a conditional triplet loss adapted to small samples; a query scan is then labelled by its nearest class in the embedding space. The approach reaches 92.81% accuracy, above published DenseNet, ResNet and Inception baselines.'),
 ],
}
SHORT_TITLES = {'scope': 'SCOPE', 'fbnn': 'Scaling Up Bayesian Neural Networks (TMLR)', 'mgmt': 'MGMT · Heterogeneous Graph Alignment', 'crossgraph': 'MGMT · Cross-Graph Functional Alignment', 'polaris': 'POLARIS', 'aema': 'AEMA', 'strong': 'The STRONG Study', 'oct': 'Retinal OCT with limited data'}
THEME_IMAGES = {'uncertainty': 'theme-uncertainty.svg', 'science': 'theme-science.svg', 'agents': 'theme-agents.svg'}
CARD_W, CARD_H = 900, 506


def figure_visual(p):
    figs = FIGURES.get(p['id'])
    if not figs:
        return f'<a class="paper-visual" href="{p["url"]}" tabindex="-1" aria-hidden="true"><img src="/images/research/{p["id"]}.svg" width="640" height="360" alt="" loading="lazy"></a>'
    first, n = figs[0], len(figs)
    plural = 'figure' if n == 1 else 'figures'
    label = f"View {('the' if n == 1 else n)} {plural} from {SHORT_TITLES[p['id']]}"
    if first['ext'] == 'svg':  # designed figure: show the whole drawing, letterboxed
        img = f'<img class="contain" src="/images/figures/{first["file"]}.svg" width="{first["w"]}" height="{first["h"]}" alt="{escape(first["alt"])}" loading="lazy">'
    else:
        img = f'<img src="/images/figures/{first["file"]}-card.{first["ext"]}" width="{CARD_W}" height="{CARD_H}" alt="{escape(first["alt"])}" loading="lazy">'
    count = 'View figure' if n == 1 else f'{n} figures'
    return f'''<figure class="paper-visual paper-figure"><a class="figure-open" href="/images/figures/{first['file']}.{first['ext']}" data-paper="{p['id']}" data-index="0" aria-label="{escape(label)}">{img}</a>
      <figcaption>{escape(first['lead'])}<span class="figure-count">{count} <span aria-hidden="true">⤢</span></span></figcaption></figure>'''


def figure_link(p):
    figs = FIGURES.get(p['id'])
    if not figs:
        return ''
    n = len(figs)
    label = 'Figure' if n == 1 else f'Figures ({n})'
    return f'''<a class="figure-open" href="/images/figures/{figs[0]['file']}.{figs[0]['ext']}" data-paper="{p['id']}" data-index="0">{label} <span aria-hidden="true">⤢</span></a>'''


def lightbox_html():
    data = {p['id']: dict(title=p['title'], short=SHORT_TITLES[p['id']], url=p['url'],
                          figures=[dict(src=f"/images/figures/{f['file']}.{f['ext']}", w=f['w'], h=f['h'], alt=f['alt'], caption=f['caption']) for f in FIGURES[p['id']]])
            for p in papers if p['id'] in FIGURES}
    payload = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    return f'''<dialog class="lightbox" id="lightbox" aria-labelledby="lightbox-title">
<div class="lightbox-panel"><div class="lightbox-bar"><p class="lightbox-title" id="lightbox-title"></p><button type="button" class="lightbox-close" data-close aria-label="Close figure viewer">✕</button></div>
<div class="lightbox-stage"><button type="button" class="lightbox-nav prev" data-step="-1" aria-label="Previous figure">‹</button><img id="lightbox-image" alt=""><button type="button" class="lightbox-nav next" data-step="1" aria-label="Next figure">›</button></div>
<div class="lightbox-caption"><p class="lightbox-counter" id="lightbox-counter"></p><p id="lightbox-text"></p><a class="text-link" id="lightbox-link" href="#">Open paper <span aria-hidden="true">↗</span></a></div></div></dialog>
<script type="application/json" id="figure-data">{payload}</script>'''



THEMES = [
    dict(id='uncertainty', title='Bayesian ML & uncertainty',
         question='How can models express what they do not know?',
         description='I develop efficient Bayesian inference and conformal methods for predictions whose uncertainty is useful and well calibrated.',
         ids=['scope', 'fbnn']),
    dict(id='science', title='Biomedical AI & AI for science',
         question='How can we learn from complex biological data?',
         description='I study graph representations and interpretable learning across heterogeneous data, with applications in neural decoding and biomedical prediction.',
         ids=['mgmt', 'crossgraph']),
    dict(id='agents', title='LLM agents & evaluation',
         question='How can we make agent workflows more reliable?',
         description='I build structured planning and evaluation methods for agentic systems, bringing together verifiable execution, reproducible tests, and human oversight.',
         ids=['polaris', 'aema'])
]


def paper_html(p, compact=False):
    level = 'h3' if compact else 'h2'
    authors = escape(p['authors']).replace('Zahra Moslemi', '<strong>Zahra Moslemi</strong>')
    return f'''<article class="paper" id="{p['id']}" data-topics="{p['topics']}">
      {figure_visual(p)}
      <div class="paper-content"><p class="paper-meta">{p['year']} <span aria-hidden="true">/</span> {p['type']}</p>
      <{level}><a href="{p['url']}">{escape(p['title'])}</a></{level}>
      <p class="authors">{authors}</p>
      <p class="venue">{escape(p['venue'])}</p>
      <p class="summary">{escape(p['summary'])}</p>
      <div class="paper-links"><a href="{p['url']}">Paper <span aria-hidden="true">↗</span></a>
      {f'<a href="{p["pdf"]}">PDF <span aria-hidden="true">↗</span></a>' if p['pdf'] else ''}
      {figure_link(p)}</div></div></article>'''


def shell(title, path, body):
    desc='Zahra Moslemi, Statistics PhD candidate at UC Irvine. Research in Bayesian machine learning, uncertainty quantification, biomedical AI, and reliable LLM agents.'
    nav=''.join(f'<a href="{href}"'+(' aria-current="page"' if path==href else '')+f'>{label}</a>' for label,href in [('About','/'),('Research','/#research'),('Publications','/publications/'),('Experience','/#experience'),('CV','/cv/')])
    structured={'@context':'https://schema.org','@type':'Person','name':'Zahra Moslemi','url':SITE,'image':SITE+'/images/profile.jpg','jobTitle':'PhD candidate in Statistics','affiliation':{'@type':'CollegeOrUniversity','name':'University of California, Irvine'},'email':'mailto:zmoslemi@uci.edu','sameAs':[SCHOLAR,'https://github.com/zahraMoslemi','https://www.linkedin.com/in/zahra-moslemi/']}
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | Zahra Moslemi</title><meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}"><meta name="theme-color" content="#7b3045">
<meta property="og:type" content="website"><meta property="og:title" content="{escape(title)} | Zahra Moslemi">
<meta property="og:description" content="{desc}"><meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}/images/profile.jpg">
<meta name="twitter:card" content="summary"><link rel="icon" href="/images/zm-monogram.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/portfolio.css"><script src="/assets/js/portfolio.js" defer></script>
<script type="application/ld+json">{json.dumps(structured)}</script></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-inner"><a class="brand" href="/" aria-label="Zahra Moslemi, home">Zahra <span>@ UCI</span></a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-navigation">Menu</button>
<nav class="nav" id="main-navigation" aria-label="Main navigation">{nav}</nav></div></header>
<main id="main"{'' if path=='/' else ' class="wrap"'}>{body}</main>
<footer class="site-footer"><div class="wrap footer-inner"><span>© 2026 Zahra Moslemi <span class="footer-dot">·</span> Updated October 2026</span><div class="social-links"><a href="mailto:zmoslemi@uci.edu">Email</a><a href="{SCHOLAR}">Scholar</a><a href="https://github.com/zahraMoslemi">GitHub</a><a href="https://www.linkedin.com/in/zahra-moslemi/">LinkedIn</a></div></div></footer></body></html>'''


def theme_card(theme, number):
    return f'''<a class="theme-card {theme['id']}" href="#theme-{theme['id']}">
      <img src="/images/figures/{THEME_IMAGES[theme['id']]}" alt="" width="1200" height="675">
      <div class="theme-caption"><span class="theme-index">0{number}</span><h3>{escape(theme['title'])}</h3><span class="theme-arrow" aria-hidden="true">↓</span></div>
      <p>{escape(theme['question'])}</p></a>'''


def theme_section(theme, number):
    selected = [next(p for p in papers if p['id']==paper_id) for paper_id in theme['ids']]
    return f'''<section class="research-theme {theme['id']}" id="theme-{theme['id']}" aria-labelledby="heading-{theme['id']}">
      <div class="theme-heading"><span class="section-number">0{number}</span><div><h2 id="heading-{theme['id']}">{escape(theme['title'])}</h2><p>{escape(theme['description'])}</p></div></div>
      <div class="paper-list">{''.join(paper_html(p,True) for p in selected)}</div>
      <a class="text-link theme-more" href="/publications/?topic={theme['id']}">All papers in this area <span aria-hidden="true">↗</span></a></section>'''


home=f'''<section class="profile-band" aria-labelledby="intro-title"><div class="wrap profile">
<img class="portrait" src="/images/profile.jpg" width="288" height="335" alt="Zahra Moslemi" fetchpriority="high">
<div class="profile-name"><p class="hello">Hello, I’m</p><h1 id="intro-title">Zahra Moslemi</h1><a class="profile-email" href="mailto:zmoslemi@uci.edu">zmoslemi@uci.edu</a><div class="profile-links"><a href="{SCHOLAR}">Scholar</a><a href="https://github.com/zahraMoslemi">GitHub</a><a href="https://www.linkedin.com/in/zahra-moslemi/">LinkedIn</a></div></div>
<div class="affiliation"><p>PhD candidate in Statistics</p><p>University of California, Irvine</p><p class="graduation">Expected January 2027</p></div></div></section>
<div class="wrap home-content"><section class="introduction" aria-label="About me"><p>I work at the intersection of <strong>statistical machine learning, biomedical AI, and reliable agentic systems</strong>. At UC Irvine, I am advised by <a href="https://www.ics.uci.edu/~babaks/">Prof. Babak Shahbaba</a>. My research brings Bayesian inference and uncertainty quantification to problems where data are limited, heterogeneous, or shifting.</p>
<div class="research-statement">I study how to make machine learning <em>more reliable</em>, from scientific data to agent workflows.</div>
<p class="opportunity-note"><span class="note-label">Looking ahead</span> I’m exploring research, applied science, and postdoctoral opportunities for 2027. <a href="mailto:zmoslemi@uci.edu">Get in touch <span aria-hidden="true">↗</span></a></p></section>

<section class="research-overview" id="research" aria-labelledby="research-title"><div class="section-heading"><h2 id="research-title">Research directions</h2><span>Explore a theme to see related work</span></div><div class="theme-grid">{''.join(theme_card(theme,i) for i,theme in enumerate(THEMES,1))}</div></section>

<div class="highlights-heading"><h2>Research highlights</h2><a class="text-link" href="/publications/">All publications &amp; preprints <span aria-hidden="true">↗</span></a></div>
{''.join(theme_section(theme,i) for i,theme in enumerate(THEMES,1))}

<section class="section" id="experience"><div class="section-heading"><h2>Industry experience</h2><span>Research Scientist internships</span></div>
'''

home+='''<div class="experience-list">
<article class="experience-row"><div class="experience-date">Summer 2026 · San Mateo</div><div><h3>ClearNote Health</h3><p class="role">Research Scientist Intern</p><p>Developed a biology-informed vision transformer for pancreatic-cancer cfDNA fragmentomics using joint-embedding prediction. Worked on conformal and Bayesian methods for uncertainty-aware biomedical prediction.</p></div></article>
<article class="experience-row"><div class="experience-date">Summer 2025 · Boston</div><div><h3>Accenture · Center for Advanced AI</h3><p class="role">Research Scientist Intern</p><p>Built multi-agent planning and evaluation workflows with AutoGen and DSPy, and integrated human review through Azure AI Foundry. This work contributed to POLARIS and AEMA, presented at AAAI 2026 workshops.</p></div></article>
<article class="experience-row"><div class="experience-date">Summer 2024 · San Mateo</div><div><h3>ClearNote Health</h3><p class="role">Research Scientist Intern</p><p>Combined diffusion-based synthetic data with Perceiver IO for biomedical learning under class imbalance and data scarcity. Developed reproducible experiments and evaluated calibration and robustness under distribution shift.</p></div></article></div>
<div class="skills" aria-label="Selected technical skills"><span>Python</span><span>PyTorch</span><span>SQL</span><span>Hugging Face</span><span>DSPy</span><span>AutoGen</span><span>Azure AI Foundry</span><span>Nextflow</span></div></section>

<section class="section two-col" id="background"><div><div class="section-heading"><div><h2>Education</h2></div></div>
<div class="education-item"><h3>PhD in Statistics</h3><p>University of California, Irvine</p><p class="dates">2023–present · Expected January 2027</p><p>Research focus: machine learning and Bayesian inference</p></div>
<div class="education-item"><h3>MS in Statistics</h3><p>University of California, Irvine</p><p class="dates">2021–2023</p></div>
<div class="education-item"><h3>BS in Industrial Engineering</h3><p>Sharif University of Technology</p><p class="dates">2016–2020</p></div></div>
<div><div class="section-heading"><div><h2>Honors &amp; service</h2></div></div><ul class="recognition-list">
<li>Best Poster Runner-up<span>NeurIPS 2025 · AI4Science Workshop</span></li>
<li>Best Poster Award<span>NeurIPS 2025 · New Perspectives in Graph Machine Learning Workshop</span></li>
<li>Gold Reviewer<span>ICML 2026</span></li>
<li>Henry Samueli Endowed Fellowship<span>University of California, Irvine · 2024</span></li>
</ul></div></section>
'''
home+='''<section class="contact-section" id="contact"><div><h2>Let’s connect</h2><p>I’m interested in research scientist, applied scientist, research engineering, and postdoctoral opportunities in machine learning, biomedical AI, and AI for science.</p></div><a class="button" href="mailto:zmoslemi@uci.edu">Email me <span aria-hidden="true">↗</span></a></section></div>'''+lightbox_html()

pubbody='''<section class="page-intro"><p class="eyebrow">Research</p><h1>Publications &amp; preprints</h1><p>Statistical machine learning, biomedical AI, and reliable agentic systems. Publication and review status are listed with each paper.</p><a class="text-link" href="'''+SCHOLAR+'''">Google Scholar <span aria-hidden="true">↗</span></a></section>
<section class="publications-page" aria-label="Research papers"><div class="filters" aria-label="Filter papers by topic"><button data-filter="all" aria-pressed="true">All papers</button><button data-filter="uncertainty" aria-pressed="false">Bayesian ML &amp; uncertainty</button><button data-filter="science" aria-pressed="false">Health &amp; science</button><button data-filter="agents" aria-pressed="false">LLM agents</button></div><p class="result-count" id="result-count" role="status" aria-live="polite">8 papers</p>'''+''.join(paper_html(p) for p in papers)+'''</section>'''+lightbox_html()

cvbody='''<section class="page-intro"><p class="eyebrow">Curriculum vitae</p><h1>Research &amp; experience</h1><p>My research, publications, education, and industry experience. Updated October 2026.</p></section>
<section class="cv-summary"><dl><dt>Education</dt><dd>PhD candidate in Statistics, UC Irvine. Expected January 2027. MS in Statistics, UC Irvine; BS in Industrial Engineering, Sharif University of Technology.</dd><dt>Research</dt><dd>Bayesian machine learning, uncertainty quantification, biomedical AI, graph representation learning, and LLM agents and evaluation.</dd><dt>Industry</dt><dd>Research Scientist internships at ClearNote Health (2024 and 2026) and Accenture’s Center for Advanced AI (2025).</dd><dt>Opportunities</dt><dd>Research scientist, applied scientist, research engineering, and postdoctoral positions. Open to U.S. locations.</dd><dt>Contact</dt><dd><a href="mailto:zmoslemi@uci.edu">zmoslemi@uci.edu</a></dd></dl></section>'''

# Keep generated documents as HTML so Jekyll does not run them through Markdown.
pages=[('_pages/about.html','/','Research & Applied Machine Learning',home),('_pages/publications.html','/publications/','Publications',pubbody),('_pages/cv.html','/cv/','Curriculum Vitae',cvbody)]
PREVIEW.mkdir(exist_ok=True)
for filename,path,title,body in pages:
    html="\n".join(line.rstrip() for line in shell(title,path,body).splitlines())+"\n"
    extra='redirect_from:\n  - /about/\n  - /about.html\n' if path=='/' else ''
    (ROOT/filename).write_text(f'---\nlayout: null\ntitle: "{title}"\npermalink: {path}\n{extra}---\n'+html)
    target=PREVIEW/path.strip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html)
assets=['assets/css/portfolio.css','assets/js/portfolio.js','images/profile.jpg','images/zm-monogram.svg']
assets += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'images/research').glob('*.svg'))]
assets += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'images/figures').glob('*')) if p.suffix in ('.png', '.jpg', '.svg')]
for filename in assets:
    source=ROOT/filename
    if source.exists():
        target=PREVIEW/filename;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(source.read_bytes())
(ROOT/'_data/portfolio_publications.json').write_text(json.dumps(papers,ensure_ascii=False,indent=2)+'\n')
print(f'Generated 3 portfolio pages; preview: {PREVIEW}')
