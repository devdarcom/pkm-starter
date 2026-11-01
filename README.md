# PKM: repozytorium startowe kursu

Budujesz własny system bazy wiedzy z atomów: transkrypcje i notatki zamieniają się w audytowalną wiedzę (decyzje, reguły, fakty, pytania, pojęcia), z cytatem i wskaźnikiem do źródła. Markdown jest źródłem prawdy, Obsidian służy do czytania i przeglądu, git daje audyt, a Claude Code robi pracę wymagającą rozumienia tekstu. Kod (`tools/kb/`) piszesz sam, z agentem, w kolejnych zadaniach.

## Jak zacząć

1. **Utwórz własne repozytorium z tego szablonu** i ustaw je jako **prywatne**. Odpowiadasz za to, co w nim trzymasz: za dane, dostęp i zgody na materiały z pracy.
2. **Wymagania:** Python 3.9+, git, Claude Code, Obsidian (do przeglądu changesetów).
3. `pip install -r requirements.txt`
4. Uruchom testy: `python3 -m unittest discover -s tests -t .` Na starcie wszystko ma być zielone.
5. W `kb.yaml` i `schema/people.yaml` wpisz siebie (ten sam slug w obu plikach).
6. Zadanie 1 zacznij po pierwszym spotkaniu. Numer bieżącego zadania trzymasz w `zadanie.txt`.

## Co jest w repozytorium

| Ścieżka | Co to |
|---|---|
| `CLAUDE.md` | złote zasady i zasady pracy z agentem; agent czyta go w każdej sesji |
| `DLACZEGO.md` | dlaczego każdy element ramy jest taki, a nie inny |
| `rama.yaml` | manifest ramy: elementy, rodzaj (kontrakt albo zalecane), od którego zadania |
| `odstepstwa.yaml` | Twoje świadome odstępstwa od ramy (zatwierdzasz je sam) |
| `zadanie.txt` | numer bieżącego zadania; elementy z późniejszych zadań nie są jeszcze sprawdzane |
| `schema/` | typy atomów, statusy, relacje, pola zarządzane; obszary i osoby |
| `.claude/agents/`, `.claude/skills/` | prompty agentów i skille `/kb-*` (baza reguł, możesz dopisać swoją domenę) |
| `prompty-z-adnotacjami/` | te same prompty z komentarzem, jaką porażkę zapobiega każda reguła |
| `.githooks/commit-msg` | hook git (podpinasz w zadaniu 2.) |
| `kb` | launcher: uruchamia `python3 -m kb.cli`; kod w `tools/kb/` piszesz Ty |
| `tests/` | szkielet testów (`helpers.py`) i test ramy (`tests/rama/`) |
| `dodatki/` | rzeczy na później: hooki Claude Code (zadanie 7.), szablon CI (zadanie 8.), tory dodatkowe (rozmowy z agentem, sprzeczności) |
| `sources/`, `inbox/`, `atoms/`, `glossary/`, `areas/`, `actions/`, `eval/` | dane bazy; w większości zapisują je narzędzia, nie Ty |

## Jak działa rama

Kurs prowadzi tą samą drogą, jaką zbudowano ten system, a jednocześnie daje każdemu **działający wynik w skończonym czasie**.

- **Kontrakty (sztywne tylko tam, gdzie muszą):** układ katalogów, format atomu i changesetu, komendy `./kb`, format wyjścia agentów. Na nich opierają się testy odbiorcze, pokazy i plan B.
- **Zalecane:** reszta (zasady, reguły w promptach, hooki, konwencje, testy, CI, pętla PKM). Dostajesz wersję startową z uzasadnieniem w `DLACZEGO.md`.
- **Odstępstwa są dozwolone i zatwierdzasz je sam.** Dopisz wpis do `odstepstwa.yaml` (`element`, `powod`, `skutek`, `jak_sprawdzam`, wszystkie niepuste). Test ramy wymaga wpisu tylko wtedy, gdy element jest zmieniony albo go brakuje.
- **Ścieżka standardowa mieści się w czasie zadania, odstępstwo zwykle nie.** Plan B zawsze masz: tag `spotkanie-N` w repozytorium wzorcowym.

## Skille a komendy spoza rdzenia kursu

Skille `/kb-*` pochodzą z pełnego systemu i wołają komendy, które w kursie powstają stopniowo (kontrakt każdej z nich jest na karcie zadania). Kilka z nich wykracza poza rdzeń: `person`, `speakers` (rejestr osób i mapowanie mówców), `conflict-scan`, `conflict-mark`, `conflict-dismiss` i `relate` (sprzeczności i relacje), `protocol-gold`, `eval-conflicts`, `stats`, `manual`, `bump` i `confirm`. Gdy skill używa komendy, której jeszcze nie zbudowałeś, przeczytaj ten krok, pomiń go albo zbuduj komendę z agentem. To normalne, a nie błąd repozytorium.

## Prompt startowy zadania

Każde zadanie zaczynasz od tego promptu (wstaw numer zadania):

```
Przeczytaj CLAUDE.md i kartę zadania N. Złote zasady obowiązują, chyba że odstepstwa.yaml mówi inaczej.
1. Zaproponuj plan: pliki, komendy ./kb, co robi skrypt, a co model. Poczekaj na moją akceptację.
2. Zaimplementuj to w tools/kb/. Nie zmieniaj plików ramy (lista w rama.yaml).
3. Napisz testy tego, co zbudowałeś (unittest, szkielet w tests/helpers.py).
4. Uruchom komendę odbioru z karty i testy, pokaż wynik.
```

## Pętla PKM (od zadania 5.)

W każdym tygodniu pracy własnej uruchom całą pętlę na 2–3 nowych własnych źródłach (20–30 minut): `/kb-collect`, `/kb-extract`, przegląd w Obsidianie, `/kb-apply`, `./kb lint`, `/kb-compile --stale`. Dzięki temu do zadań 8. i 9. (eval i UI) masz prawdziwą bazę.

## Prywatność

Surowe źródła trafiają do repozytorium (`sources/raw/`), a usunięcie czegokolwiek z historii gita wymaga jej przepisania. Dlatego decyduj z góry, jakich materiałów używasz. Na kanale kursu i w nagraniach wklejaj wyłącznie dane zanonimizowane albo przykładowe.
