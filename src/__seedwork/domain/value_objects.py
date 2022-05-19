from abc import ABC
from dataclasses import dataclass, field, fields
import json
import uuid

from __seedwork.domain.exceptions import InvalidUuidException


@dataclass(frozen=True)
class ValueObject(ABC):

    def __str__(self) -> str:
        field_names = [field.name for field in fields(self)]
        return str(getattr(self, field_names[0])) \
            if len(field_names) == 1 \
            else json.dumps({field_name: getattr(self, field_name) for field_name in field_names})

@dataclass(frozen=True)
class UniqueEntityId(ValueObject):

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    def __post_init__(self) -> None:
        id_value = str(self.id) if isinstance(self.id, uuid.UUID) else self.id
        object.__setattr__(self, 'id', id_value)

        self.__validate()

    def __validate(self) -> None:
        try:
            uuid.UUID(self.id)
        except ValueError as ex:
            raise InvalidUuidException() from ex

    def __str__(self) -> str:
        return f"{self.id}"
1