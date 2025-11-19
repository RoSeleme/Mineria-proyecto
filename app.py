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
## 1. FILTRO INTERACTIVO (Requerimiento de la consigna)
# Se usa st.sidebar para que el filtro aparezca en el panel lateral
provincias_disponibles = sorted(df['provincia_nombre'].unique())
provincias_filtradas = st.sidebar.multiselect(
    "📍 Seleccione Provincia(s):",
    options=provincias_disponibles,
    default=provincias_disponibles  # Por defecto, muestra todas
)

df_filtrado = df[df['provincia_nombre'].isin(provincias_filtradas)]

if df_filtrado.empty:
    st.warning("No hay datos para las provincias seleccionadas. Ajuste su filtro.")
    st.stop()


# ------------------------------------------------------------------
## 2. VISUALIZACIÓN 2: Top Provincias (Distribución Geográfica)

col_prov_1, col_prov_2 = st.columns([1, 2])

# Métrica adicional (para que la columna 1 no quede vacía)
victimas_filtradas = len(df_filtrado)
col_prov_1.metric("Víctimas en Provincias Seleccionadas", f"{victimas_filtradas:,.0f}".replace(",", "."))


# Gráfico de Barras para el TOP 10 (Se adapta si se selecciona menos provincias)
df_prov_top = df_filtrado['provincia_nombre'].value_counts().nlargest(10).reset_index()
df_prov_top.columns = ['Provincia', 'Fatalidades']

fig_prov = px.bar(
    df_prov_top,
    x='Fatalidades',
    y='Provincia',
    orientation='h',
    title='Top 10 Provincias con Mayor Cantidad de Siniestros Fatales',
    labels={'Fatalidades': 'Nº de Víctimas Fatales', 'Provincia': ''},
    color='Fatalidades'
)
fig_prov.update_layout(yaxis={'categoryorder':'total ascending'}, title_x=0.5)
col_prov_2.plotly_chart(fig_prov, use_container_width=True)
