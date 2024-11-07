from flask import Blueprint, request, jsonify
from app.controllers.predictionController import predict_antimicrobial
from database.db_mysql import save_query
import datetime
api_bp = Blueprint('api', __name__)

@api_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        sequence = data.get('sequence')
        user_ip = request.remote_addr  # Captura la IP del usuario

        prediction = predict_antimicrobial(sequence)

        # Guardar la consulta, respuesta y la IP en la base de datos
        save_query(sequence, prediction, user_ip)

        return jsonify(prediction=prediction)
    except FileNotFoundError as e:
        print("Archivo no encontrado:", e)
        return jsonify(error="Modelo no encontrado."), 500
    except Exception as e:
        print("Error en el procesamiento de la predicción:", e)  # Esto ayudará a ver el error en la consola
        return jsonify(error=str(e)), 500  # Devuelve el error en el formato JSON