import os
import sys
import tkinter as tk


def show_message(message):
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
    border_color = "#FF0000"
    border_width = 6
    canvas.create_line(0, 0, win_w, 0, fill=border_color, width=border_width)
    canvas.create_line(0, win_h, win_w, win_h, fill=border_color, width=border_width)
    canvas.create_text(win_w // 2, win_h // 2, text=message,
                       fill="white", font=("Arial", 20, "bold"))
    root.after(3000, root.destroy)
    root.mainloop()


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.argv[0])  # рядом с KenshiTranslator.exe
    else:
        return os.path.dirname(os.path.abspath(__file__))  # рядом с clear_mods.py


def main():
    base_dir = get_base_dir()
    mods_file = os.path.join(base_dir, "mods_all.json")

    if os.path.exists(mods_file):
        try:
            os.remove(mods_file)
            show_message("MOD LIST DELETED")
        except Exception:
            show_message("ERROR DELETING FILE")
    else:
        show_message("PRESS SCAN MOD :)")


if __name__ == "__main__":
    main()
