import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 🔹 CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Análisis Laboral", layout="wide")

# 🔹 TÍTULO PRINCIPAL
st.title("📊 Análisis del Mercado Laboral Informal")

# 🔹 INFO DEL GRUPO
st.markdown("### 👥 Grupo 6")

st.markdown("""
**Integrantes:**
-  Jara Mesia, Mateo Francisco
-  Moron Espino, Jesus Maximiliano
-  Perez Nuñez, Aeiderik Calet
-  Quijano Rodriguez, César Ignacio
-  Quispe Tocasca, David Alexander
""")

st.caption("Curso: Economía | 2026")

st.divider()

# 🔹 CARGA DE DATOS
df = pd.read_csv("Equipo6_EconomiaInformal.csv")

# 🔹 VISTA GENERAL
st.subheader("📋 Vista general de los datos")
st.write(df.head())

st.divider()

# 🔹 CREACIÓN DE VARIABLE
df['Subempleado'] = (df['Horas_Trabajadas_Semana'] < 30) & (df['Tiene_Contrato_Escrito'] == 'No')

st.subheader("📉 Análisis de Subempleo")
st.write(df['Subempleado'].value_counts())

st.divider()

# 🔹 GRÁFICOS EN COLUMNAS (SE VE MÁS PRO)
col1, col2 = st.columns(2)

# 🔸 Gráfico 1
with col1:
    st.subheader("💰 Ingreso por Tipo de Actividad")
    ingreso_actividad = df.groupby('Tipo_Actividad')['Ingreso_Mensual'].mean().sort_values()

    fig1, ax1 = plt.subplots()
    ax1.barh(ingreso_actividad.index, ingreso_actividad.values)
    ax1.set_xlabel('Ingreso Promedio (S/)')
    ax1.set_title('Ingreso por Actividad')

    st.pyplot(fig1)

# 🔸 Gráfico 2
with col2:
    st.subheader("📍 Contrato por Zona")
    contrato_zona = df.groupby(['Zona', 'Tiene_Contrato_Escrito']).size().unstack()
    contrato_zona_pct = contrato_zona.div(contrato_zona.sum(axis=1), axis=0) * 100

    fig2, ax2 = plt.subplots()
    contrato_zona_pct.plot(kind='bar', ax=ax2)

    st.pyplot(fig2)

st.divider()

# 🔹 GRÁFICO FINAL
st.subheader("📊 Acceso a Beneficios")

beneficios_formal = df.groupby(['Formalidad', 'Acceso_Beneficios']).size().unstack()
beneficios_pct = beneficios_formal.div(beneficios_formal.sum(axis=1), axis=0) * 100

fig3, ax3 = plt.subplots()
beneficios_pct.plot(kind='bar', ax=ax3)

st.pyplot(fig3)