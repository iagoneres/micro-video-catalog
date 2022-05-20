from abc import ABC
from dataclasses import FrozenInstanceError, dataclass, is_dataclass
import unittest
from unittest.mock import patch
import uuid

from __seedwork.domain.exceptions import InvalidUuidException
from __seedwork.domain.value_objects import UniqueEntityId, ValueObject


@dataclass(frozen=True)
class StubOneAttribute(ValueObject):
    attribute_1: str


@dataclass(frozen=True)
class StubTwoAttributes(ValueObject):
    attribute_1: str
    attribute_2: str


class TestValueObjectUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(ValueObject))

    def test_if_is_a_abstract_class(self):
        self.assertIsInstance(ValueObject(), ABC)

    def test_init_attribute(self):
        value_object_1 = StubOneAttribute(attribute_1="value1")
        self.assertEqual(value_object_1.attribute_1, 'value1')

        value_object_2 = StubTwoAttributes(
            attribute_1="value1", attribute_2="value2")
        self.assertEqual(value_object_2.attribute_1, 'value1')
        self.assertEqual(value_object_2.attribute_2, 'value2')

    def test_convert_to_string(self):
        value_object_1 = StubOneAttribute(attribute_1="value1")
        self.assertEqual(value_object_1.attribute_1, str(value_object_1))

        value_object_2 = StubTwoAttributes(
            attribute_1="value1", attribute_2="value2")
        self.assertEqual(
            '{"attribute_1": "value1", "attribute_2": "value2"}', str(value_object_2))


class TestUniqueEntityIdUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_exception_when_uuid_is_invalid(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            with self.assertRaises(InvalidUuidException) as assert_error:
                UniqueEntityId('Fake ID')
            mock_validate.assert_called_once()
            self.assertEqual(
                assert_error.exception.args[0], 'ID must be a valid UUID')

    def test_accept_uuid_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            value_object = UniqueEntityId(
                '08976216-4179-40bd-ba77-d357c95b9bba')
            mock_validate.assert_called_once()
            self.assertEqual(
                value_object.id, '08976216-4179-40bd-ba77-d357c95b9bba')

    def test_uuid_conversion_to_str_on_create(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            uuid_value = uuid.uuid4()
            value_object = UniqueEntityId(uuid_value)
            mock_validate.assert_called_once()
            self.assertEqual(value_object.id, str(uuid_value))

    def test_generate_id_when_id_is_not_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = 'Fake Id'

    def test_convert_to_str(self):
        value_object = UniqueEntityId()
        self.assertEqual(value_object.id, str(value_object))
