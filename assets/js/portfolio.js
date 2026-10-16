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
