import re
from random import randint
from typing import List

from xray_url_decoder.XraySetting import StreamSettings, Mux


class UserVless:
    id: str
    alterId: int
    email: str
    security: str
    encryption: str
    flow: str

    def __init__(self, id: str, alter_id: int = 0, email: str = "t@t.tt", security: str = "auto",
                 encryption: str = "none", flow: str = "") -> None:
        self.id = id
        self.alterId = alter_id
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


class Vless:
    tag: str
    protocol: str
    settings: SettingsVless
    streamSettings: StreamSettings
    mux: Mux

    def __init__(self, name: str, settings: SettingsVless, stream_settings: StreamSettings, mux: Mux) -> None:
        self.tag = name # "proxy_" + str(randint(1111, 9999999)) + "_" + re.sub(r'([/:+])+', '', name[:120])
        self.protocol = "vless"
        self.settings = settings
        self.streamSettings = stream_settings
        self.mux = mux
