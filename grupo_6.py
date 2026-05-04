import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análisis Laboral", layout="wide")

# 🔹 TÍTULO
st.title("📊 Economía Informal y Subempleo en el Perú")

# 🔹 INTEGRANTES
st.markdown("### 👥 Grupo 6")
st.markdown("""
**Integrantes:**
-  Jara Mesia, Mateo Francisco
-  Moron Espino, Jesus Maximiliano
-  Perez Nuñez, Aeiderik Calet
-  Quijano Rodriguez, César Ignacio
-  Quispe Tocasca, David Alexander
""")

st.caption("Universidad de Lima | 2026")

st.divider()

# 🔹 CARGA DE DATOS
df = pd.read_csv("Grupo 6/Equipo6_EconomiaInformal.csv")
df.columns = df.columns.str.strip()

# 🔹 LIMPIEZA (CLAVE PARA QUE NO CAMBIEN RESULTADOS)
df['Acceso_Beneficios'] = df['Acceso_Beneficios'].astype(str).str.strip().str.lower()
df['Tiene_Contrato_Escrito'] = df['Tiene_Contrato_Escrito'].astype(str).str.strip().str.lower()

# 🔹 PRECARIEDAD (LÓGICA CORRECTA)
df['Precariedad'] = 'Moderada_precariedad'

# Alta precariedad
df.loc[
    (df['Acceso_Beneficios'] == 'ninguno') &
    (df['Tiene_Contrato_Escrito'] == 'no') &
    ((df['Horas_Trabajadas_Semana'] > 48) | (df['Horas_Trabajadas_Semana'] < 20)),
    'Precariedad'
] = 'Alta_precariedad'

# Empleo estable (CONDICIÓN MÁS ESTRICTA)
df.loc[
    (df['Acceso_Beneficios'] == 'completo') &  # ⚠️ si no existe, cambiar luego
    (df['Tiene_Contrato_Escrito'] == 'si') &
    (df['Horas_Trabajadas_Semana'].between(30, 48)),
    'Precariedad'
] = 'Empleo_estable'

# 🔹 SUBEMPLEO
df['Subempleado'] = (df['Horas_Trabajadas_Semana'] < 30) & (df['Tiene_Contrato_Escrito'] == 'no')

# 🔹 VISTA GENERAL
st.subheader("📋 Vista general")
st.write(df.head())

st.subheader("📊 Distribución de precariedad")
st.write(df['Precariedad'].value_counts())

st.subheader("📉 Subempleo")
st.write(df['Subempleado'].value_counts())

st.divider()

# =========================
# 📊 GRÁFICO 1
# =========================
col1, col2 = st.columns([2,1])

with col1:
    ingreso_actividad = df.groupby('Tipo_Actividad')['Ingreso_Mensual'].mean().sort_values()

    fig1, ax1 = plt.subplots(figsize=(9,5))
    bars = ax1.barh(ingreso_actividad.index, ingreso_actividad.values)

    for bar, val in zip(bars, ingreso_actividad.values):
        ax1.text(val + 10, bar.get_y() + bar.get_height()/2, f'S/ {val:.0f}')

    ax1.set_title('Ingreso Promedio por Tipo de Actividad')
    st.pyplot(fig1)

with col2:
    st.markdown("Diferencias de ingreso según actividad económica.")

st.divider()

# =========================
# 📊 GRÁFICO 4 (CLAVE)
# =========================
col1, col2 = st.columns([2,1])

with col1:
    ingreso_por_precariedad = (
        df.groupby('Precariedad')['Ingreso_Mensual']
        .mean()
        .sort_values()
        .round(2)
    )

    colores = {
        'Alta_precariedad': 'darkred',
        'Moderada_precariedad': 'orange',
        'Empleo_estable': 'darkgreen'
    }

    bar_colors = [colores.get(i, 'gray') for i in ingreso_por_precariedad.index]

    fig4, ax4 = plt.subplots(figsize=(9,5))
    ingreso_por_precariedad.plot(kind='barh', ax=ax4, color=bar_colors)

    for i, v in enumerate(ingreso_por_precariedad):
        ax4.text(v + 10, i, f'S/. {v:.2f}')

    ax4.set_title("Ingreso promedio según nivel de precariedad")

    st.pyplot(fig4)

with col2:
    st.markdown("""
Alta precariedad → menor ingreso  
Moderada → nivel intermedio  
Estable → mayor ingreso  
""")

st.write("📌 Valores reales:")
st.write(ingreso_por_precariedad)

st.divider()

# =========================
# 🧾 CONCLUSIONES
# =========================
st.subheader("🧾 Conclusiones")

porcentaje_subempleo = df['Subempleado'].mean() * 100

st.markdown(f"""
- El **{porcentaje_subempleo:.1f}%** de trabajadores está en subempleo  
- La precariedad reduce ingresos  
- Existen diferencias estructurales en el mercado laboral  

➡️ Se evidencia desigualdad en la calidad del empleo
""")