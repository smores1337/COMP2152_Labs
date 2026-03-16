import os
import sys
import platform

def display(title, data):
    print(f"\n--- {title} ---")
    for k, v in data.items():
        print(f"  {k:<12} : {v}")

def safe_run(label, func, *args):
    try:
        result = func(*args)
        if result is None:
            print(f"  [!] {label} returned None — missing return?")
            return {}
        return result
    except Exception as e:
        print(f"  [ERROR] {label}: {e}")
        return {}

def get_system_info():
    return {
        "os":      platform.system(),
        "node":    platform.node(),
        "release": platform.release(),
        "machine": platform.machine()
    }

def get_python_info():
    return {
        "version":    sys.version,
        "executable": sys.executable,
        "platform":   sys.platform
    }

def get_directory_info(path):
    exists = os.path.exists(path)
    return {
        "path":         os.path.abspath(path),
        "exists":       exists,
        "file_count":   len(os.listdir(path)) if exists else 0,
        "is_directory": os.path.isdir(path)
    }

if __name__ == "__main__":
    print("=" * 60)
    print("  SYSTEM INFORMATION REPORTER")
    print("=" * 60)

    info = safe_run("System Info", get_system_info)
    if info: display("System Info", info)

    info = safe_run("Python Info", get_python_info)
    if info: display("Python Info", info)