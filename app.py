from pathlib import Path
import streamlit as st

from scripts.predict import buscar_cartas
from database.history import (
    guardar_busqueda,
    obtener_historial
)

PROJECT_ROOT = Path(__file__).resolve().parent

DATASET = PROJECT_ROOT / "dataset" / "processed"

RESULTS = PROJECT_ROOT / "results"
RESULTS.mkdir(exist_ok=True)

# --------------------------------------------------------

st.set_page_config(
    page_title="Identificador Pokémon",
    page_icon="🎴",
    layout="wide"
)

st.title("🎴 Identificador de Cartas Pokémon")

st.markdown(
    """
Identifica cartas Pokémon utilizando **Machine Learning**
basado en **MobileNetV2** y búsqueda por similitud mediante
**Embeddings**.
"""
)

# --------------------------------------------------------
# Sidebar
# --------------------------------------------------------

with st.sidebar:

    st.title("🎴 Pokémon Card AI")

    st.divider()

    st.success("Modelo: MobileNetV2")

    st.success("Método: Cosine Similarity")

    st.info(
        "Sube una imagen y el sistema buscará "
        "las cartas más parecidas."
    )

# --------------------------------------------------------

imagen = st.file_uploader(
    "Selecciona una imagen",
    type=["png", "jpg", "jpeg"]
)

# --------------------------------------------------------

if imagen:

    ruta_temporal = RESULTS / "temp.png"

    with open(ruta_temporal, "wb") as f:
        f.write(imagen.getbuffer())

    col1, col2 = st.columns(2)

    # ----------------------------------------------------
    # Imagen subida
    # ----------------------------------------------------

    with col1:

        st.subheader("📷 Imagen subida")

        st.image(
            imagen,
            width=260
        )

    # ----------------------------------------------------

    if st.button(
        "🔍 Buscar carta",
        use_container_width=True
    ):

        barra = st.progress(
            0,
            text="Preparando imagen..."
        )

        barra.progress(
            20,
            text="Generando características..."
        )

        resultados = buscar_cartas(
            ruta_temporal
        )

        barra.progress(
            70,
            text="Buscando coincidencias..."
        )

        guardar_busqueda(
            resultados[0]["carta"],
            resultados[0]["set"],
            resultados[0]["similitud"]
        )

        barra.progress(
            100,
            text="Proceso finalizado"
        )

        barra.empty()

        st.success("Carta encontrada correctamente.")

        # ==================================================
        # Resultado
        # ==================================================

        with col2:

            mejor = resultados[0]

            st.subheader("🏆 Mejor coincidencia")

            ruta_imagen = (
                DATASET /
                mejor["archivo"]
            )

            if ruta_imagen.exists():

                st.image(
                    str(ruta_imagen),
                    width=180
                )

            colA, colB = st.columns(2)

            with colA:

                st.metric(
                    "Similitud",
                    f"{mejor['similitud']:.2f}%"
                )

            with colB:

                st.metric(
                    "Código",
                    mejor["codigo"]
                )

            st.write(
                f"### {mejor['carta']}"
            )

            st.write(
                f"**Set:** {mejor['set']}"
            )

            st.divider()

            st.subheader(
                "📋 Otras coincidencias"
            )

            for carta in resultados[1:]:

                with st.container(border=True):

                    c1, c2 = st.columns([3, 1])

                    with c1:

                        st.write(
                            f"**{carta['carta']}**"
                        )

                        st.caption(
                            f"Set: {carta['set']}"
                        )

                        st.caption(
                            f"Código: {carta['codigo']}"
                        )

                    with c2:

                        st.metric(
                            "Match",
                            f"{carta['similitud']:.2f}%"
                        )

        # ==================================================
        # Historial
        # ==================================================

        st.divider()

        st.subheader(
            "📜 Historial de búsquedas"
        )

        historial = obtener_historial()

        if historial:

            st.dataframe(
                historial,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Todavía no existen búsquedas."
            )