import shutil
from gitRepo import getLatestRowProxies, commitPushRowProxiesFile

with open("collected-proxies/row-url/all.txt", 'r') as rowProxiesFile:
    if len(rowProxiesFile.readlines()) < 1000:
        print("row proxies count(under 1000) => ", rowProxiesFile.readlines())
        exit(0)


getLatestRowProxies()

shutil.copyfile("collected-proxies/row-url/actives.txt", "collected-proxies/row-url/all.txt")

commitPushRowProxiesFile("------cleaning all row url list base on actives-------")
