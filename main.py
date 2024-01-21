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
#import module.token_checker as token_checker
#import module.proxy_checker as proxy_checker

# Bypass Module Import
#import bypass.solver.solver as solver
#import bypass.solver.get_balance as get_balance
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

root = tk.Tk()
root.geometry("1280x720")
root.resizable(0, 0)
root.title("ThreeCoinRaider | "+version)
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(data=get_icon.get_window_icon()))
root.configure(bg="#fff")

#import Variable
from data.settings import Setting

#Set language

language = json.load(open('./config.json', 'r', encoding="utf-8"))["language"]

lang_load = json.load(open('./data/language.json', 'r', encoding="utf-8"))

def lang_load_set(name):
  return lang_load[language][name]

set_font = (lang_load[language]["font"], 16, "bold")
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

def clear_frame(frame):
  for widget in frame.winfo_children():
    widget.destroy()
  frame.pack_forget()

def module_scroll_frame(num1, num2):
  global module_frame
  frame_scroll = module_frame = ctk.CTkScrollableFrame(root, fg_color=c2, bg_color=c2, width=1000, height=630)
  module_frame.place(x=245, y=70)
  clear_frame(frame_scroll)
  if num1 == 1:
    if num2 == 1:
  
      printl("debug", "Open Join Leave Tab")
        
    if num2 == 2:
        
      printl("debug", "Open Spammer Tab")
        
  if num1 == 2:
    if num2 == 1:
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
      ctk.CTkOptionMenu(modules_frame10_01, width=508, height=25, corner_radius=4, values=["English | EN", "Japanese | JP"], fg_color=c1, button_color=c1, button_hover_color=c1, dropdown_fg_color=c1, dropdown_hover_color=c12, dropdown_text_color="#fff", font=("Roboto", 12, "bold"), dropdown_font=("Roboto", 12, "bold"), command=set_config, variable=Setting.language_variable).place(x=5,y=55)
      tk.Label(modules_frame10_01, bg="#010b32", fg="#fff", text="Language", font=("Roboto", 11, "bold")).place(x=0,y=30)
      
      
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
      
      
      # Frame Numnber 10_04
      modules_frame10_04 = ctk.CTkFrame(module_frame, width=470, height=210, border_width=0, fg_color="#010b32")
      modules_frame10_04.grid(row=1, column=1, padx=6, pady=6)
      tk.Label(modules_frame10_04, bg="#010b32", fg="#fff", text="Proxies", font=("Roboto", 12, "bold")).place(x=15,y=0)
      tk.Canvas(modules_frame10_04, bg=c6, highlightthickness=0, height=4, width=470).place(x=0, y=25)
      
      printl("debug", "Open Setting Tab")
        
    if num2 == 2:
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
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/join_leave.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("joiner_leaver"), width=195, height=40, font=set_font, anchor="w", command= lambda: module_scroll_frame(1, 1)).place(x=20,y=12)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/join_leave.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("spammer"), width=195, height=40, font=set_font, anchor="w", command= lambda: module_scroll_frame(1, 2)).place(x=20,y=57)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/join_leave.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("soon"), width=195, height=40, font=set_font, anchor="w").place(x=20,y=102)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/join_leave.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("soon"), width=195, height=40, font=set_font, anchor="w").place(x=20,y=148)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/join_leave.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("soon"), width=195, height=40, font=set_font, anchor="w").place(x=20,y=194)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/join_leave.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("soon"), width=195, height=40, font=set_font, anchor="w").place(x=20,y=240)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/setting.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("settings"), width=195, height=40, font=set_font, anchor="w", command= lambda: module_scroll_frame(2, 1)).place(x=20,y=286)
  ctk.CTkButton(master=modulelist, image=ctk.CTkImage(Image.open("data/info.png"),size=(20, 20)), compound="left", fg_color=c4, hover_color=c5, corner_radius=0, text=lang_load_set("about"), width=195, height=40, font=set_font, anchor="w", command= lambda: module_scroll_frame(2, 2)).place(x=20,y=332)
  
  credit_frame = ctk.CTkFrame(root, width=1020, height=50, fg_color=c1, bg_color=c2)
  credit_frame.place(x=245, y=10)
  ctk.CTkButton(master=credit_frame, image=ctk.CTkImage(Image.open("data/link.png"),size=(20, 20)), compound="right", fg_color=c1, text_color="#fff", corner_radius=0, text="", width=20, height=20, font=set_font, anchor="w", command= lambda: CTkMessagebox(title="Version Info", message=f"Version: {version}\n\nDeveloper: {developer}\nTester: {testers}", width=450)).place(x=10,y=10)
  ctk.CTkLabel(master=credit_frame, fg_color=c1, text_color="#fff", corner_radius=0, text=lang_load_set("username")+": "+os.getlogin(), width=20, height=20, font=set_font, anchor="w").place(x=40,y=5)
  ctk.CTkLabel(master=credit_frame, fg_color=c1, text_color="#fff", corner_radius=0, text="Hwid: "+get_hwid(), width=20, height=20, font=set_font, anchor="w").place(x=40,y=25)

# Load First
logo = f"""
       &#BB#&   
     B?^:::^~?B   _______ _                    _____      _       _____       _     _           
    P^:::^^^^^^P |__   __| |                  / ____|    (_)     |  __ \     (_)   | |          
    J~~^^~~~~~~J    | |  | |__  _ __ ___  ___| |     ___  _ _ __ | |__) |__ _ _  __| | ___ _ __ 
    B7~!!~~~!~7B    | |  | '_ \| '__/ _ \/ _ \ |    / _ \| | '_ \|  _  // _` | |/ _` |/ _ \ '__|
     #5J7777J55     | |  | | | | | |  __/  __/ |___| (_) | | | | | | \ \ (_| | | (_| |  __/ |   
       &&&&&&&      |_|  |_| |_|_|  \___|\___|\_____\___/|_|_| |_|_|  \_\__,_|_|\__,_|\___|_|   
                                          This Software was OSS
"""
print(Colorate.Horizontal(Colors.cyan_to_blue, logo, 1))
print(f"""
You HWID: [{get_hwid()}]                Version: [{version}]
-----------------------"""
)

# Load Menu
printl("debug", "Loading Tkinter")
module_list_frame()
module_scroll_frame(2,2)

root.mainloop()