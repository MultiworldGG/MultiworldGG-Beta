from . import MegaMixTestBase

# The worst case settings are DLC songs off, and enabling streamer mode.
# This ends up with only 25 valid songs that can be chosen.
# These tests ensure that this won't fail generation


class TestWorstCaseTest(MegaMixTestBase):
    options = {
        "starting_song_count": 10,
        "dlc_packs": [],
        "allow_megamix_dlc_songs": True,
        "song_difficulty_min": 'easy',
        "song_difficulty_max": 'exextreme',
        "include_songs": ["DYE [603]", "Gizmo [442]", "Kokoro [55]"],
        "exclude_songs": ["2D Dream Fever [723]", "Break It, Break It! [734]", "Change Me [59]"],
        "megamix_mod_data": '',
    }