from typing import List


class Mux:
    enabled: bool
    concurrency: int

    def __init__(self, enabled: bool = None, concurrency: int = None) -> None:
        self.enabled = enabled if enabled is not None else False
        self.concurrency = concurrency if concurrency is not None else -1


class TLSSettings:
    server_name: str
    reject_unknown_sni: bool
    allow_insecure: bool
    alpn: List[str]
    min_version: str
    max_version: str
    cipher_suites: str
    certificates: List[str]
    disable_system_root: bool
    enable_session_resumption: bool
    fingerprint: str
    pinned_peer_certificate_chain_sha256: List[str]

    def __init__(self, server_name: str, reject_unknown_sni: bool = None, allow_insecure: bool = None,
                 alpn: List[str] = None, min_version: str = None, max_version: str = None, cipher_suites: str = None,
                 certificates: List[str] = None, disable_system_root: bool = None,
                 enable_session_resumption: bool = None, fingerprint: str = None,
                 pinned_peer_certificate_chain_sha256: List[str] = None) -> None:
        self.server_name = server_name
        self.reject_unknown_sni = reject_unknown_sni if reject_unknown_sni is not None else False
        self.allow_insecure = allow_insecure if allow_insecure is not None else False
        self.alpn = alpn if alpn is not None else ["h2", "http/1.1"]
        self.min_version = min_version if min_version is not None else "1.1"
        self.max_version = max_version if max_version is not None else "1.3"
        self.cipher_suites = cipher_suites if cipher_suites is not None else ""
        self.certificates = certificates if certificates is not None else []
        self.disable_system_root = disable_system_root if disable_system_root is not None else False
        self.enable_session_resumption = enable_session_resumption if enable_session_resumption is not None else False
        self.fingerprint = fingerprint if fingerprint is not None else "chrome"
        self.pinned_peer_certificate_chain_sha256 = pinned_peer_certificate_chain_sha256 if pinned_peer_certificate_chain_sha256 is not None else [""]


class WsSettingsVless:
    path: str
    headers: dict

    def __init__(self, path: str = None, headers=None) -> None:
        self.path = path if path is not None else "/"
        self.headers = headers if headers is not None else {}


class GrpcSettings:
    service_name: str
    multi_mode: bool
    idle_timeout: int
    health_check_timeout: int
    permit_without_stream: bool
    initial_windows_size: int

    def __init__(self, service_name: str = None, multi_mode: bool = None, idle_timeout: int = None,
                 health_check_timeout: int = None,
                 permit_without_stream: bool = None, initial_windows_size: int = None) -> None:
        self.service_name = service_name if service_name is not None else ""
        self.multi_mode = multi_mode if multi_mode is not None else False
        self.idle_timeout = idle_timeout if idle_timeout is not None else 60
        self.health_check_timeout = health_check_timeout if health_check_timeout is not None else 20
        self.permit_without_stream = permit_without_stream if permit_without_stream is not None else False
        self.initial_windows_size = initial_windows_size if initial_windows_size is not None else 0


class RealitySettings:
    server_name: str
    fingerprint: str
    show: bool
    public_key: str
    short_id: str
    spider_x: str

    def __init__(self, server_name: str, public_key: str, short_id: str = None, fingerprint: str = None, show: bool = None, spider_x: str = None) -> None:
        self.server_name = server_name
        self.public_key = public_key
        self.fingerprint = fingerprint if fingerprint is not None else "chrome"
        self.show = show if show is not None else False
        self.short_id = short_id if short_id is not None else ""
        self.spider_x = spider_x if spider_x is not None else "/"


class TCPSettings:
    accept_proxy_protocol: bool
    header: dict

    def __init__(self, accept_proxy_protocol: bool = None, header: dict = None) -> None:
        self.accept_proxy_protocol = accept_proxy_protocol if accept_proxy_protocol is not None else False
        self.header = header if header is not None else {}


class StreamSettings:
    network: str
    security: str
    tls_settings: TLSSettings
    reality_settings: RealitySettings
    ws_settings: WsSettingsVless
    grpc_settings: GrpcSettings
    tcp_settings: TCPSettings

    def __init__(self, network: str, security: str, ws_settings: WsSettingsVless = None,
                 grpc_settings: GrpcSettings = None, tcp_settings: TCPSettings = None, tls_settings: TLSSettings = None,
                 reality_settings: RealitySettings = None) -> None:
        self.network = network
        self.security = security
        if tls_settings is not None:
            self.tls_settings = tls_settings
        if ws_settings is not None:
            self.ws_settings = ws_settings
        if reality_settings is not None:
            self.reality_settings = reality_settings
        if grpc_settings is not None:
            self.grpc_settings = grpc_settings
        if tcp_settings is not None:
            self.tcp_settings = tcp_settings
