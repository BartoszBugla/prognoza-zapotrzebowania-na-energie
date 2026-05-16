"""
Generuje docs/raport.docx, docs/prezentacja.pptx i docs/figures/.
Uruchom: .venv\\Scripts\\python scripts\\build_docs.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor
from pptx import Presentation
from pptx.dml.color import RGBColor as PptRGB
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches as Inch
from pptx.util import Pt as PptPt
from scipy import stats as sp_stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
FIGURES = DOCS / "figures"

# Kolorystyka
BLUE = PptRGB(21, 101, 192)
GREEN = PptRGB(46, 125, 50)
DARK = PptRGB(38, 50, 56)
GRAY = PptRGB(96, 125, 139)
WHITE = PptRGB(255, 255, 255)
LIGHT = PptRGB(236, 239, 241)

TEAM = {
    "tytul": "Analiza i prognozowanie zapotrzebowania na energię elektryczną w Hiszpanii",
    "przedmiot": "Analiza i wizualizacja danych – Pandas, DataFrame",
    "uczelnia": "Merito Chorzów",
    "rok": "2025/2026",
    "semestr": "3 (letni)",
    "czlonkowie": [
        ("Dawid Hetmańczyk", "126674"),
        ("Bartosz Bugla", "180737"),
    ],
}

sns.set_theme(style="whitegrid")
plt.rcParams.update({"figure.dpi": 150, "font.size": 11, "axes.titlesize": 13})


def load_and_prepare() -> pd.DataFrame:
    energy_df = pd.read_csv(
        ROOT / "datasets" / "energy_dataset.csv",
        parse_dates=["time"],
        index_col="time",
    )
    energy_df.index = pd.to_datetime(energy_df.index, utc=True)
    energy_df = energy_df.drop(
        columns=[c for c in energy_df.columns if energy_df[c].isnull().all()]
    ).ffill().bfill()

    weather_df = pd.read_csv(
        ROOT / "datasets" / "weather_features.csv",
        parse_dates=["dt_iso"],
        index_col="dt_iso",
    )
    weather_df.index = pd.to_datetime(weather_df.index, utc=True)
    wnum = weather_df.select_dtypes(include=[np.number]).groupby(level=0).mean()
    for col in ["temp", "temp_min", "temp_max"]:
        if col in wnum.columns:
            wnum[col] -= 273.15
    wnum = wnum.rename(
        columns={
            "temp": "temperatura_sr",
            "humidity": "wilgotnosc",
            "wind_speed": "predkosc_wiatru",
            "pressure": "cisnienie",
            "clouds_all": "zachmurzenie",
            "rain_1h": "opady",
        }
    )
    wcols = [c for c in ["temperatura_sr", "wilgotnosc", "predkosc_wiatru", "cisnienie", "zachmurzenie", "opady"] if c in wnum.columns]
    wavg = wnum[wcols]

    df = energy_df.join(wavg, how="left")
    df[wcols] = df[wcols].ffill().bfill()

    ren = ["generation biomass", "generation hydro run-of-river and poundage",
           "generation hydro water reservoir", "generation other renewable",
           "generation solar", "generation wind offshore", "generation wind onshore", "generation geothermal"]
    fos = ["generation fossil brown coal/lignite", "generation fossil gas",
           "generation fossil hard coal", "generation fossil oil"]
    gen = [c for c in df.columns if c.startswith("generation ")]

    df["generacja_oze"] = df[[c for c in ren if c in df.columns]].sum(axis=1)
    df["generacja_paliwa"] = df[[c for c in fos if c in df.columns]].sum(axis=1)
    df["generacja_calkowita"] = df[gen].sum(axis=1)
    df["udzial_oze"] = (df["generacja_oze"] / df["generacja_calkowita"] * 100).round(1)
    df["godzina"] = df.index.hour
    df["dzien_tyg"] = df.index.dayofweek
    df["miesiac"] = df.index.month
    df["weekend"] = df["dzien_tyg"].isin([5, 6]).astype(int)
    return df


def compute_stats(df: pd.DataFrame) -> dict:
    daily = df["total load actual"].resample("D").mean().dropna()
    sh_stat, sh_p = sp_stats.shapiro(daily.sample(min(500, len(daily)), random_state=42))
    wd = df.loc[df["weekend"] == 0, "total load actual"]
    we = df.loc[df["weekend"] == 1, "total load actual"]
    mw_stat, mw_p = sp_stats.mannwhitneyu(wd, we, alternative="two-sided")
    clean = df[["total load actual", "temperatura_sr", "price day ahead"]].dropna()
    pt = sp_stats.pearsonr(clean["total load actual"], clean["temperatura_sr"])
    pp = sp_stats.pearsonr(clean["total load actual"], clean["price day ahead"])

    feats = ["godzina", "dzien_tyg", "miesiac", "weekend", "temperatura_sr"]
    mdf = df[feats + ["total load actual"]].dropna()
    tr, te = mdf[mdf.index.year < 2018], mdf[mdf.index.year == 2018]
    m = LinearRegression().fit(tr[feats], tr["total load actual"])
    pred = m.predict(te[feats])
    mae = mean_absolute_error(te["total load actual"], pred)
    mape = mean_absolute_percentage_error(te["total load actual"], pred) * 100

    return {
        "n": len(df),
        "d0": str(df.index.min().date()),
        "d1": str(df.index.max().date()),
        "load_mu": df["total load actual"].mean(),
        "load_sd": df["total load actual"].std(),
        "sh_p": sh_p,
        "mw_p": mw_p,
        "wd_mu": wd.mean(),
        "we_mu": we.mean(),
        "r_temp": pt.statistic,
        "r_price": pp.statistic,
        "mae": mae,
        "mape": mape,
    }


def save_figures(df: pd.DataFrame) -> dict[str, Path]:
    FIGURES.mkdir(parents=True, exist_ok=True)
    paths = {}

    fig, ax = plt.subplots(figsize=(11, 3.8))
    df["total load actual"].resample("D").mean().plot(ax=ax, color="#1565C0", lw=0.9)
    ax.set_title("Średnie dzienne zużycie energii — Hiszpania 2015–2018", fontweight="bold")
    ax.set_xlabel(""); ax.set_ylabel("MW")
    fig.tight_layout()
    paths["czas"] = FIGURES / "01_zuzycie_czas.png"
    fig.savefig(paths["czas"], bbox_inches="tight", facecolor="white")
    plt.close()

    fig, ax = plt.subplots(figsize=(9, 4.5))
    for wk, lb, col in [(0, "Dzień roboczy", "#1565C0"), (1, "Weekend", "#43A047")]:
        p = df[df["weekend"] == wk].groupby("godzina")["total load actual"].mean()
        ax.plot(p.index, p.values, "o-", label=lb, color=col, lw=2, ms=4)
    ax.set_title("Profil dobowy zużycia", fontweight="bold")
    ax.set_xlabel("Godzina"); ax.set_ylabel("MW"); ax.legend()
    fig.tight_layout()
    paths["profil"] = FIGURES / "02_profil_dobowy.png"
    fig.savefig(paths["profil"], bbox_inches="tight", facecolor="white")
    plt.close()

    fig, ax = plt.subplots(figsize=(9, 5))
    pv = df.pivot_table(values="total load actual", index="godzina", columns="miesiac", aggfunc="mean")
    sns.heatmap(pv, cmap="YlOrRd", ax=ax, cbar_kws={"label": "MW"})
    ax.set_title("Zużycie — godzina × miesiąc", fontweight="bold")
    fig.tight_layout()
    paths["heat"] = FIGURES / "03_heatmapa.png"
    fig.savefig(paths["heat"], bbox_inches="tight", facecolor="white")
    plt.close()

    fig, ax = plt.subplots(figsize=(9, 4.5))
    mix = df[["generacja_oze", "generacja_paliwa"]].resample("MS").mean()
    mix.columns = ["OZE", "Paliwa kopalne"]
    mix.plot.area(ax=ax, color=["#43A047", "#6D4C41"], alpha=0.85)
    ax.set_title("Produkcja energii — OZE vs paliwa kopalne", fontweight="bold")
    ax.set_ylabel("MW")
    fig.tight_layout()
    paths["oze"] = FIGURES / "04_miks_energetyczny.png"
    fig.savefig(paths["oze"], bbox_inches="tight", facecolor="white")
    plt.close()

    feats = ["godzina", "dzien_tyg", "miesiac", "weekend", "temperatura_sr"]
    mdf = df[feats + ["total load actual"]].dropna()
    tr, te = mdf[mdf.index.year < 2018], mdf[mdf.index.year == 2018]
    pred = LinearRegression().fit(tr[feats], tr["total load actual"]).predict(te[feats])
    fig, ax = plt.subplots(figsize=(11, 3.8))
    s = te.iloc[:168]
    ax.plot(s.index, s["total load actual"], label="Rzeczywiste", color="#1565C0", lw=1.5)
    ax.plot(s.index, pred[:168], label="Prognoza (MLR)", color="#E53935", ls="--", lw=1.5)
    ax.set_title("Prognoza zużycia — pierwszy tydzień 2018", fontweight="bold")
    ax.set_ylabel("MW"); ax.legend()
    fig.tight_layout()
    paths["prog"] = FIGURES / "05_prognoza.png"
    fig.savefig(paths["prog"], bbox_inches="tight", facecolor="white")
    plt.close()

    return paths


# ─── PowerPoint ─────────────────────────────────────────────────────────────

def _slide_blank(prs: Presentation):
    return prs.slides.add_slide(prs.slide_layouts[6])


def _bar(slide, prs, top=Inch(0), height=Inch(1.05), color=BLUE):
    sh = slide.shapes.add_shape(1, Inch(0), top, prs.slide_width, height)  # rectangle
    sh.fill.solid()
    sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    return sh


def _textbox(slide, left, top, width, height, text, size=18, bold=False, color=DARK, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = PptPt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    return tb


def build_ppt(stats: dict, figs: dict[str, Path]) -> Path:
    prs = Presentation()
    prs.slide_width = Inch(13.333)
    prs.slide_height = Inch(7.5)
    W, H = prs.slide_width, prs.slide_height

    # ── Slajd tytułowy ──
    s = _slide_blank(prs)
    bg = s.shapes.add_shape(1, 0, 0, W, H)
    bg.fill.solid(); bg.fill.fore_color.rgb = BLUE; bg.line.fill.background()
    _textbox(s, Inch(0.8), Inch(1.6), Inch(11.5), Inch(1.2),
             TEAM["tytul"], size=32, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    _textbox(s, Inch(0.8), Inch(2.9), Inch(11.5), Inch(0.6),
             TEAM["przedmiot"], size=20, color=WHITE, align=PP_ALIGN.CENTER)
    team_txt = "  |  ".join(f"{n} ({a})" for n, a in TEAM["czlonkowie"])
    _textbox(s, Inch(0.8), Inch(3.7), Inch(11.5), Inch(0.5),
             team_txt, size=14, color=WHITE, align=PP_ALIGN.CENTER)
    _textbox(s, Inch(0.8), Inch(4.4), Inch(11.5), Inch(0.4),
             f'{TEAM["uczelnia"]}  •  {TEAM["rok"]}  •  semestr {TEAM["semestr"]}',
             size=13, color=WHITE, align=PP_ALIGN.CENTER)

    def content_slide(title: str, bullets: list[str], subtitle: str = ""):
        s = _slide_blank(prs)
        _bar(s, prs)
        _textbox(s, Inch(0.55), Inch(0.22), Inch(12), Inch(0.55), title, size=26, bold=True, color=WHITE)
        y = Inch(1.25)
        if subtitle:
            _textbox(s, Inch(0.7), y, Inch(11.8), Inch(0.4), subtitle, size=14, color=GRAY)
            y += Inch(0.45)
        for b in bullets:
            _textbox(s, Inch(0.85), y, Inch(11.5), Inch(0.55), f"•  {b}", size=17, color=DARK)
            y += Inch(0.52)

    def image_slide(title: str, img: Path, caption: str = ""):
        s = _slide_blank(prs)
        _bar(s, prs)
        _textbox(s, Inch(0.55), Inch(0.22), Inch(12), Inch(0.55), title, size=24, bold=True, color=WHITE)
        s.shapes.add_picture(str(img), Inch(0.65), Inch(1.15), width=Inch(12.0))
        if caption:
            _textbox(s, Inch(0.65), Inch(6.85), Inch(12), Inch(0.35), caption, size=11, color=GRAY, align=PP_ALIGN.CENTER)

    content_slide(
        "Cel projektu",
        [
            "Analiza godzinowego zapotrzebowania na energię w Hiszpanii (2015–2018)",
            "Identyfikacja wzorców sezonowych, dobowych i tygodniowych",
            "Badanie wpływu pogody i miksu energetycznego (OZE vs paliwa)",
            "Prognoza zużycia — regresja liniowa (baseline)",
        ],
    )

    content_slide(
        "Zbiór danych",
        [
            f'{stats["n"]:,} obserwacji godzinowych  •  {stats["d0"]} – {stats["d1"]}',
            "Zużycie, produkcja ze źródeł, ceny, pogoda (5 miast)",
            "Źródło: Kaggle / ENTSO-E, Red Eléctrica",
            "Narzędzia: Python, Pandas, Matplotlib, Seaborn, Plotly, scikit-learn",
        ],
    )

    content_slide(
        "Przygotowanie danych",
        [
            "Wczytanie CSV → DataFrame z indeksem czasowym (UTC)",
            "Usunięcie pustych kolumn, uzupełnienie braków (ffill/bfill)",
            "Scalenie energii + pogody, cechy: godzina, weekend, udział OZE",
        ],
    )

    image_slide("Zużycie energii w czasie", figs["czas"],
                "Wyraźna sezonowość — wyższe zużycie zimą i latem.")
    image_slide("Profil dobowy", figs["profil"],
                "Dwa szczyty w dni robocze; niższe i płstsze zużycie w weekendy.")
    image_slide("Heatmapa: godzina × miesiąc", figs["heat"])
    image_slide("Miks energetyczny", figs["oze"],
                "Rosnący udział OZE w strukturze produkcji.")

    content_slide(
        "Wyniki statystyczne",
        [
            f'Średnie zużycie: {stats["load_mu"]:,.0f} MW (σ = {stats["load_sd"]:,.0f})',
            f'Shapiro-Wilk: p = {stats["sh_p"]:.2e} → brak normalności (testy nieparametryczne)',
            f'Mann-Whitney (weekend): p = {stats["mw_p"]:.2e} → weekend istotnie niższy',
            f'Śr. dzień roboczy: {stats["wd_mu"]:,.0f} MW  |  weekend: {stats["we_mu"]:,.0f} MW',
            f'Korelacja zużycie–temperatura: r = {stats["r_temp"]:.2f}',
        ],
    )

    image_slide(
        "Prognoza zużycia (regresja liniowa)",
        figs["prog"],
        f'MAE ≈ {stats["mae"]:,.0f} MW  |  MAPE ≈ {stats["mape"]:.1f}% na danych 2018',
    )

    content_slide(
        "Wnioski",
        [
            "Silna sezonowość i cykl tygodniowy zużycia energii",
            "OZE i paliwa kopalne uzupełniają się sezonowo",
            f'Model baseline (5 cech) osiąga MAPE ≈ {stats["mape"]:.1f}%',
            "Temperatura i pora dnia to kluczowe predyktory",
        ],
    )

    # Koniec
    s = _slide_blank(prs)
    bg = s.shapes.add_shape(1, 0, 0, W, H)
    bg.fill.solid(); bg.fill.fore_color.rgb = GREEN; bg.line.fill.background()
    _textbox(s, Inch(1), Inch(2.8), Inch(11), Inch(1),
             "Dziękujemy za uwagę", size=36, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    _textbox(s, Inch(1), Inch(4.0), Inch(11), Inch(0.5),
             "Pytania?", size=22, color=WHITE, align=PP_ALIGN.CENTER)

    out = DOCS / "prezentacja.pptx"
    prs.save(out)
    return out


# ─── Word ───────────────────────────────────────────────────────────────────

def build_report(stats: dict, figs: dict[str, Path]) -> Path:
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    t = doc.add_heading(TEAM["tytul"], 0)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER

    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = meta.add_run(
        f'{TEAM["przedmiot"]}\n{TEAM["uczelnia"]}  •  {TEAM["rok"]}  •  semestr {TEAM["semestr"]}\n'
    )
    r.font.size = Pt(12)
    for n, a in TEAM["czlonkowie"]:
        p = doc.add_paragraph(f"{n} — album {a}")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    def h1(t): doc.add_heading(t, 1)
    def h2(t): doc.add_heading(t, 2)
    def para(t): doc.add_paragraph(t)
    def img(path, w=6.0):
        doc.add_picture(str(path), width=Inches(w))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    h1("1. Opis problemu")
    para(
        "Celem jest analiza i prognozowanie zapotrzebowania na energię elektryczną w Hiszpanii "
        "na podstawie publicznych danych godzinowych (2015–2018). Badamy wzorce sezonowe i dobowe, "
        "wpływ pogody oraz budujemy prosty model predykcyjny w Pythonie z biblioteką Pandas."
    )

    h1("2. Opis zbioru danych")
    para(
        f'Zbiór Kaggle „Energy Consumption, Generation, Prices and Weather”: {stats["n"]:,} wierszy godzinowych, '
        f'okres {stats["d0"]} – {stats["d1"]}. Zmienne: produkcja ze źródeł, zużycie, ceny, pogoda (5 miast).'
    )

    h1("3. Analiza danych")
    h2("3.1 Pre-processing")
    para(
        "Wczytanie CSV z parsowaniem dat, usunięcie pustych kolumn, uzupełnienie braków, "
        "scalenie danych pogodowych (średnia z 5 miast, °C), cechy pochodne: godzina, weekend, udział OZE."
    )

    h2("3.2 Wizualizacja")
    para("Poniżej wybrane wykresy; pełna analiza w pliku analiza.ipynb (w tym dashboard Plotly).")
    for key in ["czas", "profil", "heat", "oze"]:
        img(figs[key])

    h2("3.3 Statystyka")
    para(
        f'Średnie zużycie: {stats["load_mu"]:,.0f} MW. Test Shapiro-Wilka: p = {stats["sh_p"]:.2e}. '
        f'Mann-Whitney (weekend vs dzień roboczy): p = {stats["mw_p"]:.2e} — różnica istotna. '
        f'Korelacja zużycie–temperatura: r = {stats["r_temp"]:.2f}.'
    )

    h2("3.4 Analiza zaawansowana")
    para(
        "Dekompozycja szeregu czasowego, ACF/PACF, prognoza regresją liniową "
        f'(MAE = {stats["mae"]:,.0f} MW, MAPE = {stats["mape"]:.1f}%).'
    )
    img(figs["prog"])

    h1("4. Wnioski")
    for w in [
        "Zużycie ma silną sezonowość i niższy poziom w weekendy.",
        "Profil dobowy: dwa szczyty w dni robocze.",
        "OZE rośnie sezonowo; gaz reguluje szczyty.",
        f'Model MLR osiąga MAPE ≈ {stats["mape"]:.1f}% — sensowny baseline.',
    ]:
        doc.add_paragraph(w, style="List Bullet")

    h1("5. Załączniki")
    para("Kod: analiza.ipynb  |  Prezentacja: docs/prezentacja.pptx")

    out = DOCS / "raport.docx"
    doc.save(out)
    return out


def main():
    print("Ładowanie danych...")
    df = load_and_prepare()
    stats = compute_stats(df)
    print("Wykresy...")
    figs = save_figures(df)
    print("Prezentacja...")
    ppt = build_ppt(stats, figs)
    print("Raport...")
    doc = build_report(stats, figs)
    print(f"\nGotowe:\n  {ppt}\n  {doc}\n  {FIGURES}/")


if __name__ == "__main__":
    main()
