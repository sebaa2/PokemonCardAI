from pathlib import Path
import streamlit as st

from scripts.predict import buscar_cartas
from database.history import guardar_busqueda
from database.history import obtener_historial

PROJECT_ROOT = Path(__file__).resolve().parent
DATASET = PROJECT_ROOT / "dataset" / "processed"

RESULTS = PROJECT_ROOT / "results"
RESULTS.mkdir(exist_ok=True)

st.set_page_config(
    page_title="Identificador Pokémon",
    page_icon="🎴",
    layout="wide"
)

st.title("🎴 Identificador de Cartas Pokémon")

st.write(
    "Sube una imagen para identificar la carta."
)

imagen = st.file_uploader(
    "Selecciona una imagen",
    type=["png", "jpg", "jpeg"]
)

if imagen:

    ruta_temporal = RESULTS / "temp.png"

    with open(ruta_temporal, "wb") as f:
        f.write(imagen.getbuffer())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Imagen subida")
        st.image(imagen, use_container_width=True)

    if st.button("Buscar carta"):

        with st.spinner("Analizando carta..."):

            resultados = buscar_cartas(ruta_temporal)

            guardar_busqueda(
                resultados[0]["carta"],
                resultados[0]["set"],
                resultados[0]["similitud"]
            )

        with col2:

            st.subheader("Resultado")

            for i, carta in enumerate(resultados, start=1):
                ruta_imagen = DATASET / carta["archivo"]

                st.markdown(f"### {i}. {carta['carta']}")

                if ruta_imagen.exists():
                    st.image(
                    str(ruta_imagen),
                    width=220
            )

                st.write(f"**Set:** {carta['set']}")

                st.write(f"**Código:** {carta['codigo']}")

                st.write(f"**Similitud:** {carta['similitud']:.2f}%")

                st.divider()


