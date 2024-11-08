import os
import pickle

# Mapa de codificación básico de aminoácidos a números
amino_acid_map = {
    'A': 1, 'R': 2, 'N': 3, 'D': 4, 'C': 5,
    'Q': 6, 'E': 7, 'G': 8, 'H': 9, 'I': 10,
    'L': 11, 'K': 12, 'M': 13, 'F': 14, 'P': 15,
    'S': 16, 'T': 17, 'W': 18, 'Y': 19, 'V': 20
}


def encode_sequence(sequence, fixed_length=1477):
    # Convertir secuencia de aminoácidos en una lista de números
    encoded_sequence = [amino_acid_map.get(aa, 0) for aa in sequence]

    # Ajustar la longitud de la secuencia a 1477 características
    if len(encoded_sequence) < fixed_length:
        encoded_sequence.extend([0] * (fixed_length - len(encoded_sequence)))  # Rellenar con ceros
    else:
        encoded_sequence = encoded_sequence[:fixed_length]  # Truncar si es más larga

    return encoded_sequence


def load_models():
    # Ruta base para cargar los modelos
    base_path = os.path.dirname(__file__)  # Obtiene el directorio actual de este archivo

    # Rutas absolutas a los archivos .pkl
    model_paths = {
        "SVM": os.path.join(base_path, 'model_SVM_ABPs.pkl'),
        "RF": os.path.join(base_path, 'model_RF_ABPs.pkl'),
        "NN": os.path.join(base_path, 'model_NN_AMPs.pkl')
    }

    # Verificar existencia de archivos y cargar modelos
    for model_name, path in model_paths.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo {model_name} no se encuentra en la ruta: {path}")

    with open(model_paths["SVM"], 'rb') as file:
        model_SVM = pickle.load(file)
    with open(model_paths["RF"], 'rb') as file:
        model_RF = pickle.load(file)
    with open(model_paths["NN"], 'rb') as file:
        model_NN = pickle.load(file)

    return model_SVM, model_RF, model_NN



def make_prediction(models, sequence):
    model_SVM, model_RF, model_NN = models

    # Codificar la secuencia a una longitud fija de 1477 características
    encoded_sequence = encode_sequence(sequence)

    # Realizar predicciones directamente con cada modelo
    prediction_svm = model_SVM.predict([encoded_sequence])
    prediction_rf = model_RF.predict([encoded_sequence])
    prediction_nn = model_NN.predict([encoded_sequence])

    return {
        "SVM": prediction_svm[0],
        "RandomForest": prediction_rf[0],
        "NeuralNetwork": prediction_nn[0]
    }
