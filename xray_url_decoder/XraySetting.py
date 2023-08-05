from typing import List


class Mux:
    enabled: bool
    concurrency: int

    def __init__(self, enabled: bool = None, concurrency: int = None) -> None:
        self.enabled = enabled if enabled is not None else False
        self.concurrency = concurrency if concurrency is not None else -1


class TLSSettings:
    serverName: str
    rejectUnknownSni: bool
    allowInsecure: bool
    alpn: List[str]
    minVersion: str
    maxVersion: str
    cipherSuites: str
    certificates: List[str]
    disableSystemRoot: bool
    enableSessionResumption: bool
    fingerprint: str
    pinnedPeerCertificateChainSha256: List[str]

    def __init__(self, server_name: str, reject_unknown_sni: bool = None, allow_insecure: bool = None,
                 alpn: List[str] = None, min_version: str = None, max_version: str = None, cipher_suites: str = None,
                 certificates: List[str] = None, disable_system_root: bool = None,
                 enable_session_resumption: bool = None, fingerprint: str = None,
                 pinned_peer_certificate_chain_sha256: List[str] = None) -> None:
        if server_name is not None:
            self.serverName = server_name
        if reject_unknown_sni is not None:
            self.rejectUnknownSni = reject_unknown_sni
        if allow_insecure is not None:
            self.allowInsecure = allow_insecure
        if alpn is not None:
            self.alpn = alpn
        if min_version is not None:
            self.minVersion = min_version
        if max_version is not None:
            self.maxVersion = max_version
        if cipher_suites is not None:
            self.cipherSuites = cipher_suites
        if certificates is not None:
            self.certificates = certificates
        if disable_system_root is not None:
            self.disableSystemRoot = disable_system_root
        if enable_session_resumption is not None:
            self.enableSessionResumption = enable_session_resumption
        if fingerprint is not None:
            self.fingerprint = fingerprint
        if pinned_peer_certificate_chain_sha256 is not None:
            self.pinnedPeerCertificateChainSha256 = pinned_peer_certificate_chain_sha256


class WsSettingsVless:
    path: str
    headers: dict

    def __init__(self, path: str = None, headers=None) -> None:
        self.path = path if path is not None else "/"
        self.headers = headers if headers is not None else {}


class GrpcSettings:
    serviceName: str
    multiMode: bool
    idleTimeout: int
    healthCheckTimeout: int
    permitWithoutStream: bool
    initialWindowsSize: int

    def __init__(self, service_name: str = None, multi_mode: bool = None, idle_timeout: int = None,
                 health_check_timeout: int = None,
                 permit_without_stream: bool = None, initial_windows_size: int = None) -> None:
        if service_name is not None:
            self.serviceName = service_name
        if multi_mode is not None:
            self.multiMode = multi_mode
        if idle_timeout is not None:
            self.idleTimeout = idle_timeout
        if health_check_timeout is not None:
            self.healthCheckTimeout = health_check_timeout
        if permit_without_stream is not None:
            self.permitWithoutStream = permit_without_stream
        if initial_windows_size is not None:
            self.initialWindowsSize = initial_windows_size


class RealitySettings:
    serverName: str
    fingerprint: str
    show: bool
    publicKey: str
    shortId: str
    spiderX: str

    def __init__(self, server_name: str, public_key: str, short_id: str = None, fingerprint: str = None,
                 show: bool = None, spider_x: str = None) -> None:
        self.serverName = server_name
        self.publicKey = public_key
        self.fingerprint = fingerprint if fingerprint is not None else "chrome"
        self.show = show if show is not None else False
        self.shortId = short_id if short_id is not None else ""
        self.spiderX = spider_x if spider_x is not None else "/"


class TCPSettings:
    acceptProxyProtocol: bool
    header: dict

    def __init__(self, accept_proxy_protocol: bool = None, header: dict = None) -> None:
        self.acceptProxyProtocol = accept_proxy_protocol if accept_proxy_protocol is not None else False
        if header is not None:
            self.header = header


class StreamSettings:
    network: str
    security: str
    tlsSettings: TLSSettings
    realitySettings: RealitySettings
    wsSettings: WsSettingsVless
    grpcSettings: GrpcSettings
    tcpSettings: TCPSettings

    def __init__(self, network: str, security: str, ws_settings: WsSettingsVless = None,
                 grpc_settings: GrpcSettings = None, tcp_settings: TCPSettings = None, tls_settings: TLSSettings = None,
                 reality_settings: RealitySettings = None) -> None:
        self.network = network
        self.security = security
        if tls_settings is not None:
            self.tlsSettings = tls_settings
        if ws_settings is not None:
            self.wsSettings = ws_settings
        if reality_settings is not None:
            self.realitySettings = reality_settings
        if grpc_settings is not None:
            self.grpcSettings = grpc_settings
        if tcp_settings is not None:
            self.tcpSettings = tcp_settings
