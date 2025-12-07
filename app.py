from flask import Flask, jsonify, render_template, redirect, url_for, request, send_file
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx
from pykrige.ok import OrdinaryKriging
import numpy as np
import seaborn as sns
import os
from datetime import date, datetime
from sqlalchemy import create_engine

app = Flask(__name__)

# Konfiguracja
DATA_DIR = "data"
PLOT_DIR = "static/exports"
CSV_FILE = os.path.join(DATA_DIR, "dane.csv")

# Upewnij się, że katalogi istnieją
os.makedirs(PLOT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

MAPA_ZMIENNYCH = {
    "pm25": ("PM25", "PM25"),
    "temp": ("temperatura", "temperatura"),
    "hum": ("wilgotnosc", "wilgotnosc")
}

def load_data():
    """Wczytaj dane z pliku CSV"""
    try:
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
        return df
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Błąd podczas wczytywania danych: {e}")
        return None

def get_available_dates():
    """Pobierz dostępne daty z danych"""
    df = load_data()
    if df is None:
        return []
    
    if 'data' in df.columns:
        try:
            dates = sorted(df['data'].unique())
            return dates
        except:
            return []
    return []

def get_available_variables():
    """Pobierz dostępne zmienne"""
    return list(MAPA_ZMIENNYCH.keys())

@app.route('/')
def index():
    dates = get_available_dates()
    variables = get_available_variables()
    return render_template('index.html', dates=dates, variables=variables)

@app.route('/api/dates')
def api_dates():
    """API endpoint do pobrania dostępnych dat"""
    dates = get_available_dates()
    return jsonify(dates)

@app.route('/api/variables')
def api_variables():
    """API endpoint do pobrania dostępnych zmiennych"""
    variables = get_available_variables()
    return jsonify(variables)

def rysuj_mape_dla_daty(data_pomiaru: str, zmienna: str = "pm25"):
    """Rysuj mapę punktów dla danej daty"""
    _, kolumna = MAPA_ZMIENNYCH[zmienna]
    
    df = load_data()
    if df is None:
        return False
    
    # Filtruj dane dla danej daty
    df_filtered = df[df['data'] == data_pomiaru].copy()
    
    if df_filtered.empty:
        print(f"Brak danych dla daty {data_pomiaru}")
        return False
    
    # Sprawdź czy kolumna istnieje
    if kolumna not in df_filtered.columns:
        print(f"Kolumna {kolumna} nie istnieje w danych")
        return False
    
    # Upewnij się, że mamy kolumny 'nazwa', 'lat', 'lon'
    if not all(col in df_filtered.columns for col in ['nazwa', 'lat', 'lon']):
        print("Brakuje wymaganych kolumn: nazwa, lat, lon")
        return False
    
    df_filtered["geometry"] = df_filtered.apply(lambda r: Point(r["lon"], r["lat"]), axis=1)
    gdf = gpd.GeoDataFrame(df_filtered, geometry="geometry", crs="EPSG:4326")

    fig, ax = plt.subplots(figsize=(14, 10), dpi=100, facecolor='white')
    ax.set_facecolor('#e8f4f8')
    
    # Set axis limits BEFORE adding basemap
    buffer = 0.1
    ax.set_xlim(gdf.geometry.x.min() - buffer, gdf.geometry.x.max() + buffer)
    ax.set_ylim(gdf.geometry.y.min() - buffer, gdf.geometry.y.max() + buffer)
    
    # Basemap OSM w EPSG:4326
    try:
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=11, alpha=0.4, crs='EPSG:4326')
    except Exception as e:
        print(f"Błąd basemapy: {e}")
    
    # Reset axis limits AFTER basemap
    ax.set_xlim(gdf.geometry.x.min() - buffer, gdf.geometry.x.max() + buffer)
    ax.set_ylim(gdf.geometry.y.min() - buffer, gdf.geometry.y.max() + buffer)
    
    # Punkty z skalą kolorów
    gdf.plot(ax=ax, column=kolumna, cmap="RdYlBu_r", legend=True, markersize=200, 
             alpha=0.95, edgecolor='white', linewidth=3, zorder=15)
    
    # Etykiety miast
    for _, row in gdf.iterrows():
        ax.text(row.geometry.x + 0.015, row.geometry.y + 0.008, row["nazwa"], 
                fontsize=11, fontweight='bold', color='darkblue',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9, edgecolor='gray', linewidth=1.5))
    
    # Legenda
    leg = ax.get_legend()
    if leg:
        leg.set_title(f"{zmienna.upper()}", prop={'size': 11, 'weight': 'bold'})
        leg.set_bbox_to_anchor((1.02, 1), loc='upper left')
        leg.frame.set_alpha(0.95)
    
    ax.grid(True, linestyle='--', alpha=0.3, color='gray')
    ax.margins(0.08)
    ax.set_xlabel('Długość geograficzna (°)', fontsize=10)
    ax.set_ylabel('Szerokość geograficzna (°)', fontsize=10)
    
    # Tytuł
    ax.set_title(f"Mapa punktów pomiarowych – {zmienna.upper()} ({data_pomiaru})", 
                 fontsize=15, fontweight='bold', pad=15)
    
    plt.tight_layout()
    return True

