from cnvt.ssl_tls.extensions import (
    ExtensionType,
    Extension,
    SupportedVersions,
)
from cnvt.ssl_tls.tls_parameters import ProtocolVersion
from cnvt.sock import Payload


class ExtensionMock(Extension):
    extension_data: bytearray
    EXTENSION_TYPE = ExtensionType._MAX

    @property
    def extension_data_bytes(self) -> bytearray:
        return self.extension_data


def test_extension_type():
    assert ExtensionType.get_from_num(44) == ExtensionType.COOKIE
    assert ExtensionType.KEY_SHARE.as_bytes() == b'\x00\x33'

def test_extension():
    ext = ExtensionMock(extension_data=bytearray(b'\x01'))
    assert ext.extension_data_bytes == b'\x01'
    assert ext.pack() == Payload(data=b'\xFF\xFF\x00\x01\x01')
    assert ext.as_bytes() == bytearray(b'\xFF\xFF\x00\x01\x01')

def test_supported_versions():
    sv = SupportedVersions(
        extension_data=[ProtocolVersion.TLSV1_3],
    )
    assert sv.extension_data_bytes == b'\x03\x04'
    assert sv.pack() == Payload(data=b'\x00\x2b\x00\x02\x03\x04')
    assert sv.as_bytes() == bytearray(b'\x00\x2b\x00\x02\x03\x04')