# kb-verifier: reguły z uzasadnieniem

Prompt: [`.claude/agents/kb-verifier.md`](../.claude/agents/kb-verifier.md). Agent sprawdza **wierność** tekstu pochodnego wobec materiału, który ten tekst cytuje: szkicu syntezy obszaru wobec paczki atomów (albo szkicu protokołu rozmowy wobec transkrypcji). Wołany przez `/kb-compile`. **Tylko odczyt.**

| # | Reguła w prompcie | Dlaczego | Co się psuje, gdy ją usuniesz | K/Z |
|---|---|---|---|---|
| 1 | Narzędzie tylko `Read`; „Nie modyfikujesz żadnych plików” | Weryfikator ma być niezależnym sędzią. Gdy może poprawiać, przestaje być sędzią | Weryfikator „naprawia” szkic po cichu, a nikt nie widzi, co zmienił | Z |
| 2 | Sprawdzanie **każdego zdania lub punktu** z cytowaniem | Kontrola cytowań w skrypcie sprawdza tylko, że cytowanie jest. Czy jest trafne, ocenia dopiero weryfikator | Zdanie z poprawnym cytowaniem, ale niezgodne z atomem, przechodzi | Z |
| 3 | Oceny: `OK`, `CZĘŚCIOWO` (dodaje szczegół, uogólnia, wzmacnia lub osłabia), `BRAK` (nie wynika z cytowanego materiału) | Skala jest jawna i da się ją zastosować do każdego zdania. „Czy to zdanie wynika z atomu” ma jedną odpowiedź | Ogólne uwagi („trochę nieścisłe”) bez wskazania zdania | Z |
| 4 | `STATUS`: stan obecny opisany na podstawie atomu zastąpionego lub odrzuconego | To najgroźniejszy błąd syntezy: obowiązuje to, co już nie obowiązuje | Strona podaje nieaktualną decyzję jako obowiązującą | Z |
| 5 | Zwracasz **tylko problemy**, w formacie `- [BRAK] linia 12: „…” – cytuje s14, gdzie jest „…”; proponowana poprawka: „…”` | Kompilator dostaje dokładnie to, co ma poprawić, i może zmienić tylko wskazane miejsca | Długie raporty z `OK` zasłaniają realne problemy | K |
| 6 | Brak problemów: odpowiedz dokładnie `WERYFIKACJA OK` | Skill `/kb-compile` rozpoznaje sukces po tym zdaniu | Skill nie wie, czy szkic przeszedł, i uruchamia kolejne poprawki bez potrzeby | K |
| 7 | Dla protokołu rozmowy dodatkowe oceny `KATEGORIA` i `POMINIĘTE` | Protokół ma pokazywać ustalenia, odrzucone warianty i otwarte kwestie. Ważne ustalenie bez wpisu to utrata wiedzy | Zmienione później ustalenie wisi jako obowiązujące | Z |

**Co wolno dopisać:** nic, co poszerzałoby uprawnienia (zapis, edycja). Można natomiast zaostrzyć kryteria, np. traktować każde `CZĘŚCIOWO` jako błąd blokujący.
