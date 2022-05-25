from typing import Any
import unittest

from __seedwork.domain.validators import ValidatorRules
from __seedwork.domain.exceptions import ValidationException


class TestValidatorRules(unittest.TestCase):

    def test_values_methods(self):
        validator = ValidatorRules.values('some value', 'attribute')

        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, 'some value')
        self.assertEqual(validator.attribute, 'attribute')

    def test_required_rule_with_invalid_values(self):

        invalid_data = [
            {'value': None, "attribute": "attribute"},
            {'value': "", "attribute": "attribute"}
        ]

        for data in invalid_data:
            message = f"value: {data['value']}, attribute: {data['attribute']}"
            with self.assertRaises(ValidationException, msg=message) as assert_error:
                ValidatorRules.values(
                    data['value'], data['attribute']).required()

            self.assertEqual('The "attribute" is required.',
                             assert_error.exception.args[0])

    def test_required_rule_with_valid_values(self):
        valid_data = [
            {'value': 'test', 'attribute': 'attribute'},
            {'value': 5, 'attribute': 'attribute'},
            {'value': 0, 'attribute': 'attribute'},
            {'value': False, 'attribute': 'attribute'}
        ]

        for data in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(
                    data['value'], data['attribute']).required(),
                ValidatorRules
            )

    def test_string_rule_with_invalid_values(self):

        invalid_data = [
            {'value': 5, 'attribute': 'attribute'},
            {'value': True, 'attribute': 'attribute'},
            {'value': {}, 'attribute': 'attribute'}
        ]

        for data in invalid_data:
            message = f"value: {data['value']}, attribute: {data['attribute']}"
            with self.assertRaises(ValidationException, msg=message) as assert_error:
                ValidatorRules.values(
                    data['value'], data['attribute']).string()

            self.assertEqual('The "attribute" must be a string.',
                             assert_error.exception.args[0])

    def test_string_rule_with_valid_values(self):
        valid_data = [
            {'value': None, 'attribute': 'attribute'},
            {'value': "", 'attribute': 'attribute'},
            {'value': 'some value', 'attribute': 'attribute'},
        ]

        for data in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(
                    data['value'], data['attribute']).string(),
                ValidatorRules
            )

    def test_max_length_rule_with_invalid_values(self):

        invalid_data = [
            {'value': "t"*5, 'attribute': 'attribute'},
        ]

        value_length = 4
        for data in invalid_data:
            message = f"value: {data['value']}, attribute: {data['attribute']}"
            with self.assertRaises(ValidationException, msg=message) as assert_error:
                ValidatorRules.values(
                    data['value'], data['attribute']).max_length(value_length)

            expected_message = f'The "attribute" must be less than {value_length} characters.'
            self.assertEqual(expected_message, assert_error.exception.args[0])

    def test_max_length_rule_with_valid_values(self):
        valid_data = [
            {'value': "t"*5, 'attribute': 'attribute'},
            {'value': None, 'attribute': 'attribute'},
        ]

        value_length = 5
        for data in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(
                    data['value'], data['attribute']).max_length(value_length),
                ValidatorRules
            )