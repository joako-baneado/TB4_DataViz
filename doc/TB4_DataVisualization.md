TRABAJO 4 — TB4  |  DATA VISUALIZATION

TRABAJO 4 — TB4

Campo

Fecha

Detalle

19/06/26

Horario de construcción

7:00 p.m. – 11:00 p.m.  (4 horas)

Modalidad

Calificación

Grupal, hasta 5 integrantes

Vigesimal  (0 – 20)

CONDICIONES DE INICIO

Cada integrante llega con su entorno de trabajo ya configurado: Python instalado, librerías base
disponibles, cuenta de GitHub activa y cuenta de Streamlit Cloud vinculada al repositorio. No se
descuenta tiempo por problemas de configuración de entorno que ocurran después de las 7:00
p.m.

Datasets oficiales

Los datasets se descargan al inicio del examen desde las URLs siguientes. La primera tarea del
examen es integrar ambos mediante merge por country + year.

Dataset A  —  Our World in Data Energy (OWID)
Cobertura: ~200 países  |  1965–2024  |  ~130 variables
URL CSV: https://owid-public.owid.io/data/energy/owid-energy-data.csv
Codebook: https://github.com/owid/energy-data/blob/master/owid-energy-
codebook.csv

Dataset B  —  Global Data on Sustainable Energy 2000–2020 (Kaggle)
Cobertura: 176 países × 21 años  |  21 columnas
URL: https://www.kaggle.com/datasets/anshtanwar/global-data-on-
sustainable-energy
Variables clave: access_to_electricity,
renewable_share_of_total_energy,
CO2_emissions, gdp_per_capita, energy_intensity_primary_energy

DISTRIBUCIÓN DE TIEMPO RECOMENDADA

Página 1 de 8

TRABAJO 4 — TB4  |  DATA VISUALIZATION

PREGUNTAS DE EVALUACIÓN

El examen se estructura en torno a diez preguntas concretas. Durante la hora de evaluación, el
docente selecciona preguntas de esta lista y el grupo debe responderlas navegando el dashboard
en vivo. No hay presentación libre ni diapositivas; el dashboard es el único instrumento de
respuesta.

El grupo conoce esta lista desde el inicio del examen y debe construir el dashboard pensando en
que cada pregunta tenga una respuesta visual clara y navegable.

BLOQUE A  —  Panorama global  (Preguntas 1 a 3)

Pregunta 1   Líderes de la transición

¿Cuáles son los cinco países que más aumentaron su participación de energías renovables
entre 2000 y 2020, y cuántos puntos porcentuales ganaron? El dashboard debe mostrar esta
respuesta con una visualización que permita comparar la magnitud del cambio entre países
de forma inmediata, sin que el evaluador tenga que calcular nada.
Variables clave: renewable_share_of_total_energy, country, year (delta 2000–2020)

Pregunta 2   Trayectoria regional

¿Cómo evolucionó la intensidad de carbono de la electricidad en las principales regiones del
mundo entre 2000 y 2020? ¿Qué región redujo más y cuál empeoró? El dashboard debe
permitir comparar la trayectoria de múltiples regiones en un mismo gráfico, con la región de
mayor y menor reducción identificable sin ambigüedad.
Variables clave: carbon_intensity_elec, region, year

Pregunta 3   Riqueza vs. renovables

¿Existe una relación entre el PIB per cápita de un país y su participación de energías
renovables? ¿Los países más ricos son necesariamente los más renovables? El dashboard
debe mostrar esta relación con un gráfico que cruce ambas variables para todos los países
disponibles en un año seleccionable por el evaluador.
Variables clave: gdp_per_capita, renewable_share_of_total_energy, year
(seleccionable)

BLOQUE B  —  Patrones y comparaciones  (Preguntas 4 a 7)

Pregunta 4   Pobreza energética y fósiles

En el año que el evaluador indique, ¿qué países tenían menos del 50 % de acceso a
electricidad y al mismo tiempo una alta dependencia de combustibles fósiles? Mostrar ambas
dimensiones simultáneamente.
Variables clave: access_to_electricity, fossil_fuel_consumption (o equivalente
OWID), year (seleccionable)

Página 2 de 8

TRABAJO 4 — TB4  |  DATA VISUALIZATION

Pregunta 5   Ranking de consumo

¿Cómo cambió el ranking de los doce mayores consumidores de energía per cápita entre
2000 y 2020? ¿Qué países subieron y cuáles bajaron posiciones? El dashboard debe
mostrar el movimiento de cada país de forma rastreable visualmente a lo largo del tiempo.
Variables clave: energy_per_capita (OWID), country, year

Pregunta 6   Mix eléctrico por país

Para el país que el evaluador seleccione, ¿cuál fue su mix de generación eléctrica por fuente
(carbón, gas, nuclear, solar, eólica, hidro) en el año de mayor producción renovable? El
dashboard debe responder esta pregunta para cualquier país del dataset.
Variables clave: coal_elec, gas_elec, nuclear_elec, solar_elec, wind_elec,
hydro_elec (OWID), country seleccionable

