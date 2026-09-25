"""Régénère en/index.html à partir de index.html (texte FR -> attributs data-en).
A relancer après chaque modification de index.html :  python3 _outils/generer_page_en.py
Nécessite beautifulsoup4 (pip install beautifulsoup4)."""
import re, os
from bs4 import BeautifulSoup
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
soup=BeautifulSoup(open(os.path.join(root,'index.html'),encoding='utf-8').read(),'html.parser')
soup.html['lang']='en'
for el in soup.select('[data-en]'):
    frag=BeautifulSoup(el['data-en'],'html.parser'); el.clear()
    for c in list(frag.contents): el.append(c)
for el in soup.select('[data-en-ph]'): el['placeholder']=el['data-en-ph']
def meta(sel,attr,val): soup.select_one(sel)[attr]=val
soup.title.string="Holiday apartment for 6 in Les Carroz d'Arâches — Lodge Le Chamois 4★"
meta('meta[name=description]','content',"Lodge Le Chamois: 4-star 83 m² apartment for 6 in the heart of Les Carroz d'Arâches, Grand Massif ski area. 45 m² terrace, Nordic bath, 3 bedrooms including a master suite.")
meta('link[rel=canonical]','href','https://lodgelechamois.com/en/')
meta('meta[property="og:title"]','content',"Lodge Le Chamois — 4★ holiday apartment in Les Carroz d'Arâches, Grand Massif")
meta('meta[property="og:description"]','content',"Charming 83 m² apartment for 6, 45 m² west- and north-facing terrace and Nordic bath, in the centre of Les Carroz d'Arâches (Grand Massif).")
meta('meta[property="og:url"]','content','https://lodgelechamois.com/en/')
meta('meta[property="og:locale"]','content','en_GB')
meta('meta[property="og:locale:alternate"]','content','fr_FR')
meta('meta[name="twitter:description"]','content',"4★ apartment for 6, 45 m² terrace and Nordic bath, in the heart of the Grand Massif.")
for b in soup.select('.lang-toggle button'):
    cls=[c for c in b.get('class',[]) if c!='active']
    if b['data-lang']=='en': cls.append('active')
    if cls: b['class']=cls
    elif 'class' in b.attrs: del b['class']
out=str(soup)
out=out.replace('src="./','src="../').replace("url('./","url('../").replace("'./'+","'../'+").replace('href="blog/index.html"','href="../blog/index-en.html"')
out=out.replace('/mentions-legales.html#donnees','/mentions-legales.html#en').replace('href="/mentions-legales.html"','href="/mentions-legales.html#en"')
out=out.replace('"url":"https://lodgelechamois.com/"','"url":"https://lodgelechamois.com/en/"',1)
os.makedirs(os.path.join(root,'en'),exist_ok=True)
open(os.path.join(root,'en','index.html'),'w',encoding='utf-8').write(out)
print('en/index.html régénéré')
