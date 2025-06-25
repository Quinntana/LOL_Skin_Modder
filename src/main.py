import os
import time
import shutil
import subprocess
from config import PROJECT_ROOT, DOWNLOAD_DIR, INSTALL_DIR, LOG_DIR, DATA_DIR
from logger import setup_logger
from champions import get_current_champion, get_champion_names
from skin_downloader import download_repo
from skin_installer import install_skins
from update_checker import check_and_update

logger = setup_logger(__name__)

def verify_paths():
    """Ensure all required directories exist"""
    required_dirs = [DOWNLOAD_DIR, INSTALL_DIR, LOG_DIR]
    for directory in required_dirs:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Verified directory: {directory}")

def process_champion(champion):
    """Full processing pipeline for a champion"""
    logger.info(f"Processing {champion}")

    if not download_repo():
        logger.error("Failed to download skins repository")
        return 0

    installed = install_skins(champion)
    logger.info(f"Installed {installed} skins for {champion}")
    return installed

def factory_reset():
    """Reset all downloaded and installed content"""
    logger.info("Performing factory reset")

    try:
        # Clear downloaded skins repository
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
    print("\nLeague Skin Manager")
    print("1. Install skins for current champion")
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
                process_champion(champion)
            else:
                print("Invalid champion name")

        elif choice == "2":
            champions = get_champion_names()
            if not champions:
                print("Failed to get champion list")
                continue

            print(f"Found {len(champions)} champions")
            start = time.time()

            for i, champ in enumerate(champions, 1):
                print(f"\nProcessing {i}/{len(champions)}: {champ}")
                process_champion(champ)

            print(f"\nCompleted in {time.time()-start:.1f} seconds")

        elif choice == "3":
            factory_reset()
            print("Reset complete")
            return

        elif choice == "4":
            try:
                # Path to CSLOL Manager executable
                cslol_path = os.path.join(INSTALL_DIR, "cslol-manager.exe")

                if os.path.exists(cslol_path):
                    print(f"Launching CSLOL Manager from {cslol_path}")
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
        # Initial setup
        verify_paths()
        os.chdir(PROJECT_ROOT)
        print("Checking for updates...")
        if check_and_update():
            print("Updated successfully")

        # Start application
        main_menu()
    except KeyboardInterrupt:
        print("\nOperation cancelled")
    except Exception as e:
        logger.exception("Critical error occurred")
        print(f"Error: {e}\nSee logs for details")
    finally:
        print("Exiting application")