Pregunta 7   América Latina: ¿quiénes mejoraron?

¿Qué países de América Latina mejoraron su intensidad de carbono entre 2000 y 2020 y
cuáles la empeoraron? Mostrar la dirección y magnitud del cambio para todos los países de
la región simultáneamente.
Variables clave: carbon_intensity_elec delta 2000–2020, filtrado por región =
América Latina

Página 3 de 8

TRABAJO 4 — TB4  |  DATA VISUALIZATION

BLOQUE C  —  Posición de Perú  (Preguntas 8 y 9)

Pregunta 8   Perú en la región

¿En qué posición se encuentra Perú respecto al promedio de América Latina en participación
de energías renovables, acceso a electricidad e intensidad energética? Las tres dimensiones
deben ser visibles en una sola visualización.
Variables clave: renewable_share_of_total_energy, access_to_electricity,
energy_intensity_primary_energy — Perú vs. promedio LA

Pregunta 9   Perú vs. vecinos

¿Cómo fue la trayectoria de Perú en consumo de energía per cápita comparada con Chile,
Colombia y Brasil entre 2000 y 2020? ¿En qué años Perú se alejó o se acercó al grupo?
Variables clave: energy_per_capita (OWID), country = Perú / Chile / Colombia /
Brasil, 2000–2020

BLOQUE D  —  Lectura crítica  (Pregunta 10)

Pregunta 10   Defensa de diseño

El evaluador selecciona cualquier gráfico del dashboard y pregunta: ¿por qué eligieron este
tipo de visualización para responder esta pregunta y no otro? ¿Qué encoding está usando y
qué limitación tiene este gráfico? Esta pregunta no se responde con el dashboard, sino con
argumentación verbal del equipo. Se evalúa que el equipo comprende las decisiones de
diseño que tomó, no que las haya memorizado.
Variables clave: Cualquier gráfico del dashboard — respuesta verbal

REQUERIMIENTOS TÉCNICOS DEL DASHBOARD

Para que el dashboard pueda responder las diez preguntas, debe incluir los siguientes tipos de
visualización y controles.

Visualizaciones obligatorias

–  Gráfico de barras divergentes o slope chart: para mostrar cambios entre dos períodos

(Preguntas 1 y 7).

–  Gráfico de líneas múltiples: para trayectorias temporales comparadas entre países o

regiones (Preguntas 2 y 9).

–  Scatter plot con al menos 3 encodings (posición x, posición y, color o tamaño): para

relaciones entre variables (Preguntas 3 y 4).

–  Bump chart o ranking visual: para cambios de posición en el tiempo (Pregunta 5).
–  Gráfico de composición por fuente (barras apiladas o barras al 100 %): para mix energético

por país (Pregunta 6).

–  Gráfico multidimensional con Perú destacado: para comparación regional (Pregunta 8).

Controles interactivos mínimos

–  Selector de país o región con multiselect que afecte simultáneamente al menos dos gráficos.

Página 4 de 8

TRABAJO 4 — TB4  |  DATA VISUALIZATION

–  Selector de año o rango temporal con slider que actualice al menos dos gráficos.
–  Tooltip en cada gráfico que muestre al menos 2 métricas adicionales al pasar el cursor.

Restricciones de diseño absolutas

Sin gráficos de torta ni donut en ninguna sección del dashboard. Sin gráficos 3D en ninguna
forma. El incumplimiento descuenta 1 punto por instancia detectada durante la evaluación.

Paleta de color: al menos una variante validada como colorblind safe en Colorbrewer
(colorbrewer2.org). Ver Anexo A al final de este documento para el procedimiento de validación.

Herramientas de despliegue aceptadas

Herramienta

Plataforma gratuita

URL resultante

Streamlit (Python)

streamlit.io/cloud

share.streamlit.io/usuario/repo

Dash + Plotly (Python)  Render o Railway

Tableau

Power BI

Tableau Public

Power BI Service

appname.onrender.com

public.tableau.com/...

app.powerbi.com/...

Página 5 de 8

TRABAJO 4 — TB4  |  DATA VISUALIZATION

ENTREGABLES FINALES

Son dos entregables únicos. Ambos se comparten con el docente exactamente a las 11:00 p.m.
La ausencia de cualquiera impide la evaluación completa del TB4.

Entregable 1  —  Dashboard en URL pública

Una aplicación web funcional, accesible desde cualquier navegador sin instalación ni credenciales.
No es un PDF, no es un notebook con celdas, no es una presentación de diapositivas; es una
aplicación que responde en tiempo real a los controles del usuario.

La URL se comparte con el docente a las 11:00 p.m. exactas. Un dashboard inaccesible en ese
momento descuenta automáticamente 14 puntos (bloques A, B y C de evaluación). El bloque D se
evalúa igualmente.

Entregable 2  —  Repositorio GitHub público

