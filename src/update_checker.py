import os
import requests
import shutil
import zipfile
import tempfile
from config import (
    INSTALL_DIR,
    GITHUB_RELEASES_URL,
    DATA_DIR,
    VERSION_FILE,
    LOL_VERSION_FILE,
    DOWNLOAD_DIR,
    LOL_VERSION_URL,
)
from logger import setup_logger

logger = setup_logger(__name__)

def get_installed_version():
    """Get currently installed manager version"""
    try:
        with open(VERSION_FILE) as f:
            return f.read().strip().replace("Version: ", "")
    except FileNotFoundError:
        return None


def get_latest_manager_version():
    """Get latest manager version from GitHub"""
    try:
        response = requests.get(GITHUB_RELEASES_URL, timeout=10)
        response.raise_for_status()
        return response.json().get("tag_name", "").replace("-prerelease", "")
    except Exception as e:
        logger.error(f"Manager version check failed: {e}")
        return None

def get_latest_lol_version():
    """Fetch latest League of Legends version from Riot API"""
    try:
        versions = requests.get(LOL_VERSION_URL, timeout=5).json()
        return versions[0] if versions else None
    except Exception as e:
        logger.error(f"LoL version fetch failed: {e}")
        return None

def download_asset(asset_url, temp_dir):
    """Download update asset"""
    temp_file = os.path.join(temp_dir, os.path.basename(asset_url))
    try:
        with requests.get(asset_url, stream=True, timeout=30) as response:
            response.raise_for_status()
            with open(temp_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        return temp_file
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return None


def install_update(temp_file, new_version):
    """Install update from downloaded file and record version"""
    try:
        for item in os.listdir(INSTALL_DIR):
            if item != "installed":
                path = os.path.join(INSTALL_DIR, item)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

        with zipfile.ZipFile(temp_file, "r") as zip_ref:
            zip_ref.extractall(DATA_DIR)

        with open(VERSION_FILE, "w") as f:
            f.write(new_version)

        return True
    except Exception as e:
        logger.error(f"Installation failed: {e}")
        return False


def check_and_update():
    """
    Check for manager updates and LoL version changes.
    - Updates the manager if a new release exists.
    - Resets skins if LoL version has changed.
    Returns:
        dict: { 'manager_updated': bool, 'lol_version_changed': bool }
    """
    results = {'manager_updated': False, 'lol_version_changed': False}

    current_mgr = get_installed_version()
    latest_mgr = get_latest_manager_version()

    if latest_mgr and current_mgr != latest_mgr:
        logger.info(f"Manager update: {current_mgr} -> {latest_mgr}")
        try:
            release_data = requests.get(GITHUB_RELEASES_URL, timeout=10).json()
            asset_url = next(
                (a["browser_download_url"] for a in release_data.get("assets", [])
                if a["name"].endswith(".zip")),
                None
            )
            if asset_url:
                with tempfile.TemporaryDirectory() as tmp:
                    tmp_file = download_asset(asset_url, tmp)
                    if tmp_file and install_update(tmp_file, latest_mgr):
                        logger.info("Manager updated successfully")
                        results['manager_updated'] = True
            else:
                assets = release_data.json().get("assets", [])
                logger.warning(f"No .zip asset found in latest release ({latest_mgr}). "
                f"Available assets: {[a['name'] for a in assets]}")
        except Exception as e:
            logger.error(f"Manager update process failed: {e}")

    current_lol = None
    if os.path.exists(LOL_VERSION_FILE):
        with open(LOL_VERSION_FILE, 'r') as f:
            current_lol = f.read().strip()

    latest_lol = get_latest_lol_version()
    if latest_lol and current_lol != latest_lol:
        logger.info(f"LoL version changed: {current_lol} -> {latest_lol}")
        print(f"New LoL version detected: {latest_lol}. Resetting skins...")

        shutil.rmtree(DOWNLOAD_DIR, ignore_errors=True)
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        installed_dir = os.path.join(INSTALL_DIR, "installed")
        shutil.rmtree(installed_dir, ignore_errors=True)
        os.makedirs(installed_dir, exist_ok=True)

        with open(LOL_VERSION_FILE, 'w') as f:
            f.write(latest_lol)
        results['lol_version_changed'] = True

    return results
