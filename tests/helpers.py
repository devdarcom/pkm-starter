"""Szkielet testów uczestnika na poziomie CLI: izolowany katalog bazy i wywołania ./kb jako procesu.

Dzięki temu testy nie zależą od tego, jak zorganizujesz kod w tools/kb/, a nigdy nie dotykają Twojej prawdziwej bazy.
Użycie:

    from tests.helpers import KBCase

    class MojTest(KBCase):
        def test_validate_odrzuca_atom_bez_obszaru(self):
            self.zapisz_atom("atoms/rules/RULE-0001.md", {"id": "RULE-0001", "type": "rule", ...}, "# Tytuł\\n")
            self.assertEqual(self.kb("validate").returncode, 1)
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
DZIEN_TESTOWY = "2026-11-01"


class KBCase(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="kb-test-")).resolve()
        self.addCleanup(shutil.rmtree, self.root, True)
        shutil.copytree(REPO / "schema", self.root / "schema")
        for plik in ("kb.yaml", "kb"):
            shutil.copy(REPO / plik, self.root / plik)
        shutil.copytree(REPO / ".githooks", self.root / ".githooks")
        os.symlink(REPO / "tools", self.root / "tools")
        for d in ("sources/raw", "inbox/done", "atoms/decisions", "atoms/rules", "atoms/questions", "atoms/facts",
                  "atoms/_tracked", "glossary", "areas", "actions"):
            (self.root / d).mkdir(parents=True)
        (self.root / ".gitignore").write_text(".kb/\n", encoding="utf-8")
        for args in (("init", "-q", "-b", "main"), ("config", "user.name", "Tester"),
                     ("config", "user.email", "t@example.com"), ("config", "core.hooksPath", ".githooks"),
                     ("add", "-A"), ("commit", "-q", "--no-verify", "-m", "init")):
            subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True)

    # ---- pomocnicze ----
    def kb(self, *args, stdin=None):
        """Wywołuje ./kb w izolowanym katalogu. Zwraca CompletedProcess (returncode, stdout, stderr)."""
        env = {**os.environ, "KB_ROOT": str(self.root), "KB_TODAY": DZIEN_TESTOWY}
        return subprocess.run([str(self.root / "kb"), *args], cwd=self.root, capture_output=True, text=True,
                              input=stdin, env=env)

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True)

    def zapisz(self, rel: str, tekst: str) -> Path:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(tekst, encoding="utf-8")
        return p

    def zapisz_atom(self, rel: str, meta: dict, tresc: str, commit: bool = True) -> Path:
        """Zapisuje plik atomu (frontmatter + treść) i opcjonalnie commituje, żeby drzewo było czyste."""
        fm = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)
        p = self.zapisz(rel, f"---\n{fm}---\n{tresc}")
        if commit:
            self.git("add", "-A")
            self.git("commit", "-q", "--no-verify", "-m", f"seed {meta.get('id', rel)}")
        return p
