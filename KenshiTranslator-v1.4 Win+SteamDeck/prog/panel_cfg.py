import tkinter as tk
import os, sys, json, zipfile
from pathlib import Path
from datetime import datetime
import lang

# Цвета и стили как в основном GUI
DARK_BG = "#222222"
BTN_BG = "#2b2b2b"
BTN_ACTIVE = "#333333"
BTN_BORDER = "#555555"
BTN_BORDER_ACTIVE = "#666666"
BTN_FG = "white"

ALL_MODS_FILE = "mods_all.json"
SETTINGS_FILE = "settings.json"

# === безопасная загрузка языка ===
lang.ensure_lang_file()
if not os.path.exists(SETTINGS_FILE):
    lang.show_lang_selector()

with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
    settings = json.load(f)
language = settings.get("language", "English")
with open("lang.json", "r", encoding="utf-8") as f:
    lang_data = json.load(f)
LANG = lang_data.get(language, lang_data.get("English", {}))


# =============== ВСПЛЫВАЮЩЕЕ СООБЩЕНИЕ ==========================
def show_message(message, border_color="#FFD700", on_close=None):
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

    def close_and_callback():
        root.destroy()
        if on_close:
            on_close()

    root.after(2000, close_and_callback)
    root.mainloop()


# =============== ПОИСК MODS.CFG ==========================
def find_mods_cfg():
    prog_dir = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
    parent = prog_dir.parent

    # === Локальная установка ===
    if parent.parent.name.lower() == "mods":
        kenshi_dir = prog_dir.parent.parent.parent
        cfg_file = kenshi_dir / "data" / "mods.cfg"
        if cfg_file.exists():
            return cfg_file

    # === Steam Workshop ===
    if "233860" in str(prog_dir):
        path = prog_dir
        while path.name.lower() != "steamapps" and path.parent != path:
            path = path.parent
        kenshi_dir = path / "common" / "Kenshi"
        cfg_file = kenshi_dir / "data" / "mods.cfg"
        if cfg_file.exists():
            return cfg_file

    return None


