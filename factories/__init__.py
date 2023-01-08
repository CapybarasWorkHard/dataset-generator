from typing import Generic, TypeVar

InstanceType = TypeVar('InstanceType')


class Factory(Generic[InstanceType]):
    def create(self) -> InstanceType:
        raise NotImplementedError()
