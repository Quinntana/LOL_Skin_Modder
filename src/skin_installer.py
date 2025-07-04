import os
import io
import zipfile
from config import INSTALL_DIR, DOWNLOAD_DIR, REPO_ZIP_PATH, INSTALLED_DIR
from logger import setup_logger

logger = setup_logger(__name__)

def install_skins(champion, skip_chromas=False):
    """Install skins directly from repository zip to CSLOL Manager"""
    installed = 0
    try:
        with zipfile.ZipFile(REPO_ZIP_PATH) as repo_zip:
            skin_files = [
                f for f in repo_zip.namelist()
                if f.startswith(f"lol-skins-main/skins/{champion}/")
                and f.endswith(".zip")
            ]

            if skip_chromas:
                skin_files = [f for f in skin_files if 'chromas' not in f]

            if not skin_files:
                logger.warning(f"No skins found for {champion}")
                return 0

            for skin_path in skin_files:
                skin_name = os.path.splitext(os.path.basename(skin_path))[0]
                install_path = os.path.join(INSTALLED_DIR, skin_name)

                os.makedirs(install_path, exist_ok=True)

                with repo_zip.open(skin_path) as skin_zip:
                    with zipfile.ZipFile(io.BytesIO(skin_zip.read())) as skin_archive:
                        skin_archive.extractall(install_path)

                installed += 1
                logger.info(f"Installed skin: {skin_name}")

    except Exception as e:
        logger.error(f"Skin installation failed: {e}")

    return installed
