# silesiaAIR

Nowoczesna aplikacja webowa do wizualizacji i analizy danych geoprzestrzennych, skoncentrowana na monitoringu jakości powietrza w Górnośląsko-Zagłębiowskiej Metropolii (GZM).

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Opis projektu

silesiaAIR to platforma wizualizacji geoprzestrzennej oparta na Flask, zaprojektowana do analizy danych atmosferycznych z 14 miast Górnośląsko-Zagłębiowskiej Metropolii. Aplikacja oferuje interaktywne mapy, analizę statystyczną oraz wiele metod interpolacji do monitoringu środowiska.

## Funkcjonalności

- **Interaktywne mapy** - Wyświetlanie punktów pomiarowych na mapach OpenStreetMap z automatyczną obsługą współrzędnych (EPSG:4326)
- **Wiele metod interpolacji**
  - Mapy punktowe - Bezpośrednia wizualizacja lokalizacji pomiarowych
  - IDW (Inverse Distance Weighting) - Interpolacja na siatce 150×150
  - Kriging - Zaawansowana metoda geostatystyczna z wariogramem sferycznym
- **Wizualizacje statystyczne** - Wykresy słupkowe, liniowe i pudełkowe do analizy rozkładu danych
- **Generowanie raportów PDF** - Kompleksowe raporty z 12 metrykami statystycznymi, w tym kwartylami, wariancją i współczynnikiem zmienności
- **Obsługa motywów** - Tryb jasny i ciemny z zapamiętywaniem w localStorage
- **Responsywny design** - Interfejs przyjazny dla urządzeń mobilnych z modalnym kalendarzem i wizualnymi wskaźnikami dostępności danych

## Stack technologiczny

- **Backend**: Flask 3.1.2
- **Geoprzestrzenne**: GeoPandas, Contextily (OSM), PyKrige
- **Wizualizacja**: Matplotlib (DPI 100), Seaborn
- **Przetwarzanie danych**: Pandas, NumPy, scikit-learn
- **Generowanie PDF**: pdfkit (HTML-to-PDF), reportlab (fallback)
- **Frontend**: Vanilla JavaScript, CSS3 z gradientowymi motywami

## Instalacja

### Wymagania wstępne

- Python 3.8 lub nowszy
- Menedżer pakietów pip
- wkhtmltopdf (do generowania PDF)

### Konfiguracja

1. Sklonuj repozytorium:
```bash
git clone <adres-repozytorium>
cd projekt-geoinformatyczny-v2
```

2. Zainstaluj zależności Python:
```bash
pip install -r requirements.txt
```

3. Zainstaluj wkhtmltopdf:
- **Windows**: Pobierz z [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)
- **Linux**: `sudo apt-get install wkhtmltopdf`
- **macOS**: `brew install wkhtmltopdf`

4. Przygotuj katalog na dane:
```bash
mkdir -p data
```

5. Umieść plik CSV w `data/dane.csv` (zobacz sekcję Format danych)

## Użycie

### Uruchamianie aplikacji

```bash
python app.py
```

Aplikacja uruchomi się pod adresem `http://localhost:5000`

### Wdrożenie produkcyjne

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Format danych

Aplikacja wymaga pliku CSV (`data/dane.csv`) o następującej strukturze:

| Kolumna | Opis | Typ | Przykład |
|---------|------|-----|----------|
| `nazwa` | Nazwa stacji pomiarowej | string | Katowice |
| `lat` | Szerokość geograficzna (WGS84) | float | 50.2569 |
| `lon` | Długość geograficzna (WGS84) | float | 19.0273 |
| `data` | Data pomiaru | string (YYYY-MM-DD) | 2024-01-15 |
| `PM25` | Stężenie PM2.5 | float | 35.2 |
| `temperatura` | Temperatura (°C) | float | 12.5 |
| `wilgotnosc` | Wilgotność (%) | float | 65.0 |

### Przykład

```csv
nazwa,lat,lon,data,PM25,temperatura,wilgotnosc
Katowice,50.2569,19.0273,2024-01-15,35.2,12.5,65.0
Sosnowiec,50.2917,19.1397,2024-01-15,28.7,11.8,68.5
```

## Konfiguracja

