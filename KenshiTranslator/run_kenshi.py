import subprocess
from pathlib import Path
from tkinter import messagebox
import sys
import threading


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent.parent
    else:
        return Path(__file__).resolve().parent.parent


def main():
    base = get_base_dir()
    exe = base / "kenshi_x64.exe"

    if not exe.exists():
        messagebox.showerror("Ошибка", "⚠ Kenshi не найден")
        return

    try:
        proc = subprocess.Popen([str(exe)], cwd=str(base))

        import __main__
        if hasattr(__main__, "root"):
            root = __main__.root

            # спрятать окно через 2 сек
            root.after(2000, root.withdraw)

            # ждать завершение Kenshi и только тогда закрыться
            def wait_and_exit():
                proc.wait()
                root.destroy()

            threading.Thread(target=wait_and_exit, daemon=True).start()

    except Exception as e:
        messagebox.showerror("Ошибка запуска Kenshi", str(e))