# =============== PROFILE SYSTEM ===================
def save_profile(app, idx):
    exe_dir = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
    all_json = exe_dir / ALL_MODS_FILE
    settings_file = exe_dir / SETTINGS_FILE

    if not all_json.exists():
        show_message(LANG.get("messages", {}).get("3", ""), border_color="#FFD700")
        return

    with open(all_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    enabled_mods = [m["name"] for m in data.get("mods", []) if "name" in m and m.get("enabled", False)]
    disabled_mods = [m["name"] for m in data.get("mods", []) if "name" in m and not m.get("enabled", False)]

    if not enabled_mods and not disabled_mods:
        show_message(LANG.get("messages", {}).get("22", ""), border_color="#FFD700")
        return

    if settings_file.exists():
        with open(settings_file, "r", encoding="utf-8") as f:
            settings = json.load(f)
    else:
        settings = {}

    profile_key = f"Profile-{idx}"
    settings[profile_key] = {
        "config": True,
        "enabled": enabled_mods,
        "disabled": disabled_mods
    }

    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

    show_message(LANG.get("messages", {}).get("17", "").format(idx=idx), border_color="#00FF00")


def load_profile(app, idx):
    exe_dir = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
    all_json = exe_dir / ALL_MODS_FILE
    settings_file = exe_dir / SETTINGS_FILE

    if not settings_file.exists():
        show_message(LANG.get("messages", {}).get("18", "").format(idx=idx), border_color="#FF0000")
        return

    with open(settings_file, "r", encoding="utf-8") as f:
        settings = json.load(f)

    profile_key = f"Profile-{idx}"
    profile = settings.get(profile_key)
    if not profile or not profile.get("config", False):
        show_message(LANG.get("messages", {}).get("19", "").format(idx=idx), border_color="#FFD700")
        return

    enabled_mods = profile.get("enabled", [])
    disabled_mods = profile.get("disabled", [])

    if not enabled_mods and not disabled_mods:
        show_message(LANG.get("messages", {}).get("20", "").format(idx=idx), border_color="#FFD700")
        return

    if not all_json.exists():
        show_message(LANG.get("messages", {}).get("3", ""), border_color="#FFD700")
        return

    with open(all_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    for mod in data.get("mods", []):
        if "name" not in mod:
            continue
        if mod["name"] in enabled_mods:
            mod["enabled"] = True
        elif mod["name"] in disabled_mods:
            mod["enabled"] = False

    with open(all_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    app.refresh_mods(data["mods"])
    show_message(LANG.get("messages", {}).get("21", "").format(idx=idx),
                 border_color="#00FF00", on_close=lambda: app.save_btn.invoke())

# =============== PANEL ============================
def make_button(parent, text, cmd=None):
    btn = tk.Button(parent, text=text, command=cmd,
                    width=14,
                    font=("Segoe UI", 10, "bold"),
                    bg=BTN_BG, fg=BTN_FG,
                    activebackground=BTN_ACTIVE, activeforeground=BTN_FG,
                    relief="solid", bd=1,
                    highlightbackground=BTN_BORDER,
                    highlightcolor=BTN_BORDER_ACTIVE,
                    highlightthickness=1)
    btn.pack(pady=2, ipady=1)
    return btn


# =============== PANEL ============================
def show_panel(root, app):
    panel_width = 118
    panel_height = 480

    panel = tk.Frame(root, width=panel_width, height=panel_height, bg=DARK_BG)
    panel.place(x=root.winfo_width(), y=0)
    panel.pack_propagate(False)

    top_bar = tk.Frame(panel, bg=DARK_BG, height=24)
    top_bar.pack(fill="x", side="top")
    author = tk.Label(top_bar, text="CFG PANEL",
                      bg=DARK_BG, fg="red", font=("Segoe UI", 10, "bold"))
    author.pack(side="right", padx=5)

    btn_frame = tk.Frame(panel, bg=DARK_BG)
    btn_frame.pack(fill="both", expand=True, padx=8, pady=5)

    make_button(btn_frame, LANG["buttons"]["1"], cmd=app.scan_btn.invoke)
    make_button(btn_frame, LANG["buttons"]["2"], cmd=app.load_cfg_btn.invoke)
    make_button(btn_frame, LANG["buttons"]["3"], cmd=app.sorting_btn.invoke)
    make_button(btn_frame, LANG["buttons"]["4"], cmd=app.save_btn.invoke)
    make_button(btn_frame, LANG["buttons"]["5"], cmd=app.clear_btn.invoke)

    tk.Frame(btn_frame, height=1, width=120, bg="#444444").pack(pady=5)

    def make_dual_buttons(parent, left_text, right_text, left_cmd, right_cmd):
        row = tk.Frame(parent, bg=DARK_BG)
        row.pack(fill="x", pady=2)

        left_btn = tk.Button(row, text=left_text,
                             command=left_cmd, font=("Segoe UI", 10, "bold"),
                             bg=BTN_BG, fg=BTN_FG,
                             activebackground=BTN_ACTIVE, activeforeground=BTN_FG,
                             relief="solid", bd=1,
                             highlightbackground=BTN_BORDER,
                             highlightcolor=BTN_BORDER_ACTIVE,
                             highlightthickness=1)
        left_btn.grid(row=0, column=0, sticky="nsew")

        right_btn = tk.Button(row, text=right_text,
                              command=right_cmd, font=("Segoe UI", 10, "bold"),
                              bg=BTN_BG, fg=BTN_FG,
                              activebackground=BTN_ACTIVE, activeforeground=BTN_FG,
                              relief="solid", bd=1,
                              highlightbackground=BTN_BORDER,
                              highlightcolor=BTN_BORDER_ACTIVE,
                              highlightthickness=1)
        right_btn.grid(row=0, column=1, sticky="nsew")

        row.columnconfigure(0, weight=1, uniform="buttons")
        row.columnconfigure(1, weight=1, uniform="buttons")

    make_dual_buttons(btn_frame, "Load 1", "Save 1",
                      lambda: load_profile(app, 1),
                      lambda: save_profile(app, 1))
    make_dual_buttons(btn_frame, "Load 2", "Save 2",
                      lambda: load_profile(app, 2),
                      lambda: save_profile(app, 2))
    make_dual_buttons(btn_frame, "Load 3", "Save 3",
                      lambda: load_profile(app, 3),
                      lambda: save_profile(app, 3))

    tk.Frame(btn_frame, height=1, width=120, bg="#444444").pack(pady=5)

    make_button(btn_frame, LANG["buttons"]["8"], cmd=app.start_btn.invoke)
    make_button(btn_frame, LANG["buttons"]["9"], cmd=app.exit_btn.invoke)

    back_btn = make_button(btn_frame, LANG["buttons"]["14"])
    def animate_out(x):
        end_x = root.winfo_width()
        if x < end_x:
            panel.place(x=x, y=0)
            root.after(15, animate_out, x + 10)
        else:
            panel.destroy()
    back_btn.configure(command=lambda: animate_out(root.winfo_width() - panel_width))

    def animate_in(x):
        target_x = root.winfo_width() - panel_width
        if x > target_x:
            panel.place(x=x, y=0)
            root.after(15, animate_in, x - 10)
        else:
            panel.place(x=target_x, y=0)
    animate_in(root.winfo_width())


# =============== CONFIG FUNCTIONS =================
def load_config(app):
    cfg_file = find_mods_cfg()
    if not cfg_file:
        show_message(LANG["messages"]["7"], border_color="#FF0000")
        return

    exe_dir = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
    all_json = exe_dir / ALL_MODS_FILE
    if not all_json.exists():
        show_message(LANG["messages"]["3"], border_color="#FFD700")
        return

    with open(cfg_file, "r", encoding="utf-8") as f:
        enabled_mods = [line.strip() for line in f if line.strip()]

    with open(all_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    for mod in data["mods"]:
        if "name" in mod:
            mod["enabled"] = False

    for mod in data["mods"]:
        if "name" not in mod:
            continue
        if mod["name"] in enabled_mods:
            mod["enabled"] = True

    with open(all_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    app.refresh_mods(data["mods"])
    app.status.set(LANG["messages"]["23"])
    show_message(LANG["messages"]["23"], border_color="#00FF00")


def save_config(app):
    cfg_file = find_mods_cfg()
    if not cfg_file:
        show_message(LANG["messages"]["8"], border_color="#FF0000")
        return

    exe_dir = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
    all_json = exe_dir / ALL_MODS_FILE
    if not all_json.exists():
        show_message(LANG["messages"]["3"], border_color="#FFD700")
        return

    with open(all_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        enabled_mods = [m["name"] for m in data.get("mods", []) if "name" in m and m.get("enabled", False)]

    with open(cfg_file, "w", encoding="utf-8") as f:
        for mod in enabled_mods:
            f.write(mod + "\n")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    backup_dir = exe_dir
    backup_zip = backup_dir / f"backup-{timestamp}-cfg.zip"
    with zipfile.ZipFile(backup_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(cfg_file, "mods.cfg")

    backups = sorted(backup_dir.glob("backup-*-cfg.zip"), key=os.path.getmtime, reverse=True)
    for old in backups[5:]:
        try:
            old.unlink()
        except Exception:
            pass

    app.status.set(LANG["messages"]["26"].format(count=len(enabled_mods), backup=backup_zip.name))
    show_message(LANG["messages"]["26"].split(",")[0].format(count=len(enabled_mods)), border_color="#00FF00")

