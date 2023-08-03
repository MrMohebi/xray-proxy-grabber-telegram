from XrayRouting import *
from XrayInbound import *


class XrayConfigSimple:
    policy: dict
    log: dict
    inbounds: List[Inbound]
    outbounds: List[dict]
    stats: dict
    routing: XrayRouting

    def __init__(self, inbounds: List[Any], outbounds: List[dict], routing: XrayRouting, stats: dict = None,
                 policy: dict = None, log: dict = None) -> None:
        self.policy = policy if policy is not None else {
            "system": {
                "statsOutboundUplink": True,
                "statsOutboundDownlink": True
            }
        }
        self.log = log if log is not None else {
            "access": "",
            "error": "",
            "loglevel": "warning"
        }
        self.inbounds = inbounds
        self.outbounds = outbounds
        self.stats = stats
        self.routing = routing
