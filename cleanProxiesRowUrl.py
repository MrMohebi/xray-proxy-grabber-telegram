import json
from urllib.parse import urlparse

from gitRepo import getLatestActiveConfigs, getLatestRowProxies, commitPushRowProxiesFile


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

        activeConfigObj = json.loads(activeConfig)
        # TODO: only supports vless by now!
        with open("./proxies_row_url.txt", 'r') as rowProxiesFile:
            for (index, rowProxyUrl) in enumerate(rowProxiesFile):
                if activeConfigObj["settings"]["vnext"][0]["users"][0]["id"] == urlparse(rowProxyUrl).username and activeConfigObj["settings"]["vnext"][0]["port"] == urlparse(rowProxyUrl).port and activeConfigObj["settings"]["vnext"][0]["address"] == urlparse(rowProxyUrl).hostname:
                    lineNumberOfFounds.append(index + 1)

keep_only_lines_and_remove_duplicates("./proxies_row_url.txt", lineNumberOfFounds)

commitPushRowProxiesFile("------cleaning url list-------")
