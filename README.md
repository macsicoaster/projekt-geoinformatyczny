[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)

# silesiaAIR

Aplikacja do wizualizacji danych geoprzestrzennych - monitorowanie jakości powietrza w Górnośląsko-Zagłębiowskiej Metropolii.

## O aplikacji

Aplikacja umożliwia wizualizację i analizę danych jakości powietrza z 14 stacji pomiarowych w Górnośląsko-Zagłębiowskiej Metropolii. Dane pobierane są z bazy PostgreSQL i przetwarzane przy użyciu zaawansowanych metod interpolacji przestrzennej (IDW, Kriging, RBF) oraz narzędzi analizy statystycznej. Wyniki wizualizacji można eksportować do raportu PDF.

## Funkcje

- **10 metod wizualizacji**: Mapa punktów, IDW, Kriging, RBF, Voronoi, wykresy statystyczne, histogramy, heatmapy, scatter plot
- **Mapowanie geograficzne**: OpenStreetMap z obsługą EPSG:4326
- **Baza danych**: PostgreSQL do przechowywania danych
- **Interfejs**: Responsywny design, dark mode, kalendarz do wyboru daty
- **PDF**: Generowanie raportów

## Tech

- Python 3.13 + Flask 3.1.2
- PostgreSQL baza danych
- GeoPandas, Matplotlib, Seaborn
- Bootstrap + vanilla JavaScript

## Szybki start

### Wymagania
- Python 3.13+
- PostgreSQL 12+

### Instalacja

```bash
# Sklonuj repozytorium
git clone https://github.com/macsicoaster/projekt-geoinformatyczny.git
cd projekt-geoinformatyczny

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom aplikację
python app.py
```

Otwórz http://localhost:5000

## Konfiguracja bazy danych

Zmień dane połączenia w `app.py`:

```python
DB_NAME = "silesiaair"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
```

### Struktura tabeli

Tabela `measurements` powinna mieć kolumny:
- `nazwa` - nazwa stacji
- `lat`, `lon` - współrzędne geograficzne
- `data` - data pomiaru (YYYY-MM-DD)
- `pm25`, `pm10`, `no2`, `so2`, `co`, `o3` - parametry powietrza
- `temperatura`, `wilgotnosc`, `cisnienie`, `predkosc_wiatru` - parametry pogody

## Dostępne stacje (GZM)

Katowice, Sosnowiec, Dąbrowa Górnicza, Czeladź, Mysłowice, Piekary Śląskie, Chorzów, Bytom, Zabrze, Gliwice, Mikołów, Ruda Śląska, Tarnowskie Góry, Pyskowice

## Metody wizualizacji

1. **Mapa** - punkty na mapie z kolorami
2. **IDW** - interpolacja Inverse Distance Weighting
3. **Kriging** - zaawansowana interpolacja geostatystyczna
4. **RBF** - Radial Basis Function interpolacja
5. **Voronoi** - diagram Voronoia
6. **Wykresy** - statystyczne wykresy
7. **Rozkłady** - histogramy zmiennych
8. **Histogram** - duży histogram z krzywą normalną
9. **Heatmap** - mapa ciepła
10. **Scatter** - wykres rozrzutu między zmiennymi

## API Endpoints

- `GET /` - główna strona
- `GET /api/dates` - dostępne daty
- `GET /api/variables` - dostępne zmienne
- `POST /generuj` - generuj wizualizację
- `POST /generuj_pdf` - generuj PDF
- `GET /health` - status aplikacji

## Struktura projektu

```
projekt-geoinformatyczny-v2/
├── app.py                    # główna aplikacja
├── requirements.txt          # zależności
├── templates/
│   ├── index.html           # strona główna
│   └── wynik.html           # wyniki
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   ├── img/
│   └── exports/             # wygenerowane wykresy
└── data/                     # katalog na dane
```

---

Aplikacja edukacyjna do monitoringu jakości powietrza w regionie śląskim
