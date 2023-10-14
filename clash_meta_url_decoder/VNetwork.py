class RealityOpts:
    publicKey: str
    shortId: str

    def __init__(self, publicKey: str, shortId: str = None):
        self.publicKey = publicKey
        self.shortId = shortId if shortId is not None else ""


class GrpcOpts:
    grpcServiceName: str

    def __init__(self, grpcServiceName: str):
        self.grpcServiceName = grpcServiceName


class WsHeaders:
    Host: str

    def __init__(self, Host: str):
        self.Host = Host


class WsOpts:
    path: str
    headers: WsHeaders

    def __init__(self, host: str = None, path: str = None):
        if host is not None:
            self.headers = WsHeaders(host)
        self.path = path if path is not None else "/"


class VNetwork:
    network: str
    tls: bool
    servername: str
    flow: str
    udp: bool
    clientFingerprint: str
    fingerprint: str
    wsOpts: WsOpts
    grpcOpts: GrpcOpts
    realityOpts: RealityOpts

    def __init__(self,
                 network: str,
                 tls: bool = None,
                 servername: str = None,
                 flow: str = None,
                 udp: bool = None,
                 clientFingerprint: str = None,
                 fingerprint: str = None,
                 wsOpts: WsOpts = None,
                 grpcOpts: GrpcOpts = None,
                 realityOpts: RealityOpts = None) -> None:
        self.network = network
        self.tls = tls if tls is not None else False
        self.udp = udp if udp is not None else False
        self.clientFingerprint = clientFingerprint if clientFingerprint is not None else "chrome"

        if servername is not None:
            self.servername = servername
        if flow is not None:
            self.flow = flow
        if fingerprint is not None:
            self.fingerprint = fingerprint
        if wsOpts is not None:
            self.wsOpts = wsOpts
        if grpcOpts is not None:
            self.grpcOpts = grpcOpts
        if realityOpts is not None:
            self.realityOpts = realityOpts

