import subprocess
import re
import random
import threading

import module.spam.utilities.user_scrape as user_scrape

def start(token_file, proxie_file, tokens, module_status, serverid, channelid, contents, allchannel, allping, mentions, threads):
    global process
    users = ""
    print("Starting the process.")
    print(threads)
    if allping == True:
        users = user_scrape.get_members(serverid, channelid, random.choice(tokens))
        if users == None:
            print("[-] んーメンバーが取得できなかったっぽい token死なないように一回止めるね")
            return
        else:
            print(users)
    command = ['go', 'run', 'spammer_go.go', serverid, channelid, contents, f'{token_file}', f'{proxie_file}', f'{threads}', f'{allchannel}'] + users
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True, cwd=r"./module/spam/")
    monitor_thread = threading.Thread(target=monitor_process, args=(module_status, channelid))
    monitor_thread.start()

def stop():
    global process
    print("Stopping the process.")
    if process.poll() is None:
        process.terminate()

def monitor_process(module_status, channelid):
    global process
    while process.poll() is None:
        output = process.stdout.readline().strip()
        if output:
            matches = re.findall(r'\b\d+\b', output)
            if matches:
                channelid = matches[0]
            if 'Success' in output:
                print(f"[+] 送信に成功しました ChannelID: {channelid}")
                module_status(2, 2, 1)
            else:
                print(f"[-] 送信に失敗しました ChannelID: {channelid}")
                module_status(2, 2, 2)