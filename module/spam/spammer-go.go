package main

import (
	"C"
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net/http"
	"net/url"
	"strings"
	"sync"
	"time"
)

func main() {
	// main関数を記述
	send_requests()
}

//export send_requests
func send_requests() {
	var wg sync.WaitGroup

	for i := 0; i < 25; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()

			for {
				sendRequest("https://discord.com/api/v9/channels/1189118504809529375/messages")
			}
		}()
	}

	wg.Wait()
}

func sendRequest(url string) {
	proxy := getRandomProxy()

	headers := map[string]string{
		"Accept":             "*/*",
		"Accept-Encoding":    "gzip, deflate, br",
		"Accept-Language":    "en-US",
		"Authorization":      getRandomToken(),
		"Connection":         "keep-alive",
		"Content-Type":       "application/json",
		"Host":               "discord.com",
		"Origin":             "https://discord.com",
		"Pragma":             "no-cache",
		"Sec-Fetch-Dest":     "empty",
		"Sec-Fetch-Mode":     "cors",
		"Sec-Fetch-Site":     "same-origin",
		"sec-ch-ua-platform": "Windows",
		"sec-ch-ua-mobile":   "?0",
		"TE":                 "Trailers",
	}

	postData := map[string]interface{}{
		"content": "<@1188845591439081551> Hello, Discord!",
	}

	postJSON, err := json.Marshal(postData)
	if err != nil {
		fmt.Println("JSON marshal error:", err)
		return
	}

	client := &http.Client{
		Transport: &http.Transport{
			Proxy: http.ProxyURL(proxy),
		},
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(postJSON))
	if err != nil {
		fmt.Println("Request error:", err)
		return
	}

	for key, value := range headers {
		req.Header.Set(key, value)
	}

	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Request error:", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode == 200 {
		fmt.Println("Success:", resp.StatusCode, proxy)
	} else {
		fmt.Println("Failed:", resp.StatusCode, proxy)
	}
}

func getRandomToken() string {
	tokens := readTokensFromFile("token.txt")
	if len(tokens) == 0 {
		fmt.Println("No tokens found in token.txt")
		return ""
	}

	rand.Seed(time.Now().UnixNano())
	return tokens[rand.Intn(len(tokens))]
}

func readTokensFromFile(filename string) []string {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return nil
	}

	return strings.Fields(string(content))
}

func getRandomProxy() *url.URL {
	proxies := readProxiesFromFile("proxies.txt")
	if len(proxies) == 0 {
		fmt.Println("No proxies found in proxies.txt")
		return nil
	}

	rand.Seed(time.Now().UnixNano())
	return proxies[rand.Intn(len(proxies))]
}

func readProxiesFromFile(filename string) []*url.URL {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return nil
	}

	lines := strings.Split(string(content), "\n")
	var proxyList []*url.URL

	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line != "" {
			proxyURL, err := url.Parse("http://" + line)
			if err != nil {
				fmt.Println("Error parsing proxy URL:", err)
			} else {
				proxyList = append(proxyList, proxyURL)
			}
		}
	}

	return proxyList
}