def rysuj_mape_idw(data_pomiaru: str, zmienna: str = "pm25"):
    """Rysuj mapę interpolacji IDW dla danej daty"""
    _, kolumna = MAPA_ZMIENNYCH[zmienna]
    
    df = load_data()
    if df is None:
        return False
    
    df_filtered = df[df['data'] == data_pomiaru].copy()
    
    if df_filtered.empty:
        print(f"Brak danych dla daty {data_pomiaru}")
        return False
    
    if kolumna not in df_filtered.columns:
        print(f"Kolumna {kolumna} nie istnieje w danych")
        return False
    
    if not all(col in df_filtered.columns for col in ['nazwa', 'lat', 'lon']):
        print("Brakuje wymaganych kolumn")
        return False
    
    df_filtered["geometry"] = df_filtered.apply(lambda row: Point(row["lon"], row["lat"]), axis=1)
    gdf = gpd.GeoDataFrame(df_filtered, geometry="geometry", crs="EPSG:4326")
    
    # Użyj współrzędnych geograficznych (lat/lon) do interpolacji
    x = gdf.geometry.x.values  # longitude
    y = gdf.geometry.y.values  # latitude
    z = gdf[kolumna].values

    # Buffer w stopniach geograficznych (~1 stopień ≈ 111 km)
    buffer = 0.1  # ~11 km
    grid_x = np.linspace(x.min() - buffer, x.max() + buffer, 150)
    grid_y = np.linspace(y.min() - buffer, y.max() + buffer, 150)
    grid_x, grid_y = np.meshgrid(grid_x, grid_y)

    def idw(xi, yi, x, y, z, power=2):
        dist = np.sqrt((x - xi) ** 2 + (y - yi) ** 2)
        dist[dist == 0] = 1e-10
        weights = 1 / dist ** power
        return np.sum(weights * z) / np.sum(weights)

    zgrid = np.zeros_like(grid_x)
    for i in range(grid_x.shape[0]):
        for j in range(grid_x.shape[1]):
            zgrid[i, j] = idw(grid_x[i, j], grid_y[i, j], x, y, z)

    fig, ax = plt.subplots(figsize=(14, 10), dpi=100, facecolor='white')
    ax.set_facecolor('white')
    
    # Set axis limits BEFORE adding basemap
    ax.set_xlim(grid_x.min(), grid_x.max())
    ax.set_ylim(grid_y.min(), grid_y.max())
    
    # Basemap OSM w EPSG:4326
    try:
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=11, alpha=0.35, crs='EPSG:4326')
    except Exception as e:
        print(f"Błąd basemapy: {e}")
    
    # Reset axis limits AFTER basemap
    ax.set_xlim(grid_x.min(), grid_x.max())
    ax.set_ylim(grid_y.min(), grid_y.max())
    
    # Heatmap na górze z przezroczystością
    im = ax.imshow(
        zgrid,
        extent=(grid_x.min(), grid_x.max(), grid_y.min(), grid_y.max()),
        origin='lower',
        cmap='RdYlBu_r',
        alpha=0.6,
        vmin=z.min(),
        vmax=z.max(),
        zorder=5
    )
    
    # Punkty pomiarowe
    ax.scatter(x, y, c='darkblue', s=120, edgecolors='white', linewidth=2.5, zorder=15, marker='o')
    
    # Etykiety miast
    for _, row in gdf.iterrows():
        ax.text(row.geometry.x + 0.015, row.geometry.y + 0.008, row["nazwa"], 
                fontsize=9, color='darkblue', fontweight='bold', zorder=20,
                bbox=dict(boxstyle='round,pad=0.35', facecolor='white', alpha=0.95, edgecolor='gray', linewidth=1.5))
    
    # Mapa kolorów
    cbar = plt.colorbar(im, ax=ax, label=f"{zmienna.upper()} (IDW)", pad=0.02, shrink=0.9)
    cbar.ax.tick_params(labelsize=9)
    
    # Tytuł
    ax.set_title(f"Interpolacja {zmienna.upper()} metodą IDW – {data_pomiaru}", 
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Długość geograficzna (°)', fontsize=10)
    ax.set_ylabel('Szerokość geograficzna (°)', fontsize=10)
    plt.tight_layout()
    return True

def rysuj_mape_kriging(data_pomiaru: str, zmienna: str = "pm25"):
    """Rysuj mapę interpolacji Kriging dla danej daty"""
    _, kolumna = MAPA_ZMIENNYCH[zmienna]
    
    df = load_data()
    if df is None:
        return False
    
    df_filtered = df[df['data'] == data_pomiaru].copy()
    
    if df_filtered.empty:
        print(f"Brak danych dla daty {data_pomiaru}")
        return False
    
    if kolumna not in df_filtered.columns:
        print(f"Kolumna {kolumna} nie istnieje w danych")
        return False
    
    if not all(col in df_filtered.columns for col in ['nazwa', 'lat', 'lon']):
        print("Brakuje wymaganych kolumn")
        return False
    
    # Przygotuj dane
    df_filtered["geometry"] = df_filtered.apply(lambda row: Point(row["lon"], row["lat"]), axis=1)
    gdf = gpd.GeoDataFrame(df_filtered, geometry="geometry", crs="EPSG:4326")
    
    # Użyj współrzędnych geograficznych (lat/lon) do interpolacji
    x = gdf.geometry.x.values.astype(float)  # longitude
    y = gdf.geometry.y.values.astype(float)  # latitude
    z = gdf[kolumna].values.astype(float)
    
    # Utwórz grid w współrzędnych geograficznych
    buffer = 0.1  # ~11 km
    xi = np.linspace(x.min() - buffer, x.max() + buffer, 120)
    yi = np.linspace(y.min() - buffer, y.max() + buffer, 120)
    XI, YI = np.meshgrid(xi, yi)
    
    # Kriging - prosta implementacja
    try:
        ok = OrdinaryKriging(
            x, y, z,
            variogram_model='spherical',
            verbose=False,
            enable_plotting=False,
            nlags=6
        )
        zi, ss = ok.execute('grid', xi, yi)
    except Exception as e:
        print(f"Błąd Kringinga: {e}, używam IDW")
        # Fallback do IDW
        zi = np.zeros_like(XI)
        for i in range(XI.shape[0]):
            for j in range(XI.shape[1]):
                # IDW
                distances = np.sqrt((x - XI[i, j])**2 + (y - YI[i, j])**2)
                distances = np.where(distances < 1e-6, 1e-6, distances)
                weights = 1.0 / distances**2
                zi[i, j] = np.sum(weights * z) / np.sum(weights)
    
    # Rysowanie
    fig, ax = plt.subplots(figsize=(14, 10), dpi=100, facecolor='white')
    ax.set_facecolor('white')
    
    # Set axis limits BEFORE adding basemap
    ax.set_xlim(XI.min(), XI.max())
    ax.set_ylim(YI.min(), YI.max())
    
    # Basemap OSM w EPSG:4326
    try:
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=11, alpha=0.35, crs='EPSG:4326')
    except Exception as e:
        print(f"Błąd basemapy: {e}")
    
    # Reset axis limits AFTER basemap
    ax.set_xlim(XI.min(), XI.max())
    ax.set_ylim(YI.min(), YI.max())
    
    # Heatmap na górze z przezroczystością
    im = ax.contourf(XI, YI, zi, levels=15, cmap='RdYlBu_r', alpha=0.6, zorder=5)
    cs = ax.contour(XI, YI, zi, levels=8, colors='gray', alpha=0.4, linewidths=0.7, zorder=6)
    
    # Punkty pomiarowe
    scatter = ax.scatter(x, y, c=z, s=180, cmap='RdYlBu_r', edgecolors='white', 
                        linewidth=2.5, zorder=15, vmin=z.min(), vmax=z.max())
    
    # Etykiety miast
    for idx, row in gdf.iterrows():
        ax.text(row.geometry.x + 0.015, row.geometry.y + 0.008, row["nazwa"],
                fontsize=9, color='darkblue', fontweight='bold', zorder=20,
                bbox=dict(boxstyle='round,pad=0.35', facecolor='white', alpha=0.95, edgecolor='gray', linewidth=1.5))
    
    # Kolorbar
    cbar = plt.colorbar(scatter, ax=ax, label=f"{zmienna.upper()}", pad=0.02, shrink=0.9)
    cbar.ax.tick_params(labelsize=9)
    
    # Tytuł
    ax.set_title(f"Interpolacja {zmienna.upper()} metodą Kriging – {data_pomiaru}",
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Długość geograficzna (°)', fontsize=10)
    ax.set_ylabel('Szerokość geograficzna (°)', fontsize=10)
    ax.grid(True, alpha=0.2, linestyle='--')
    
    plt.tight_layout()
    return True

def rysuj_wykresy_dla_daty(data_pomiaru: str, zmienna: str = "pm25"):
    """Rysuj wykresy statystyczne dla danej daty"""
    _, kolumna = MAPA_ZMIENNYCH[zmienna]
    
    df = load_data()
    if df is None:
        return False
    
    df_filtered = df[df['data'] == data_pomiaru].copy()
    
    if df_filtered.empty:
        print(f"Brak danych dla daty {data_pomiaru}")
        return False
    
    if kolumna not in df_filtered.columns:
        print(f"Kolumna {kolumna} nie istnieje w danych")
        return False
    
    if 'nazwa' not in df_filtered.columns:
        print("Brakuje kolumny 'nazwa'")
        return False
    
    sns.set_style("whitegrid", {'grid.color': '0.9'})
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.5), dpi=100, facecolor='white')
    fig.suptitle(f"Analiza {zmienna.upper()} – {data_pomiaru}", fontsize=16, fontweight='bold', y=1.00)

    # Wykres słupkowy
    sns.barplot(data=df_filtered, x="nazwa", y=kolumna, ax=axs[0], palette="RdYlBu_r", 
                order=df_filtered.sort_values(kolumna, ascending=False)["nazwa"])
    axs[0].set_title(f"Wartości {zmienna.upper()}", fontsize=12, fontweight='bold', pad=12)
    axs[0].set_xlabel("Miasto", fontsize=10, fontweight='bold')
    axs[0].set_ylabel(f"{zmienna.upper()}", fontsize=10, fontweight='bold')
    axs[0].set_xticklabels(axs[0].get_xticklabels(), rotation=45, ha='right', fontsize=9)
    axs[0].grid(axis='y', alpha=0.3)
    axs[0].set_facecolor('#f9f9f9')

    # Wykres liniowy
    sorted_data = df_filtered.sort_values(kolumna, ascending=False)
    axs[1].plot(sorted_data["nazwa"], sorted_data[kolumna], marker="o", markersize=7, 
                linewidth=2, color='#2563eb', markerfacecolor='#dbeafe', markeredgecolor='#2563eb', markeredgewidth=1.5)
    axs[1].set_title(f"Trend {zmienna.upper()}", fontsize=12, fontweight='bold', pad=12)
    axs[1].set_xlabel("Miasto", fontsize=10, fontweight='bold')
    axs[1].set_ylabel(f"{zmienna.upper()}", fontsize=10, fontweight='bold')
    axs[1].set_xticklabels(sorted_data["nazwa"], rotation=45, ha='right', fontsize=9)
    axs[1].grid(True, alpha=0.3, linestyle='--')
    axs[1].set_facecolor('#f9f9f9')

    # Wykres pudełkowy
    bp = axs[2].boxplot([df_filtered[kolumna]], widths=0.5, patch_artist=True, 
                         labels=[zmienna.upper()],
                         boxprops=dict(facecolor='#3b82f6', alpha=0.7),
                         medianprops=dict(color='red', linewidth=2),
                         whiskerprops=dict(linewidth=1.5),
                         capprops=dict(linewidth=1.5))
    axs[2].set_title(f"Rozkład {zmienna.upper()}", fontsize=12, fontweight='bold', pad=12)
    axs[2].set_ylabel(f"{zmienna.upper()}", fontsize=10, fontweight='bold')
    axs[2].grid(axis='y', alpha=0.3)
    axs[2].set_facecolor('#f9f9f9')
    
    # Dodaj statystyki na ostatnim wykresie
    stats_text = f"Min: {df_filtered[kolumna].min():.1f}\nMaks: {df_filtered[kolumna].max():.1f}\nŚr: {df_filtered[kolumna].mean():.1f}"
    axs[2].text(1.25, df_filtered[kolumna].min(), stats_text, fontsize=9, 
                bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    return True

@app.route('/generuj', methods=['POST'])
def generuj():
    """Generuj wizualizację na podstawie wybranych parametrów"""
    data = request.form.get('data', '').strip()
    zmienna = request.form.get('zmienna', 'pm25').strip()
    metoda = request.form.get('metoda', 'mapa').strip()

    if not data:
        return jsonify({'status': 'error', 'message': 'Data pomiaru jest wymagana'}), 400
    
    if zmienna not in MAPA_ZMIENNYCH:
        return jsonify({'status': 'error', 'message': 'Nieprawidłowa zmienna'}), 400

    if metoda not in ['mapa', 'idw', 'kriging', 'wykres']:
        return jsonify({'status': 'error', 'message': 'Nieprawidłowa metoda'}), 400

    try:
        output_path = os.path.join(PLOT_DIR, "wykres.png")

        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        if metoda == "mapa":
            success = rysuj_mape_dla_daty(data, zmienna)
        elif metoda == "idw":
            success = rysuj_mape_idw(data, zmienna)
        elif metoda == "kriging":
            success = rysuj_mape_kriging(data, zmienna)
        elif metoda == "wykres":
            success = rysuj_wykresy_dla_daty(data, zmienna)

        if not success:
            plt.close('all')
            return jsonify({'status': 'error', 'message': 'Brak danych dla wybranych parametrów'}), 404

        plt.savefig(output_path, dpi=100, bbox_inches='tight', pad_inches=0.2)
        plt.close('all')

        return redirect(url_for('wynik', data=data, zmienna=zmienna, metoda=metoda))

    except Exception as e:
        app.logger.error(f"Błąd podczas generowania wykresu: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Błąd: {str(e)}'}), 500

@app.route('/wynik')
def wynik():
    """Wyświetl wynik wizualizacji"""
    data = request.args.get('data', '')
    zmienna = request.args.get('zmienna', 'pm25')
    metoda = request.args.get('metoda', 'mapa')
    
    return render_template(
        'wynik.html',
        obraz=url_for('static', filename='exports/wykres.png'),
        data=data,
        zmienna=zmienna,
        metoda=metoda
    )

@app.route('/eksportuj', methods=['POST'])
def eksportuj():
    """Eksportuj dane do CSV"""
    zmienna = request.form.get('zmienna', 'pm25')
    
    try:
        df = load_data()
        if df is None:
            return jsonify({'status': 'error', 'message': 'Brak danych'}), 500
        
        # Utwórz nazwę pliku
        filename = f"{zmienna}_export_{date.today()}.csv"
        filepath = os.path.join(PLOT_DIR, filename)
        
        df.to_csv(filepath, index=False)
        
        return jsonify({
            'status': 'success',
            'message': f'Dane zostały zapisane jako {filename}',
            'filename': filename,
            'download_url': url_for('static', filename=f'exports/{filename}')
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/generuj_pdf', methods=['POST'])
def generuj_pdf():
    """Generuj raport PDF z wizualizacją"""
    try:
        data = request.json
        data_pomiaru = data.get('data')
        zmienna = data.get('zmienna')
        metoda = data.get('metoda')
        
        if not all([data_pomiaru, zmienna, metoda]):
            return jsonify({'status': 'error', 'message': 'Brakuje wymaganych parametrów'}), 400
        
        # Wczytaj dane
        df = load_data()
        if df is None:
            return jsonify({'status': 'error', 'message': 'Nie udało się wczytać danych'}), 500
        
        df_filtered = df[df['data'] == data_pomiaru].copy()
        if df_filtered.empty:
            return jsonify({'status': 'error', 'message': 'Brak danych dla wybranej daty'}), 404
        
        # Przygotuj dane do raportu
        _, kolumna = MAPA_ZMIENNYCH[zmienna]
        
        stats_html = ""
        if kolumna in df_filtered.columns:
            # Oblicz metryki statystyczne
            values = df_filtered[kolumna]
            min_val = values.min()
            max_val = values.max()
            mean_val = values.mean()
            median_val = values.median()
            std_val = values.std()
            q1_val = values.quantile(0.25)
            q3_val = values.quantile(0.75)
            iqr_val = q3_val - q1_val
            var_val = values.var()
            cv_val = (std_val / mean_val * 100) if mean_val != 0 else 0
            
            stats_html = f"""
            <h2>Statystyki Danych</h2>
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <tr style="background-color: #f0f9ff;">
                    <td colspan="2" style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold; text-align: center; background-color: #3b82f6; color: white;">Miary Tendencji Centralnej</td>
                </tr>
                <tr style="background-color: #f3f4f6;">
                    <td style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold; width: 50%;">Średnia (Mean):</td>
                    <td style="border: 1px solid #e5e7eb; padding: 10px;">{mean_val:.4f}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold;">Mediana (Median):</td>
                    <td style="border: 1px solid #e5e7eb; padding: 10px;">{median_val:.4f}</td>
                </tr>
                
                <tr style="background-color: #f0f9ff;">
                    <td colspan="2" style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold; text-align: center; background-color: #3b82f6; color: white;">Miary Rozproszenia</td>
                </tr>
                <tr style="background-color: #f3f4f6;">
                    <td style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold;">Minimalna wartość (Min):</td>
                    <td style="border: 1px solid #e5e7eb; padding: 10px;">{min_val:.4f}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold;">Maksymalna wartość (Max):</td>
                    <td style="border: 1px solid #e5e7eb; padding: 10px;">{max_val:.4f}</td>
                </tr>
                <tr style="background-color: #f3f4f6;">
                    <td style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold;">Zakres (Range):</td>
                    <td style="border: 1px solid #e5e7eb; padding: 10px;">{max_val - min_val:.4f}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold;">Odchylenie Standardowe (Std Dev):</td>
                    <td style="border: 1px solid #e5e7eb; padding: 10px;">{std_val:.4f}</td>
                </tr>
                <tr style="background-color: #f3f4f6;">
                    <td style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold;">Wariancja (Variance):</td>
                    <td style="border: 1px solid #e5e7eb; padding: 10px;">{var_val:.4f}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold;">Współczynnik Zmienności (CV %):</td>
                    <td style="border: 1px solid #e5e7eb; padding: 10px;">{cv_val:.2f}%</td>
                </tr>
                
                <tr style="background-color: #f0f9ff;">
                    <td colspan="2" style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold; text-align: center; background-color: #3b82f6; color: white;">Kwartyle i Percentyle</td>
                </tr>
                <tr style="background-color: #f3f4f6;">
                    <td style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold;">Q1 (25. percentyl):</td>
                    <td style="border: 1px solid #e5e7eb; padding: 10px;">{q1_val:.4f}</td>
                </tr>
                <tr>
                    <td style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold;">Q3 (75. percentyl):</td>
                    <td style="border: 1px solid #e5e7eb; padding: 10px;">{q3_val:.4f}</td>
                </tr>
                <tr style="background-color: #f3f4f6;">
                    <td style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold;">IQR (Rozstęp międzykwartylowy):</td>
                    <td style="border: 1px solid #e5e7eb; padding: 10px;">{iqr_val:.4f}</td>
                </tr>
                
                <tr style="background-color: #f0f9ff;">
                    <td colspan="2" style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold; text-align: center; background-color: #3b82f6; color: white;">Liczebność Próby</td>
                </tr>
                <tr style="background-color: #f3f4f6;">
                    <td style="border: 1px solid #e5e7eb; padding: 10px; font-weight: bold;">Liczba obserwacji (N):</td>
                    <td style="border: 1px solid #e5e7eb; padding: 10px;">{len(df_filtered)}</td>
                </tr>
            </table>
            """
        
        # Przygotuj obrazek
        viz_image_path = os.path.join(PLOT_DIR, "wykres.png")
        img_html = ""
        if os.path.exists(viz_image_path):
            img_html = f'<img src="{os.path.abspath(viz_image_path)}" style="width: 100%; max-width: 600px; margin: 20px 0;">'
        
        # Utwórz HTML
        html_content = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    color: #1f2937;
                    line-height: 1.6;
                    margin: 20px;
                }}
                h1 {{
                    color: #1f2937;
                    text-align: center;
                    font-size: 24px;
                    margin-bottom: 30px;
                }}
                h2 {{
                    color: #374151;
                    font-size: 14px;
                    margin-top: 20px;
                    margin-bottom: 12px;
                }}
                .metadata {{
                    background-color: #f3f4f6;
                    border: 1px solid #d1d5db;
                    border-radius: 4px;
                    padding: 15px;
                    margin-bottom: 20px;
                }}
                .metadata-row {{
                    display: flex;
                    margin: 8px 0;
                }}
                .metadata-label {{
                    font-weight: bold;
                    width: 150px;
                }}
                table {{
                    width: 100%;
                }}
            </style>
        </head>
        <body>
            <h1>silesiaAIR - Raport Wizualizacji Danych</h1>
            
            <div class="metadata">
                <div class="metadata-row">
                    <span class="metadata-label">Data:</span>
                    <span>{data_pomiaru}</span>
                </div>
                <div class="metadata-row">
                    <span class="metadata-label">Zmienna:</span>
                    <span>{zmienna.upper()}</span>
                </div>
                <div class="metadata-row">
                    <span class="metadata-label">Metoda:</span>
                    <span>{metoda.upper()}</span>
                </div>
                <div class="metadata-row">
                    <span class="metadata-label">Data raportu:</span>
                    <span>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
                </div>
            </div>
            
            {stats_html}
            
            <h2>Wizualizacja</h2>
            {img_html}
            
            <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #d1d5db; color: #6b7280; font-size: 12px; text-align: center;">
                &copy; 2025 silesiaAIR. Wizualizacja Danych Geoprzestrzennych dla GZM.
            </footer>
        </body>
        </html>
        """
        
        # Zapisz HTML tymczasowo
        html_filename = f"raport_{zmienna}_{data_pomiaru}.html"
        html_path = os.path.join(PLOT_DIR, html_filename)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Konwertuj do PDF
        pdf_filename = f"raport_{zmienna}_{data_pomiaru}.pdf"
        pdf_path = os.path.join(PLOT_DIR, pdf_filename)
        
        try:
            import pdfkit
            pdfkit.from_file(html_path, pdf_path, options={
                'encoding': 'UTF-8',
                'quiet': '',
                'enable-local-file-access': None,
                'margin-top': '0.5in',
                'margin-bottom': '0.5in',
                'margin-left': '0.5in',
                'margin-right': '0.5in'
            })
        except Exception as e:
            app.logger.warning(f"pdfkit nie zadziałał ({e}), próbuję alternatywną metodę")
            # Fallback - użyj reportlab z prostszym podejściem
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
            
            doc = SimpleDocTemplate(pdf_path, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
            story = []
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f2937'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#374151'),
                spaceAfter=12,
                fontName='Helvetica-Bold'
            )
            
            story.append(Paragraph("silesiaAIR - Raport Wizualizacji Danych", title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Metadane
            metadata_data = [
                ['Data:', data_pomiaru],
                ['Zmienna:', zmienna.upper()],
                ['Metoda:', metoda.upper()],
                ['Data raportu:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            ]
            metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
            metadata_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
            ]))
            story.append(metadata_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Statystyki danych
            if kolumna in df_filtered.columns:
                values = df_filtered[kolumna]
                min_val = values.min()
                max_val = values.max()
                mean_val = values.mean()
                median_val = values.median()
                std_val = values.std()
                q1_val = values.quantile(0.25)
                q3_val = values.quantile(0.75)
                iqr_val = q3_val - q1_val
                var_val = values.var()
                cv_val = (std_val / mean_val * 100) if mean_val != 0 else 0
                
                story.append(Paragraph("Miary Tendencji Centralnej", heading_style))
                stats_data_1 = [
                    ['Średnia (Mean):', f"{mean_val:.4f}"],
                    ['Mediana (Median):', f"{median_val:.4f}"]
                ]
                stats_table_1 = Table(stats_data_1, colWidths=[2.5*inch, 3.5*inch])
                stats_table_1.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
                ]))
                story.append(stats_table_1)
                story.append(Spacer(1, 0.2*inch))
                
                story.append(Paragraph("Miary Rozproszenia", heading_style))
                stats_data_2 = [
                    ['Minimalna wartość (Min):', f"{min_val:.4f}"],
                    ['Maksymalna wartość (Max):', f"{max_val:.4f}"],
                    ['Zakres (Range):', f"{max_val - min_val:.4f}"],
                    ['Odchylenie Standardowe (Std Dev):', f"{std_val:.4f}"],
                    ['Wariancja (Variance):', f"{var_val:.4f}"],
                    ['Współczynnik Zmienności (CV %):', f"{cv_val:.2f}%"]
                ]
                stats_table_2 = Table(stats_data_2, colWidths=[2.5*inch, 3.5*inch])
                stats_table_2.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
                ]))
                story.append(stats_table_2)
                story.append(Spacer(1, 0.2*inch))
                
                story.append(Paragraph("Kwartyle i Percentyle", heading_style))
                stats_data_3 = [
                    ['Q1 (25. percentyl):', f"{q1_val:.4f}"],
                    ['Q3 (75. percentyl):', f"{q3_val:.4f}"],
                    ['IQR (Rozstęp międzykwartylowy):', f"{iqr_val:.4f}"],
                    ['Liczba obserwacji (N):', str(len(df_filtered))]
                ]
                stats_table_3 = Table(stats_data_3, colWidths=[2.5*inch, 3.5*inch])
                stats_table_3.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
                ]))
                story.append(stats_table_3)
                story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(f"Metoda: {metoda}", heading_style))
            story.append(Spacer(1, 0.3*inch))
            
            if os.path.exists(viz_image_path):
                story.append(PageBreak())
                story.append(Paragraph("Wizualizacja", heading_style))
                story.append(Spacer(1, 0.2*inch))
                img = Image(viz_image_path, width=6.5*inch, height=4.875*inch)
                story.append(img)
            
            doc.build(story)
        
        # Usuń plik HTML
        try:
            os.remove(html_path)
        except:
            pass
        
        return jsonify({
            'status': 'success',
            'message': f'Raport PDF został wygenerowany',
            'filename': pdf_filename,
            'download_url': url_for('pobierz_pdf', filename=pdf_filename)
        })
    
    except Exception as e:
        app.logger.error(f"Błąd podczas generowania PDF: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/pobierz_pdf/<filename>')
def pobierz_pdf(filename):
    """Pobierz plik PDF"""
    try:
        filepath = os.path.join(PLOT_DIR, filename)
        if not os.path.exists(filepath):
            return jsonify({'status': 'error', 'message': 'Plik nie znaleziony'}), 404
        
        return send_file(filepath, mimetype='application/pdf', as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
