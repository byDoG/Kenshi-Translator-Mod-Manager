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
    """Читает .mod файл как бинарный и вытаскивает все строки с .mod"""
    refs = []
    try:
        with open(mod_file, "rb") as f:
            data = f.read()

        # ищем все подпоследовательности, заканчивающиеся на .mod
        matches = re.findall(rb"[A-Za-z0-9 \-\+\(\)_',!]+\.mod", data, flags=re.IGNORECASE)
        for m in matches:
            s = m.decode("latin-1", errors="ignore").strip()
            refs.append(s)

        # убираем дубли, сохраняя порядок
        refs = list(dict.fromkeys(refs))

    except Exception as e:
        refs = [f"ERROR: {e}"]

    return refs


def clean_refs(refs):
    """Удаляем мусор: ID-шники, ведущие запятые, системные моды и префикс base,"""
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

        # убираем ведущую запятую
        if s.startswith(","):
            s = s[1:].strip()

        # убираем префикс base, (если он остался у обычного мода)
        if s.lower().startswith("base,"):
            s = s[5:].strip()

        # выкидываем строки, начинающиеся с числа и дефиса (5008195-Sailback.mod)
        if re.match(r"^\d+-", s):
            continue

        # оставляем только если заканчивается на .mod
        if not s.lower().endswith(".mod"):
            continue

        # убираем системные моды (из blacklist)
        if s.lower() in blacklist:
            continue

        clean.append(s)
    return clean


def main():
    # 📂 ищем Kenshi/mods (один уровень выше KenshiTranslator)
    base = get_base_dir()
    mods_dir = base / "mods"
    print(f"[DEBUG] Ищу моды в {mods_dir}")

    all_json = get_json_dir() / ALL_MODS_FILE
    if all_json.exists():
        with open(all_json, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"mods": []}

    mods_dict = {m["name"]: m for m in data["mods"]}

    if not mods_dir.exists():
        print("[DEBUG] Папка mods не найдена!")
        return

    found_any = False
    for mod_file in mods_dir.rglob("*.mod"):
        found_any = True
        name = mod_file.stem
        raw_deps = extract_mod_references(mod_file)
        deps = clean_refs(raw_deps)

        print(f"[LOCAL] {name}: {len(deps)} deps")

        mods_dict[name] = {
            "name": name,
            "enabled": True,
            "dependencies": deps,
            "references": [],  # пока пусто
        }

    if not found_any:
        print("[DEBUG] В папке и подпапках нет .mod файлов!")

    data["mods"] = list(mods_dict.values())
    with open(all_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[DEBUG] Записано {len(data['mods'])} мод(ов) в {all_json}")


if __name__ == "__main__":
    main()