import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.predictionModels import *
from app.Services.SequenceProcessor import *
from database.db_mysql import *


class TestIntegrationWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todas las pruebas"""
        # Cargar variables de entorno
        load_dotenv()

        # Cargar los modelos una sola vez para todas las pruebas
        try:
            cls.models = load_models()
            cls.models_loaded = True
        except Exception as e:
            print(f"Error cargando modelos: {e}")
            cls.models_loaded = False

    def setUp(self):
        """Configuración para cada prueba individual"""
        self.test_sequences = {
            'antimicrobial': "GIGKFLHSAKKFGKAFVGEIMNS",  # Secuencia conocida antimicrobial
            'non_antimicrobial': "MNIFEMLRIDEGLRLKIYKDT",  # Secuencia conocida no antimicrobial
            'multiple': "GIGKFLHSAKKFGKAFVGEIMNS, MNIFEMLRIDEGLRLKIYKDT"  # Múltiples secuencias
        }
        self.test_ip = "127.0.0.1"

    def test_full_workflow_single_model(self):
        """Prueba el flujo completo usando solo el modelo SVM"""
        if not self.models_loaded:
            self.skipTest("Modelos no cargados correctamente")

        # 1. Procesar la secuencia
        sequence = self.test_sequences['antimicrobial']

        # 2. Realizar predicción
        predictions = make_prediction(self.models, sequence, ["SVM"])

        # Verificar estructura de la predicción
        self.assertIsNotNone(predictions)
        self.assertEqual(len(predictions), 1)
        self.assertIn("SVM_probability", predictions[0])
        self.assertIsNone(predictions[0].get("RandomForest_probability"))
        self.assertIsNone(predictions[0].get("NeuralNetwork_probability"))

        # 3. Guardar en base de datos
        with patch('database.db_mysql.connect_to_database') as mock_db:
            mock_connection = MagicMock()
            mock_cursor = MagicMock()
            mock_connection.cursor.return_value = mock_cursor
            mock_db.return_value = mock_connection

            save_query(sequence, predictions, self.test_ip)

            # Verificar que se guardó en la base de datos
            mock_cursor.execute.assert_called_once()
            mock_connection.commit.assert_called_once()

    def test_full_workflow_all_models(self):
        """Prueba el flujo completo usando todos los modelos"""
        if not self.models_loaded:
            self.skipTest("Modelos no cargados correctamente")

        sequence = self.test_sequences['antimicrobial']

        # Realizar predicción con todos los modelos
        predictions = make_prediction(self.models, sequence, ["SVM", "RF", "NN"])

        # Verificar que todas las predicciones están presentes
        self.assertIsNotNone(predictions)
        self.assertEqual(len(predictions), 1)
        prediction = predictions[0]

        # Verificar que todos los modelos generaron predicciones
        self.assertIn("SVM_probability", prediction)
        self.assertIn("RandomForest_probability", prediction)
        self.assertIn("NeuralNetwork_probability", prediction)
        self.assertIn("average_probability", prediction)

        # Verificar que las probabilidades están en el rango correcto
        for key in ["SVM_probability", "RandomForest_probability", "NeuralNetwork_probability"]:
            self.assertGreaterEqual(prediction[key], 0)
            self.assertLessEqual(prediction[key], 1)

    def test_multiple_sequences_workflow(self):
        """Prueba el flujo completo con múltiples secuencias"""
        if not self.models_loaded:
            self.skipTest("Modelos no cargados correctamente")

        sequences = self.test_sequences['multiple']

        # Realizar predicciones
        predictions = make_prediction(self.models, sequences, ["SVM", "RF", "NN"])

        # Verificar que se procesaron todas las secuencias
        self.assertEqual(len(predictions), 2)

        # Verificar cada predicción
        for prediction in predictions:
            self.assertIn("input_sequence", prediction)
            self.assertIn("average_probability", prediction)
            self.assertIn("final_prediction", prediction)

    def test_model_selection_workflow(self):
        """Prueba diferentes combinaciones de modelos"""
        if not self.models_loaded:
            self.skipTest("Modelos no cargados correctamente")

        sequence = self.test_sequences['antimicrobial']
        model_combinations = [
            ["SVM"],
            ["RF"],
            ["NN"],
            ["SVM", "RF"],
            ["SVM", "NN"],
            ["RF", "NN"],
            ["SVM", "RF", "NN"]
        ]

        for models_to_use in model_combinations:
            with self.subTest(models=models_to_use):
                predictions = make_prediction(self.models, sequence, models_to_use)

                prediction = predictions[0]
                # Verificar que solo están presentes las predicciones de los modelos seleccionados
                if "SVM" in models_to_use:
                    self.assertIsNotNone(prediction["SVM_probability"])
                else:
                    self.assertIsNone(prediction.get("SVM_probability"))

                if "RF" in models_to_use:
                    self.assertIsNotNone(prediction["RandomForest_probability"])
                else:
                    self.assertIsNone(prediction.get("RandomForest_probability"))

                if "NN" in models_to_use:
                    self.assertIsNotNone(prediction["NeuralNetwork_probability"])
                else:
                    self.assertIsNone(prediction.get("NeuralNetwork_probability"))

    def test_error_handling_workflow(self):
        """Prueba el manejo de errores en el flujo completo"""
        if not self.models_loaded:
            self.skipTest("Modelos no cargados correctamente")

        # Probar con una secuencia inválida
        invalid_sequence = "123ABCXYZ"

        predictions = make_prediction(self.models, invalid_sequence, ["SVM", "RF", "NN"])

        # Verificar que se manejó el error correctamente
        self.assertIsNotNone(predictions)
        self.assertEqual(len(predictions), 1)
        self.assertIn("error", predictions[0])

        # Probar el guardado con error
        with patch('database.db_mysql.connect_to_database') as mock_db:
            mock_db.return_value = None  # Simular error de conexión

            # Verificar que no hay excepciones no manejadas
            save_query(invalid_sequence, predictions, self.test_ip)


if __name__ == '__main__':
    unittest.main()