# PUJ-ML-Proyecto

Proyecto desarrollado para la asignatura **Machine Learning** de la **Pontificia Universidad Javeriana**, enfocado en la predicción del desempeño académico de estudiantes colombianos en las pruebas **Saber 11** a partir de variables sociodemográficas.

## Integrantes del grupo

* Carlos Manuel Carvajales Castrillo
* Mateo Ruiz Mendoza

---

## Descripción del proyecto

El objetivo de este proyecto consiste en construir y evaluar modelos de aprendizaje automático capaces de predecir el nivel de desempeño académico de los estudiantes utilizando únicamente variables sociodemográficas disponibles en los conjuntos de datos del ICFES.

Durante el desarrollo se realizó:

* Análisis exploratorio de datos (EDA).
* Preprocesamiento y limpieza de información.
* Tratamiento de valores faltantes mediante eliminación e imputación.
* Construcción y evaluación de diferentes modelos de clasificación.
* Comparación de desempeño mediante métricas de clasificación.
* Selección y despliegue del mejor modelo obtenido.

Los modelos evaluados fueron:

* Regresión Logística
* Random Forest
* Redes Neuronales Artificiales
* XGBoost

Tras la comparación experimental de los distintos enfoques evaluados, el modelo seleccionado para despliegue fue **XGBoost para clasificación binaria (Bajo / Alto)**, al obtener el mejor desempeño global en las métricas de evaluación consideradas.

---

## Estructura del proyecto

```text
PUJ-ML-Proyecto/
│
├── artifacts/
│   ├── model_metadata.joblib
│   └── xgb_icfes_binario.joblib
│
├── excel_files/
│   ├── output_multiple.xlsx
│   ├── output_multiple_predicciones.xlsx
│   └── plantilla_datos.xlsx
│
├── Notebooks/
│   ├── images/
│   ├── EDA_Introduccion_a_proyecto.ipynb
│   ├── preprocesamiento.ipynb
│   ├── random_forest.ipynb
│   ├── regresion_logistica.ipynb
│   ├── RN.ipynb
│   ├── saber11_20221_20224.parquet
│   └── xgboost.ipynb
│
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
```

---

## Descripción de carpetas y archivos

### `Notebooks/`

Contiene todo el desarrollo experimental del proyecto:

* **EDA_Introduccion_a_proyecto.ipynb**

  * Introducción general.
  * Motivación.
  * Objetivos.
  * Análisis exploratorio de datos.

* **preprocesamiento.ipynb**

  * Limpieza de datos.
  * Construcción de variables objetivo.
  * Selección de características.
  * Tratamiento de valores faltantes.

* **regresion_logistica.ipynb**

  * Entrenamiento y evaluación del modelo de Regresión Logística.

* **random_forest.ipynb**

  * Entrenamiento y evaluación del modelo Random Forest.

* **RN.ipynb**

  * Entrenamiento y evaluación de Redes Neuronales Artificiales.

* **xgboost.ipynb**

  * Entrenamiento y evaluación del modelo XGBoost.
  * Generación de los artefactos utilizados posteriormente en producción.

---

### `artifacts/`

Contiene los artefactos necesarios para realizar inferencias:

* **xgb_icfes_binario.joblib**

  * Modelo XGBoost entrenado.

* **model_metadata.joblib**

  * Metadatos del modelo:

    * Variables de entrada.
    * Etiquetas de salida.
    * Valores válidos para cada característica.

---

### `excel_files/`

Archivos de ejemplo para probar la aplicación:

* **plantilla_datos.xlsx**

  * Plantilla de entrada para predicciones masivas.

* **output_multiple.xlsx**

  * Ejemplo de archivo válido para realizar inferencias.

* **output_multiple_predicciones.xlsx**

  * Ejemplo de salida generada por la aplicación.

---

## Aplicación Streamlit

El proyecto incluye una aplicación desarrollada en **Streamlit** para realizar predicciones de dos maneras:

### Predicción individual

Permite seleccionar manualmente los valores de cada variable y obtener:

* Predicción del modelo.
* Etiqueta asociada.
* Probabilidad para cada clase.
* Tiempo de procesamiento.

### Predicción masiva

Permite:

1. Descargar una plantilla Excel.
2. Cargar múltiples registros simultáneamente.
3. Generar predicciones para todos los registros.
4. Descargar un nuevo archivo Excel con los resultados.

