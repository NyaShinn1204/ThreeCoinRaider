import subprocess
import signal
import threading

def start(channelid):
    global process
    print("Starting the process.")
    process = subprocess.Popen(['go', 'run', 'spammer-go.go', channelid], stdout=subprocess.PIPE, text=True, cwd=r"./module/spam/")
    monitor_thread = threading.Thread(target=monitor_process, args=(channelid,))
    monitor_thread.start()

def stop():
    global process
    print("Stopping the process.")
    if process.poll() is None:
        process.terminate()

def monitor_process(channelid):
    global process
    while process.poll() is None:
        output = process.stdout.readline().strip()
        if output:
            if 'Success' in output:
                print(f"[+] 送信に成功しました ChannelID: {channelid}")
            else:
                print(f"[-] 送信に失敗しました ChannelID: {channelid}")
