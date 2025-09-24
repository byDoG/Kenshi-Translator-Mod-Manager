import json
from KenshiTranslator import get_json_dir, ALL_MODS_FILE

def filter_deps(mods):
    """Фильтр: убираем .mod и выставляем sorting=false"""
    for mod in mods:
        clean = []
        for dep in mod.get("dependencies", []):
            dep = dep.removesuffix(".mod")
            if dep and dep not in clean:
                clean.append(dep)
        mod["dependencies"] = clean
        mod["sorting"] = False
    return mods


def order_mods():
    all_json = get_json_dir() / ALL_MODS_FILE
    if not all_json.exists():
        return

    with open(all_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    mods = data.get("mods", [])
    mods = filter_deps(mods)

    enabled = [m for m in mods if m.get("enabled", False)]
    disabled = [m for m in mods if not m.get("enabled", False)]

    ordered = []

    # Шаг 1 — Сироты
    orphans = [m for m in enabled if not m.get("dependencies")]
    orphans.sort(key=lambda x: x["name"].lower())
    for m in orphans:
        m["sorting"] = True
        ordered.append(m)

    # Шаг 2 — Heavy
    heavies = [m for m in enabled if len(m.get("dependencies", [])) >= 2]
    for m in heavies:
        deps = m.get("dependencies", [])
        ok = True
        for dep in deps:
            if dep == m["name"] or not any(x["name"] == dep for x in mods):
                ok = False
        if ok:
            ordered.append(m)
            m["sorting"] = True
        else:
            m["sorting"] = "unweighted"
            ordered.append(m)

    # Шаг 3 — Patch
    patches = [m for m in enabled if len(m.get("dependencies", [])) == 1]
    for m in patches:
        parent = m["dependencies"][0]
        if parent == m["name"] or not any(x["name"] == parent for x in mods):
            m["sorting"] = "unweighted"
            ordered.append(m)
        else:
            m["sorting"] = True
            idx = next((i for i, o in enumerate(ordered) if o["name"] == parent), None)
            if idx is not None:
                ordered.insert(idx + 1, m)
            else:
                ordered.append(m)

    # Шаг 4 — Unknown (собираем всё, что осталось без sorting=True)
    unknowns = [m for m in enabled if m.get("sorting") is not True]
    for m in unknowns:
        m["sorting"] = "unweighted"
    # убрать из already ordered, если затесались раньше
    ordered = [m for m in ordered if m not in unknowns]
    ordered.extend(unknowns)

    # Шаг 5 — Disabled
    disabled.sort(key=lambda x: x["name"].lower())
    ordered.extend(disabled)

    data["mods"] = ordered
    with open(all_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
