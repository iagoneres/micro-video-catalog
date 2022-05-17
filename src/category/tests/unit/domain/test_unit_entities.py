from dataclasses import is_dataclass
from datetime import datetime
import unittest

from category.domain.entities import Category

class TestCategoryUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor_with_mandatory_params(self):
        data = {
            'name': 'Category', 
        }

        category = Category(**data)

        self.assertEqual(category.name, data['name'])
        self.assertEqual(category.description, None)
        self.assertEqual(category.is_active, True)
        self.assertIsInstance(category.created_at, datetime)
    
    def test_constructor(self):
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
        category_1 = Category(name='Category 1')
        category_2 = Category(name='Category 2')

        self.assertNotEqual(
            category_1.created_at.timestamp(),
            category_2.created_at.timestamp()
        )