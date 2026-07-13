# Pokemon Card AI

Sistema de reconocimiento de cartas Pokémon utilizando Machine Learning y Computer Vision.

## Tecnologías

- Python 3.10+
- TensorFlow
- MobileNetV2
- OpenCV
- NumPy
- Scikit-Learn

## Funcionalidades

- Preparación automática del dataset.
- Extracción de embeddings.
- Reconocimiento de cartas mediante similitud del coseno.
- Compatible con miles de cartas Pokémon.

## Estructura del proyecto

```
PokemonCardAI/
├── dataset/
├── models/
├── results/
├── scripts/
├── requirements.txt
└── README.md
```

## Instalación

```bash
git clone https://github.com/TU_USUARIO/PokemonCardAI.git
cd PokemonCardAI

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

## Dataset

Este proyecto utiliza el dataset **Pokemon TCG All Image Cards** de Kaggle.

El dataset no está incluido en este repositorio.

## Autor

Sebastián Cisternas