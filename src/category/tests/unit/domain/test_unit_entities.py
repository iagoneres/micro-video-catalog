from dataclasses import FrozenInstanceError, is_dataclass
from datetime import datetime
import unittest
from unittest.mock import patch

from category.domain.entities import Category


class TestCategoryUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor_with_mandatory_params(self):
        with patch.object(Category, 'validate') as mock_validate_method:
            data = {
                'name': 'Category',
            }

            category = Category(**data)
            mock_validate_method.assert_called_once()
            self.assertEqual(category.name, data['name'])
            self.assertEqual(category.description, None)
            self.assertEqual(category.is_active, True)
            self.assertIsInstance(category.created_at, datetime)

    def test_constructor(self):
        with patch.object(Category, 'validate'):
            data = {
                'name': 'Category',
                'description': 'some description',
                'is_active': False,
                'created_at': datetime.now()
            }
            category = Category(**data)

            self.assertEqual(category.name, data['name'])
            self.assertEqual(category.description, data['description'])
            self.assertEqual(category.is_active, data['is_active'])
            self.assertIsInstance(category.created_at, datetime)
            self.assertEqual(category.created_at, data['created_at'])

    def test_if_created_at_is_generated_in_constructor(self):
        with patch.object(Category, 'validate'):
            category_1 = Category(name='Category 1')
            category_2 = Category(name='Category 2')

            self.assertNotEqual(
                category_1.created_at.timestamp(),
                category_2.created_at.timestamp()
            )

    def test_is_immutable(self):
        with patch.object(Category, 'validate'):
            with self.assertRaises(FrozenInstanceError):
                value_object = Category(name="Teste")
                value_object.name = 'Fake Name'

    def test_update(self):
        with patch.object(Category, 'validate'):
            category = Category(name="Movie Category")
            category.update('Documentary', 'Some Description')

            self.assertEqual(category.name, 'Documentary')
            self.assertEqual(category.description, 'Some Description')

    def test_activate(self):
        with patch.object(Category, 'validate'):
            category = Category(name="Movie", is_active=False)
            category.activate()

            self.assertTrue(category.is_active)

    def test_deactivate(self):
        with patch.object(Category, 'validate'):
            category = Category(name="Movie", is_active=True)
            category.deactivate()

            self.assertFalse(category.is_active)
