import subprocess
from pathlib import Path
import sys
import threading
import json
import os
import platform
import tkinter as tk

# === безопасная загрузка языка ===
LANG_FILE = "lang.json"
SETTINGS_FILE = "settings.json"

if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        settings = json.load(f)
    lang_name = settings.get("language", "English")
else:
    lang_name = "English"

if os.path.exists(LANG_FILE):
    with open(LANG_FILE, "r", encoding="utf-8") as f:
        lang_data = json.load(f)
else:
    lang_data = {"English": {"messages": {}, "buttons": {}}}

LANG = lang_data.get(lang_name, lang_data.get("English", {}))

IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"


# === Всплывающее сообщение ===
def show_message(message, border_color="#FF0000"):
    root = tk.Tk()
    root.overrideredirect(True)
    win_w, win_h = 500, 90
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    pos_x = (screen_w // 2) - (win_w // 2)
    pos_y = (screen_h // 2) - (win_h // 2)
    root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")

    canvas = tk.Canvas(root, width=win_w, height=win_h, highlightthickness=0, bg="#222222")
    canvas.pack(fill="both", expand=True)

    border_width = 6
    canvas.create_line(0, 0, win_w, 0, fill=border_color, width=border_width)
    canvas.create_line(0, win_h, win_w, win_h, fill=border_color, width=border_width)
    canvas.create_text(win_w // 2, win_h // 2, text=message,
                       fill="white", font=("Arial", 20, "bold"))
    root.after(3000, root.destroy)
    root.mainloop()


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.argv[0]).resolve().parent  # рядом с KenshiTranslator.exe / -linux
    else:
        return Path(__file__).resolve().parent


def main():
    prog_dir = get_base_dir()
    parent2 = prog_dir.parent.parent
    exe = None

    if IS_WINDOWS:
        # Проверка локала (mods)
        if parent2.name.lower() == "mods":
            base = parent2.parent  # Kenshi
            for candidate in ["Kenshi_x64.exe", "kenshi_GOG_x64.exe"]:
                exe_path = base / candidate
                if exe_path.exists():
                    exe = exe_path
                    break

        # Проверка стима (233860)
        elif parent2.name == "233860":
            steamapps = parent2.parent.parent.parent
            base = steamapps / "common" / "Kenshi"
            for candidate in ["Kenshi_x64.exe", "kenshi_GOG_x64.exe"]:
                exe_path = base / candidate
                if exe_path.exists():
                    exe = exe_path
                    break

        if not exe:
            show_message(LANG.get("messages", {}).get("6", ""), border_color="#FF0000")
            return

        try:
            proc = subprocess.Popen([str(exe)], cwd=str(exe.parent))

            import __main__
            if hasattr(__main__, "root"):
                root = __main__.root
                root.after(2000, root.withdraw)

                def wait_and_exit():
                    proc.wait()
                    root.destroy()

                threading.Thread(target=wait_and_exit, daemon=True).start()

        except Exception as e:
            msg = LANG.get("messages", {}).get("36", "").format(error=e)
            show_message(msg, border_color="#FF0000")

    elif IS_LINUX:
        # === Steam Deck / Linux ===
        try:
            # 1. Попробовать запустить через steam -applaunch
            result = subprocess.Popen(["steam", "-applaunch", "233860"],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            show_message("Launching Kenshi via Steam...", border_color="#00FF00")
            return

        except Exception:
            try:
                # 2. Альтернатива — открыть URI протокол Steam
                subprocess.Popen(["xdg-open", "steam://rungameid/233860"],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                show_message("Launching Kenshi (xdg-open)...", border_color="#00FF00")
                return
            except Exception as e:
                msg = LANG.get("messages", {}).get("36", "").format(error=e)
                show_message(msg, border_color="#FF0000")
                return


if __name__ == "__main__":
    main()
