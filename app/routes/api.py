from flask import Blueprint, request, jsonify
from app.controllers.predictionController import predict_antimicrobial
from database.db_mysql import save_query
import json  # Importa json para convertir el diccionario a una cadena
api_bp = Blueprint('api', __name__)

@api_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        sequence = data.get('sequence')
        user_ip = request.remote_addr  # Captura la IP del usuario

        # Realizar la predicción
        prediction = predict_antimicrobial(sequence)

        # Guardar la consulta, respuesta y la IP en la base de datos
        save_query(sequence, json.dumps(prediction), user_ip)

        # Devolver la predicción en formato JSON
        return jsonify(prediction=prediction)

    except FileNotFoundError as e:
        print("Archivo no encontrado:", e)
        return jsonify(error="Modelo no encontrado."), 500
    except Exception as e:
        print("Error en el procesamiento de la predicción:", e)
        return jsonify(error="Error en el procesamiento de la predicción."), 500
