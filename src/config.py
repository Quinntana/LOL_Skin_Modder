import os
import sys

if getattr(sys, 'frozen', False):
    PROJECT_ROOT = os.path.dirname(sys.executable)
else:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DOWNLOAD_DIR = os.path.join(DATA_DIR, "skins")
INSTALL_DIR = os.path.join(DATA_DIR, "cslol-manager")
INSTALLED_DIR = os.path.join(PROJECT_ROOT, "data", "cslol-manager", "installed")
PROFILE_FILE = os.path.join(INSTALLED_DIR, "default_profile.txt")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
LOL_VERSION_FILE = os.path.join(DATA_DIR, "lol_version.txt")
VERSION_FILE = os.path.join(INSTALL_DIR, "version.txt")
REPO_ZIP_PATH = os.path.join(DOWNLOAD_DIR, "lol-skins-main.zip")

LOL_VERSION_URL = "https://ddragon.leagueoflegends.com/api/versions.json"
CHAMPION_DATA_URL = "https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
GITHUB_RELEASES_URL = "https://api.github.com/repos/LeagueToolkit/cslol-manager/releases/latest"
SKINS_REPO_URL = "https://github.com/darkseal-org/lol-skins/archive/refs/heads/main.zip"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(INSTALL_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
