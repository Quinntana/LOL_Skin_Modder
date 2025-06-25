import os
import io
import zipfile
from config import INSTALL_DIR, DOWNLOAD_DIR, REPO_ZIP_PATH
from logger import setup_logger

logger = setup_logger(__name__)

def install_skins(champion):
    """Install skins directly from repository zip to CSLOL Manager"""
    installed = 0
    try:
        with zipfile.ZipFile(REPO_ZIP_PATH) as repo_zip:
            # Find all skins for this champion
            skin_files = [
                f for f in repo_zip.namelist()
                if f.startswith(f"lol-skins-main/skins/{champion}/")
                and f.endswith(".zip")
            ]

            if not skin_files:
                logger.warning(f"No skins found for {champion}")
                return 0

            for skin_path in skin_files:
                skin_name = os.path.splitext(os.path.basename(skin_path))[0]
                install_path = os.path.join(INSTALL_DIR, "installed", skin_name)

                # Create installation directory
                os.makedirs(install_path, exist_ok=True)

                # Extract skin directly from repo zip
                with repo_zip.open(skin_path) as skin_zip:
                    with zipfile.ZipFile(io.BytesIO(skin_zip.read())) as skin_archive:
                        skin_archive.extractall(install_path)

                installed += 1
                logger.info(f"Installed skin: {skin_name}")

    except Exception as e:
        logger.error(f"Skin installation failed: {e}")

    return installed
