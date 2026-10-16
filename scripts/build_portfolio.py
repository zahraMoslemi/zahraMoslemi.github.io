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
CV = '/files/Zahra_Moslemi_CV.pdf'
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

def paper_html(p, compact=False):
    level = 'h3' if compact else 'h2'
    authors = escape(p['authors']).replace('Zahra Moslemi', '<strong>Zahra Moslemi</strong>')
    return f'''<article class="paper" id="{p['id']}" data-topics="{p['topics']}">
      <div class="paper-meta"><strong>{p['year']}</strong><span>{p['type']}</span></div>
      <div><{level}><a href="{p['url']}">{escape(p['title'])}</a></{level}>
      {'' if compact else f'<p class="authors">{authors}</p>'}
      <p class="venue">{escape(p['venue'])}</p>
      <p class="summary">{escape(p['summary'])}</p>
      <div class="paper-links"><a href="{p['url']}">Read paper <span aria-hidden="true">↗</span></a>
      {f'<a href="{p["pdf"]}">PDF <span aria-hidden="true">↗</span></a>' if p['pdf'] else ''}</div></div></article>'''

def shell(title, path, body):
    desc='Zahra Moslemi, Statistics PhD candidate at UC Irvine. Research in Bayesian machine learning, uncertainty quantification, biomedical AI, and reliable LLM agents.'
    nav=''.join(f'<a href="{href}"'+(' aria-current="page"' if path==href else '')+f'>{label}</a>' for label,href in [('Research','/#research'),('Publications','/publications/'),('Experience','/#experience')])
    structured={'@context':'https://schema.org','@type':'Person','name':'Zahra Moslemi','url':SITE,'image':SITE+'/images/profile.jpg','jobTitle':'PhD candidate in Statistics','affiliation':{'@type':'CollegeOrUniversity','name':'University of California, Irvine'},'email':'mailto:zmoslemi@uci.edu','sameAs':[SCHOLAR,'https://github.com/zahraMoslemi','https://www.linkedin.com/in/zahra-moslemi/']}
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | Zahra Moslemi</title><meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}"><meta name="theme-color" content="#172f34">
<meta property="og:type" content="website"><meta property="og:title" content="{escape(title)} | Zahra Moslemi">
<meta property="og:description" content="{desc}"><meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}/images/profile.jpg">
<meta name="twitter:card" content="summary"><link rel="icon" href="/images/zm-monogram.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/portfolio.css"><script src="/assets/js/portfolio.js" defer></script>
<script type="application/ld+json">{json.dumps(structured)}</script></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap header-inner"><a class="brand" href="/" aria-label="Zahra Moslemi, home"><span aria-hidden="true">Z</span>Zahra Moslemi</a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-navigation">Menu</button>
<nav class="nav" id="main-navigation" aria-label="Main navigation">{nav}<a class="nav-cv" href="/cv/">CV <span aria-hidden="true">↗</span></a></nav></div></header>
<main id="main" class="wrap">{body}</main>
<footer class="site-footer"><div class="wrap footer-inner"><span>© 2026 Zahra Moslemi · Updated October 2026</span><div class="social-links"><a href="mailto:zmoslemi@uci.edu">Email</a><a href="{SCHOLAR}">Scholar</a><a href="https://github.com/zahraMoslemi">GitHub</a><a href="https://www.linkedin.com/in/zahra-moslemi/">LinkedIn</a></div></div></footer></body></html>'''

home='''<section class="hero" aria-labelledby="intro-title"><div>
<p class="eyebrow">Statistics PhD candidate · UC Irvine</p>
<h1 id="intro-title">Zahra Moslemi</h1>
<p class="lead">Reliable machine learning.<br>Grounded in statistical thinking.</p>
<p class="bio">I develop methods for learning and decision-making under uncertainty, with applications in biomedical AI and agentic systems. At UC Irvine, I work with <a href="https://www.ics.uci.edu/~babaks/">Prof. Babak Shahbaba</a> on Bayesian inference, graph representation learning, and model reliability.</p>
<div class="actions"><a class="button primary" href="/publications/">Explore my research <span aria-hidden="true">↗</span></a><a class="button" href="/files/Zahra_Moslemi_CV.pdf">Download CV <span aria-hidden="true">↓</span></a></div></div>
<figure class="portrait"><img src="/images/profile.jpg" width="288" height="335" alt="Zahra Moslemi" fetchpriority="high"><figcaption>UNIVERSITY OF CALIFORNIA, IRVINE<br>Department of Statistics</figcaption></figure></section>
<div class="availability"><span><i class="status-dot" aria-hidden="true"></i><strong>Open to research and applied science opportunities</strong></span><span>Expected PhD: January 2027 · Open to U.S. locations</span></div>

