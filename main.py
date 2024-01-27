#import data.icon as get_icon
#import tkinter as tk 
#root = tk.Tk() 
#root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(data=get_icon.get_window_icon()))
#root.mainloop()
#
import os
import time
import json
import threading
import webbrowser
import subprocess
import requests
import colorama
import tkinter as tk
import customtkinter as ctk
from PIL import Image
from pystyle import *
from colorama import Fore
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from CTkToolTip import *

# Data Module Import
import data.icon as get_icon

# Module Import

import module.spam.spammer_go as module_go_spammer
import module.spam.spammer as module_normal_spammer
#import module.joiner as module_joiner
#import module.leaver as module_leaver
#import module.spam.spammer as module_spammer
#import module.vc_join as module_vc_join
#import module.spam.reply as module_reply
#import module.spam.ticket as module_ticket
#import module.spam.reaction as module_reaction
#import module.spam.threads as module_threads
#import module.spam.pusher as module_pusher

# Utilities Module Import
import module.token_checker as token_checker
import module.proxy_checker as proxy_checker

# Bypass Module Import
#import bypass.solver.solver as solver
import module.joiner.utilities.get_balance as get_balance

version = "1.0.0"
theme = "twocoin"
developer = "NyaShinn1204"
contributors = "None"
testers = "None"

def get_filename():
  return os.path.basename(__file__)

def printl(num, data):
  if num == "error":
    print(f"[{Fore.LIGHTRED_EX}Error{Fore.RESET}] [{get_filename()}] " + data)
  if num == "debug":
    print(f"[{Fore.LIGHTCYAN_EX}Debug{Fore.RESET}] [{get_filename()}] " + data)
  if num == "info":
    print(f"[{Fore.LIGHTGREEN_EX}Info{Fore.RESET}] [{get_filename()}] " + data)
    
def extractfi(input_str):
  if len(input_str) >= 5:
    replaced_str = input_str[:-5] + '*' * 5
    return replaced_str
  else:
    return input_str

c1 = "#0D2845"
c2 = "#020b1f"
c3 = "#0a2b63"
c4 = "#020b1f"
c5 = "#00bbe3"
c6 = "#0a2b63"
c7 = "#000117"
c8 = "#489ea1"
c9 = "#454c7f"
c10 = "#2D2DA0"
c11 = "#041432"
c12 = "#3a88e3"
c13 = "#010b32"

root = tk.Tk()
root.geometry("1280x720")
root.resizable(0, 0)
root.title("ThreeCoinRaider | "+version)
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(data=get_icon.get_window_icon()))
root.configure(bg="#fff")

#import Variable
from data.settings import Setting, SettingVariable

#Set language

language = json.load(open('./config.json', 'r', encoding="utf-8"))["language"]

lang_load = json.load(open('./data/language.json', 'r', encoding="utf-8"))

def lang_load_set(name):
  return lang_load[language][name]

def set_fonts(size, mode):
  if mode == None:
    return (lang_load[language]["font"], size)
  else:
    return (lang_load[language]["font"], size, "bold")
Setting.language_variable.set(lang_load[language]["name"])

def get_hwid():
  try:
    if os.name == 'posix':
      uuid = "Linux unsupported"
      return uuid
    else:
      cmd = 'wmic csproduct get uuid'
      uuid = str(subprocess.check_output(cmd))
      pos1 = uuid.find("\\n")+2
      uuid = uuid[pos1:-15]
      return uuid
  except:
    printl("error", "get_hwid error wrong")


# load Check Def
def check_config():
  printl("debug", "Checking Config")
  try:
    if os.path.exists(r"config.json") and not json.load(open('./config.json', 'r', encoding="utf-8"))["token_path"] == "":
      tokens = open(json.load(open('./config.json', 'r', encoding="utf-8"))["token_path"], 'r').read().splitlines()
      Setting.tokens = []
      Setting.validtoken = 0
      Setting.invalidtoken = 0
      Setting.token_filenameLabel.set(os.path.basename(json.load(open('./config.json', 'r', encoding="utf-8"))["token_path"]))
      Setting.totaltokenLabel.set("Total: "+str(len(tokens)).zfill(3))
      threading.Thread(target=token_checker.check(tokens, update_token)).start()
      printl("info", "Checked Config")
    else:
      printl("error", "Config Not Found")
      printl("error", "Please point to it manually.")
      token_load()
  except Exception as error:
    printl("error", "Config Check Error")
    printl("error", error)
    token_load()

# Token Tab
def token_load():
  filepath = filedialog.askopenfilename(filetype=[("", "*.txt")], initialdir=os.path.abspath(os.path.dirname(__file__)), title="Select Tokens")
  if filepath == "":
    return
  tokens = open(filepath, 'r').read().splitlines()
  if tokens == []:
    return
  data = json.load(open('config.json'))
  data['token_path'] = filepath
  json.dump(data, open('config.json', 'w'), indent=4)
  printl("info", f"Set Token File {os.path.basename(filepath)}")
  Setting.tokens = []
  Setting.validtoken = 0
  Setting.invalidtoken = 0
  Setting.token_filenameLabel.set(os.path.basename(filepath))
  Setting.validtokenLabel.set("Valid: 000")
  Setting.invalidtokenLabel.set("Invalid: 000")
  Setting.totaltokenLabel.set("Total: "+str(len(tokens)).zfill(3))
  threading.Thread(target=token_checker.check(tokens, update_token)).start()

