# Dodatki: rzeczy na później

Nic z tego katalogu nie jest aktywne. Kopiujesz plik we wskazane miejsce dopiero wtedy, gdy dochodzisz do odpowiedniego zadania.

| Plik | Kiedy | Gdzie skopiować | Uwaga |
|---|---|---|---|
| `claude-settings-zadanie-7.json` | zadanie 7. | nad `.claude/settings.json` | Hooki wołają `./kb guard` i `./kb post-edit`. Podpinaj dopiero, gdy te komendy istnieją, bo inaczej każdy zapis pliku zakończy się błędem |
| `github-actions-tests.yml` | zadanie 8. | `.github/workflows/tests.yml` | Uruchamia testy (z testem ramy) i `./kb validate` |
| `claude/agents/kb-summarizer.md` | tor dodatkowy: rozmowy z agentem | `.claude/agents/` | Pisze protokół rozmowy nad dosłowną transkrypcją |
| `claude/agents/kb-conflict-judge.md` | tor dodatkowy: sprzeczności | `.claude/agents/` | Ocenia pary atomów pod kątem sprzeczności |
| `claude/skills/kb-capture/` | tor dodatkowy: rozmowy z agentem | `.claude/skills/` | Zapisuje rozmowę z agentem jako źródło (wymaga `kb capture` i komend protokołu) |

Tory dodatkowe (rozmowy z agentem, relacje i sprzeczności) wymagają komend `./kb`, których nie ma w rdzeniu kursu (`capture`, `protocol-*`, `conflict-*`, `relate`). Przed skopiowaniem plików zbuduj je z agentem według własnego planu albo kart toru dodatkowego.
