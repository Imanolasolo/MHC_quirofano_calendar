import streamlit as st
import json
import base64
from datetime import datetime
import pandas as pd
from streamlit_calendar import calendar

# Definir los recursos (quirófanos)
resources = [
    {"id": "quir1", "title": "Quirófano 1"},
    {"id": "quir2", "title": "Quirófano 2"}
]

# Cargar eventos guardados si existen
try:
    with open('events.json', 'r') as f:
        calendar_events = json.load(f)
except FileNotFoundError:
    calendar_events = []

# Configurar título de la página e ícono de pestaña
st.set_page_config(
    page_title="Calendario Quirofanos MHC",
    page_icon=":calendar:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://wa.me/5930993513082?text=Solicito%20ayuda%20con%20la%20app%20MHC',
        'Report a bug': "https://wa.me/5930993513082?text=Solicito%20ayuda%20con%20la%20app%20MHC",
        'About': "# App creada por CodeCodix"
    }
)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64_of_bin_file('MHC_Marketing_background.jpg')

st.markdown(
    f"""
    <style>
    .stApp {{
        background: url('data:image/jpeg;base64,{img_base64}') no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Función para mostrar el calendario de eventos
def show_calendar(events):
    st.title("Calendario de Quirófanos")
    
    # Configuración del calendario
    calendar_options = {
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
        "slotMinTime": "06:00:00",
        "slotMaxTime": "20:00:00",
        "initialView": "dayGridMonth",
        "resources": resources
    }

    # Mostrar el calendario
    st.write("Calendario de Eventos")
    calendar(events=events, options=calendar_options)

    # Mostrar eventos en una tabla
    st.header("Eventos Programados")
    if events:
        df_events = pd.DataFrame(events)
        df_events['start'] = pd.to_datetime(df_events['start'])
        df_events['end'] = pd.to_datetime(df_events['end'])
        df_events['duration'] = df_events['end'] - df_events['start']
        df_events['resourceId'] = df_events['resourceId'].replace({resource['id']: resource['title'] for resource in resources})
        st.table(df_events[['title', 'start', 'end', 'duration', 'resourceId']])
    else:
        st.write("No hay eventos programados.")

def ViewCalendar():
    show_calendar(calendar_events)

# Ejecutar la función para mostrar el calendario
if __name__ == "__main__":
    ViewCalendar()