<section class="section" id="research"><div class="section-heading"><div><p class="eyebrow">Research directions</p><h2>From uncertainty to useful AI.</h2></div></div>
<div class="research-grid">
<article class="research-area"><span class="research-number">01</span><h3>Bayesian ML &amp; uncertainty</h3><p>Efficient posterior inference and calibrated predictions: understanding what a model knows, where it is uncertain, and how to use that uncertainty.</p><p class="tag-line">Bayesian neural networks · Conformal prediction · MCMC</p><a class="text-link" href="/publications/?topic=uncertainty">Related papers ↗</a></article>
<article class="research-area"><span class="research-number">02</span><h3>AI for health &amp; science</h3><p>Learning from sparse, heterogeneous biological data through graph models, transformers, and generative methods, with an emphasis on interpretable predictions.</p><p class="tag-line">Biomedical AI · Graph learning · Representation learning</p><a class="text-link" href="/publications/?topic=science">Related papers ↗</a></article>
<article class="research-area"><span class="research-number">03</span><h3>LLM agents &amp; evaluation</h3><p>Planning and evaluation for agentic systems that operate in real workflows, with reproducible tests, verifiable execution, and human oversight.</p><p class="tag-line">Multi-agent systems · DSPy · Reliable evaluation</p><a class="text-link" href="/publications/?topic=agents">Related papers ↗</a></article></div>
<div class="current-work"><strong>Current collaboration with Google Research.</strong> I work on time-series foundation models and uncertainty-aware model selection for sparse longitudinal data, including evaluation under missingness and distribution shift.</div></section>

<section class="section" id="selected-work"><div class="section-heading"><div><p class="eyebrow">Selected work</p><h2>Research in focus.</h2></div><a class="text-link" href="/publications/">All publications &amp; preprints ↗</a></div>
<article class="feature"><div><p class="eyebrow">New preprint · October 2026</p><h3>SCOPE Before You Sample</h3><p class="subtitle">Conformal scores guide posterior exploration for fast, calibrated Bayesian prediction.</p><p>We use the geometry of prediction scores to focus posterior computation on the directions that matter for predictive coverage.</p><p><span class="label">Under review at AISTATS 2027</span></p><a class="text-link" href="https://arxiv.org/abs/2610.17146">Read the preprint ↗</a></div><div class="feature-side"><div class="metric">12–15×</div><p>faster than full HMC on the paper’s real-data benchmarks.</p><p class="note">Reported in SCOPE, arXiv:2610.17146.</p></div></article>
<div class="paper-list">'''+''.join(paper_html(next(p for p in papers if p['id']==i),True) for i in ['fbnn','crossgraph','polaris'])+'''</div></section>

<section class="section" id="experience"><div class="section-heading"><div><p class="eyebrow">Industry experience</p><h2>Research that meets real data.</h2></div></div>
<div class="experience-list">
<article class="experience-row"><div class="experience-date">Summer 2026 · San Mateo</div><div><h3>ClearNote Health</h3><p class="role">Research Scientist Intern</p><p>Developed a biology-informed vision transformer for pancreatic-cancer cfDNA fragmentomics using joint-embedding prediction. Worked on conformal and Bayesian methods for uncertainty-aware biomedical prediction.</p></div></article>
<article class="experience-row"><div class="experience-date">Summer 2025 · Boston</div><div><h3>Accenture · Center for Advanced AI</h3><p class="role">Research Scientist Intern · T-Mobile collaboration</p><p>Built multi-agent planning and evaluation workflows with AutoGen and DSPy, and integrated human review through Azure AI Foundry. This work contributed to POLARIS and AEMA, presented at AAAI 2026 workshops.</p></div></article>
<article class="experience-row"><div class="experience-date">Summer 2024 · San Mateo</div><div><h3>ClearNote Health</h3><p class="role">Research Scientist Intern</p><p>Combined diffusion-based synthetic data with Perceiver IO for biomedical learning under class imbalance and data scarcity. Developed reproducible experiments and evaluated calibration and robustness under distribution shift.</p></div></article></div>
<div class="skills" aria-label="Selected technical skills"><span>Python</span><span>PyTorch</span><span>SQL</span><span>Hugging Face</span><span>DSPy</span><span>AutoGen</span><span>Azure AI Foundry</span><span>Nextflow</span></div></section>