def update_token(status, token):
  if status == True:
    Setting.tokens.append(token)
    Setting.validtoken += 1
    Setting.validtokenLabel.set("Valid: "+str(Setting.validtoken).zfill(3))
  if status == False:
    Setting.invalidtoken += 1
    Setting.invalidtokenLabel.set("Invalid: "+str(Setting.invalidtoken).zfill(3))

# Proxy Tab
def proxy_load():
  threading.Thread(target=proxy_main).start()
  
def proxy_main():
  proxy_type = Setting.proxytype.get()
  print(proxy_type)
  if proxy_type == "":
    print("[-] Cancel proxy")
    return
  proxy_filepath()

def proxy_filepath():
  filepath = filedialog.askopenfilename(filetype=[("", "*.txt")], initialdir=os.path.abspath(os.path.dirname(__file__)), title="Select Proxies")
  if filepath == "":
    return
  proxies = open(filepath, 'r').read().splitlines()
  if proxies == []:
    return
  data = json.load(open('config.json'))
  data['proxie_path'] = filepath
  json.dump(data, open('config.json', 'w'), indent=4)
  printl("info", f"Set Proxie File {os.path.basename(filepath)}")
  Setting.proxies = []
  Setting.totalproxies = str(len(proxies))
  Setting.vaildproxies = 0
  Setting.invaildproxies = 0
  Setting.proxy_filenameLabel.set(os.path.basename(filepath))
  Setting.totalProxiesLabel.set("Total: "+Setting.totalproxies.zfill(3))
  print("[+] Load: " + Setting.totalproxies + "Proxies")
  time.sleep(1)
  threading.Thread(target=proxy_checker.check(update_proxy, proxies, Setting.proxytype.get()))
  if Setting.vaildproxies == 0:
    printl("error","Not Found Load Vaild Proxies")
  else:
    printl("info","Success Load Vaild Proxies: " + str(Setting.vaildproxies))
     
def update_proxy(status, proxy):
  if status == True:
    Setting.proxies.append(proxy)
    Setting.vaildproxies += 1
    Setting.validProxiesLabel.set("Valid: "+str(Setting.vaildproxies).zfill(3))
  if status == False:
    Setting.invaildproxies += 1
    Setting.invalidProxiesLabel.set("Invalid: "+str(Setting.invaildproxies).zfill(3))

def module_thread(num1, num2, num3):
  tokens = Setting.tokens
  proxies = Setting.proxies
  proxytype = Setting.proxytype.get()
  proxysetting = Setting.proxy_enabled.get()
  delay = 0.1
  mentions = 20
  if num1 == 2:
    if num2 == 1:
      if num3 == 1:
        serverid = str(Setting.nmspam_serverid.get())
        channelid = str(Setting.nmspam_channelid.get())
        allchannel = Setting.nmspam_allch.get()
        allping = Setting.nmspam_allping.get()
        randomstring = Setting.nmspam_rdstring.get()
        ratelimit = Setting.nmspam_ratefixer.get()
        randomconvert = Setting.nmspam_randomconvert.get()
    
        contents = nmspam_message.get("0.0","end-1c")
        #mentions = Setting.delay99_02.get()
    
        delay = Setting.nmspam_delay.get()
    
        if serverid == "":
          print("[-] ServerID is not set")
          return
        if channelid == "":
          print("[-] ChannelID is not set")
          return    
    
        threading.Thread(target=module_normal_spammer.start, args=(delay, tokens, module_status, proxysetting, proxies, proxytype, serverid, channelid, contents, allchannel, allping, mentions, randomstring, ratelimit, randomconvert)).start()

      if num3 == 2:
        threading.Thread(target=module_normal_spammer.stop).start()

    if num2 == 2:
      if num3 == 1:
        token_file = json.load(open('./config.json', 'r', encoding="utf-8"))["token_path"]
        proxie_file = json.load(open('./config.json', 'r', encoding="utf-8"))["proxie_path"]
        
        if proxie_file == "":
          print("This Module use Proxie.")
          return
        
        serverid = str(Setting.gospam_serverid.get())
        channelid = str(Setting.gospam_channelid.get())
        allchannel = Setting.gospam_allch.get()
        
        contents = gospam_message.get("0.0","end-1c")
        threads = round(Setting.gospam_threads.get())
            
        #if serverid == "":
        #  print("[-] ServerID is not set")
        #  return
        if channelid == "":
          print("[-] ChannelID is not set")
          return    
    
        threading.Thread(target=module_go_spammer.start, args=(token_file, proxie_file, module_status, serverid, channelid, contents, allchannel, threads)).start()

      if num3 == 2:
        threading.Thread(target=module_go_spammer.stop).start()

