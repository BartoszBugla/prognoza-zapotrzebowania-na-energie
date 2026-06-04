# Skrypt prezentacji — Analiza cen i źródeł energii w Polsce i Europie

> Czas prezentacji: ~12–15 minut
> Wykresy: folder `charts/`

---

## Slajd 1 — Strona tytułowa

**Tytuł:** Analiza cen i źródeł energii w Polsce i Europie

> Dzień dobry. Nazywam się [imię i nazwisko]. Dziś zaprezentuję analizę polskiego rynku energii elektrycznej, ze szczególnym uwzględnieniem cen, miksu energetycznego i porównania z wybranymi krajami Unii Europejskiej.

---

## Slajd 2 — Źródło danych

**Wykres:** brak (tekst + schemat pipeline)

> Dane pochodzą z platformy ENTSO-E Transparency — oficjalnego źródła danych o rynku energii w Europie. Cały proces składa się z trzech etapów: najpierw skrypt ETL pobiera surowe dane godzinowe, następnie przeprowadzam transformację — uzupełniam braki, unifikuję strefy czasowe — a na końcu wykonuję właściwą analizę.
>
> Dla Polski dysponuję danymi z lat 2015–2025 — ponad 96 tysięcy rekordów godzinowych. Dla wybranych krajów europejskich — Niemiec, Francji i Hiszpanii — mam dane od 2020 roku.

---

## Slajd 3 — Co zostało przeanalizowane

**Wykres:** brak (agenda)

> W ramach projektu przeanalizowałem pięć głównych obszarów:
> 1. Ceny energii w Polsce i zjawisko ujemnych cen
> 2. Strukturę miksu energetycznego — przede wszystkim rolę węgla
> 3. Porównanie Polski z innymi krajami UE
> 4. Dekompozycję szeregu czasowego zapotrzebowania
> 5. Analizę statystyczną — czy weekend istotnie obniża zapotrzebowanie
>
> Zacznijmy od cen.

---

## Slajd 4 — Średnia roczna cena prądu

**Wykres:** `charts/01_srednia_roczna_cena.png`

> Na tym wykresie widzimy średnią roczną cenę day-ahead na polskim rynku. Warto zwrócić uwagę na kilka kluczowych momentów.
>
> W latach 2015–2016 ceny były niskie — około 35–37 euro za megawatogodzinę. W 2017 nastąpił gwałtowny skok do 136 euro, a w 2018–2019 ceny osiągnęły rekordowe poziomy powyżej 200 euro. Było to efektem rosnących cen uprawnień do emisji CO2 i drożejącego węgla.
>
> Pod koniec 2019 Polska przystąpiła do rynkowego łączenia cen (market coupling), co natychmiast obniżyło ceny. Rok 2020 to pandemia — spadek zapotrzebowania i najniższe ceny od lat: 47 euro.
>
> Potem mamy kryzys energetyczny 2021–2022, a od 2023 roku widoczna jest stabilizacja w okolicach 100 euro, z trendem spadkowym — częściowo dzięki rosnącej roli OZE.

---

## Slajd 5 — Rozrzut cen (boxplot)

**Wykres:** `charts/02_cena_boxplot.png`

> Ten boxplot pokazuje coś, czego nie widać na prostym wykresie średnich — rozrzut cen w ciągu roku.
>
> Zwróćcie uwagę na lata 2018–2019: nie tylko średnia jest wysoka, ale wąsy rozciągają się powyżej 800–1000 euro. Oznacza to, że zdarzały się godziny ekstremalnie wysokich cen.
>
> Z kolei od 2023 roku po raz pierwszy widzimy wąsy poniżej zera — to zjawisko ujemnych cen, o którym powiem za chwilę.
>
> Mediana (linia w środku pudełka) jest zwykle niższa od średniej, co wskazuje na prawostronne skrzywienie rozkładu — pojedyncze szczyty cenowe podnoszą średnią.

---

## Slajd 6 — Ujemne ceny energii (fotowoltaika)

**Wykres:** `charts/03_ujemne_ceny.png`

> To jedno z najbardziej fascynujących zjawisk na współczesnym rynku energii. Od 2023 roku na polskim rynku pojawiają się godziny z ujemną ceną — w 2023 było ich 43, w 2024 już prawie 200, a w 2025 ponad 310.
>
> Prawy panel pokazuje, kiedy to się dzieje — zdecydowanie dominują godziny 10–15, czyli szczyt produkcji fotowoltaicznej. W uproszczeniu: w słoneczne dni produkujemy więcej prądu niż potrafimy zużyć, a konwencjonalne bloki energetyczne nie mogą się wystarczająco szybko wyłączyć, więc producenci dosłownie płacą za odbiór energii.
>
> To zjawisko znacząco obniża średnią roczną cenę i jest bezpośrednim efektem szybkiego rozwoju PV w Polsce.

