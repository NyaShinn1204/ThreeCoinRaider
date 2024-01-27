import time
import threading
import requests
import base64
import re
import os
from colorama import Fore

import bypass.header as header
import module.joiner.utilities.solver as solver

pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
gray = Fore.LIGHTBLACK_EX + Fore.WHITE

changenick = False

# Fix Nerd Code
# And Fix Can't use Captcha Solver
# Skkiding.. :sad:

def get_filename():
  return os.path.basename(__file__)    

def printl(num, data):
  if num == "error":
    print(f"[{Fore.LIGHTRED_EX}Error{Fore.RESET}] [{get_filename()}] " + data)
  if num == "info":
    print(f"[{Fore.LIGHTGREEN_EX}Info{Fore.RESET}] [{get_filename()}] " + data)
    
def start(tokens, serverid, invitelink, memberscreen, delay, module_status, answers, apis, bypasscaptcha, delete_joinms, join_channelid):
    for token in tokens:
        threading.Thread(target=joiner_thread, args=(token, serverid, invitelink, memberscreen, module_status, answers, apis, bypasscaptcha, delete_joinms, join_channelid)).start()
        time.sleep(float(delay))

def extract(format_token):
    if re.compile(r"(.+):").match(format_token):
        return format_token.split(":")[1]
    else:
        token = format_token
    return token

def accept_rules_bypass(token, requests, serverid):
    extract_token = f"{extract(token+']').split('.')[0]}.{extract(token+']').split('.')[1]}"
    session = header.get_session.get_session()
    req_header = header.request_header(token)
    headers = req_header
    if 'show_verification_form' in requests:
        bypass_rules = session.get(f"https://discord.com/api/v9/guilds/{serverid}/member-verification?with_guild=false", headers=headers).json()
        accept_rules = session.get(f"https://discord.com/api/v9/guilds/{serverid}/requests/@me", headers=headers, json=bypass_rules)
        if accept_rules.status_code == 201 or accept_rules.status_code == 204:
            printl("info", f"{pretty}Success MemberBypass {gray}| " + Fore.CYAN + extract_token + Fore.RESET)
            return
        else:
            printl("error", f"{pretty}Failed MemberBypass {gray}| " + Fore.CYAN + extract_token + Fore.RESET)
            print(accept_rules.text)
            
def change_nicker(token, serverid, nickname):
    extract_token = f"{extract(token+']').split('.')[0]}.{extract(token+']').split('.')[1]}"
    req_header = header.request_header(token)
    headers = req_header
    req = requests.patch(f"https://discord.com/api/v9/guilds/{serverid}/members/@me/nick", headers=headers,
        json={
            "nick": nickname
        }
    )
    if req.status_code == 200:
        print(f'Successfully Changed Nickname {gray}| ' + Fore.CYAN + extract_token + Fore.RESET)
    if req.status_code != 200:
        print(f'Error Changing Nickname {gray}| ' + Fore.CYAN + extract_token + Fore.RESET)

def delete_join_msg(token, join_channel_id):
    extract_token = f"{extract(token+']').split('.')[0]}.{extract(token+']').split('.')[1]}"
    req_header = header.request_header(token)
    headers = req_header
    messages = requests.get(f"https://discord.com/api/v9/channels/{join_channel_id}/messages?limit=100",headers=headers).json()
    for message in messages:
        bot_token_id = base64.b64decode(token.split(".")[0]+"==").decode()
        if message["content"] == "" and bot_token_id == message["author"]["id"]:
            deleted_join = requests.delete(f"https://discord.com/api/v9/channels/{join_channel_id}/messages/{message['id']}",headers=headers)
            if deleted_join.status_code == 204:
                printl("info", f"{pretty}Success Delete Join Message {gray}| " + Fore.CYAN + extract_token + Fore.RESET)
            else:
                printl("error", f"{pretty}Failed Delete Join Message {gray}| " + Fore.CYAN + extract_token + Fore.RESET)
                print(deleted_join.text)
            break
        
