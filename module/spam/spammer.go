package main

import (
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
	url := "https://discord.com/api/v9/channels/1189118504809529375/messages"

	// WaitGroupを初期化
	var wg sync.WaitGroup

	// 200個のgoroutineを起動して並列にリクエストを送信
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()

			for {
				// ランダムにプロキシを選択
				sendRequest(url)

				// 少し待機
				//time.Sleep(time.Second * 5)
			}
		}()
	}

	// すべてのgoroutineが完了するのを待つ
	wg.Wait()
}

func sendRequest(url string) {
	// プロキシ情報の取得
	proxy := getRandomProxy()

	// 各ゴルーチンで異なるトークンを使用する
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

	// POSTデータの作成（適宜変更してください）
	postData := map[string]interface{}{
		"content": "Hello, Discord!",
	}

	// JSONに変換
	postJSON, err := json.Marshal(postData)
	if err != nil {
		fmt.Println("JSON marshal error:", err)
		return
	}

	// プロキシを使用してHTTPクライアントを作成
	client := &http.Client{
		Transport: &http.Transport{
			Proxy: http.ProxyURL(proxy),
		},
	}

	// POSTリクエストの作成
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(postJSON))
	if err != nil {
		fmt.Println("Request error:", err)
		return
	}

	// ヘッダーの設定
	for key, value := range headers {
		req.Header.Set(key, value)
	}

	// リクエストの送信
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Request error:", err)
		return
	}
	defer resp.Body.Close()

	// レスポンスの表示
	if resp.StatusCode == 200 {
		fmt.Println("Sushi:", resp.StatusCode, proxy)
	} else {
		fmt.Println("Failed:", resp.StatusCode, proxy)
	}
}

// token.txtからランダムにトークンを取得する関数
func getRandomToken() string {
	tokens := readTokensFromFile("token.txt")
	if len(tokens) == 0 {
		fmt.Println("No tokens found in token.txt")
		return ""
	}

	rand.Seed(time.Now().UnixNano())
	return tokens[rand.Intn(len(tokens))]
}

// token.txtからトークンを読み込む関数
func readTokensFromFile(filename string) []string {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return nil
	}

	return strings.Fields(string(content))
}

// proxies.txtからランダムにプロキシを取得する関数
func getRandomProxy() *url.URL {
	proxies := readProxiesFromFile("proxies.txt")
	if len(proxies) == 0 {
		fmt.Println("No proxies found in proxies.txt")
		return nil
	}

	rand.Seed(time.Now().UnixNano())
	return proxies[rand.Intn(len(proxies))]
}

// proxies.txtからプロキシを読み込む関数
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
