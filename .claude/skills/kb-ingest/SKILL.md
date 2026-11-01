---
name: kb-ingest
description: Dodaje POJEDYNCZE źródło (transkrypcję lub dokument TXT/MD) do bazy wiedzy – normalizuje, dzieli na adresowalne fragmenty ^sN, ustala datę wydarzenia, mapuje mówców i commituje snapshot. Dla wielu plików z folderu użyj /kb-collect, dla rozmowy z agentem /kb-capture.
argument-hint: <ścieżka-do-pliku> [tytuł] [data YYYY-MM-DD]
---

# /kb-ingest

1. Ustal plik i tytuł (domyślnie nazwa pliku).
2. **Data wydarzenia** (`valid_from` atomów). Podaj `--date` tylko wtedy, gdy ją znasz. W przeciwnym razie skrypt ustala ją sam w tej kolejności: data w nazwie pliku → data w nagłówku treści → data modyfikacji pliku → dzisiaj.
3. **Podgląd:** `./kb ingest "<plik>" --dry-run` pokazuje typ, datę, `date_source`, mówców i to, czy plik już jest w bazie. Jeśli źródło daty jest słabe (`data modyfikacji pliku`, `dzisiaj`), zapytaj, czy data jest poprawna, **zanim** zapiszesz. Źródła są niezmienne, więc późniejsza poprawka daty jest kłopotliwa.
4. **Zapis:**
   ```
   ./kb ingest "<plik>" [--title "<tytuł>"] [--date <YYYY-MM-DD>]
   ```
   Typ (`transcript` lub `document`) rozpoznaje się automatycznie. `--kind` wymuś tylko wtedy, gdy rozpoznanie zawiedzie.
5. Jeśli są `unresolved_speakers`. Dla każdej nieznanej etykiety:
   - sprawdź podobne osoby: `./kb person similar "<etykieta>"`,
   - zapytaj człowieka (AskUserQuestion): (a) to istniejąca osoba → `./kb person alias <slug> "<etykieta>"`, (b) nowa osoba → zapytaj o imię i rolę, potem `./kb person add <slug> "<Imię>" --alias "<etykieta>" --role "<rola>"`, (c) osoba bez znaczenia → zostaw nierozwiązaną,
   - **mandat**: nowa osoba dostaje `decides: []` i `org_mandate: false`. Flag `--decides` i `--org-mandate` użyj tylko wtedy, gdy człowiek sam o to poprosi. Nigdy ich nie zgaduj,
   - po rozstrzygnięciu zmapuj: `./kb speakers <SRC-id> "Speaker 1=anna-k"`.
6. Zgłoś id, typ, liczbę fragmentów, datę i commit. Zaproponuj `/kb-extract <SRC-id>`.

Obsługiwane są tylko `.txt` i `.md`.
