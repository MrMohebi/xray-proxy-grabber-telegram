import json
import sys
import yaml
from gitRepo import commitPushRActiveProxiesFile, getLatestActiveConfigs

sys.path.append('./xray_url_decoder/')
sys.path.append('./clash_meta_url_decoder/')
sys.path.append('./xray_ping/')

from xray_url_decoder.XrayUrlDecoder import XrayUrlDecoder
from xray_ping.XrayPing import XrayPing
from clash_meta_url_decoder.ClashMetaUrlDecoder import ClashMetaDecoder


def is_good_for_game(config: XrayUrlDecoder):
    return (config.type in ['tcp', 'grpc']) and (config.security in [None, "tls"])


# for more info, track this issue https://github.com/MetaCubeX/Clash.Meta/issues/801
def is_buggy_in_clash_meta(config: ClashMetaDecoder):
    return config.security == "reality" and config.type == "grpc"


with open("collected-proxies/row-url/all.txt", 'r') as rowProxiesFile:
    configs = []
    clash_meta_configs = []
    for_game_proxies = []
    for url in rowProxiesFile:
        if len(url) > 10:
            try:
                # ############# xray ############
                c = XrayUrlDecoder(url)
                c_json = c.generate_json_str()
                if c.isSupported and c.isValid:
                    configs.append(c_json)

                # ############# clash Meta ##########
                ccm = ClashMetaDecoder(url)
                ccm_json = ccm.generate_obj_str()
                if c.isSupported and c.isValid and (not is_buggy_in_clash_meta(ccm)):
                    clash_meta_configs.append(json.loads(ccm_json))

                if is_good_for_game(c):
                    for_game_proxies.append(url)
            except:
                print("There is error with this proxy => " + url)

    # getLatestGoodForGame()
    # with open("collected-proxies/row-url/for_game.txt", 'w') as forGameProxiesFile:
    #     for forGame in for_game_proxies:
    #         forGameProxiesFile.write(forGame)
    # commitPushForGameProxiesFile()

    delays = XrayPing(configs)
    getLatestActiveConfigs()

    with open("collected-proxies/clash-meta/all.yaml", 'w') as allClashProxiesFile:
        yaml.dump({"proxies": clash_meta_configs}, allClashProxiesFile, Dumper=yaml.BaseDumper)

    with open("collected-proxies/xray-json/actives_all.txt", 'w') as activeProxiesFile:
        for active in delays.actives:
            activeProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("collected-proxies/xray-json/actives_under_1000ms.txt", 'w') as active1000ProxiesFile:
        for active in delays.realDelay_under_1000:
            active1000ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("collected-proxies/xray-json/actives_under_1500ms.txt", 'w') as active1500ProxiesFile:
        for active in delays.realDelay_under_1500:
            active1500ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("collected-proxies/xray-json/actives_no_403_under_1000ms.txt", 'w') as active1000no403ProxiesFile:
        for active in delays.no403_realDelay_under_1000:
            active1000no403ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("collected-proxies/xray-json/actives_for_ir_server_no403_u1s.txt",
              'w') as active1000no403ForServerProxiesFile:
        for active in delays.no403_realDelay_under_1000:
            if active['proxy']["streamSettings"]["network"] not in ["ws", "grpc"]:
                active1000no403ForServerProxiesFile.write(json.dumps(active['proxy']) + "\n")

commitPushRActiveProxiesFile()
