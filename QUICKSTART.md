# 🚀 Szybki Start - GeoViz

## Instalacja i uruchomienie w 3 krokach

### Krok 1: Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### Krok 2: Przygotuj dane

Dane CSV są już dostępne w folderze `data/dane.csv` jako przykład.

Jeśli chcesz użyć własnych danych:
1. Umieść plik CSV o nazwie `dane.csv` w folderze `data/`
2. Plik musi zawierać kolumny: `nazwa`, `lat`, `lon`, `data`, `PM25`, `temperatura`, `wilgotnosc`

### Krok 3: Uruchom aplikację

```bash
python app.py
```

Aplikacja będzie dostępna pod adresem: **http://localhost:5000**

---

## Struktura katalogów

```
projekt-geoinformatyczny-v2/
├── app.py                  ← Główna aplikacja
├── requirements.txt        ← Zależności Python
├── README.md              ← Dokumentacja
├── QUICKSTART.md          ← Ten plik
├── data/
│   └── dane.csv           ← Dane (CSV)
├── templates/
│   ├── index.html         ← Strona główna
│   └── wynik.html         ← Strona wyników
└── static/
    ├── css/
    │   └── style.css      ← Styles
    ├── js/
    │   └── script.js      ← JavaScript
    ├── img/
    │   └── logo.svg       ← Logo
    └── exports/           ← Wyeksportowane pliki
```

---

## Format pliku CSV

Twój plik `dane.csv` musi mieć następujące kolumny:

```
nazwa,lat,lon,data,PM25,temperatura,wilgotnosc
Warszawa,52.2297,21.0122,2024-01-15,28.5,5.2,65
Kraków,50.0647,19.9450,2024-01-15,32.1,4.8,72
```

---

## Funkcje

✅ Mapa punktów  
✅ Interpolacja IDW  
✅ Kriging  
✅ Wykresy statystyczne  
✅ Export danych CSV  
✅ Responsywny interfejs  

---

## Wskazówki

- 🎨 Logo można zmienić - umieść plik SVG w `static/img/logo.svg`
- 📁 Wszystkie eksportowane pliki trafiają do `static/exports/`
- 🔧 Aby zmienić port: `python app.py` (domyślnie 5000)
- 🌐 Zmień `debug=True` na `debug=False` w app.py dla produkcji

---

## Rozwiązywanie problemów

### Problem: "No module named 'geopandas'"
Rozwiązanie: Zainstaluj zależności: `pip install -r requirements.txt`

### Problem: "Brak danych dla wybranej daty"
Rozwiązanie: Sprawdź czy data istnieje w pliku CSV

### Problem: Błąd "Cannot import name 'Point'"
Rozwiązanie: Zainstaluj bibliotekę Shapely: `pip install shapely`

---

Zabawy! 🎉
