# SIDI at Wellesley College

Website for the Student Interdisciplinary Data Initiative, with About, People, Past events, and Resources pages.

**Website:** https://wellesley-sidi.github.io/

## Update the site

Edit `content.json` to update the E-Board, past events, or resource links. Profiles show only each person's name, class year, and major. The page templates and About copy are in `build.py`.

Photos, logos, fonts, styles, and JavaScript are in `static/`. The original source photos and logos remain in the club's Google Drive. Font licenses are included beside the self-hosted font files in `static/assets/`.

Every push to `main` builds the site and publishes it to GitHub Pages through the workflow in `.github/workflows/pages.yml`. Check the repository's Actions tab for deployment progress. The generated `dist/` directory is not committed.

## Preview locally

Python 3 is the only build requirement; no packages need to be installed.

```sh
BASE_PATH='' SITE_URL=http://localhost:4173 python3 build.py
python3 -m http.server 4173 --directory dist
```

Open http://localhost:4173. Run `python3 build.py` again to generate the production site at `/`.

`BASE_PATH` controls the URL prefix, and `SITE_URL` controls canonical and social image URLs. Update these values in the publishing workflow if the site moves to a different repository or a custom domain.
