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

# 🔹 VARIABLES
df['Precariedad'] = df['Ingreso_Mensual'].apply(
    lambda x: 'Alta' if x < 1000 else 'Moderada' if x < 2000 else 'Estable'
)

df['Subempleado'] = (df['Horas_Trabajadas_Semana'] < 30) & (df['Tiene_Contrato_Escrito'] == 'No')

# 🔹 VISTA GENERAL
st.subheader("📋 Vista general")
st.write(df.head())

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

    ax1.set_title('Ingreso por Tipo de Actividad')

    st.pyplot(fig1)

with col2:
    st.markdown("""
### 🔎 Interpretación

Existe una **clara diferencia de ingresos según el tipo de actividad**, lo que refleja desigualdades estructurales dentro del mercado laboral.

Algunos sectores concentran mejores ingresos, mientras que otros permanecen rezagados.
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
    contrato_zona_pct.plot(
        kind='bar',
        ax=ax2,
        color=['#d9534f','#5cb85c'],
        edgecolor='white'
    )

    for p in ax2.patches:
        ax2.annotate(str(round(p.get_height(),1)) + '%',
        (p.get_x() + p.get_width()/2., p.get_height()),
        ha='center', xytext=(0,5), textcoords='offset points')

    st.pyplot(fig2)

with col2:
    st.markdown("""
### 🌎 Análisis territorial

La **zona rural concentra mayor proporción de trabajadores sin contrato**, lo que evidencia brechas estructurales en la calidad del empleo.

Esto demuestra que el mercado laboral peruano **no es homogéneo**, sino profundamente desigual según la región.
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
    beneficios_pct.plot(kind='bar', ax=ax3, color=['#f0ad4e','#5bc0de','#5cb85c'])

    for c in ax3.containers:
        ax3.bar_label(c, fmt='%.0f%%')

    st.pyplot(fig3)

with col2:
    st.markdown("""
### 📊 Hallazgo clave

La cobertura de beneficios es **limitada tanto en trabajadores formales como informales**, lo que revela fallas en la fiscalización laboral.

Esto reduce la protección social y aumenta la vulnerabilidad.
""")

st.divider()

# =========================
# 📊 GRÁFICO 4
# =========================
col1, col2 = st.columns([2,1])

with col1:
    ingreso_por_precariedad = df.groupby('Precariedad')['Ingreso_Mensual'].mean().sort_values().round(2)

    fig4, ax4 = plt.subplots(figsize=(9,5))
    ingreso_por_precariedad.plot(kind='barh', ax=ax4, color=['darkred','orange','darkgreen'])

    for i, v in enumerate(ingreso_por_precariedad):
        ax4.text(v + 10, i, f'S/. {v:.2f}')

    st.pyplot(fig4)

with col2:
    st.markdown("""
### 💡 Análisis económico

Los resultados muestran que:

- **Alta precariedad → menores ingresos**
- **Empleo estable → mayores ingresos**
- La precariedad moderada se ubica en un punto intermedio  

Esto confirma que la informalidad genera una **trampa de pobreza laboral**, donde los trabajadores más vulnerables también son los que menos ingresos perciben.
""")

st.divider()

# =========================
# 🔍 ANÁLISIS PROFUNDO (DEL WORD)
# =========================
st.subheader("📌 Análisis Económico")

st.markdown("""
Desde una perspectiva económica, la precariedad laboral debe entenderse como un fenómeno **multidimensional**, más allá de la simple distinción entre formal e informal.

Existe una **zona intermedia o “gris”**, donde los trabajadores no están completamente desprotegidos pero tampoco cuentan con condiciones laborales adecuadas.

Además, se observan diferencias territoriales importantes:
- Departamentos con menor desarrollo presentan mayor precariedad.
- Regiones como Huancavelica y Cusco concentran mayores niveles de vulnerabilidad.
- Lima, como principal polo económico, muestra mejores condiciones relativas.

Esto evidencia que el mercado laboral peruano es **heterogéneo**, por lo que las políticas públicas deben adaptarse a cada realidad regional.
""")

# =========================
# 🧾 CONCLUSIONES
# =========================
st.subheader("🧾 Conclusiones")

st.markdown("""
- El **25.5% de los trabajadores** se encuentra en condición de subempleo.  
- El empleo formal no necesariamente implica mayor ingreso, pero sí mayor protección.  
- Existen **fuertes brechas territoriales** en la calidad del empleo.  
- La cobertura de beneficios es limitada.  
- La precariedad laboral se asocia directamente con menores ingresos.  

➡️ En conjunto, estos resultados evidencian una **trampa de pobreza laboral** que requiere intervención pública para ser revertida.
""")