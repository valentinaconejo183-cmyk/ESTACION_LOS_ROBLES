import requests
import csv
import os
from datetime import datetime
import pytz

# Configuracion Los Robles - Popayan
LAT = 2.3913
LON = -76.6567
ZONA = pytz.timezone('America/Bogota')
ARCHIVO = 'datos_los_robles.csv'

url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,cloud_cover,shortwave_radiation&timezone=America%2FBogota"

try:
    r = requests.get(url)
    datos = r.json()
    curr = datos['current']
    elev = datos['elevation']

    ahora = datetime.now(ZONA)
    
    fila = [ahora.strftime("%Y-%m-%d %H:%M:%S"), curr['time'], curr['temperature_2m'], curr['relative_humidity_2m'], curr['cloud_cover'], curr['shortwave_radiation'], elev]
    
    existe = os.path.isfile(ARCHIVO)
    with open(ARCHIVO, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=´;´)
        if not existe:
            writer.writerow(['fecha_hora_recoleccion','hora_api','temperatura_C','humedad_%','nubosidad_%','radiacion_Wm2','elevacion_m'])
        writer.writerow(fila)
    
    print(f"Dato guardado: {fila}")

except Exception as e:
    print(f"Error: {e}")
