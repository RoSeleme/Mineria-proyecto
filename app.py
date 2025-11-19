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
 
# SECCIÓN 1: EVOLUCIÓN ANUAL DE VÍCTIMAS FATALES
st.subheader("Evolución anual de víctimas fatales comprendidas entre el periodo 2017–2023")

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
    title="Víctimas fatales por año",
    text="victimas"
)

fig_anio.update_traces(textposition="outside")
fig_anio.update_layout(
    xaxis=dict(dtick=1),
    yaxis_title="Cantidad de víctimas",
    bargap=0.2,
    height=500
)

st.plotly_chart(fig_anio, use_container_width=True)


