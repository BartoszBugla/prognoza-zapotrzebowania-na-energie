# ⚡ Transformacja Energetyczna Polski (2015–2024)

> **Projekt zaliczeniowy:** Analiza i wizualizacja danych – Pandas, DataFrame  
> **Uczelnia:** Uniwersytet WSB Merito Chorzów  
> **Zespół:** Dawid Hetmańczyk (126674), Bartosz Bugla (180737)

Projekt analizuje ewolucję polskiego rynku energii w oparciu o dane z ENTSO-E. Przedstawia transformację z energetyki węglowej w stronę odnawialnych źródeł (OZE) i ukazuje bieżące wyzwania rynkowe (m.in. ujemne ceny energii i zjawisko *duck curve*).

## 🗂️ Struktura
- **`_etl.ipynb`** – pobieranie danych z API ENTSO-E.
- **`_data_transformation.ipynb`** – czyszczenie i konsolidacja danych.
- **`_analysis.ipynb`** – główna analiza, wizualizacje (Plotly) i mapy interaktywne (Folium).
- **`datasets/`** – surowe i przetworzone dane w formacie CSV.

## 🚀 Szybki start

Projekt używa szybkiego menedżera pakietów **[uv](https://github.com/astral-sh/uv)**.

```bash
# 1. Instalacja zależności środowiska
uv sync

# 2. Konfiguracja API (podaj swój klucz z ENTSO-E w pliku .env)
cp .env.example .env

# 3. Uruchomienie środowiska Jupyter
uv run --with jupyter jupyter lab
```