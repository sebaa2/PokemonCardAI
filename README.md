# Pokémon Card AI

Aplicación web para identificar cartas Pokémon a partir de una fotografía. Combina visión computacional para detectar una o varias cartas en la imagen y *transfer learning* con MobileNetV2 para encontrar las coincidencias más similares en un índice local.

---

> Proyecto educativo. Las imágenes, nombres y marcas de Pokémon pertenecen a sus respectivos propietarios.

## 📌 Características

- Detecta una o varias cartas en una misma fotografía.
- Genera embeddings con MobileNetV2 y compara mediante similitud del coseno.
- Muestra las cinco coincidencias más cercanas por cada carta detectada.
- Indica el nivel de confianza de cada coincidencia.
- Guarda las búsquedas en una base de datos SQLite local.
- Incluye un panel de historial con métricas, filtros, gráficos y exportación a CSV.
- Permite actualizar el índice de embeddings al incorporar cartas nuevas.

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

<img width="1454" height="833" alt="image" src="https://github.com/user-attachments/assets/65e5224c-fb0f-4e1b-8503-01c11e617d53" />

---

## Resultado de búsqueda

> Agregar captura mostrando la mejor coincidencia y el Top 5.

<img width="1242" height="586" alt="image" src="https://github.com/user-attachments/assets/1ff6b24d-f62c-4c2e-955e-6adb45ba636f" />

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
