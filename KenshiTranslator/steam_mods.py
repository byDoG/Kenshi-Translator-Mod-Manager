import json
import re

import sys

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent.parent  # Kenshi
    else:
        return Path(__file__).resolve().parent.parent  # Kenshi


from pathlib import Path
import sys
from pathlib import Path

def get_json_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent   # KenshiTranslator
    else:
        return Path(__file__).resolve().parent         # KenshiTranslator


ALL_MODS_FILE = "mods_all.json"


def extract_mod_references(mod_file: Path):
    refs = []
    try:
        with open(mod_file, "rb") as f:
            data = f.read()
        matches = re.findall(rb"[A-Za-z0-9 \-\+\(\)_',!]+\.mod", data, flags=re.IGNORECASE)
        for m in matches:
            s = m.decode("latin-1", errors="ignore").strip()
            refs.append(s)
        refs = list(dict.fromkeys(refs))
    except Exception as e:
        refs = [f"ERROR: {e}"]
    return refs


def clean_refs(refs):
    blacklist = {
        "base,rebirth.mod",
        "rebirth.mod",
        "base,newwworld.mod",
        "newwworld.mod",
        "base,dialogue.mod",
        "dialogue.mod",
    }
    clean = []
    for r in refs:
        s = r.strip()
        if s.startswith(","):
            s = s[1:].strip()
        if s.lower().startswith("base,"):
            s = s[5:].strip()
        if re.match(r"^\d+-", s):
            continue
        if not s.lower().endswith(".mod"):
            continue
        if s.lower() in blacklist:
            continue
        clean.append(s)
    return clean


def main():
    base = get_base_dir()  # Kenshi
    steam_dir = base.parent.parent / "workshop" / "content" / "233860"
    print(f"[DEBUG] Ищу моды в {steam_dir}")

    all_json = get_json_dir() / ALL_MODS_FILE
    if all_json.exists():
        with open(all_json, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"mods": []}

    mods_dict = {m["name"]: m for m in data["mods"]}
    if not steam_dir.exists():
        print("[DEBUG] Папка Steam Workshop не найдена!")
        return

    found_any = False
    for mod_file in steam_dir.rglob("*.mod"):
        found_any = True
        name = mod_file.stem
        raw_deps = extract_mod_references(mod_file)
        deps = clean_refs(raw_deps)
        print(f"[STEAM] {name}: {len(deps)} deps")
        mods_dict[name] = {"name": name, "enabled": True, "dependencies": deps, "references": []}

    if not found_any:
        print("[DEBUG] В Workshop-папке нет .mod файлов!")

    data["mods"] = list(mods_dict.values())
    with open(all_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[DEBUG] Записано {len(data['mods'])} мод(ов) в {all_json}")


if __name__ == "__main__":
    main()