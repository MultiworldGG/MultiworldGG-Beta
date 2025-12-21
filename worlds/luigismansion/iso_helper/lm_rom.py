import shutil

from worlds.Files import APPatch, APPlayerContainer, AutoPatchRegister
from settings import get_settings, Settings
from NetUtils import convert_to_base_types
import Utils

from hashlib import md5
from typing import Any
import json, logging, sys, os, zipfile, tempfile
import urllib.request

logger = logging.getLogger()
MAIN_PKG_NAME = "worlds.luigismansion.LMGenerator"

RANDOMIZER_NAME = "Luigi's Mansion"
LM_USA_MD5 = 0x6e3d9ae0ed2fbd2f77fa1ca09a60c494

class InvalidCleanISOError(Exception):
    """
    Exception raised for when user has an issue with their provided Luigi's Mansion ISO.

    Attributes:
        message -- Explanation of the error
    """

    def __init__(self, message="Invalid Clean ISO provided"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"InvalidCleanISOError: {self.message}"

class LMPlayerContainer(APPlayerContainer):
    game = RANDOMIZER_NAME
    compression_method = zipfile.ZIP_DEFLATED
    patch_file_ending = ".aplm"

    def __init__(self, player_choices: dict, patch_path: str, player_name: str, player: int,
        server: str = ""):
        self.output_data = player_choices
        super().__init__(patch_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("patch.aplm", json.dumps(self.output_data, indent=4, default=convert_to_base_types))
        super().write_contents(opened_zipfile)

class LMUSAAPPatch(APPatch, metaclass=AutoPatchRegister):
    game = RANDOMIZER_NAME
    hash = LM_USA_MD5
    patch_file_ending = ".aplm"
    result_file_ending = ".iso"

    procedure = ["custom"]

    def __init__(self, *args: Any, **kwargs: Any):
        super(LMUSAAPPatch, self).__init__(*args, **kwargs)

    def __get_archive_name(self) -> str:
        if not (Utils.is_linux or Utils.is_windows):
            message = f"Your OS is not supported with this randomizer {sys.platform}."
            logger.error(message)
            raise RuntimeError(message)

        lib_path = ""
        if Utils.is_windows:
            lib_path = "lib-windows"
        elif Utils.is_linux:
            lib_path = "lib-linux"

        logger.info(f"Dependency archive name to use: {lib_path}")
        return lib_path

    def __get_temp_folder_name(self) -> str:
        from ..LMClient import CLIENT_VERSION
        temp_path = os.path.join(tempfile.gettempdir(), "luigis_mansion", CLIENT_VERSION, "libs")
        return temp_path

    def patch(self, aplm_patch: str) -> str:
        # Get the AP Path for the base ROM
        lm_clean_iso = self.get_base_rom_path()
        logger.info("Provided Luigi's Mansion ISO Path was: " + lm_clean_iso)

        base_path = os.path.splitext(aplm_patch)[0]
        output_file = base_path + self.result_file_ending

        # Verify we have a clean rom of the game first
        self.verify_base_rom(lm_clean_iso, throw_on_missing_speedups=True)

        # Use our randomize function to patch the file into an ISO.
        from ..LMGenerator import LuigisMansionRandomizer
        with zipfile.ZipFile(aplm_patch, "r") as zf:
            aplm_bytes = zf.read("patch.aplm")
        LuigisMansionRandomizer(lm_clean_iso, output_file, aplm_bytes)
        return output_file
