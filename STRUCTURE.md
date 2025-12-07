## 🗂️ Struktura projektu GeoViz v2

```
projekt-geoinformatyczny-v2/
│
├─── 📄 Pliki główne
│    ├── app.py ........................ Aplikacja Flask (główny plik)
│    ├── requirements.txt ............. Zależności Python
│    ├── Procfile ..................... Deploy na Heroku
│    ├── .env ......................... Zmienne środowiskowe
│    └── .gitignore ................... Ignorowanie plików Git
│
├─── 📚 Dokumentacja
│    ├── README.md .................... Pełna dokumentacja
│    ├── QUICKSTART.md ............... Szybki start (3 kroki)
│    ├── INSTALLATION.md ............. Instrukcja instalacji
│    ├── SUMMARY.md .................. Podsumowanie projektu
│    ├── STRUCTURE.md ................ Ten plik
│    └── START.txt ................... Informacje startowe
│
├─── 🧪 Testing
│    └── test_structure.py ........... Test walidacyjny struktury
│
├─── 📊 Dane
│    └── data/
│         └── dane.csv ............... Przykładowe dane (10 miast)
│
├─── 🌐 Frontend (Szablony)
│    └── templates/
│         ├── index.html ............ Strona główna (forma)
│         └── wynik.html ............ Strona wyników
│
└─── 🎨 Statyczne pliki
     └── static/
          ├── css/
          │   └── style.css ........ Nowoczesne style (CSS3)
          │
          ├── js/
          │   └── script.js ........ JavaScript
          │
          ├── img/
          │   └── logo.svg ......... Logo (SVG gradient)
          │
          └── exports/
              ├── wykres.png ....... Wygenerowana wizualizacja
              ├── dane.csv ......... Eksportowane dane
              └── [inne pliki] .... Inne eksporty
```

---

## 📋 Opis plików

### Pliki główne

| Plik | Opis |
|------|------|
| `app.py` | Główna aplikacja Flask - obsługuje CSV, generuje wykresy |
| `requirements.txt` | Lista bibliotek do instalacji |
| `Procfile` | Konfiguracja dla Heroku (opcjonalnie) |
| `.env` | Zmienne środowiskowe |

### Dokumentacja

| Plik | Opis |
|------|------|
| `README.md` | Pełna dokumentacja projektu |
| `QUICKSTART.md` | Szybki start w 3 krokach |
| `INSTALLATION.md` | Szczegółowa instrukcja instalacji |
| `SUMMARY.md` | Podsumowanie zmian i funkcji |

### Dane

| Plik | Opis |
|------|------|
| `data/dane.csv` | Przykładowe dane CSV (10 miast, 3 dni) |

### Szablony HTML

| Plik | Opis |
|------|------|
| `templates/index.html` | Strona główna z formularzem |
| `templates/wynik.html` | Strona wyświetlająca wynik |

### Style i skrypty

| Plik | Opis |
|------|------|
| `static/css/style.css` | Nowoczesne style (ciemny motyw) |
| `static/js/script.js` | Dodatkowy JavaScript |
| `static/img/logo.svg` | Logo aplikacji (gradient) |

### Eksporty

| Katalog | Opis |
|---------|------|
| `static/exports/` | Wszystkie wygenerowane wykresy i dane |

---

## 🔄 Przepływ danych

```
1. użytkownik
   ↓
2. index.html (formularz)
   ↓
3. app.py - route /generuj
   ↓
4. CSV (data/dane.csv) - wczytanie danych
   ↓
5. Wizualizacja (matplotlib)
   ↓
6. Zapis (static/exports/wykres.png)
   ↓
7. wynik.html (wyświetlenie)
```

---

## 🎯 Ścieżki API

| Ścieżka | Metoda | Opis |
|--------|--------|------|
| `/` | GET | Strona główna |
| `/api/dates` | GET | Dostępne daty z CSV |
| `/api/variables` | GET | Dostępne zmienne |
| `/generuj` | POST | Generuj wizualizację |
| `/wynik` | GET | Wyświetl wynik |
| `/eksportuj` | POST | Eksportuj dane CSV |
| `/health` | GET | Health check |

---

## 🎨 Kolory i motyw

| Kolor | Kod | Użycie |
|-------|-----|--------|
| Indygo | #6366f1 | Główny kolor (przyciski, linki) |
| Różowy | #ec4899 | Akcent (gradientu) |
| Złoty | #f59e0b | Accent (akcentu) |
| Zielony | #10b981 | Sukces |
| Czerwony | #ef4444 | Błąd |

---

## 📱 Responsywność

Aplikacja jest responsywna dla:
- 📱 Telefony (< 480px)
- 📱 Małe tablety (480-768px)
- 💻 Tablety (768-1024px)
- 🖥️ Komputery (> 1024px)

---

## 🔧 Zmienne CSS

W `static/css/style.css`:

```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #ec4899;
    --dark-bg: #0f172a;
    --dark-surface: #1e293b;
    --text-primary: #f1f5f9;
    --text-secondary: #cbd5e1;
}
```

Zmień te zmienne aby dostosować wygląd!

---

## 🚀 Rozwój

Aby dodać nowe funkcje:

1. **Nowe route** - W `app.py` dodaj `@app.route(...)`
2. **Nowe szablony** - W `templates/` utwórz `.html`
3. **Style** - W `static/css/style.css` dodaj CSS
4. **Logika** - W `app.py` dodaj nowe funkcje

---

## 📦 Zależności

Główne biblioteki (zobacz `requirements.txt`):
- **Flask** - Framework webowy
- **GeoPandas** - Geospatial data
- **Matplotlib** - Wizualizacja
- **Pandas** - Manipulacja danymi
- **Shapely** - Geometria

---

Gotowe! 🎉
