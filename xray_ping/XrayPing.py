import json
import time
from random import randint
import subprocess
from threading import Thread
from pathlib import Path

import requests

from XrayInbound import *
from XrayRouting import *
from XrayConfig import XrayConfigSimple


def real_delay(port: int, proxy_name: str):
    test_url = 'http://detectportal.firefox.com/success.txt'
    err_403_url = 'https://open.spotify.com/'
    proxy = "socks5://127.0.0.1:{}".format(port)
    delay = -1
    statusCode = -1
    try:
        start_time = time.time()
        requests.get(test_url, timeout=10, proxies=dict(http=proxy, https=proxy))
        end_time = time.time()
        delay = end_time - start_time
        err_403_res = requests.get(err_403_url, timeout=10, proxies=dict(http=proxy, https=proxy))
        statusCode = err_403_res.status_code
    except:
        pass
    print(f"Delay of {proxy_name}: {delay} seconds ")

    return dict(proxy=proxy_name, realDelay_ms=round(delay if delay <= 0 else delay * 1000), is403=(statusCode == 403))


def appendBypassMode(config: XrayConfigSimple) -> XrayConfigSimple:
    inbounds = [Inbound(
        "bypass_mode_43583495349",
        3080,
        "0.0.0.0",
        "socks",
        Sniffing(),
        SocksSettings()
    )] + config.inbounds
    outbounds = [{'tag': 'direct-out_095667567568', 'protocol': 'freedom'}] + config.outbounds
    rules = [Rule(
        "bypass_mode_43583495349",
        "direct-out_095667567568",
        []
    )] + config.routing.rules
    print(config.outbounds)

    route = XrayRouting(
        "IPIfNonMatch",
        "hybrid",
        rules
    )
    return XrayConfigSimple(inbounds, outbounds, route)


class XrayPing:
    result: list[dict] = []
    actives: list[dict] = []
    realDelay_under_1000: list[dict] = []
    realDelay_under_1500: list[dict] = []
    no403_realDelay_under_1000: list[dict] = []

    def __init__(self, configs: list[str], limit: int = 200) -> None:
        confs: list[dict] = [json.loads(c) for c in configs]

        socks = []
        rules = []
        # just to make sure there is no duplicated port :|
        socksPorts = list(set([randint(2000, 49999) for _ in range(len(confs) * 2)]))

        for index, outbound in enumerate(confs):
            socksInbound = Inbound(
                "socks__" + outbound["tag"],
                socksPorts[index],
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

        xrayConfig = appendBypassMode(XrayConfigSimple(socks, confs, route))

        confFinalStr = json.dumps(xrayConfig, default=lambda x: x.__dict__)

        configFilePath = "./xray_config_ping.json"
        with open(configFilePath, 'w') as f:
            f.write(confFinalStr)

        runXrayThread = Thread(target=subprocess.run,
                               args=([Path("xray_ping/xray").resolve(), "run", "-c", configFilePath],))
        runXrayThread.daemon = True
        runXrayThread.start()
        # runXrayThread.join()

        time.sleep(5)

        if real_delay(3080, "bypass_mode")["realDelay_ms"] < 0:
            print("***************************************************************************")
            print(confFinalStr)
            raise Exception("Created config is incorrect! it's printed above")

        proxiesSorted = []
        for index, s in enumerate(socks):
            proxiesSorted.append(real_delay(s.port, s.tag.split("__")[1]))
        proxiesSorted = sorted(proxiesSorted, key=lambda d: d['realDelay_ms'])

        for index, r in enumerate(proxiesSorted):

            r["proxy"] = confs[index]
            self.result.append(r)
            if r["realDelay_ms"] > 0 and len(self.actives) < limit:
                self.actives.append(r)

            if 1000 >= r['realDelay_ms'] > 0 and len(self.realDelay_under_1000) < limit:
                self.realDelay_under_1000.append(r)
                if not r["is403"]:
                    self.no403_realDelay_under_1000.append(r)

            if 1500 >= r['realDelay_ms'] > 0  and len(self.realDelay_under_1500) < limit:
                self.realDelay_under_1500.append(r)
