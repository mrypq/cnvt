from __future__ import annotations

import sys
import socket
from typing import TypeAlias, Iterator


uint8: TypeAlias = int
uint16: TypeAlias = int
uint24: TypeAlias = int
uint32: TypeAlias = int
uint64: TypeAlias = int
opaque: TypeAlias = bytearray


class NWByte:
    BO = 'big'

    @classmethod
    def uint8(cls, n: int) -> bytearray:
        return bytearray(n.to_bytes(1, cls.BO))

    @classmethod
    def uint16(cls, n: int) -> bytearray:
        return bytearray(n.to_bytes(2, cls.BO))

    @classmethod
    def uint24(cls, n: int) -> bytearray:
        return bytearray(n.to_bytes(3, cls.BO))

    @classmethod
    def uint32(cls, n: int) -> bytearray:
        return bytearray(n.to_bytes(4, cls.BO))

    @classmethod
    def to_int(cls, b: bytearray) -> int:
        return int.from_bytes(b, cls.BO)

    @staticmethod
    def sum(*args: tuple[bytes|bytearray]) -> bytearray:
        return bytearray(b''.join(args))


class Payload:
    def __init__(self, data: bytes|bytearray=b''):
        self.data = bytearray(data)

    @property
    def length(self) -> int:
        return len(self.data)

    def add_bytes(self, b: bytearray, len_size=0):
        if len_size:
            length = len(b)
            self.data += bytearray(length.to_bytes(len_size, 'big'))
        self.data += b

    def add_uint8(self, n: int, len_size=0):
        self.add_bytes(NWByte.uint8(n), len_size)

    def add_uint16(self, n: int, len_size=0):
        self.add_bytes(NWByte.uint16(n), len_size)

    def add_payload(self, payload: Payload, len_size=0):
        self.add_bytes(payload.data, len_size)

    def add_bytes_list(self, l: list[bytearray], len_size=0):
        b = NWByte.sum(*l)
        self.add_bytes(b, len_size)

    def read_bytes(self, n: int, len_size=0) -> bytearray:
        if len_size:
            self.data = self.data[len_size:]
        b, self.data = self.data[:n], self.data[n:]
        return bytearray(b)
    
    def read_int(self, n: int, len_size=0) -> int:
        b = self.read_bytes(n, len_size)
        return NWByte.to_int(b)

    def read_uint8(self, len_size=0) -> uint8:
        return self.read_int(1, len_size)

    def read_uint16(self, len_size=0) -> uint16:
        return self.read_int(2, len_size)

    def read_uint24(self, len_size=0) -> uint24:
        return self.read_int(3, len_size)

    def read_uint32(self, len_size=0) -> uint32:
        return self.read_int(4, len_size)

    def read_uint64(self, len_size=0) -> uint64:
        return self.read_int(5, len_size)

    def read_vector(self, len_size: int) -> tuple[int, bytearray]:
        length = self.read_int(len_size)
        b = self.read_bytes(length)
        return length, b

    def read_payload(self, len_size: int) -> tuple[int, Payload]:
        length, b = self.read_vector(len_size)
        return length, Payload(b)

    def read_list(self, len_size: int, data_size: int) -> Iterator[bytearray]:
        length, p = self.read_payload(len_size)
        for _ in range(length//data_size):
            yield p.read_bytes(data_size)

    def read_int_list(self, len_size: int, data_size: int) -> Iterator[int]:
        length, p = self.read_payload(len_size)
        for _ in range(length//data_size):
            yield p.read_int(data_size)

    def __eq__(self, other: Payload):
        if isinstance(self, other.__class__):
            return self.data == other.data
        return False


class Socket:
    def __init__(self, host: str, port: int|str):
        self.host = host
        self.port = self.convert_port(port)
        self.connect()

    def connect(self, timeout=5):
        try:
            self.sock = socket.create_connection(
                address=(self.host, self.port),
                timeout=timeout,
            )
        except socket.timeout:
            raise TimeoutError
        except:
            sys.exit(3)

    def close(self):
        self.sock.close()

    def write(self, payload: bytearray):
        self.sock.sendall(payload)

    def read(self, n=2048) -> Payload:
        return Payload(self.sock.recv(n))

    def readuntil(self, b: bytearray) -> Payload:
        '''指定された文字列が現れるまで読み込む'''
        res = b''
        while not res.endswith(b):
            res += self.sock.recv(1)
        return Payload(res)

    @staticmethod
    def convert_port(port: int|str) -> int:
        if isinstance(port, int):
            return port
        else:
            try:
                return int(port)
            except:
                raise TypeError