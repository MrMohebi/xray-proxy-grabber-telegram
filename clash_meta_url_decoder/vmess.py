from clash_meta_url_decoder.VBase import VBase
from clash_meta_url_decoder.VNetwork import VNetwork


class Vmess(VBase, VNetwork):
    uuid: str
    alterId: int
    cipher: str

    def __init__(self, uuid: str, vBase: VBase, bNetwork: VNetwork, alterId: int = None, cipher: str = None) -> None:
        self.uuid = uuid
        self.cipher = cipher if cipher is not None else "auto"
        try:
            self.alterId = int(alterId)
        except:
            self.alterId = 0
        VBase.__init__(self, vBase.type, vBase.name, vBase.server, vBase.port)
        VNetwork.__init__(self,
                          (bNetwork.network if hasattr(bNetwork, "network") else None),
                          (bNetwork.tls if hasattr(bNetwork, "tls") else None),
                          (bNetwork.servername if hasattr(bNetwork, "servername") else None),
                          (bNetwork.flow if hasattr(bNetwork, "flow") else None),
                          (bNetwork.udp if hasattr(bNetwork, "udp") else None),
                          (bNetwork.clientFingerprint if hasattr(bNetwork, "clientFingerprint") else None),
                          (bNetwork.fingerprint if hasattr(bNetwork, "fingerprint") else None),
                          (bNetwork.wsOpts if hasattr(bNetwork, "wsOpts") else None),
                          (bNetwork.grpcOpts if hasattr(bNetwork, "grpcOpts") else None),
                          (bNetwork.realityOpts if hasattr(bNetwork, "realityOpts") else None))
