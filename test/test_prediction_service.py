import unittest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch, mock_open
from app.Services.SequenceProcessor import *


class TestPredictionService(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.valid_sequence = "SDQAKILWKLQFCRL"
        self.long_sequence = "KLMVPRKLMVPRKLMVPR"
        self.invalid_sequence = "KLM123VPR"

    def test_generate_descriptors(self):
        """Prueba la generación de descriptores para una secuencia válida"""
        descriptors = generate_descriptors(self.valid_sequence)

        # Verificar que los descriptores tienen la dimensión correcta
        self.assertEqual(len(descriptors), 1477)

        # Verificar que los descriptores son números flotantes
        self.assertTrue(np.issubdtype(descriptors.dtype, np.floating))

        # Verificar que no hay valores NaN
        self.assertFalse(np.isnan(descriptors).any())

    def test_process_sequence(self):
        """Prueba el procesamiento completo de una secuencia"""
        processed = process_sequence(self.valid_sequence)

        # Verificar la forma del array resultante
        self.assertEqual(processed.shape, (1, 1477))

        # Verificar que la secuencia se normaliza correctamente
        with patch('app.Services.SequenceProcessor.generate_descriptors') as mock_gen:
            process_sequence("  klmvpr  ")
            mock_gen.assert_called_with("KLMVPR")

    def test_generate_descriptors_padding(self):
        """Prueba el padding de descriptores cuando hay menos de 1477 características"""
        # Crear un mock que devuelva menos características
        with patch('propy.PyPro.GetProDes') as mock_pypro:
            class MockDesObject:
                def GetAAComp(self): return {'A': 0.1, 'C': 0.2}

                def GetDPComp(self): return {'AA': 0.1}

                def GetCTD(self): return {'CTD1': 0.1}

                def GetPAAC(self, lamda, weight): return {'PAAC1': 0.1}

            mock_pypro.return_value = MockDesObject()

            descriptors = generate_descriptors(self.valid_sequence)
            self.assertEqual(len(descriptors), 1477)

    def test_generate_descriptors_truncation(self):
        """Prueba la truncación de descriptores cuando hay más de 1477 características"""
        descriptors = generate_descriptors(self.long_sequence)
        self.assertEqual(len(descriptors), 1477)

    def test_invalid_sequence(self):
        """Prueba el manejo de secuencias inválidas"""
        with self.assertRaises(Exception):
            generate_descriptors(self.invalid_sequence)

    def test_load_models(self):
        """Prueba la carga de modelos"""
        # Mock para simular la existencia de archivos
        with patch('os.path.exists') as mock_exists, \
                patch('builtins.open', mock_open()), \
                patch('pickle.load') as mock_load:
            mock_exists.return_value = True
            mock_load.return_value = "mock_model"

            models = load_models()

            # Verificar que se devuelven tres modelos
            self.assertEqual(len(models), 3)

            # Verificar que se intentó cargar cada modelo
            self.assertEqual(mock_load.call_count, 3)

    def test_model_not_found(self):
        """Prueba el manejo de archivos de modelo faltantes"""
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False

            with self.assertRaises(FileNotFoundError):
                load_models()

    def test_sequence_normalization(self):
        """Prueba la normalización de secuencias"""
        test_cases = [
            ("  KLMVPR  ", "KLMVPR"),  # Espacios en blanco
            ("klmvpr", "KLMVPR"),  # Minúsculas
            (" KlMvPr ", "KLMVPR")  # Combinación
        ]

        for input_seq, expected in test_cases:
            with patch('app.Services.SequenceProcessor.generate_descriptors') as mock_gen:
                process_sequence(input_seq)
                mock_gen.assert_called_with(expected)


if __name__ == '__main__':
    unittest.main()