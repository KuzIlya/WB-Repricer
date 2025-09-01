import os
import sys
import platform
import subprocess

APP_NAME = "wb_helper"
ENTRY_POINT = "app/main.py"

def build():
    if not os.path.exists(ENTRY_POINT):
        print(f"❌ Entry point '{ENTRY_POINT}' не найден.")
        sys.exit(1)

    system = platform.system()
    print(f"🛠️ Сборка для: {system}")

    base_cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--name", APP_NAME,
    ]

    if system == "Windows":
        base_cmd.append("--windowed")
    else:
        print("🔍 Лог будет доступен в терминале.")

    base_cmd.append(ENTRY_POINT)

    try:
        subprocess.run(base_cmd, check=True)
        print(f"✅ Сборка завершена. Файл: dist/{APP_NAME}{'.exe' if system == 'Windows' else ''}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при сборке: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build()
