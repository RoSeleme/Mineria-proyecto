import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Siniestros Viales en Argentina", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("siniestros_limpio(1).csv")
    return df

df = load_data()



# TÍTULO Y DESCRIPCIÓN GENERAL
st.title(" Siniestros Viales Fatales en Argentina (2017–2023)")
st.write("Este dashboard forma parte del proyecto final de la materia Minería de Datos.")

st.subheader("Vista general del dataset")
st.dataframe(df.head())
 
