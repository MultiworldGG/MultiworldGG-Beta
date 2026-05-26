from enum import Enum

class ClientState(Enum):
    INITIAL = "initial"
    GAME = "game"
    LEGACY_KVUI = "legacy_kvui"
    TRANSITIONING = "transitioning"