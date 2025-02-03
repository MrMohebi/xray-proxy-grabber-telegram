import shutil
from gitRepo import getLatestRowProxies, commitPushRowProxiesFile

with open("collected-proxies/row-url/all.txt", 'r') as rowProxiesFile:
    if len(rowProxiesFile.readlines()) < 400:
        print("row proxies count(under 400) => ", rowProxiesFile.readlines())
        exit(0)


getLatestRowProxies()

shutil.copyfile("collected-proxies/row-url/actives.txt", "collected-proxies/row-url/all.txt")

commitPushRowProxiesFile("------cleaning all row url list base on actives-------")
