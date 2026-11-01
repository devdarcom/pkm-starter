---
name: kb-lint
description: Przegląd zdrowia bazy wiedzy – walidacja, fakty do potwierdzenia, pytania po terminie, sygnały TRK do awansu, nieaktualne syntezy, zalegające changesety. Użyj okresowo lub gdy użytkownik pyta o stan bazy.
---

# /kb-lint

1. `./kb lint` zwraca raport w Markdownie (kod wyjścia 1 oznacza błędy walidacji).
2. Przedstaw go zwięźle, od najpilniejszych:
   - **błędy walidacji**: wskaż plik i konkretną poprawkę,
   - **under_review** (podstawa zmieniona): dla każdego pokaż, od czego zależy i co się zmieniło. Nadal obowiązuje: `./kb confirm <ID>`. Przestało: `/kb-correct`,
   - **otwarte sprzeczności**: pokaż oba atomy obok siebie i zapytaj, która wersja obowiązuje. Zmiana świata: `/kb-correct` (supersede). Model się mylił: `/kb-correct` (correct lub deprecate). Fałszywy alarm lub rozstrzygnięcie poza bazą: `./kb conflict-dismiss <ID> <CEL> "powód"`,
   - **fakty po `review_by`**: zapytaj, czy nadal aktualne. Tak: `./kb confirm <ID>`. Nie: `/kb-correct` (deprecate lub supersede),
   - **sygnały TRK z ≥ 2 dowodami**: zaproponuj awans przez `/kb-correct` (`promote`),
   - **syntezy do przebudowy** i obszary bez syntezy: `/kb-compile <obszar>`,
   - **changesety > 7 dni**: przypomnij o przeglądzie,
   - ostrzeżenia o pojęciach bez hasła: przy następnej ekstrakcji powinny trafić do słownika.
3. Opcjonalnie (gdy użytkownik chce głębszy przegląd): dla każdej strony w `areas/` uruchom `./kb compile-prep <obszar>` i `kb-verifier` na stronie i paczce, a potem zgłoś rozjazdy.
4. Niczego nie naprawiaj automatycznie. Zaproponuj kroki i wykonaj je dopiero po zgodzie.

## `/kb-lint --deep` – sprzeczności wśród atomów w bazie
Kosztuje wywołania modelu, więc nie jest częścią zwykłego lintu. Szuka par, które nigdy nie trafiły razem do matchera.
1. `./kb conflict-scan [obszar] [--max N] [--changed]` zapisuje `.kb/work/scan/pairs.json` (pary zintegrowanych decyzji, reguł lub faktów (także różnych typów) z tego samego obszaru, podobne tekstowo, jeszcze nieosądzone). Jeśli `pairs` = 0, powiedz to i zakończ. Jeśli `over_max` > 0, wspomnij, że reszta czeka na kolejny przebieg. `--changed` ogranicza skan do atomów nowych lub zmienionych od ostatniego skanu (po `/kb-apply` i `./kb bump`); pierwszy przebieg bez zapisanego stanu obejmuje wszystko. Pełny skan bez `--changed` ma sens rzadko: po zmianie promptów albo jako przegląd okresowy.
2. Wywołaj `kb-conflict-judge` z `pairs.json` i `.kb/work/scan/verdicts.json`.
3. `./kb conflict-scan --record .kb/work/scan/verdicts.json`. Pary `compatible` są zapamiętane (nie wrócą, dopóki któryś atom się nie zmieni). Wynik `to_review` to pary do decyzji człowieka.
4. Dla każdej pary z `to_review` pokaż oba atomy i notę sędziego, a potem zapytaj (AskUserQuestion):
   - **sprzeczne, rozstrzygam później** → `./kb conflict-mark <A> <B> "uzasadnienie"` (zapisuje `contradicts`, para trafia do sekcji „Otwarte sprzeczności”),
   - **sprzeczne i wiem, która obowiązuje** → `/kb-correct` (supersede działa także między typami, np. decyzja zastępuje regułę; alternatywy: correct lub deprecate jednej ze stron); nie trzeba wcześniej robić `conflict-mark`,
   - **nie sprzeczne** → `./kb conflict-mark <A> <B> "dlaczego" --no` (zapamiętane lokalnie w `.kb/`, bez commitu).
5. Podsumuj liczby: ocenione pary, zgodne, oznaczone, do późniejszej decyzji.
