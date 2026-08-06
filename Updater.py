import tempfile, os, sys, subprocess
import logging
from Utils import normalize_tag, tuplize_version, is_frozen, is_windows, is_linux, is_macos

GITHUB_OWNER = "MultiworldGG"
GITHUB_REPO  = "MultiworldGG"
GITHUB_API_LATEST = (
    f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
)
GITHUB_RELEASES_PAGE = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"

def can_check_for_updates() -> bool:
    """Whether this process runs from an installed build the updater can replace.

    Frozen-only: source checkouts always return False. Windows installs are
    always updatable (Inno installer handoff); Linux only when running from an
    AppImage; macOS only when running from a .app bundle.
    """
    if not is_frozen():
        return False
    if is_windows:
        return True
    if is_linux:
        return bool(os.environ.get("APPIMAGE"))
    if is_macos:
        return ".app/Contents/MacOS/" in os.path.realpath(sys.executable)
    return False

def get_release_page_url() -> str:
    """Fallback for platforms without an in-app installer handoff: the release
    page to open in a browser (non-Windows, until installer paths are ported)."""
    return GITHUB_RELEASES_PAGE

def select_installer_asset(assets: list[dict]) -> dict:
    if is_windows:
        release_assets = [a for a in assets if a["name"].lower().endswith(".exe")]
    elif is_linux:
        release_assets = [a for a in assets if a["name"].lower().endswith(".appimage")]
    elif is_macos:
        release_assets = [a for a in assets if a["name"].lower().endswith(".dmg")]
    else:
        raise RuntimeError("This platform is not supported.")

    if not release_assets:
        raise RuntimeError("No feasible installer found in latest release for this platform.")

    return release_assets[0]

def get_latest_release_info() -> tuple:
    import requests
    resp = requests.get(GITHUB_API_LATEST, headers={"Accept":"application/vnd.github.v3+json"})
    resp.raise_for_status()
    data = resp.json()

    tag = normalize_tag(data["tag_name"])
    installer = select_installer_asset(data["assets"])
    download_url = installer["browser_download_url"]
    changelog = data.get("body") or "No changelog available."
    logging.info(f"latest release {tag} under url {download_url}")
    return tuplize_version(tag), download_url, changelog

def download_and_install_win(url: str, progress_callback=None):
    """Download installer to a temp file and launch it.

    progress_callback(bytes_downloaded, total_bytes) is called from the
    download thread whenever a chunk is written.  total_bytes is -1 when the
    server does not report Content-Length.
    """
    import requests
    fd, path = tempfile.mkstemp(suffix=".exe")
    os.close(fd)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get("Content-Length", -1))
        downloaded = 0
        with open(path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
                downloaded += len(chunk)
                if progress_callback:
                    progress_callback(downloaded, total)
    subprocess.Popen([path, "/SILENT", "/SUPPRESSMSGBOXES", "/RESTARTAPPLICATIONS", "/TASKS=deletelib"], shell=False)
    os._exit(0)
