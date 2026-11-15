"""Recopie les tarifs de l'onglet « Tarifs » de l'Excel de pilotage dans index.html (bloc PRICE_CONFIG),
pour l'affichage du prix au survol des dates du calendrier.

Usage :  python3 _outils/generer_tarifs_site.py "<chemin de l'Excel de pilotage>"
Puis :   python3 _outils/generer_page_en.py
Nécessite openpyxl. Ne modifie pas l'Excel.
"""
import os, re, sys, json, datetime as dt
import openpyxl

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
xl = sys.argv[1]
ws = openpyxl.load_workbook(xl, data_only=False)['Tarifs']

def find_row(label):
    for r in range(1, ws.max_row + 1):
        if ws.cell(r, 2).value == label:
            return r
    raise SystemExit(f'Ligne « {label} » introuvable dans l\'onglet Tarifs')

# paramètres
majo = float(ws['F7'].value or 0)
nmin_default = int(ws['F8'].value or 3)

# niveaux : sous l'en-tête « Code » de la section 2
r = find_row('Code') + 1
levels = {}
while ws.cell(r, 3).value in ('Nuit', 'Semaine'):
    code, mode, nmin = ws.cell(r, 2).value, ws.cell(r, 3).value, ws.cell(r, 4).value
    sem, nuit = ws.cell(r, 6).value, ws.cell(r, 7).value
    if isinstance(nmin, str):
        nmin = nmin_default
    if mode == 'Nuit':
        levels[code] = {'mode': 'night', 'price': round(float(nuit)), 'min': int(nmin)}
    else:
        levels[code] = {'mode': 'week', 'price': round(float(sem)), 'night': round(float(sem) / 7 * (1 + majo)), 'min': int(nmin)}
    r += 1

# calendrier : sous l'en-tête « Du » de la section 3
r = find_row('Du') + 1
periods = []
while r <= ws.max_row:
    du, au, code = ws.cell(r, 2).value, ws.cell(r, 3).value, ws.cell(r, 6).value
    if isinstance(du, dt.datetime) and isinstance(au, dt.datetime) and code in levels:
        p = {'start': du.strftime('%Y-%m-%d'), 'end': au.strftime('%Y-%m-%d')}
        p.update(levels[code])
        periods.append(p)
    r += 1
if not periods:
    raise SystemExit('Aucune période lue dans l\'onglet Tarifs')

block = ('/* PRICES:START (généré par _outils/generer_tarifs_site.py, ne pas modifier à la main) */\n'
         'const PRICE_CONFIG=' + json.dumps(periods, ensure_ascii=False, separators=(',', ':')).replace('},{', '},\n  {') + ';\n'
         '/* PRICES:END */')
p = os.path.join(root, 'index.html')
html = open(p, encoding='utf-8').read()
new, n = re.subn(r'/\* PRICES:START.*?/\* PRICES:END \*/', lambda m: block, html, flags=re.S)
if n != 1:
    raise SystemExit('Bloc PRICES:START/END introuvable dans index.html')
open(p, 'w', encoding='utf-8').write(new)
print(f'{len(periods)} périodes de tarifs écrites dans index.html')
