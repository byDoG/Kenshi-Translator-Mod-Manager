import os
import sys
import tkinter as tk
import json

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
        return os.path.dirname(sys.argv[0])
    else:
        return os.path.dirname(os.path.abspath(__file__))


def main():
    base_dir = get_base_dir()
    mods_file = os.path.join(base_dir, "mods_all.json")

    if os.path.exists(mods_file):
        try:
            os.remove(mods_file)
            show_message(LANG.get("messages", {}).get("1", ""), border_color="#FF0000")
        except Exception:
            show_message(LANG.get("messages", {}).get("2", ""), border_color="#FF0000")
    else:
        show_message(LANG.get("messages", {}).get("3", ""), border_color="#FFD700")


if __name__ == "__main__":
    main()
