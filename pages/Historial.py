"""Panel de estadísticas del historial de identificaciones."""

from database.history import obtener_historial_completo
import base64
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def cargar_css():
    with open(PROJECT_ROOT / "assets" / "style.css", encoding="utf-8") as archivo_css:
        st.markdown(f"<style>{archivo_css.read()}</style>",
                    unsafe_allow_html=True)


st.set_page_config(page_title="Historial | Pokemon Card AI",
                   page_icon="🃏", layout="wide")
cargar_css()

logo_base64 = base64.b64encode(
    (PROJECT_ROOT / "assets" / "logo.png").read_bytes()).decode("ascii")
st.markdown(
    f'''<section class="hero">
        <div class="hero__glow hero__glow--one"></div><div class="hero__glow hero__glow--two"></div>
        <img class="hero__logo" src="data:image/png;base64,{logo_base64}" alt="Logo Pokemon Card AI">
        <div class="hero__content"><p class="eyebrow">ACTIVIDAD DE LA COLECCIÓN</p>
        <h1>Historial <span>AI</span></h1>
        <p class="hero__subtitle">Revisa las cartas identificadas y la distribución de tus búsquedas por expansión.</p></div>
        <div class="hero__badge"><span class="status-dot"></span>Base de datos activa</div>
    </section>''',
    unsafe_allow_html=True,
)

historial = obtener_historial_completo()
columnas = ["Carta", "Expansión", "Similitud", "Fecha"]
datos = pd.DataFrame(historial, columns=columnas)

if datos.empty:
    st.info(
        "Aún no hay búsquedas guardadas. Identifica una carta para generar estadísticas.")
    st.stop()

datos["Similitud"] = pd.to_numeric(datos["Similitud"], errors="coerce")
datos["Fecha"] = pd.to_datetime(datos["Fecha"], errors="coerce")

total_busquedas = len(datos)
similitud_promedio = datos["Similitud"].mean()
ultima_busqueda = datos["Fecha"].max()

cartas_unicas = datos["Carta"].nunique()
expansiones_unicas = datos["Expansión"].nunique()
mejor_similitud = datos["Similitud"].max()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Búsquedas",
        total_busquedas
    )

with c2:
    st.metric(
        "Cartas únicas",
        cartas_unicas
    )

with c3:
    st.metric(
        "Expansiones",
        expansiones_unicas
    )

c4, c5, c6 = st.columns(3)

with c4:
    st.metric(
        "Similitud promedio",
        f"{similitud_promedio:.1f}%"
    )

with c5:
    st.metric(
        "Mejor coincidencia",
        f"{mejor_similitud:.1f}%"
    )

with c6:

    fecha = (
        ultima_busqueda.strftime("%d-%m-%Y %H:%M")
        if pd.notna(ultima_busqueda)
        else "-"
    )

    st.metric(
        "Última búsqueda",
        fecha
    )

por_expansion = (
    datos.groupby("Expansión").size().sort_values(
        ascending=False).head(10).rename("Búsquedas")
)

tendencia_temporal = (
    datos.dropna(subset=["Fecha"])
    .assign(Fecha=lambda registros: registros["Fecha"].dt.normalize())
    .groupby("Fecha")
    .size()
    .rename("Búsquedas")
)

tab_estadisticas, tab_tendencias = st.tabs(["📊 Estadísticas", "📈 Tendencias"])

with tab_estadisticas:
    st.markdown(
        '<div class="section-heading"><span>01</span><div><h2>Búsquedas por expansión</h2>'
        '<p>Distribución de todas las identificaciones almacenadas.</p></div></div>',
        unsafe_allow_html=True,
    )
    st.bar_chart(por_expansion, color="#ffcb05", use_container_width=True)

with tab_tendencias:
    st.markdown(
        '<div class="section-heading"><span>01</span><div><h2>Búsquedas a lo largo del tiempo</h2>'
        '<p>Evolución diaria de las identificaciones almacenadas.</p></div></div>',
        unsafe_allow_html=True,
    )
    if tendencia_temporal.empty:
        st.info("No hay fechas disponibles para mostrar la tendencia.")
    else:
        st.line_chart(tendencia_temporal, color="#e3350d", use_container_width=True)


st.markdown(
    '<div class="section-heading"><span>02</span><div><h2>Registros recientes</h2>'
    '<p>Las últimas 20 coincidencias guardadas en la base de datos.</p></div></div>',
    unsafe_allow_html=True,
)

buscar = st.text_input(
    "Buscar carta"
)

expansion = st.selectbox(
    "Expansión",
    ["Todas"] + sorted(
        datos["Expansión"].unique()
    )
)

similitud = st.slider(
    "Similitud mínima",
    0,
    100,
    70
)

filtrado = datos.copy()

if buscar:

    filtrado = filtrado[
        filtrado["Carta"]
        .str.contains(
            buscar,
            case=False
        )
    ]

if expansion != "Todas":

    filtrado = filtrado[
        filtrado["Expansión"] == expansion
    ]

filtrado = filtrado[
    filtrado["Similitud"] >= similitud
]

tabla = (
    filtrado
    .sort_values(
        "Fecha",
        ascending=False
    )
    .head(20)
)

tabla["Similitud"] = tabla["Similitud"].map(
    lambda valor: f"{valor:.2f}%"
    if pd.notna(valor)
    else "—"
)

tabla["Fecha"] = (
    tabla["Fecha"]
    .dt.strftime("%d-%m-%Y %H:%M")
    .fillna("—")
)

st.dataframe(
    tabla,
    use_container_width=True,
    hide_index=True
)

csv = datos.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "Descargar historial en CSV",
    data=csv,
    file_name="historial_busquedas_pokemon.csv",
    mime="text/csv",
    use_container_width=True,
)
