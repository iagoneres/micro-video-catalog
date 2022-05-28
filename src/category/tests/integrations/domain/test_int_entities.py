import unittest

from category.domain.entities import Category
from __seedwork.domain.exceptions import ValidationException


class TestCategoryIntegration(unittest.TestCase):

    def test_create_with_invalid_cases_for_name_attribute(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name=None)

        self.assertEqual(
            assert_error.exception.args[0], 'The "name" is required.')

        with self.assertRaises(ValidationException) as assert_error:
            Category(name='')

        self.assertEqual(
            assert_error.exception.args[0], 'The "name" is required.')

        with self.assertRaises(ValidationException) as assert_error:
            Category(name=5)

        self.assertEqual(
            assert_error.exception.args[0], 'The "name" must be a string.')

        with self.assertRaises(ValidationException) as assert_error:
            Category(name='a'*256)

        self.assertEqual(
            assert_error.exception.args[0], 'The "name" must be less than 255 characters.')

    def test_create_with_invalid_cases_for_description_attribute(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name='Category', description=5)

        self.assertEqual(
            assert_error.exception.args[0], 'The "description" must be a string.')

    def test_create_with_invalid_cases_for_is_active_attribute(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name='Category', is_active=5)

        self.assertEqual(
            assert_error.exception.args[0], 'The "is_active" must be a boolean.')

    def test_create_with_valid_cases(self):
        try:
            Category(name='Category')
            Category(name='Category', description=None)
            Category(name='Category', description='')
            Category(name='Category', is_active=True)
            Category(name='Category', is_active=False)
            Category(name='Category',
                     description='some description', is_active=False)
        except ValidationException as exception:
            self.fail(
                f'Some attribute is not valid. Error: {exception.args[0]}')

    def test_update_with_invalid_cases_for_name_attribute(self):
        category = Category(name='Category')

        with self.assertRaises(ValidationException) as assert_error:
            category.update(None, None)

        self.assertEqual(
            assert_error.exception.args[0], 'The "name" is required.')

        with self.assertRaises(ValidationException) as assert_error:
            category.update('', None)

        self.assertEqual(
            assert_error.exception.args[0], 'The "name" is required.')

        with self.assertRaises(ValidationException) as assert_error:
            category.update(5, None)

        self.assertEqual(
            assert_error.exception.args[0], 'The "name" must be a string.')

        with self.assertRaises(ValidationException) as assert_error:
            category.update('a'*256, None)

        self.assertEqual(
            assert_error.exception.args[0], 'The "name" must be less than 255 characters.')

    def test_update_with_valid_cases(self):
        category = Category(name='Category')
        try:
            category.update('Category', 'some description')
            category.update('Category', None)
            category.update('Category', '')
        except ValidationException as exception:
            self.fail(
                f'Some attribute is not valid. Error: {exception.args[0]}')
