import requests
from config import LOL_VERSION_URL, CHAMPION_DATA_URL
from update_checker import get_latest_lol_version
from logger import setup_logger

logger = setup_logger(__name__)

def get_current_champion():
    """Get current in-game champion from local API"""
    url = "https://127.0.0.1:2999/liveclientdata/playerlist"
    try:
        response = requests.get(url, verify=False, timeout=3)
        if response.status_code == 200:
            return response.json()[0]['championName']
    except (requests.ConnectionError, requests.Timeout):
        logger.info("No active game detected")
    except Exception as e:
        logger.error(f"Champion detection failed: {e}")
    return None

def get_champion_names():
    """Fetch all champion names from Riot API"""
    try:
        version = get_latest_lol_version()
        champion_data = requests.get(
            CHAMPION_DATA_URL.format(version=version),
            timeout=5
        ).json()
        return [champ["name"] for champ in champion_data["data"].values()]
    except Exception as e:
        logger.error(f"Champion list fetch failed: {e}")
        return []
