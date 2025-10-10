import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import ttk
import time
import platform
import traceback
import lang     # должно быть здесь

# === определение платформы ===
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

# === безопасные импорты win32 ===
if IS_WINDOWS:
    import pythoncom
    import win32com.client

# ================== ЯЗЫК ==================
lang.ensure_lang_file()
if not os.path.exists("settings.json"):
    lang.show_lang_selector()

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)
language = settings.get("language")
with open("lang.json", "r", encoding="utf-8") as f:
    lang_data = json.load(f)
LANG = lang_data[language]

SETTINGS_FILE = "settings.json"
# ================== теперь можно подключать остальные ==================

import scan_mods
import run_kenshi
import clear_mods
import panel_cfg
import panel_translate
import panel_info


# ================== HELPERS ==================

def show_message_window(message, border_color="#FF0000"):
    root = tk.Tk()
    root.overrideredirect(True)
    win_w, win_h = 500, 90
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    pos_x = (screen_w // 2) - (win_w // 2)
    pos_y = (screen_h // 2) - (win_h // 2)
    root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
    canvas = tk.Canvas(root, width=win_w, height=win_h,
                       highlightthickness=0, bg="#222222")
    canvas.pack(fill="both", expand=True)
    border_width = 6
    canvas.create_line(0, 0, win_w, 0, fill=border_color, width=border_width)
    canvas.create_line(0, win_h, win_w, win_h, fill=border_color, width=border_width)
    canvas.create_text(win_w // 2, win_h // 2, text=message,
                       fill="white", font=("Arial", 20, "bold"))
    root.after(3000, root.destroy)
    root.mainloop()


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)


def create_shortcut(exe_dir):
    if IS_LINUX:
        # На Linux просто пропускаем создание ярлыка, но не выдаём ошибку
        return True
    try:
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        shortcut_path = os.path.join(desktop, "Kenshi Translator.lnk")
        target = os.path.join(exe_dir, "KenshiTranslator.exe")
        pythoncom.CoInitialize()
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = target
        shortcut.WorkingDirectory = exe_dir
        shortcut.IconLocation = f"{target},0"
        shortcut.Save()
        return True
    except Exception as e:
        print(f"Ошибка при создании ярлыка: {e}")
        return False

# ================== PATH CHECK ==================

def check_paths(settings, exe_dir):
    print("[DEBUG] exe_dir:", exe_dir)

    if "mods" in exe_dir.lower():
        kenshi_dir = os.path.dirname(os.path.dirname(os.path.dirname(exe_dir)))
        mods_path = os.path.join(kenshi_dir, "MODS")
        print("[DEBUG] mods_path:", mods_path, "exists=", os.path.isdir(mods_path))
        if os.path.isdir(mods_path):
            settings["local"] = True
            save_settings(settings)
            steamapps_dir = os.path.dirname(os.path.dirname(kenshi_dir))
            workshop_dir = os.path.join(steamapps_dir, "workshop", "content", "233860")
            if os.path.isdir(workshop_dir):
                settings["steam"] = True
                save_settings(settings)
                show_message_window(LANG["messages"]["4"], border_color="#00FF00")
                return settings
            else:
                show_message_window(LANG["messages"]["5"], border_color="#FFFF00")
                return settings

    if "233860" in exe_dir:
        steam_dir = os.path.dirname(os.path.dirname(exe_dir))
        if os.path.basename(steam_dir) == "233860":
            steamapps_dir = os.path.dirname(os.path.dirname(os.path.dirname(steam_dir)))
            common_dir = os.path.join(steamapps_dir, "common", "Kenshi")
            mods_dir = os.path.join(common_dir, "MODS")
            settings["steam"] = True
            save_settings(settings)
            if os.path.isdir(mods_dir):
                settings["local"] = True
                save_settings(settings)
                show_message_window(LANG["messages"]["4"], border_color="#00FF00")
                return settings
            else:
                show_message_window(LANG["messages"]["6"], border_color="#FF0000")
                return None

    show_message_window(LANG["messages"]["7"], border_color="#FF0000")
    return None

# ================== STARTUP ==================
def startup_main():
    try:
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
        else:
            exe_dir = os.path.dirname(os.path.abspath(__file__))

        if os.path.basename(exe_dir).lower() != "prog":
            show_message_window(LANG["messages"]["7"], border_color="#FF0000")
            sys.exit(1)

        # === ПРОВЕРКА НАЛИЧИЯ SETTINGS ===
        if not os.path.exists(SETTINGS_FILE):
            lang.show_lang_selector()
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)

            # === СОЗДАНИЕ ЯРЛЫКА ===
            if not settings.get("shortcut"):
                if IS_LINUX:
                    settings["shortcut"] = True
                    save_settings(settings)
                else:
                    if create_shortcut(exe_dir):
                        settings["shortcut"] = True
                        save_settings(settings)
                        show_message_window(LANG["messages"]["8"], border_color="#FF0000")
                    else:
                        show_message_window(LANG["messages"]["2"], border_color="#FF0000")
                        return None  # ⛔ не идём дальше, если ярлык не создался

            # === ПРОВЕРКА ПАПОК ===
            return check_paths(settings, exe_dir)

        # === ЕСЛИ SETTINGS ЕСТЬ ===
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)

        # === ЕСЛИ ЯРЛЫК ЕЩЁ НЕ СОЗДАН (ПЕРВЫЙ ЗАПУСК) ===
        if not settings.get("shortcut"):
            if IS_LINUX:
                settings["shortcut"] = True
                save_settings(settings)
            else:
                if create_shortcut(exe_dir):
                    settings["shortcut"] = True
                    save_settings(settings)
                    show_message_window(LANG["messages"]["8"], border_color="#FF0000")
                else:
                    show_message_window(LANG["messages"]["2"], border_color="#FF0000")
                    return None  # ⛔ не идём дальше, если ярлык не создался

        # === ПРОВЕРКА ПАПОК ===
        if settings.get("steam"):
            if settings.get("local"):
                return settings
            else:
                show_message_window(LANG["messages"]["6"], border_color="#FF0000")
                return None

        if settings.get("local"):
            return settings

        return check_paths(settings, exe_dir)

    except Exception:
        traceback.print_exc()
        input("Press Enter to exit...")
        return None

