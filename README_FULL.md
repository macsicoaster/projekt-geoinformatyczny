# GeoViz - Wizualizacja Danych Geoprzestrzennych

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

Nowoczesna aplikacja webowa do analizy i wizualizacji danych geoprzestrzennych. Obsługuje pliki CSV, oferuje wiele metod interpolacji oraz nowoczesny, responsywny interfejs.

## ✨ Cechy

- 🗺️ **Wizualizacja map** - Wyświetlanie punktów pomiarowych na mapach
- 📊 **Metody interpolacji** - IDW, Kriging, mapy punktów
- 📈 **Wykresy statystyczne** - Histogramy, wykresy liniowe, pudełkowe
- 📁 **Obsługa CSV** - Łatwe importowanie danych
- 🌙 **Ciemny motyw** - Nowoczesny dark mode
- 📱 **Responsywny** - Działa na komputerach i telefonach
- 🚀 **Zero zależności** - Brak wymagania Azure lub bazy danych
- 💾 **Export** - Pobierz wykresy i dane

## 📦 Wymagania

- Python 3.8+
- pip (menadżer pakietów)
- ~500MB miejsca na dysku

## 🚀 Szybki Start

### 1. Zainstaluj zależności

```bash
cd d:\projekt-geoinformatyczny-v2
pip install -r requirements.txt
```

### 2. Uruchom aplikację

```bash
python app.py
```

### 3. Otwórz w przeglądarce

```
http://localhost:5000
```

**To wszystko!** 🎉

## 📊 Przygotowanie danych

### Format CSV

Plik `data/dane.csv` musi zawierać:

```csv
nazwa,lat,lon,data,PM25,temperatura,wilgotnosc
Warszawa,52.2297,21.0122,2024-01-15,28.5,5.2,65
Kraków,50.0647,19.9450,2024-01-15,32.1,4.8,72
```

### Kolumny wymagane

| Kolumna | Typ | Opis |
|---------|-----|------|
| `nazwa` | tekst | Nazwa stacji pomiarowej |
| `lat` | liczba | Szerokość geograficzna |
| `lon` | liczba | Długość geograficzna |
| `data` | data | Data w formacie YYYY-MM-DD |
| `PM25` | liczba | Stężenie PM2.5 |
| `temperatura` | liczba | Temperatura (°C) |
| `wilgotnosc` | liczba | Wilgotność (%) |

## 🎨 Metody wizualizacji

### Mapa punktów
Wyświetla punkty pomiarowe na mapie OSM. Każdy punkt jest kolorowany zgodnie z wartością zmiennej. Idealna do szybkiego przeglądu rozkładu przestrzennego.

### Interpolacja IDW
Metoda Inverse Distance Weighting interpoluje wartości między punktami. Wartość w każdym punkcie siatki jest średnią ważoną wartości w punktach pomiarowych.

**Formuła:** `z = Σ(w_i * z_i) / Σ(w_i)` gdzie `w_i = 1 / d_i²`

### Kriging
Zaawansowana metoda geostatystyczna. Interpoluje dane uwzględniając strukturę przestrzenną zjawiska i zapewnia niepewność oszacowania.

**Użycie:** Dla danych z silną strukturą przestrzenną

### Wykresy statystyczne
Prezentuje rozkład wartości zmiennej w postaci:
- 📊 Histogramu (wykres słupkowy)
- 📈 Wykresu liniowego
- 📦 Diagramu pudełkowego (box plot)

## 🏗️ Struktura projektu

```
projekt-geoinformatyczny-v2/
├── app.py                      ← Główna aplikacja Flask
├── requirements.txt            ← Zależności
├── README.md                   ← Dokumentacja (ten plik)
├── QUICKSTART.md               ← Szybki start
├── INSTALLATION.md             ← Instalacja
├── CHANGELOG.md                ← Historia zmian
├── STRUCTURE.md                ← Struktura katalogów
├── test_structure.py           ← Test walidacyjny
│
├── data/
│   └── dane.csv               ← Plik CSV z danymi
│
├── templates/
│   ├── index.html             ← Strona główna
│   └── wynik.html             ← Strona wyników
│
└── static/
    ├── css/
    │   └── style.css          ← Style CSS
    ├── js/
    │   └── script.js          ← JavaScript
    ├── img/
    │   └── logo.svg           ← Logo
    └── exports/               ← Eksportowane wykresy
```

## 🔧 Konfiguracja

