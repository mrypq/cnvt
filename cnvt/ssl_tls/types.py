from enum import Enum
from typing import Iterator
from typing_extensions import Self


class TLSEnum(Enum):
    def __init__(self, num: int|list[int]):
        match num:
            case int():
                self.num = num
            case list():
                try:
                    self.num = int.from_bytes(bytearray(num), 'big')
                except:
                    raise ValueError
            case _:
                raise ValueError

    @property
    def _max(self) -> int:
        return max([v.num for v in self.get_all()])

    @property
    def _bsize(self) -> int:
        if isinstance(self.value, list):
            return len(self.value)
        m = self._max if self._max > 0 else 1
        bsize = 0
        while m != 0:
            m >>= 8
            bsize += 1
        return bsize

    @classmethod
    def get_all(cls) -> Iterator[Self]:
        for v in cls.__members__.values():
            yield v

    @classmethod
    def get_all_with_ignores(cls, ignores: list[Self]) -> Iterator[Self]:
        for v in cls.__members__.values():
            if v not in ignores:
                yield v

    @classmethod
    def get_from_num(cls, num: int) -> Self:
        for v in cls.__members__.values():
            if v.num == num:
                return v

    def as_bytes(self) -> bytearray:
        return bytearray(self.num.to_bytes(self._bsize,'big'))