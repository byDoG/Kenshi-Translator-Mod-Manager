import os
import sys
import json
import tkinter as tk
import webbrowser
from pathlib import Path

DARK_BG = "#222222"
TEXT_FG = "white"
TITLE_FG = "#FFD966"  # жёлтый для значений
LINK_FG = "red"       # красный для ссылок и Steam ID
PANEL_MAX_H = 110

_panel = None
_text_box = None
_close_job = None


def _get_prog_dir():
    # Универсальный путь: питон, exe, батник
    return Path(os.path.dirname(os.path.abspath(sys.argv[0])))


def show_panel(root, anchor_widget, mods_file="mods_all.json"):
    global _panel, _text_box, _close_job

    mod = _get_mod_data(mods_file)
    if not mod:
        return

    if not _panel or not _panel.winfo_exists():
        panel = tk.Toplevel(root)
        panel.overrideredirect(True)
        panel.configure(bg=DARK_BG)
        panel.lift()
        panel.transient(root)

        container = tk.Frame(panel, bg=DARK_BG)
        container.pack(fill="both", expand=True)

        tk.Frame(container, bg="red", width=1).pack(side="left", fill="y")
        tk.Frame(container, bg="red", width=1).pack(side="right", fill="y")

        text = tk.Text(container, bg=DARK_BG, fg=TEXT_FG,
                       wrap="word", borderwidth=0, highlightthickness=0,
                       padx=10, pady=5)
        text.pack(side="left", fill="both", expand=True)
        text.bind("<MouseWheel>", lambda e: _on_mousewheel(e, text))

        # теги
        text.tag_config("label", foreground=TEXT_FG, font=("TkDefaultFont", 10))
        text.tag_config("value", foreground=TITLE_FG, font=("TkDefaultFont", 11))
        text.tag_config("link", foreground=LINK_FG, font=("TkDefaultFont", 11))

        _panel = panel
        _text_box = text

        anchor_widget.update_idletasks()
        x = anchor_widget.winfo_rootx()
        y = anchor_widget.winfo_rooty() + anchor_widget.winfo_height()
        w = anchor_widget.winfo_width()
        panel.geometry(f"{w}x0+{x}+{y}")

        def update_position(event=None):
            if not panel.winfo_exists():
                return
            anchor_widget.update_idletasks()
            x = anchor_widget.winfo_rootx()
            y = anchor_widget.winfo_rooty() + anchor_widget.winfo_height()
            w = anchor_widget.winfo_width()
            h = panel.winfo_height()
            panel.geometry(f"{w}x{h}+{x}+{y}")

        anchor_widget.bind("<Configure>", update_position)
        root.bind("<Configure>", update_position)

        _animate_expand(_panel, anchor_widget, target_h=PANEL_MAX_H, duration=1000)

    _text_box.config(state="normal")
    _text_box.delete("1.0", "end")

    _insert_field("Название", mod.get("name", ""))
    _insert_field("Автор", mod.get("author", ""))
    _insert_field("Версия", mod.get("version", ""))
    _insert_field("Язык", mod.get("language", ""))

    # Steam ID
    steam_id = mod.get("steam_id", "")
    if steam_id and steam_id.isdigit():
        _text_box.insert("end", "Steam ID: ", ("label",))
        tag = f"steam_{steam_id}"
        _text_box.insert("end", f"{steam_id}\n", (tag,))
        _text_box.tag_config(tag, foreground=LINK_FG, font=("TkDefaultFont", 11))
        _text_box.tag_bind(tag, "<Enter>", lambda e: _text_box.config(cursor="hand2"))
        _text_box.tag_bind(tag, "<Leave>", lambda e: _text_box.config(cursor=""))
        _text_box.tag_bind(tag, "<Button-1>", lambda e, sid=steam_id: _open_steam_id_folder(sid))
    elif steam_id:
        _insert_field("Steam ID", steam_id)

    # Ссылки
    links = mod.get("links", [])
    if links:
        _text_box.insert("end", "Ссылки:\n", ("label",))
        for i, url in enumerate(links):
            tag = f"link_{i}"
            _text_box.insert("end", f"{url}\n", (tag,))
            _text_box.tag_config(tag, foreground=LINK_FG, font=("TkDefaultFont", 11))
            _text_box.tag_bind(tag, "<Enter>", lambda e: _text_box.config(cursor="hand2"))
            _text_box.tag_bind(tag, "<Leave>", lambda e: _text_box.config(cursor=""))
            _text_box.tag_bind(tag, "<Button-1>", lambda e, u=url: webbrowser.open(u))

    _insert_field("Обновлено", mod.get("updated", ""))

    deps = mod.get("dependencies", [])
    if deps:
        _text_box.insert("end", "Зависимости:\n", ("label",))
        for d in deps:
            _text_box.insert("end", f"{d}\n", ("value",))

    _text_box.config(state="disabled")

    if _close_job and _panel and _panel.winfo_exists():
        _panel.after_cancel(_close_job)
    _close_job = _panel.after(10000, lambda: _animate_collapse(_panel, anchor_widget, duration=1000))


