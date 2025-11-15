from BaseClasses import CollectionState


class PhoaLogic:
    player: int

    def __init__(self, player: int):
        self.player = player

    def has_anuri_temple_access(self, state: CollectionState) -> bool:
        return state.has_any({"Slingshot", "Bombs"}, self.player)