---

## Requisitos

### Python

Se recomienda utilizar:

```text
Python 3.11+
```

### Dependencias principales

```text
streamlit==1.49.1
numpy==2.3.2
pandas==2.3.2
scikit-learn==1.7.2
xgboost==3.1.0
joblib==1.5.2
openpyxl==3.1.5
```

Instalación:

```bash
pip install -r requirements.txt
```

---

## Ejecución local

Desde la raíz del proyecto:

```bash
streamlit run main.py
```

La aplicación quedará disponible por defecto en:

```text
http://localhost:8501
```

---

## Instalación de Docker

Para ejecutar la aplicación mediante contenedores es necesario tener Docker instalado en el sistema.

### Windows

1. Descargar Docker Desktop desde:

```text
https://www.docker.com/products/docker-desktop/
```

2. Ejecutar el instalador y seguir los pasos del asistente.

3. Reiniciar el equipo si es solicitado.

4. Verificar la instalación:

```bash
docker --version
docker compose version
```

### Linux (Ubuntu)

Actualizar repositorios:

```bash
sudo apt update
```

Instalar dependencias:

```bash
sudo apt install -y ca-certificates curl gnupg
```

Agregar la llave oficial de Docker:

```bash
sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
| sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

Agregar el repositorio:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Instalar Docker:

```bash
sudo apt update

sudo apt install -y \
docker-ce \
docker-ce-cli \
containerd.io \
docker-buildx-plugin \
docker-compose-plugin
```

Verificar instalación:

```bash
docker --version
docker compose version
```

(Opcional) Ejecutar Docker sin sudo:

```bash
sudo usermod -aG docker $USER
```

Cerrar sesión y volver a ingresar para aplicar los cambios.

### Verificación

Ejecutar:

```bash
docker run hello-world
```

Si aparece el mensaje de bienvenida, Docker se encuentra correctamente instalado.

---

## Ejecución mediante Docker

### Construir imagen

```bash
docker build -t puj-ml-proyecto .
```

### Ejecutar contenedor

```bash
docker run -p 8501:8501 puj-ml-proyecto
```

La aplicación estará disponible en:

```text
http://localhost:8501
```

---

## Ejecución mediante Docker Compose

Construcción y despliegue:

```bash
docker compose up --build
```

Ejecución posterior:

```bash
docker compose up
```

Detener contenedores:

```bash
docker compose down
```

---

## Consideraciones de uso

* Los archivos Excel cargados deben contener exactamente las columnas utilizadas durante el entrenamiento.
* Se recomienda utilizar la plantilla descargable desde la aplicación para evitar errores de formato.
* El modelo fue entrenado para clasificación binaria de desempeño académico:

  * **Bajo**
  * **Alto**

* Los valores categóricos no observados durante el entrenamiento son manejados automáticamente por el pipeline de preprocesamiento.

---

## Distribución de responsabilidades

Las actividades desarrolladas durante el proyecto fueron distribuidas de la siguiente manera:

| Actividad | Responsable |
|------------|------------|
| Experimentación con Redes Neuronales (RN) | Mateo Ruiz Mendoza |
| Experimentación con Regresión Logística (RL) | Mateo Ruiz Mendoza |
| Experimentación con XGBoost | Carlos Manuel Carvajales Castrillo |
| Experimentación con Random Forest | Carlos Manuel Carvajales Castrillo |
| Elaboración del informe final | Mateo Ruiz Mendoza y Carlos Manuel Carvajales Castrillo |
| Desarrollo de la aplicación Front-End (Streamlit) | Mateo Ruiz Mendoza y Carlos Manuel Carvajales Castrillo |
| Presentación final del proyecto | Mateo Ruiz Mendoza y Carlos Manuel Carvajales Castrillo |
| Video de sustentación | Mateo Ruiz Mendoza y Carlos Manuel Carvajales Castrillo |

---

## Observaciones

Este repositorio tiene fines académicos y fue desarrollado como parte de las actividades de la asignatura de Machine Learning. Los resultados obtenidos no deben interpretarse como herramientas oficiales de evaluación educativa, sino como una aplicación práctica de técnicas de ciencia de datos y aprendizaje automático sobre datos reales del contexto educativo colombiano.