El repositorio debe permitir que cualquier persona reproduzca el dashboard ejecutando un solo
comando desde la terminal.

Estructura mínima obligatoria:
TB4-DataViz/
  README.md          ← primera línea: URL del dashboard en producción
  requirements.txt   ← dependencias con versión exacta
  app.py             ← archivo principal del dashboard
  paleta.md          ← validación de accesibilidad de color (ver Anexo
A)
  data/
    merge.py         ← script que descarga y une los dos datasets

Un repositorio privado descuenta 1 punto. Un repositorio sin requirements.txt o sin merge.py
descuenta 1 punto adicional.

TABLA DE CALIFICACIÓN

La nota se asigna en función de cuántas preguntas el dashboard responde de forma clara,
correcta e inmediata durante la hora de evaluación.

Bloque

Preguntas

A — Panorama global

1, 2, 3

B — Patrones y
comparaciones

4, 5, 6, 7

C — Posición de Perú

8, 9

D — Lectura crítica

10

TOTAL

Pts. por
pregunta

2 puntos

2 puntos

2 puntos

2 puntos

Total

6

8

4

2

20

Página 6 de 8

TRABAJO 4 — TB4  |  DATA VISUALIZATION

Criterio de calificación por pregunta

Puntaje

Condición

2 puntos

1 punto

0 puntos

El dashboard responde la pregunta con una visualización clara, el tipo de gráfico
es apropiado y el equipo lee el resultado sin dudar.

El dashboard muestra los datos relevantes, pero la visualización es confusa,
incompleta o requiere explicación adicional para entenderse.

El dashboard no puede responder la pregunta, la visualización es incorrecta o el
dato no aparece.

Penalizaciones automáticas

Infracción

Descuento

Gráfico de torta, donut o 3D en cualquier sección

−1 punto por instancia

Dashboard inaccesible a las 10:00 p.m.

Repositorio privado

Repositorio sin requirements.txt o sin merge.py

−14 puntos (bloques A, B
y C)

−1 punto

−1 punto

POLÍTICA DE USO DE INTELIGENCIA ARTIFICIAL

El uso de herramientas de IA (GitHub Copilot, ChatGPT, Claude u otras) para generar código está
permitido durante las 3 horas de construcción y no requiere declararse.

Lo que se evalúa en la hora de evaluación no es el código, sino el criterio: ¿por qué ese gráfico?,
¿por qué esa escala?, ¿por qué ese encoding?, ¿qué dice ese dato? Si durante la Pregunta 10 el
equipo no puede responder, se descuenta la totalidad de los 2 puntos del Bloque D.

Página 7 de 8

TRABAJO 4 — TB4  |  DATA VISUALIZATION

ANEXO A  —  Validación de Accesibilidad de Color

¿Por qué importa?

Aproximadamente el 8 % de los hombres tiene alguna forma de daltonismo. El tipo más frecuente,
la deuteranopia, impide distinguir el rojo del verde. Un dashboard que no puede ser leído por parte
de la audiencia no cumple el estándar de visualización de alto impacto. La validación de color no
es un requisito burocrático: es parte del diseño.

Paso 1  —  Elegir la paleta en Colorbrewer

Ingresar a colorbrewer2.org. Seleccionar el número de colores necesarios y el tipo de dato a
codificar:

–  Secuencial: datos con un solo sentido de variación, de menor a mayor. Ejemplo: consumo

energético donde el color va de amarillo claro a rojo oscuro.

–  Divergente: datos con un punto medio significativo y dos direcciones opuestas. Ejemplo:

países que mejoraron vs. empeoraron, con gris neutro en el centro.

–  Cualitativo: categorías sin jerarquía. Ejemplo: regiones del mundo donde cada una tiene un

color distinto sin implicar orden.

Activar el filtro "colorblind safe" en el panel lateral. Solo las paletas que pasen ese filtro son válidas
para el TB4. Copiar los códigos hexadecimales.

Paso 2  —  Simular daltonismo en Viz Palette

Ingresar a projects.susielu.com/viz-palette. Pegar los códigos hex elegidos. La herramienta
muestra cómo se ve la paleta para visión normal, deuteranopia, protanopia y tritanopia. Verificar
que todos los colores sean distinguibles entre sí en la simulación de deuteranopia. Si dos colores
se vuelven indistinguibles, reemplazar uno y repetir.

Paso 3  —  Archivo paleta.md en el repositorio

Crear un archivo paleta.md en la raíz del repositorio con el siguiente contenido:

# Paleta de color — TB4

Tipo: [Secuencial / Divergente / Cualitativo]
Fuente: ColorBrewer — [nombre de la paleta]
Validación: colorblind safe confirmado

Colores adoptados:
#hex1  →  [qué variable o categoría codifica]
#hex2  →  [qué variable o categoría codifica]

Simulación deuteranopia: [descripción del resultado]

Este archivo reemplaza cualquier documentación adicional sobre color. No requiere redacción
extensa: es documentación técnica concisa.

Página 8 de 8

