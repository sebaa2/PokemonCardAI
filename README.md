# 🎴 Pokémon Card AI

Sistema de reconocimiento de cartas Pokémon mediante **Machine Learning** y **Computer Vision**, desarrollado en **Python**. El proyecto utiliza **Transfer Learning con MobileNetV2** para generar embeddings de las imágenes y encontrar la carta más similar mediante **Cosine Similarity**.

La aplicación cuenta con una interfaz web desarrollada con **Streamlit**, permitiendo cargar imágenes, visualizar los resultados y almacenar el historial de búsquedas.

---

## ⚠️ Aviso

Este proyecto utiliza un dataset de cartas Pokémon obtenido desde Kaggle. Las imágenes y marcas comerciales pertenecen a sus respectivos propietarios y se utilizan únicamente con fines educativos y de investigación.

## 📌 Características

- 🎴 Identificación automática de cartas Pokémon.
- 🧠 Modelo basado en MobileNetV2 (Transfer Learning).
- 📊 Comparación mediante Cosine Similarity.
- 🏆 Muestra las 5 cartas más similares.
- 🖥️ Interfaz web desarrollada con Streamlit.
- 💾 Historial de búsquedas utilizando SQLite.
- 📷 Vista previa de la imagen analizada.
- ⚡ Actualización incremental de embeddings al agregar nuevas cartas.

---

## 🛠️ Tecnologías

- Python 3.10+
- TensorFlow / Keras
- MobileNetV2
- NumPy
- Scikit-Learn
- Pillow
- Streamlit
- SQLite

---

## 📂 Estructura del proyecto

```text
PokemonCardAI/
│
├── app.py                    # Aplicación Streamlit
├── database/
│   ├── history.py            # Funciones de SQLite
│   └── pokemon.db
│
├── dataset/
│   ├── processed/            # Imágenes procesadas
│   └── embeddings/           # Embeddings y nombres
│
├── results/                  # Imágenes temporales
│
├── scripts/
│   ├── prepare_dataset.py
│   ├── create_embeddings.py
│   ├── update_embeddings.py
│   ├── check_dataset.py
│   └── predict.py
│
├── requirements.txt
└── README.md
```

---

# 🚀 Instalación

Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/PokemonCardAI.git
cd PokemonCardAI
```

Crear un entorno virtual.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Instalar dependencias.

```bash
pip install -r requirements.txt
```

---

# ▶️ Ejecutar la aplicación

Iniciar la interfaz web.

```bash
streamlit run app.py
```

Luego abrir el navegador en:

```
http://localhost:8501
```

---

# 🧠 Funcionamiento

El proceso de identificación sigue los siguientes pasos:

1. El usuario carga una imagen de una carta Pokémon.
2. La imagen se redimensiona y preprocesa.
3. MobileNetV2 genera un embedding de la imagen.
4. El embedding se compara con todos los embeddings del dataset utilizando Cosine Similarity.
5. Se muestran las cinco coincidencias con mayor similitud.
6. La mejor coincidencia se almacena en el historial SQLite.

---

# 📦 Dataset

Este proyecto utiliza el dataset **Pokemon TCG All Image Cards** disponible en Kaggle.

El dataset **no se incluye** en este repositorio debido a su tamaño.

---

# 🔄 Preparación del dataset

## Primera ejecución

Procesar el dataset:

```bash
python scripts/prepare_dataset.py
```

Generar todos los embeddings:

```bash
python scripts/create_embeddings.py
```

---

## Cuando se agregan nuevas cartas

Actualizar únicamente las nuevas imágenes:

```bash
python scripts/prepare_dataset.py
python scripts/update_embeddings.py
python scripts/check_dataset.py
```

---

# 📷 Capturas

## Pantalla principal

> Agregar captura de la aplicación.

---

## Resultado de búsqueda

> Agregar captura mostrando la mejor coincidencia y el Top 5.

---

## Historial

> Agregar captura del historial de búsquedas.

---

# 🚀 Mejoras futuras

- Captura desde cámara web.
- Reconocimiento mediante OCR del número de colección.
- Filtros avanzados para el historial.
- Estadísticas de uso.
- Soporte para nuevos datasets.

---

# Autor

**Sebastián Cisternas**
