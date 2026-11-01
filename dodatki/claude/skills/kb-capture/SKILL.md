---
name: kb-capture
description: Zapisuje rozmowę z agentem (bieżącą lub wcześniejszą sesję Claude Code) jako źródło bazy wiedzy – dosłowna transkrypcja z logu sesji jako dowód plus zatwierdzony przez człowieka protokół ustaleń jako czytelna mapa. Użyj, gdy użytkownik mówi „zapisz tę rozmowę do bazy”, „przechwyć ustalenia z tej sesji”.
argument-hint: "[od czego zacząć, np. fragment wiadomości] [do czego]"
---

# /kb-capture

Rozmowa trafia do bazy w dwóch warstwach:
- **transkrypcja**: dosłownie z logu sesji (`./kb capture`), a nie z pamięci. To ona jest dowodem.
- **protokół**: co ustalono, co odrzucono, fakty i otwarte kwestie. Każdy punkt linkuje do fragmentów transkrypcji, a **Ty go zatwierdzasz**.

Zasada: **wynik rozmowy z modelem jest ustaleniem człowieka (`me` z `kb.yaml`), nie modelu.**

## 1. Transkrypcja
1. **Zakres.** Domyślnie cała bieżąca sesja. Gdy ustalenia dotyczą części rozmowy, ustal z użytkownikiem fragment pierwszej i ostatniej wiadomości zakresu. `--from` i `--to` działają z dokładnością do pojedynczej wiadomości (także Claude'a), więc podaj fragment dokładnie tej wiadomości, od której/na której zakres ma się zaczynać/kończyć.
   - inne sesje: `./kb capture --list`, potem `--session <id>`.
2. **Podgląd:** `./kb capture [--session ID] [--from "…"] [--to "…"] --dry-run`. Pokaż datę, liczbę wiadomości, pierwszą i ostatnią. Zaproponuj krótki tytuł opisujący temat.
3. **Zapis:** to samo polecenie bez `--dry-run`, z `--title "…"`. Zapamiętaj `id` źródła.

## 2. Protokół
4. `./kb protocol-prep <SRC>` zwraca `pack` i `draft`.
5. Uruchom `kb-summarizer`:
   > Paczka: `<pack>`. Zapisz szkic do: `<draft>`.
6. `./kb protocol-check <SRC>`. Przy błędach (punkt bez linku, nieistniejący fragment, zła sekcja) odeślij je do `kb-summarizer` (maks. 2 rundy).
7. Uruchom `kb-verifier`:
   > Szkic: `<draft>`. Materiał: `<pack>`.

   Problemy odeślij raz do `kb-summarizer`, a potem powtórz krok 6.
8. **Zatwierdzenie.** Pokaż użytkownikowi protokół w całości (sekcje i punkty bez linków, dla czytelności) oraz uwagi weryfikatora, jeśli zostały. Zapytaj, czy zatwierdza. Poprawki wprowadza `kb-summarizer` albo użytkownik bezpośrednio w pliku `<draft>`; po zmianach wróć do kroku 6.
9. Po zatwierdzeniu: `./kb protocol-finish <SRC>` wstawia protokół do źródła nad transkrypcją i commituje z `Approved-by`.

## 3. Dalej
10. Zaproponuj `/kb-extract <SRC>` (samodzielnie albo z innymi źródłami, `--pending`). Ekstraktor dostaje protokół jako mapę ustaleń, a cytaty bierze z transkrypcji.
11. Jeśli to źródło ma posłużyć do pomiaru jakości: `./kb protocol-gold <SRC>` tworzy **szkic** wzorca w `eval/gold/`, który trzeba przejrzeć (patrz `/kb-eval`).

Pomijane przy zapisie transkrypcji: wywołania narzędzi, myślenie modelu, subagenci i tagi IDE. Bloki kodu są zastępowane znacznikiem. Ten sam zakres zapisany drugi raz zostanie odrzucony jako duplikat.

Rozmowa trafia do repozytorium tak jak inne źródła. Przed zapisem upewnij się, że nie zawiera danych, których użytkownik nie chce przechowywać.
