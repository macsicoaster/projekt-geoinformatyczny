import csv
import random
from datetime import datetime, timedelta
import argparse

# Lista miast GZM (Górnośląsko-Zagłębiowska Metropolia)
CITIES = [
    ('Katowice',       50.2643, 19.0235),   # zgodnie z danymi GPS :contentReference[oaicite:0]{index=0}
    ('Sosnowiec',      50.2779, 19.1267),   # :contentReference[oaicite:1]{index=1}
    ('Dąbrowa Górnicza', 50.3215, 19.1949), # np. 50.3216897,19.1949126 :contentReference[oaicite:2]{index=2}
    ('Czeladź',        50.3173, 19.0705),   # brak jednoznacznego źródła — poprzednie ~50.3019,19.0944; do zweryfikowania ręcznie
    ('Mysłowice',      50.2422, 19.1383),   # przyjmijmy ~50.240,19.133 — zgodnie z przybliżonymi danymi w tabelach regionalnych :contentReference[oaicite:3]{index=3}
    ('Piekary Śląskie',50.3802, 18.9265),   # :contentReference[oaicite:4]{index=4}
    ('Chorzów',        50.3058, 18.9742),   # :contentReference[oaicite:5]{index=5}
    ('Bytom',          50.3500, 18.9100),   # przybliżone; źródła pokazują między 50.34-50.35 N i 18.91 E (np. wg tabel miejskich) :contentReference[oaicite:6]{index=6}
    ('Zabrze',         50.3249, 18.7858),   # :contentReference[oaicite:7]{index=7}
    ('Gliwice',        50.3100, 18.6700),   # przybliżone — dane atlasowe/regionalne sugerują ~50.31,18.67 :contentReference[oaicite:8]{index=8}
    ('Mikołów',        50.1790, 18.9040),   # przybliżone; bazując na pozycji między Katowicami i okolicznymi miasteczkami (do sprawdzenia) :contentReference[oaicite:9]{index=9}
    ('Ruda Śląska',    50.2584, 18.8563),   # :contentReference[oaicite:10]{index=10}
    ('Tarnowskie Góry',50.4455, 18.8615),   # :contentReference[oaicite:11]{index=11}
    ('Pyskowice',      50.3956, 18.6345),   # poprzednia 50.3972,19.2458 wydaje się błędna (zbyt duża długość E); sugeruję manualne sprawdzenie — oficjalne online dane są sprzeczne
]



class AtmosphericDataGenerator:
    """Generator fałszywych danych atmosferycznych dla miast GZM."""
    
    def __init__(self):
        """Inicjalizuje generator z listą miast GZM."""
        self.cities = CITIES
        print(f"Wczytano {len(self.cities)} miast z Górnośląsko-Zagłębiowskiej Metropolii\n")
    
    def generate_value(self, previous_value, min_val, max_val):
        """Generuje wartość z zmiennością ±5% od poprzedniej."""
        variation = random.uniform(0.95, 1.05)
        new_value = previous_value * variation
        return round(max(min_val, min(max_val, new_value)), 1)
    
    def generate_data(self, start_date, end_date, output_file):
        """Generuje dane atmosferyczne dla wszystkich miast w wybranym zakresie dat."""
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            print("Błąd: Niepoprawny format daty. Użyj YYYY-MM-DD")
            return
        
        if start > end:
            print("Błąd: Data rozpoczęcia nie może być późniejsza niż data zakończenia")
            return
        
        num_days = (end - start).days + 1
        print(f"Generowanie danych:")
        print(f"  Zakres: {start_date} do {end_date} ({num_days} dni)")
        print(f"  Liczba miast: {len(self.cities)}")
        print(f"  Całkowita liczba rekordów: {num_days * len(self.cities)}\n")
        
        # Inicjalne wartości dla każdego miasta
        prev_values = {
            city[0]: {
                'PM25': random.uniform(25, 40),
                'temperatura': random.uniform(-10, 10),
                'wilgotnosc': random.uniform(40, 80)
            }
            for city in self.cities
        }
        
        data = []
        current_date = start
        
        while current_date <= end:
            date_str = current_date.strftime('%Y-%m-%d')
            
            for city_name, lat, lon in self.cities:
                # Generuj wartości z zmiennością ±5% od poprzednich
                pm25 = self.generate_value(prev_values[city_name]['PM25'], 5, 50)
                temp = self.generate_value(prev_values[city_name]['temperatura'], -30, 40)
                humidity = self.generate_value(prev_values[city_name]['wilgotnosc'], 10, 100)
                
                # Zaktualizuj poprzednie wartości
                prev_values[city_name] = {
                    'PM25': pm25,
                    'temperatura': temp,
                    'wilgotnosc': humidity
                }
                
                data.append({
                    'nazwa': city_name,
                    'lat': lat,
                    'lon': lon,
                    'data': date_str,
                    'PM25': pm25,
                    'temperatura': temp,
                    'wilgotnosc': humidity
                })
            
            current_date += timedelta(days=1)
        
        # Zapisz do pliku CSV
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['nazwa', 'lat', 'lon', 'data', 'PM25', 'temperatura', 'wilgotnosc'])
                writer.writeheader()
                writer.writerows(data)
            
            print(f"✓ Dane zapisane do: {output_file}")
            print(f"✓ Wygenerowano {len(data)} rekordów")
        except Exception as e:
            print(f"Błąd przy zapisywaniu pliku: {e}")
    
    def list_cities(self):
        """Wyświetla listę miast."""
        print("Miasta w Górnośląsko-Zagłębiowskiej Metropolii:")
        print("-" * 50)
        for i, (name, lat, lon) in enumerate(self.cities, 1):
            print(f"{i:2}. {name:20} ({lat:.4f}, {lon:.4f})")


def main():
    generator = AtmosphericDataGenerator()
    
    # Ustalenie dat domyślnie
    start_date = '2025-01-01'
    end_date = '2025-01-31'
    output_file = 'data/generated_data.csv'
    
    generator.generate_data(start_date, end_date, output_file)


if __name__ == '__main__':
    main()
