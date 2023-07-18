from random import randint
from v2raySetting import *


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


class Vless:
    tag: str
    protocol: str
    settings: SettingsVless
    stream_settings: StreamSettings
    mux: Mux

    def __init__(self, settings: SettingsVless, stream_settings: StreamSettings, mux: Mux) -> None:
        self.tag = "proxy_" + str(randint(1111, 9999))
        self.protocol = "vless"
        self.settings = settings
        self.stream_settings = stream_settings
        self.mux = mux
