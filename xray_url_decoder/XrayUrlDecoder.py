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
        self.name = self.url.fragment if len(self.url.fragment) > 0 else ""
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
                print("schema {} is not supported yet".format(self.url.scheme))

    def stream_setting_obj(self) -> StreamSettings:
        wsSetting = None
        grpcSettings = None
        tcpSettings = None
        tlsSettings = None
        realitySettings = None

        match self.queries["type"]:
            case "grpc":
                grpcSettings = GrpcSettings(self.getQuery("serviceName"))
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
        vless = Vless(self.name, setting, streamSetting, mux)

        return vless

    def vless_json_str(self) -> str:
        return json.dumps(self.vless_json(), default=lambda x: x.__dict__)