def joiner_thread(token, serverid, invitelink, memberscreen, module_status, answers, apis, bypasscaptcha, delete_joinms, join_channelid):
    extract_token = f"{extract(token+']').split('.')[0]}.{extract(token+']').split('.')[1]}"
    session = header.get_session.get_session()
    req_header = header.request_header_fingerprint(token)
    headers = req_header
    try:
        joinreq = session.post(f"https://discord.com/api/v9/invites/{invitelink}", headers=headers, json={})
        if joinreq.status_code == 400:
            if bypasscaptcha == True:
                printl("info", f"{pretty}Solving Captcha{gray} | " + Fore.GREEN + extract_token + Fore.RESET)
                payload = {
                    "captcha_key": solver.bypass_captcha(answers, token, "https://discord.com", joinreq.json()['captcha_sitekey'], apis)
                }
                newresponse = session.post(f"https://discord.com/api/v9/invites/{invitelink}", headers=headers, json=payload)
                if newresponse.status_code == 200:
                    if "captcha_key" not in newresponse.json():
                        if joinreq.json().get("message") == "The user is banned from this guild.":
                            printl("error", f"{pretty}サーバーからBANされています {gray}| " + Fore.CYAN + extract_token + Fore.RESET)
                            module_status(1, 1, 2)
                        if "You need to verify your account in order to perform this action." in newresponse.json():
                            printl("error", f"{pretty}認証が必要です {gray}| " + Fore.CYAN + extract_token + Fore.RESET)
                            module_status(1, 1, 2)
                        printl("info", f"{pretty}Successfully Token Join {gray}| " + Fore.CYAN + extract_token + Fore.RESET)
                        if delete_joinms == True:
                            printl("info", f"{pretty}Deleting Join Message {gray}| " + Fore.CYAN + extract_token + Fore.RESET)
                            delete_join_msg(token, join_channelid)
                        module_status(1, 1, 1)
                    if memberscreen == True:
                        accept_rules_bypass(token, joinreq.json(), joinreq.json()["guild"]["id"])
                    if changenick == True:
                        change_nicker(token, joinreq.json()["guild"]["id"], "みけねこ的うるはるしあ")
                else:
                    printl("error", f"{pretty}Failed Captcha Bypass {gray}| " + Fore.CYAN + extract_token + Fore.RESET+ " | " + newresponse.text.replace("\n", ""))
            else:
                if "captcha_key" in joinreq.json():
                    printl("error", f"{pretty}Failed Token Join (Captcha Wrong) {gray}| " + Fore.CYAN + extract_token + Fore.RESET)
                    print(joinreq.json())
                    module_status(1, 1, 2)
        if joinreq.status_code == 200:
            if "captcha_key" not in joinreq.json():
                if joinreq.json().get("message") == "The user is banned from this guild.":
                    printl("error", f"{pretty}サーバーからBANされています {gray}| " + Fore.CYAN + extract_token + Fore.RESET)
                    module_status(1, 1, 2)
                if "You need to verify your account in order to perform this action." in joinreq.json():
                    printl("error", f"{pretty}認証が必要です {gray}| " + Fore.CYAN + extract_token + Fore.RESET)
                    module_status(1, 1, 2)
                printl("info", f"{pretty}Successfully Token Join {gray}| " + Fore.CYAN + extract_token + Fore.RESET)
                if delete_joinms == True:
                    printl("info", f"{pretty}Deleting Join Message {gray}| " + Fore.CYAN + extract_token + Fore.RESET)
                    delete_join_msg(token, headers, join_channelid)
                module_status(1, 1, 1)
            if memberscreen == True:
                accept_rules_bypass(token, joinreq.json(), joinreq.json()["guild"]["id"])
            if changenick == True:
                delete_join_msg(token, joinreq.json()["guild"]["id"], "みけねこ的うるはるしあ")
    except Exception as err:
        print(f"[-] ERROR: {err} ")
        return