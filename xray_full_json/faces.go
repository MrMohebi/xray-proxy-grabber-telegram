package main

type RoutingFile struct {
	Routing struct {
		DomainStrategy string `json:"domainStrategy"`
		DomainMatcher  string `json:"domainMatcher"`
		Balancers      []struct {
			Tag      string   `json:"tag"`
			Selector []string `json:"selector"`
			Strategy struct {
				Type string `json:"type"`
			} `json:"strategy"`
		} `json:"balancers"`
		Rules []struct {
			InboundTag  []string `json:"inboundTag"`
			Domain      []any    `json:"domain,omitempty"`
			BalancerTag string   `json:"balancerTag,omitempty"`
			Type        string   `json:"type"`
			OutboundTag string   `json:"outboundTag,omitempty"`
			IP          []string `json:"ip,omitempty"`
		} `json:"rules"`
	} `json:"routing"`
	BurstObservatory struct {
		SubjectSelector []string `json:"subjectSelector"`
		PingConfig      struct {
			Destination  string `json:"destination"`
			Interval     string `json:"interval"`
			Connectivity string `json:"connectivity"`
			Timeout      string `json:"timeout"`
			Sampling     int    `json:"sampling"`
		} `json:"pingConfig"`
	} `json:"burstObservatory"`
}

type OutboundConfigBase struct {
	Tag      string `json:"tag"`
	Protocol string `json:"protocol"`
}

type InboundFile struct {
	Inbounds []Inbound `json:"inbounds"`
}

type Inbound struct {
	Listen   string      `json:"listen"`
	Port     int         `json:"port"`
	Protocol string      `json:"protocol"`
	Settings interface{} `json:"settings,omitempty"`
	Sniffing Sniffing    `json:"sniffing,omitempty"`
	Tag      string      `json:"tag"`
}

type Sniffing struct {
	DestOverride []string `json:"destOverride"`
	Enabled      bool     `json:"enabled"`
}

type SettingsSocks struct {
	Auth      string          `json:"auth"`
	Accounts  []BasicAccounts `json:"accounts"`
	UDP       bool            `json:"udp"`
	UserLevel int             `json:"userLevel"`
}

type SettingsHttp struct {
	Accounts  []BasicAccounts `json:"accounts"`
	UserLevel int             `json:"userLevel"`
}

type BasicAccounts struct {
	User string `json:"user"`
	Pass string `json:"pass"`
}
