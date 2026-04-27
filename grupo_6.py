import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análisis Laboral", layout="wide")

# 🔹 TÍTULO
st.title("📊 Análisis del Mercado Laboral Informal")

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

# 🔥 CARGA DE DATOS (ARREGLADO)
df = pd.read_csv("Grupo 6/Equipo6_EconomiaInformal.csv")

# 🔥 LIMPIEZA Y VARIABLES
df.columns = df.columns.str.strip()

df['Precariedad'] = df['Ingreso_Mensual'].apply(
    lambda x: 'Alta' if x < 1000 else 'Media' if x < 2000 else 'Baja'
)

df['Subempleado'] = (df['Horas_Trabajadas_Semana'] < 30) & (df['Tiene_Contrato_Escrito'] == 'No')

# 🔹 DATOS
st.subheader("📋 Vista general")
st.write(df.head())

st.subheader("📉 Subempleo")
st.write(df['Subempleado'].value_counts())

st.subheader("⚠️ Precariedad")
st.write(df['Precariedad'].value_counts())

st.divider()

# =========================
# 📊 GRÁFICO 1
# =========================
st.subheader("💰 Ingreso por Tipo de Actividad")

ingreso_actividad = df.groupby('Tipo_Actividad')['Ingreso_Mensual'].mean().sort_values()

fig1, ax1 = plt.subplots(figsize=(9,5))
bars = ax1.barh(
    ingreso_actividad.index,
    ingreso_actividad.values,
    color=['#FDCF76','#89AEB2','#3465e0','#E08963','#7be069']
)

for bar, val in zip(bars, ingreso_actividad.values):
    ax1.text(val + 10, bar.get_y() + bar.get_height()/2, f'S/ {val:.0f}', va='center')

ax1.set_xlabel('Ingreso Mensual Promedio (S/)')
ax1.set_title('Ingreso Promedio por Tipo de Actividad')

st.pyplot(fig1)

# =========================
# 📊 GRÁFICO 2
# =========================
st.subheader("📍 Contrato por Zona")

contrato_zona = df.groupby(['Zona', 'Tiene_Contrato_Escrito']).size().unstack()
contrato_zona_pct = contrato_zona.div(contrato_zona.sum(axis=1), axis=0) * 100

fig2, ax2 = plt.subplots(figsize=(7,5))
contrato_zona_pct.plot(
    kind='bar',
    ax=ax2,
    color=['#d9534f','#5cb85c'],
    edgecolor='white'
)

ax2.set_title('Proporción con/sin Contrato Escrito por Zona (%)')
ax2.set_ylabel('Porcentaje (%)')
ax2.set_xlabel('Zona')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
ax2.legend(['Sin contrato (No)', 'Con contrato (Sí)'], title='Contrato')

for p in ax2.patches:
    ax2.annotate(
        str(round(p.get_height(), 1)) + '%',
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center', va='center',
        xytext=(0, 5),
        textcoords='offset points'
    )

st.pyplot(fig2)

# =========================
# 📊 GRÁFICO 3
# =========================
st.subheader("📊 Acceso a Beneficios")

beneficios_formal = df.groupby(['Formalidad', 'Acceso_Beneficios']).size().unstack()
beneficios_pct = beneficios_formal.div(beneficios_formal.sum(axis=1), axis=0) * 100

fig3, ax3 = plt.subplots(figsize=(8,5))
beneficios_pct.plot(
    kind='bar',
    ax=ax3,
    color=['#f0ad4e','#5bc0de','#5cb85c'],
    edgecolor='white'
)

for c in ax3.containers:
    ax3.bar_label(c, fmt='%.0f%%', padding=3)

ax3.set_title('Acceso a Beneficios según Formalidad (%)')
ax3.set_ylabel('Porcentaje (%)')
ax3.set_xlabel('Formalidad')
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=0)
ax3.legend(title='Beneficios')

st.pyplot(fig3)

# =========================
# 📊 GRÁFICO 4
# =========================
st.subheader("📉 Ingreso por Nivel de Precariedad")

ingreso_por_precariedad = df.groupby('Precariedad')['Ingreso_Mensual'].mean().sort_values().round(2)

fig4, ax4 = plt.subplots(figsize=(9,5))
ingreso_por_precariedad.plot(
    kind='barh',
    ax=ax4,
    color=['darkred', 'orange', 'darkgreen']
)

ax4.set_title('Comparativa de Ingresos Promedio por Nivel de Precariedad')
ax4.set_xlabel('Ingreso Mensual Promedio (S/.)')
ax4.set_ylabel('Nivel de Precariedad')
ax4.grid(axis='x', linestyle='--', alpha=1)

for index, value in enumerate(ingreso_por_precariedad):
    ax4.text(value + 10, index, f'S/. {value:.2f}', va='center')

st.pyplot(fig4)

st.divider()

# 🔍 HALLAZGOS
st.subheader("🔍 Hallazgos clave")

st.markdown("""
- Existe diferencia de ingresos según tipo de actividad.
- Hay desigualdad en contratos según zona.
- La informalidad reduce beneficios.
- A mayor precariedad, menor ingreso.
- Existe subempleo en la muestra.
""")