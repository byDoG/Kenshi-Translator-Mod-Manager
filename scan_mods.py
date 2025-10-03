import json
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path
import tkinter as tk
import __main__
import sys

ALL_MODS_FILE = "mods_all.json"
SETTINGS_FILE = "settings.json"

BASE_DEPENDENCIES = {
    "gamedata.base",
    "rebirth.mod",
    "dialogue.mod",
    "newwworld.mod"
}

SYSTEM_NAMES = {"rebirth", "gamedata", "dialogue", "newwworld", "rebirthmod", "gamedatabaserebirthmod"}

def show_msg(text, timeout=3000):
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
    canvas.create_text(win_w // 2, win_h // 2, text=text,
                       fill="white", font=("Arial", 20, "bold"))

    def close_and_exit():
        root.destroy()
        try:
            if hasattr(__main__, "root"):
                __main__.root.destroy()
        except Exception:
            sys.exit(1)

    root.after(timeout, close_and_exit)
    root.mainloop()

def get_prog_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    else:
        return Path(__file__).resolve().parent

def clean_author(decoded: str) -> str:
    decoded = decoded.strip()
    m = re.match(r"^[A-Za-z0-9 _\-\.\*']+", decoded)
    if m:
        decoded = m.group(0)
    decoded = decoded.strip()

    # пусто
    if not decoded:
        return "Unknown"

    # системные имена
    if decoded.lower() in SYSTEM_NAMES:
        return "Unknown"

    # короткие/мусорные ники (менее 3 символов)
    if len(decoded) < 3:
        return "Unknown"

    # явный мусор
    if "\u0000" in decoded or "gamedata.base" in decoded.lower() or "rebirth.mod" in decoded.lower():
        return "Unknown"

    return decoded

def parse_mod_binary(mod_file: Path):
    try:
        with open(mod_file, "rb") as f:
            header = f.read(200*1024)

        build, version = 0, 0
        version_bytes = header[1:9]
        if len(version_bytes) == 8:
            raw_build, raw_version = struct.unpack("<II", version_bytes)
            build = version_bytes[3]
            version = version_bytes[-1]

        deps = []
        if len(header) >= 0x14:
            dep_block_size = struct.unpack("<I", header[0x10:0x14])[0]
            dep_block = header[0x14:0x14+dep_block_size]
            refs = re.findall(rb"[A-Za-z0-9 _'\-!]+\.mod", dep_block, flags=re.IGNORECASE)
            for r in refs:
                d = r.decode("ascii", errors="ignore").strip()
                d_low = d.lower()
                if re.match(r"^\d+-", d):
                    continue
                if d_low in BASE_DEPENDENCIES:
                    continue
                deps.append(d)
            deps = list(dict.fromkeys(deps))

        author = "Unknown"
        if len(header) > 0x1C:
            block = header[0x0C:0x0C+32]
            counter = struct.unpack("<I", block[0:4])[0]

            if 1 <= counter <= 16:
                raw_name = block[4:4+counter]
                try:
                    decoded = raw_name.decode("ascii", errors="ignore")
                except:
                    decoded = ""
                author = clean_author(decoded)
            else:
                try:
                    decoded = block.decode("ascii", errors="ignore")
                except:
                    decoded = ""
                author = clean_author(decoded)

        lang = "Unknown"
        text = header.decode("ascii", errors="ignore")
        if re.search(r"[А-Яа-яЁё]", text):
            lang = "RU"
        elif "RU" in text.upper():
            lang = "RU"
        elif "EN" in text.upper():
            lang = "EN"

        is_animation = b".skeleton" in header.lower()

        return author, build, version, lang, is_animation, deps
    except Exception as e:
        print(f"[BINARY PARSE ERROR] {mod_file}: {e}")
        return "Unknown", 0, 0, "Unknown", False, []

def parse_info(info_file: Path):
    data = {
        "steam_id": "",
        "name": "",
        "tags": [],
        "updated": ""
    }
    try:
        tree = ET.parse(info_file)
        root = tree.getroot()
        sid = root.findtext("id")
        name = root.findtext("title") or root.findtext("mod")
        tags = [t.text for t in root.findall("tags/string") if t.text]
        updated = root.findtext("lastUpdate")

        data["steam_id"] = sid or ""
        data["name"] = name or ""
        data["tags"] = tags or []
        data["updated"] = updated or ""
    except Exception as e:
        print(f"[INFO PARSE ERROR] {info_file}: {e}")
    return data

def extract_links(mod_file: Path):
    links = []
    try:
        with open(mod_file, "rb") as f:
            data = f.read()
        url_pattern = re.compile(
            rb"(https?://[^\s\"']*(?:nexusmods\.com|github\.com)[^\s\"']*)",
            flags=re.IGNORECASE,
        )
        raw_urls = url_pattern.findall(data)
        decoded = []
        for b in raw_urls:
            try:
                s = b.decode("ascii", errors="ignore").strip().replace("\x00", "")
                if s:
                    decoded.append(s)
            except Exception:
                continue
        links = list(dict.fromkeys(decoded))
    except Exception as e:
        print(f"[LINK PARSE ERROR] {mod_file}: {e}")
    return links

