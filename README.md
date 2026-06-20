https://share.streamlit.io/usuario/repo (Reemplazar con la URL final de Streamlit Cloud)

# Trabajo 4 (TB4) - Data Visualization
Este repositorio contiene la solución completa para el Trabajo 4 (TB4) de Data Visualization. Se ha implementado un dashboard interactivo utilizando Streamlit y un Jupyter Notebook como bitácora de desarrollo y registro de compilación de datos.

## Estructura del Repositorio
- `app.py`: Archivo principal del dashboard interactivo en Streamlit.
- `desarrollo.ipynb`: Jupyter Notebook que contiene la bitácora de desarrollo, fusión de datos, cálculos matemáticos y gráficos de prueba.
- `requirements.txt`: Dependencias exactas de Python para reproducir el proyecto.
- `paleta.md`: Documentación de la validación de accesibilidad colorblind-safe de la paleta de colores.
- `data/`:
  - `merge.py`: Script para automatizar la descarga y fusión de los datasets (OWID + Kaggle). Generado automáticamente desde el notebook.
  - `merged_dataset.csv`: Dataset final unificado (países + agregados regionales).

## Ejecución Local

### Prerrequisitos
Tener instalado Python 3.12 y pip.

### Instrucciones
1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. (Opcional) Ejecutar el procesamiento de datos. Si no cuentas con el dataset unificado, ejecuta el script de fusión:
   ```bash
   python data/merge.py
   ```

4. Correr la aplicación de Streamlit:
   ```bash
   streamlit run app.py
   ```

## Decisiones de Diseño (Storytelling con Datos)
- **Claridad Visual:** Todos los ejes Y de barras parten estrictamente en 0. Se usan barras horizontales para países y deltas para evitar etiquetas en diagonal de difícil lectura.
- **Leyendas Integradas:** Se omiten cajas flotantes y se colocan anotaciones de texto directamente al final de las trayectorias de las líneas.
- **Regla del 60-30-10:** Reducción de carga cognitiva con fondos e interfaces claras (60%), contexto en grises apagados (30%), y destaque de Perú en naranja de alto contraste (10%).
