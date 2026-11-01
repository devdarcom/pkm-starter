---
name: kb-apply
description: Stosuje przejrzany changeset z /inbox – tworzy i aktualizuje atomy, słownik i action itemy, waliduje i commituje z trailerem zatwierdzającego.
argument-hint: <CS-id>
disable-model-invocation: true
---

# /kb-apply

To bramka zatwierdzenia. Uruchamia się tylko na wyraźne polecenie użytkownika.

1. Bez argumentu wypisz otwarte changesety (`ls inbox/CS-*.md`) i zapytaj, który zastosować.
2. Sprawdzenie na sucho: `./kb check <CS-id>`.
   - Jeśli są `errors`, pokaż je w czytelnej formie (propozycja → co poprawić) i **zakończ**. Changeset poprawia użytkownik. Ty możesz go edytować tylko na jego wyraźną prośbę i nigdy nie zaznaczasz decyzji za niego.
   - Pokaż podsumowanie decyzji (`przyjmij` / `jako nowy` / `śledź` / `odrzuć`).
   - Jeśli `will_be_under_review` nie jest puste, pokaż **przed zatwierdzeniem**, które atomy trafią do przeglądu i z czyjej podstawy (promień rażenia). To tylko informacja, ale daje człowiekowi szansę zmienić decyzję.
3. `./kb apply <CS-id>`. Polecenie odmówi działania, jeśli w `atoms/`, `glossary/` lub `areas/` są niezacommitowane zmiany. Wtedy podpowiedz `git commit -m "kb(edit): …"` (kosmetyka) albo `./kb bump <ID> "opis"` (zmiana znaczenia).
4. Zgłoś log zmian (nowe ID, zastąpienia, awanse), `under_review` (atomy do przeglądu: `./kb confirm <ID>`, jeśli nadal obowiązują, albo `/kb-correct`), commit oraz `stale_areas`. Dla nieaktualnych syntez zaproponuj `/kb-compile <obszar>`.
5. Jeśli powstały action itemy, wspomnij, że trafiły do `actions/inbox.md`.
6. **Sprzeczności z nowymi atomami.** Uruchom `./kb conflict-scan --changed` (tylko atomy nowe lub zmienione od ostatniego skanu, więc koszt nie rośnie z bazą). Jeśli `pairs` = 0, nic nie mów. Jeśli > 0, zapytaj, czy ocenić je teraz (kroki 2–5 sekcji „/kb-lint --deep” w `.claude/skills/kb-lint/SKILL.md`: `kb-conflict-judge`, `--record`, decyzje człowieka). Odmowa jest w porządku: pary wrócą przy `/kb-lint --deep`.
