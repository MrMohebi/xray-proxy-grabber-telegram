import json
import sys
from urllib.parse import urlparse

sys.path.append('./xray_url_decoder/')

from gitRepo import getLatestActiveConfigs, getLatestRowProxies, commitPushRowProxiesFile
from xray_url_decoder.XrayUrlDecoder import XrayUrlDecoder


def keep_only_lines_and_remove_duplicates(file_path, lines_to_keep):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    lines_to_keep = set(lines_to_keep)  # Convert to a set for faster lookup
    new_lines = [line for i, line in enumerate(lines, start=1) if i in lines_to_keep]

    unique_lines = []
    seen_lines = set()
    for line in new_lines:
        if line not in seen_lines:
            unique_lines.append(line)
            seen_lines.add(line)

    new_content = '\n'.join(line.rstrip() for line in unique_lines if line.strip())

    with open(file_path, 'w') as file:
        file.write(new_content)


getLatestActiveConfigs()
getLatestRowProxies()

lineNumberOfFounds = []
with open("./proxies_active.txt", 'r') as activeProxiesFile:
    for activeConfig in activeProxiesFile:
        if len(activeConfig) < 10: continue

        with open("./proxies_row_url.txt", 'r') as rowProxiesFile:
            for (index, rowProxyUrl) in enumerate(rowProxiesFile):
                try:
                    config = XrayUrlDecoder(rowProxyUrl)
                    if config.isSupported and config.isValid and config.is_equal_to_config(activeConfig):
                        lineNumberOfFounds.append(index + 1)
                except:
                    print("Error with these => ")
                    print(rowProxyUrl)
                    print(activeConfig)


keep_only_lines_and_remove_duplicates("./proxies_row_url.txt", lineNumberOfFounds)

commitPushRowProxiesFile("------cleaning url list-------")
