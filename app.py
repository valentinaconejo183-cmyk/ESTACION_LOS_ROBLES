import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="FotoboltAI - Los Robles", layout="wide")

st.title("FotoboltAI - Estacion Los Robles")
st.write("Dashboard para decidir si es buen dia para fotos en exterior en Popayan, Cauca")
st.write("Estacion: Los Robles - Lat: 2.391301, Lon: -76.656703")

# 1. LEER EL CSV QUE YA ESTA EN GITHUB
st.subheader("Datos recolectados de Los Robles")
try:
    df = pd.read_csv("datos_los_robles.csv")
    st.write(f"Total de datos recolectados: {len(df)}")
    st.dataframe(df.tail(10))
except Exception as e:
    st.warning("Aun no se pudo leer datos_los_robles.csv")
    st.write(e)

# 2. API EN VIVO OPEN-METEO - LOS ROBLES
st.subheader("Clima en vivo - Los Robles")

# Coordenadas exactas de Valentina - Estacion Los Robles
lat_los_robles = 2.391301
lon_los_robles = -76.656703

url = f"https://api.open-meteo.com/v1/forecast?latitude={lat_los_robles}&longitude={lon_los_robles}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,cloud_cover"

# Se dejan en None por si la API falla (la seccion de bloques los usa mas abajo)
temp = None
humedad = None

try:
    datos = requests.get(url).json()
    actual = datos['current']

    temp = actual['temperature_2m']
    humedad = actual['relative_humidity_2m']
    viento = actual['wind_speed_10m']
    nubosidad = actual['cloud_cover']

    # 3. LAS 4 METRICAS
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Temperatura", f"{temp} C")
    col2.metric("Humedad", f"{humedad} %")
    col3.metric("Viento", f"{viento} km/h")
    col4.metric("Nubosidad", f"{nubosidad} %")

    # 4. LOGICA DE NEGOCIO
    st.subheader("Recomendacion para el fotografo")
    if nubosidad > 70:
        st.warning("CONDICION MEDIA - Luz difusa, mejor estudio")
    elif viento > 20:
        st.warning("Cuidado con tripode / equipo - Viento alto")
    else:
        st.success("CONDICION BUENA para exterior")

except Exception as e:
    st.error("No se pudo conectar con Open-Meteo")
    st.write(e)

# 4B. ANALISIS DE BLOQUES (resultados de la camara con OpenCV)
st.subheader("Analisis de bloques - Los Robles")
try:
    bloques = pd.read_csv("resultados_bloques.csv")
    if len(bloques) == 0:
        raise ValueError("resultados_bloques.csv esta vacio")
    ultimo = bloques.iloc[-1]

    def en_cm(valor):
        return f"{valor} cm" if pd.notna(valor) else "sin calibrar"

    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Bloques detectados", int(ultimo["n_bloques"]))
    b2.metric("Largo", en_cm(ultimo["largo_cm"]))
    b3.metric("Alto", en_cm(ultimo["alto_cm"]))
    b4.metric("Color", str(ultimo["color"]))

    # Frase que junta el clima en vivo con el bloque analizado
    if temp is not None:
        clima = f"Hoy hace {temp} C y la humedad es {humedad} %"
    else:
        clima = "No hay clima en vivo en este momento"
    if pd.notna(ultimo["largo_cm"]) and pd.notna(ultimo["alto_cm"]):
        medidas = f"mide {ultimo['largo_cm']} cm de largo y {ultimo['alto_cm']} cm de alto"
    else:
        medidas = f"mide {ultimo['largo_px']} px de largo y {ultimo['alto_px']} px de alto"
    st.info(f"{clima}. El bloque analizado {medidas} y es de color {ultimo['color']}.")

    st.caption(f"Ultima foto analizada: {ultimo['fecha']}")
    st.write(f"Total de analisis guardados: {len(bloques)}")
    st.dataframe(bloques.tail(10))
except FileNotFoundError:
    st.info("Aun no hay resultados_bloques.csv en el repositorio.")
except Exception as e:
    st.warning("No se pudo leer resultados_bloques.csv")
    st.write(e)

# 5. SUBIR PORTAFOLIO
st.subheader("Portafolio")
foto = st.file_uploader("Sube tu foto", type=["jpg", "png", "jpeg"])
if foto:
    st.image(foto, caption="Tu foto")

# 6. FORMULARIO AGENDA
st.subheader("Agendar sesion")
nombre = st.text_input("Nombre")
fecha = st.date_input("Fecha")
if st.button("Guardar Datos"):
    st.success(f"Guardado {nombre} para {fecha}")
