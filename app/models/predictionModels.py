import os
import pickle
import numpy as np
from propy import PyPro
import pandas as pd


def generate_descriptors(sequence):
    """
    Generate sequence descriptors using ProPy3.

    Args:
        sequence (str): Input protein/peptide sequence

    Returns:
        np.ndarray: Array of descriptors
    """
    try:
        # Crear objeto ProPy
        DesObject = PyPro.GetProDes(sequence)
        descriptors = []

        # Generar descriptores de la secuencia
        aac = DesObject.GetAAComp()  # Composición de aminoácidos
        descriptors.append(pd.Series(aac))

        dpc = DesObject.GetDPComp()  # Composición de dipéptidos
        descriptors.append(pd.Series(dpc))

        ctd = DesObject.GetCTD()  # Composición de características físico-químicas
        descriptors.append(pd.Series(ctd))

        paac = DesObject.GetPAAC(lamda=10, weight=0.05)  # Composición pseudo-aminoácida
        descriptors.append(pd.Series(paac))

        # Combinar todos los descriptores
        all_descriptors = pd.concat(descriptors)
        features = all_descriptors.values.astype(np.float32)

        # Asegurarse de que el número de características coincida con las del modelo
        if len(features) < 1477:
            padding = np.zeros(1477 - len(features))  # Rellenar con ceros si hay menos características
            features = np.concatenate([features, padding])
        elif len(features) > 1477:
            features = features[:1477]  # Recortar a 1477 características si es necesario

        return features

    except Exception as e:
        print(f"Error generating descriptors: {str(e)}")
        raise


def process_sequence(sequence):
    """Procesar la secuencia para generar el vector de características."""
    sequence = sequence.upper().strip()  # Normalizar la secuencia
    descriptors = generate_descriptors(sequence)
    return descriptors.reshape(1, -1)  # Redimensionar para usar en el modelo


def load_models():
    """Cargar los tres modelos desde archivos pickle."""
    base_path = os.path.dirname(__file__)

    # Rutas a los archivos de los modelos
    model_paths = {
        "SVM": os.path.join(base_path, 'model_SVM_ABPs.pkl'),
        "RF": os.path.join(base_path, 'model_RF_ABPs.pkl'),
        "NN": os.path.join(base_path, 'model_NN_AMPs.pkl')
    }

    # Verificar existencia de archivos
    for model_name, path in model_paths.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file {model_name} not found at: {path}")

    # Cargar los modelos desde los archivos pickle
    with open(model_paths["SVM"], 'rb') as file:
        model_SVM = pickle.load(file)
    with open(model_paths["RF"], 'rb') as file:
        model_RF = pickle.load(file)
    with open(model_paths["NN"], 'rb') as file:
        model_NN = pickle.load(file)

    return model_SVM, model_RF, model_NN


def make_prediction(models, sequence, selected_models):
    model_SVM, model_RF, model_NN = models
    encoded_sequence = process_sequence(sequence)

    probabilities = {}

    # Predicciones individuales
    if "SVM" in selected_models:
        probabilities["SVM_probability"] = round(model_SVM.predict_proba(encoded_sequence)[0][1], 2)
    else:
        probabilities["SVM_probability"] = None

    if "RF" in selected_models:
        probabilities["RandomForest_probability"] = round(model_RF.predict_proba(encoded_sequence)[0][1], 2)
    else:
        probabilities["RandomForest_probability"] = None

    if "NN" in selected_models:
        probabilities["NeuralNetwork_probability"] = round(model_NN.predict_proba(encoded_sequence)[0][1], 2)
    else:
        probabilities["NeuralNetwork_probability"] = None

    # Cálculo del promedio solo con valores válidos
    valid_probabilities = [
        value for value in probabilities.values() if value is not None
    ]
    avg_probability = round(sum(valid_probabilities) / len(valid_probabilities), 2) if valid_probabilities else None

    probabilities["average_probability"] = avg_probability
    probabilities["final_prediction"] = (
        "It's a peptide"
        if avg_probability is not None and avg_probability >= 0.5
        else "It is not a peptide"
    )

    return probabilities



