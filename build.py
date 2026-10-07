import json,html,os,re,shutil
from pathlib import Path
from datetime import date
ROOT=Path(__file__).parent
data=json.loads((ROOT/'content.json').read_text())
BASE_PATH='/' + os.environ.get('BASE_PATH','').strip('/')
if BASE_PATH=='/':BASE_PATH=''
SITE_URL=os.environ.get('SITE_URL','https://wellesley-sidi.github.io'+BASE_PATH).rstrip('/')
out=ROOT/'dist'
shutil.copytree(ROOT/'static',out,dirs_exist_ok=True)
e=html.escape
arrow='<span class="arrow" aria-hidden="true">↗</span>'
mail='mailto:sidi-e-board@wellesley.edu'
links=[('About','/'),('People','/people/'),('Past events','/events/'),('Resources','/resources/')]
def header(active):
 nav=''.join('<a href="'+u+'"'+(' aria-current="page"' if n==active else '')+'>'+n+'</a>' for n,u in links)
 return f'<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="logo" href="/" aria-label="SIDI home"><img src="/assets/logo-02.webp" alt="SIDI" width="130" height="42"><span>Wellesley<br>College</span></a><button class="menu-button" aria-controls="main-nav" aria-expanded="false">Menu +</button><nav class="nav" id="main-nav" aria-label="Main navigation">{nav}</nav><a class="contact-link" href="{mail}">Say hello ↗</a></div></header>'
def footer():
 nav=''.join(f'<a href="{u}">{n}</a>' for n,u in links)
 return f'<footer class="site-footer"><div class="wrap"><div class="footer-main"><div class="footer-brand"><img src="/assets/logo-03.webp" alt="SIDI" loading="lazy"><p>Student Interdisciplinary Data Initiative<br>Wellesley College</p></div><nav class="footer-column" aria-label="Footer navigation">{nav}</nav><div class="footer-column"><a href="https://www.instagram.com/wellesleysidi/" target="_blank" rel="noopener noreferrer">Instagram ↗</a><a href="{mail}">sidi-e-board@wellesley.edu ↗</a></div></div><div class="footer-bottom"><span>© 2026 SIDI · Wellesley College</span></div></div></footer>'
def write_page(active,path,body,desc):
 title=('About SIDI — Wellesley College' if active=='About' else active+' — SIDI at Wellesley')
 route='' if path=='' else path+'/'
 doc=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#2e3488"><meta property="og:title" content="{title}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:image" content="{SITE_URL}/assets/fair-2.webp"><link rel="icon" type="image/webp" href="/assets/logo-20.webp"><link rel="canonical" href="{SITE_URL}/{route}"><link rel="stylesheet" href="/fonts.css"><link rel="stylesheet" href="/style.css"><script src="/site.js" defer></script></head><body>{header(active)}<main id="main">{body}</main>{footer()}</body></html>'
 doc=re.sub(r'((?:href|src)=")/(?!/)',lambda m:m[1]+BASE_PATH+'/',doc)
 dest=out/path;dest.mkdir(parents=True,exist_ok=True);(dest/'index.html').write_text(doc)
def page_hero(title):
 return f'<section class="page-hero simple-hero"><h1>{title}</h1></section>'
about=f"""
<div class="wrap">
<section class="hero about-hero">
<div class="hero-top"><h1>About <em>SIDI.</em></h1><div class="hero-note"><p>The Student Interdisciplinary Data Initiative is a student-led community at Wellesley College for anyone curious about data.</p></div></div>
<div class="hero-photo"><img src="/assets/fair-2.webp" alt="SIDI members welcoming students at the Wellesley Fall Orgs Fair" fetchpriority="high" width="1200" height="800"></div>
<div class="image-caption"><span>Fall Orgs Fair, 2026</span><span>Wellesley College</span></div>
</section>
<section class="about-copy"><div><p>We bring students across disciplines together through workshops, peer mentorship, and conversations about data. Explore new skills, meet students and alums, and discover how data connects to your interests.</p><p>All Wellesley class years, majors, and experience levels are welcome. There are no membership fees.</p><a class="arrow-link" href="{mail}">Contact SIDI {arrow}</a></div><div class="about-links"><a href="/people/">People {arrow}</a><a href="/events/">Past events {arrow}</a><a href="/resources/">Resources {arrow}</a></div></section>
</div>"""
write_page('About','',about,'SIDI is the Student Interdisciplinary Data Initiative at Wellesley College. A community for everyone curious about data.')
people=page_hero('People')
people+='<p class="board-term">2026–2027 E-Board</p><div class="people-grid body-end">'
for p in data['roster']:
 key=p['firstName'].lower()
 if key=='ilishaa':key='ilisha'
 image=out/'assets'/f'{key}.webp'
 if image.exists():portrait=f'<img class="portrait" src="/assets/{key}.webp" alt="{e(p["name"])}" loading="lazy" width="400" height="480">'
 else:portrait=f'<div class="initials"><strong aria-hidden="true">{"".join(w[0] for w in p["name"].split())}</strong><small>Meet {e(p["firstName"])}</small></div>'
 year=f'<p class="class-year">Class of {e(p["year"])}</p>' if p['year'] else ''
 major=f'<p class="major">{e(p["major"])}</p>' if p['major'] else ''
 people+=f'<article class="person-card">{portrait}<h2>{e(p["name"])}</h2>{year}{major}</article>'
