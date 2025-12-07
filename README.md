# GeoViz - Wizualizacja Danych Geoprzestrzennych

Nowoczesna aplikacja webowa do analizy i wizualizacji danych geoprzestrzennych.

## Cechy

- 🗺️ **Wizualizacja map** - Wyświetlanie punktów pomiarowych na mapach interaktywnych
- 📈 **Wiele metod interpolacji** - IDW, Kriging, mapy punktów
- 📊 **Wykresy statystyczne** - Analiza rozkładu danych
- 📁 **Obsługa CSV** - Łatwe importowanie danych z plików CSV
- 🎨 **Nowoczesny interfejs** - Responsywny design z ciemnym motywem
- 📱 **Responsywność** - Działa na komputerach i urządzeniach mobilnych

## Wymagania

- Python 3.8+
- Wszystkie pakiety wymienione w `requirements.txt`

## Instalacja

1. Sklonuj repozytorium lub rozpakuj projekt
2. Przejdź do folderu projektu:
   ```
   cd projekt-geoinformatyczny-v2
   ```

3. Zainstaluj wymagane pakiety:
   ```
   pip install -r requirements.txt
   ```

## Przygotowanie danych

1. Utwórz folder `data/` w głównym katalogu projektu
2. Umieść plik CSV o nazwie `dane.csv` w folderze `data/`

### Format pliku CSV

Plik CSV musi zawierać następujące kolumny:

| Kolumna | Opis | Typ |
|---------|------|-----|
| `nazwa` | Nazwa stacji pomiarowej | tekst |
| `lat` | Szerokość geograficzna | liczba |
| `lon` | Długość geograficzna | liczba |
| `data` | Data pomiaru (YYYY-MM-DD) | data |
| `PM25` | Stężenie PM2.5 | liczba |
| `temperatura` | Temperatura | liczba |
| `wilgotnosc` | Wilgotność | liczba |

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
