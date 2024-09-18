package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"
)

// nodemon --exec go run . --signal SIGTERM

func main() {
	var (
		source        = flag.String("source", "https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/xray-json/actives_no_403_under_1000ms.txt", "xray json file source which contains outbound jsons, see default file for example")
		outputFile    = flag.String("output", "./result.json", "combined json file output")
		authUser      = flag.String("auth-user", "", "user for inbound auth - leave it blank for no auth")
		authPass      = flag.String("auth-pass", "", "password for inbound auth - leave it blank for no auth")
		templatesPath = flag.String("templates-path", "./default_template_configs", "path to template files")
		help          = flag.Bool("help", false, "Display help message")
	)

	flag.Parse()

	if *help {
		flag.Usage()
		os.Exit(0)
	}

	var (
		routingPath   = filepath.Join(*templatesPath, "routing.json")
		outboundsPath = filepath.Join(*templatesPath, "outbounds.json")
		inboundsPath  = filepath.Join(*templatesPath, "inbounds.json")
		basePath      = filepath.Join(*templatesPath, "base.json")
	)

	configBases, configsStr, err := getProxies(*source)
	if err != nil {
		log.Fatalln(err)
	}

	var outboundTags []string
	for _, configBase := range configBases {
		if configBase.Tag != "direct-out" {
			outboundTags = append(outboundTags, configBase.Tag)
		}
	}

	err = os.WriteFile(outboundsPath, []byte("{\"outbounds\":"+configsStr+"}"), 0644)
	if err != nil {
		log.Fatalf("failed writing to outboundsFile: %s", err)
	}

	println("updated " + outboundsPath)

	routing := getRouting(routingPath)
	for index, balancer := range routing.Routing.Balancers {
		if balancer.Tag == "public-proxies" {
			routing.Routing.Balancers[index].Selector = outboundTags
			routing.BurstObservatory.SubjectSelector = outboundTags
		}
	}

	routingStr, err := json.Marshal(routing)
	if err != nil {
		log.Fatalln(err)
	}
	err = os.WriteFile(routingPath, routingStr, 0644)
	if err != nil {
		log.Fatalf("failed writing to routingFile: %s", err)
	}
	println("updated " + routingPath)

	if len(*authUser) > 0 && len(*authPass) > 0 {
		inbounds := getInbounds(inboundsPath)

		for i := 0; i < len(inbounds); i++ {
			if inbounds[i].Protocol == "socks" {
				inbounds[i].Listen = "0.0.0.0"
				inbounds[i].Settings = SettingsSocks{
					Auth: "password",
					Accounts: []BasicAccounts{
						{
							User: *authUser,
							Pass: *authPass,
						},
					},
					UDP:       true,
					UserLevel: 8,
				}

			}
			if inbounds[i].Protocol == "http" {
				inbounds[i].Listen = "0.0.0.0"
				inbounds[i].Settings = SettingsHttp{
					Accounts: []BasicAccounts{
						{
							User: *authUser,
							Pass: *authPass,
						},
					},
					UserLevel: 8,
				}
				inbounds[i].Sniffing = Sniffing{
					DestOverride: []string{},
					Enabled:      false,
				}
			}
		}

		inboundsStr, err := json.Marshal(InboundFile{Inbounds: inbounds})
		if err != nil {
			log.Fatalln(err)
		}
		err = os.WriteFile(inboundsPath, inboundsStr, 0644)
		if err != nil {
			log.Fatalf("failed writing to file: %s", err)
		}

	} else {
		println("no auth provided. so inbound will be accessible from 127.0.0.1 with no auth")
	}

	err = mergeJSONFiles([]string{basePath, inboundsPath, outboundsPath, routingPath}, *outputFile)
	if err != nil {
		log.Fatal(err)
	}
}

func mergeJSONFiles(files []string, outputFile string) error {
	var mergedData interface{}

	for _, file := range files {
		fileData, err := ioutil.ReadFile(file)
		if err != nil {
			return err
		}
		var currentData interface{}
		err = json.Unmarshal(fileData, &currentData)
		if err != nil {
			return err
		}
		mergedData = merge(mergedData, currentData)
	}
	mergedBytes, err := json.MarshalIndent(mergedData, "", "  ")
	if err != nil {
		return err
	}
	err = ioutil.WriteFile(outputFile, mergedBytes, 0644)
	if err != nil {
		return err
	}

	return nil
}

func merge(a, b interface{}) interface{} {
	switch a := a.(type) {
	case map[string]interface{}:
		b := b.(map[string]interface{})
		for k, v := range b {
			if existingValue, ok := a[k]; ok {
				a[k] = merge(existingValue, v)
			} else {
				a[k] = v
			}
		}
		return a
	case []interface{}:
		b := b.([]interface{})
		return append(a, b...)
	default:
		return b
	}
}

func getRouting(filePath string) RoutingFile {
	jsonFile, err := os.Open(filePath)
	if err != nil {
		fmt.Println(err)
	}
	defer jsonFile.Close()
	byteValue, _ := ioutil.ReadAll(jsonFile)

	var result RoutingFile
	err = json.Unmarshal(byteValue, &result)
	if err != nil {
		fmt.Println(err)
	}
	return result
}

func getInbounds(filePath string) []Inbound {
	jsonFile, err := os.Open(filePath)
	if err != nil {
		fmt.Println(err)
	}
	defer jsonFile.Close()
	byteValue, _ := ioutil.ReadAll(jsonFile)

	var result InboundFile
	err = json.Unmarshal(byteValue, &result)
	if err != nil {
		fmt.Println(err)
	}
	return result.Inbounds
}

func getProxies(path string) ([]OutboundConfigBase, string, error) {
	var proxies string

	if IsUrl(path) {
		resp, err := http.Get(path)
		if err != nil {
			return nil, "", err
		}
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			return nil, "", err
		}
		proxies = string(body)
	} else {
		fileData, err := ioutil.ReadFile(path)
		if err != nil {
			return nil, "", err
		}
		proxies = string(fileData)
	}

	proxies = "[" + strings.Trim(strings.Replace(proxies, "\n", ",", -1), ",") + ",{\"tag\": \"direct-out\",\"protocol\": \"freedom\"}]"

	var configs []OutboundConfigBase
	err := json.Unmarshal([]byte(proxies), &configs)
	if err != nil {
		return nil, "", err
	}

	println("Got new proxies from => " + path)

	return configs, proxies, nil
}

func IsUrl(str string) bool {
	u, err := url.Parse(str)
	return err == nil && u.Scheme != "" && u.Host != ""
}
