from flask import Blueprint, request, jsonify
from app.controllers.predictionController import predict_antimicrobial

api_bp = Blueprint('api', __name__)

@api_bp.route('/predict', methods=['POST'])
def predict():
    data = request.json
    sequence = data.get('sequence')
    user_ip = request.remote_addr  # Captura la IP del usuario

    prediction = predict_antimicrobial(sequence)

    # Guardar la consulta, respuesta y la IP en la base de datos
    save_query(sequence, prediction, user_ip)

    return jsonify(prediction=prediction)
