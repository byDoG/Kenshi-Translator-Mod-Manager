import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
from pathlib import Path
import zipfile
from datetime import datetime
import json
import os
import steam_mods
import local_mods
import order_mods
import run_kenshi
from pathlib import Path

def get_json_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent   # KenshiTranslator
    else:
        return Path(__file__).resolve().parent         # KenshiTranslator

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent.parent  # Kenshi
    else:
        return Path(__file__).resolve().parent.parent  # Kenshi

ICONS_DIR = "icons"
ALL_MODS_FILE = "mods_all.json"

DARK_BG = "#222222"
BTN_BG = "#2b2b2b"
BTN_ACTIVE = "#333333"
BTN_BORDER = "#555555"
BTN_BORDER_ACTIVE = "#666666"
BTN_FG = "white"
SEPARATOR_COLOR = "#555555"  # цвет разделителя

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kenshi Translator — BY D0G911")
        self.root.geometry("620x470")
        self.root.minsize(620, 460)
        self.root.configure(bg=DARK_BG)

        DEFAULT_FONT = ("Segoe UI", 10)
        root.option_add("*Font", DEFAULT_FONT)

        # иконки
        self.icon_checked = tk.PhotoImage(file=os.path.join(ICONS_DIR, "check.png"))
        self.icon_unchecked = tk.PhotoImage(file=os.path.join(ICONS_DIR, "cross.png"))
        self.icon_warning = tk.PhotoImage(file=os.path.join(ICONS_DIR, "warning.png"))

        # статусная строка
        self.status = tk.StringVar(value="Ready")
        tk.Label(root, textvariable=self.status, bg=DARK_BG, fg="white").pack(anchor="w", padx=5, pady=2)

        # контейнер
        container = tk.Frame(root, bg=DARK_BG)
        container.pack(fill="both", expand=True)

        # таблица + скроллбар
        tree_frame = tk.Frame(container, bg=DARK_BG)
        tree_frame.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=DARK_BG,
                        fieldbackground=DARK_BG,
                        foreground="white")
        style.configure("Treeview.Heading",
                        background=DARK_BG,
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[("active", BTN_ACTIVE)])
        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background=DARK_BG,
                        darkcolor=DARK_BG,
                        lightcolor=DARK_BG,
                        troughcolor=DARK_BG,
                        bordercolor=DARK_BG,
                        arrowcolor="white")
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

        self.root.option_add("*TCombobox*Listbox*Background", DARK_BG)
        self.root.option_add("*TCombobox*Listbox*Foreground", "white")
        self.root.option_add("*TCombobox*Listbox*selectBackground", BTN_ACTIVE)
        self.root.option_add("*TCombobox*Listbox*selectForeground", "white")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("lang", "progress"),
            show="tree headings",
            height=18
        )

        self.tree.heading("#0", text="Enabled (0 Mods)")
        self.tree.column("#0", width=300, anchor="w")
        self.tree.heading("lang", text="Language")
        self.tree.column("lang", width=90, anchor="center")
        self.tree.heading("progress", text="Progress")
        self.tree.column("progress", width=90, anchor="center")

        yscroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=yscroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")

        self.tree.bind("<ButtonPress-1>", self.on_drag_start)
        self.tree.bind("<B1-Motion>", self.on_drag_motion)
        self.tree.bind("<ButtonRelease-1>", self.on_drag_drop)
        self.tree.bind("<Double-1>", self.toggle_mod)

        # панель справа
        frame = tk.Frame(container, bg=DARK_BG)
        frame.pack(side="right", fill="y", padx=8, pady=5)

        self.steam_btn = self.make_button(frame, "Steam Mods", self.run_steam)
        self.local_btn = self.make_button(frame, "Local Mods", self.run_local)
        self.load_cfg_btn = self.make_button(frame, "Load CFG", self.load_from_cfg)
        self.sorting_btn = self.make_button(frame, "Sorting Mods", self.sort_mods)
        self.save_btn = self.make_button(frame, "Save CFG", self.save_config)
        self.clear_btn = self.make_button(frame, "Clear", self.clear_mods)

        self.make_separator(frame)

        translators = ["ChatGPT", "Google", "Google2", "Microsoft", "Yandex", "DeepL"]
        self.translator_choice = tk.StringVar(value=translators[0])
        self.translator_menu = ttk.Combobox(frame, textvariable=self.translator_choice,
                                            values=translators, state="readonly", width=12)
        self.translator_menu.pack(pady=5)

        langs = ["English", "German", "French", "Spanish", "Italian",
                 "Japanese", "Chinese", "Korean", "Portuguese", "Ukrainian", "Russian"]
        self.source_lang = tk.StringVar(value="English")
        self.source_menu = ttk.Combobox(frame, textvariable=self.source_lang,
                                        values=langs, state="readonly", width=12)
        self.source_menu.pack(pady=5)
        self.target_lang = tk.StringVar(value="Russian")
        self.target_menu = ttk.Combobox(frame, textvariable=self.target_lang,
                                        values=langs, state="readonly", width=12)
        self.target_menu.pack(pady=5)

        self.make_separator(frame)
        self.translate_btn = self.make_button(frame, "Translate", self.translate_mod)
        self.exit_btn = self.make_button(frame, "Exit", self.root.quit)

        self.make_separator(frame)
        self.start_btn = self.make_button(frame, "Start Kenshi", run_kenshi.main)

        self.dragging_item = None
        self.separator_line = None

    def make_button(self, parent, text, cmd):
        btn = tk.Button(parent,
                        text=text,
                        command=cmd,
                        width=14,
                        bg=BTN_BG, fg=BTN_FG,
                        activebackground=BTN_ACTIVE,
                        activeforeground=BTN_FG,
                        disabledforeground=BTN_BG,
                        relief="solid", bd=1,
                        highlightbackground=BTN_BORDER,
                        highlightcolor=BTN_BORDER_ACTIVE,
                        highlightthickness=1)
        btn.pack(pady=3)
        return btn

    def make_separator(self, parent):
        tk.Frame(parent, height=1, width=120, bg="#444444").pack(pady=5)

    # ======================
    #  ЛОГИКА МОДОВ
    # ======================

    def refresh_mods(self, mods):
        self.tree.delete(*self.tree.get_children())
        enabled = [m for m in mods if m.get("enabled")]
        disabled = [m for m in mods if not m.get("enabled")]

        self.tree.heading("#0", text=f"Enabled ({len(enabled)} Mods)")

        for mod in enabled:
            icon = self.icon_warning if mod.get("sorting") == "unweighted" else self.icon_checked
            self.tree.insert("", "end", image=icon, text=mod["name"], values=("?", "0%"), tags=("enabled",))

        if enabled and disabled:
            self.root.after(50, self.place_separator, len(enabled))

        for mod in disabled:
            self.tree.insert("", "end", image=self.icon_unchecked, text=mod["name"],
                             values=("?", "0%"), tags=("disabled",))

    def place_separator(self, enabled_count):
        if self.separator_line:
            self.separator_line.destroy()
        last_enabled = self.tree.get_children()[enabled_count - 1]
        bbox = self.tree.bbox(last_enabled)
        if not bbox:
            return
        x, y, w, h = bbox
        self.separator_line = tk.Frame(self.tree, bg=SEPARATOR_COLOR, height=1)
        self.separator_line.place(x=0, y=y + h, width=self.tree.winfo_width())
        self.tree.bind("<Configure>", lambda e: self.separator_line.place(x=0, y=y + h, width=e.width))

    def load_from_cfg(self):
        base = get_base_dir()
        cfg_file = base / "data" / "mods.cfg"
        enabled_mods = []
        if cfg_file.exists():
            with open(cfg_file, "r", encoding="utf-8") as f:
                enabled_mods = [line.strip().removesuffix(".mod") for line in f if line.strip()]
        all_json = get_json_dir() / ALL_MODS_FILE
        if not all_json.exists():
            messagebox.showerror("Ошибка", "mods_all.json не найден")
            return
        with open(all_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        for mod in data["mods"]:
            mod["enabled"] = mod["name"] in enabled_mods
        with open(all_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.refresh_mods(data["mods"])
        self.status.set("✅ Загружено из mods.cfg")

    def load_from_json(self):
        all_json = get_json_dir() / ALL_MODS_FILE
        if not all_json.exists():
            self.status.set("❌ mods_all.json not found")
            return
        with open(all_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.refresh_mods(data.get("mods", []))
        self.status.set("✅ Loaded from mods_all.json")

    def run_steam(self):
        self.status.set("Загрузка Steam модов...")
        self.root.after(100, self._run_steam)

    def _run_steam(self):
        steam_mods.main()
        self.load_from_json()
        self.status.set("✅ Steam моды добавлены")

    def run_local(self):
        self.status.set("Загрузка Local модов...")
        self.root.after(100, self._run_local)

    def _run_local(self):
        local_mods.main()
        self.load_from_json()
        self.status.set("✅ Local моды добавлены")

    def clear_mods(self):
        self.tree.delete(*self.tree.get_children())
        all_json = get_json_dir() / ALL_MODS_FILE
        if all_json.exists():
            try:
                all_json.unlink()
                self.status.set("🗑️ Список и mods_all.json очищены")
            except Exception as e:
                self.status.set(f"⚠️ Ошибка при удалении mods_all.json: {e}")
        else:
            self.status.set("Список очищен (mods_all.json не найден)")

    def toggle_mod(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        mod_name = self.tree.item(item, "text")
        all_json = get_json_dir() / ALL_MODS_FILE
        if not all_json.exists():
            return
        with open(all_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        for mod in data["mods"]:
            if mod["name"] == mod_name:
                mod["enabled"] = not mod.get("enabled", False)
                break
        with open(all_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.refresh_mods(data["mods"])

    # --- Save Config (fixed backups) ---
    def save_config(self):
        self.save_btn.config(state="disabled")
        self.status.set("Сохранение mods.cfg...")

        base = get_base_dir()
        data_dir = base / "data"
        cfg_file = data_dir / "mods.cfg"

        enabled_mods = []
        all_json = get_json_dir() / ALL_MODS_FILE
        if all_json.exists():
            with open(all_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                enabled_mods = [m["name"] for m in data.get("mods", []) if m.get("enabled", False)]

        with open(cfg_file, "w", encoding="utf-8") as f:
            for mod in enabled_mods:
                f.write(mod + ".mod\n")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        backup_dir = get_json_dir()
        backup_dir.mkdir(exist_ok=True)

        backup_zip = backup_dir / f"backup-{timestamp}-cfg.zip"
        with zipfile.ZipFile(backup_zip, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(cfg_file, "mods.cfg")

        backups = sorted(backup_dir.glob("backup-*-cfg.zip"),
                         key=os.path.getmtime, reverse=True)
        for old in backups[5:]:
            try:
                old.unlink()
            except Exception:
                pass

        self.status.set(f"✅ Saved {len(enabled_mods)} mods, CFG → {backup_zip.name}")
        self.save_btn.config(state="normal")

    def translate_mod(self):
        item = self.tree.focus()
        if not item:
            return
        mod_name = self.tree.item(item, "text")
        messagebox.showinfo("Translate", f"Переводим {mod_name}... (заглушка)")

    def sort_mods(self):
        self.status.set("✨ Запуск сортировки модов...")
        self.root.update_idletasks()
        try:
            order_mods.order_mods()
            self.load_from_json()
            self.status.set("✅ Сортировка завершена (сохраните через Save CFG)")
        except Exception as e:
            self.status.set(f"❌ Ошибка сортировки: {e}")

    def on_drag_start(self, event):
        self.dragging_item = self.tree.identify_row(event.y)

    def on_drag_motion(self, event):
        if not self.dragging_item:
            return
        target_item = self.tree.identify_row(event.y)
        if not target_item:
            return
        self.tree.selection_set(target_item)

    def on_drag_drop(self, event):
        if not self.dragging_item:
            return
        try:
            target_item = self.tree.identify_row(event.y)
            if not target_item or target_item == self.dragging_item:
                return
            to_index = self.tree.index(target_item)
            mod_name = self.tree.item(self.dragging_item, "text")
            mod_tags = self.tree.item(self.dragging_item, "tags")
            mod_enabled = "enabled" in mod_tags

            self.tree.delete(self.dragging_item)
            self.tree.insert("", to_index,
                             image=self.icon_checked if mod_enabled else self.icon_unchecked,
                             text=mod_name,
                             values=("?", "0%"),
                             tags=("enabled",) if mod_enabled else ("disabled",))

            all_json = get_json_dir() / ALL_MODS_FILE
            mods_all = []
            for child in self.tree.get_children():
                name = self.tree.item(child, "text")
                tags = self.tree.item(child, "tags")
                mods_all.append({"name": name, "enabled": "enabled" in tags})
            with open(all_json, "w", encoding="utf-8") as f:
                json.dump({"mods": mods_all}, f, ensure_ascii=False, indent=2)
            self.refresh_mods(mods_all)
        except tk.TclError:
            pass
        finally:
            self.dragging_item = None

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
