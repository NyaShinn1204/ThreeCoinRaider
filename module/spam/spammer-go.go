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
	"os"
	"strconv"
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
	args := os.Args[1:]
	serverid := args[0]
	channelid := args[1]
	contents := args[2]
	token_file := args[3]
	proxie_file := args[4]
	threads_str := args[5]
	threads, err := strconv.Atoi(threads_str)

	if err != nil {
		// エラー処理: 文字列を整数に変換できない場合の処理を追加してください
		fmt.Println("threadsの変換に失敗しました:", err)
		return
	}

	var wg sync.WaitGroup

	for i := 0; i < threads; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()

			for {
				sendRequest(fmt.Sprintf("https://discord.com/api/v9/channels/%s/messages", channelid), serverid, contents, token_file, proxie_file)
			}
		}()
	}

	wg.Wait()
}

func sendRequest(url string, serverid string, contents string, token_file string, proxie_file string) {
	proxy := getRandomProxy(proxie_file)

	headers := map[string]string{
		"Accept":             "*/*",
		"Accept-Encoding":    "gzip, deflate, br",
		"Accept-Language":    "en-US",
		"Authorization":      getRandomToken(token_file),
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
		"content": contents,
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

func getRandomToken(filepath string) string {
	tokens := readTokensFromFile(filepath)
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

func getRandomProxy(filepath string) *url.URL {
	proxies := readProxiesFromFile(filepath)
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
