import ipaddress
import json
import base64
import re
import uuid
from collections import namedtuple
from urllib.parse import parse_qs, ParseResult, urlencode, urlparse, urlunparse

from clash_meta_url_decoder.IsValid import isValid_link
from clash_meta_url_decoder.VBase import VBase
from clash_meta_url_decoder.VNetwork import VNetwork, GrpcOpts, WsOpts, RealityOpts
from clash_meta_url_decoder.trojan import Trojan
from clash_meta_url_decoder.vless import Vless
from clash_meta_url_decoder.vmess import Vmess


def camel_to_kebab(obj):
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            # Convert camelCase to kebab-case
            kebab_key = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', key).lower()
            new_obj[kebab_key] = camel_to_kebab(value) if isinstance(value, dict) else value
        return new_obj
    elif isinstance(obj, list):
        return [camel_to_kebab(item) for item in obj]
    else:
        return obj


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


def class_to_json_str_kabab(obj):
    return json.dumps(camel_to_kebab(vars(obj)), default=lambda x: camel_to_kebab(vars(x)), ensure_ascii=False)


class ClashMetaDecoder:
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

    def generate_obj_str(self) -> str:
        match self.url.scheme:
            case "vless":
                return class_to_json_str_kabab(self.vless())
            case "vmess":
                return class_to_json_str_kabab(self.vmess()).replace("alter-id", "alterId")
            case "trojan":
                return class_to_json_str_kabab(self.trojan())
            case _:
                self.isSupported = False
                print("schema {} is not supported yet".format(self.url.scheme))

    def vNetwork_obj(self) -> VNetwork | None:
        wsOpts = None
        grpcOpts = None
        realityOpts = None

        isTLS = False

        match self.type:
            case "grpc":
                if self.getQuery("serviceName") is not None:
                    grpcOpts = GrpcOpts(self.getQuery("serviceName"))
            case "ws":
                wsOpts = WsOpts(self.getQuery("sni"), self.getQuery("path"))
            case _:
                self.type = "tcp"

        match self.security:
            case "tls":
                isTLS = True
            case "reality":
                isTLS = True
                realityOpts = RealityOpts(self.getQuery("pbk"), self.getQuery("sid"))
            case "none":
                isTLS = False
            case _:
                isTLS = False

        vNetwork = VNetwork(self.type, isTLS, self.getQuery("sni"), self.getQuery("flow"), False, self.getQuery("fp"),
                            "", wsOpts, grpcOpts, realityOpts)

        return vNetwork

    def vless(self) -> Vless:
        vBase = VBase("vless", self.name, self.url.hostname, self.url.port)
        vNetwork = self.vNetwork_obj()
        vless = Vless(self.url.username, vBase, vNetwork)

        return vless

    def vmess(self) -> Vmess:
        vBase = VBase("vmess", self.name, self.url.hostname, self.url.port)
        vNetwork = self.vNetwork_obj()
        vmess = Vmess(self.url.username, vBase, vNetwork, alterId=self.getQuery("aid"), cipher=self.getQuery("scy"))

        return vmess

    def trojan(self) -> Trojan:
        vBase = VBase("trojan", self.name, self.url.hostname, self.url.port)
        trojan = Trojan(self.url.username, vBase)

        return trojan
