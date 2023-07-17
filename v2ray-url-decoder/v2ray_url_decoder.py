import json
import uuid
from typing import AnyStr
from urllib.parse import urlparse, parse_qs, ParseResult
from vless import *


class V2rayUrlDecoder:
    url: ParseResult
    queries: dict
    link: str
    name: str

    def __init__(self, link):
        self.link = link
        self.url = urlparse(self.link)
        self.queries = parse_qs(self.url.query)
        self.name = self.url.fragment

    def generate_json(self):
        match self.url.scheme:
            case "vless":
                self.vless_json()
            case _:
                print("URL is incorrect")

    def vless_json(self):
        user = UserVless(self.url.username)
        vnext = VnextVless(self.url.hostname, self.url.port, [user])
        setting = SettingsVless([vnext])
        tlsSetting = TLSSettingsVless(self.queries["sni"])
        wsSetting = WsSettingsVless()
        streamSetting = StreamSettingsVless(self.queries["type"], self.queries["security"], tlsSetting, wsSetting)
        mux = MuxVless()
        vless = Vless(setting, streamSetting, mux)

        jsonStr = json.dumps(vless, default=lambda x: x.__dict__)

        print(jsonStr)


x = V2rayUrlDecoder(
    "vless://c3f0e733-40d1-41d9-afe6-75029a13a418@init1984-mtn.linuxmember.online:2087?security=tls&sni=inittes.parsiran.top&type=grpc&servicename=@init1984#@init1984%20-%20mtn")

x.generate_json()

z = V2rayUrlDecoder(
    "vless://86dee03e-8119-4215-e719-279602c5a366@cljoon.wtf-broo.ir:2087?encryption=none&security=tls&sni=cljoon.wtf-broo.ir&alpn=h2%2Chttp%2F1.1&fp=chrome&type=ws&path=%2F#JoonWS-MrAR")

z.generate_json()
