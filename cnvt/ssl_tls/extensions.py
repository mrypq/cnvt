from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Any

from .types import TLSEnum
from ..sock import Payload, NWByte
from .tls_parameters import ProtocolVersion


class ExtensionType(TLSEnum):
    SERVER_NAME = 0
    MAX_FRAGMENT_LENGTH = 1
    STATUS_REQUEST = 5
    SUPPORTED_GROUPS = 10
    SIGNATURE_ALGORITHMS = 13
    USE_SRTP = 14
    HEARTBEAT = 15
    APPLICATION_LAYER_PROTOCOL_NEGOTIATION = 16
    SIGNED_CERTIFICATE_TIMESTAMP = 18
    CLIENT_CERTIFICATE_TYPE = 19
    SERVER_CERTIFICATE_TYPE = 20
    PADDING = 21
    PRE_SHARED_KEY = 41
    EARLY_DATA = 42
    SUPPORTED_VERSIONS = 43
    COOKIE = 44
    PSK_KEY_EXCHANGE_MODES = 45
    CERTIFICATE_AUTHORITIES = 47
    OID_FILTERS = 48
    POST_HANDSHAKE_AUTH = 49
    SIGNATURE_ALGORITHMS_CERT = 50
    KEY_SHARE = 51
    _MAX = 65535


@dataclass(slots=True)
class Extension:
    extension_data: Any
    EXTENSION_TYPE: ClassVar[ExtensionType]

    def as_bytes(self) -> bytearray:
        return self.pack().data

    @property
    def extension_data_bytes(self) -> bytearray:
        raise NotImplementedError

    def pack(self) -> Payload:
        p = Payload()
        p.add_bytes(self.EXTENSION_TYPE.as_bytes())
        p.add_bytes(self.extension_data_bytes, len_size=2)
        return p


@dataclass(slots=True)
class SupportedVersions(Extension):
    extension_data: list[ProtocolVersion]|ProtocolVersion
    EXTENSION_TYPE = ExtensionType.SUPPORTED_VERSIONS

    @property
    def extension_data_bytes(self) -> bytearray:
        match self.extension_data:
            case ProtocolVersion():
                return self.extension_data.as_bytes()
            case list():
                return NWByte.sum(*[p.as_bytes() for p in self.extension_data])