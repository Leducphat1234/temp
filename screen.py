import pygame
import sys
import threading
import pystray
import PIL.Image
from datetime import datetime
import subprocess
from tkinter import messagebox
import os
from win10toast import ToastNotifier


filename = "screen.exe"
colorfile = "color.txt"
circlefile = "circle.txt"
notification = ToastNotifier()

title = "Boring screen"


def main():
    screencolor = "#ffffff"

    def checktime():
        global screencolor
        if datetime.now().hour >= 6 and datetime.now().hour < 18:
            screencolor = "#ffffff"
        else:
            screencolor = "#1E1E1E"
        return screencolor
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode()
    pygame.display.set_caption(title)
    global colorfile
    if '_MEIPASS2' in os.environ:
        colorfile = os.path.join(os.environ['_MEIPASS2'], colorfile)
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
            cir.write("10\n") # radius
            cir.write("10\n") # width
    except FileExistsError:
        pass
    a = 0
    screencolor = checktime()
    screen.fill(screencolor)
    while True:
        with open(colorfile, "r") as f:
            color = f.read()
            color = color.split()
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
        with open(circlefile, "r") as cir:
            cir = cir.read().split()
            radius = int(cir[0])
            width = int(cir[1])
            pygame.draw.circle(screen, pygame.Color(color[a]), (mousex, mousey), radius, width)
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
notification.show_toast("Screen", "The boring screen is in the system tray.")
trayimage = PIL.Image.open("boringscreen.png")


def onclicked(icon: pystray.Icon, item):
    item = str(item)
    if item == "Exit":
        icon.stop()

        sys.exit()
    if item == "Turn on the screen":
        run()


icon = pystray.Icon("Boring Screen", trayimage, menu=pystray.Menu(
    pystray.MenuItem("Turn on the screen", onclicked),
    pystray.MenuItem("Exit", onclicked),
))
icon.run()

sys.exit()
