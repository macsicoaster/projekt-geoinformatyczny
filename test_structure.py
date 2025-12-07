"""
Test pliku - sprawdzenie czy aplikacja się poprawnie ładuje
"""

import os
import sys

def check_structure():
    """Sprawdzenie struktury katalogów"""
    print("🔍 Sprawdzanie struktury projektu...\n")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'templates/index.html',
        'templates/wynik.html',
        'static/css/style.css',
        'data/dane.csv'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - BRAKUJE!")
            all_ok = False
    
    print()
    
    required_dirs = [
        'data',
        'templates',
        'static',
        'static/css',
        'static/js',
        'static/img',
        'static/exports'
    ]
    
    for dir in required_dirs:
        if os.path.isdir(dir):
            print(f"✅ {dir}/")
        else:
            print(f"❌ {dir}/ - BRAKUJE!")
            all_ok = False
    
    print()
    return all_ok

def check_imports():
    """Sprawdzenie czy można załadować aplikację Flask"""
    print("🔍 Sprawdzanie importów...\n")
    
    try:
        import flask
        print("✅ Flask")
    except ImportError:
        print("❌ Flask - zainstaluj: pip install flask")
    
    try:
        import geopandas
        print("✅ GeoPandas")
    except ImportError:
        print("❌ GeoPandas - zainstaluj: pip install geopandas")
    
    try:
        import pandas
        print("✅ Pandas")
    except ImportError:
        print("❌ Pandas - zainstaluj: pip install pandas")
    
    try:
        import matplotlib
        print("✅ Matplotlib")
    except ImportError:
        print("❌ Matplotlib - zainstaluj: pip install matplotlib")
    
    try:
        import shapely
        print("✅ Shapely")
    except ImportError:
        print("❌ Shapely - zainstaluj: pip install shapely")
    
    print()

def check_data():
    """Sprawdzenie pliku CSV"""
    print("🔍 Sprawdzanie danych CSV...\n")
    
    if not os.path.exists('data/dane.csv'):
        print("❌ Plik data/dane.csv nie istnieje!")
        return False
    
    try:
        import pandas as pd
        df = pd.read_csv('data/dane.csv')
        print(f"✅ Plik CSV wczytany pomyślnie")
        print(f"   Liczba wierszy: {len(df)}")
        print(f"   Liczba kolumn: {len(df.columns)}")
        print(f"   Kolumny: {', '.join(df.columns)}")
        print()
        
        required_columns = ['nazwa', 'lat', 'lon', 'data', 'PM25', 'temperatura', 'wilgotnosc']
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            print(f"❌ Brakujące kolumny: {', '.join(missing)}")
            return False
        else:
            print("✅ Wszystkie wymagane kolumny są obecne")
        
        print()
        return True
    except Exception as e:
        print(f"❌ Błąd podczas czytania CSV: {e}")
        return False

def main():
    """Główna funkcja testowa"""
    print("=" * 50)
    print("  🚀 GeoViz - Test Struktury Projektu")
    print("=" * 50)
    print()
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
    
    structure_ok = check_structure()
    check_imports()
    data_ok = check_data()
    
    print("=" * 50)
    if structure_ok and data_ok:
        print("✅ WSZYSTKO OK! Możesz uruchomić: python app.py")
    else:
        print("⚠️  Są problemy - rozwiąż je zgodnie z komunikatami wyżej")
    print("=" * 50)

if __name__ == '__main__':
    main()
