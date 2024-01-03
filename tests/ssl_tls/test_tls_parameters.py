from cnvt.ssl_tls.tls_parameters import (
    ProtocolVersion,
    CompressionMethod,
    SignatureScheme,
    NamedGroup,
    CipherSuite,
    HandshakeType,
    ContentType,
)


def test_protocol_version():
    assert ProtocolVersion.get_from_num(0x0303) == ProtocolVersion.TLSV1_2
    assert ProtocolVersion.SSLV3.as_bytes() == b'\x03\x00'

def test_compression_method():
    assert CompressionMethod.get_from_num(0) == CompressionMethod.NULL
    assert CompressionMethod.NULL.as_bytes() == b'\x00'

def test_signatue_schme():
    assert SignatureScheme.get_from_num(0x0807) == SignatureScheme.ED25519
    assert SignatureScheme.ECDSA_SHA1.as_bytes() == b'\x02\x03'

def test_named_group():
    assert NamedGroup.get_from_num(30) == NamedGroup.X448
    assert NamedGroup.SECP192R1.as_bytes() == b'\x00\x13'

def test_cipher_suite():
    assert CipherSuite.get_from_num(0x0007) == CipherSuite.TLS_RSA_WITH_IDEA_CBC_SHA
    assert CipherSuite.TLS_FALLBACK_SCSV.as_bytes() == b'\x56\x00'

def test_handshake_type():
    assert HandshakeType.get_from_num(1) == HandshakeType.CLIENT_HELLO
    assert HandshakeType.SERVER_HELLO.as_bytes() == b'\x02'

def test_content_type():
    assert ContentType.get_from_num(22) == ContentType.HANDSHAKE
    assert ContentType.ALERT.as_bytes() == b'\x15'