def module_status(num1, num2, num3):
  if num1 == 2:
    if num2 == 1:
      if num3 == 1:
        SettingVariable.nmspamresult_success +=1
        Setting.suc_nmspam_Label.set("Success: "+str(SettingVariable.nmspamresult_success).zfill(3))
      if num3 == 2:
        SettingVariable.nmspamresult_failed +=1
        Setting.fai_nmspam_Label.set("Failed: "+str(SettingVariable.nmspamresult_failed).zfill(3))
    if num2 == 2:
      if num3 == 1:
        SettingVariable.gospamresult_success +=1
        Setting.suc_gospam_Label.set("Success: "+str(SettingVariable.gospamresult_success).zfill(3))
      if num3 == 2:
        SettingVariable.gospamresult_failed +=1
        Setting.fai_gospam_Label.set("Failed: "+str(SettingVariable.gospamresult_failed).zfill(3))


def clear_frame(frame):
  for widget in frame.winfo_children():
    widget.destroy()
  frame.pack_forget()

def module_scroll_frame(num1, num2):
  global module_frame
  global nmspam_message, gospam_message
  frame_scroll = module_frame = ctk.CTkScrollableFrame(root, fg_color=c2, bg_color=c2, width=1000, height=630)
  module_frame.place(x=245, y=70)
  clear_frame(frame_scroll)
  if num1 == 1:
    if num2 == 1:
      # Join Leave
      # Frame Number 01_01
      def hcaptcha_select():
        global answers, api
        if Setting.joiner_bypasscap.get() == True:
          answers = ctk.CTkInputDialog(text = "Select Sovler\n1, CapSolver\n2, CapMonster\n3, 2Cap\n4, Anti-Captcha").get_input()
          if answers in ['1','2','3','4']:
            print("[+] Select " + answers)
            api = ctk.CTkInputDialog(text = "Input API Key").get_input()
            if api == "":
              print("[-] Not Set. Please Input")
              Setting.joiner_bypasscap.set(False)
            else:
              print("[~] Checking API Key: " + extractfi(api))
              if answers == "1":
                if get_balance.get_balance_capsolver(api) == 0.0:
                  Setting.joiner_bypasscap.set(False)
              if answers == "2":
                if get_balance.get_balance_capmonster(api) == 0.0:
                  Setting.joiner_bypasscap.set(False)
              if answers == "3":
                if get_balance.get_balance_2cap(api) == 0.0:
                  Setting.joiner_bypasscap.set(False)
              if answers == "4":
                if get_balance.get_balance_anticaptcha(api) == 0.0:
                  Setting.joiner_bypasscap.set(False)
          else:
            print("[-] Not Set. Please Input")
            Setting.joiner_bypasscap.set(False)

      modules_frame01_01 = ctk.CTkFrame(module_frame, width=470, height=275, border_width=0, fg_color=c13)
      modules_frame01_01.grid(row=0, column=0, padx=6, pady=6)
      tk.Label(modules_frame01_01, bg=c13, fg="#fff", text="Joiner", font=("Roboto", 12, "bold")).place(x=15,y=0)
      tk.Canvas(modules_frame01_01, bg=c6, highlightthickness=0, height=4, width=470).place(x=0, y=25)
      
      ctk.CTkCheckBox(modules_frame01_01, bg_color=c13, text_color="#fff", border_color=c3, checkbox_width=20, checkbox_height=20, hover=False, border_width=3, text="Bypass MemberScreen", variable=Setting.joiner_bypassms).place(x=5,y=31)
      test = ctk.CTkLabel(modules_frame01_01, text_color="#fff", text="(?)")
      test.place(x=170,y=31)
      CTkToolTip(test, delay=0.5, message="Bypass the member screen when you join.") 
      ctk.CTkCheckBox(modules_frame01_01, bg_color=c13, text_color="#fff", border_color=c3, checkbox_width=20, checkbox_height=20, hover=False, border_width=3, text="Bypass hCaptcha", variable=Setting.joiner_bypasscap, command=hcaptcha_select).place(x=5,y=55) 
      test = ctk.CTkLabel(modules_frame01_01, text_color="#fff", text="(?)")
      test.place(x=140,y=55)
      CTkToolTip(test, delay=0.5, message="Automatically resolve hcaptcha")
      ctk.CTkCheckBox(modules_frame01_01, bg_color=c13, text_color="#fff", border_color=c3, checkbox_width=20, checkbox_height=20, hover=False, border_width=3, text="Delete Join Message", variable=Setting.joiner_deletems).place(x=5,y=79)
      test = ctk.CTkLabel(modules_frame01_01, text_color="#fff", text="(?)")
      test.place(x=160,y=79)
      CTkToolTip(test, delay=0.5, message="Delete the message when you join") 
      
      ctk.CTkButton(modules_frame01_01, text="Clear        ", fg_color=c2, hover_color=c5, width=75, height=25, command=lambda: Setting.joiner_link.set("")).place(x=5,y=109)
      ctk.CTkEntry(modules_frame01_01, bg_color=c13, fg_color=c7, border_color=c4, text_color="#fff", width=150, height=20, textvariable=Setting.joiner_link).place(x=85,y=109)
      tk.Label(modules_frame01_01, bg=c13, fg="#fff", text="Invite Link", font=("Roboto", 12)).place(x=240,y=107)
      ctk.CTkButton(modules_frame01_01, text="Clear        ", fg_color=c2, hover_color=c5, width=75, height=25, command=lambda: Setting.joiner_serverid.set("")).place(x=5,y=138)
      ctk.CTkEntry(modules_frame01_01, bg_color=c13, fg_color=c7, border_color=c4, text_color="#fff", width=150, height=20, textvariable=Setting.joiner_serverid).place(x=85,y=138)
      tk.Label(modules_frame01_01, bg=c13, fg="#fff", text="Server ID", font=("Roboto", 12)).place(x=240,y=136)
      ctk.CTkButton(modules_frame01_01, text="Clear        ", fg_color=c2, hover_color=c5, width=75, height=25, command=lambda: Setting.joiner_channelid.set("")).place(x=5,y=167)
      ctk.CTkEntry(modules_frame01_01, bg_color=c13, fg_color=c7, border_color=c4, text_color="#fff", width=150, height=20, textvariable=Setting.joiner_channelid).place(x=85,y=167)
      tk.Label(modules_frame01_01, bg=c13, fg="#fff", text="Channel ID", font=("Roboto", 12)).place(x=240,y=165)

      CTkLabel(modules_frame01_01, text_color="#fff", text="Delay Time (s)", font=("Roboto", 15)).place(x=5,y=192)
      def show_value01_01(value):
          tooltip01_01.configure(message=round(value, 1))
      test = ctk.CTkSlider(modules_frame01_01, from_=0.1, to=3.0, variable=Setting.joiner_delay, command=show_value01_01)
      test.place(x=5,y=217)
      tooltip01_01 = CTkToolTip(test, message=round(Setting.joiner_delay.get(), 1))

      ctk.CTkButton(modules_frame01_01, text="Start", fg_color=c2, hover_color=c5, width=60, height=25, command=lambda: module_thread(1_1_1)).place(x=5,y=237)

      tk.Label(modules_frame01_01, bg=c13, fg="#fff", text="Join Status", font=("Roboto", 12)).place(x=205,y=190)
      tk.Label(modules_frame01_01, bg=c13, fg="#fff", textvariable=Setting.suc_joiner_Label, font=("Roboto", 12)).place(x=210,y=215)
      tk.Label(modules_frame01_01, bg=c13, fg="#fff", textvariable=Setting.fai_joiner_Label, font=("Roboto", 12)).place(x=210,y=240)
  
      printl("debug", "Open Join Leave Tab")
              
    if num2 == 2:
      # Spammer
      
      # Normal Spammer
      # Frame Number 02_01
      modules_frame02_01 = ctk.CTkFrame(module_frame, width=470, height=300, border_width=0, fg_color=c13)
      modules_frame02_01.grid(row=0, column=0, padx=6, pady=6)
      tk.Label(modules_frame02_01, bg=c13, fg="#fff", text="Normal Spammer", font=("Roboto", 12, "bold")).place(x=15,y=0)
      tk.Canvas(modules_frame02_01, bg=c6, highlightthickness=0, height=4, width=470).place(x=0, y=25)
      
      ctk.CTkCheckBox(modules_frame02_01, bg_color=c13, text_color="#fff", border_color=c3, checkbox_width=20, checkbox_height=20, hover=False, border_width=3, variable=Setting.nmspam_allping, text="All Ping").place(x=5,y=30)
      test = ctk.CTkLabel(modules_frame02_01, text_color="#fff", text="(?)")
      test.place(x=80,y=30)
      CTkToolTip(test, delay=0.5, message="Add a Mention to a random user to the message to be spammed") 
      ctk.CTkCheckBox(modules_frame02_01, bg_color=c13, text_color="#fff", border_color=c3, checkbox_width=20, checkbox_height=20, hover=False, border_width=3, variable=Setting.nmspam_allch, text="All Ch").place(x=5,y=52)
      test = ctk.CTkLabel(modules_frame02_01, text_color="#fff", text="(?)")
      test.place(x=70,y=52)
      CTkToolTip(test, delay=0.5, message="Randomly select channels to spam") 
      ctk.CTkCheckBox(modules_frame02_01, bg_color=c13, text_color="#fff", border_color=c3, checkbox_width=20, checkbox_height=20, hover=False, border_width=3, variable=Setting.nmspam_rdstring, text="Random String").place(x=5,y=74)
      test = ctk.CTkLabel(modules_frame02_01, text_color="#fff", text="(?)")
      test.place(x=120,y=74)
      CTkToolTip(test, delay=0.5, message="Adds a random string to the message to be spammed") 
      ctk.CTkCheckBox(modules_frame02_01, bg_color=c13, text_color="#fff", border_color=c3, checkbox_width=20, checkbox_height=20, hover=False, border_width=3, variable=Setting.nmspam_ratefixer, text="RateLimitFixer").place(x=5,y=96)
      test = ctk.CTkLabel(modules_frame02_01, text_color="#fff", text="(?)")
      test.place(x=120,y=96)
      CTkToolTip(test, delay=0.5, message="Wait a few seconds if the rate limit is reached") 
      ctk.CTkCheckBox(modules_frame02_01, bg_color=c13, text_color="#fff", border_color=c3, checkbox_width=20, checkbox_height=20, hover=False, border_width=3, variable=Setting.nmspam_randomconvert, text="RandomConvert").place(x=5,y=118)
      test = ctk.CTkLabel(modules_frame02_01, text_color="#fff", text="(?)")
      test.place(x=125,y=118)
      CTkToolTip(test, delay=0.5, message="Randomly converts messages to spam") 
      
      ctk.CTkButton(modules_frame02_01, text="Clear        ", fg_color=c2, hover_color=c5, width=75, height=25).place(x=5,y=146)
      ctk.CTkEntry(modules_frame02_01, bg_color=c13, fg_color=c4, border_color=c4, text_color="#fff", width=150, height=20, textvariable=Setting.nmspam_serverid).place(x=85,y=146)
      tk.Label(modules_frame02_01, bg=c13, fg="#fff", text="Server ID", font=("Roboto", 12)).place(x=240,y=144)
      ctk.CTkButton(modules_frame02_01, text="Clear        ", fg_color=c2, hover_color=c5, width=75, height=25).place(x=5,y=175)
      ctk.CTkEntry(modules_frame02_01, bg_color=c13, fg_color=c4, border_color=c4, text_color="#fff", width=150, height=20, textvariable=Setting.nmspam_channelid).place(x=85,y=175)
      tk.Label(modules_frame02_01, bg=c13, fg="#fff", text="Channel ID", font=("Roboto", 12)).place(x=240,y=173)


      CTkLabel(modules_frame02_01, text_color="#fff", text="Delay Time (s)", font=("Roboto", 15)).place(x=5,y=197)
      def show_value02_01(value):
          tooltip02_01.configure(message=round(value, 1))
      test = ctk.CTkSlider(modules_frame02_01, from_=0.1, to=3.0, variable=Setting.nmspam_delay, command=show_value02_01)
      test.place(x=5,y=222)
      tooltip02_01 = CTkToolTip(test, message=round(Setting.nmspam_delay.get(), 1))

      tk.Label(modules_frame02_01, bg=c13, fg="#fff", text="Message", font=("Roboto", 12)).place(x=150,y=30)
      nmspam_message = ctk.CTkTextbox(modules_frame02_01, bg_color=c13, fg_color=c4, text_color="#fff", width=250, height=75)
      nmspam_message.place(x=150,y=55)
        
      ctk.CTkButton(modules_frame02_01, text="Start", fg_color="#00051e", hover_color=c5, border_width=1, border_color="#00051e", width=60, height=25, command=lambda: module_thread(2, 1, 1)).place(x=5,y=245)
      ctk.CTkButton(modules_frame02_01, text="Stop", fg_color="#00051e", hover_color=c5, border_width=1, border_color="#00051e", width=60, height=25, command=lambda: module_thread(2, 1, 2)).place(x=70,y=245)

      tk.Label(modules_frame02_01, bg=c13, fg="#fff", text="Status", font=("Roboto", 12)).place(x=330,y=144)
      tk.Label(modules_frame02_01, bg=c13, fg="#fff", textvariable=Setting.suc_nmspam_Label, font=("Roboto", 12)).place(x=335,y=169)
      tk.Label(modules_frame02_01, bg=c13, fg="#fff", textvariable=Setting.fai_nmspam_Label, font=("Roboto", 12)).place(x=335,y=194)
        
      # Go Spammer
      # Frame Number 02_02
      modules_frame02_02 = ctk.CTkFrame(module_frame, width=470, height=300, border_width=0, fg_color=c13)
      modules_frame02_02.grid(row=0, column=1, padx=6, pady=6)
      tk.Label(modules_frame02_02, bg=c13, fg="#fff", text="Go Spammer", font=("Roboto", 12, "bold")).place(x=15,y=0)
      tk.Canvas(modules_frame02_02, bg=c6, highlightthickness=0, height=4, width=470).place(x=0, y=25)
    
      ctk.CTkCheckBox(modules_frame02_02, bg_color=c13, text_color="#fff", border_color=c3, checkbox_width=20, checkbox_height=20, hover=False, border_width=3, variable=Setting.gospam_allch, text="All Ch").place(x=5,y=30)
      test = ctk.CTkLabel(modules_frame02_02, text_color="#fff", text="(?)")
      test.place(x=70,y=30)
      CTkToolTip(test, delay=0.5, message="Randomly select channels to spam") 
      
      ctk.CTkButton(modules_frame02_02, text="Clear        ", fg_color=c2, hover_color=c5, width=75, height=25).place(x=5,y=146)
      ctk.CTkEntry(modules_frame02_02, bg_color=c13, fg_color=c4, border_color=c4, text_color="#fff", width=150, height=20, textvariable=Setting.gospam_serverid).place(x=85,y=146)
      tk.Label(modules_frame02_02, bg=c13, fg="#fff", text="Server ID", font=("Roboto", 12)).place(x=240,y=144)
      ctk.CTkButton(modules_frame02_02, text="Clear        ", fg_color=c2, hover_color=c5, width=75, height=25).place(x=5,y=175)
      ctk.CTkEntry(modules_frame02_02, bg_color=c13, fg_color=c4, border_color=c4, text_color="#fff", width=150, height=20, textvariable=Setting.gospam_channelid).place(x=85,y=175)
      tk.Label(modules_frame02_02, bg=c13, fg="#fff", text="Channel ID", font=("Roboto", 12)).place(x=240,y=173)


      CTkLabel(modules_frame02_02, text_color="#fff", text="Threads", font=("Roboto", 15)).place(x=5,y=197)
      def show_value02_02(value):
          tooltip02_02.configure(message=round(value))
      test = ctk.CTkSlider(modules_frame02_02, from_=1, to=50, variable=Setting.gospam_threads, command=show_value02_02)
      test.place(x=5,y=222)
      tooltip02_02 = CTkToolTip(test, message=round(Setting.gospam_threads.get()))

      tk.Label(modules_frame02_02, bg=c13, fg="#fff", text="Message", font=("Roboto", 12)).place(x=150,y=30)
      gospam_message = ctk.CTkTextbox(modules_frame02_02, bg_color=c13, fg_color=c4, text_color="#fff", width=250, height=75)
      gospam_message.place(x=150,y=55)
        
      ctk.CTkButton(modules_frame02_02, text="Start", fg_color="#00051e", hover_color=c5, border_width=1, border_color="#00051e", width=60, height=25, command=lambda: module_thread(2, 2, 1)).place(x=5,y=245)
      ctk.CTkButton(modules_frame02_02, text="Stop", fg_color="#00051e", hover_color=c5, border_width=1, border_color="#00051e", width=60, height=25, command=lambda: module_thread(2, 2, 2)).place(x=70,y=245)

      tk.Label(modules_frame02_02, bg=c13, fg="#fff", text="Status", font=("Roboto", 12)).place(x=330,y=144)
      tk.Label(modules_frame02_02, bg=c13, fg="#fff", textvariable=Setting.suc_gospam_Label, font=("Roboto", 12)).place(x=335,y=169)
      tk.Label(modules_frame02_02, bg=c13, fg="#fff", textvariable=Setting.fai_gospam_Label, font=("Roboto", 12)).place(x=335,y=194)        

      printl("debug", "Open Spammer Tab")
        
  if num1 == 2:
    if num2 == 1:
      # Setting
      
      # Other
      # Frame Number 10_01
      modules_frame10_01 = ctk.CTkFrame(module_frame, width=470, height=210, border_width=0, fg_color="#010b32")
      modules_frame10_01.grid(row=0, column=0, padx=6, pady=6)
      tk.Label(modules_frame10_01, bg="#010b32", fg="#fff", text="Other", font=("Roboto", 12, "bold")).place(x=15,y=0)
      tk.Canvas(modules_frame10_01, bg=c6, highlightthickness=0, height=4, width=470).place(x=0, y=25)
      
      
      def set_config(value):
          data = json.load(open('config.json'))
          if value == "English | EN":
            lang = "en-us"
          if value == "Japanese | JP":
            lang = "ja-jp"
          data['language'] = lang
          json.dump(data, open('config.json', 'w'), indent=4)
      ctk.CTkOptionMenu(modules_frame10_01, width=450, height=25, corner_radius=4, values=["English | EN", "Japanese | JP"], fg_color=c1, button_color=c1, button_hover_color=c1, dropdown_fg_color=c1, dropdown_hover_color=c12, dropdown_text_color="#fff", font=("Roboto", 12, "bold"), dropdown_font=("Roboto", 12, "bold"), command=set_config, variable=Setting.language_variable).place(x=5,y=55)
      tk.Label(modules_frame10_01, bg="#010b32", fg="#fff", text=lang_load_set("language"), font=set_fonts(11, "bold")).place(x=0,y=30)
      
      # Coming Soon
      # Frame Number 10_02
      modules_frame10_02 = ctk.CTkFrame(module_frame, width=470, height=210, border_width=0, fg_color="#010b32")
      modules_frame10_02.grid(row=0, column=1, padx=6, pady=6)
      tk.Label(modules_frame10_02, bg="#010b32", fg="#fff", text="Coming Soon", font=("Roboto", 12, "bold")).place(x=15,y=0)
      tk.Canvas(modules_frame10_02, bg=c6, highlightthickness=0, height=4, width=470).place(x=0, y=25)


      # Frame Numnber 10_03
      modules_frame10_03 = ctk.CTkFrame(module_frame, width=470, height=210, border_width=0, fg_color="#010b32")
      modules_frame10_03.grid(row=1, column=0, padx=6, pady=6)
      tk.Label(modules_frame10_03, bg="#010b32", fg="#fff", text="Tokens", font=("Roboto", 12, "bold")).place(x=15,y=0)
      tk.Canvas(modules_frame10_03, bg=c6, highlightthickness=0, height=4, width=470).place(x=0, y=25)

      ctk.CTkButton(modules_frame10_03, text=lang_load_set("selectfile"), fg_color=c2, hover_color=c5, width=75, height=25, command=lambda: token_load(), font=set_fonts(12, None)).place(x=5,y=33)
      ctk.CTkEntry(modules_frame10_03, bg_color="#010b32", fg_color=c7, border_color=c4, text_color="#fff", width=150, height=20, state="disabled").place(x=85,y=33)
      ctk.CTkLabel(modules_frame10_03, bg_color="#010b32", fg_color=c4, text_color="#fff", text="", width=150, height=20, textvariable=Setting.token_filenameLabel).place(x=85,y=33)
      tk.Label(modules_frame10_03, bg="#010b32", fg="#fff", text=lang_load_set("filename"), font=set_fonts(12, None)).place(x=240,y=31)

      tk.Label(modules_frame10_03, bg="#010b32", fg="#fff", text="Status", font=("Roboto", 12)).place(x=5,y=70)
      tk.Label(modules_frame10_03, bg="#010b32", fg="#fff", text="Total: 000", font=("Roboto", 12), textvariable=Setting.totaltokenLabel).place(x=10,y=95)
      tk.Label(modules_frame10_03, bg="#010b32", fg="#fff", text="Valid: 000", font=("Roboto", 12), textvariable=Setting.validtokenLabel).place(x=10,y=115)
      tk.Label(modules_frame10_03, bg="#010b32", fg="#fff", text="Invalid: 000", font=("Roboto", 12), textvariable=Setting.invalidtokenLabel).place(x=10,y=135)
      
      
      # Frame Numnber 10_04
      modules_frame10_04 = ctk.CTkFrame(module_frame, width=470, height=210, border_width=0, fg_color="#010b32")
      modules_frame10_04.grid(row=1, column=1, padx=6, pady=6)
      tk.Label(modules_frame10_04, bg="#010b32", fg="#fff", text="Proxies", font=("Roboto", 12, "bold")).place(x=15,y=0)
      tk.Canvas(modules_frame10_04, bg=c6, highlightthickness=0, height=4, width=470).place(x=0, y=25)

      ctk.CTkCheckBox(modules_frame10_04, bg_color="#010b32", text_color="#fff", border_color=c3, checkbox_width=20, checkbox_height=20, hover=False, border_width=3, variable=Setting.proxy_enabled, text="Enabled").place(x=5,y=31)
      def set_socket(socks):
        Setting.proxytype.set(socks)
      ctk.CTkOptionMenu(modules_frame10_04, height=25, corner_radius=4, values=["http", "https", "socks4", "socks5"], fg_color=c1, button_color=c1, button_hover_color=c1, dropdown_fg_color=c1, dropdown_hover_color=c12, dropdown_text_color="#fff", font=("Roboto", 12, "bold"), dropdown_font=("Roboto", 12, "bold"), command=set_socket, variable=Setting.proxytype).place(x=5,y=57)
      

      
      tk.Label(modules_frame10_04, bg="#010b32", fg="#fff", text="Socket Type", font=("Roboto", 12)).place(x=150,y=55)
      ctk.CTkButton(modules_frame10_04, text="Select File", fg_color=c2, hover_color=c5, width=75, height=25, command=lambda: proxy_load()).place(x=5,y=90)
      ctk.CTkEntry(modules_frame10_04, bg_color="#010b32", fg_color=c7, border_color=c4, text_color="#fff", width=150, height=20, state="disabled").place(x=85,y=90)
      ctk.CTkLabel(modules_frame10_04, bg_color="#010b32", fg_color=c4, text_color="#fff", text="", width=150, height=20, textvariable=Setting.proxy_filenameLabel).place(x=85,y=90)
      tk.Label(modules_frame10_04, bg="#010b32", fg="#fff", text="File Name", font=("Roboto", 12)).place(x=240,y=87)
    
      tk.Label(modules_frame10_04, bg="#010b32", fg="#fff", text="Status", font=("Roboto", 12)).place(x=5,y=120)
      tk.Label(modules_frame10_04, bg="#010b32", fg="#fff", text="Total: 000", font=("Roboto", 12), textvariable=Setting.totalProxiesLabel).place(x=10,y=145)
      tk.Label(modules_frame10_04, bg="#010b32", fg="#fff", text="Valid: 000", font=("Roboto", 12), textvariable=Setting.validProxiesLabel).place(x=10,y=165)
      tk.Label(modules_frame10_04, bg="#010b32", fg="#fff", text="Invalid: 000", font=("Roboto", 12), textvariable=Setting.invalidProxiesLabel).place(x=10,y=185)
   
      
      printl("debug", "Open Setting Tab")
        
    if num2 == 2:
      # About
      credits_frame = ctk.CTkFrame(module_frame, width=940, height=400, border_width=0, fg_color=c2)
      credits_frame.grid(row=1, column=1, padx=6, pady=6)
      tk.Label(credits_frame, bg=c2, fg=c8, text="ThreeCoinRaider github:", font=("Roboto", 12)).place(x=0,y=0)
      test = tk.Label(credits_frame, bg=c2, fg=c9, text="Github link", font=("Roboto", 12, "underline"))
      test.place(x=175,y=0)
      test.bind("<Button-1>", lambda e:webbrowser.open_new("https://github.com/NyaShinn1204/ThreeCoinRaider"))
      tk.Label(credits_frame, bg=c2, fg=c8, text="ThreeCoinRaider discord:", font=("Roboto", 12)).place(x=0,y=25)
      test = tk.Label(credits_frame, bg=c2, fg=c9, text="Discord invite link", font=("Roboto", 12, "underline"))
      test.place(x=180,y=25)
      test.bind("<Button-1>", lambda e:webbrowser.open_new("https://discord.gg/4AZNXaCVHv"))
      tk.Label(credits_frame, bg=c2, fg="#fff", text="Main developer and updater:", font=("Roboto", 12)).place(x=0,y=50)
      tk.Label(credits_frame, bg=c2, fg=c10, text=developer, font=("Roboto", 12)).place(x=210,y=50)
      tk.Label(credits_frame, bg=c2, fg="#fff", text="Main contributors:", font=("Roboto", 12)).place(x=0,y=75)
      tk.Label(credits_frame, bg=c2, fg=c10, text=contributors, font=("Roboto", 12)).place(x=137,y=75)
      tk.Label(credits_frame, bg=c2, fg="#fff", text="Main testers:", font=("Roboto", 12)).place(x=0,y=100)
      tk.Label(credits_frame, bg=c2, fg=c10, text=testers, font=("Roboto", 12)).place(x=100,y=100)
      
      tk.Label(credits_frame, bg=c2, fg="#fff", text="Respect:", font=("Roboto", 12)).place(x=0,y=150)
      tk.Label(credits_frame, bg=c2, fg=c10, text="Akebi GC", font=("Roboto", 12)).place(x=15,y=170)
      tk.Label(credits_frame, bg=c2, fg=c10, text="Bkebi GC", font=("Roboto", 12)).place(x=15,y=190)
      tk.Label(credits_frame, bg=c2, fg=c10, text="TwoCoinRaider", font=("Roboto", 12)).place(x=15,y=210)

      printl("debug", "Open About Tab")

