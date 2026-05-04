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

# =========================
# 🔥 PRECARIEDAD (CORRECTA)
# =========================
df['Precariedad'] = 'Moderada_precariedad'

# Alta precariedad
df.loc[
    (df['Acceso_Beneficios'] == 'Ninguno') &
    (df['Tiene_Contrato_Escrito'] == 'No') &
    ((df['Horas_Trabajadas_Semana'] > 48) | (df['Horas_Trabajadas_Semana'] < 20)),
    'Precariedad'
] = 'Alta_precariedad'

# Empleo estable
df.loc[
    (df['Acceso_Beneficios'] == 'completo') &
    (df['Tiene_Contrato_Escrito'] == 'Sí') &
    (df['Horas_Trabajadas_Semana'].between(30, 48)),
    'Precariedad'
] = 'Empleo_estable'

# 🔹 SUBEMPLEO
df['Subempleado'] = (df['Horas_Trabajadas_Semana'] < 30) & (df['Tiene_Contrato_Escrito'] == 'No')

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
    bars = ax1.barh(
        ingreso_actividad.index,
        ingreso_actividad.values,
        color=['#FDCF76','#89AEB2','#3465e0','#E08963','#7be069']
    )

    for bar, val in zip(bars, ingreso_actividad.values):
        ax1.text(val + 10, bar.get_y() + bar.get_height()/2, f'S/ {val:.0f}', va='center')

    ax1.set_title('Ingreso Promedio por Tipo de Actividad')

    st.pyplot(fig1)

with col2:
    st.markdown("""
### 🔎 Interpretación
Se observan diferencias claras de ingresos entre actividades, lo que evidencia desigualdad en el mercado laboral.
""")

st.divider()

# =========================
# 📊 GRÁFICO 2
# =========================
col1, col2 = st.columns([2,1])

with col1:
    contrato_zona = df.groupby(['Zona', 'Tiene_Contrato_Escrito']).size().unstack()
    contrato_zona_pct = contrato_zona.div(contrato_zona.sum(axis=1), axis=0) * 100

    fig2, ax2 = plt.subplots(figsize=(7,5))
    contrato_zona_pct.plot(kind='bar', ax=ax2, color=['#d9534f','#5cb85c'])

    for p in ax2.patches:
        ax2.annotate(
            str(round(p.get_height(),1)) + '%',
            (p.get_x() + p.get_width()/2., p.get_height()),
            ha='center', xytext=(0,5), textcoords='offset points'
        )

    ax2.set_title("Contrato por zona (%)")

    st.pyplot(fig2)

with col2:
    st.markdown("""
### 🌎 Interpretación
Las zonas rurales presentan mayor informalidad, reflejando desigualdad territorial.
""")

st.divider()

# =========================
# 📊 GRÁFICO 3
# =========================
col1, col2 = st.columns([2,1])

with col1:
    beneficios_formal = df.groupby(['Formalidad', 'Acceso_Beneficios']).size().unstack()
    beneficios_pct = beneficios_formal.div(beneficios_formal.sum(axis=1), axis=0) * 100

    fig3, ax3 = plt.subplots(figsize=(8,5))
    beneficios_pct.plot(kind='bar', ax=ax3)

    for c in ax3.containers:
        ax3.bar_label(c, fmt='%.0f%%')

    ax3.set_title("Acceso a beneficios (%)")

    st.pyplot(fig3)

with col2:
    st.markdown("""
### 📊 Interpretación
El acceso a beneficios es limitado incluso en algunos trabajadores formales.
""")

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

    # Colores correctos por categoría
    colores = {
        'Alta_precariedad': 'darkred',
        'Moderada_precariedad': 'orange',
        'Empleo_estable': 'darkgreen'
    }

    bar_colors = [colores[i] for i in ingreso_por_precariedad.index]

    fig4, ax4 = plt.subplots(figsize=(9,5))
    ingreso_por_precariedad.plot(kind='barh', ax=ax4, color=bar_colors)

    for i, v in enumerate(ingreso_por_precariedad):
        ax4.text(v + 10, i, f'S/. {v:.2f}')

    ax4.set_title("Ingreso promedio según nivel de precariedad")

    st.pyplot(fig4)

with col2:
    st.markdown("""
### 💡 Interpretación
Los trabajadores con mayor precariedad presentan menores ingresos promedio, mientras que el empleo estable muestra los niveles más altos.
""")

st.write("📌 Valores reales:")
st.write(ingreso_por_precariedad)

st.divider()

# =========================
# 🔍 ANÁLISIS
# =========================
st.subheader("📌 Análisis Económico")

st.markdown("""
La precariedad laboral es un fenómeno multidimensional que depende de condiciones como acceso a beneficios, estabilidad contractual y horas trabajadas.

Los resultados muestran segmentación del mercado laboral, donde ciertos grupos enfrentan mayor vulnerabilidad.
""")

# =========================
# 🧾 CONCLUSIONES (DINÁMICAS)
# =========================
st.subheader("🧾 Conclusiones")

porcentaje_subempleo = df['Subempleado'].mean() * 100

st.markdown(f"""
- El **{porcentaje_subempleo:.1f}% de los trabajadores** se encuentra en subempleo.  
- La precariedad laboral está asociada a condiciones desfavorables.  
- Existen desigualdades entre sectores y zonas.  
- Los trabajadores en alta precariedad presentan menores ingresos promedio.  

➡️ Se evidencia una brecha estructural en la calidad del empleo.
""")