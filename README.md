LOL Skin Modder




LOL Skin Modder is a comprehensive tool for managing custom skins in League of Legends. It automates downloading official skins from community repositories, integrates with CSLOL Manager for installation, and provides features like factory reset and batch processing. Built with Python, this project aims to make custom skins accessible to all players, especially those impacted by Riot’s pricing and Vanguard restrictions.

Features
Automatic Skin Downloading: Fetches official League of Legends skins from the darkseal-org/lol-skins GitHub repository.
CSLOL Manager Integration: Seamlessly checks for and installs the latest CSLOL Manager version, preserving your installed skins.
Current Champion Detection: Detects your in-game champion and installs skins with one command.
Batch Skin Installation: Downloads and installs skins for all champions in a single run.
Factory Reset: Clears downloaded skins and resets the installation directory while preserving user-installed mods.
Cross-Platform Support: Works on Windows and macOS (with ZIP extraction for Windows and tarball support for macOS).
Logging: Detailed logs for debugging and tracking operations, saved to skin_manager.log.
Modular Design: Separates functionality into modules (champ_list.py, skin_downloader.py, skin_installer.py, update_checker.py) for easy maintenance.
Prerequisites
Python 3.8+: Ensure Python is installed on your system.
Dependencies: Install required packages with:
bash

Collapse

Wrap

Copy
pip install requests
League of Legends Client: Must be installed and running for current champion detection.
CSLOL Manager: Optional but recommended for skin installation. The script will download it if missing.
Administrator Privileges: Required on Windows for CSLOL Manager updates and directory modifications.
Installation
Clone the Repository:
bash

Collapse

Wrap

Copy
git clone https://github.com/<your-username>/LOL Skin Modder.git
cd LOL Skin Modder
Install Dependencies:
bash

Collapse

Wrap

Copy
pip install -r requirements.txt
(Create a requirements.txt with requests if not already present.)
Set Up Directories:
The script creates skins and cslol-manager directories in the project root automatically.
Ensure write permissions for C:\Users\<your-username>\Downloads\Code\LOL API\ or adjust INSTALL_DIR in main.py.
Run the Script:
bash

Collapse

Wrap

Copy
python main.py
Usage
Running the Program
Launch main.py to start the skin manager:

bash

Collapse

Wrap

Copy
python main.py
Main Menu
Upon startup, the script checks for CSLOL Manager updates and presents the following options:

text

Collapse

Wrap

Copy
=== League of Legends Skin Manager ===
Checking for CSLOL Manager updates...
INFO:root:CSLOL Manager is up to date.

1. Download skins for current champion
2. Download skins for all champions
3. Factory reset
0. Exit

Enter mode (0-3):
Mode 1: Current Champion
Detects your current in-game champion and downloads/installs available skins.
Example output:
text

Collapse

Wrap

Copy
INFO:root:Detecting current champion...
INFO:root:Detected champion: Aurelion Sol
INFO:root:Processing champion: Aurelion Sol
INFO:root:Successfully installed 2 skins for Aurelion Sol!
Mode 2: All Champions
Downloads and installs skins for every champion listed in the Data Dragon API.
Includes a confirmation prompt due to time and disk space usage.
Example output:
text

Collapse

Wrap

Copy
INFO:root:Found 165 champions.
WARNING:root:This may take a long time and use significant disk space!
Download and install skins for all 165 champions? (y/n): y
INFO:root:[1/165] Processing champion: Aatrox
INFO:root:✓ Installed 3 skins for Aatrox
...
INFO:root:Installation complete: 150/165 successful
Mode 3: Factory Reset
Deletes all downloaded skins and resets the cslol-manager/installed directory, preserving user-installed mods.
Requires double confirmation to prevent accidental data loss.
Example output:
text

Collapse

Wrap

Copy
INFO:root:=== Factory Reset ===
WARNING:root:This will delete all downloaded skins and installed mods!
Are you sure? (yes/no): yes
Type 'RESET' to confirm: RESET
INFO:root:✓ Reset skins directory successfully
INFO:root:=== Factory Reset Complete ===
Mode 0: Exit
Exits the program cleanly.
Project Structure
text

Collapse

Wrap

Copy
LOL Skin Modder/
├── main.py              # Main script coordinating all operations
├── champ_list.py        # Champion detection and list retrieval
├── skin_downloader.py   # Skin fetching and downloading logic
├── skin_installer.py    # Skin extraction and installation
├── update_checker.py    # CSLOL Manager update handling
├── skins/               # Downloaded skin ZIPs (auto-created)
├── cslol-manager/       # CSLOL Manager installation (auto-created)
│   ├── installed/       # Extracted skins for CSLOL Manager
│   └── version.txt      # Tracks CSLOL Manager version
├── skin_manager.log     # Log file for debugging
└── README.md            # This file
How It Works
Startup:
Checks for CSLOL Manager updates using update_checker.py.
Downloads cslol-manager-windows.zip from GitHub if missing or outdated, extracts it, and preserves the installed folder.
Skin Management:
Uses champ_list.py to detect the current champion or fetch all champions.
skin_downloader.py retrieves skin URLs from darkseal-org/lol-skins and downloads ZIP files.
skin_installer.py extracts ZIPs to cslol-manager/installed for use with CSLOL Manager.
Reset:
Clears skins/ and cslol-manager/installed/ while keeping CSLOL Manager intact.
Contributing
We welcome contributions! To contribute:

Fork the Repository:
bash

Collapse

Wrap

Copy
git fork https://github.com/<your-username>/LOL Skin Modder.git
Make Changes:
Add features, fix bugs, or improve documentation in a new branch.
Submit a Pull Request:
Push your changes and open a PR with a clear description.
Issues:
Report bugs or suggest features via the GitHub Issues tab.
Troubleshooting
CSLOL Manager Update Fails:
Run the script as an administrator on Windows.
Check your internet connection for GitHub API access.
Skin Download Fails:
Verify the darkseal-org/lol-skins repository is accessible.
Ensure DOWNLOAD_DIR has write permissions.
Champion Detection Fails:
Ensure the League client is running and you’re in a game.
Logs:
Check skin_manager.log for detailed error messages.
Notes
Non-Profit: This project is free and open-source, inspired by the spirit of tools like R3nzSkin.
Riot Disclaimer: This project is not endorsed by Riot Games and may violate their Terms of Service. Use at your own risk.
Performance: Batch mode (Mode 2) can take hours and requires significant disk space (~10-20 GB).
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
darkseal-org/lol-skins: For providing a community-maintained skin repository.
LeagueToolkit/cslol-manager: For the CSLOL Manager tool integration.
R3nzSkin: Inspiration for accessible skin management tools.
Contact
For questions or support:

GitHub Issues: Open an issue on this repository.
Email: <your-email@example.com> (optional, replace with your contact if desired).
Customization Notes
Replace <your-username>: Update with your GitHub username in badges and URLs.
Adjust Paths: If your INSTALL_DIR differs from C:\Users\archi\Downloads\Code\LOL API\cslol-manager, update the README accordingly.
Add Screenshots: Enhance the README with screenshots of the menu or installation process using GitHub’s image hosting (e.g., ![Screenshot](path/to/screenshot.png)).
License File: Create a LICENSE file with the MIT License text if not already present.
This README provides a professional, detailed overview similar to hydy100/R3nzSkin, tailored to your project’s unique features like CSLOL Manager updates and factory reset. Let me know if you’d like further adjustments!
