import pytest

from cnvt.ssl_tls.types import TLSEnum


def TLSEnum_mock(a, b):
    return TLSEnum(
        value='TLSEnumMock',
        names=(
            ('A', a),
            ('B', b),
            )
    )

TLSEnumIntMock = TLSEnum_mock(0, 1)
TLSEnumIntListMock = TLSEnum_mock([0x00, 0x04], [0x00, 0x05])
TLSEnumMaxZeroMock = TLSEnum_mock(0, 0)


def test_tls_enum_init():
    a = TLSEnumIntMock.A
    assert a.name == 'A'
    assert a.value == 0
    assert a.num == 0

    b = TLSEnumIntListMock.B
    assert b.name == 'B'
    assert b.value == [0x00, 0x05]
    assert b.num == 5

    with pytest.raises(ValueError) as e:
        TLSEnumStrMock = TLSEnum_mock('a', 'b')
    assert e.type == ValueError

    with pytest.raises(ValueError) as e:
        TLSEnumStrListMock = TLSEnum_mock(['a'], ['b'])
    assert e.type == ValueError

def test_tls_enum_max():
    assert TLSEnumIntMock.A._max == 1
    assert TLSEnumIntListMock.A._max == 5
    assert TLSEnumMaxZeroMock.A._max == 0

def test_tls_enum_bsize():
    assert TLSEnumIntMock.A._bsize == 1
    assert TLSEnumIntListMock.A._bsize == 2
    assert TLSEnumMaxZeroMock.A._bsize == 1

def test_tls_enum_get_all():
    all_values = list(TLSEnumIntMock.get_all())
    assert all_values == [
        TLSEnumIntMock.A,
        TLSEnumIntMock.B,
    ]

def test_tls_enum_get_all_with_ignores():
    all_values = list(TLSEnumIntMock.get_all_with_ignores([TLSEnumIntMock.B]))
    assert all_values == [
        TLSEnumIntMock.A,
    ]

def test_tls_enum_get_from_num():
    assert TLSEnumIntMock.get_from_num(1) == TLSEnumIntMock.B
    assert TLSEnumIntListMock.get_from_num(4) == TLSEnumIntListMock.A

def test_tls_enum_as_bytes():
    assert TLSEnumIntMock.A.as_bytes() == b'\x00'
    assert TLSEnumIntListMock.B.as_bytes() == b'\x00\x05'