import os
import pickle
import numpy as np
from propy import PyPro
import pandas as pd

def generate_descriptors(sequence):
    try:
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
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')

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