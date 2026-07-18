from vision.mutli_predict import analizar_imagen
import streamlit as st
from pathlib import Path
import sys
import json

# Permitir importar módulos del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


def obtener_total_cartas():
    try:
        with open(
            "dataset/embeddings/processed_index.json",
            "r",
            encoding="utf-8"
        ) as f:
            index = json.load(f)

        return len(index)

    except FileNotFoundError:
        return 0


def cargar_css():

    with open(
        "assets/style.css"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


# =========================
# Configuración página
# =========================

st.set_page_config(
    page_title="Pokemon Card AI",
    page_icon="🃏",
    layout="wide"
)

cargar_css()

col1, col2 = st.columns(
    [1, 4]
)

with col1:

    st.markdown(
        '''
        <div class="app-logo">
            <img src="data:image/png;base64,{}" alt="Pokemon Card AI logo">
        </div>
        '''.format(
            __import__("base64").b64encode(
                (PROJECT_ROOT / "assets" / "logo.png").read_bytes()
            ).decode("ascii")
        ),
        unsafe_allow_html=True
    )

with col2:

    st.title(" Pokemon Card AI")

    st.caption(
        "Reconocimiento automático de cartas Pokémon mediante Computer Vision y Machine Learning"
    )

    c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "📦 Cartas",
        f"{obtener_total_cartas():,}".replace(",", ".")
    )

with c2:
    st.metric(
        "🧠 Modelo",
        "MobileNetV2"
    )

with c3:
    st.metric(
        "⚡ Framework",
        "TensorFlow"
    )

with c4:
    st.metric(
        "🖥 Interfaz",
        "Streamlit"
    )

st.write(
    "Sistema de reconocimiento de cartas Pokémon utilizando "
    "Computer Vision y Machine Learning"
)


# =========================
# Carpetas
# =========================

RESULTS = PROJECT_ROOT / "results"

UPLOADS = RESULTS / "uploads"

UPLOADS.mkdir(
    parents=True,
    exist_ok=True
)


# =========================
# Subida imagen
# =========================

archivo = st.file_uploader(
    "Sube una imagen con cartas Pokémon",
    type=[
        "png",
        "jpg",
        "jpeg"
    ]
)


if archivo:

    ruta_imagen = UPLOADS / archivo.name

    with open(
        ruta_imagen,
        "wb"
    ) as f:

        f.write(
            archivo.getbuffer()
        )

    st.success(
        "Imagen cargada correctamente"
    )

    # Mostrar original

    st.subheader(
        "Imagen original"
    )

    st.image(
        ruta_imagen,
        width=400
    )

    # =========================
    # Ejecutar análisis
    # =========================

    with st.spinner(
        "Detectando cartas..."
    ):

        resultados, imagen_detectada = analizar_imagen(
            ruta_imagen
        )

    st.success(
        f"Cartas encontradas: {len(resultados)}"
    )

    # =========================
    # Imagen detecciones
    # =========================

    st.subheader(
        "Detecciones"
    )

    st.image(
        imagen_detectada,
        width=700
    )

    # =========================
    # Resultados
    # =========================

    st.subheader(
        "Resultados"
    )

    for carta in resultados:

        st.divider()

        st.markdown(
            f"""
            ## 🃏 Carta #{carta['id']}
            """
        )

        col1, col2 = st.columns(
            [1, 2]
        )

        with col1:

            st.image(
                carta["ruta"],
                width=180
            )

        with col2:

            mejor = carta[
                "coincidencias"
            ][0]

            st.write(
                f"**Carta:** {mejor['carta']}"
            )

            st.write(
                f"**Set:** {mejor['set']}"
            )

            st.write(
                f"**Código:** {mejor['codigo']}"
            )

            st.write(
                f"**Similitud:** {mejor['similitud']:.2f}%"
            )

            if mejor["similitud"] < 70:

                st.toast(
                    "Resultado no seguro: la coincidencia es menor al 70%. "
                    "Verifica la carta manualmente.",
                    icon="⚠️"
                )

            st.write(
                "Top 5 coincidencias"
            )

            for resultado in carta["coincidencias"]:

                st.write(
                    f"- {resultado['carta']} "
                    f"({resultado['similitud']:.2f}%)"
                )