---

## Slajd 7 — Czy Polska jest eko? Mix energetyczny

**Wykres:** `charts/04_mix_energetyczny.png`

> Przejdźmy do kluczowego pytania: jak wygląda transformacja energetyczna w Polsce?
>
> Ten wykres skumulowany pokazuje ewolucję miksu energetycznego na przestrzeni 10 lat. W 2015 roku węgiel stanowił 83% produkcji — Polska była jednym z najbardziej uzależnionych od węgla krajów w Europie.
>
> W 2024 ten udział spadł do 55% — nadal dużo, ale trend jest wyraźny. Widać rosnący udział wiatru i fotowoltaiki. Wiatr wzrósł z 7% do 15%, a PV — z zera do 11%.
>
> Rok 2025 jest niepełny w danych, ale widać dalsze przyspieszenie — udział węgla spadł do około 40%.

---

## Slajd 7b — Spadek produkcji z węgla (opcjonalny)

**Wykres:** `charts/05_wegiel_trend.png`

> Jeśli spojrzymy na produkcję z węgla w wartościach bezwzględnych — spadek jest jeszcze bardziej dramatyczny. Z 128 TWh w 2015 do 89 TWh w 2024 — to redukcja o 30%.
>
> Prawy panel porównuje profil miesięczny: w 2015 węgiel pracował na stałym, wysokim poziomie przez cały rok. W 2024 widzimy wyraźną sezonowość — mniej węgla latem, gdy PV i wiatr dostarczają więcej energii.

---

## Slajd 8 — Polska na tle UE

**Wykres:** `charts/07_polska_vs_ue.png` + `charts/08_ceny_ue_roczne.png`

> Jak Polska wypada na tle Unii? Porównałem średnie ceny i zużycie energii dla Polski, Francji i Hiszpanii w latach 2020–2024. Dla Niemiec niestety nie mam danych cenowych w tym zbiorze.
>
> Polska z ceną 102 euro jest tańsza niż Francja (114 euro), ale droższa od Hiszpanii (93 euro). Pod względem zużycia Polska konsumuje około 168 TWh rocznie — znacznie mniej niż Niemcy (479 TWh) czy Francja (442 TWh).
>
> Na drugim wykresie widać, jak ceny roczne zmieniały się w poszczególnych krajach. Charakterystyczny jest wspólny skok w 2022 roku (kryzys energetyczny), a potem konwergencja cen w 2023–2024 — efekt integracji europejskiego rynku energii.

---

## Slajd 9 — Dekompozycja szeregu czasowego

**Wykres:** `charts/09_dekompozycja.png`

> Teraz przechodzimy do bardziej zaawansowanej analizy. Zastosowałem addytywną dekompozycję szeregu czasowego na dziennym zapotrzebowaniu.
>
> Pierwszy panel to surowe dane — widać dużą zmienność. Drugi panel izoluje trend — wyraźnie widać rosnące zapotrzebowanie do 2019, gwałtowny spadek w 2020 (pandemia COVID-19, zaznaczona na czerwono), odbicie w 2021–2022, a następnie ponowny spadek.
>
> Trzeci panel to sezonowość roczna — piękne, regularne fale odpowiadające zimowym szczytom i letnim spadkom zapotrzebowania. Czwarty to reszty — anomalie, które nie pasują do trendu ani sezonowości.

---

## Slajd 10 — Wartości odstające: święta i anomalie

**Wykres:** `charts/10_swieta_zapotrzebowanie.png`

> Na wykresie zapotrzebowania dziennego dla roku 2024 nałożyłem daty polskich świąt państwowych. Czerwone linie przerywane oznaczają Nowy Rok, Trzech Króli, Święto Pracy, Konstytucję 3 Maja, Wniebowzięcie NMP, Dzień Niepodległości i Boże Narodzenie.
>
> Widać, że każde święto powoduje wyraźny spadek zapotrzebowania — porównywalny z weekendowym. To ważna informacja dla operatorów sieci i traderów energii, którzy muszą przewidywać takie spadki.
>
> Warto też zauważyć ogólną sezonowość — wyższe zapotrzebowanie zimą (styczeń, grudzień) i niższe latem.

---

