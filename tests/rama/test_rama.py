"""Test ramy na Twoim repozytorium: elementy ścieżki standardowej są na miejscu albo świadomie zastąpione odstępstwem.

Gdy test zawodzi, masz dwie drogi: naprawić element albo dopisać odstępstwo do odstepstwa.yaml
(element, powod, skutek, jak_sprawdzam, wszystkie niepuste). Wyjaśnienie elementów: DLACZEGO.md.
Bieżące zadanie ustawiasz w zadanie.txt; elementy z późniejszych zadań nie są jeszcze sprawdzane.
"""
import re
import unittest
from pathlib import Path

from tests.rama.rama_check import ocen, wczytaj_manifest

ROOT = Path(__file__).resolve().parents[2]


class RamaTest(unittest.TestCase):
    def test_odstepstwa_sa_kompletne(self):
        self.assertEqual(ocen(ROOT)["bledy_odstepstw"], [],
                         "odstepstwa.yaml: każdy wpis wymaga pól element, powod, skutek, jak_sprawdzam (niepustych)")

    def test_elementy_ramy_sa_na_miejscu_albo_maja_odstepstwo(self):
        w = ocen(ROOT)
        manifest = wczytaj_manifest(ROOT)
        for eid, problemy in w["niespelnione"]:
            with self.subTest(element=eid):
                rodzaj = manifest[eid].get("rodzaj", "?")
                self.fail(f"element „{eid}” ({rodzaj}, zadanie {manifest[eid].get('od_zadania', 1)}) niespełniony:\n  - "
                          + "\n  - ".join(problemy)
                          + f"\nNapraw go albo dopisz odstępstwo do odstepstwa.yaml. Wyjaśnienie: DLACZEGO.md, sekcja „{eid}”.")


class SpojnoscDokumentacjiTest(unittest.TestCase):
    def test_kazdy_element_manifestu_ma_wyjasnienie_w_dlaczego(self):
        tekst = (ROOT / "DLACZEGO.md").read_text(encoding="utf-8")
        naglowki = set(re.findall(r"^## ([a-z0-9-]+)\s*$", tekst, flags=re.M))
        manifest = set(wczytaj_manifest(ROOT))
        self.assertEqual(manifest - naglowki, set(), "elementy z rama.yaml bez sekcji w DLACZEGO.md")
        self.assertEqual(naglowki - manifest, set(), "sekcje w DLACZEGO.md bez elementu w rama.yaml")
