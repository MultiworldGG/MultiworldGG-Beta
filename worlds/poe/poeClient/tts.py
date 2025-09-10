import asyncio
import logging
import sys
import threading

from worlds.poe.poeClient import fileHelper
fileHelper.load_vendor_modules()


from worlds.poe.poeClient import itemFilter
import os
import typing
if typing.TYPE_CHECKING:
    from worlds.poe.poeClient.vendor.pyttsx3 import pyttsx3, pythoncom
    from worlds.poe.Client import PathOfExileContext
else:
    import pyttsx3

from pathlib import Path

logger = logging.getLogger("poeClient.tts")
_debug = True
_verbose = False
_engine = None  # Global TTS engine instance
WPM = 250  # Default words per minute for TTS
tasks: list[typing.Tuple[str, str, int]] = []  # List to hold async tasks for TTS generation

tts_lock = threading.Lock()  # Lock to ensure thread-safe access to TTS generation

def start_tts_engine():
    """Initialize the TTS engine."""
    global _engine
    if _engine is None:
        try:
            if sys.platform == "win32":
                _engine = pyttsx3.init()
            else:
                _engine = pyttsx3.init(driverName='espeak')
            logger.debug("TTS engine initialized successfully.")
        except Exception as e:
            logger.error(f"[ERROR] Failed to initialize TTS engine: {e}")
            _engine = None
    return _engine        
    
def get_item_name_tts_text(ctx: "PathOfExileContext", network_item) -> str:
    if network_item.player == ctx.slot:
        return ctx.item_names.lookup_in_slot(network_item.item, network_item.player)
    else:
        return (ctx.player_names[network_item.player] + " ... " +
         ctx.item_names.lookup_in_slot(network_item.item, network_item.player))

def safe_tts(text, filename, rate=250, volume=1, voice_id=None, overwrite=False):
    if not overwrite and Path(filename).exists():
        if _debug:
            logger.info(f"[DEBUG] File already exists: {filename}")
        return
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    tasks.append((text, filename, rate))
    run_tts_tasks()

async def safe_tts_async(text, filename, rate=250, volume=1, voice_id=None, overwrite=False):
    if _verbose:
        logger.info(f"[DEBUG] Async TTS: text='{text}', filename='{filename}'")

    if not overwrite and Path(filename).exists():
        if _debug:
            logger.info(f"[DEBUG] File already exists: {filename}")
        return
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    tasks.append((text, filename, rate))
    await async_run_tts_tasks()

#def generate_tts_from_missing_locations(ctx: "PathOfExileContext", WPM: int = WPM) -> None:
#    """Generate TTS files for missing locations."""
#    if not ctx or not ctx.missing_locations:
#        logger.info("[DEBUG] No missing locations to generate TTS for.")
#        return
#
#    missing_location_ids = ctx.missing_locations
#    logger.debug(f"[DEBUG] Generating TTS for {len(missing_location_ids)} items...")
#    for base_item_location_id in missing_location_ids:
#        network_item = ctx.locations_info[base_item_location_id]
#        item_text = get_item_name_tts_text(ctx, network_item)
#        filename = fileHelper.safe_filename(f"{item_text.lower()}_{WPM}.wav")
#
#        relative_path = f"{itemFilter.TTS_FILTER_SOUNDS_DIR_NAME}/{filename.lower()}"
#        full_path = itemFilter.filter_sounds_path / f"{filename}"
#
#        if not os.path.exists(full_path):
#            if _verbose:
#                logger.info(f"[DEBUG] Generating TTS for item: {item_text} at {full_path}")
#                safe_tts(
#                    text=item_text,
#                    filename=full_path
#                )
#        itemFilter.base_item_id_to_relative_wav_path[base_item_location_id] = relative_path


def generate_tts_tasks_from_missing_locations(ctx: "PathOfExileContext", tts_speed: int = None) -> None:

    tts_dir = itemFilter.poe_doc_path / itemFilter.TTS_FILTER_SOUNDS_DIR_NAME
    tts_dir.mkdir(parents=True, exist_ok=True)

    """Generate TTS files for missing locations."""
    if not ctx or not ctx.missing_locations:
        logger.info("[DEBUG] No missing locations to generate TTS for.")
        return
    speed = 250
    if tts_speed is None:
        if not ctx.filter_options: logger.error("[Error] No client options available for TTS.")
    else:
        speed = int(ctx.filter_options.tts_speed)

    missing_location_ids = ctx.missing_locations
    logger.debug(f"[DEBUG] Generating TTS for {len(missing_location_ids)} items...")
    for base_item_location_id in missing_location_ids:
        network_item = ctx.locations_info[base_item_location_id]
        item_text = get_item_name_tts_text(ctx, network_item)
        filename = fileHelper.safe_filename(f"{item_text.lower()}_{speed}.wav")

        relative_path = f"{itemFilter.TTS_FILTER_SOUNDS_DIR_NAME}/{filename.lower()}"
        full_path = itemFilter.poe_doc_path / itemFilter.TTS_FILTER_SOUNDS_DIR_NAME / f"{filename}"

        if not os.path.exists(full_path):
            if _debug:
                logger.info(f"[DEBUG] Generating TTS for item: {item_text} at {full_path}")
                tasks.append((
                    item_text,
                    full_path,
                    speed
                ))
        itemFilter.base_item_id_to_relative_tts_wav_path[base_item_location_id] = relative_path


