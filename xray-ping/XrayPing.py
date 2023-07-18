import json
import time
from random import randint
import subprocess
from threading import Thread

import requests

from XrayInbound import *
from XrayRouting import *
from XrayConfig import XrayConfigSimple


def real_delay(port: int, proxy_name: str):
    test_url = 'https://guthib.com/'
    proxy = "socks5://127.0.0.1:{}".format(port)
    delay = -1
    try:
        start_time = time.time()
        requests.get(test_url, timeout=10, proxies=dict(http=proxy,https=proxy))
        end_time = time.time()
        delay = end_time - start_time
    except:
        pass
    print(f"Delay of {proxy_name}: {delay} seconds ")

    return dict(proxyName=proxy_name, realDelay_ms=round(delay if delay <= 0 else delay*1000))


class XrayPing:
    result: list

    def __init__(self, configs: list[str]) -> None:
        confs = [json.loads(c) for c in configs]

        socks = []
        rules = []
        for outbound in confs:
            socksInbound = Inbound(
                "socks__" + outbound["tag"],
                randint(11111, 49999),
                "0.0.0.0",
                "socks",
                Sniffing(),
                SocksSettings()
            )
            rule = Rule(
                socksInbound.tag,
                outbound["tag"],
                []
            )

            socks.append(socksInbound)
            rules.append(rule)

        route = XrayRouting(
            "IPIfNonMatch",
            "hybrid",
            rules
        )

        xrayConfig = XrayConfigSimple(socks, confs, route)

        confFinalStr = json.dumps(xrayConfig, default=lambda x: x.__dict__)

        configFilePath = "./xray_config_ping.json"
        with open(configFilePath, 'w') as f:
            f.write(confFinalStr)

        runXrayThread = Thread(target=subprocess.run, args=(["./xray", "run", "-c", configFilePath],))
        runXrayThread.daemon = True
        runXrayThread.start()
        # runXrayThread.join()

        time.sleep(5)

        result = []
        for s in socks:
            result.append(real_delay(s.port, s.tag.split("__")[1]))

        print(result)

x = [
    '{"tag": "proxy_7799", "protocol": "vless", "settings": {"vnext": [{"address": "init1984-mtn.linuxmember.online", "port": 2087, "users": [{"id": "c3f0e733-40d1-41d9-afe6-75029a13a418", "alterId": 0, "email": "t@t.tt", "security": "auto", "encryption": "none", "flow": ""}]}]}, "streamSettings": {"network": "grpc", "security": "tls", "tlsSettings": {"serverName": "inittes.parsiran.top", "rejectUnknownSni": false, "allowInsecure": false, "alpn": ["h2", "http/1.1"], "minVersion": "1.1", "maxVersion": "1.3", "cipherSuites": "", "certificates": [], "disableSystemRoot": false, "enableSessionResumption": false, "fingerprint": "chrome", "pinnedPeerCertificateChainSha256": [""]}, "grpcSettings": {"serviceName": "@init1984", "multiMode": false, "idleTimeout": 60, "healthCheckTimeout": 20, "permitWithoutStream": false, "initialWindowsSize": 0}}, "mux": {"enabled": false, "concurrency": -1}}',
    '{"tag": "proxy_9182", "protocol": "vless", "settings": {"vnext": [{"address": "cljoon.wtf-broo.ir", "port": 2087, "users": [{"id": "86dee03e-8119-4215-e719-279602c5a366", "alterId": 0, "email": "t@t.tt", "security": "auto", "encryption": "none", "flow": ""}]}]}, "streamSettings": {"network": "ws", "security": "tls", "tlsSettings": {"serverName": "cljoon.wtf-broo.ir", "rejectUnknownSni": false, "allowInsecure": false, "alpn": ["h2", "http/1.1"], "minVersion": "1.1", "maxVersion": "1.3", "cipherSuites": "", "certificates": [], "disableSystemRoot": false, "enableSessionResumption": false, "fingerprint": "chrome", "pinnedPeerCertificateChainSha256": [""]}, "wsSettings": {"path": "/", "headers": {}}}, "mux": {"enabled": false, "concurrency": -1}}',
    '{"tag": "proxy_1903", "protocol": "vless", "settings": {"vnext": [{"address": "levi.wtf-broo.ir", "port": 57356, "users": [{"id": "1fbe1e72-1a3b-4b75-dce5-5598631f7efc", "alterId": 0, "email": "t@t.tt", "security": "auto", "encryption": "none", "flow": ""}]}]}, "streamSettings": {"network": "grpc", "security": "reality", "realitySettings": {"serverName": "telewebion.com", "publicKey": "sq7N8HmEL1cPskTNP4h5M31BqAoeIQ76bBcCDh9fKQc", "fingerprint": "chrome", "show": false, "shortId": "", "spiderX": "/"}, "grpcSettings": {"serviceName": "", "multiMode": false, "idleTimeout": 60, "healthCheckTimeout": 20, "permitWithoutStream": false, "initialWindowsSize": 0}}, "mux": {"enabled": false, "concurrency": -1}}',
    '{"tag": "proxy_9324", "protocol": "vless", "settings": {"vnext": [{"address": "me.gymbroo.xyz", "port": 7575, "users": [{"id": "825560ab-6b2c-4605-9f23-7d88df39e3d2", "alterId": 0, "email": "t@t.tt", "security": "auto", "encryption": "none", "flow": ""}]}]}, "streamSettings": {"network": "tcp", "security": "none", "tcpSettings": {"acceptProxyProtocol": false}}, "mux": {"enabled": false, "concurrency": -1}}']

c = XrayPing(x)
