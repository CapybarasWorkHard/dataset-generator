from typing import Generic, TypeVar

_InstanceType = TypeVar('_InstanceType')


class Factory(Generic[_InstanceType]):
    """Allows you to dynamically create classes"""

    def create(self) -> _InstanceType:
        raise NotImplementedError()
