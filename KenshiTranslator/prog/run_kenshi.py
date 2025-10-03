import subprocess
from pathlib import Path
from tkinter import messagebox
import sys
import threading


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.argv[0]).resolve().parent  # рядом с KenshiTranslator.exe
    else:
        return Path(__file__).resolve().parent     # рядом с run_kenshi.py


def main():
    prog_dir = get_base_dir()
    parent2 = prog_dir.parent.parent

    exe = None

    # Проверка локала (mods)
    if parent2.name.lower() == "mods":
        base = parent2.parent  # Kenshi
        for candidate in ["Kenshi_x64.exe", "kenshi_GOG_x64.exe"]:
            exe_path = base / candidate
            if exe_path.exists():
                exe = exe_path
                break

    # Проверка стима (233860)
    elif parent2.name == "233860":
        steamapps = parent2.parent.parent.parent  # prog->3572656370->233860->content->workshop->steamapps
        base = steamapps / "common" / "Kenshi"
        for candidate in ["Kenshi_x64.exe", "kenshi_GOG_x64.exe"]:
            exe_path = base / candidate
            if exe_path.exists():
                exe = exe_path
                break

    if not exe:
        messagebox.showerror("Ошибка", "⚠ Kenshi не найден")
        return

    try:
        proc = subprocess.Popen([str(exe)], cwd=str(exe.parent))

        import __main__
        if hasattr(__main__, "root"):
            root = __main__.root
            root.after(2000, root.withdraw)

            def wait_and_exit():
                proc.wait()
                root.destroy()

            threading.Thread(target=wait_and_exit, daemon=True).start()

    except Exception as e:
        messagebox.showerror("Ошибка запуска Kenshi", str(e))


if __name__ == "__main__":
    main()
