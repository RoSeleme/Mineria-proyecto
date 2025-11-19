import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Siniestros Viales en Argentina", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("siniestros_limpio (1).csv")
    return df

df = load_data()


# TÍTULO Y DESCRIPCIÓN GENERAL
st.title("Análisis Exploratorio de Siniestros Viales Fatales en Argentina (2017 – Mar. 2023)")
st.markdown("Dashboard interactivo para la exploración de patrones de riesgo vial utilizando datos del Sistema de Alerta Temprana (SAT).")

st.subheader("Vista general del dataset")
st.dataframe(df.head())


# ------------------------------------------------------------------
# SECCIÓN 1: EVOLUCIÓN ANUAL DE VÍCTIMAS FATALES
st.subheader("Evolución anual de víctimas fatales comprendidas entre el periodo 2017–2023 ( año 2023 parcial)")

# Agrupo por año y realizo conteo de las víctimas
df_anio = df.groupby("anio").size().reset_index(name="victimas")

# Métricas principales
# Contar el total de filas ya que cada fila del df es una víctima fatal.
total_victimas = len(df)
#Calculo de cantidad de año para sacar promedio.
cantidad_anios = df_anio["anio"].nunique()
promedio_anual = total_victimas / cantidad_anios
promedio_diario = total_victimas / (cantidad_anios * 365)

# (Uso .0f como separador de miles con punto en los números).
col1, col2, col3 = st.columns(3)
col1.metric("Total víctimas fatales (2017–2023)", f"{total_victimas:,.0f}".replace(",", "."))  
col2.metric("Promedio anual", f"{promedio_anual:,.0f}".replace(",", "."))
col3.metric("Promedio diario aproximado", f"{promedio_diario:,.1f}".replace(",", "."))

# Gráfico de barras con Plotly
fig_anio = px.bar(
    df_anio,
    x="anio",
    y="victimas",
    labels={"anio": "Año", "victimas": "Cantidad de víctimas fatales"},
    title="Tendencia de Siniestros Fatales por Año",
    text="victimas"
)

fig_anio.update_traces(textposition="outside")
fig_anio.update_layout(
    xaxis=dict(dtick=1),
    yaxis_title="Cantidad de víctimas",
    bargap=0.2,
    height=500
)

# Anotación para el año 2020 (Punto de inflexión - pandemia)
fig_anio.add_annotation(
    x=2020,  # Columna 'anio'
    y=df_anual[df_anual['anio'] == 2020]['Fatalidades'].iloc[0],  # El valor exacto de fatalidades de 2020
    text="Baja por Pandemia COVID-19",
    showarrow=True,
    arrowhead=1,
    ax=-50,
    ay=-80,
    font=dict(size=12, color="blue")
)

fig_anio.add_hline(
    y=promedio_anual,
    line_dash="dot",
    line_color="red",
    annotation_text=f"Promedio Anual: {promedio_anual:,.0f}".replace(",", "."),
    annotation_position="top right"
)

st.plotly_chart(fig_anio, use_container_width=True)

st.markdown(
    """
    <p style='font-size: small; color: #7f7f7f;'>
    * La línea punteada roja representa el promedio anual de víctimas fatales.
    </p>
    """, 
    unsafe_allow_html=True
)


st.subheader("Distribución Geográfica y Condicionalidad (KDD: Exploración de Patrones)")

# ------------------------------------------------------------------
