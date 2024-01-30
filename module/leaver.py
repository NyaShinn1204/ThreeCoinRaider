import requests
import time
import re
import os
import threading
from colorama import Fore

import bypass.header as header

status = True

def status():
    global status
    return status

def stop():
    global status
    status = False

def get_filename():
  return os.path.basename(__file__)    

def printl(num, data):
  if num == "error":
    print(f"[{Fore.LIGHTRED_EX}Error{Fore.RESET}] [{get_filename()}] " + data)
  if num == "info":
    print(f"[{Fore.LIGHTGREEN_EX}Info{Fore.RESET}] [{get_filename()}] " + data)

def extract(format_token):
    if re.compile(r"(.+):").match(format_token):
        return format_token.split(":")[1]
    else:
        token = format_token
    return token

def start(serverid, delay, tokens):
    for token in tokens:
        threading.Thread(target=leaver_thread, args=(serverid, token)).start()
        time.sleep(float(delay))
    
def leaver_thread(serverid, token):
    if status is False:
        return
    extract_token = f"{extract(token+']').split('.')[0]}.{extract(token+']').split('.')[1]}"
    session = header.get_session.get_session()
    req_header = header.request_header(token)
    headers = req_header
    try:
        if status is False:
            return
        x = session.delete(f"https://discord.com/api/v9/users/@me/guilds/{serverid}", headers=headers)
        if x.status_code == 204:
            printl("info", "[+] Success Leave: "+extract_token)
            return
        elif x.status_code == 403:
            printl("error", "[-] Failed Leave: "+extract_token)
            return
    except Exception:
        printl("error", "[-] Failed Leave: "+extract_token)
        return
