import json
from urllib.parse import urlparse, parse_qs, ParseResult
from vless import *


class XrayUrlDecoder:
    url: ParseResult
    queries: dict
    link: str
    name: str

    def __init__(self, link):
        self.link = link
        self.url = urlparse(self.link)
        self.name = self.url.fragment
        q = parse_qs(self.url.query)
        self.queries = {key: value[0] for key, value in q.items()}

    def getQuery(self, key) -> str | None:
        try:
            return self.queries[key]
        except KeyError:
            return None

    def generate_json(self):
        match self.url.scheme:
            case "vless":
                self.vless_json()
            case _:
                print("URL is incorrect")

    def stream_setting_obj(self) -> StreamSettings:
        wsSetting = None
        grpcSettings = None
        tcpSettings = None
        tlsSettings = None
        realitySettings = None

        match self.queries["type"]:
            case "grpc":
                grpcSettings = GrpcSettings(self.getQuery("servicename"))
            case "ws":
                wsSetting = WsSettingsVless(self.getQuery("path"), {})
            case "tcp":
                tcpSettings = TCPSettings()
            case _:
                print("type '{}' is not supported yet".format(self.queries["type"]))

        match self.queries["security"]:
            case "tls":
                tlsSettings = TLSSettings(self.getQuery("sni"), fingerprint=self.getQuery("fp"))
            case "reality":
                realitySettings = RealitySettings(self.getQuery("sni"), self.getQuery("pbk"),
                                                  fingerprint=self.getQuery("fp"), spider_x=self.getQuery("spx"))

        streamSetting = StreamSettings(self.queries["type"], self.queries["security"], wsSetting, grpcSettings,
                                       tcpSettings, tlsSettings, realitySettings)

        return streamSetting

    def vless_json(self) -> Vless:
        user = UserVless(self.url.username)
        vnext = VnextVless(self.url.hostname, self.url.port, [user])
        setting = SettingsVless([vnext])
        streamSetting = self.stream_setting_obj()
        mux = Mux()
        vless = Vless(setting, streamSetting, mux)

        return vless

    def vless_json_str(self) -> str:
        return json.dumps(self.vless_json(), default=lambda x: x.__dict__)

a = XrayUrlDecoder(
    "vless://c3f0e733-40d1-41d9-afe6-75029a13a418@init1984-mtn.linuxmember.online:2087?security=tls&sni=inittes.parsiran.top&type=grpc&servicename=@init1984#@init1984%20-%20mtn")
a.generate_json()

b = XrayUrlDecoder(
    "vless://86dee03e-8119-4215-e719-279602c5a366@cljoon.wtf-broo.ir:2087?encryption=none&security=tls&sni=cljoon.wtf-broo.ir&alpn=h2%2Chttp%2F1.1&fp=chrome&type=ws&path=%2F#JoonWS-MrAR")
b.generate_json()

c = XrayUrlDecoder(
    "vless://1fbe1e72-1a3b-4b75-dce5-5598631f7efc@levi.wtf-broo.ir:57356?encryption=none&security=reality&sni=telewebion.com&fp=chrome&pbk=sq7N8HmEL1cPskTNP4h5M31BqAoeIQ76bBcCDh9fKQc&spx=%2F&type=grpc#Heaven%2B2-qngk0z2yv")
c.generate_json()

d = XrayUrlDecoder(
    "vless://825560ab-6b2c-4605-9f23-7d88df39e3d2@me.gymbroo.xyz:7575?headerType=none&security=none&type=tcp#ttt-tz32bsup")
d.generate_json()


print([a.vless_json_str(), b.vless_json_str(), c.vless_json_str(), d.vless_json_str()])


