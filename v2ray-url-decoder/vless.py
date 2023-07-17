from random import randint
from typing import List


class MuxVless:
    enabled: bool
    concurrency: int

    def __init__(self, enabled: bool = False, concurrency: int = -1) -> None:
        self.enabled = enabled
        self.concurrency = concurrency


class UserVless:
    id: str
    alter_id: int
    email: str
    security: str
    encryption: str
    flow: str

    def __init__(self, id: str, alter_id: int = 0, email: str = "t@t.tt", security: str = "auto",
                 encryption: str = "none", flow: str = "") -> None:
        self.id = id
        self.alter_id = alter_id
        self.email = email
        self.security = security
        self.encryption = encryption
        self.flow = flow


class VnextVless:
    address: str
    port: int
    users: List[UserVless]

    def __init__(self, address: str, port: int, users: List[UserVless]) -> None:
        self.address = address
        self.port = port
        self.users = users


class SettingsVless:
    vnext: List[VnextVless]

    def __init__(self, vnext: List[VnextVless]) -> None:
        self.vnext = vnext


class TLSSettingsVless:
    allow_insecure: bool
    server_name: str
    alpn: List[str]
    fingerprint: str
    show: bool

    def __init__(self, server_name: str, allow_insecure: bool = False, alpn=None, fingerprint: str = "chrome",
                 show: bool = False) -> None:
        if alpn is None:
            alpn = ["h2", "http/1.1"]

        self.allow_insecure = allow_insecure
        self.server_name = server_name
        self.alpn = alpn
        self.fingerprint = fingerprint
        self.show = show


class WSHeadersVless:
    pass

    def __init__(self, ) -> None:
        pass


class WsSettingsVless:
    path: str
    headers: WSHeadersVless

    def __init__(self, headers=None, path: str = "/") -> None:
        self.path = path
        self.headers = headers


class GrpcSettingsVless:
    service_name: str
    multi_mode: bool
    idle_timeout: int
    health_check_timeout: int
    permit_without_stream: bool
    initial_windows_size: int

    def __init__(self, service_name: str = "", multi_mode: bool = "false", idle_timeout: int = 60,
                 health_check_timeout: int = 20,
                 permit_without_stream: bool = False, initial_windows_size: int = 0) -> None:
        self.service_name = service_name
        self.multi_mode = multi_mode
        self.idle_timeout = idle_timeout
        self.health_check_timeout = health_check_timeout
        self.permit_without_stream = permit_without_stream
        self.initial_windows_size = initial_windows_size


class RealitySettingsVless:
    server_name: str
    fingerprint: str
    show: bool
    public_key: str
    short_id: str
    spider_x: str

    def __init__(self, server_name: str, public_key: str, short_id: str, fingerprint: str = "chrome",
                 show: bool = False, spider_x: str = "/") -> None:
        self.server_name = server_name
        self.fingerprint = fingerprint
        self.show = show
        self.public_key = public_key
        self.short_id = short_id
        self.spider_x = spider_x


class StreamSettingsVless:
    network: str
    security: str
    tls_settings: TLSSettingsVless | None
    reality_settings: RealitySettingsVless | None
    ws_settings: WsSettingsVless | None
    grpc_settings: GrpcSettingsVless | None

    def __init__(self, network: str, security: str, tls_settings: TLSSettingsVless=None, reality_settings: RealitySettingsVless = None, ws_settings: WsSettingsVless=None, grpc_settings: GrpcSettingsVless = None) -> None:
        self.network = network
        self.security = security
        self.tls_settings = tls_settings
        self.ws_settings = ws_settings


class Vless:
    tag: str = ""
    protocol: str = "vless"
    settings: SettingsVless
    stream_settings: StreamSettingsVless
    mux: MuxVless

    def __init__(self, settings: SettingsVless, stream_settings: StreamSettingsVless, mux: MuxVless) -> None:
        self.tag = "proxy_" + str(randint(1111, 9999))
        self.settings = settings
        self.stream_settings = stream_settings
        self.mux = mux
