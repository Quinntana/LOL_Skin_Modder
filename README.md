# LOL_Skin_Modder_VN

![GitHub release (latest by date)](https://img.shields.io/github/v/release/Quinntana/LOL_Skin_Modder)
![GitHub license](https://img.shields.io/github/license/Quinntana/LOL_Skin_Modder)
![GitHub stars](https://img.shields.io/github/stars/Quinntana/LOL_Skin_Modder?style=social)

**LOL_Skin_Modder_VN** is a powerful tool designed to enhance your League of Legends experience by automating the management of custom skins. It downloads official skins from community repositories, integrates with CSLOL Manager for seamless installation, and offers features like batch processing and factory reset. Built with Python, this project is perfect for players looking to bypass Riot’s pricing barriers or explore custom skin options in a post-Vanguard world.

---

## Features

- **Automatic Skin Downloading**: Retrieves official League of Legends skins from the `darkseal-org/lol-skins` GitHub repository.
- **CSLOL Manager Integration**: Automatically updates CSLOL Manager, preserving your installed skins during upgrades.
- **Current Champion Detection**: Identifies your in-game champion and installs skins with a single command.
- **Batch Skin Installation**: Downloads and installs skins for all champions in one go.
- **Factory Reset**: Clears downloaded skins and resets the installation directory while keeping user-installed mods intact.
- **Cross-Platform Support**: Compatible with Windows (ZIP extraction) and macOS (tarball support).
- **Detailed Logging**: Tracks operations and errors in `skin_manager.log` for easy debugging.
- **Modular Design**: Organized into modules (`champ_list.py`, `skin_downloader.py`, `skin_installer.py`, `update_checker.py`) for maintainability.

---

## Usage
Download and run the exe or if you want to run it yourself, follow the step below:
1. Install dependencies.
   ```bash
   pip install -r requirements.txt
3. Run:
   ```bash
   cd src
   python main.py

## Showcase
https://www.youtube.com/watch?v=WTbJWBQ6bfI