### Zmienne środowiskowe (`.env`)

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=change-this-in-production
```

### Zmiana portu

W pliku `app.py` na końcu:

```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Zmień port
```

### Zmiana kolorów

W `static/css/style.css`:

```css
:root {
    --primary-color: #6366f1;      /* Zmień na swój kolor */
    --secondary-color: #ec4899;    /* Zmień na swój kolor */
}
```

## 🌐 API Endpoints

| Endpoint | Metoda | Opis |
|----------|--------|------|
| `/` | GET | Strona główna |
| `/api/dates` | GET | Pobierz dostępne daty |
| `/api/variables` | GET | Pobierz dostępne zmienne |
| `/generuj` | POST | Generuj wizualizację |
| `/wynik` | GET | Wyświetl wynik |
| `/eksportuj` | POST | Eksportuj dane CSV |
| `/health` | GET | Health check |

## 🎓 Przykłady

### Generowanie wizualizacji

```python
# Aplikacja automatycznie:
# 1. Wczytuje dane z CSV
# 2. Filtruje dla wybranej daty
# 3. Generuje wizualizację (matplotlib)
# 4. Zapisuje do static/exports/
# 5. Wyświetla w przeglądarce
```

### Export danych

```bash
# Kliknij "Eksportuj dane"
# Pobierze CSV z danymi
```

## 🛠️ Instalacja z Virtual Environment

### Windows (PowerShell)

```bash
# Utwórz venv
python -m venv venv

# Aktywuj
.\venv\Scripts\Activate.ps1

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom
python app.py
```

### Linux/Mac

```bash
# Utwórz venv
python3 -m venv venv

# Aktywuj
source venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom
python app.py
```

## 🐛 Rozwiązywanie problemów

### Problem: "No module named 'geopandas'"

```bash
pip install -r requirements.txt
```

### Problem: "Port 5000 jest już zajęty"

```python
# Zmień port w app.py
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

### Problem: "Brak danych dla wybranej daty"

1. Sprawdź czy `data/dane.csv` istnieje
2. Sprawdź format daty: `YYYY-MM-DD`
3. Uruchom: `python test_structure.py`

### Problem: "Błąd przy wczytywaniu CSV"

1. Sprawdź separatory (muszą być przecinkami)
2. Sprawdź encoding (UTF-8)
3. Sprawdź nazwy kolumn
4. Uruchom: `python test_structure.py`

## 🧪 Testing

Sprawdzenie struktury projektu:

```bash
python test_structure.py
```

Wyświetli:
- ✅ Czy istnieją wymagane pliki
- ✅ Czy są zainstalowane biblioteki
- ✅ Czy CSV ma poprawny format

## 📚 Dokumentacja

- **README.md** (ten plik) - Pełna dokumentacja
- **QUICKSTART.md** - Szybki start w 3 krokach
- **INSTALLATION.md** - Szczegółowa instalacja
- **CHANGELOG.md** - Historia zmian
- **STRUCTURE.md** - Szczegółowa struktura

## 🎯 Zaawansowane

### Dodanie nowych zmiennych

W `app.py`:

```python
MAPA_ZMIENNYCH = {
    "pm25": ("PM25", "PM25"),
    "temperatura": ("temperatura", "temperatura"),
    "wilgotnosc": ("wilgotnosc", "wilgotnosc"),
    "nowa_zmienna": ("nowa_kolumna", "nowa_kolumna"),  # Dodaj tutaj
}
```

W `data/dane.csv`:

```csv
nazwa,lat,lon,data,PM25,temperatura,wilgotnosc,nowa_kolumna
...
```

### Zmiana interpolacji

W `app.py` funkcja `rysuj_mape_kriging()`:

```python
# Zmień variogram model
ok = OrdinaryKriging(
    x, y, z,
    variogram_model="spherical",  # linear, exponential, gaussian, spherical
    verbose=False,
    enable_plotting=False
)
```

### Dodanie nowego layoutu

W `templates/`:

1. Utwórz `nowy_template.html`
2. W `app.py` dodaj route:

```python
@app.route('/nowy')
def nowy():
    return render_template('nowy_template.html')
```

3. Umieść link w `index.html`

## 🚀 Deploy

### Heroku

```bash
heroku create nazwa-aplikacji
git push heroku main
```

### PythonAnywhere

1. Upload plików
2. Konfiguracja WSGI
3. Reload

### Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 📊 Technologie

- **Backend**: Flask 3.1.2
- **Geoprzestrzeń**: GeoPandas 1.1.1, Shapely 2.1.2
- **Wizualizacja**: Matplotlib 3.10.7, Seaborn 0.13.2
- **Dane**: Pandas 2.3.3, NumPy 2.3.5
- **Mapy**: Contextily 1.7.0, OpenStreetMap
- **Interpolacja**: PyKrige 1.7.3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## 📄 Licencja

MIT License - Wolny do użytku komercyjnego i prywatnego

## 👤 Autor

Projekt GeoViz v2

## 🤝 Wkład

Pytania? Sprawdź:
- Dokumentację w folderze (README.md, QUICKSTART.md)
- Komentarze w kodzie (app.py)
- Dokumentację bibliotek online

## 🔗 Zasoby

- [Flask Documentation](https://flask.palletsprojects.com/)
- [GeoPandas Documentation](https://geopandas.org/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Shapely Documentation](https://shapely.readthedocs.io/)

## 📞 Pomoc

Jeśli coś nie działa:

1. Sprawdź `test_structure.py`
2. Czytaj komunikaty błędów
3. Sprawdź dokumentację
4. Uruchom `pip install --upgrade -r requirements.txt`

## 🎉 Podziękowania

Dziękuję za korzystanie z GeoViz!

---

**Wersja: 2.0.0**  
**Ostatnia aktualizacja: 2024**  
**Status: Produkcyjny** ✅
