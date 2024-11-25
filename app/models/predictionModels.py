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


def make_prediction(models, sequence):
    """
    Realizar predicciones usando probabilidades de los modelos.

    Args:
        models (tuple): (model_SVM, model_RF, model_NN)
        sequence (str): Secuencia peptídica de entrada

    Returns:
        dict: Diccionario con las probabilidades y la predicción final
    """
    model_SVM, model_RF, model_NN = models

    try:
        # Procesar la secuencia
        encoded_sequence = process_sequence(sequence)

        # Obtener las probabilidades de la clase positiva (índice 1)
        prob_svm = model_SVM.predict_proba(encoded_sequence)[0][1]
        prob_rf = model_RF.predict_proba(encoded_sequence)[0][1]
        prob_nn = model_NN.predict_proba(encoded_sequence)[0][1]

        # Calcular la probabilidad promedio
        avg_probability = (prob_svm + prob_rf + prob_nn) / 3

        # Definir umbral para la predicción final (puede ajustarse)
        threshold = 0.5

        # Realizar la predicción final según la probabilidad promedio
        final_prediction = "Es un péptido antimicrobiano" if avg_probability >= threshold else "No es un péptido antimicrobiano"

        # Devolver los resultados detallados
        results = {
            "SVM_probability": round(prob_svm, 4),
            "RandomForest_probability": round(prob_rf, 4),
            "NeuralNetwork_probability": round(prob_nn, 4),
            "average_probability": round(avg_probability, 4),
            "final_prediction": final_prediction
        }

        return results

    except Exception as e:
        print(f"Error in prediction pipeline: {str(e)}")
        raise


def print_prediction_results(sequence, results):
    """
    Imprimir los resultados de la predicción de manera formateada.

    Args:
        sequence (str): Secuencia de entrada
        results (dict): Resultados de la predicción
    """
    print("\nPrediction Results")
    print("-" * 50)
    print(f"Sequence: {sequence}")
    print(f"SVM Probability: {results['SVM_probability']:.4f}")
    print(f"Random Forest Probability: {results['RandomForest_probability']:.4f}")
    print(f"Neural Network Probability: {results['NeuralNetwork_probability']:.4f}")
    print(f"Average Probability: {results['average_probability']:.4f}")
    print(f"Final Prediction: {results['final_prediction']}")
    print("-" * 50)
