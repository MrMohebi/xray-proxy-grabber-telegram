from typing import List, Any


class Rule:
    inboundTag: str
    domain: List[Any]
    outboundTag: str
    type: str

    def __init__(self, inbound_tag: str, outbound_tag: str, domain: List[Any],  type: str = None) -> None:
        self.inboundTag = inbound_tag
        self.domain = domain
        self.outboundTag = outbound_tag
        self.type = type if type is not None else "field"


class XrayRouting:
    domainStrategy: str
    domainMatcher: str
    rules: List[Rule]

    def __init__(self, domain_strategy: str, domain_matcher: str, rules: List[Rule]) -> None:
        self.domainStrategy = domain_strategy
        self.domainMatcher = domain_matcher
        self.rules = rules
