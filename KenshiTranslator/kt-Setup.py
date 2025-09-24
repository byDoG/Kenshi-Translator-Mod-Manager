import os
import sys
import shutil
import tkinter as tk
from win32com.client import Dispatch
import winshell
import subprocess

# Файлы и папки, которые включаем в установку
INSTALL_ITEMS = [
    "KenshiTranslator.exe",
    "LICENSE.md",
    "icons"
]

def resource_path(relative_path):
    """Возвращает путь к ресурсу как в dev, так и в exe"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def copy_item(src, dst):
    """Копирование файла или папки с заменой"""
    if os.path.isdir(src):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for root, dirs, files in os.walk(src):
            rel_path = os.path.relpath(root, src)
            target_root = os.path.join(dst, rel_path) if rel_path != "." else dst
            if not os.path.exists(target_root):
                os.makedirs(target_root)
            for f in files:
                shutil.copy2(os.path.join(root, f), os.path.join(target_root, f))
    else:
        shutil.copy2(src, dst)

def main():
    folder_name = "KenshiTranslator"

    # Целевая папка (3 уровня вверх)
    target = os.path.abspath(os.path.join(os.getcwd(), "..", "..", ".."))
    dest = os.path.join(target, folder_name)

    # Создаём папку назначения, если её нет
    if not os.path.exists(dest):
        os.makedirs(dest)

    # Копируем все нужные файлы/папки
    for item in INSTALL_ITEMS:
        src_path = resource_path(item)
        dst_path = os.path.join(dest, item)
        copy_item(src_path, dst_path)

    # Путь к exe
    translator_exe = os.path.join(dest, "KenshiTranslator.exe")

    # Ярлык на рабочем столе
    desktop = winshell.desktop()
    shortcut_path = os.path.join(desktop, "Kenshi Translator.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = translator_exe
    shortcut.WorkingDirectory = dest
    shortcut.IconLocation = os.path.join(dest, "icons", "icon.ico")
    shortcut.save()

    # Окно INSTALLED!!!
    root = tk.Tk()
    root.overrideredirect(True)
    root.configure(bg="#2e2e2e")
    label = tk.Label(root, text="INSTALLED!!!", fg="white", bg="#2e2e2e", font=("Arial", 20, "bold"))
    label.pack(padx=30, pady=20)
    root.after(5000, root.destroy)
    root.eval('tk::PlaceWindow . center')
    root.mainloop()

    # Самоудаление
    exe_path = sys.argv[0]
    bat_path = exe_path + ".bat"
    with open(bat_path, "w", encoding="utf-8") as bat:
        bat.write(f"""@echo off
ping 127.0.0.1 -n 3 >nul
del "{exe_path}"
del "%~f0"
""")
    subprocess.Popen([bat_path], shell=True)

if __name__ == "__main__":
    main()
