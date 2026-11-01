"""Testy samego mechanizmu ramy (na kopii repozytorium w katalogu tymczasowym)."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tests.rama.rama_check import ocen

REPO = Path(__file__).resolve().parents[2]


class RamaCheckerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="rama-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.root = self.tmp / "repo"
        shutil.copytree(REPO, self.root, symlinks=True,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", ".kb"))

    def odstepstwa(self, tekst):
        (self.root / "odstepstwa.yaml").write_text(tekst, encoding="utf-8")

    def niespelnione(self, w):
        return {eid for eid, _ in w["niespelnione"]}

    def test_stan_startowy_na_zadaniu_1_jest_zielony(self):
        w = ocen(self.root, 1)
        self.assertEqual(w["niespelnione"], [])
        self.assertEqual(w["bledy_odstepstw"], [])
        self.assertIn("zlote-zasady", w["ok"])

    def test_elementy_z_pozniejszych_zadan_nie_sa_sprawdzane(self):
        w = ocen(self.root, 1)
        self.assertIn("hooki-claude", w["poza_zakresem"])
        self.assertIn("kontrakt-cli", w["poza_zakresem"])

    def test_zadanie_2_wymaga_cli_i_testow_uczestnika(self):
        self.assertTrue({"kontrakt-cli", "testy-z-kodem"} <= self.niespelnione(ocen(self.root, 2)))

    def test_po_dodaniu_cli_i_testu_zadanie_2_przechodzi(self):
        (self.root / "tools/kb/cli.py").write_text("def main():\n    return 0\n", encoding="utf-8")
        (self.root / "tests/test_moj.py").write_text("import unittest\n", encoding="utf-8")
        self.assertEqual(ocen(self.root, 2)["niespelnione"], [])

    def test_usuniecie_zasady_z_claude_md_jest_wykryte(self):
        p = self.root / "CLAUDE.md"
        p.write_text(p.read_text(encoding="utf-8").replace("LLM proponuje, skrypt zapisuje", "model robi wszystko"),
                     encoding="utf-8")
        self.assertIn("zlote-zasady", self.niespelnione(ocen(self.root, 1)))

    def test_brak_katalogu_ramy_jest_wykryty(self):
        shutil.rmtree(self.root / "inbox" / "done")
        self.assertIn("uklad-katalogow", self.niespelnione(ocen(self.root, 1)))

    def test_zepsuty_schemat_jest_wykryty(self):
        (self.root / "schema/schema.yaml").write_text("schema_version: 1\ntypes: {}\n", encoding="utf-8")
        self.assertIn("format-atomu", self.niespelnione(ocen(self.root, 1)))

    def test_pole_zarzadzane_usuniete_ze_schematu_jest_wykryte(self):
        p = self.root / "schema/schema.yaml"
        p.write_text(p.read_text(encoding="utf-8").replace("  - evidence\n", "", 1), encoding="utf-8")
        w = ocen(self.root, 1)
        self.assertIn("format-atomu", self.niespelnione(w))

    def test_odstepstwo_z_kompletnym_wpisem_zalicza_element(self):
        (self.root / "CLAUDE.md").write_text("pusty plik", encoding="utf-8")
        self.odstepstwa("odstepstwa:\n  - element: zlote-zasady\n    powod: moje zasady są gdzie indziej\n"
                        "    skutek: agent nie czyta ich z CLAUDE.md\n    jak_sprawdzam: ręcznie przy każdym zadaniu\n")
        w = ocen(self.root, 1)
        self.assertIn("zlote-zasady", w["odstepstwa"])
        self.assertEqual(w["niespelnione"], [])
        self.assertEqual(w["bledy_odstepstw"], [])

    def test_wpis_z_pustym_polem_nie_liczy_sie_i_jest_bledem(self):
        (self.root / "CLAUDE.md").write_text("pusty plik", encoding="utf-8")
        self.odstepstwa("odstepstwa:\n  - element: zlote-zasady\n    powod: bo tak\n    skutek: ''\n    jak_sprawdzam: x\n")
        w = ocen(self.root, 1)
        self.assertIn("zlote-zasady", self.niespelnione(w))
        self.assertTrue(any("puste pola: skutek" in b for b in w["bledy_odstepstw"]))

    def test_nieznany_element_w_odstepstwach_to_blad(self):
        self.odstepstwa("odstepstwa:\n  - element: literowka\n    powod: a\n    skutek: b\n    jak_sprawdzam: c\n")
        self.assertTrue(any("nieznany element 'literowka'" in b for b in ocen(self.root, 1)["bledy_odstepstw"]))

    def test_zepsuty_yaml_odstepstw_to_blad(self):
        self.odstepstwa("odstepstwa: [niezamkniete\n")
        self.assertTrue(any("niepoprawny YAML" in b for b in ocen(self.root, 1)["bledy_odstepstw"]))

    def test_brak_pliku_odstepstw_to_blad(self):
        (self.root / "odstepstwa.yaml").unlink()
        self.assertTrue(any("brak pliku" in b for b in ocen(self.root, 1)["bledy_odstepstw"]))

    def test_odstepstwa_bez_listy_sa_dozwolone(self):
        self.odstepstwa("odstepstwa:\n")
        self.assertEqual(ocen(self.root, 1)["bledy_odstepstw"], [])

    def test_hooki_claude_przechodza_po_wgraniu_ustawien_z_dodatkow(self):
        shutil.copy(self.root / "dodatki/claude-settings-zadanie-7.json", self.root / ".claude/settings.json")
        json.loads((self.root / ".claude/settings.json").read_text(encoding="utf-8"))   # poprawny JSON
        self.assertNotIn("hooki-claude", self.niespelnione(ocen(self.root, 7)))

    def test_hooki_claude_nie_przechodza_na_ustawieniach_startowych(self):
        self.assertIn("hooki-claude", self.niespelnione(ocen(self.root, 7)))

    def test_ci_przechodzi_po_skopiowaniu_szablonu(self):
        self.assertIn("ci", self.niespelnione(ocen(self.root, 8)))
        (self.root / ".github/workflows").mkdir(parents=True)
        shutil.copy(self.root / "dodatki/github-actions-tests.yml", self.root / ".github/workflows/tests.yml")
        self.assertNotIn("ci", self.niespelnione(ocen(self.root, 8)))

    def test_zadanie_czytane_z_pliku_a_zly_plik_daje_1(self):
        (self.root / "zadanie.txt").write_text("7\n", encoding="utf-8")
        self.assertEqual(ocen(self.root)["zadanie"], 7)
        (self.root / "zadanie.txt").write_text("abc", encoding="utf-8")
        self.assertEqual(ocen(self.root)["zadanie"], 1)

    def test_nieznany_typ_kontroli_w_manifescie_jest_zglaszany(self):
        p = self.root / "rama.yaml"
        p.write_text(p.read_text(encoding="utf-8") + "\n  dziwny:\n    nazwa: x\n    od_zadania: 1\n    sprawdz:\n      - cos: 1\n",
                     encoding="utf-8")
        self.assertIn("dziwny", self.niespelnione(ocen(self.root, 1)))

    def test_plik_niewykonywalny_jest_wykryty(self):
        (self.root / "kb").chmod(0o644)
        (self.root / "tools/kb/cli.py").write_text("x = 1\n", encoding="utf-8")
        self.assertIn("kontrakt-cli", self.niespelnione(ocen(self.root, 2)))