<section class="section two-col" id="background"><div><div class="section-heading"><div><p class="eyebrow">Background</p><h2>Education.</h2></div></div>
<div class="education-item"><h3>PhD in Statistics</h3><p>University of California, Irvine</p><p class="dates">2023–present · Expected January 2027</p><p>Research focus: machine learning and Bayesian inference</p></div>
<div class="education-item"><h3>MS in Statistics</h3><p>University of California, Irvine</p><p class="dates">2021–2023</p></div>
<div class="education-item"><h3>BS in Industrial Engineering</h3><p>Sharif University of Technology</p><p class="dates">2016–2020 · Ranked 4th of 200</p></div></div>
<div><div class="section-heading"><div><p class="eyebrow">Selected recognition</p><h2>Honors &amp; service.</h2></div></div><ul class="recognition-list">
<li>Best Poster Runner-up<span>NeurIPS 2025 · AI4Science Workshop</span></li>
<li>Best Poster Award<span>NeurIPS 2025 · New Perspectives in Graph Machine Learning Workshop</span></li>
<li>Gold Reviewer<span>ICML 2026</span></li>
<li>Henry Samueli Endowed Fellowship<span>University of California, Irvine · 2024</span></li>
</ul></div></section>
<section class="contact-section" id="contact"><div><p class="eyebrow">Let’s connect</p><h2>Interested in working together?</h2><p>I’m exploring research scientist, applied scientist, research engineering, and postdoctoral opportunities in machine learning, biomedical AI, and AI for science.</p></div><a class="button" href="mailto:zmoslemi@uci.edu">zmoslemi@uci.edu <span aria-hidden="true">↗</span></a></section>'''

pubbody='''<section class="page-intro"><p class="eyebrow">Research output</p><h1>Publications &amp; preprints.</h1><p>My work spans statistical machine learning, biomedical applications, and reliable agentic systems. Publication and review status are listed with each paper.</p><a class="text-link" href="'''+SCHOLAR+'''">Google Scholar ↗</a></section>
<section class="publications-page" aria-label="Research papers"><div class="filters" aria-label="Filter papers by topic"><button data-filter="all" aria-pressed="true">All papers</button><button data-filter="uncertainty" aria-pressed="false">Bayesian ML &amp; uncertainty</button><button data-filter="science" aria-pressed="false">Health &amp; science</button><button data-filter="agents" aria-pressed="false">LLM agents</button></div><p class="result-count" id="result-count" role="status" aria-live="polite">8 papers</p>'''+''.join(paper_html(p) for p in papers)+'''</section>'''

cvbody='''<section class="page-intro"><p class="eyebrow">Curriculum vitae</p><h1>Research &amp; experience.</h1><p>My CV brings together my research, publications, education, and industry experience. Updated October 2026, including the SCOPE preprint.</p></section>
<section class="cv-summary"><a class="button primary" href="/files/Zahra_Moslemi_CV.pdf">Download CV <span aria-hidden="true">↓</span></a>
<dl><dt>Education</dt><dd>PhD candidate in Statistics, UC Irvine. Expected January 2027. MS in Statistics, UC Irvine; BS in Industrial Engineering, Sharif University of Technology.</dd><dt>Research</dt><dd>Bayesian machine learning, uncertainty quantification, biomedical AI, graph representation learning, and LLM agents and evaluation.</dd><dt>Industry</dt><dd>Research Scientist internships at ClearNote Health (2024 and 2026) and Accenture’s Center for Advanced AI (2025).</dd><dt>Opportunities</dt><dd>Research scientist, applied scientist, research engineering, and postdoctoral positions. Open to U.S. locations.</dd><dt>Contact</dt><dd><a href="mailto:zmoslemi@uci.edu">zmoslemi@uci.edu</a></dd></dl></section>'''

pages=[('_pages/about.md','/','Research & Applied Machine Learning',home),('_pages/publications.html','/publications/','Publications',pubbody),('_pages/cv.md','/cv/','Curriculum Vitae',cvbody)]
PREVIEW.mkdir(exist_ok=True)
for filename,path,title,body in pages:
    html="\n".join(line.rstrip() for line in shell(title,path,body).splitlines())+"\n"
    extra='redirect_from:\n  - /about/\n  - /about.html\n' if path=='/' else ''
    (ROOT/filename).write_text(f'---\nlayout: null\ntitle: "{title}"\npermalink: {path}\n{extra}---\n'+html)
    target=PREVIEW/path.strip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html)
for filename in ['assets/css/portfolio.css','assets/js/portfolio.js','images/profile.jpg','images/zm-monogram.svg','files/Zahra_Moslemi_CV.pdf']:
    source=ROOT/filename
    if source.exists():
        target=PREVIEW/filename;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(source.read_bytes())
(ROOT/'_data/portfolio_publications.json').write_text(json.dumps(papers,ensure_ascii=False,indent=2)+'\n')
print(f'Generated 3 portfolio pages; preview: {PREVIEW}')
