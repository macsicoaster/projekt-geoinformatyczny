# 📋 INSTRUKCJA INSTALACJI - GeoViz v2

## Projekt został pomyślnie utworzony! 🎉

Nowa, nowoczesna wersja aplikacji GeoViz znajduje się w folderze:
```
d:\projekt-geoinformatyczny-v2
```

---

## ✨ Co zostało zmienione?

### ✅ Usunięto Azure
- Aplikacja nie wymaga już Azure Storage
- Dane zapisywane są lokalnie w folderze `static/exports/`

### ✅ Zmiana źródła danych
- ❌ Już nie odczytuje z bazy danych PostgreSQL
- ✅ Teraz odczytuje z pliku CSV (`data/dane.csv`)

### ✅ Nowoczesny interfejs
- 🎨 Ciemny motyw z gradientami
- 📱 Responsywny design (działa na mobilnych)
- 🖼️ Miejsce na logo w nagłówku
- ✨ Gładkie animacje i przejścia
- 🌙 Profesjonalny wygląd

### ✅ Wizualizacje zachowane
- 🗺️ Mapa punktów
- 📊 Interpolacja IDW
- 🔮 Kriging
- 📈 Wykresy statystyczne

---

## 🚀 SZYBKI START

### 1️⃣ Zainstaluj zależności
```bash
cd d:\projekt-geoinformatyczny-v2
pip install -r requirements.txt
```

### 2️⃣ Uruchom aplikację
```bash
python app.py
```

### 3️⃣ Otwórz w przeglądarce
```
http://localhost:5000
```

---

## 📁 Struktura projektu

```
projekt-geoinformatyczny-v2/
│
├── app.py                          ← Główna aplikacja Flask
├── requirements.txt                ← Zależności
├── README.md                       ← Pełna dokumentacja
├── QUICKSTART.md                   ← Szybki start
├── Procfile                        ← Deploy na Heroku
│
├── data/
│   └── dane.csv                    ← 📊 Dane (CSV format)
│
├── templates/
│   ├── index.html                  ← Strona główna z formularzem
│   └── wynik.html                  ← Strona wyników
│
└── static/
    ├── css/
    │   └── style.css               ← Nowoczesne style (CSS3)
    ├── js/
    │   └── script.js               ← JavaScript
    ├── img/
    │   └── logo.svg                ← Logo (SVG)
    └── exports/                    ← Wyeksportowane wykresy
```

---

## 📊 Format pliku CSV

Plik `dane.csv` zawiera przykładowe dane dla 10 polskich miast.

**Wymagane kolumny:**
| Kolumna | Typ | Przykład |
|---------|-----|---------|
| nazwa | tekst | Warszawa |
| lat | liczba | 52.2297 |
| lon | liczba | 21.0122 |
| data | data | 2024-01-15 |
| PM25 | liczba | 28.5 |
| temperatura | liczba | 5.2 |
| wilgotnosc | liczba | 65 |

---

## 🎨 Dostosowanie do swoich potrzeb

### Zmiana logo
Zamiast domyślnego logo, umieść swoje w:
```
static/img/logo.svg
```

### Wgranie własnych danych
1. Przygotuj plik CSV z danymi
2. Umieść go w folderze `data/` jako `dane.csv`
3. Uruchom aplikację - dane zostaną automatycznie wczytane

### Zmiana kolorów
W pliku `static/css/style.css` zmień zmienne CSS:
```css
:root {
    --primary-color: #6366f1;      /* Zmień na swój kolor */
    --secondary-color: #ec4899;    /* Zmień na swój kolor */
    ...
}
```

---

## 🔧 Zmienne środowiskowe

Aplikacja korzysta z pliku `.env`:
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-this
```

---

## 📌 Główne funkcje aplikacji

1. **Strona główna** (`/`)
   - Wybór daty z dostępnych w CSV
   - Wybór zmiennej (PM25, temperatura, wilgotność)
   - Wybór metody wizualizacji
   - Przycisk generowania wizualizacji
   - Przycisk eksportu danych

2. **Generowanie wizualizacji** (`/generuj`)
   - Odczytuje dane z CSV
   - Generuje mapę lub wykresy
   - Zapisuje obraz do `static/exports/`

3. **Wyświetlanie wyniku** (`/wynik`)
   - Pokazuje wygenerowaną wizualizację
   - Przycisk pobrania obrazu
   - Przycisk drukowania
   - Opis użytej metody

4. **Eksport danych** (`/eksportuj`)
   - Eksportuje dane do CSV
   - Udostępnia do pobrania

---

## ✅ Cechy nowoczesnego interfejsu

- 🌙 **Ciemny motyw** - Wygodny dla oczu
- 📱 **Responsywny** - Działa na telefonach
- ♿ **Dostępny** - Dobre kontrastu i czcionki
- 🎨 **Estetyczny** - Gradientu i efekty wizualne
- ⚡ **Szybki** - Animacje fluid 60fps
- 🖼️ **Nowoczesny** - CSS3, HTML5

---

## 🆘 Rozwiązywanie problemów

### ❌ "No module named 'geopandas'"
```bash
pip install -r requirements.txt
```

### ❌ "Brak danych dla wybranej daty"
- Sprawdź czy plik CSV ma dane dla tej daty
- Sprawdź format daty (powinno być YYYY-MM-DD)

### ❌ "Port 5000 jest już zajęty"
W aplikacji zmień port w ostatniej linii app.py:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Zmień na 5001
```

### ❌ "Błędy przy importowaniu bibliotek"
Upewnij się, że jesteś w poprawnym wirtualnym środowisku i zainstaluj ponownie:
```bash
pip install --upgrade -r requirements.txt
```

---

## 📚 Dokumentacja

- **README.md** - Pełna dokumentacja projektu
- **QUICKSTART.md** - Szybki start
- Komentarze w kodzie - Wyjaśnienia funkcji

---

## 🎯 Następne kroki

1. ✅ Zainstaluj zależności
2. ✅ Uruchom aplikację
3. ✅ Przetestuj z przykładowymi danymi
4. ✅ Dodaj swoje dane CSV
5. ✅ Dostosuj wygląd (kolory, logo)

---

## 📧 Wsparcie

Jeśli masz pytania, sprawdź:
- Dokumentację bibliotek (GeoPandas, Flask, Matplotlib)
- Komentarze w kodzie
- README.md dla szczegółów

---

**Gotowe do użycia! Powodzenia! 🚀**
