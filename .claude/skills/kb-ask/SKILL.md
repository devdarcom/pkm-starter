---
name: kb-ask
description: Odpowiada na pytania o wiedzę organizacji/projektu wyłącznie na podstawie atomów z bazy, z cytowaniem ID i wersji; obsługuje pytania o historię decyzji. Użyj, gdy użytkownik pyta „co ustaliliśmy…”, „dlaczego…”, „kto odpowiada za…”, „jak było wcześniej…”.
argument-hint: <pytanie>
---

# /kb-ask

1. Wyszukaj: `./kb search "<słowa kluczowe>" --status integrated,under_review --k 10`. Spróbuj 2–3 sformułowań, w tym pojęć ze słownika (`glossary/`, aliasy).
2. Przeczytaj trafne atomy (`./kb show <ID>`). Przy pytaniach o historię:
   - `./kb related <ID>` daje łańcuch `supersedes` / `superseded_by` / `alternatives`,
   - `./kb search … --status superseded,rejected_alternative,corrected` pokazuje dawne stany,
   - `./kb show <ID>@v<N>` pokazuje dawną wersję treści.
3. Odpowiedz:
   - **tylko** na podstawie atomów `integrated` i `under_review`, przy każdym twierdzeniu `[[ID]]` (dla wersji >1 `ID@vN`). Atom `under_review` oznacz wprost: „podstawa zmieniona, czeka na przegląd” (podaj z `history`, co się zmieniło),
   - osobno, jako **„Sygnały niepotwierdzone”**, wymień trafne `tracked` (TRK), jeśli są, z siłą sygnału z pola `signal` (np. „3 dowody z 2 źródeł”),
   - przy decyzjach podaj, kto i kiedy zdecydował oraz czy miał mandat,
   - gdy baza nie zawiera odpowiedzi, powiedz to wprost i wskaż otwarte pytania (`question`), jeśli dotyczą tematu.
4. Nie uzupełniaj wiedzą ogólną ani domysłami. Odpowiedzi **nie zapisujesz** do bazy. Jeśli użytkownik chce ją zachować, zaproponuj `/kb-correct` z akcją `new` (przejdzie przez przegląd).
