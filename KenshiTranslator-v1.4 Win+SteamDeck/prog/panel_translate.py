import tkinter as tk
from tkinter import ttk
import json
import os

# Цвета и стили как в основном GUI
DARK_BG = "#222222"
BTN_BG = "#2b2b2b"
BTN_ACTIVE = "#333333"
BTN_BORDER = "#555555"
BTN_BORDER_ACTIVE = "#666666"
BTN_FG = "white"

SETTINGS_FILE = "settings.json"
LANG_FILE = "lang.json"

# === безопасная загрузка языка ===
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


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


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
    btn.pack(pady=3)
    return btn


def show_panel(root, app):
    panel_width = 118
    panel_height = 480

    panel = tk.Frame(root, width=panel_width, height=panel_height, bg=DARK_BG)
    panel.place(x=root.winfo_width(), y=0)
    panel.pack_propagate(False)

    # ===== Верхний бар =====
    top_bar = tk.Frame(panel, bg=DARK_BG, height=24)
    top_bar.pack(fill="x", side="top")

    author = tk.Label(top_bar, text=LANG.get("buttons", {}).get("7", ""),
                      bg=DARK_BG, fg="red", font=("Segoe UI", 10, "bold"))
    author.pack(side="right", padx=5)

    # ===== Фрейм для элементов =====
    content_frame = tk.Frame(panel, bg=DARK_BG)
    content_frame.pack(fill="both", expand=True, padx=8, pady=5)

    DEFAULT_FONT = ("Segoe UI", 10)
    root.option_add("*Font", DEFAULT_FONT)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TCombobox",
                    fieldbackground=DARK_BG,
                    background=DARK_BG,
                    foreground="white",
                    selectbackground=BTN_ACTIVE,
                    selectforeground="white",
                    arrowcolor="white")
    style.map("TCombobox",
              fieldbackground=[("readonly", DARK_BG)],
              foreground=[("readonly", "white")])

    root.option_add("*TCombobox*Listbox*Background", DARK_BG)
    root.option_add("*TCombobox*Listbox*Foreground", "white")
    root.option_add("*TCombobox*Listbox*selectBackground", BTN_ACTIVE)
    root.option_add("*TCombobox*Listbox*selectForeground", "white")

    # --- Кнопки сверху: Scan и Clear ---
    make_button(content_frame, LANG.get("buttons", {}).get("1", ""), cmd=app.scan_btn.invoke)
    make_button(content_frame, LANG.get("buttons", {}).get("5", ""), cmd=app.clear_btn.invoke)

    # --- Данные для комбобоксов ---
    translators = ["ChatGPT", "Google2", "Microsoft", "Yandex", "DeepL"]
    langs = [
        "English",
        "Deutsch",
        "Français",
        "Español",
        "Italiano",
        "日本語",
        "中文",
        "한국어",
        "Português",
        "Українська",
        "Русский"
    ]

    settings = load_settings()
    if "translator" not in settings:
        settings["translator"] = "ChatGPT"
    if "source_lang" not in settings:
        settings["source_lang"] = "English"
    if "target_lang" not in settings:
        settings["target_lang"] = "Русский"
    save_settings(settings)

    translator_choice = tk.StringVar(value=settings["translator"])
    source_lang = tk.StringVar(value=settings["source_lang"])
    target_lang = tk.StringVar(value=settings["target_lang"])

    translator_menu = ttk.Combobox(content_frame, textvariable=translator_choice,
                                   values=translators, state="readonly", width=12)
    translator_menu.pack(pady=5)

    source_menu = ttk.Combobox(content_frame, textvariable=source_lang,
                               values=langs, state="readonly", width=12)
    source_menu.pack(pady=5)

    target_menu = ttk.Combobox(content_frame, textvariable=target_lang,
                               values=langs, state="readonly", width=12)
    target_menu.pack(pady=5)

    def update_settings(event=None):
        settings["translator"] = translator_choice.get()
        settings["source_lang"] = source_lang.get()
        settings["target_lang"] = target_lang.get()
        save_settings(settings)

    translator_menu.bind("<<ComboboxSelected>>", update_settings)
    source_menu.bind("<<ComboboxSelected>>", update_settings)
    target_menu.bind("<<ComboboxSelected>>", update_settings)

    # --- Кнопки действий ---
    make_button(content_frame, LANG.get("buttons", {}).get("10", ""))
    make_button(content_frame, LANG.get("buttons", {}).get("11", ""))
    make_button(content_frame, LANG.get("buttons", {}).get("12", ""))
    make_button(content_frame, LANG.get("buttons", {}).get("13", ""))

    # --- Back и Exit ---
    back_btn = make_button(content_frame, LANG.get("buttons", {}).get("14", ""))
    exit_btn = make_button(content_frame, LANG.get("buttons", {}).get("9", ""), cmd=app.exit_btn.invoke)

    # ===== Анимация =====
    def animate_in(x):
        target_x = root.winfo_width() - panel_width
        if x > target_x:
            panel.place(x=x, y=0)
            root.after(15, animate_in, x - 10)
        else:
            panel.place(x=target_x, y=0)

    def animate_out(x):
        end_x = root.winfo_width()
        if x < end_x:
            panel.place(x=x, y=0)
            root.after(15, animate_out, x + 10)
        else:
            panel.destroy()

    back_btn.configure(command=lambda: animate_out(root.winfo_width() - panel_width))
    animate_in(root.winfo_width())
