---
name: kb-extract
description: Zamienia jedno lub wiele źródeł z /sources w JEDEN changeset do przeglądu w /inbox – równolegli ekstraktorzy na oknach, dopasowanie do istniejących atomów i między źródłami partii, triage i budżet. Użyj po /kb-ingest, /kb-collect lub /kb-capture albo gdy użytkownik prosi o wyciągnięcie wiedzy ze źródeł.
argument-hint: "<SRC-id …> | --pending"
---

# /kb-extract

Orkiestrujesz potok. **Nie piszesz** kandydatów ani decyzji sam: robią to subagenci, a skrypty `./kb` pilnują schematu.

1. **Źródła.** Podane `SRC-…` albo `--pending`, czyli wszystkie źródła bez changesetu (`./kb pending`). Kilka źródeł oznacza **jeden** changeset partii, a ta sama rzecz z różnych źródeł zostanie połączona w jedną propozycję z wieloma dowodami.
2. **Mówcy.** Sprawdź frontmatter każdego źródła. Jeśli któryś mówca w `speakers` ma `null`, zatrzymaj się i poproś o mapowanie (`./kb speakers`).
3. **Okna:** `./kb extract-prep <SRC …>` (albo `--pending`) zwraca `cs`, `context`, `windows` (każde z polem `source`), `open_changesets` i `already_extracted`.
   - `open_changesets` niepuste: uprzedź, że treści otwartych changesetów nie są jeszcze w bazie, więc matcher ich nie zobaczy. Zaproponuj najpierw `/kb-apply`. To ostrzeżenie, nie blokada.
   - `already_extracted` niepuste: te źródła mają już changeset. Zapytaj, czy na pewno ekstrahować ponownie.
4. **Ekstrakcja równoległa.** W **jednej wiadomości** uruchom `kb-extractor` dla każdego okna:
   > Kontekst: `<context>`. Okno: `<path>`. Zapisz kandydatów do: `<out>`.
5. **Kontrola schematu:** `./kb match-prep <cs>`. Przy błędach uruchom ponownie `kb-extractor` tylko dla wadliwych okien i podaj mu listę błędów (maks. 2 próby na okno).
6. **Dopasowanie.** Jeśli `with_matches > 0` (podobne atomy w bazie lub podobni kandydaci z innych źródeł partii), uruchom `kb-matcher`:
   > Paczka: `<matchpack>`. Zapisz decyzje do: `<out>`.

   W przeciwnym razie zapisz do `<out>` dokładnie `{"decisions": []}`.
7. **Changeset:** `./kb build <cs>`. Przy błędzie w `matched.json` wróć do kroku 6 z listą błędów.
8. **Raport** (krótko): liczba źródeł i propozycji według akcji, ile potwierdzonych w kilku źródłach (`multi_source`), ile poza budżetem, szum, action itemy, ścieżka pliku. Wymień pozycje do uwagi: zastąpienia, sprzeczności („SPRZECZNOŚĆ:”, z rekomendacją skryptu: zastąp albo śledź; człowiek może je zamknąć polem „zastąp” w przeglądzie), decyzje bez mandatu.
9. Przypomnij o przeglądzie w Obsidianie (dokładnie jedno pole na propozycję), a potem o `/kb-apply <cs>`.

Nie zaznaczaj pól w changesecie za użytkownika. Przegląd jest bramką człowieka.
