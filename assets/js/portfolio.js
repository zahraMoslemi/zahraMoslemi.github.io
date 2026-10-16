document.documentElement.classList.add('js');
const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');
if (menu && nav) {
  menu.addEventListener('click', () => {
    const expanded = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(expanded));
    nav.classList.toggle('open', expanded);
  });
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    nav.classList.remove('open'); menu.setAttribute('aria-expanded', 'false');
  }));
}
const filters = [...document.querySelectorAll('[data-filter]')];
const papers = [...document.querySelectorAll('[data-topics]')];
const count = document.querySelector('#result-count');
function filterPapers(topic) {
  let visible = 0;
  papers.forEach(paper => {
    paper.hidden = topic !== 'all' && !paper.dataset.topics.split(' ').includes(topic);
    if (!paper.hidden) visible++;
  });
  filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === topic)));
  if (count) count.textContent = `${visible} ${visible === 1 ? 'paper' : 'papers'}`;
}
filters.forEach(button => button.addEventListener('click', () => filterPapers(button.dataset.filter)));
if (filters.length) {
  const initial = new URLSearchParams(location.search).get('topic');
  filterPapers(filters.some(button => button.dataset.filter === initial) ? initial : 'all');
}

const lightbox = document.querySelector('#lightbox');
const figureData = document.querySelector('#figure-data');
if (lightbox && figureData && typeof lightbox.showModal === 'function') {
  const data = JSON.parse(figureData.textContent);
  const image = lightbox.querySelector('#lightbox-image');
  const title = lightbox.querySelector('#lightbox-title');
  const counter = lightbox.querySelector('#lightbox-counter');
  const text = lightbox.querySelector('#lightbox-text');
  const link = lightbox.querySelector('#lightbox-link');
  const navs = [...lightbox.querySelectorAll('.lightbox-nav')];
  let current = { id: null, index: 0 };
  function show(id, index) {
    const entry = data[id];
    if (!entry) return;
    const n = entry.figures.length;
    index = ((index % n) + n) % n;
    const figure = entry.figures[index];
    image.src = figure.src; image.width = figure.w; image.height = figure.h; image.alt = figure.alt;
    title.textContent = entry.short;
    counter.textContent = `Figure ${index + 1} of ${n}`;
    text.textContent = figure.caption;
    link.href = entry.url;
    navs.forEach(button => { button.hidden = n < 2; });
    current = { id, index };
    if (!lightbox.open) lightbox.showModal();
    const next = entry.figures[(index + 1) % n];
    if (next && next.src !== figure.src) { const pre = new Image(); pre.src = next.src; }
  }
  document.querySelectorAll('.figure-open').forEach(trigger => trigger.addEventListener('click', event => {
    event.preventDefault();
    show(trigger.dataset.paper, Number(trigger.dataset.index || 0));
  }));
  navs.forEach(button => button.addEventListener('click', () => show(current.id, current.index + Number(button.dataset.step))));
  lightbox.querySelector('[data-close]').addEventListener('click', () => lightbox.close());
  lightbox.addEventListener('click', event => { if (event.target === lightbox) lightbox.close(); });
  lightbox.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight') show(current.id, current.index + 1);
    if (event.key === 'ArrowLeft') show(current.id, current.index - 1);
  });
  lightbox.addEventListener('close', () => image.removeAttribute('src'));
}
