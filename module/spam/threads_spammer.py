import random
import string
import threading
import time
import json
import re
from httpx import Client
from httpx_socks import SyncProxyTransport

import bypass.header as header

status = True
timelock = False

def status():
    global status
    return status

def stop():
    global status
    status = False

def randomname(n):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(n))  

def extract(format_token):
    if re.compile(r"(.+):").match(format_token):
        return format_token.split(":")[1]
    else:
        token = format_token
    return token

def start(delay, tokens, module_status, proxysetting, proxies, proxytype, serverid, channelid, contents):
    global status
    global timelock
    status = True
    
    token = random.choice(tokens)
    
    print(token)
    print(serverid)
    
    while status is True:
        if status == False:
            break
        if timelock == True:
            print("[-] RateLimit Fixing...")
            time.sleep(8)
            print("[+] RateLimit Fixed")
            timelock = False
        threading.Thread(target=spammer_thread, args=(tokens, module_status, proxysetting, proxies, proxytype,
                        channelid, contents)).start()
        time.sleep(float(delay))
        
def spammer_thread(tokens, module_status, proxysetting, proxies, proxytype, channelid, contents):
    global status
    global timelock

    if timelock == True:
        return
    if status is False:
        return
    token = random.choice(tokens)
    content = contents
    if content == "":
        print("[-] メッセージが設定されていないので初期のメッセージを送信します")
        content = "ThreeCoinRaider On Top :skull:"
    data = {"name": content, "type": "11", "auto_archive_duration": "4320", "location": "Thread Browser Toolbar"}
    req_header = header.request_header(token)
    headers = req_header
    extract_token = f"{extract(token+']').split('.')[0]}.{extract(token+']').split('.')[1]}"
    try:
        if status is False:
            return
        request = Client()
        if proxysetting == True:
            proxy = random.choice(proxies)
            request = Client(transport=SyncProxyTransport.from_url(f'{proxytype}://{proxy}'))
        x = request.post(f"https://discord.com/api/v9/channels/{channelid}/threads", headers=headers, json=data)
        if x.status_code == 403:
            print(f"[-] このチャンネルで作成できません ChannelID: {channelid} Token: {extract_token}.******** Status: {x.status_code}")
            module_status(2, 3, 2)
        if x.status_code == 404:
            print(f"[-] このチャンネルは存在しません ChannelID: {channelid} Token: {extract_token}.******** Status: {x.status_code}")
            module_status(2, 3, 2)
        if x.status_code == 201:
            module_status(2, 3, 1)
            if proxysetting == True:
                print(f"[+] 作成に成功しました ChannelID: {channelid} Token: {extract_token}.******** Proxy: {proxy}")
            else:
                print(f"[+] 作成に成功しました ChannelID: {channelid} Token: {extract_token}.********")
        else:
            if x.status_code == 429 or x.status_code == 20016:
                print("[-] RateLimit!! Please Wait!! "+str(x.json()["retry_after"]))
            else:
                print("Unknown Error: Please Create Issue ", x.text, x.status_code)
            module_status(2, 3, 2)
    except Exception as error:
        print(error)
        pass