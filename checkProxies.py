import json
import sys
import uuid
import subprocess
from ruamel.yaml import YAML
from gitRepo import commitPushRActiveProxiesFile, getLatestActiveConfigs
import consts

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
                cusTag = uuid.uuid4().hex

                # ############# xray ############
                c = XrayUrlDecoder(url, cusTag)
                c_json = c.generate_json_str()
                if c.isSupported and c.isValid:
                    configs.append(c_json)

                # ############# clash Meta ##########
                ccm = ClashMetaDecoder(url, cusTag)
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

    delays = XrayPing(configs, 200)
    getLatestActiveConfigs()

    yaml = YAML()
    with open("collected-proxies/clash-meta/all.yaml", 'w') as allClashProxiesFile:
        yaml.dump({"proxies": clash_meta_configs}, allClashProxiesFile)

    with open("collected-proxies/clash-meta/actives_under_1000ms.yaml", 'w') as active1000ClashProxiesFile:
        values_to_filter = {d['proxy']['tag'].split("_@_")[0] for d in delays.realDelay_under_1000}
        filtered_array = [item for item in clash_meta_configs if item['name'].split("_@_")[0] in values_to_filter]
        yaml.dump({"proxies": filtered_array}, active1000ClashProxiesFile)

    with open("collected-proxies/clash-meta/actives_under_1500ms.yaml", 'w') as active1500ClashProxiesFile:
        values_to_filter = {d['proxy']['tag'].split("_@_")[0] for d in delays.realDelay_under_1500}
        filtered_array = [item for item in clash_meta_configs if item['name'].split("_@_")[0] in values_to_filter]
        yaml.dump({"proxies": filtered_array}, active1500ClashProxiesFile)

    with open(consts.xrayJsonPath["active"]["all"], 'w') as activeProxiesFile:
        for active in delays.actives:
            activeProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open(consts.xrayJsonPath["active"]["under1000ms"], 'w') as active1000ProxiesFile:
        for active in delays.realDelay_under_1000:
            active1000ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open(consts.xrayJsonPath["active"]["under1500ms"], 'w') as active1500ProxiesFile:
        for active in delays.realDelay_under_1500:
            active1500ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open(consts.xrayJsonPath["active"]["no403under1000ms"], 'w') as active1000no403ProxiesFile:
        for active in delays.no403_realDelay_under_1000:
            active1000no403ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    for key in consts.xrayJsonPath["active"]:
        subprocess.call([
            consts.xrayFullJsonExePath,
            "-source",
            consts.xrayJsonPath["active"][key],
            "-output",
            consts.xrayJsonFullPath["active"][key],
            "-templates-path",
            consts.xrayFullJsonTemplatesPath
        ])




commitPushRActiveProxiesFile()
