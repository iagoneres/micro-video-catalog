from dataclasses import dataclass
from typing import Any

from __seedwork.domain.exceptions import ValidationException


@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    attribute: str

    @staticmethod
    def values(value: Any, attribute: str):
        return ValidatorRules(value, attribute)

    def required(self) -> 'ValidatorRules':
        if self.value is None or self.value == "":
            raise ValidationException(f'The "{self.attribute}" is required.')
        return self

    def string(self) -> 'ValidatorRules':
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationException(
                f'The "{self.attribute}" must be a string.')
        return self

    def max_length(self, max_length: int) -> 'ValidatorRules':
        if self.value is not None and len(self.value) > max_length:
            raise ValidationException(
                f'The "{self.attribute}" must be less than {max_length} characters.')
        return self

    def boolean(self) -> 'ValidatorRules':
        if self.value is not None and self.value is not True and self.value is not False:
            raise ValidationException(
                f'The "{self.attribute}" must be a boolean')
        return self
