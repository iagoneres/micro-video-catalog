from abc import ABC
from dataclasses import dataclass, is_dataclass
import unittest

from __seedwork.domain.entities import Entity
from __seedwork.domain.value_objects import UniqueEntityId


@dataclass(frozen=True, kw_only=True)
class StubEntity(Entity):
    attribute_1: str
    attribute_2: str


class TestEntityUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Entity))

    def test_if_is_a_abstract_class(self):
        self.assertIsInstance(Entity(), ABC)

    def test_set_id_and_attributes(self):
        entity = StubEntity(attribute_1='value_1', attribute_2='value_2')
        self.assertEqual(entity.attribute_1, 'value_1')
        self.assertEqual(entity.attribute_2, 'value_2')
        self.assertIsInstance(entity.unique_entity_id, UniqueEntityId)
        self.assertEqual(entity.unique_entity_id.id, entity.id)

    def test_accept_a_valid_uuid(self):
        entity = StubEntity(
            unique_entity_id='08976216-4179-40bd-ba77-d357c95b9bba',
            attribute_1='value_1',
            attribute_2='value_2'
        )

        self.assertDictEqual(entity.to_dict(), {
            'id': '08976216-4179-40bd-ba77-d357c95b9bba',
            'attribute_1': 'value_1',
            'attribute_2': 'value_2'
        })
