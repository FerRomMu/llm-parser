import unittest
import json
from src.llm_parser import LlmParser

class TestLlmParser(unittest.TestCase):

    def setUp(self):
        # Se crea una instancia de LlmParser con el formato por defecto (JSON)
        self.parser = LlmParser()

    def test_default_format(self):
        # Test para verificar que el formato por defecto es 'JSON'
        self.assertEqual(self.parser.format, 'JSON')

    def test_invalid_format(self):
        # Test para verificar que lanza un error si se pasa un formato no implementado
        with self.assertRaises(NotImplementedError) as context:
            LlmParser(format="XML")
        self.assertEqual(str(context.exception), 'Format type "XML" not implemented yet.')

    def test_valid_json(self):
        # Test para verificar que se devuelve un json válido con estado 'VALID'
        llm_response = '{"key": "value"}'
        result = self.parser.parse(llm_response)
        self.assertEqual(result['state'], 'VALID')
        self.assertEqual(result['json'], json.loads(llm_response))

    def test_extra_text(self):
        # Test para verificar el estado 'ERROR_EXTRA_TEXT' cuando hay texto adicional fuera del JSON
        llm_response = 'Some extra text before json {"key": "value"}'
        result = self.parser.parse(llm_response)
        self.assertEqual(result['state'], 'ERROR_EXTRA_TEXT')
        self.assertEqual(result['json'], json.loads('{"key": "value"}'))

    def test_invalid_json(self):
        # Test para verificar el estado 'ERROR_INVALID_JSON' cuando el JSON es inválido
        llm_response = '{"key": "value"'  # Falta el cierre del JSON
        result = self.parser.parse(llm_response)
        self.assertEqual(result['state'], 'ERROR_INVALID_JSON')
        self.assertEqual(result['json'], {})

    def test_parse_with_missing_keys(self):
        # Test para verificar el estado 'MISSING_KEYS' cuando faltan claves en el JSON
        llm_response = '{"key1": "value1"}'
        expected_keys = ['key1', 'key2']
        result = self.parser.parse_with_keys(llm_response, expected_keys)
        self.assertEqual(result['state'], 'MISSING_KEYS')
        self.assertEqual(result['json'], json.loads(llm_response))

    def test_parse_with_all_keys_present(self):
        # Test para verificar que se devuelve un JSON válido cuando todas las claves están presentes
        llm_response = '{"key1": "value1", "key2": "value2"}'
        expected_keys = ['key1', 'key2']
        result = self.parser.parse_with_keys(llm_response, expected_keys)
        self.assertEqual(result['state'], 'VALID')
        self.assertEqual(result['json'], json.loads(llm_response))

if __name__ == '__main__':
    unittest.main()