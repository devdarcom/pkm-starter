---
name: kb-compile
description: Kompiluje stronę obszaru w /areas (synteza „jak dziś wygląda X”) z atomów integrated, z cytowaniem ID przy każdym zdaniu i weryfikacją wierności. Użyj, gdy lint lub apply zgłosi nieaktualną syntezę albo użytkownik prosi o stronę obszaru.
argument-hint: <obszar>… | --stale
---

# /kb-compile

Argumenty: jeden lub kilka obszarów (`produkt journey`) albo `--stale`. Dla `--stale` weź listę z `./kb compile-stale` (flaga stale, brak strony, zmieniony zbiór atomów); pusta lista = „nic do przebudowy”. Nieznany obszar zgłoś przed startem i pomiń.

Dla wielu obszarów: krok 1 wykonaj dla wszystkich, potem kroki 2 i 4 uruchamiaj równolegle (jeden `kb-compiler`/`kb-verifier` na obszar, wszystkie w jednej wiadomości). Kroki 3 i 5 wykonuj osobno dla każdego obszaru, po kolei (każdy `compile-finish` to osobny commit). Błąd jednego obszaru nie zatrzymuje pozostałych. Pytanie o publikację (krok 4) zadaj raz, zbiorczo.

Dla każdego obszaru:

1. `./kb compile-prep <obszar>` zwraca `pack` i `draft`.
2. Uruchom `kb-compiler`:
   > Paczka: `<pack>`. Zapisz szkic do: `<draft>`.
3. `./kb compile-check <obszar>`. Przy błędach (linia bez cytowania, ID spoza paczki) odeślij je do `kb-compiler` (maks. 2 rundy).
4. Uruchom `kb-verifier`:
   > Szkic: `<draft>`. Paczka: `<pack>`.

   Jeśli zgłosi problemy, odeślij je do `kb-compiler` raz, a potem powtórz krok 3. Problemy, które zostaną po tej rundzie, pokaż użytkownikowi i zapytaj, czy publikować.
5. `./kb compile-finish <obszar>` zapisuje `areas/<obszar>.md` z `compiled_from` (ID@wersja) i commituje.
6. Zgłoś (przy wielu obszarach: tabela obszar → strona, zacytowane, niezacytowane, błędy): ścieżkę strony, liczbę zacytowanych atomów i niezacytowane atomy, jeśli są.

Nigdy nie edytuj `areas/` bezpośrednio, bo blokuje to hook. Poprawki treści idą przez atomy (`/kb-correct`).