### Obsługiwane miasta (GZM)

Aplikacja zawiera predefiniowane współrzędne dla 14 miast:
- Katowice, Sosnowiec, Dąbrowa Górnicza, Czeladź
- Mysłowice, Piekary Śląskie, Chorzów, Bytom
- Zabrze, Gliwice, Mikołów, Ruda Śląska
- Tarnowskie Góry, Pyskowice

### Parametry wizualizacji

- **Rozdzielczość map**: 14×10 cali, 100 DPI (renderowanie i zapis)
- **Układ współrzędnych**: EPSG:4326 (WGS84 geograficzny)
- **Strefa buforowa**: 0.1° (~11 km)
- **Siatka IDW**: 150×150 punktów
- **Siatka Kriging**: 120×120 punktów
- **Schemat kolorów**: RdYlBu_r (odwrócony Czerwony-Żółty-Niebieski)

## Endpointy API

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/` | GET | Główny interfejs aplikacji |
| `/api/dates` | GET | Lista dostępnych dat pomiarowych |
| `/api/variables` | GET | Lista dostępnych zmiennych |
| `/generuj` | POST | Generowanie wizualizacji |
| `/wynik` | GET | Wyświetlenie wyniku wizualizacji |
| `/eksportuj` | POST | Eksport danych do CSV |
| `/generuj_pdf` | POST | Generowanie raportu PDF |
| `/pobierz_pdf/<filename>` | GET | Pobieranie raportu PDF |
| `/health` | GET | Sprawdzenie stanu aplikacji |

## Struktura projektu

```
projekt-geoinformatyczny-v2/
├── app.py                 # Główna aplikacja Flask
├── requirements.txt       # Zależności Python
├── Procfile              # Konfiguracja wdrożenia Heroku
├── data/
│   └── dane.csv          # Dane pomiarowe
├── static/
│   ├── css/
│   │   └── style.css     # Główny arkusz stylów
│   ├── js/
│   │   └── script.js     # Logika klienta
│   ├── img/              # Zasoby graficzne
│   └── exports/          # Wygenerowane wizualizacje
└── templates/
    ├── index.html        # Główny interfejs
    └── wynik.html        # Wyświetlanie wyników
```

## Szczegóły funkcjonalności

### Metody interpolacji

**IDW (Inverse Distance Weighting)**
- Rozdzielczość siatki: 150×150
- Średnia ważona odległością z sąsiednich punktów
- Najlepsze dla: Szybkiej interpolacji przestrzennej

**Kriging**
- Rozdzielczość siatki: 120×120
- Kriging zwykły z wariogramem sferycznym
- Najlepsze dla: Statystycznej predykcji przestrzennej z niepewnością

### Metryki statystyczne

Wygenerowane raporty PDF zawierają:
- **Tendencja centralna**: Średnia, Mediana
- **Rozproszenie**: Min, Max, Rozstęp, Odch. std., Wariancja, CV%
- **Kwartyle**: Q1, Q3, IQR, Liczebność próby

### Kalendarz wyboru daty

- Wizualne rozróżnienie dat z dostępnymi danymi (podświetlenie niebieskie)
- Nawigacja po miesiącach z polską lokalizacją
- Interfejs modalny
- Zsynchronizowany z przesyłaniem formularza

## Wsparcie przeglądarek

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Rozwiązywanie problemów

### Najczęstsze problemy

**1. Błąd "Image size too large"**
- Sprawdź czy układ współrzędnych to EPSG:4326 (nie EPSG:3857)
- Upewnij się, że wartości lat/lon są w stopniach, nie w metrach

**2. Polskie znaki wyświetlają się jako kwadraty w PDF**
- Upewnij się, że wkhtmltopdf jest zainstalowany
- Sprawdź kodowanie UTF-8 w pliku CSV

**3. Mapy wyświetlają się jako puste**
- Sprawdź połączenie internetowe dla map bazowych OpenStreetMap
- Upewnij się, że współrzędne są w prawidłowych zakresach (lat: 49-51, lon: 18-20)

**4. Interpolacja Kriging zawodzi**
- Automatycznie przechodzi na IDW
- Sprawdź czy jest wystarczająca liczba punktów danych (minimum 3)

## Współtworzenie

Wkład w rozwój projektu jest mile widziany. Prosimy o przestrzeganie wytycznych:
1. Forkuj repozytorium
2. Utwórz branch funkcjonalności (`git checkout -b feature/ulepszenie`)
3. Commituj zmiany (`git commit -am 'Dodanie nowej funkcji'`)
4. Push do brancha (`git push origin feature/ulepszenie`)
5. Otwórz Pull Request

## Licencja

Ten projekt jest licencjonowany na licencji MIT - szczegóły w pliku LICENSE.

## Podziękowania

- Współtwórcom OpenStreetMap za kafelki map bazowych
- Zespołom GeoPandas i Contextily za biblioteki geoprzestrzenne
- Społeczności Flask za framework webowy

## Kontakt

W razie pytań lub wsparcia, prosimy o otwarcie issue w repozytorium GitHub.

---

**Uwaga**: Ta aplikacja jest przeznaczona do celów edukacyjnych i badawczych związanych z monitoringiem jakości powietrza w regionie śląskim Polski.

### Przykład CSV

```csv
nazwa,lat,lon,data,PM25,temperatura,wilgotnosc
Warszawa,52.2297,21.0122,2024-01-15,28.5,5.2,65
Kraków,50.0647,19.9450,2024-01-15,32.1,4.8,72
Gdańsk,54.3520,18.6466,2024-01-15,24.3,3.5,78
```

## Uruchomienie

Uruchom aplikację z wiersza poleceń:

```bash
python app.py
```

Aplikacja będzie dostępna pod adresem `http://localhost:5000`

