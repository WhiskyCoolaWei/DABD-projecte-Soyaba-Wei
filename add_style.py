#!/usr/bin/env python3
"""
Afegeix <link rel="stylesheet" href="style.css"> a totes les pagines
del frontend que encara no l'enllacen (excepte dashboard.html i
dashboardPacient.html, que ja tenen el seu propi <style> complet).

Execucio (des de ~/Public/healthlog-app):
    python3 add_style.py
"""
import pathlib

FRONTEND = pathlib.Path("frontend")
EXCLUDE  = {"dashboard.html", "dashboardPacient.html"}
LINK     = '  <link rel="stylesheet" href="style.css">'
MARKER   = '<meta charset="UTF-8">'

if not FRONTEND.is_dir():
    raise SystemExit("Error: no trobo la carpeta 'frontend/'. Executa des de ~/Public/healthlog-app")

afegits, ja_tenia, sense_marcador = [], [], []

for f in sorted(FRONTEND.glob("*.html")):
    if f.name in EXCLUDE:
        continue
    text = f.read_text(encoding="utf-8")
    if "style.css" in text:
        ja_tenia.append(f.name)
        continue
    if MARKER not in text:
        sense_marcador.append(f.name)
        continue
    text = text.replace(MARKER, MARKER + "\n" + LINK, 1)
    f.write_text(text, encoding="utf-8")
    afegits.append(f.name)

print(f"Enllac afegit a {len(afegits)} pagines:")
for n in afegits:
    print(f"  + {n}")

if ja_tenia:
    print(f"\nJa el tenien ({len(ja_tenia)}):")
    for n in ja_tenia:
        print(f"  = {n}")

if sense_marcador:
    print(f"\nAVIS — no s'ha trobat '<meta charset=\"UTF-8\">' (revisar a ma):")
    for n in sense_marcador:
        print(f"  ! {n}")
