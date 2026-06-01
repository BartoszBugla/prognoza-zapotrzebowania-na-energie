# Prognozowanie zapotrzebowania na energię — Hiszpania (2015–2018)

Praca zaliczeniowa: **Analiza i wizualizacja danych – Pandas, DataFrame**  
Uczelnia: Merito Chorzów | Zespół: Dawid Hetmańczyk (126674), Bartosz Bugla (180737)

## Pliki do oddania

| Plik | Opis |
|------|------|
| `analiza.ipynb` | Główna analiza (Pandas) |
| `docs/raport.docx` | Raport |
| `docs/prezentacja.pptx` | Prezentacja |
| `datasets/` | Dane CSV |

Opcjonalnie (poza Pandas): `etl.ipynb`, `uczenie-maszynowe-projekt.ipynb`

## Uruchomienie

1. Otwórz `analiza.ipynb`
2. **Run All** — pierwsza komórka kodu zainstaluje pakiety z `requirements.txt`
3. Gotowe

Ręcznie (jeśli wolisz terminal):

```powershell
pip install -r requirements.txt
```

## Dane

[Kaggle – Energy Consumption, Generation, Prices and Weather](https://www.kaggle.com/datasets/nicholasjhana/energy-consumption-generation-prices-and-weather)

## Regeneracja raportu / prezentacji

Skrypt buduje pełny raport Word (~10 rozdziałów, 8 wykresów) oraz prezentację PowerPoint (~25 slajdów) z **aktualnych wyników analizy**:

```powershell
.\.venv\Scripts\python scripts\build_docs.py
```

Wynik: `docs/raport.docx`, `docs/prezentacja.pptx`, `docs/figures/*.png`

## Oddanie

Udostępnić repozytorium prowadzącej na GitHub: **akkosan** (lub folder OneDrive sekcji).
