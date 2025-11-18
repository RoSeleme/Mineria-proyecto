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
 
