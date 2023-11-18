import re
from random import randint
from typing import List

from xray_url_decoder.XraySetting import StreamSettings, Mux


class UserVmess:
    id: str
    security: str
    level: int
    alterId: int

    def __init__(self, id: str, alterId: int = None, security: str = None, level: int = None) -> None:
        self.id = id
        self.security = security if security is not None else "auto"
        self.level = level if level is not None else 0
        self.alterId = alterId if alterId is not None else 0


class VnextVmess:
    address: str
    port: int
    users: List[UserVmess]

    def __init__(self, address: str, port: int, users: List[UserVmess]) -> None:
        self.address = address
        self.port = port
        self.users = users


class SettingsVmess:
    vnext: List[VnextVmess]

    def __init__(self, vnext: List[VnextVmess]) -> None:
        self.vnext = vnext


class Vmess:
    tag: str
    protocol: str
    settings: SettingsVmess
    streamSettings: StreamSettings
    mux: Mux

    def __init__(self, name: str, settings: SettingsVmess, stream_settings: StreamSettings, mux: Mux) -> None:
        self.tag = name # "proxy_" + str(randint(1111, 9999999)) + "_" + re.sub(r'([/:+])+', '', name[:120])
        self.protocol = "vmess"
        self.settings = settings
        self.streamSettings = stream_settings
        self.mux = mux