def module_list_frame():
  global modulelist
  tk.Label(root, bg=c2, width=1024, height=720).place(x=0,y=0)
  tk.Label(root, bg=c4, width=32, height=720).place(x=0,y=0)
  tk.Label(root, bg=c4, text="THREECOIN RAIDER", fg="#fff", font=("Carlito", 20, "bold")).place(x=5,y=25)
  
  modulelist = ctk.CTkFrame(master=root, width=230, height=720, corner_radius=0, fg_color=c4)
  modulelist.place(x=0,y=100)
  tk.Canvas(bg=c6, highlightthickness=0, height=2080, width=4).place(x=230, y=0)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/join_leave.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("joiner_leaver"), width=195, height=40, font=set_fonts(16, "bold"), anchor="w", command= lambda: module_scroll_frame(1, 1)).place(x=20,y=12)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/spammer.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("spammer"), width=195, height=40, font=set_fonts(16, "bold"), anchor="w", command= lambda: module_scroll_frame(1, 2)).place(x=20,y=57)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/join_leave.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("soon"), width=195, height=40, font=set_fonts(16, "bold"), anchor="w").place(x=20,y=102)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/join_leave.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("soon"), width=195, height=40, font=set_fonts(16, "bold"), anchor="w").place(x=20,y=148)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/join_leave.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("soon"), width=195, height=40, font=set_fonts(16, "bold"), anchor="w").place(x=20,y=194)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/join_leave.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("soon"), width=195, height=40, font=set_fonts(16, "bold"), anchor="w").place(x=20,y=240)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/setting.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("settings"), width=195, height=40, font=set_fonts(16, "bold"), anchor="w", command= lambda: module_scroll_frame(2, 1)).place(x=20,y=286)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/info.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("about"), width=195, height=40, font=set_fonts(16, "bold"), anchor="w", command= lambda: module_scroll_frame(2, 2)).place(x=20,y=332)
  
  credit_frame = ctk.CTkFrame(root, width=1020, height=50, fg_color=c1, bg_color=c2)
  credit_frame.place(x=245, y=10)
  ctk.CTkButton(master=credit_frame, image=ctk.CTkImage(Image.open("data/link.png"),size=(20, 20)), compound="right", fg_color=c1, text_color="#fff", corner_radius=0, text="", width=20, height=20, font=set_fonts(16, None), anchor="w", command= lambda: CTkMessagebox(title="Version Info", message=f"Version: {version}\n\nDeveloper: {developer}\nTester: {testers}", width=450)).place(x=10,y=10)
  ctk.CTkLabel(master=credit_frame, fg_color=c1, text_color="#fff", corner_radius=0, text=lang_load_set("username")+": "+os.getlogin(), width=20, height=20, font=set_fonts(16, "bold"), anchor="w").place(x=40,y=5)
  ctk.CTkLabel(master=credit_frame, fg_color=c1, text_color="#fff", corner_radius=0, text="Hwid: "+get_hwid(), width=20, height=20, font=set_fonts(16, "bold"), anchor="w").place(x=40,y=25)

