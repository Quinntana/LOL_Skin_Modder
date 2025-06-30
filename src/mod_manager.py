import os
import subprocess
import winreg
import sys
from config import INSTALLED_DIR, PROFILE_FILE, INSTALL_DIR

CSLOL_TOOL_PATH = os.path.join(INSTALL_DIR,"cslol-tools"    , "mod-tools.exe")

def detect_game_path():
    """Attempt to detect the League of Legends game path on Windows."""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Riot Games, Inc\League of Legends") as key:
            path, _ = winreg.QueryValueEx(key, "Path")
            if os.path.exists(os.path.join(path, "League of Legends.exe")):
                return path
    except FileNotFoundError:
        pass
    default_path = r"C:\Riot Games\League of Legends"
    if os.path.exists(os.path.join(default_path, "League of Legends.exe")):
        return default_path
    return None

def validate_game_path(path):
    """Validate if the game path contains League of Legends.exe."""
    return os.path.exists(os.path.join(path, "League of Legends.exe"))

def get_available_mods():
    """Retrieve list of available mods from the installed directory."""
    mods = []
    if os.path.exists(INSTALLED_DIR):
        for item in os.listdir(INSTALLED_DIR):
            if os.path.isdir(os.path.join(INSTALLED_DIR, item)) and item != "META":
                mods.append(item)
    return sorted(mods)

def load_enabled_mods():
    """Load enabled mods from the default profile file."""
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

def save_enabled_mods(enabled_mods):
    """Save enabled mods to the default profile file."""
    os.makedirs(INSTALLED_DIR, exist_ok=True)
    with open(PROFILE_FILE, "w") as f:
        for mod in enabled_mods:
            f.write(f"{mod}\n")

def display_mods(available_mods, enabled_mods):
    """Display available and enabled mods."""
    print("\nAvailable Mods:")
    for i, mod in enumerate(available_mods, 1):
        status = "[Enabled]" if mod in enabled_mods else ""
        print(f"{i}. {mod} {status}")

def parse_selection(input_str, available_mods):
    """Parse user input for mod selection."""
    if input_str.lower() == "all":
        return available_mods
    try:
        indices = [int(i.strip()) - 1 for i in input_str.split(",") if i.strip()]
        return [available_mods[i] for i in indices if 0 <= i < len(available_mods)]
    except (ValueError, IndexError):
        print("Invalid selection. Proceeding with no changes.")
        return []

def run_patching(game_path, overlay_dir):
    """Run the CS LOL patching process."""
    cmd = [CSLOL_TOOL_PATH, "runoverlay", overlay_dir, PROFILE_FILE, "--game:", game_path]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        for line in process.stdout:
            print(line.strip())
        process.wait()
    except KeyboardInterrupt:
        print("\nPatching cancelled by user.")
        process.terminate()

def main():
    game_path = detect_game_path()
    if not game_path:
        game_path = input("Could not detect game path. Enter the game path (or 'test' for testing): ").strip()
        if game_path.lower() == "test":
            print("Warning: Running in test mode with a dummy game path.")
            game_path = "test_path"
        elif not validate_game_path(game_path):
            print("Warning: Invalid game path provided. Proceeding anyway for testing.")

    available_mods = get_available_mods()
    if not available_mods:
        print("No mods found in the 'installed' directory.")
        return

    enabled_mods = load_enabled_mods()
    display_mods(available_mods, enabled_mods)

    enable_input = input("\nSelect mods to enable (numbers separated by commas, or 'all'): ").strip()
    mods_to_enable = parse_selection(enable_input, available_mods)
    for mod in mods_to_enable:
        if mod not in enabled_mods:
            enabled_mods.append(mod)

    disable_input = input("Select mods to disable (numbers separated by commas, or 'all'): ").strip()
    mods_to_disable = parse_selection(disable_input, available_mods)
    enabled_mods = [mod for mod in enabled_mods if mod not in mods_to_disable]

    save_enabled_mods(enabled_mods)
    print("Profile updated with enabled mods:", ", ".join(enabled_mods) if enabled_mods else "None")

    overlay_dir = INSTALLED_DIR
    print("\nStarting patching process. Press Ctrl+C to cancel.")
    run_patching(game_path, overlay_dir)

if __name__ == "__main__":
    main()
