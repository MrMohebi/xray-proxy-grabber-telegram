import json
import shutil
import sys
from urllib.parse import urlparse

sys.path.append('./xray_url_decoder/')

from gitRepo import getLatestActiveConfigs, getLatestRowProxies, commitPushRowProxiesFile
from xray_url_decoder.XrayUrlDecoder import XrayUrlDecoder


def is_duplicated_config(proxy: str, seen_lines: set[str]):
    isDuplicated = False

    configs: list[XrayUrlDecoder] = []
    for url in seen_lines:
        if len(url) > 10:
            try:
                configs.append(XrayUrlDecoder(url))
            except:
                pass

    try:
        c_str = XrayUrlDecoder(proxy).generate_json_str()
        for conf in configs:
            if conf.is_equal_to_config(c_str):
                isDuplicated = True
    except:
        pass

    return isDuplicated


def keep_only_lines_and_remove_duplicates(file_path, lines_to_keep):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if lines_to_keep is None:
        new_lines = lines
    else:
        lines_to_keep = set(lines_to_keep)  # Convert to a set for faster lookup
        new_lines = [line for i, line in enumerate(lines, start=1) if i in lines_to_keep]

    unique_lines = []
    seen_lines = set()
    for line in new_lines:
        if line not in seen_lines:
            if not is_duplicated_config(line, seen_lines):
                unique_lines.append(line)
            seen_lines.add(line)

    new_content = '\n'.join(line.rstrip() for line in unique_lines if line.strip())

    with open(file_path, 'w') as file:
        file.write(new_content)


getLatestActiveConfigs()
getLatestRowProxies()

lineNumberOfFounds = []
with open("collected-proxies/xray-json/actives_all.txt", 'r') as activeProxiesFile:
    for activeConfig in activeProxiesFile:
        if len(activeConfig) < 10: continue

        with open("collected-proxies/row-url/all.txt", 'r') as rowProxiesFile:
            # remove if it's not in active proxies
            for (index, rowProxyUrl) in enumerate(rowProxiesFile):
                if len(rowProxyUrl) < 10: continue

                try:
                    config = XrayUrlDecoder(rowProxyUrl)
                    if config.isSupported and config.isValid and config.is_equal_to_config(activeConfig):
                        lineNumberOfFounds.append(index + 1)
                except:
                    pass

shutil.copyfile("collected-proxies/row-url/all.txt", "collected-proxies/row-url/actives.txt")

keep_only_lines_and_remove_duplicates("collected-proxies/row-url/actives.txt", lineNumberOfFounds)
keep_only_lines_and_remove_duplicates("collected-proxies/row-url/all.txt", None)

commitPushRowProxiesFile("------cleaning url list-------")
