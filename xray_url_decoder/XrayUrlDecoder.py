import ipaddress
import json
import base64
import uuid
from urllib.parse import parse_qs, ParseResult, urlencode, urlparse, urlunparse
from xray_url_decoder.IsValid import isValid_tls, isValid_reality, isValid_userVless, isValid_vnextVless, isValid_link
from xray_url_decoder.XraySetting import GrpcSettings, TCPSettings, WsSettingsVless, RealitySettings, TLSSettings, Mux
from xray_url_decoder.trojan import Trojan, ServerTrojan, SettingsTrojan
from xray_url_decoder.vless import Vless, UserVless, SettingsVless, VnextVless
from xray_url_decoder.vmess import Vmess, UserVmess, VnextVmess, SettingsVmess
from xray_url_decoder.XraySetting import StreamSettings
from collections import namedtuple


def is_ipv6_address(hostname):
    try:
        ipaddress.IPv6Address(hostname)
        return True
    except ipaddress.AddressValueError:
        return False


def convertVmessLinkToStandardLink(link):
    data: dict = json.loads(base64.b64decode(link[8:]).decode('utf-8'))

    data['type'] = data['net']
    data['path'] = data.get('path', None)
    data['aid'] = data.get('aid', None)
    data['security'] = data.get('tls', None)

    if is_ipv6_address(data["add"]):
        data["add"] = "[{}]".format(data["add"])

    Components = namedtuple(
        typename='Components',
        field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
    )

    url = urlunparse(
        Components(
            scheme='vmess',
            netloc='{username}@{hostname}:{port}'.format(username=data['id'], hostname=data["add"], port=data["port"]),
            query=urlencode(data),
            path='',
            url='',
            fragment=data['ps']
        )
    )
    return url


class XrayUrlDecoder:
    url: ParseResult
    queries: dict
    link: str
    name: str
    isSupported: bool
    isValid: bool
    type: str
    security: str

    def __init__(self, link, tagUUID=None):
        match link[:5]:
            case "vmess":
                link = convertVmessLinkToStandardLink(link)

        if tagUUID is None:
            tagUUID = uuid.uuid4().hex

        self.link = link
        self.url = urlparse(self.link)
        self.name = tagUUID + "_@_" + (self.url.fragment if len(self.url.fragment) > 0 else "")
        q = parse_qs(self.url.query)
        self.queries = {key: value[0] for key, value in q.items()}
        self.isSupported = True
        self.isValid = True

        self.type = self.getQuery("type")
        self.security = self.getQuery("security")

        if not isValid_link(self.url.username, self.url.hostname, self.url.port):
            self.isValid = False

    def setIsValid(self, status: bool):
        if not status:
            self.isValid = status

    def getQuery(self, key) -> str | None:
        try:
            return self.queries[key]
        except KeyError:
            return None

    def generate_json(self) -> Vless | Vmess | Trojan | None:
        match self.url.scheme:
            case "vless":
                return self.vless_json()
            case "vmess":
                return self.vmess_json()
            case "trojan":
                return self.trojan_json()
            case _:
                self.isSupported = False
                print("schema {} is not supported yet".format(self.url.scheme))

    def generate_json_str(self) -> str:
        json_obj = self.generate_json()
        if json_obj is None:
            return ""
        return json.dumps(json_obj, default=lambda x: x.__dict__, ensure_ascii=False)

    def stream_setting_obj(self) -> StreamSettings | None:
        wsSetting = None
        grpcSettings = None
        tcpSettings = None
        tlsSettings = None
        realitySettings = None

        match self.type:
            case "grpc":
                grpcSettings = GrpcSettings(self.getQuery("serviceName"))
            case "ws":
                headers = {}
                if self.getQuery("sni") is not None:
                    headers["Host"] = self.getQuery("sni")
                wsSetting = WsSettingsVless(self.getQuery("path"), headers)

            case "tcp":
                tcpSettings = TCPSettings()
            case _:
                self.isSupported = False
                print("type '{}' is not supported yet".format(self.type))
                return

        match self.security:
            case "tls":
                alpn = None
                if self.getQuery("alpn") is not None:
                    alpn = self.getQuery("alpn").split(",")
                tlsSettings = TLSSettings(self.getQuery("sni"), fingerprint=self.getQuery("fp"), alpn=alpn)
                self.setIsValid(isValid_tls(tlsSettings))

            case "reality":
                realitySettings = RealitySettings(self.getQuery("sni"), self.getQuery("pbk"),
                                                  fingerprint=self.getQuery("fp"), spider_x=self.getQuery("spx"),
                                                  short_id=self.getQuery("sid"))
                self.setIsValid(isValid_reality(realitySettings))

            case _:
                self.isSupported = False
                print("security '{}' is not supported yet".format(self.security))
                return

        streamSetting = StreamSettings(self.type, self.security, wsSetting, grpcSettings,
                                       tcpSettings, tlsSettings, realitySettings)

        return streamSetting

    def vless_json(self) -> Vless:
        user = UserVless(self.url.username, flow=self.getQuery("flow"))
        vnext = VnextVless(self.url.hostname, self.url.port, [user])
        setting = SettingsVless([vnext])
        streamSetting = self.stream_setting_obj()
        mux = Mux()
        vless = Vless(self.name, setting, streamSetting, mux)

        self.setIsValid(isValid_userVless(user) and isValid_vnextVless(vnext))

        return vless

    def vmess_json(self) -> Vmess:
        user = UserVmess(self.url.username, alterId=self.getQuery("aid"), security=self.getQuery("scy"))
        vnext = VnextVmess(self.url.hostname, self.url.port, [user])
        setting = SettingsVmess([vnext])
        streamSetting = self.stream_setting_obj()
        mux = Mux()
        vmess = Vmess(self.name, setting, streamSetting, mux)

        return vmess

    def trojan_json(self) -> Trojan:
        server = ServerTrojan(self.url.hostname, self.url.port, self.url.username)
        setting = SettingsTrojan([server])
        streamSetting = self.stream_setting_obj()
        mux = Mux()
        trojan = Trojan(self.name, setting, streamSetting, mux)

        return trojan

    def is_equal_to_config(self, config_srt: str) -> bool:
        config = json.loads(config_srt)
        if config['protocol'] != self.url.scheme:
            return False

        match self.url.scheme:
            case "vless":
                return (config["settings"]["vnext"][0]["users"][0]["id"] == self.url.username and
                        config["settings"]["vnext"][0]["port"] == self.url.port and
                        config["settings"]["vnext"][0]["address"] == self.url.hostname)
            case "vmess":
                return (config["settings"]["vnext"][0]["users"][0]["id"] == self.url.username and
                        config["settings"]["vnext"][0]["port"] == self.url.port and
                        config["settings"]["vnext"][0]["address"] == self.url.hostname)
            case "trojan":
                return (config["settings"]["servers"][0]["password"] == self.url.username and
                        config["settings"]["servers"][0]["port"] == self.url.port and
                        config["settings"]["servers"][0]["address"] == self.url.hostname)

        return False
