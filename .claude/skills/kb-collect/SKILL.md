---
name: kb-collect
description: Zbiera wszystkie NOWE pliki TXT/MD ze wskazanego folderu (np. eksportu z dyktafonu) do bazy wiedzy jedną partią – ustala daty wydarzeń, mapuje mówców i od razu przygotowuje jeden changeset dla całej partii. Użyj, gdy użytkownik wskazuje folder z nagraniami lub notatkami albo mówi „wciągnij nowe pliki”.
argument-hint: "[folder]  (domyślnie collect_folder z kb.yaml)"
---

# /kb-collect

1. **Folder.** Weź go z argumentu albo z `collect_folder` w `kb.yaml`. Jeśli nie ma żadnego, zapytaj. Folder jest tylko czytany: pliki zostają na miejscu, a kopie trafiają do `sources/raw/`.
2. **Podgląd:** `./kb collect "<folder>" --dry-run`. Pokaż tabelę:
   - **nowe pliki**: nazwa, typ (transkrypcja / dokument), **data i jej źródło**, nierozpoznani mówcy,
   - **pominięte**: już w bazie, duplikat w partii, nieobsługiwany format.

   Zwróć uwagę na daty z mniej pewnych źródeł (`data modyfikacji pliku`, `dzisiaj (brak innej daty)`). Zapytaj, czy je poprawić. Data trafi do `valid_from` atomów i ustawia kolejność w genealogii decyzji.
3. **Ingest:** `./kb collect "<folder>" --date "plik.txt=2026-10-21" …` (jedno `--date` na poprawkę). Wszystkie pliki trafiają do bazy jednym commitem.
4. **Mówcy.** Etykiety typu „Speaker 1” są **osobne dla każdego nagrania**, więc rozstrzygaj je per źródło (ta sama osoba w kilku nagraniach pod różnymi etykietami → jeden `person add`, potem `alias`). Dla każdego źródła z `unresolved_speakers` i każdej nieznanej etykiety:
   - sprawdź podobne osoby: `./kb person similar "<etykieta>"`,
   - zapytaj człowieka (AskUserQuestion): (a) to istniejąca osoba → `./kb person alias <slug> "<etykieta>"`, (b) nowa osoba → zapytaj o imię i rolę, potem `./kb person add <slug> "<Imię>" --alias "<etykieta>" --role "<rola>"`, (c) osoba bez znaczenia → zostaw nierozwiązaną,
   - **mandat**: nowa osoba dostaje `decides: []` i `org_mandate: false`. Flag `--decides` i `--org-mandate` użyj tylko wtedy, gdy człowiek sam o to poprosi. Nigdy ich nie zgaduj,
   - po rozstrzygnięciu zmapuj: `./kb speakers <SRC-id> "Speaker 1=anna-k"`.
5. **Ekstrakcja partii:** przejdź do `/kb-extract` z listą `id` ze wszystkich nowych źródeł (jeden changeset). Jeśli użytkownik woli tylko ingest, zakończ i podpowiedz `/kb-extract --pending`.

Ponowne uruchomienie na tym samym folderze jest bezpieczne: pliki już obecne w bazie (po sha256) są pomijane.
