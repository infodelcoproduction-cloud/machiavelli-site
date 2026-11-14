"""Pages de partage : une petite page par montre (m/<id>.html) avec l'aperçu (titre, prix, photo)
que WhatsApp, Instagram, Facebook, iMessage… affichent quand on partage le lien. Elle renvoie aussitôt
vers la fiche de la montre sur le site. À relancer après chaque mise à jour de data/stock.json."""
import json, os, glob, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
base = json.load(open('data/site.json', encoding='utf-8'))['base'].rstrip('/') + '/'
stock = json.load(open('data/stock.json', encoding='utf-8'))
os.makedirs('m', exist_ok=True)
e = lambda s: html.escape(str(s or ''), quote=True)
euro = lambda n: '€ ' + f'{n:,}'.replace(',', '.')
keep = set()
for w in stock:
    title = f"{w.get('brand', '')} {w.get('model', '')}".strip()
    price = 'Réservée' if w.get('price') is None else euro(w['price']) + ' TTC'
    bits = [('Réf. ' + w['ref']) if w.get('ref') else '', w.get('year') if w.get('year') not in (None, '', 'Non communiquée') else '',
            w.get('set') if w.get('set') not in (None, '', 'Non communiqué') else '', w.get('cond') if w.get('cond') not in (None, '', 'Non communiqué') else '', price]
    desc = ' · '.join(b for b in bits if b)
    img = base + 'photos/' + w['photos'][0] + '.jpg' if w.get('photos') else base + 'img/og.jpg'
    url = base + 'm/' + w['id'] + '.html'
    target = '../#montre-' + w['id']
    page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} — Machiavelli Watches</title><meta name="description" content="{e(desc)}"><meta name="robots" content="noindex,follow">
<meta property="og:type" content="product"><meta property="og:site_name" content="Machiavelli Watches"><meta property="og:locale" content="fr_BE">
<meta property="og:title" content="{e(title)} — {e(price)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{e(img)}"><meta property="og:url" content="{e(url)}">
<meta name="twitter:card" content="summary_large_image"><link rel="canonical" href="{e(base)}#montre-{e(w['id'])}"><link rel="icon" type="image/png" href="../img/favicon.png">
<meta http-equiv="refresh" content="0; url={e(target)}"><script>location.replace({json.dumps(target)})</script></head>
<body style="margin:0;background:#2e2c2a;color:#f4efe8;font-family:Georgia,serif;display:grid;place-items:center;min-height:100vh"><a href="{e(target)}" style="color:#f4efe8">{e(title)} — Machiavelli Watches</a></body></html>
'''
    path = f"m/{w['id']}.html"
    with open(path, 'w', encoding='utf-8') as f: f.write(page)
    keep.add(path)
for p in glob.glob('m/*.html'):
    if p not in keep: os.remove(p)
print(f'{len(keep)} pages de partage')
