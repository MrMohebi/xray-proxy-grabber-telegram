import uuid
from curses.ascii import isalnum

from xray_url_decoder.XraySetting import TLSSettings, RealitySettings
from xray_url_decoder.vless import UserVless, VnextVless


def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


def isValid_link(username: str, address: str, port: int) -> bool:
    if is_valid_uuid(username):
        return True

    return False


def isValid_tls(config: TLSSettings) -> bool:
    return True
    # if config.serverName is not None and len(config.serverName):
    #     pass
    #
    # return False


def isValid_reality(config: RealitySettings) -> bool:
    if config.serverName is not None and config.publicKey is not None and len(config.serverName) > 2 and len(
            config.publicKey) > 2 and (config.shortId is "" or isalnum(config.shortId)):
        return True

    return False


def isValid_userVless(config: UserVless) -> bool:
    if config.id is not None and len(config.id) > 2:
        return True

    return False


def isValid_vnextVless(config: VnextVless) -> bool:
    if config.address is not None and config.port is not None and len(config.address) > 2 and config.port > 0 and len(
            config.users) > 0:
        return True

    return False
