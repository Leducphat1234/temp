from tkinter import messagebox
import pygame
import sys
import threading
import pystray
import PIL.Image
from datetime import datetime
from win10toast import ToastNotifier
from tkinter import *
import subprocess


filename = "screen.exe"
colorfile = "color.txt"
circlefile = "circle.txt"
bgcolorfile = "bgcolor.txt"
modefile = "mode.txt"
notification = ToastNotifier()

title = "Boring screen"


def main():

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode()
    pygame.display.set_caption(title)
    try:
        with open(colorfile, "x") as c:
            rainbowcolor = ["Red", "Orange", "Yellow",
                            "Green", "Blue", "Indigo", "Purple"]
            for i in range(len(rainbowcolor)):
                c.write(rainbowcolor[i] + "\n")
    except FileExistsError:
        pass
    try:
        with open(circlefile, "x") as cir:
            cir.write("radius: 10\n")
            cir.write("width: 10\n")
    except FileExistsError:
        pass
    try:
        with open(bgcolorfile, "x") as bg:
            bg.write("day: #ffffff\n")
            bg.write("night: #1e1e1e\n")
    except FileExistsError:
        pass
    try:
        with open(modefile, "x") as m:
            m.write("move")
    except FileExistsError:
        pass
    def checktime():
        with open(bgcolorfile, "r") as bg:
            bgcolor = bg.read().split()
            color_day = bgcolor[1]
            color_night = bgcolor[3]
        if datetime.now().hour >= 6 and datetime.now().hour < 18:
            return color_day
        else:
            return color_night
    a = 0
    screencolor = checktime()
    try: screen.fill(screencolor)
    except ValueError: messagebox.showerror("Screen", f"Invalid screen color\nYou can fix this by deleting the {bgcolorfile} file.")
    with open(modefile, "r") as m:
        modevalue = m.read().lower()
    if modevalue == "move":
        while True:
            with open(circlefile, "r") as cir:
                cir = cir.read().split()
                try:
                    radius = int(cir[1])
                    width = int(cir[3])
                except IndexError:
                    messagebox.showerror("Screen", f"Cannot read {circlefile} file\nYou can fix it by deleting the file.")
            with open(colorfile, "r") as f:
                color = f.read().split()
            checktime()
            if a > len(color) - 1:
                a = 0
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    screen.fill(screencolor)
            pygame.mouse.set_visible(False)
            mousex, mousey = pygame.mouse.get_pos()
            pygame.draw.circle(screen, pygame.Color(color[a]), (mousex, mousey), radius, width)
            a += 1
            pygame.display.flip()
            clock.tick(60)
    elif modevalue == "drag":
        while True:
            with open(circlefile, "r") as cir:
                cir = cir.read().split()
                try:
                    radius = int(cir[1])
                    width = int(cir[3])
                except IndexError:
                    messagebox.showerror("Screen", f"Cannot read {circlefile} file\nYou can fix it by deleting the file.")
            with open(colorfile, "r") as f:
                color = f.read().split()
            checktime()
            if a > len(color) - 1:
                a = 0
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button != 1:
                        screen.fill(screencolor)
            mouse_press_checker = pygame.mouse.get_pressed()
            if mouse_press_checker[0]:
                pygame.draw.circle(screen, pygame.Color(color[a]), (mousex, mousey), radius, width)
            mousex, mousey = pygame.mouse.get_pos()
            a += 1
            pygame.display.flip()
            clock.tick(60)


def run():
    # app = pywinauto.application.Application()
    # handle = pywinauto.findwindows.find_windows(title=title)
    # window = app.window_(handle=handle)
    run = threading.Thread(target=main)
    run.start()
    run.join()


run()
# notification.show_toast("Screen", "The screen settings is in the system tray.")
trayimage = PIL.Image.open("boringscreen.png")


def onclicked(icon: pystray.Icon, item):
    item = str(item)
    if item == "Exit":
        icon.stop()
        sys.exit()
    if item == "Turn on the screen":
        run()
    if item == "Edit the circle size":
        subprocess.call(["notepad", circlefile])
    if item == "Edit the color of the circle":
        subprocess.call(["notepad", colorfile])
    if item == "Edit the background color":
        subprocess.call(["notepad", bgcolorfile])
    if item == "Edit the mode of the screen":
        subprocess.call(["notepad", modefile])


icon = pystray.Icon("Boring Screen", trayimage, menu=pystray.Menu(
    pystray.MenuItem("Turn on the screen", onclicked, default=True),
    pystray.MenuItem("Edit the circle size", onclicked),
    pystray.MenuItem("Edit the color of the circle", onclicked),
    pystray.MenuItem("Edit the background color", onclicked),
    pystray.MenuItem("Edit the mode of the screen", onclicked),
    pystray.MenuItem("Exit", onclicked),
), visible=True)
icon.run()

sys.exit()