# Load First
logo = f"""
       &#BB#&   
     B?^:::^~?B        _______ _                    _____      _       _____       _     _           
    P^:::^^^^^^P      |__   __| |                  / ____|    (_)     |  __ \     (_)   | |          
    J~~^^~~~~~~J         | |  | |__  _ __ ___  ___| |     ___  _ _ __ | |__) |__ _ _  __| | ___ _ __ 
    B7~!!~~~!~7B         | |  | '_ \| '__/ _ \/ _ \ |    / _ \| | '_ \|  _  // _` | |/ _` |/ _ \ '__|
     #5J7777J55          | |  | | | | | |  __/  __/ |___| (_) | | | | | | \ \ (_| | | (_| |  __/ |   
       &&&&&&&           |_|  |_| |_|_|  \___|\___|\_____\___/|_|_| |_|_|  \_\__,_|_|\__,_|\___|_|   
                                    :skull:  Proudly Free, Never For Free  :skull:
"""
print(Colorate.Horizontal(Colors.cyan_to_blue, logo, 1))
print(f"""
You HWID: [{get_hwid()}]                Version: [{version}]
-----------------------"""
)

# Load Menu
check_config()
printl("debug", "Loading Tkinter")
module_list_frame()
module_scroll_frame(2,2)

root.mainloop()