def normalize_link(url: str) -> str:
    url = re.sub(r"\[/?[^\]]+\]", "", url).strip()
    m_prof = re.match(r"(https?://(?:www\.|next\.)?nexusmods\.com/profile/([A-Za-z0-9_-]+))/mods", url)
    if m_prof:
        return f"https://www.nexusmods.com/profile/{m_prof.group(2)}/mods"
    m_mod = re.match(r"(https?://(?:www\.|next\.)?nexusmods\.com/kenshi/mods/(\d+))", url)
    if m_mod:
        return f"https://www.nexusmods.com/kenshi/mods/{m_mod.group(2)}"
    return url

def make_dummy():
    return {
        "name": "__panel_dummy__",
        "dummy": True,
        "mod_name": "",
    }

def ensure_dummy(mods_list):
    mods_list = [m for m in mods_list if m.get("name") != "__panel_dummy__"]
    mods_list.insert(0, make_dummy())
    return mods_list

def build_entry(mod_file: Path, info_file: Path):
    info = parse_info(info_file) if info_file and info_file.exists() else {}
    info_tags = info.get("tags", [])

    author, build, version, language, is_animation, deps = parse_mod_binary(mod_file)

    tags_list = []
    if is_animation:
        if deps:
            tags_list.extend(info_tags)
            if "Animation" not in tags_list:
                tags_list.append("Animation")
        else:
            tags_list.append("Animation")
            for t in info_tags:
                if t not in tags_list:
                    tags_list.append(t)
    else:
        tags_list.extend(info_tags)

    links = []
    steam_id = info.get("steam_id", "").strip()
    if steam_id and steam_id.isdigit():
        links.append(f"https://steamcommunity.com/sharedfiles/filedetails/?id={steam_id}")
    for l in extract_links(mod_file):
        clean = normalize_link(l)
        if clean and clean not in links:
            links.append(clean)

    tags_str = ", ".join(tags_list)

    entry = {
        "name": mod_file.name,
        "enabled": True,
        "author": author,
        "build": build,
        "version": version,
        "language": language,
        "steam_id": steam_id,
        "tags": tags_str,
        "links": links,
        "updated": info.get("updated", ""),
        "references": [],
        "dependencies": deps
    }
    return entry

def scan_dir(mods_dir: Path, mods_dict: dict, tag: str):
    if not mods_dir or not mods_dir.exists():
        print(f"[{tag}] ПАПКА {mods_dir} НЕ НАЙДЕНА")
        return mods_dict, 0
    found = 0
    for sub in mods_dir.iterdir():
        if sub.is_dir():
            for mod_file in sub.glob("*.mod"):
                repo = mod_file.parent
                info_files = list(repo.glob("*.info"))
                info_file = info_files[0] if info_files else None
                entry = build_entry(mod_file, info_file)
                mods_dict[entry["name"]] = entry
                print(f"[{tag}] {entry['name']}: build {entry['build']} v{entry['version']} by {entry['author']}")
                found += 1
    if found == 0:
        print(f"[{tag}] В ПАПКЕ {mods_dir} НЕТ .mod ФАЙЛОВ!")
    return mods_dict, found

def main():
    prog_dir = get_prog_dir()
    root_dir = prog_dir.parent.parent

    settings = prog_dir / SETTINGS_FILE
    if not settings.exists():
        show_msg("ERROR SETTINGS NOT FOUND", 3000)
        return

    with open(settings, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    if not cfg.get("steam", False) and not cfg.get("local", False):
        show_msg("MODS NOT FOUND", 3000)
        return

    all_json = prog_dir / ALL_MODS_FILE
    if all_json.exists():
        with open(all_json, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"mods": []}

    mods_dict = {m["name"]: m for m in data.get("mods", []) if "name" in m}

    total_found = 0

    if cfg.get("steam", False):
        steam_dir = root_dir.parent.parent.parent / "workshop" / "content" / "233860"
        mods_dict, found = scan_dir(steam_dir, mods_dict, "STEAM")
        total_found += found

    if cfg.get("local", False):
        local_dir = root_dir.parent.parent.parent / "common" / "Kenshi" / "mods"
        mods_dict, found = scan_dir(local_dir, mods_dict, "LOCAL")
        total_found += found

    mods_list = list(mods_dict.values())

    if total_found == 0:
        mods_list = []
    mods_list = ensure_dummy(mods_list)

    data["mods"] = mods_list
    with open(all_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    if total_found == 0:
        show_msg("MODS NOT FOUND", 3000)
        return

    print(f"[SCAN] ЗАПИСАНО {len(data['mods'])} МОД(ОВ) В {all_json}")
    return len(data["mods"])

if __name__ == "__main__":
    main()
