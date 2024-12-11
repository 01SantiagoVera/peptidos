from flask import Blueprint, request, jsonify
from app.Services.SequenceProcessor import process_sequence, load_models
from database.db_mysql import save_query
from app.models.predictionModels import make_prediction
import numpy as np

api_bp = Blueprint('api', __name__)

@api_bp.route('/predict', methods=['POST'])
def predict():
    try:
        # Verificar si la solicitud contiene un archivo
        if 'file' in request.files and request.files['file']:
            uploaded_file = request.files['file']

            # Procesar el archivo para obtener las secuencias
            sequences = []
            for line in uploaded_file:
                line = line.decode("utf-8").strip()
                if line:  # Ignorar líneas vacías
                    sequences.append(line)
            if not sequences:
                return jsonify(error="El archivo está vacío o no contiene secuencias válidas."), 400
        else:
            # Obtener la secuencia desde el cuerpo de la solicitud (formulario o JSON)
            sequence = request.form.get('sequence', '').strip()
            if not sequence:
                return jsonify(error="No se proporcionó una secuencia ni un archivo válido."), 400
            sequences = [sequence]

        # Obtener los modelos seleccionados
        selected_models = request.form.getlist('model')
        if not selected_models:
            selected_models = ['SVM', 'RF', 'NN']  # Usar modelos por defecto

        # Cargar los modelos
        models = load_models()

        # Realizar las predicciones para todas las secuencias
        predictions = []
        for seq in sequences:
            # Usar la función de predicción
            prediction = make_prediction(models, seq, selected_models)
            predictions.append(prediction)

            # Guardar en la base de datos
            user_ip = request.remote_addr
            save_query(seq, prediction, user_ip)
        return jsonify(predictions=predictions)

    except FileNotFoundError as e:
        print("Archivo no encontrado:", e)
        return jsonify(error="Modelo no encontrado."), 500
    except Exception as e:
        print("Error en el procesamiento de la predicción:", e)
        return jsonify(error=str(e)), 500

