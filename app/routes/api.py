from flask import Blueprint, request, jsonify
from database.db_mysql import save_query
from app.models.predictionModels import *
api_bp = Blueprint('api', __name__)
@api_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        sequence = data.get('sequence')
        selected_models = data.get('models', ['SVM', 'RF', 'NN'])  # Modelos por defecto

        # Validar que haya al menos un modelo seleccionado
        if not selected_models:
            return jsonify(error="No se seleccionaron modelos para la predicción."), 400

        models = load_models()
        prediction = make_prediction(models, sequence, selected_models)

        # Guardar la consulta, respuesta y la IP en la base de datos
        user_ip = request.remote_addr
        save_query(sequence, prediction, user_ip)

        return jsonify(prediction=prediction)
    except FileNotFoundError as e:
        print("Archivo no encontrado:", e)
        return jsonify(error="Modelo no encontrado."), 500
    except Exception as e:
        print("Error en el procesamiento de la predicción:", e)
        return jsonify(error=str(e)), 500
