---
name: kb-eval
description: Mierzy jakość ekstrakcji względem ręcznie oznaczonego zestawu referencyjnego (precyzja, kompletność, trafność typów) i statystyki przeglądów; podpowiada strojenie promptu ekstraktora. Użyj przy tworzeniu zestawu referencyjnego, po zmianie promptów lub gdy użytkownik pyta o jakość.
argument-hint: [CS-id] [eval/gold/<SRC-id>.yaml]
---

# /kb-eval

## Tworzenie zestawu referencyjnego (raz na źródło)
1. Źródło musi być po `/kb-ingest`. Otwórz plik źródła `sources/<data wgrania>/<SRC-id>.md` (fragmenty `^sN`).
2. Razem z użytkownikiem oznacz **ręcznie**, co powinno zostać wyłuskane, i zapisz `eval/gold/<SRC-id>.yaml`:
   ```yaml
   source: SRC-000042-warsztat
   items:
     - {span: [s2, s7], type: decision, note: "gość zamiast rejestracji (SSO jako alternatywa w środku)"}
     - {span: [s9, s10], type: question}
     - {span: [s12, s12], type: fact}
   ```
   Odrzucone alternatywy są częścią decyzji, a nie osobnymi pozycjami. Action itemów i szumu nie oznaczamy.
   Pozycje proponuje człowiek, nie model, bo inaczej pomiar mierzy model sam sobą.
3. **Wyjątek: rozmowa z zatwierdzonym protokołem.** `./kb protocol-gold <SRC>` zamienia punkty protokołu w szkic wzorca (Ustalenia → decision, Fakty → fact, Otwarte kwestie → question; odrzucone warianty pomija, bo są alternatywami). Protokół napisał model, a człowiek tylko go zatwierdził, więc przejrzyj szkic krytycznie: popraw typy (ustalenie bywa regułą), zakresy `span` i sprawdź w transkrypcji, czy czegoś nie brakuje. Taki wzorzec liczy się jako słabszy niż oznaczony od zera, więc w zestawie powinny być też co najmniej 2 nagrania oznaczone ręcznie.

## Pomiar
1. Uruchom `/kb-extract <SRC-id>` do etapu `match-prep` włącznie (changesetu nie trzeba stosować).
2. `./kb eval <CS-id> eval/gold/<SRC-id>.yaml` zwraca precision, recall, type_accuracy, `missed` i `extra`.
3. `./kb stats` pokazuje decyzje przeglądów per typ i odsetek odrzuceń.
4. Interpretacja i strojenie (`.claude/agents/kb-extractor.md`):
   - niska precyzja lub dużo odrzuceń danego typu: zaostrz definicję typu i dodaj przykład negatywny,
   - niski recall: sprawdź `missed`; często chodzi o zbyt wąską jednostkę stwierdzenia albo o wypowiedzi rozproszone między mówcami,
   - zła trafność typów: doprecyzuj granice (decyzja vs reguła, fakt vs decyzja).
5. Po zmianie promptu powtórz pomiar na **wszystkich** plikach w `eval/gold/` (regresja). Wyniki zapisz w `eval/WYNIKI.md` (data, zmiana, metryki).

Cel MVP: przegląd godzinnej rozmowy < 15 min, duplikaty < 5%.

## Do zrobienia: testy na prawdziwych danych
Dotychczasowe testy przeszły na fikstury i ręcznie napisanych wynikach subagentów. **Prompty i heurystyki niżej nie zostały jeszcze zmierzone na prawdziwych nagraniach i prawdziwej bazie.** Nie traktuj ich wyników jako sprawdzonych, dopóki ta lista nie zostanie odhaczona (wyniki do `eval/WYNIKI.md`).

### Sprzeczności (priorytet)
Zestaw `eval/gold-conflicts.yaml`, oznaczany **ręcznie** przez człowieka na prawdziwych atomach (5–10 par sprzecznych, tyle samo zgodnych, w tym pary międzytypowe i takie, w których sprzeczność jest wyrażona innymi słowami):
```yaml
pairs:
  - {a: DEC-0001, b: DEC-0007, verdict: contradiction, note: "obowiązkowa vs opcjonalna rejestracja"}
  - {a: RULE-0003, b: DEC-0004, verdict: compatible, note: "inny segment klientów"}
```
Mierzymy osobno:
1. **Matcher przy ekstrakcji** (`area_matches` + `SPRZECZNOŚĆ:`): czy sprzeczny kandydat jest oznaczony. Cel z planu: ≥ 80% bez wzrostu duplikatów. Sprawdź też, czy `area_matches` nie zawyża kosztu tokenów.
2. **`conflict-scan`**: czy znana para trafia do `pairs.json` (recall doboru par) i ile par do osądu przypada na atom (koszt).
3. **`kb-conflict-judge`**: zgodność werdyktu z oznaczeniem człowieka (precyzja i recall dla `contradiction`; ile `unclear`). Szczególnie pary międzytypowe i „różne słowa, ta sama rzecz”.
4. **Rekomendacja „zastąp”**: ile razy rekomendacja skryptu zgadza się z decyzją człowieka w przeglądzie.
Do napisania, gdy zestaw będzie istniał: `./kb eval-conflicts` (porównanie `verdicts.json` i matcher z gold-conflicts). Do tego czasu liczymy ręcznie.

### Pozostałe
- Ekstrakcja (kb-extractor, kb-matcher) na 2–3 nagraniach oznaczonych od zera i 1 z protokołu (jak wyżej). Cel: przegląd < 15 min na godzinę rozmowy, duplikaty < 5%.
- Partie (`/kb-collect`): ta sama decyzja w kilku źródłach (`same_as`) i sprzeczne źródła w jednej partii.
- Rejestr osób: czy dopytywanie o mówców (`person similar/add/alias`) nie tworzy duplikatów i czy mandat nigdy nie jest nadawany bez decyzji człowieka.
- `/kb-capture`: wierność protokołu (kb-summarizer + kb-verifier) na prawdziwej rozmowie.
- `/kb-compile`: wierność syntez i kontrola cytowań na prawdziwych atomach, w tym podobszary.
- Skala: czas i koszt `match-prep`, `conflict-scan --changed` i pełnego skanu na bazie rzędu setek atomów.

