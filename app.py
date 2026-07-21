"""Interfaz principal de Pokemon Card AI."""

import base64
import json
import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from vision.mutli_predict import analizar_imagen


def obtener_total_cartas():
    """Devuelve el total de cartas disponibles en el índice local."""
    try:
        with open(
            PROJECT_ROOT / "dataset" / "embeddings" / "processed_index.json",
            encoding="utf-8",
        ) as archivo_indice:
            return len(json.load(archivo_indice))
    except FileNotFoundError:
        return 0


def cargar_css():
    with open(PROJECT_ROOT / "assets" / "style.css", encoding="utf-8") as archivo_css:
        st.markdown(f"<style>{archivo_css.read()}</style>", unsafe_allow_html=True)


@st.dialog("Identificando cartas", dismissible=False)
def mostrar_progreso(ruta_imagen, token_archivo):
    """Muestra un modal bloqueante mientras se ejecuta la identificación."""
    st.markdown(
        '<div class="processing-modal"><div class="processing-icon">◈</div>'
        '<h3>Analizando tu colección</h3>'
        '<p>La imagen se está procesando. Esto puede tardar unos segundos.</p></div>',
        unsafe_allow_html=True,
    )
    estado = st.empty()
    progreso = st.progress(8)
    estado.caption("Preparando la imagen…")
    progreso.progress(25)
    estado.caption("Detectando cartas y buscando coincidencias…")

    resultados, imagen_detectada = analizar_imagen(ruta_imagen)

    progreso.progress(88)
    estado.caption("Organizando los resultados…")
    st.session_state["resultado_analisis"] = (resultados, imagen_detectada)
    st.session_state["archivo_analizado"] = token_archivo
    progreso.progress(100)
    estado.caption("Análisis completado.")
    st.rerun()


st.set_page_config(page_title="Pokemon Card AI", page_icon="🃏", layout="wide")
cargar_css()

logo_base64 = base64.b64encode((PROJECT_ROOT / "assets" / "logo.png").read_bytes()).decode("ascii")
st.markdown(
    f'''<section class="hero">
        <div class="hero__glow hero__glow--one"></div><div class="hero__glow hero__glow--two"></div>
        <img class="hero__logo" src="data:image/png;base64,{logo_base64}" alt="Logo Pokemon Card AI">
        <div class="hero__content"><p class="eyebrow">COLECCIÓN INTELIGENTE</p>
        <h1>Pokémon Card <span>AI</span></h1>
        <p class="hero__subtitle">Identifica tus cartas en segundos mediante visión computacional y aprendizaje automático.</p></div>
        <div class="hero__badge"><span class="status-dot"></span>Sistema listo</div>
    </section>''',
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Cartas indexadas", f"{obtener_total_cartas():,}".replace(",", "."))
with c2:
    st.metric("Modelo", "MobileNetV2")
with c3:
    st.metric("Framework", "TensorFlow")
with c4:
    st.metric("Interfaz", "Streamlit")

st.markdown(
    '<div class="section-heading"><span>01</span><div><h2>Analiza tu imagen</h2>'
    '<p>Sube una fotografía clara con una o varias cartas visibles.</p></div></div>',
    unsafe_allow_html=True,
)

RESULTS = PROJECT_ROOT / "results"
UPLOADS = RESULTS / "uploads"
UPLOADS.mkdir(parents=True, exist_ok=True)

archivo = st.file_uploader(
    "Arrastra una imagen o selecciona un archivo", type=["png", "jpg", "jpeg"]
)

if archivo:
    ruta_imagen = UPLOADS / archivo.name
    token_archivo = f"{archivo.name}-{archivo.size}"

    if st.session_state.get("archivo_analizado") != token_archivo:
        with open(ruta_imagen, "wb") as imagen_subida:
            imagen_subida.write(archivo.getbuffer())
        mostrar_progreso(ruta_imagen, token_archivo)

    resultado_analisis = st.session_state.get("resultado_analisis")
    if not resultado_analisis:
        st.stop()

    resultados, imagen_detectada = resultado_analisis

    st.success(f"Cartas encontradas: {len(resultados)}")

    original_col, detection_col = st.columns([1, 1.5], gap="large")
    with original_col:
        st.markdown('<div class="image-label">IMAGEN ORIGINAL</div>', unsafe_allow_html=True)
        st.image(ruta_imagen, use_container_width=True)
    with detection_col:
        st.markdown('<div class="image-label">CARTAS DETECTADAS</div>', unsafe_allow_html=True)
        st.image(imagen_detectada, use_container_width=True)

    st.markdown(
        '<div class="section-heading results-heading"><span>02</span><div><h2>Resultados del análisis</h2>'
        '<p>Las coincidencias se ordenan por porcentaje de similitud.</p></div></div>',
        unsafe_allow_html=True,
    )

    for carta in resultados:
        mejor = carta["coincidencias"][0]
        similitud = mejor["similitud"]
        confianza = "Alta confianza" if similitud >= 85 else "Confianza media" if similitud >= 70 else "Revisar resultado"
        clase_confianza = "high" if similitud >= 85 else "medium" if similitud >= 70 else "low"

        col_imagen, col_info = st.columns([1, 2], gap="large")
        with col_imagen:
            st.image(carta["ruta"], use_container_width=True)
        with col_info:
            st.markdown(
                f'''<div class="result-card__header"><div><p class="result-card__eyebrow">CARTA #{carta['id']}</p>
                <h3>{mejor['carta']}</h3></div><div class="confidence {clase_confianza}">{similitud:.1f}%
                <small>{confianza}</small></div></div>''',
                unsafe_allow_html=True,
            )
            st.write(f"**Set:** {mejor['set']}")
            st.write(f"**Código:** {mejor['codigo']}")

            if similitud < 70:
                st.warning("Resultado poco seguro: verifica la carta manualmente.")

            st.markdown('<p class="matches-title">OTRAS COINCIDENCIAS</p>', unsafe_allow_html=True)
            for resultado in carta["coincidencias"]:
                st.write(f"- {resultado['carta']} ({resultado['similitud']:.2f}%)")
        st.divider()
