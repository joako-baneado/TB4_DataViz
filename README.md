https://tb4dataviz-hfam9wvdjyckrxjpscbh3c.streamlit.app/

# Trabajo 4 (TB4) - Data Visualization (S12)

Este proyecto consiste en un dashboard interactivo desarrollado en Streamlit y un Jupyter Notebook de desarrollo que analizan la evolución de la transición energética global, regional y la posición estratégica de Perú (2000-2020) bajo los principios de **Storytelling with Data**.

## Integrantes
- Joaquin Basas
- Joaquin Alvarado
- Alejandro Colfer
- Nataly Anaya
- Mark Esquivel

## Estructura del Proyecto

El proyecto está ubicado en la raíz del repositorio y contiene los siguientes archivos:
- `desarrollo.ipynb`: Bitácora de desarrollo y registro interactivo de la limpieza de datos, fusión de datasets y prototipado.
- `app.py`: Aplicación y dashboard interactivo de Streamlit que presenta las visualizaciones de las preguntas Q1 a Q9, además de la sección de defensa de diseño (Q10).
- `paleta.md`: Documentación exigida sobre la paleta de colores adoptada y su validación de accesibilidad colorblind-safe.
- `requirements.txt`: Archivo de dependencias del proyecto con versiones exactas.
- `data/`: Directorio que contiene el dataset consolidado (`merged_dataset.csv`) y el script robusto de fusión (`merge.py`).

## Instrucciones de Ejecución Local

### Prerrequisitos

Asegúrate de tener instalada una versión moderna de Python (por ejemplo, Python 3.12).

### Instalación de Dependencias

Ejecuta el siguiente comando para instalar las librerías necesarias:
```bash
pip install -r requirements.txt
```

### Ejecución del Notebook de Desarrollo

Si deseas regenerar el dataset unificado y compilar el notebook de desarrollo, ejecuta:
```bash
python -m nbconvert --to notebook --execute --inplace desarrollo.ipynb
```

### Ejecución del Dashboard de Streamlit

Para iniciar el servidor de Streamlit y visualizar el dashboard interactivo de forma local, ejecuta:
```bash
streamlit run app.py
```
