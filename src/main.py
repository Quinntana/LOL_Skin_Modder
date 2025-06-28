import os
import time
import shutil
import subprocess
import ctypes
from ctypes import wintypes
from config import PROJECT_ROOT, DOWNLOAD_DIR, INSTALL_DIR, LOG_DIR, DATA_DIR
from logger import setup_logger
from champions import get_current_champion, get_champion_names
from skin_downloader import download_repo
from skin_installer import install_skins
from update_checker import check_and_update

APP_MUTEX_NAME = "{LeagueSkinManagerVN}"

logger = setup_logger(__name__)

def verify_paths():
    """Ensure all required directories exist"""
    required_dirs = [DOWNLOAD_DIR, INSTALL_DIR, LOG_DIR]
    for directory in required_dirs:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Verified directory: {directory}")

def ensure_single_instance():
    """Ensure only one instance of the application runs at a time"""
    logger.info("Checking for existing application instance...")

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    CreateMutexW = kernel32.CreateMutexW
    CreateMutexW.argtypes = [wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR]
    CreateMutexW.restype = wintypes.HANDLE

    mutex = CreateMutexW(None, False, APP_MUTEX_NAME)
    if not mutex:
        error_code = ctypes.get_last_error()
        logger.error(f"Failed to create mutex. Error code: {error_code}")
        return False

    last_error = ctypes.get_last_error()
    if last_error == 0x000000B7:
        logger.warning("Another instance of the application is already running.")
        return False

    logger.info("No other instance detected. Continuing.")
    return True


def process_champion(champion, skip_chromas=False):
    """Full processing pipeline for a champion"""
    logger.info(f"Processing {champion}")

    if not download_repo():
        logger.error("Failed to download skins repository")
        return 0

    installed = install_skins(champion, skip_chromas)
    logger.info(f"Installed {installed} skins for {champion}")
    return installed

def factory_reset():
    """Reset all downloaded and installed content"""
    logger.info("Performing factory reset")

    try:
        if os.path.exists(DATA_DIR):
            shutil.rmtree(DATA_DIR)
            os.makedirs(DOWNLOAD_DIR)
            os.makedirs(INSTALL_DIR)
            logger.info("Reset CSLOL Manager installation")

        return True
    except Exception as e:
        logger.error(f"Factory reset failed: {e}")
        return False

def main_menu():
    """Command-line interface"""
    print("\nLeague Skin Manager VN")
    print("1. Install skins for a single champion (with chromas)")
    print("2. Install skins for all champions")
    print("3. Factory reset")
    print("4. Open CSLOL Manager")
    print("5. Exit")

    while True:
        choice = input("\nSelect option: ").strip()

        if choice == "1":
            champion = get_current_champion()
            if not champion:
                print("Champion detection failed. Enter manually:")
                champion = input("Champion name: ").strip()

            if champion:
                process_champion(champion, skip_chromas=False)
            else:
                print("Invalid champion name")

        elif choice == "2":
            print("\nWARNING: Installing chromas for all champions may cause CSLOL Manager to become slow/laggy.")
            print("If CSLOL Manager becomes unresponsive, perform a Factory Reset (option 3).")

            install_chromas = ""
            while install_chromas.lower() not in ["y", "n"]:
                install_chromas = input("Include chromas? (y/n): ").strip()

            skip_chromas = (install_chromas.lower() == "n")

            champions = get_champion_names()
            if not champions:
                print("Failed to get champion list")
                continue

            print(f"Found {len(champions)} champions")
            start = time.time()

            for i, champ in enumerate(champions, 1):
                print(f"\nProcessing {i}/{len(champions)}: {champ}")
                process_champion(champ, skip_chromas=skip_chromas)

            print(f"\nCompleted in {time.time()-start:.1f} seconds")

        elif choice == "3":
            if factory_reset():
                print("Reset complete")
                return
            else:
                print("Reset failed - see logs for details")
                return

        elif choice == "4":
            try:
                cslol_path = os.path.join(INSTALL_DIR, "cslol-manager.exe")

                if os.path.exists(cslol_path):
                    print(f"Launching CSLOL Manager")
                    subprocess.Popen([cslol_path], shell=True)
                else:
                    print("CSLOL Manager not found. Please install it first.")
            except Exception as e:
                logger.error(f"Failed to launch CSLOL Manager: {e}")
                print(f"Error launching CSLOL Manager: {e}")

        elif choice == "5":
            return

        else:
            print("Invalid option")

if __name__ == "__main__":
    try:
        if not ensure_single_instance():
            print("Cannot run multiple instances")
            exit(1)

        verify_paths()
        os.chdir(PROJECT_ROOT)
        print("Checking for updates...")
        update_result = check_and_update()
        if update_result['lol_version_changed']:
            print("Skins have been reset")
        if update_result['manager_updated']:
            print("CSLOL Manager updated successfully")

        main_menu()
    except KeyboardInterrupt:
        print("\nOperation cancelled")
    except Exception as e:
        logger.exception("Critical error occurred")
        print(f"Error: {e}\nSee logs for details")
    finally:
        print("Exiting application")
