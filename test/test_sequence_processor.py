import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.predictionModels import *
from app.Services.SequenceProcessor import *

class TestSequenceProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Carga los modelos una vez al inicio de todas las pruebas
        para evitar cargarlos en cada test
        """
        cls.models = load_models()

    def test_valid_sequence(self):
        """Prueba el procesamiento de una secuencia válida"""
        sequence = "SDQAKILWKLQFCRL"
        result = make_prediction(self.models, sequence, ["SVM", "RF", "NN"])
        self.assertIsNotNone(result)
        self.assertEqual(result[0]["input_sequence"], "SDQAKILWKLQFCRL")
        self.assertIsNotNone(result[0]["average_probability"])
        # Verificamos que las probabilidades estén en el rango correcto
        self.assertTrue(0 <= result[0]["average_probability"] <= 1)

    def test_multiple_sequences(self):
        """Prueba el procesamiento de múltiples secuencias separadas por comas"""
        sequences = "KLMPRV, ACDEKL"
        result = make_prediction(self.models, sequences, ["SVM"])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["input_sequence"], "KLMPRV")
        self.assertEqual(result[1]["input_sequence"], "ACDEKL")

    def test_invalid_characters(self):
        """Prueba el manejo de secuencias con caracteres inválidos"""
        sequence = "KLM123PVR"
        result = make_prediction(self.models, sequence, ["SVM"])
        self.assertTrue("error" in result[0])

    def test_empty_sequence(self):
        """Prueba el manejo de secuencias vacías"""
        sequence = ""
        result = make_prediction(self.models, sequence, ["SVM"])
        self.assertIsNone(result)

    def test_whitespace_handling(self):
        """Prueba el manejo de espacios en blanco"""
        sequence = "  KLMPVR  "
        result = make_prediction(self.models, sequence, ["SVM"])
        self.assertEqual(result[0]["input_sequence"], "KLMPVR")

    def test_selected_models(self):
        """Prueba la selección de modelos específicos"""
        sequence = "SDQAKILWKLQFCRL"
        # Probamos solo con SVM
        result = make_prediction(self.models, sequence, ["SVM"])
        self.assertIsNotNone(result[0]["SVM_probability"])
        self.assertIsNone(result[0]["RandomForest_probability"])
        self.assertIsNone(result[0]["NeuralNetwork_probability"])

        # Probamos solo con RF
        result = make_prediction(self.models, sequence, ["RF"])
        self.assertIsNone(result[0]["SVM_probability"])
        self.assertIsNotNone(result[0]["RandomForest_probability"])
        self.assertIsNone(result[0]["NeuralNetwork_probability"])

    def test_all_models_prediction(self):
        """Prueba predicción con todos los modelos"""
        sequence = "SDQAKILWKLQFCRL"
        result = make_prediction(self.models, sequence, ["SVM", "RF", "NN"])
        self.assertIsNotNone(result[0]["SVM_probability"])
        self.assertIsNotNone(result[0]["RandomForest_probability"])
        self.assertIsNotNone(result[0]["NeuralNetwork_probability"])
        self.assertIsNotNone(result[0]["average_probability"])

    def test_known_antimicrobial_sequence(self):
        """Prueba con una secuencia conocida antimicrobial"""
        # Aquí puedes usar una secuencia que sepas que es antimicrobial
        sequence = "GIGKFLHSAKKFGKAFVGEIMNS"  # Ejemplo de secuencia antimicrobial
        result = make_prediction(self.models, sequence, ["SVM", "RF", "NN"])
        self.assertGreaterEqual(result[0]["average_probability"], 0.5)
        self.assertEqual(result[0]["final_prediction"], "It's an Antimicrobial peptide")

    def test_known_non_antimicrobial_sequence(self):
        """Prueba con una secuencia conocida no antimicrobial"""
        # Aquí puedes usar una secuencia que sepas que no es antimicrobial
        sequence = "MRLDILKKKTGSIDRF"
        result = make_prediction(self.models, sequence, ["SVM", "RF", "NN"])
        self.assertLess(result[0]["average_probability"], 0.5)
        self.assertEqual(result[0]["final_prediction"], "It is not an Antimicrobial peptide")


if __name__ == '__main__':
    unittest.main()