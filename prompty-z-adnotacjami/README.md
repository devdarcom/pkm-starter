# Prompty agentów z adnotacjami

W `.claude/agents/` leżą prompty czterech agentów w wersji, która ma być czytana przez model, bez komentarzy. Tutaj ta sama treść jest rozpisana **regułami z uzasadnieniem**: dlaczego reguła istnieje, co się psuje, gdy ją usuniesz, i czy jest kontraktem ze skryptem.

| Agent | Plik z adnotacjami | Prompt | Od zadania |
|---|---|---|---|
| `kb-extractor` | [kb-extractor.md](kb-extractor.md) | `.claude/agents/kb-extractor.md` | 4 |
| `kb-matcher` | [kb-matcher.md](kb-matcher.md) | `.claude/agents/kb-matcher.md` | 6 |
| `kb-compiler` | [kb-compiler.md](kb-compiler.md) | `.claude/agents/kb-compiler.md` | 7 |
| `kb-verifier` | [kb-verifier.md](kb-verifier.md) | `.claude/agents/kb-verifier.md` | 7 |

**Jak z tego korzystać.**
- Prompty w `.claude/agents/` to **baza reguł**. Wolno Ci dopisać swoją domenę (opis organizacji, żargon, przykłady) i dostosować listę obszarów.
- **Nie usuwaj reguł oznaczonych jako kontrakt** bez wpisu w `odstepstwa.yaml`: skrypty `./kb` zakładają kształt wyjścia opisany w tych promptach.
- Reguły zalecane możesz zmieniać, ale najpierw przeczytaj, co zapobiegają. Test ramy sprawdza obecność kluczowych fraz, więc usunięcie reguły bez odstępstwa zawiedzie test.
- Adnotacje nie są częścią promptu: nie wklejaj ich do `.claude/agents/`, bo wydłużają kontekst i niczego nie dodają modelowi.

**Oznaczenia:** **K** = kontrakt ze skryptem (sztywne), **Z** = zalecane (odstępstwo wolno, ale zapisz je).
