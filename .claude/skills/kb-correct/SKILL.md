---
name: kb-correct
description: Przygotowuje ręczny changeset dla zmian spoza źródeł – korekta błędnego atomu, wycofanie, zastąpienie decyzją podjętą poza nagraniem, awans sygnału TRK, poprawka zdania z syntezy. Użyj, gdy użytkownik mówi, że coś w bazie jest błędne, nieaktualne albo chce dopisać wiedzę ręcznie.
argument-hint: <opis zmiany, np. "DEC-0003 źle oddaje źródło – …">
---

# /kb-correct

Najpierw ustal, **co się stało**, bo od tego zależy akcja i uczciwość genealogii:

| sytuacja | akcja | efekt |
|---|---|---|
| atom źle oddaje źródło (**model się mylił**) | `correct` (+ opcjonalnie poprawiona treść) | stary atom: `corrected` z `correction_reason`; nowy atom z `corrects` albo brak następcy |
| **świat się zmienił** (nowa decyzja lub stan) | `supersede` (+ nowa treść, `reason` = supersede_reason) | stary atom: `superseded`; nowy atom z `supersedes` |
| przestało obowiązywać, bez następcy | `deprecate` | `deprecated` z powodem |
| wiedza bez źródła w bazie (np. ustalenie mailowe) | `new` | nowy atom z dowodem `changeset` (najlepiej jednak dodać źródło przez /kb-ingest) |
| sygnał TRK się potwierdził | `promote` (typ nowego atomu może być inny niż typu TRK) | nowy atom, TRK usunięty, dowody przeniesione |

Jeśli to korekta zdania z syntezy w `areas/`, znajdź cytowane atomy i popraw **je**, a nie stronę.

Zmiana (`supersede`, `correct`, `deprecate`) atomu, od którego inne atomy zależą (`depends_on`, `refines`), odeśle je do `under_review`. `./kb check` pokaże je przed zatwierdzeniem (`will_be_under_review`).

Kroki:
1. Przeczytaj dotknięte atomy (`./kb show <ID>`, `./kb related <ID>`). Jeśli nie wiadomo, czy to `correct`, czy `supersede`, zapytaj.
2. Zapisz `.kb/work/manual-<data>.json`:
   ```json
   {"proposals": [
     {"action": "correct", "target": "RULE-0001", "reason": "na czym polegał błąd",
      "title": "poprawiony tytuł", "sections": {"Reguła": "…"}, "decided_by": "ja"},
     {"action": "new", "type": "decision", "title": "…", "sections": {"Kontekst": "…", "Decyzja": "…"},
      "areas": ["…"], "decided_by": "anna-k", "scope": "team", "valid_from": "2026-10-30",
      "evidence_note": "mail od Anny z 30.10"}
   ]}
   ```
   Przy `correct` bez następcy pomiń `sections`. Nowy atom może mieć `"depends_on": ["DEC-0001"]` i `"refines": ["RULE-0002"]` (tylko obowiązujące atomy). Relację dla istniejącego atomu dopisuje `./kb relate <ID> depends_on|refines <CEL>` (usuwanie: `--remove`).
3. `./kb manual .kb/work/manual-<data>.json --name <data>-<krótki-opis>` tworzy `inbox/CS-….md`.
4. Pokaż ścieżkę. Użytkownik przegląda changeset i zaznacza decyzje, a potem uruchamia `/kb-apply`.

Drobne poprawki **treści** bez zmiany sensu nie wymagają changesetu: wystarczy edycja w Obsidianie i `git commit -m "kb(edit): …"`. Zmiana sensu treści przy tym samym przedmiocie to edycja i `./kb bump <ID> "opis"`.
