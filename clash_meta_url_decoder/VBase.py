import re
from random import randint


def generateName(name):
    return "proxy_" + str(randint(1111, 9999999)) + "_" + re.sub(r'([/:+])+', '', name[:120])


class VBase:
    name: str
    type: str
    port: int
    server: str

    def __init__(self, type: str, name: str, server: str, port: int) -> None:
        self.server = server
        self.name = name #generateName(name)
        self.type = type
        self.port = port
