import streamlit as st
import pandas as pd
import plotly.express as px

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
st.header("📈 Evolución anual de víctimas fatales (2017–2023)")

# Agrupar por año y contar víctimas
df_anio = df.groupby("anio").size().reset_index(name="victimas")

# Métricas principales
# Contar el total de filas ya que cada fila del df es una víctima fatal.
total_victimas = len(df)
#Calculo de cantidad de año para sacar promedio.
cantidad_anios = df_anio["anio"].nunique()
promedio_anual = total_victimas / cantidad_anios
promedio_diario = total_victimas / (cantidad_anios * 365)

#(separador de miles con punto)
col1, col2, col3 = st.columns(3)
col1.metric("Total víctimas fatales (2017–2023)", f"{total_victimas:,.0f}".replace(",", "."))  
col2.metric("Promedio anual", f"{promedio_anual:,.0f}".replace(",", "."))
col3.metric("Promedio diario aproximado", f"{promedio_diario:,.1f}".replace(",", "."))
