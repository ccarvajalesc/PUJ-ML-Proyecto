import time
import joblib
import pandas as pd
import streamlit as st
from io import BytesIO

# ==========================================================
# Configuración página
# ==========================================================

st.set_page_config(
    page_title="Predicción ICFES",
    page_icon="🎓",
    layout="wide"
)

# ==========================================================
# Cargar modelo
# ==========================================================

@st.cache_resource
def load_artifacts():

    model = joblib.load(
        "artifacts/xgb_icfes_binario.joblib"
    )

    metadata = joblib.load(
        "artifacts/model_metadata.joblib"
    )

    return model, metadata


modelo, metadata = load_artifacts()

FEATURES = metadata["features"]
LABELS = metadata["labels"]
FEATURE_VALUES = metadata["feature_values"]

# ==========================================================
# Funciones
# ==========================================================
def generar_plantilla():

    ejemplo = {}

    for col in FEATURES:

        ejemplo[col] = FEATURE_VALUES[col][0]

    df = pd.DataFrame([ejemplo])

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False
        )

    return output.getvalue()

def predict_single(data):

    start = time.perf_counter()

    df = pd.DataFrame([data])

    pred = modelo.predict(df)[0]
    probs = modelo.predict_proba(df)[0]

    elapsed = (
        time.perf_counter() - start
    ) * 1000

    return {
        "prediction": int(pred),
        "prediction_label": LABELS[int(pred)],
        "probability_bajo": float(probs[0]),
        "probability_alto": float(probs[1]),
        "processing_time_ms": round(elapsed, 2)
    }


def predict_excel(df):

    preds = modelo.predict(df)

    df_result = df.copy()

    df_result["prediction"] = preds

    df_result["prediction_label"] = [
        LABELS[int(x)]
        for x in preds
    ]

    return df_result


# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("🎓 Predicción ICFES")

option = st.sidebar.radio(
    "Seleccione opción",
    [
        "Predicción Individual",
        "Predicción Masiva"
    ]
)

# ==========================================================
# Predicción individual
# ==========================================================

if option == "Predicción Individual":

    st.title(
        "Predicción Individual del Desempeño Académico"
    )

    inputs = {}

    col1, col2 = st.columns(2)

    feature_list = list(FEATURE_VALUES.keys())

    for i, feature in enumerate(feature_list):

        target_col = col1 if i % 2 == 0 else col2

        with target_col:

            inputs[feature] = st.selectbox(
                feature,
                FEATURE_VALUES[feature]
            )

    if st.button("Realizar Predicción"):

        result = predict_single(inputs)

        st.success(
            f"Predicción: {result['prediction_label']}"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Probabilidad Bajo",
            f"{result['probability_bajo']:.2%}"
        )

        c2.metric(
            "Probabilidad Alto",
            f"{result['probability_alto']:.2%}"
        )

        c3.metric(
            "Tiempo",
            f"{result['processing_time_ms']} ms"
        )

# ==========================================================
# Predicción masiva
# ==========================================================

else:

    st.title(
        "Predicción Masiva mediante Excel"
    )

    st.markdown(
        """
        El archivo debe contener exactamente las columnas
        utilizadas durante el entrenamiento.
        """
    )

    # ------------------------------------------------------
    # Descargar plantilla
    # ------------------------------------------------------

    st.subheader("Plantilla Excel")

    st.download_button(
        label="📥 Descargar plantilla",
        data=generar_plantilla(),
        file_name="plantilla_icfes.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # ------------------------------------------------------
    # Cargar archivo
    # ------------------------------------------------------

    uploaded_file = st.file_uploader(
        "Subir archivo Excel",
        type=["xlsx"]
    )

    if uploaded_file is not None:

        try:

            with st.spinner(
                "Leyendo archivo..."
            ):

                df = pd.read_excel(
                    uploaded_file
                )

            st.success(
                f"Archivo cargado correctamente "
                f"({len(df):,} registros)"
            )

            # --------------------------------------------------
            # Validar columnas
            # --------------------------------------------------

            missing = set(FEATURES) - set(df.columns)

            if missing:

                st.error(
                    "Faltan las siguientes columnas:"
                )

                st.write(
                    sorted(list(missing))
                )

                st.stop()

            # --------------------------------------------------
            # Reordenar columnas
            # --------------------------------------------------

            df = df[FEATURES]

            # --------------------------------------------------
            # Predicción
            # --------------------------------------------------

            with st.spinner(
                "Generando predicciones..."
            ):

                preds = modelo.predict(df)

            # --------------------------------------------------
            # Compatibilidad por si el modelo
            # devuelve one-hot
            # --------------------------------------------------

            import numpy as np

            preds = np.asarray(preds)

            if len(preds.shape) > 1:

                preds = preds.argmax(axis=1)

            # --------------------------------------------------
            # Construcción resultado
            # --------------------------------------------------

            result_df = df.copy()

            result_df["prediction"] = preds

            result_df["prediction_label"] = [
                LABELS[int(x)]
                for x in preds
            ]

            # --------------------------------------------------
            # Exportar Excel
            # --------------------------------------------------

            output = BytesIO()

            with pd.ExcelWriter(
                output,
                engine="openpyxl"
            ) as writer:

                result_df.to_excel(
                    writer,
                    index=False
                )

            st.success(
                "Predicciones generadas correctamente."
            )

            st.download_button(
                label="📥 Descargar Excel con predicciones",
                data=output.getvalue(),
                file_name="predicciones_icfes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:

            st.error(
                f"Error procesando archivo: {str(e)}"
            )

            import traceback

            st.code(
                traceback.format_exc()
            )