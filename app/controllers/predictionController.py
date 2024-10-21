# app/controllers/prediction_controller.py

from ..models.predictionModels import load_models, make_prediction

def predict_antimicrobial(sequence):
    models = load_models()  # Llamar a la función que carga los modelos
    prediction = make_prediction(models, sequence)  # Realizar la predicción
    return prediction
