import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análisis Laboral", layout="wide")

# =========================
# 🔹 TÍTULO
# =========================
st.title("📊 Economía Informal y Subempleo en el Perú")

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

# =========================
# 🔹 CARGA DE DATOS
# =========================
df = pd.read_csv("Grupo 6/Equipo6_EconomiaInformal.csv")
df.columns = df.columns.str.strip()

# 🔹 LIMPIEZA (IMPORTANTE)
df['Acceso_Beneficios'] = df['Acceso_Beneficios'].astype(str).str.strip().str.lower()
df['Tiene_Contrato_Escrito'] = df['Tiene_Contrato_Escrito'].astype(str).str.strip().str.lower()

# =========================
# 🔹 PRECARIEDAD (CORREGIDA Y ESTABLE)
# =========================
df['Precariedad'] = 'Moderada_precariedad'

# Alta precariedad
df.loc[
    (df['Acceso_Beneficios'] == 'ninguno') &
    (df['Tiene_Contrato_Escrito'] == 'no') &
    ((df['Horas_Trabajadas_Semana'] > 48) | (df['Horas_Trabajadas_Semana'] < 20)),
    'Precariedad'
] = 'Alta_precariedad'

# Empleo estable (AJUSTADO PARA QUE SÍ EXISTA)
df.loc[
    (df['Tiene_Contrato_Escrito'] == 'si') &
    (df['Horas_Trabajadas_Semana'].between(30, 48)),
    'Precariedad'
] = 'Empleo_estable'

# =========================
# 🔹 SUBEMPLEO
# =========================
df['Subempleado'] = (df['Horas_Trabajadas_Semana'] < 30) & (df['Tiene_Contrato_Escrito'] == 'no')

# =========================
# 🔹 VISTA GENERAL
# =========================
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

    fig1, ax1 = plt.subplots(figsize=(9, 5))
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
    st.markdown("Diferencias de ingreso según actividad económica.")

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
        ax2.annotate(str(round(p.get_height(),1)) + '%',
                     (p.get_x() + p.get_width()/2., p.get_height()),
                     ha='center', xytext=(0,5), textcoords='offset points')

    ax2.set_title("Contrato por zona (%)")
    st.pyplot(fig2)

with col2:
    st.markdown("Mayor informalidad en zonas rurales.")

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
    st.markdown("Cobertura limitada de beneficios.")

st.divider()

# =========================
# 📊 GRÁFICO 4 (CLAVE)
# =========================
col1, col2 = st.columns([2,1])

with col1:
    ingreso_precariedad = df.groupby('Precariedad')['Ingreso_Mensual'].mean().round(2)

    colores = {
        'Alta_precariedad': 'darkred',
        'Moderada_precariedad': 'orange',
        'Empleo_estable': 'darkgreen'
    }

    fig4, ax4 = plt.subplots(figsize=(9,5))
    ingreso_precariedad.plot(
        kind='barh',
        ax=ax4,
        color=[colores.get(i, 'gray') for i in ingreso_precariedad.index]
    )

    for i, v in enumerate(ingreso_precariedad):
        ax4.text(v + 10, i, f'S/. {v:.2f}')

    ax4.set_title("Ingreso promedio según precariedad")
    st.pyplot(fig4)

with col2:
    st.markdown("""
Alta → menor ingreso  
Moderada → intermedio  
Estable → mayor ingreso  
""")

st.write("📌 Valores reales:")
st.write(ingreso_precariedad)

st.divider()

# =========================
# 🧾 CONCLUSIONES
# =========================
st.subheader("🧾 Conclusiones")

porcentaje_subempleo = df['Subempleado'].mean() * 100

st.markdown(f"""
- El **{porcentaje_subempleo:.1f}%** está en subempleo  
- La precariedad reduce ingresos  
- Existen desigualdades estructurales  

➡️ Se requiere mejorar la calidad del empleo
""")