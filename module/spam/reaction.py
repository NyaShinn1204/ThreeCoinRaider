import random
import re
import threading
import time
import json
import emoji as ej
import urllib
import urllib.parse
from httpx import Client
from httpx_socks import SyncProxyTransport

import bypass.header as header

def extract(format_token):
    if re.compile(r"(.+):").match(format_token):
        return format_token.split(":")[1]
    else:
        token = format_token
    return token

def start(delay, tokens, module_status, proxysetting, proxies, proxytype, channelid, messageid, emoji):
    for token in tokens:
        threading.Thread(target=req_reaction, args=(token, module_status, proxysetting, proxies, proxytype, channelid, messageid, emoji)).start()
        time.sleep(float(delay))
    
def req_reaction(token, module_status, proxysetting, proxies, proxytype, channelid, messageid, emoji):
    req_header = header.request_header(token)
    headers = req_header
    extract_token = f"{extract(token+']').split('.')[0]}.{extract(token+']').split('.')[1]}"
    emoji2 = urllib.parse.quote_plus(ej.emojize(emoji,language='alias'))
    try:
        request = Client()
        if proxysetting == True:
            proxy = random.choice(proxies)
            request = Client(transport=SyncProxyTransport.from_url(f'{proxytype}://{proxy}'))
        x = request.put(f"https://discord.com/api/v9/channels/{channelid}/messages/{messageid}/reactions/{emoji2}/%40me", headers=headers)
        if x.status_code == 204:
            if proxysetting == True:
                print(f"[+] 付与に成功しました ChannelID: {channelid} Token: {extract_token}.******** Proxy: {proxy}")
            else:
                print(f"[+] 付与に成功しました ChannelID: {channelid} Token: {extract_token}.********")
            module_status(2, 4, 1)
        else:
            if x.status_code == 429 or x.status_code == 20016:
                print("[-] RateLimit!! "+x.json()["retry_after"])
            elif x.status_code == 403:
                print("[-] Token Not Join!! "+x.json())
            else:
                if proxysetting == True:
                    print(f"[-] 付与に失敗しました ChannelID: {channelid} Token: {extract_token}.******** Proxy: {proxy}")
                else:
                    print(f"[-] 付与に失敗しました ChannelID: {channelid} Token: {extract_token}.********")
            module_status(2, 4, 2)
    except:
        pass