people+='</div>'
write_page('People','people','<div class="wrap">'+people+'</div>','Meet the 2026–2027 SIDI E-Board at Wellesley College.')
events=page_hero('Past events')
events+='<div class="filters" aria-label="Filter past events">'
for cat in ['All','Community','Workshops','Talks','Academic']:events+=f'<button type="button" class="filter" data-category="{cat}" aria-pressed="{str(cat=="All").lower()}">{cat}</button>'
events+='<label class="filter-year" for="event-year">Year<select id="event-year"><option value="">All years</option><option>2026</option><option>2025</option></select></label></div><p class="event-count" id="event-count" role="status" aria-live="polite">7 past events</p><div class="event-grid">'
photos={0:('mentorship','SIDI Big/Little mentorship kickoff in the Science Center'),2:('fair-2','SIDI table at the Fall Orgs Fair'),3:('talk-0','Attendees at the Anna Kawakami alumnae talk'),5:('sql-0','Students working together at SQL 101')}
graphics={1:'General<br>Meeting',4:'Course<br>Preview',6:'First-Year<br>Bonding'}
for i,ev in enumerate(data['events']):
 dt=date.fromisoformat(ev['date']);label=dt.strftime('%b %d, %Y').replace(' 0',' ')
 if i in photos:picture=f'<img src="/assets/{photos[i][0]}.webp" alt="{photos[i][1]}" loading="lazy" width="600" height="400">'
 else:picture=f'<div class="event-graphic {"lime" if i==4 else ""}" aria-hidden="true"><div class="graphic-top">SIDI / {e(ev["category"])}</div><div class="graphic-title">{graphics[i]}</div><div class="graphic-bottom"><span>{dt.strftime("%m.%d.%y")}</span><span>✳</span></div></div>'
 events+=f'<article class="event-card" data-category="{e(ev["category"])}" data-year="{dt.year}">{picture}<div class="event-meta"><span>{e(ev["category"])}</span><time datetime="{ev["date"]}">{label}</time></div><h2>{e(ev["title"])}</h2><p>{e(ev["description"])}</p><p class="location">{e(ev["location"])}</p></article>'
events+='</div><p class="empty-state" id="event-empty" hidden>No events match this combination. Try another category or year.</p><div class="page-spacing"></div>'
write_page('Past events','events','<div class="wrap">'+events+'</div>','Explore SIDI’s past workshops, mentorship gatherings, alumnae talks, and community events.')
resources=page_hero('Resources')
resources+='<div class="resource-list">'
for r in data['resources']:
 resources+=f'<a class="resource-link" href="{e(r["url"],quote=True)}" target="_blank" rel="noopener noreferrer"><span class="resource-category">{e(r["category"])}</span><div class="resource-copy"><h2>{e(r["name"])}</h2><p>{e(r["description"])}</p><span class="resource-source">{e(r["source"])}</span></div><span class="resource-arrow" aria-hidden="true">↗</span><span class="sr-only"> (opens in a new tab)</span></a>'
resources+='</div><p class="resource-note">Check each listing for current deadlines and eligibility.</p><div class="page-spacing"></div>'
write_page('Resources','resources','<div class="wrap">'+resources+'</div>','Internship, product management, and software engineering resources for students and new graduates.')
# GitHub Pages does not process _redirects; keep an HTML redirect for old bookmarks.
redirect=out/'newsletter'
redirect.mkdir(exist_ok=True)
(redirect/'index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Resources — SIDI</title><meta http-equiv="refresh" content="0;url={BASE_PATH}/resources/"><link rel="canonical" href="{SITE_URL}/resources/"></head><body><p><a href="{BASE_PATH}/resources/">Continue to Resources</a></p></body></html>')
(out/'.nojekyll').touch()
not_found='<div class="wrap">'+page_hero('Page not found')+'<p><a class="arrow-link" href="/">Back to SIDI '+arrow+'</a></p><div class="page-spacing"></div></div>'
write_page('Page not found','not-found',not_found,'This page does not exist. Return to SIDI.')
(out/'404.html').write_text((out/'not-found/index.html').read_text().replace(SITE_URL+'/not-found/',SITE_URL+'/'))
(out/'not-found/index.html').unlink();(out/'not-found').rmdir()
print('Built About, People, Past events, and Resources.')