## Struktura projektu

```
projekt-geoinformatyczny-v2/
├── app.py                      # Główna aplikacja Flask
├── requirements.txt            # Lista zależności
├── README.md                   # Ten plik
├── data/
│   └── dane.csv               # Plik CSV z danymi (musisz dodać)
├── templates/
│   ├── index.html             # Strona główna
│   └── wynik.html             # Strona wyników
├── static/
│   ├── css/
│   │   └── style.css          # Style CSS
│   ├── js/
│   │   └── script.js          # JavaScript (opcjonalnie)
│   ├── img/
│   │   └── logo.svg           # Logo (opcjonalnie)
│   └── exports/               # Eksportowane wykresy i dane
└── Procfile                    # Konfiguracja dla Heroku (opcjonalnie)
```

## Użytkowanie

1. **Strona główna** - Wybierz datę, zmienną i metodę wizualizacji
2. **Generuj wizualizację** - Kliknij przycisk aby wygenerować wykres
3. **Eksportuj dane** - Pobierz dane w formacie CSV
4. **Wyniki** - Przeglądaj wizualizacje i pobieraj obrazy

## Metody wizualizacji

### Mapa punktów
Wyświetla punkty pomiarowe bezpośrednio na mapie. Każdy punkt jest kolorowany zgodnie z wartością zmiennej.

### Interpolacja IDW
Metoda Inverse Distance Weighting interpoluje wartości między punktami pomiarowymi. Wartość w każdym punkcie siatki jest obliczana jako średnia ważona wartości w punktach pomiarowych.

### Kriging
Zaawansowana metoda geostatystyczna oparta na teorii funkcji losowych. Pozwala na interpolację danych uwzględniając strukturę przestrzenną zjawiska.

### Wykresy statystyczne
Prezentuje rozkład wartości zmiennej w postaci histogramu, wykresu liniowego i diagramu pudełkowego.

## Technologie

- **Backend**: Flask (Python)
- **Geoprzestrzeń**: GeoPandas, Shapely
- **Wizualizacja**: Matplotlib, Seaborn
- **Mapy**: Contextily, OSM
- **Dane**: Pandas
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## Licencja

MIT

## Autor

Projekt GeoViz - Wizualizacja danych geoprzestrzennych

## Wsparcie

W przypadku problemów lub pytań, sprawdź dokumentację bibliotek:
- [GeoPandas](https://geopandas.org/)
- [Shapely](https://shapely.readthedocs.io/)
- [Matplotlib](https://matplotlib.org/)
- [Flask](https://flask.palletsprojects.com/)
