import streamlit as st
from datetime import datetime, timedelta
import json
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

# Función para guardar eventos
def save_events(events):
    with open('events.json', 'w') as f:
        json.dump(events, f)

# Configurar la interfaz de Streamlit
st.title("Calendario de Quirófanos")

# Opciones del calendario
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
calendar_component = calendar(events=calendar_events, options=calendar_options)
# st.write(calendar_component)

# Mostrar eventos en una tabla
st.header("Eventos Programados")
if calendar_events:
    df_events = pd.DataFrame(calendar_events)
    df_events['start'] = pd.to_datetime(df_events['start'])
    df_events['end'] = pd.to_datetime(df_events['end'])
    df_events['duration'] = df_events['end'] - df_events['start']
    df_events['resourceId'] = df_events['resourceId'].replace({resource['id']: resource['title'] for resource in resources})
    st.table(df_events[['title', 'start', 'end', 'duration', 'resourceId']])
else:
    st.write("No hay eventos programados.")

# Sidebar para gestionar eventos
with st.sidebar:
    st.header("Gestión de Eventos")
    option = st.selectbox("Selecciona una acción", ["Añadir Evento", "Editar Evento", "Eliminar Evento"])

    if option == "Añadir Evento":
        st.subheader("Añadir Nuevo Evento")
        with st.form("add_event_form"):
            event_title = st.text_input("Título del Evento")
            event_start_date = st.date_input("Fecha de Inicio", value=datetime.today())
            event_start_time = st.time_input("Hora de Inicio", value=datetime.now().time())
            event_end_date = st.date_input("Fecha de Fin", value=datetime.today())
            event_end_time = st.time_input("Hora de Fin", value=(datetime.now() + timedelta(hours=1)).time())
            event_resource = st.selectbox("Quirófano", options=[resource['id'] for resource in resources])
            submit = st.form_submit_button("Añadir Evento")
            
            if submit:
                new_event = {
                    "title": event_title,
                    "start": f"{event_start_date}T{event_start_time}",
                    "end": f"{event_end_date}T{event_end_time}",
                    "resourceId": event_resource,
                }
                calendar_events.append(new_event)
                save_events(calendar_events)
                st.success("Evento añadido con éxito")
                st.experimental_rerun()

    elif option == "Editar Evento":
        st.subheader("Editar Evento")
        if len(calendar_events) > 0:
            selected_event_index = st.selectbox("Selecciona el Evento", range(len(calendar_events)), format_func=lambda idx: calendar_events[idx]['title'])

            if selected_event_index is not None:
                selected_event = calendar_events[selected_event_index]
                with st.form("edit_event_form"):
                    new_title = st.text_input("Nuevo Título del Evento", value=selected_event['title'])
                    new_start_date = st.date_input("Nueva Fecha de Inicio", value=datetime.strptime(selected_event['start'][:10], '%Y-%m-%d'))
                    new_start_time = st.time_input("Nueva Hora de Inicio", value=datetime.strptime(selected_event['start'][11:19], '%H:%M:%S').time())
                    new_end_date = st.date_input("Nueva Fecha de Fin", value=datetime.strptime(selected_event['end'][:10], '%Y-%m-%d'))
                    new_end_time = st.time_input("Nueva Hora de Fin", value=datetime.strptime(selected_event['end'][11:19], '%H:%M:%S').time())
                    new_resource = st.selectbox("Nuevo Quirófano", options=[resource['id'] for resource in resources], index=[resource['id'] for resource in resources].index(selected_event['resourceId']))
                    edit_submit = st.form_submit_button("Guardar Cambios")
                    delete_submit = st.form_submit_button("Eliminar Evento")
                    
                    if edit_submit:
                        calendar_events[selected_event_index] = {
                            "title": new_title,
                            "start": f"{new_start_date}T{new_start_time}",
                            "end": f"{new_end_date}T{new_end_time}",
                            "resourceId": new_resource,
                        }
                        save_events(calendar_events)
                        st.success("Evento actualizado con éxito")
                        st.experimental_rerun()
                    
                    if delete_submit:
                        calendar_events.pop(selected_event_index)
                        save_events(calendar_events)
                        st.success("Evento eliminado con éxito")
                        st.experimental_rerun()
        else:
            st.write("No hay eventos para editar o eliminar.")




