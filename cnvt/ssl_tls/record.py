from dataclasses import dataclass, field

from .tls_parameters import CipherSuite, CompressionMethod, ProtocolVersion
from .extensions import Extension


@dataclass(slots=True)
class ClientHello:
    legacy_version: ProtocolVersion = ProtocolVersion.TLSV1_2
    random: bytearray = bytearray(32)
    legacy_session_id: bytearray = bytearray(0)
    cipher_suites: list[CipherSuite] = field(
        default_factory=lambda: list(
            CipherSuite.get_all_with_ignores(
                ignores=[CipherSuite.TLS_FALLBACK_SCSV],
            )
        )
    )
    legacy_compression_methods: CompressionMethod = CompressionMethod.NULL
    extensions: list[Extension] = field(default_factory=lambda: [])