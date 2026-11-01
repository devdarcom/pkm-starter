# kb-compiler: reguły z uzasadnieniem

Prompt: [`.claude/agents/kb-compiler.md`](../.claude/agents/kb-compiler.md). Agent pisze **szkic strony obszaru** („jak dziś wygląda X”) wyłącznie z paczki atomów. Wołany przez `/kb-compile`. Szkic przechodzi kontrolę cytowań (skrypt) i weryfikatora, a dopiero potem staje się stroną w `areas/`.

| # | Reguła w prompcie | Dlaczego | Co się psuje, gdy ją usuniesz | K/Z |
|---|---|---|---|---|
| 1 | Każda niepusta linia zawiera co najmniej jedno cytowanie `[[ID]]` atomu z paczki, przy zdaniu, które z niego wynika | Strona ma być widokiem na atomy, a nie osobną wiedzą. Skrypt sprawdza to mechanicznie (`compile-check`) | Zdania bez dowodu: to już nie synteza, tylko wypowiedź modelu | K |
| 2 | Wyłącznie treść z paczki: bez wiedzy ogólnej, bez wnioskowania ponad atomy, bez łagodzenia i wzmacniania | Odpowiedzialność za treść ma baza, a nie model | „Dryf”: strona zaczyna mówić więcej niż atomy, a nikt tego nie widzi | Z |
| 3 | Stan obecny tylko z `atoms` (status `integrated`); `history` (zastąpione decyzje, odrzucone alternatywy) trafia wyłącznie do sekcji „Jak do tego doszliśmy” | Zastąpiona decyzja nie obowiązuje. Opisanie jej jako stanu obecnego wprowadza w błąd | Strona twierdzi, że obowiązuje coś, co już zastąpiono | Z |
| 4 | Pojęcia ze słownika linkuj slugiem `[[konto-gościa]]` przy pierwszym użyciu; taki link nie zastępuje cytowania atomu | Autolinkowanie pomaga czytelnikowi, ale nie jest dowodem | Zdanie „zacytowane” samym pojęciem przechodzi kontrolę, choć nie ma dowodu | Z |
| 5 | Nagłówki bez cytowań, bez frontmattera | Frontmatter strony (`compiled_from`, `stale` i inne) wpisuje skrypt `compile-finish` | Model wymyśla własne metadane, a oznaczanie nieaktualności przestaje działać | K |
| 6 | Struktura: W skrócie, sekcje tematyczne (według tematu, nie typu), Otwarte pytania, Jak do tego doszliśmy; pomiń sekcje bez atomów | Czytelnik chce odpowiedzi „jak jest”, a nie spisu atomów według typu | Strona jest listą typów zamiast opisu obszaru | Z |
| 7 | Każdy atom z `atoms` powinien być zacytowany | Pominięty atom to wiedza, która jest w bazie, a nie ma jej na stronie. Skrypt zapisuje nieużyte w polu `uncited` | Strona jest niepełna, a nikt tego nie widzi | Z |
| 8 | Przy błędach ze sprawdzenia lub uwagach weryfikatora popraw tylko wskazane miejsca | Poprawianie całości psuje to, co przeszło kontrolę | Każda poprawka wprowadza nowe błędy w innych miejscach | Z |

**Co wolno dopisać:** ton i język strony (np. dla zarządu albo dla zespołu), preferowaną kolejność sekcji i własne sekcje tematyczne.
