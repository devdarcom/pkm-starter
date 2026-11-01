"""Sprawdza szkielet testów (tests/helpers.py): izolowany katalog, git i launcher ./kb."""
import os
from pathlib import Path

from tests.helpers import KBCase


class SzkieletTest(KBCase):
    def test_izolowany_katalog_ma_schemat_launcher_i_git(self):
        self.assertTrue((self.root / "schema" / "schema.yaml").is_file())
        self.assertTrue(os.access(self.root / "kb", os.X_OK))
        self.assertTrue((self.root / "tools").is_symlink())                      # kod uczestnika, bez kopiowania
        self.assertNotEqual(self.root.resolve(), Path(__file__).resolve().parents[2])
        self.assertIn("init", self.git("log", "--format=%s").stdout)

    def test_zapisz_atom_commituje_i_zostawia_czyste_drzewo(self):
        self.zapisz_atom("atoms/rules/RULE-0001.md", {"id": "RULE-0001", "type": "rule"}, "# Tytuł\n")
        self.assertEqual(self.git("status", "--porcelain").stdout.strip(), "")
        self.assertIn("seed RULE-0001", self.git("log", "-1", "--format=%s").stdout)
        self.assertTrue((self.root / "atoms/rules/RULE-0001.md").read_text(encoding="utf-8").startswith("---\n"))

    def test_kb_wola_launcher_w_izolowanym_katalogu(self):
        # Na starcie nie ma jeszcze tools/kb/cli.py, więc launcher kończy się błędem importu, ale jest wywoływany poprawnie.
        r = self.kb("--help")
        if (Path(__file__).resolve().parents[2] / "tools/kb/cli.py").exists():
            self.assertEqual(r.returncode, 0, r.stderr)
        else:
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("kb", r.stderr)