def run_tts_tasks(use_daemon: bool = True):
    """Run all TTS tasks"""
    try:
        # Disable specific loggers to avoid crashes. Something about these logs causes crashes in pyttsx3
        for logger_name in ['pyttsx3', 'comtypes', 'win32com']:
            logging.getLogger(logger_name).disabled = True
            logging.getLogger(logger_name).setLevel(logging.CRITICAL + 1)

        global tasks, _engine
        if not tasks or len(tasks) == 0:
            logger.info("[DEBUG] No TTS tasks to run.")
            return

        if _engine is None:
            _engine = start_tts_engine()

        if len(tasks) > 0:
            for text, filename, rate in tasks:
                if not os.path.exists(filename):
                    if _debug and _verbose:
                        logger.info(f"[DEBUG] Generating TTS for text: {text} at {filename}")
                    _engine.setProperty('rate', rate)
                    _engine.save_to_file(text, str(filename))
            tasks.clear()
        thread = threading.Thread(target=_engine.runAndWait, daemon=use_daemon)
        thread.start()
    except Exception as e:
        logger.info(f"[ERROR] Exception during TTS tasks: {e}")

async def async_run_tts_tasks():
    """Run all TTS tasks"""
    try:
        # Disable specific loggers to avoid crashes. Something about these logs causes crashes in pyttsx3
        for logger_name in ['pyttsx3', 'comtypes', 'win32com']:
            logging.getLogger(logger_name).disabled = True
            logging.getLogger(logger_name).setLevel(logging.CRITICAL + 1)

        global tasks, _engine
        if not tasks or len(tasks) == 0:
            logger.info("[DEBUG] No TTS tasks to run.")
            return

        if _engine is None:
            _engine = start_tts_engine()

        if len(tasks) > 0:
            for text, filename, rate in tasks:
                if not os.path.exists(filename):
                    if _debug:
                        logger.info(f"[DEBUG] Generating TTS for text: {text} at {filename}")
                    _engine.setProperty('rate', rate)
                    _engine.save_to_file(text, str(filename))
            tasks.clear()
        await asyncio.to_thread(_engine.runAndWait)
        
    except Exception as e:
        logger.info(f"[ERROR] Exception during TTS tasks: {e}")

def itterate_tts_tasks():
    """Iterate through TTS tasks and run them one by one."""
    global _engine
    if _engine:
        _engine.runAndWait()  # Process the TTS queue
    else:
        if _debug:
            logger.info("[DEBUG] TTS engine not initialized, cannot iterate tasks.")


async def async_test():
    tasks = []
    for i in range(100):
        tasks.append(safe_tts_async(f"Hello {i}", f"test{i}.wav"))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    
    import worlds.poe.Items as Items
    # mock a context with missing locations, player names, and item lookup and such
    class mockCtx:
        class mock_network_item:
            def __init__(self, item, player):
                self.item = item
                self.player = player
        class mock_item_names:
            def lookup_in_slot(self, item, player):
                # Mock item names lookup
                return f"ItemName_{str(item)} for Player{player}"
        def __init__(self):
            self.missing_locations = list(Items.item_table.keys())
            self.locations_info = {
                loc_id: self.mock_network_item(item, player)
                for (loc_id, item), player in zip(Items.item_table.items(), range(1, len(Items.item_table) + 1))
            }
            self.player_names = {player_id: f"Player{player_id}" for player_id in range(1, len(Items.item_table) + 1)}
            self.item_names = self.mock_item_names()



    ctx = mockCtx()

    generate_tts_tasks_from_missing_locations(ctx, WPM)
    run_tts_tasks()

    #thread = threading.Thread(target=generate_tts_from_missing_locations, args=(ctx,))  # comma to make it a tuple
    #thread.start()

#working??
#    asyncio.run(async_test())


   # text = "Hello, this is a test of the text-to-speech system."
   # filename = Path('C:/Users/StuBob/Documents/My Games/Path of Exile/apsound') / 'test_tts.wav'
   # safe_tts(text, filename, rate=WPM, overwrite=True)

