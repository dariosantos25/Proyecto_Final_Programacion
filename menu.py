import streamlit as st

#Hay que ejecutar este para el menu de dashboards, en consola
#streamlit run menu.py

st.set_page_config(page_title="Proyecto final", page_icon="👻", layout="wide")

st.title("Precios, consumo y natalidad en México (2000–2024)")
st.write(
    "Selecciona un dashboard en el menú de la izquierda para explorar "
    "la evolución de los precios, el consumo de los hogares y la natalidad."
)