## Slajd 11 — Weekend vs dzień roboczy

**Wykres:** `charts/11_weekend_vs_roboczy.png`

> Czy w weekend zapotrzebowanie jest istotnie niższe? Intuicyjnie — tak, bo większość przemysłu nie pracuje. Ale sprawdźmy to danymi.
>
> Boxplot po lewej jasno pokazuje różnicę — mediana weekendowa jest niższa. Prawy panel to profil dobowy: w dzień roboczy mamy wyraźny szczyt o 10–12, podczas gdy weekend jest spłaszczony i przesunięty.
>
> Średnie zapotrzebowanie w dzień roboczy to około 19 860 MW, w weekend — 16 930 MW. To różnica prawie 15%.

---

## Slajd 12 — Test statystyczny

**Wykres:** `charts/12_test_statystyczny.png`

> Ale czy ta różnica jest statystycznie istotna? Użyłem testu Mann-Whitney U, ponieważ rozkłady nie są normalne — co potwierdziłem testem Shapiro-Wilka.
>
> Wynik jest jednoznaczny: p-value wynosi praktycznie zero. Odrzucamy hipotezę zerową o braku różnicy. Cohen's d wynosi 1,07, co oznacza duży rozmiar efektu.
>
> Na wykresie widzimy średnie z 95-procentowymi przedziałami ufności — są tak wąskie, że ledwo widoczne, co wynika z ogromnej liczby obserwacji (ponad 96 tysięcy godzin).
>
> Podsumowując: zapotrzebowanie w weekend jest statystycznie istotnie i merytorycznie znacząco niższe niż w dni robocze.

---

## Slajd 13 — Podsumowanie

> Podsumowując najważniejsze wnioski:
>
> **Po pierwsze** — transformacja energetyczna w Polsce postępuje. Udział węgla spadł z 83% do 55% w ciągu dekady, ale węgiel wciąż dominuje.
>
> **Po drugie** — rozwój OZE, zwłaszcza fotowoltaiki, powoduje nowe zjawiska rynkowe, takie jak ujemne ceny energii. To wymusza modernizację systemu — potrzebujemy magazynów energii.
>
> **Po trzecie** — ceny na polskim rynku są wrażliwe na wydarzenia geopolityczne i regulacyjne. Integracja rynkowa z UE (coupling 2019) obniżyła ceny, ale kryzys 2022 pokazał podatność na szoki zewnętrzne.
>
> **Po czwarte** — zapotrzebowanie ma silną strukturę sezonową i tygodniową, co jest potwierdzone statystycznie. Święta państwowe zachowują się jak weekendy.

---

## Slajd 14 — Dziękuję za uwagę

> Dziękuję za uwagę. Chętnie odpowiem na pytania.
>
> Cały kod analityczny jest dostępny w notebooku `_analiza2.ipynb`, a pipeline danych w `_etl.ipynb` i `_data-transformation.ipynb`.

---

## Mapowanie slajdów na wykresy

| Slajd | Temat | Wykres do wstawienia |
|-------|-------|---------------------|
| 1 | Tytuł | brak |
| 2 | Źródło danych | brak (tekst) |
| 3 | Agenda | brak (tekst) |
| 4 | Średnia roczna cena | `01_srednia_roczna_cena.png` |
| 5 | Rozrzut cen | `02_cena_boxplot.png` |
| 6 | Ujemne ceny / PV | `03_ujemne_ceny.png` |
| 7 | Mix energetyczny | `04_mix_energetyczny.png` |
| 7b | Węgiel trend (opcja) | `05_wegiel_trend.png` |
| 8 | Polska vs UE | `07_polska_vs_ue.png` + `08_ceny_ue_roczne.png` |
| 9 | Dekompozycja | `09_dekompozycja.png` |
| 10 | Święta / anomalie | `10_swieta_zapotrzebowanie.png` |
| 11 | Weekend vs roboczy | `11_weekend_vs_roboczy.png` |
| 12 | Test statystyczny | `12_test_statystyczny.png` |
| 13 | Podsumowanie | brak (tekst) |
| 14 | Zakończenie | brak |

**Dodatkowe wykresy w rezerwie:**
- `06_oze_vs_cena.png` — scatter OZE% vs cena (do wstawienia jeśli ktoś zapyta o korelację OZE-cena)
- `13_rozklady.png` — histogramy i boxploty ceny/loadu (do wstawienia jeśli pytanie o normalność)
- `14_roczne_zuzycie.png` — roczne zużycie (do wstawienia na slajdzie o trendzie loadu)
