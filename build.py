import os
import shutil
import PyInstaller.__main__

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
BUILD_DIR = os.path.join(PROJECT_ROOT, 'build')
DIST_DIR = os.path.join(PROJECT_ROOT, 'dist')
EXE_NAME = 'LeagueSkinManagerVN'

def patch_config():
    """Patch config.py for executable environment"""
    config_path = os.path.join(SRC_DIR, 'config.py')
    with open(config_path, 'r') as f:
        content = f.read()

    new_content = content.replace(
        'import os\nimport sys',
        'import os\nimport sys\n\n'
        '# Handle frozen executable\n'
        'if getattr(sys, \'frozen\', False):\n'
        '    PROJECT_ROOT = os.path.dirname(sys.executable)\n'
        'else:\n'
        '    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))'
    )

    with open(config_path, 'w') as f:
        f.write(new_content)

def post_build_cleanup():
    """Ensure data directories exist in the dist folder"""
    dist_data = os.path.join(DIST_DIR, EXE_NAME, "data")
    os.makedirs(dist_data, exist_ok=True)
    print(f"Created data directory at: {dist_data}")

def main():
    for path in [BUILD_DIR, DIST_DIR]:
        if os.path.exists(path):
            shutil.rmtree(path)

    pyinstaller_args = [
        os.path.join(SRC_DIR, 'main.py'),
        '--name', EXE_NAME,
        '--onefile',
        '--console',
        '--distpath', DIST_DIR,
        '--workpath', BUILD_DIR,
        '--add-data', f'{SRC_DIR}{os.pathsep}.',
        '--hidden-import=config',
        '--hidden-import=logger',
        '--hidden-import=champions',
        '--hidden-import=skin_downloader',
        '--hidden-import=skin_installer',
        '--hidden-import=update_checker'
    ]

    PyInstaller.__main__.run(pyinstaller_args)
    print(f"\nBuild complete! Executable is in: {DIST_DIR}")


if __name__ == '__main__':
    main()
