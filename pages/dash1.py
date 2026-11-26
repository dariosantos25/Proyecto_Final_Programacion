#imports necesarios
import streamlit as st
import pandas as pd
import plotly.express as px

#Nombres mas faciles para los indicadores INPC
NOMBRES = {
    "INPC_General": "General",
    "INPC_Mercancias": "Mercancías",
    "INPC_Servicios": "Servicios",
    "INPC_Agropecuarios": "Agropecuarios",
    "INPC_Energeticos_Gobierno": "Energéticos y tarifas de gobierno",
}
COMPONENTES = [c for c in NOMBRES if c != "INPC_General"]


@st.cache_data
def leer_df():
    df = pd.read_csv("datos/Datos_Integrados.csv")
    #Inflacion anual del INPC general en %. Se calcula con todas los años
    #antes de filtrar, para no perder el primer año del rango
    df["Inflacion_General"] = df["INPC_General"].pct_change() * 100
    return df


def dashboard1():
    #Titulo de la ventana y simbolo
    st.set_page_config(
        page_title="Precios",
        page_icon="👻",
        layout="wide"
    )
    #leer los datos
    datos = leer_df()

    #Titulo, subtitulo
    st.title("Dashboard 1: Evolución de los precios")
    st.subheader("¿Cómo han evolucionado los precios de los bienes y servicios en México?")

    #filtros para el sidebar
    st.sidebar.header("Filtros")
    inicio, fin = st.sidebar.slider(
        "Rango de años",
        min_value=int(datos["Periodo"].min()),
        max_value=int(datos["Periodo"].max()),
        value=(int(datos["Periodo"].min()), int(datos["Periodo"].max()))
    )
    seleccion = st.sidebar.multiselect(
        "Componentes a comparar",
        options=COMPONENTES,
        default=COMPONENTES,
        format_func=lambda c: NOMBRES[c]
    )

    #Filtrar los datos por el rango de años
    filtrado = datos[datos["Periodo"].between(inicio, fin)]

    #indicadores
    primero = filtrado.iloc[0]
    ultimo = filtrado.iloc[-1]
    variacion = (ultimo["INPC_General"] / primero["INPC_General"] - 1) * 100
    inflacion_prom = filtrado["Inflacion_General"].mean()  #ignora el NaN de 2000

    col1, col2, col3 = st.columns(3)
    col1.metric(f"INPC general {inicio}", f"{primero['INPC_General']:.1f}")
    col2.metric(
        f"INPC general {fin}",
        f"{ultimo['INPC_General']:.1f}",
        delta=f"{variacion:.1f}% acumulado"
    )
    col3.metric("Inflación promedio anual", f"{inflacion_prom:.2f}%")
    st.caption(
        "El INPC está calculado como promedio anual de los índices mensuales, "
        "por lo que la inflación anual puede diferir ligeramente de la cifra "
        "oficial de diciembre a diciembre."
    )

    #Fila 1, Graficas A y B
    st.divider()
    colA, colB = st.columns(2)

    #Grafica A: INPC general por año
    with colA:
        st.subheader("INPC general")
        graficaA = px.line(
            filtrado,
            x="Periodo",
            y="INPC_General",
            title="Evolución del INPC general",
            labels={"Periodo": "Año", "INPC_General": "Índice INPC"},
            markers=True
        )
        st.plotly_chart(graficaA, use_container_width=True)

    #Grafica B: componentes elegidos en el multiselect
    with colB:
        st.subheader("Componentes del INPC")
        if seleccion:
            #se pasa a formato largo para tener una linea por componente
            largo = filtrado.melt(
                id_vars="Periodo",
                value_vars=seleccion,
                var_name="Componente",
                value_name="Índice"
            )
            largo["Componente"] = largo["Componente"].map(NOMBRES)
            graficaB = px.line(
                largo,
                x="Periodo",
                y="Índice",
                color="Componente",
                title="Comparación de los componentes del INPC",
                labels={"Periodo": "Año"}
            )
            st.plotly_chart(graficaB, use_container_width=True)
        else:
            st.warning("Selecciona al menos un componente en la barra lateral.")

    #Fila2, graficas c y d
    st.divider()
    colC, colD = st.columns(2)

    #Grafica C: inflacion anual del INPC general
    with colC:
        st.subheader("Inflación anual")
        graficaC = px.bar(
            filtrado.dropna(subset=["Inflacion_General"]),
            x="Periodo",
            y="Inflacion_General",
            title="Inflación anual del INPC general (%)",
            labels={"Periodo": "Año", "Inflacion_General": "Inflación (%)"}
        )
        st.plotly_chart(graficaC, use_container_width=True)

    #Grafica D: variacion acumulada de cada componente en el rango
    with colD:
        st.subheader("Variación acumulada")
        acumulada = pd.DataFrame({
            "Componente": [NOMBRES[c] for c in NOMBRES],
            "Variación (%)": [
                (ultimo[c] / primero[c] - 1) * 100 for c in NOMBRES
            ]
        }).sort_values("Variación (%)")
        graficaD = px.bar(
            acumulada,
            x="Variación (%)",
            y="Componente",
            orientation="h",
            title=f"Variación acumulada del INPC, {inicio}-{fin} (%)",
            text_auto=".1f"
        )
        st.plotly_chart(graficaD, use_container_width=True)

    #tabla con los datos seleccionados vaya
    with st.expander("Ver datos del rango seleccionado"):
        st.dataframe(filtrado, use_container_width=True)


if __name__ == "__main__":
    dashboard1()