# ================== GUI ==================
DARK_BG = "#222222"
BTN_BG = "#2b2b2b"
BTN_ACTIVE = "#333333"
BTN_BORDER = "#555555"
BTN_BORDER_ACTIVE = "#666666"
BTN_FG = "white"
SEPARATOR_COLOR = "#555555"
ICONS_DIR = "icons"
ALL_MODS_FILE = "mods_all.json"


class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kenshi Translator — D0G911")
        self.root.geometry("620x467")
        self.root.minsize(620, 467)
        self.root.configure(bg=DARK_BG)
        self.root.overrideredirect(True)
        DEFAULT_FONT = ("Segoe UI", 10, "bold")
        root.option_add("*Font", DEFAULT_FONT)

        self.icon_checked = tk.PhotoImage(file=os.path.join(ICONS_DIR, "check.png"))
        self.icon_unchecked = tk.PhotoImage(file=os.path.join(ICONS_DIR, "cross.png"))
        self.icon_warning = tk.PhotoImage(file=os.path.join(ICONS_DIR, "warning.png"))

        top_bar = tk.Frame(root, bg=DARK_BG, height=24)
        top_bar.pack(fill="x", padx=5, pady=2)
        self.status = tk.StringVar(value=LANG["messages"]["9"])
        title_bar = tk.Label(top_bar, textvariable=self.status, bg=DARK_BG, fg="white", anchor="w")
        title_bar.pack(side="left", fill="x", expand=True)
        title_bar.bind("<ButtonPress-1>", self.start_move)
        title_bar.bind("<B1-Motion>", self.do_move)
        author = tk.Label(top_bar, text="D0G911", bg=DARK_BG, fg="red", font=("Segoe UI", 10, "bold"))
        author.pack(side="right")

        container = tk.Frame(root, bg=DARK_BG)
        container.pack(fill="both", expand=True)

        tree_frame = tk.Frame(container, bg=DARK_BG)
        tree_frame.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=DARK_BG, fieldbackground=DARK_BG, foreground="white")
        style.configure("Treeview.Heading", background=DARK_BG, foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[("active", BTN_ACTIVE)])
        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background=DARK_BG,
                        darkcolor=DARK_BG,
                        lightcolor=DARK_BG,
                        troughcolor=DARK_BG,
                        bordercolor=DARK_BG,
                        arrowcolor="white")

        tree_container = tk.Frame(tree_frame, bg=DARK_BG)
        tree_container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_container, columns=("lang", "progress"), show="tree headings", height=18)
        self.tree.heading("#0", text="Enabled (0 Mods)")
        self.tree.column("#0", width=300, anchor="w")
        self.tree.heading("lang", text="Language")
        self.tree.column("lang", width=90, anchor="center")
        self.tree.heading("progress", text="Progress")
        self.tree.column("progress", width=90, anchor="center")
        yscroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=yscroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", self.toggle_mod)
        self.tree.bind("<Button-3>", self.right_click_mod)

        self.resize_border = tk.Frame(tree_frame, bg="#FF0000", height=3, cursor="sb_v_double_arrow")
        self.resize_border.pack(fill="x", side="bottom")
        self.resize_border.pack_propagate(False)
        self.resize_border.bind("<ButtonPress-1>", self.start_resize)
        self.resize_border.bind("<B1-Motion>", self.do_resize)

        frame = tk.Frame(container, bg=DARK_BG)
        frame.pack(side="right", fill="y", padx=8, pady=(0, 5))

        self.scan_btn = self.make_button(frame, LANG["buttons"]["1"], self.run_scan)
        self.load_cfg_btn = self.make_button(frame, LANG["buttons"]["2"], lambda: panel_cfg.load_config(self))
        self.sorting_btn = self.make_button(frame, LANG["buttons"]["3"], self.run_sort)
        self.save_btn = self.make_button(frame, LANG["buttons"]["4"], lambda: panel_cfg.save_config(self))
        self.clear_btn = self.make_button(frame, LANG["buttons"]["5"], self.run_clear)
        self.make_separator(frame)
        self.my_game_btn = self.make_button(frame, LANG["buttons"]["6"], lambda: panel_cfg.show_panel(self.root, self))
        self.translate_btn = self.make_button(frame, LANG["buttons"]["7"], lambda: panel_translate.show_panel(self.root, self))
        self.make_separator(frame)
        self.start_btn = self.make_button(frame, LANG["buttons"]["8"], run_kenshi.main)
        self.exit_btn = self.make_button(frame, LANG["buttons"]["9"], self.root.destroy)

    def make_button(self, parent, text, cmd):
        btn = tk.Button(parent, text=text, command=cmd, width=14,
                        font=("Segoe UI", 10, "bold"),
                        bg=BTN_BG, fg=BTN_FG,
                        activebackground=BTN_ACTIVE, activeforeground=BTN_FG,
                        relief="solid", bd=1,
                        highlightbackground=BTN_BORDER,
                        highlightcolor=BTN_BORDER_ACTIVE,
                        highlightthickness=1)
        btn.pack(pady=2, ipady=1)
        return btn

    def make_separator(self, parent):
        tk.Frame(parent, height=1, width=120, bg="#444444").pack(pady=5)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.root.geometry(f"+{x}+{y}")

    def start_resize(self, event):
        self.start_y = event.y_root
        self.start_height = self.root.winfo_height()

    def do_resize(self, event):
        delta = event.y_root - self.start_y
        new_height = self.start_height + delta
        if new_height > 200:
            self.root.geometry(f"{self.root.winfo_width()}x{new_height}")

    def refresh_mods(self, mods):
        self.tree.delete(*self.tree.get_children())
        enabled = [m for m in mods if m.get("enabled") and "name" in m and m["name"] != "__panel_dummy__"]
        disabled = [m for m in mods if not m.get("enabled") and "name" in m and m["name"] != "__panel_dummy__"]
        self.tree.heading("#0", text=f"Enabled ({len(enabled)} Mods)")

        for mod in enabled:
            self.tree.insert("", "end", image=self.icon_checked, text=mod["name"],
                             values=("?", "0%"), tags=("enabled",))

        sep_len = self.tree.column("#0", option="width") // 7
        sep_id = self.tree.insert("", "end",
                                  text="─" * sep_len,
                                  values=("", ""),
                                  tags=("separator",))
        self.tree.tag_configure("separator", foreground="#888888", background=DARK_BG)
        self.tree.item(sep_id, open=False)

        for mod in disabled:
            self.tree.insert("", "end", image=self.icon_unchecked, text=mod["name"],
                             values=("?", "0%"), tags=("disabled",))

    def run_scan(self):
        all_json = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ALL_MODS_FILE)
        if os.path.exists(all_json):
            try:
                os.unlink(all_json)
                self.status.set(LANG["messages"]["10"])
                self.root.update_idletasks()
            except Exception as e:
                self.status.set(LANG["messages"]["13"].replace("{error}", str(e)))
                return
        count = scan_mods.main()
        if os.path.exists(all_json):
            with open(all_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.refresh_mods(data.get("mods", []))
        self.status.set(LANG["messages"]["11"].replace("{count}", str(count)))

    def run_sort(self):
        try:
            import sort_mods
            sort_mods.main()
            all_json = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ALL_MODS_FILE)
            if os.path.exists(all_json):
                with open(all_json, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.refresh_mods(data.get("mods", []))
            self.status.set(LANG["messages"]["12"])
        except Exception as e:
            self.status.set(LANG["messages"]["13"].replace("{error}", str(e)))

    def run_clear(self):
        self.tree.delete(*self.tree.get_children())
        clear_mods.main()

    def toggle_mod(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        tags = self.tree.item(item, "tags")
        if "separator" in tags:
            return
        mod_name = self.tree.item(item, "text")
        all_json = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ALL_MODS_FILE)
        if not os.path.exists(all_json):
            return
        with open(all_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        for mod in data.get("mods", []):
            if mod.get("name") == mod_name:
                mod["enabled"] = not mod.get("enabled", False)
                break
        with open(all_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.refresh_mods(data["mods"])
        self.status.set(LANG["messages"]["14"].replace("{mod_name}", mod_name))

    def right_click_mod(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        tags = self.tree.item(item, "tags")
        if "separator" in tags:
            return
        mod_name = self.tree.item(item, "text")
        self.tree.selection_set(item)
        self.tree.focus(item)
        all_json = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ALL_MODS_FILE)
        if not os.path.exists(all_json):
            return
        try:
            with open(all_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            for mod in data.get("mods", []):
                if mod.get("name") == "__panel_dummy__":
                    mod["mod_name"] = mod_name
                    break
            with open(all_json, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[INFO] ПКМ по модулю: {mod_name} → записан в mods_all.json")
            panel_info.show_panel(self.root, self.resize_border)
            self.status.set(LANG["messages"]["15"].replace("{mod_name}", mod_name))
        except Exception as e:
            print(f"[ERROR] Ошибка записи ПКМ: {e}")
            self.status.set(LANG["messages"]["16"].replace("{error}", str(e)))


# ================== MAIN ==================
if __name__ == "__main__":
    settings = startup_main()
    if not settings:
        sys.exit(0)

    root = tk.Tk()
    win_w, win_h = 620, 467
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    pos_x = (screen_w // 2) - (win_w // 2)
    pos_y = (screen_h // 2) - (win_h // 2)
    root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
    app = TranslatorApp(root)
    root.mainloop()
