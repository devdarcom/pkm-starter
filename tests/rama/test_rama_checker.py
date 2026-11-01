"""Testy samego mechanizmu ramy.

Nie korzystają z Twojego repozytorium, tylko z repozytorium syntetycznego zbudowanego z rama.yaml
(spełnia wszystkie kontrole elementów do wskazanego zadania). Dzięki temu przechodzą niezależnie od tego,
na którym zadaniu jesteś i co już zbudowałeś.
"""
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from tests.rama.rama_check import ocen, wczytaj_manifest

REPO = Path(__file__).resolve().parents[2]


def zbuduj(root: Path, do_zadania: int):
    """Repozytorium spełniające kontrole wszystkich elementów z od_zadania <= do_zadania."""
    manifest = wczytaj_manifest(REPO)
    root.mkdir(parents=True)
    shutil.copy(REPO / "rama.yaml", root / "rama.yaml")
    (root / "odstepstwa.yaml").write_text("odstepstwa: []\n", encoding="utf-8")
    (root / "zadanie.txt").write_text(f"{do_zadania}\n", encoding="utf-8")
    pliki = {}
    for el in manifest.values():
        if el.get("od_zadania", 1) > do_zadania:
            continue
        for c in el.get("sprawdz") or []:
            if "katalogi" in c:
                for d in c["katalogi"]:
                    (root / d).mkdir(parents=True, exist_ok=True)
            elif "glob" in c:
                for i in range(c.get("min", 1)):
                    p = root / c["glob"].replace("**/", "").replace("*", f"fixture{i}", 1).replace("*", "x")
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text("fixture\n", encoding="utf-8")
            elif "plik" in c:
                spec = pliki.setdefault(c["plik"], {"frazy": [], "klucze": {}, "x": False})
                spec["frazy"] += c.get("zawiera") or []
                spec["x"] |= bool(c.get("wykonywalny"))
                for k in c.get("yaml_klucze") or []:
                    spec["klucze"].setdefault(k, [])
                if "yaml_lista" in c:
                    spec["klucze"].setdefault(c["yaml_lista"]["klucz"], [])
                    spec["klucze"][c["yaml_lista"]["klucz"]] += c["yaml_lista"]["zawiera"]
    for rel, spec in pliki.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        tekst = yaml.safe_dump(spec["klucze"], allow_unicode=True) if spec["klucze"] else ""
        tekst += "".join(f"# {f}\n" for f in spec["frazy"]) if spec["klucze"] else "\n".join(spec["frazy"]) + "\n"
        p.write_text(tekst, encoding="utf-8")
        if spec["x"]:
            p.chmod(0o755)
    return manifest


class RamaCheckerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="rama-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.root = self.tmp / "repo"
        self.manifest = wczytaj_manifest(REPO)

    def zbuduj(self, do_zadania=1):
        self.manifest = zbuduj(self.root, do_zadania)

    def odstepstwa(self, tekst):
        (self.root / "odstepstwa.yaml").write_text(tekst, encoding="utf-8")

    def niespelnione(self, w):
        return {eid for eid, _ in w["niespelnione"]}

    def element(self, eid):
        if eid not in self.manifest:
            self.skipTest(f"w rama.yaml nie ma elementu {eid}")
        return self.manifest[eid]

    def test_repozytorium_zgodne_z_rama_jest_zielone_na_kazdym_zadaniu(self):
        for n in range(1, 10):
            with self.subTest(zadanie=n):
                shutil.rmtree(self.root, ignore_errors=True)
                self.zbuduj(n)
                w = ocen(self.root, n)
                self.assertEqual(w["niespelnione"], [])
                self.assertEqual(w["bledy_odstepstw"], [])

    def test_elementy_z_pozniejszych_zadan_nie_sa_sprawdzane(self):
        self.zbuduj(1)
        w = ocen(self.root, 1)
        pozniejsze = {eid for eid, el in self.manifest.items() if el.get("od_zadania", 1) > 1}
        self.assertEqual(set(w["poza_zakresem"]), pozniejsze)

    def test_przejscie_do_kolejnego_zadania_wymaga_jego_elementow(self):
        self.zbuduj(1)
        nowe = {eid for eid, el in self.manifest.items()
                if el.get("od_zadania", 1) == 2 and el.get("sprawdz")}
        self.assertTrue(nowe, "w rama.yaml brak sprawdzanych elementów zadania 2")
        self.assertEqual(self.niespelnione(ocen(self.root, 2)), nowe)

    def test_usuniecie_zasady_z_claude_md_jest_wykryte(self):
        self.zbuduj(1)
        fraza = self.element("zlote-zasady")["sprawdz"][0]["zawiera"][0]
        p = self.root / "CLAUDE.md"
        p.write_text(p.read_text(encoding="utf-8").replace(fraza, "model robi wszystko"), encoding="utf-8")
        self.assertIn("zlote-zasady", self.niespelnione(ocen(self.root, 1)))

    def test_brak_katalogu_ramy_jest_wykryty(self):
        self.zbuduj(1)
        katalog = self.element("uklad-katalogow")["sprawdz"][0]["katalogi"][-1]
        shutil.rmtree(self.root / katalog)
        self.assertIn("uklad-katalogow", self.niespelnione(ocen(self.root, 1)))

    def test_zepsuty_schemat_i_brak_pola_zarzadzanego_sa_wykryte(self):
        self.zbuduj(1)
        self.element("format-atomu")
        p = self.root / "schema/schema.yaml"
        dane = yaml.safe_load(p.read_text(encoding="utf-8"))
        dane["tool_managed_fields"] = [f for f in dane["tool_managed_fields"] if f != "evidence"]
        p.write_text(yaml.safe_dump(dane), encoding="utf-8")
        self.assertIn("format-atomu", self.niespelnione(ocen(self.root, 1)))
        p.write_text("schema_version: [niezamkniete\n", encoding="utf-8")
        self.assertIn("format-atomu", self.niespelnione(ocen(self.root, 1)))

    def test_odstepstwo_z_kompletnym_wpisem_zalicza_element(self):
        self.zbuduj(1)
        self.element("zlote-zasady")
        (self.root / "CLAUDE.md").write_text("pusty plik", encoding="utf-8")
        self.odstepstwa("odstepstwa:\n  - element: zlote-zasady\n    powod: moje zasady są gdzie indziej\n"
                        "    skutek: agent nie czyta ich z CLAUDE.md\n    jak_sprawdzam: ręcznie przy każdym zadaniu\n")
        w = ocen(self.root, 1)
        self.assertIn("zlote-zasady", w["odstepstwa"])
        self.assertEqual(w["niespelnione"], [])
        self.assertEqual(w["bledy_odstepstw"], [])

    def test_wpis_z_pustym_polem_nie_liczy_sie_i_jest_bledem(self):
        self.zbuduj(1)
        self.element("zlote-zasady")
        (self.root / "CLAUDE.md").write_text("pusty plik", encoding="utf-8")
        self.odstepstwa("odstepstwa:\n  - element: zlote-zasady\n    powod: bo tak\n    skutek: ''\n    jak_sprawdzam: x\n")
        w = ocen(self.root, 1)
        self.assertIn("zlote-zasady", self.niespelnione(w))
        self.assertTrue(any("puste pola: skutek" in b for b in w["bledy_odstepstw"]))

    def test_nieznany_element_w_odstepstwach_to_blad(self):
        self.zbuduj(1)
        self.odstepstwa("odstepstwa:\n  - element: literowka\n    powod: a\n    skutek: b\n    jak_sprawdzam: c\n")
        self.assertTrue(any("nieznany element 'literowka'" in b for b in ocen(self.root, 1)["bledy_odstepstw"]))

    def test_zepsuty_lub_brakujacy_plik_odstepstw_to_blad(self):
        self.zbuduj(1)
        self.odstepstwa("odstepstwa: [niezamkniete\n")
        self.assertTrue(any("niepoprawny YAML" in b for b in ocen(self.root, 1)["bledy_odstepstw"]))
        (self.root / "odstepstwa.yaml").unlink()
        self.assertTrue(any("brak pliku" in b for b in ocen(self.root, 1)["bledy_odstepstw"]))

    def test_pusta_lista_odstepstw_jest_dozwolona(self):
        self.zbuduj(1)
        self.odstepstwa("odstepstwa:\n")
        self.assertEqual(ocen(self.root, 1)["bledy_odstepstw"], [])

    def test_zadanie_czytane_z_pliku_a_zly_plik_daje_1(self):
        self.zbuduj(1)
        (self.root / "zadanie.txt").write_text("7\n", encoding="utf-8")
        self.assertEqual(ocen(self.root)["zadanie"], 7)
        (self.root / "zadanie.txt").write_text("abc", encoding="utf-8")
        self.assertEqual(ocen(self.root)["zadanie"], 1)

    def test_nieznany_typ_kontroli_w_manifescie_jest_zglaszany(self):
        self.zbuduj(1)
        p = self.root / "rama.yaml"
        p.write_text(p.read_text(encoding="utf-8") + "\n  dziwny:\n    nazwa: x\n    od_zadania: 1\n    sprawdz:\n      - cos: 1\n",
                     encoding="utf-8")
        self.assertIn("dziwny", self.niespelnione(ocen(self.root, 1)))

    def test_plik_niewykonywalny_jest_wykryty(self):
        el = self.element("kontrakt-cli")
        self.zbuduj(el["od_zadania"])
        (self.root / "kb").chmod(0o644)
        self.assertIn("kontrakt-cli", self.niespelnione(ocen(self.root, el["od_zadania"])))


class DodatkiTest(unittest.TestCase):
    """Pliki z dodatki/ mają spełniać ramę po skopiowaniu we właściwe miejsce."""

    def sprawdz(self, eid, zrodlo, cel):
        from tests.rama.rama_check import sprawdz_element
        manifest = wczytaj_manifest(REPO)
        if eid not in manifest or not (REPO / zrodlo).exists():
            self.skipTest(f"brak elementu {eid} albo pliku {zrodlo}")
        tmp = Path(tempfile.mkdtemp(prefix="dodatki-"))
        self.addCleanup(shutil.rmtree, tmp, True)
        (tmp / cel).parent.mkdir(parents=True)
        shutil.copy(REPO / zrodlo, tmp / cel)
        self.assertEqual(sprawdz_element(tmp, manifest[eid]), [])

    def test_ustawienia_hookow_z_dodatkow(self):
        self.sprawdz("hooki-claude", "dodatki/claude-settings-zadanie-7.json", ".claude/settings.json")

    def test_szablon_ci_z_dodatkow(self):
        self.sprawdz("ci", "dodatki/github-actions-tests.yml", ".github/workflows/tests.yml")


if __name__ == "__main__":
    unittest.main()
