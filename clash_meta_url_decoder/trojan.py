from clash_meta_url_decoder.VBase import VBase


class Trojan(VBase):
    password: str
    clientFingerprint: str
    fingerprint: str
    udp: bool
    sni: str
    alpn: list[str]
    skipCertVerify: bool

    def __init__(self, password: str, vBase: VBase, clientFingerprint: str = None, fingerprint: str = None,
                 udp: bool = None, sni: str = None, alpn: list[str] = None, skipCertVerify: bool = None) -> None:

        VBase.__init__(self, vBase.type, vBase.name, vBase.server, vBase.port)

        self.password = password
        self.clientFingerprint = clientFingerprint if clientFingerprint is not None else "chrome"
        if fingerprint is not None:
            self.fingerprint = fingerprint
        if udp is not None:
            self.udp = udp
        if sni is not None:
            self.sni = sni
        if alpn is not None:
            self.alpn = alpn
        if skipCertVerify is not None:
            self.skipCertVerify = skipCertVerify
