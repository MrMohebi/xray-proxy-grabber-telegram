from typing import List


class SocksSettings:
    auth: str
    udp: bool
    allow_transparent: bool

    def __init__(self, auth: str = None, udp: bool = None, allow_transparent: bool = None) -> None:
        self.auth = auth if auth is not None else "noauth"
        self.udp = udp if udp is not None else True
        self.allow_transparent = allow_transparent if allow_transparent is not None else False


class Sniffing:
    enabled: bool
    destOverride: List[str]
    routeOnly: bool

    def __init__(self, enabled: bool = None, dest_override: List[str] = None, route_only: bool = None) -> None:
        self.enabled = enabled if enabled is not None else True
        self.destOverride = dest_override if dest_override is not None else ["http", "tls"]
        self.routeOnly = route_only if route_only is not None else False


class Inbound:
    tag: str
    port: int
    listen: str
    protocol: str
    sniffing: Sniffing
    settings: SocksSettings

    def __init__(self, tag: str, port: int, listen: str, protocol: str, sniffing: Sniffing, settings: SocksSettings) -> None:
        self.tag = tag
        self.port = port
        self.listen = listen
        self.protocol = protocol
        self.sniffing = sniffing
        self.settings = settings