def _insert_field(label, value):
    if not value:
        return
    _text_box.insert("end", f"{label}: ", ("label",))
    _text_box.insert("end", f"{value}\n", ("value",))


def _open_steam_id_folder(steam_id):
    try:
        prog_dir = _get_prog_dir()  # теперь всегда корректный prog
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(prog_dir)))  # вверх на 3 уровня

        mods_path = os.path.join(base_dir, "MODS")
        steam_path = os.path.join(base_dir, "233860")

        if os.path.isdir(mods_path):
            # локал → поднимаемся на 2 уровня выше (до steamapps)
            parent_dir = os.path.dirname(os.path.dirname(base_dir))
            path = os.path.join(parent_dir, "workshop", "content", "233860", steam_id)

        elif os.path.isdir(steam_path):
            # стим → сразу в 233860
            path = os.path.join(steam_path, steam_id)

        else:
            print("[INFO] Ни MODS, ни 233860 не найдены (ошибка путей)")
            return

        if os.path.isdir(path):
            os.startfile(path)
        else:
            print(f"[INFO] Папка {path} не найдена")

    except Exception as e:
        print(f"[ERROR] open steam_id folder: {e}")


def _animate_expand(panel, anchor, target_h, duration=1000):
    steps = 20
    delay = duration // steps
    for i in range(steps + 1):
        h = int(target_h * (i / steps))
        panel.after(i * delay, lambda hh=h: _set_height(panel, anchor, hh))


def _animate_collapse(panel, anchor, duration=1000):
    global _panel, _text_box, _close_job
    steps = 20
    delay = duration // steps
    start_h = PANEL_MAX_H
    for i in range(steps + 1):
        h = int(start_h * (1 - i / steps))
        panel.after(i * delay, lambda hh=h: _set_height(panel, anchor, hh))

    panel.after(duration + 50, lambda: _destroy_panel())


def _destroy_panel():
    global _panel, _text_box, _close_job
    if _panel and _panel.winfo_exists():
        _panel.destroy()
    _panel = None
    _text_box = None
    _close_job = None


def _set_height(panel, anchor, h):
    if not panel.winfo_exists():
        return
    anchor.update_idletasks()
    x = anchor.winfo_rootx()
    y = anchor.winfo_rooty() + anchor.winfo_height()
    w = anchor.winfo_width()
    panel.geometry(f"{w}x{h}+{x}+{y}")


def _on_mousewheel(event, text_widget):
    text_widget.yview_scroll(int(-1 * (event.delta / 120)), "units")


def _get_mod_data(mods_file):
    if not os.path.exists(mods_file):
        return None
    try:
        with open(mods_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        mod_name = None
        for m in data.get("mods", []):
            if m.get("name") == "__panel_dummy__":
                mod_name = m.get("mod_name")
                break
        if not mod_name:
            return None

        for m in data.get("mods", []):
            if m.get("name") == mod_name:
                return m
    except:
        return None
    return None
