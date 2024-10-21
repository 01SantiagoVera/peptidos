from flask import Blueprint, request, jsonify
from app.controllers.predictionController import predict_antimicrobial

api_bp = Blueprint('api', __name__)

@api_bp.route('/predict', methods=['POST'])
def predict():
    data = request.json.get('sequence')
    prediction = predict_antimicrobial(data)
    return jsonify(prediction=prediction)
