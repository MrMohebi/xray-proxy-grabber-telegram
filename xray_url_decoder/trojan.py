import re
from random import randint
from typing import List

from xray_url_decoder.XraySetting import StreamSettings, Mux


class ServerTrojan:
    address: str
    port: int
    password: str
    email: str
    level: int

    def __init__(self, address: str, port: int, password: str, email: str = "t@t.tt", level: int = 1) -> None:
        self.address = address
        self.port = port
        self.password = password
        self.email = email
        self.level = level


class SettingsTrojan:
    servers: List[ServerTrojan]

    def __init__(self, servers: List[ServerTrojan]) -> None:
        self.servers = servers


class Trojan:
    tag: str
    protocol: str
    settings: SettingsTrojan
    streamSettings: StreamSettings
    mux: Mux

    def __init__(self, name: str, settings: SettingsTrojan, stream_settings: StreamSettings, mux: Mux) -> None:
        self.tag = name # "proxy_" + str(randint(1111, 9999999)) + "_" + re.sub(r'([/:+])+', '', name[:120])
        self.protocol = "trojan"
        self.settings = settings
        self.streamSettings = stream_settings
        self.mux = mux
