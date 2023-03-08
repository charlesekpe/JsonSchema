import unittest
import os
import json
from main import SchemaGenerator

class TestSchemaGenerator(unittest.TestCase):

    def setUp(self):
        # Create an instance of SchemaGenerator for testing
        self.schema_generator = SchemaGenerator()
        self.maxDiff = None
        
        # Create sample input data for testing
        self.sample_data = {
            "message": {
                "id": 1,
                "name": "John Doe",
                "age": 30,
                "is_employee": True,
                "hobbies": ["reading", "traveling"],
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                    "state": "CA",
                    "zip": 12345
                }
            }
        }

    def test_convert(self):
        # Test if the conversion method returns the correct data types for different inputs
        self.assertEqual(self.schema_generator.convert("test"), "STRING")
        self.assertEqual(self.schema_generator.convert(123), "INTEGER")
        self.assertEqual(self.schema_generator.convert(True), "BOOLEAN")
        self.assertEqual(self.schema_generator.convert([{"key": "value"}]), "ARRAY")
        self.assertEqual(self.schema_generator.convert(["value1", "value2"]), "ENUM")
        self.assertIsNone(self.schema_generator.convert(None))

    def test_get_schema(self):
        # Test if the schema generator returns the correct schema for a given input data
        expected_schema = {
            "id": {"type": "INTEGER", "tag": "", "description": "", "required": False},
            "name": {"type": "STRING", "tag": "", "description": "", "required": False},
            "age": {"type": "INTEGER", "tag": "", "description": "", "required": False},
            "is_employee": {"type": "BOOLEAN", "tag": "", "description": "", "required": False},
            "hobbies": {"type": "ENUM", "tag": "", "description": "", "required": False},
            "address": {'street': {'type': 'STRING', 'tag': '', 'description': '', 'required': False},
                'city': {'type': 'STRING', 'tag': '', 'description': '', 'required': False},
                'state': {'type': 'STRING', 'tag': '', 'description': '', 'required': False},
                'zip': {'type': 'INTEGER', 'tag': '', 'description': '', 'required': False}}
        }
        self.assertDictEqual(self.schema_generator.get_schema(self.sample_data["message"]), expected_schema)

    def test_generate(self):
        # Test if the schema generator generates and saves the schema file correctly
        # Set dump to True to save the schema file
        self.schema_generator.generate(self.sample_data, path="./schema/test_schema.json", dump=True)

        # Check if the schema file exists and has the correct schema
        self.assertTrue(os.path.exists("./schema/test_schema.json"))
        with open("./schema/test_schema.json", "r") as f:
            schema = json.load(f)
            self.assertDictEqual(schema, self.schema_generator.get_schema(self.sample_data["message"]))

    def tearDown(self):
        # Remove the schema file after testing
        if os.path.exists("./schema/test_schema.json"):
            os.remove("./schema/test_schema.json")

if __name__ == "__main__":
    unittest.main()
