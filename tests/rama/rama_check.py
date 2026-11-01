"""Sprawdzanie ramy kursu: czy elementy ścieżki standardowej są na miejscu albo świadomie zastąpione odstępstwem.

Manifest: rama.yaml. Odstępstwa: odstepstwa.yaml. Bieżące zadanie: zadanie.txt (liczba).
Element jest sprawdzany dopiero od zadania `od_zadania`. Spełniony element nie wymaga niczego.
Niespełniony element przechodzi tylko wtedy, gdy ma w odstepstwa.yaml wpis z czterema niepustymi polami.
"""
from __future__ import annotations

import os
from pathlib import Path

import yaml

POLA_ODSTEPSTWA = ("element", "powod", "skutek", "jak_sprawdzam")


def wczytaj_manifest(root: Path) -> dict:
    return yaml.safe_load((Path(root) / "rama.yaml").read_text(encoding="utf-8"))["elementy"]


def wczytaj_zadanie(root: Path) -> int:
    try:
        return int((Path(root) / "zadanie.txt").read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return 1


def wczytaj_odstepstwa(root: Path, elementy: dict):
    """({id elementu: [wpisy]}, [błędy]). Wpis niepełny albo z nieznanym elementem jest błędem i nie liczy się jako odstępstwo."""
    p = Path(root) / "odstepstwa.yaml"
    po_elemencie, bledy = {}, []
    if not p.exists():
        return po_elemencie, ["brak pliku odstepstwa.yaml"]
    try:
        dane = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        return po_elemencie, [f"odstepstwa.yaml: niepoprawny YAML ({e})"]
    wpisy = dane.get("odstepstwa") if isinstance(dane, dict) else None
    if wpisy is None:
        wpisy = []
    if not isinstance(wpisy, list):
        return po_elemencie, ["odstepstwa.yaml: klucz 'odstepstwa' musi być listą"]
    for i, w in enumerate(wpisy, 1):
        if not isinstance(w, dict):
            bledy.append(f"wpis {i}: nie jest obiektem (oczekiwane pola: {', '.join(POLA_ODSTEPSTWA)})")
            continue
        puste = [k for k in POLA_ODSTEPSTWA if not str(w.get(k) or "").strip()]
        if puste:
            bledy.append(f"wpis {i} ({w.get('element') or '?'}): puste pola: {', '.join(puste)}")
            continue
        if w["element"] not in elementy:
            bledy.append(f"wpis {i}: nieznany element '{w['element']}' (dozwolone: {', '.join(elementy)})")
            continue
        po_elemencie.setdefault(w["element"], []).append(w)
    return po_elemencie, bledy


def sprawdz_element(root: Path, el: dict) -> list:
    """Lista problemów elementu (pusta = element na miejscu)."""
    root = Path(root)
    problemy = []
    for c in el.get("sprawdz") or []:
        if "katalogi" in c:
            problemy += [f"brak katalogu {d}" for d in c["katalogi"] if not (root / d).is_dir()]
        elif "glob" in c:
            n = len([p for p in root.glob(c["glob"]) if p.is_file()])
            if n < c.get("min", 1):
                problemy.append(f"{c['glob']}: znaleziono {n}, wymagane co najmniej {c.get('min', 1)}")
        elif "plik" in c:
            p = root / c["plik"]
            if not p.is_file():
                problemy.append(f"brak pliku {c['plik']}")
                continue
            if c.get("wykonywalny") and not os.access(p, os.X_OK):
                problemy.append(f"{c['plik']} nie jest wykonywalny (chmod +x)")
            tekst = p.read_text(encoding="utf-8", errors="replace")
            problemy += [f"{c['plik']}: brak frazy „{f}”" for f in c.get("zawiera") or [] if f not in tekst]
            if "yaml_klucze" in c or "yaml_lista" in c:
                try:
                    dane = yaml.safe_load(tekst) or {}
                except yaml.YAMLError as e:
                    problemy.append(f"{c['plik']}: niepoprawny YAML ({e})")
                    continue
                problemy += [f"{c['plik']}: brak klucza {k}" for k in c.get("yaml_klucze") or [] if k not in dane]
                if "yaml_lista" in c:
                    spec = c["yaml_lista"]
                    lista = dane.get(spec["klucz"]) or []
                    brak = [x for x in spec["zawiera"] if x not in lista]
                    if brak:
                        problemy.append(f"{c['plik']}: {spec['klucz']} nie zawiera: {', '.join(brak)}")
        else:
            problemy.append(f"nieznany typ kontroli: {sorted(c)}")
    return problemy


def ocen(root: Path, zadanie: int = None) -> dict:
    """Raport: ok, odstepstwa (niespełnione, ale z wpisem), niespelnione [(id, problemy)], bledy_odstepstw."""
    root = Path(root)
    elementy = wczytaj_manifest(root)
    zadanie = zadanie if zadanie is not None else wczytaj_zadanie(root)
    odstepstwa, bledy = wczytaj_odstepstwa(root, elementy)
    wynik = {"zadanie": zadanie, "ok": [], "odstepstwa": [], "niespelnione": [], "bledy_odstepstw": bledy,
             "poza_zakresem": []}
    for eid, el in elementy.items():
        if el.get("od_zadania", 1) > zadanie:
            wynik["poza_zakresem"].append(eid)
            continue
        problemy = sprawdz_element(root, el)
        if not problemy:
            wynik["ok"].append(eid)
        elif eid in odstepstwa:
            wynik["odstepstwa"].append(eid)
        else:
            wynik["niespelnione"].append((eid, problemy))
    return wynik
