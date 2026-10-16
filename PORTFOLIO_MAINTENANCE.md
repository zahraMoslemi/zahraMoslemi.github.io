# Zahra Moslemi's research portfolio

The homepage, publications, and CV pages have a custom responsive design. Existing
GitHub Pages/Jekyll deployment is retained. Generated HTML is checked in so no new
build service, JavaScript framework, or package installation is required.

## Updating the site

1. Edit the publication records or page copy in `scripts/build_portfolio.py`.
2. Replace `files/Zahra_Moslemi_CV.pdf` with the latest general research CV.
3. Run `python3 scripts/build_portfolio.py`.
4. Preview with `python3 -m http.server 8765 --bind 127.0.0.1 --directory _portfolio_preview`.
5. Review changes before publishing through the existing GitHub Pages branch.

The preview contains the exact HTML bodies, CSS, JavaScript, image, and CV used by
the three pages. Jekyll front matter supplies their public routes. The preview
directory and maintenance scripts are excluded from the public build.

The legacy AcademicPages sample posts, publications, talks, teaching entries,
and demonstration pages are excluded in `_config.yml`; their sources are retained.

## Content notes (October 16, 2026)

- SCOPE: arXiv:2610.17146, first author; AISTATS 2027 review status provided by Zahra.
  It is labeled a preprint under review, never an accepted AISTATS paper.
- Expected PhD graduation: January 2027.
- POLARIS and AEMA: titles, authors, and workshop venues match arXiv records
  2601.11816 and 2601.11903.
- TMLR: full author list and OpenReview link corrected to cD209Ug0X7 (zero).
- MGMT extended preprint: arXiv:2601.22593. Workshop and extended versions are
  explicitly identified.
- Internship descriptions and honors use Zahra's supplied CVs.
- Work authorization, home address, date of birth, and application answers are
  not included in website content.

## Checks

Desktop (1280px) and mobile (390px) visual inspection; mobile menu; topic filters;
image loading; no horizontal overflow; local routes/assets and PDF reference checks.
The full legacy Jekyll dependency build is not installed in this workspace.
