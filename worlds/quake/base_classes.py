import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Union

from BaseClasses import Entrance, Item, Location, Region

from .rules import RULETYPE, LambdaRule, Rule, Rules, RuleTrue

if TYPE_CHECKING:
    from ..quake import Q1World


class Q1Item(Item):
    game = "Quake1"


class Q1Location(Location):
    game = "Quake1"

    def __init__(
        self,
        player: int,
        name: str = "",
        address: Optional[int] = None,
        parent: Optional[Region] = None,
    ):
        super().__init__(player, name, address, parent)
        if address is None:
            self.event = True


@dataclass(frozen=True)
class LocationDef:
    game_id: int  # Entity id
    name: str
    classname: str  # "item_*", "weapon_*", "trigger_changelevel", "trigger_secret"
    uuid: int
    mp: int = 0  # 1 if the location only spawns in multiplayer


@dataclass(frozen=True)
class ItemDef:
    name: str
    ap_id: int  # The id for the item
    type: str  # The type of item
    props: Dict[str, Any]  # Additional type specific properties
    unique: bool = False  # Can only have one of these
    persistent: bool = False  # These are persisted in the game save
    progression: bool = (
        False  # Marks an item as being a progression item. Persistent non-progression are marked useful
    )
    silent: bool = False  # These are acquired but not notified to the player


class Q1Level(object):
    name: str
    mapfile: str
    location_defs: List[dict]
    keys: List[str]
    events: List[str] = []
    # must_dive: bool = False  # If the level has locations locked behind diving.
    must_invuln: bool = (
        False  # If the level has locations locked behind invuln lava dives.
    )
    must_bio: bool = False  # If the level has locations locked behind biosuit dives.
    has_boss: bool = (
        False  # If the level awards a boss token in the appropriate goal settings
    )

    def __init__(self):
        self.world: Optional["Q1World"] = None
        self.prefix = f"{self.mapfile}"
        self.locations: Dict[str, LocationDef] = self._make_locations()
        self.used_locations: Set[str] = (
            set()
        )  # locations actually filled in make_region

    def _make_locations(self) -> Dict[str, LocationDef]:
        ret = {}
        for loc_def in self.location_defs:
            loc_name = f'{self.prefix} {loc_def["name"]}'
            ret[loc_name] = LocationDef(
                name=loc_name,
                classname=loc_def["classname"],
                game_id=loc_def["id"],
                uuid=loc_def["uuid"],
                mp=loc_def["mp"],
            )
        return ret

    def create_region(self, world: "Q1World") -> Region:
        self.world = world
        self.used_locations = set()
        ret = self.main_region()
        self.world = None
        return ret

    def main_region(self) -> Region:
        """
        To be implemented by each level
        """
        # Default implementations: everything available in the start region
        # This is wildly incorrect logically, but helps play the levels for configuring the logic
        ret = self.region(self.name)
        self.add_locations([x["name"] for x in self.location_defs], ret)
        return ret

    def region(
        self,
        name: str,
        locations: Optional[List[str]] = None,
        hint: Optional[str] = None,
    ) -> Region:
        ret = Region(
            f"{self.prefix} {name}", self.world.player, self.world.multiworld, hint
        )
        if locations:
            self.add_locations(locations, ret)
        return ret

    def add_location(self, name: str, region: Region):
        location = f"{self.prefix} {name}"
        if name in self.events:
            region.locations.append(
                Q1Location(
                    self.world.player,
                    location,
                    None,
                    region,
                )
            )
        elif self.world.use_location(self.locations.get(location)):
            # special name case for health items as they are managed by spawnflags
            # and the classname varies from the dict entry
            if self.locations[location].classname == "item_health":
                match = re.search(r"(Megahealth|Small Medkit|Large Medkit)", location)
                if match:
                    classname = "item_health " + "(" + match.group(1) + ")"
            else:
                classname = self.locations[location].classname

            # always include secrets and exits
            if classname == "trigger_secret" or classname == "trigger_changelevel":
                pass

            # include all_kills if the option is active
            elif classname == "all_kills" and self.world.options.include_allkills:
                pass

            # handle custom included locations preset
            elif self.world.options.included_locations_preset.value == 4:
                if classname in self.world.options.custom_included_locations.value:
                    # handle item locations, where less than 100% are included
                    spawn_percentage = (
                        self.world.options.custom_included_locations.value[classname]
                        / 100
                    )
                    if not self.world.multiworld.random.random() < spawn_percentage:
                        return
                else:
                    return
            else:
                # handle non-custom preset spawn percentages
                # grab the correct preset dict
                preset_dict = self.world.location_presets[
                    self.world.options.included_locations_preset.value
                ]
                if not classname in preset_dict:
                    return
                spawn_percentage = preset_dict[classname] / 100
                if not self.world.multiworld.random.random() < spawn_percentage:
                    return
            # if all checks pass, add location
            region.locations.append(
                Q1Location(
                    self.world.player,
                    location,
                    self.world.location_name_to_id[location],
                    region,
                )
            )
            self.used_locations.add(location)

    def add_locations(self, locations: List[str], region: Region):
        for loc in locations:
            try:
                self.add_location(loc, region)
            except:
                pass
                # print("Failed to add location ", loc, " to region ", region.name)

    def get_location(self, name) -> Optional[Location]:
        try:
            return self.world.multiworld.get_location(
                f"{self.prefix} {name}", self.world.player
            )
        except KeyError:
            return None

    @staticmethod
    def _resolve_rule_type(
        rules: Optional[Union[RULETYPE, List[RULETYPE]]] = None,
    ) -> Optional[Rule]:
        if rules is None:
            return RuleTrue()
        if not isinstance(rules, List):
            rules = [rules]
        if not rules:
            return None
        rule = rules[0]
        if not isinstance(rule, Rule):
            rule = LambdaRule(rule)
        for other_rule in rules[1:]:
            if not isinstance(other_rule, Rule):
                other_rule = LambdaRule(other_rule)
            rule |= other_rule
        return rule

    def connect(
        self,
        start: Region,
        end: Region,
        rules: Optional[Union[RULETYPE, List[RULETYPE]]] = None,
    ):
        try:
            start.connect(end, None, self._resolve_rule_type(rules))
        except:
            pass
            # ("Failed to connect", start.name, " to ", end.name)

    def restrict(
        self,
        spot: Optional[Union[Location, Entrance, str]],
        rules: Union[RULETYPE, List[RULETYPE]],
    ):
        if isinstance(spot, str):
            return self.restrict(self.get_location(spot), rules)
        if spot is not None:
            spot.access_rule = self._resolve_rule_type(rules)

    @property
    def silver_key(self) -> Rule:
        return self.world.rules.can_door & self.world.rules.has(
            f"{self.prefix} Silver Key"
        )

    @property
    def gold_key(self) -> Rule:
        return self.world.rules.can_door & self.world.rules.has(
            f"{self.prefix} Gold Key"
        )

    @property
    def unlock(self) -> str:
        return f"{self.prefix} Unlock"

    @property
    def rules(self) -> Rules:
        return self.world.rules

    @property
    def items(self) -> List[str]:
        ret = []
        for color in ("Silver", "Gold"):
            if color in self.keys:
                ret.append(f"{self.prefix} {color} Key")
        return ret

    @property
    def map(self) -> str:
        return f"{self.prefix} Automap"

    def event(self, name: str) -> Rule:
        return self.world.rules.has(f"{self.prefix} {name}")


class Q1Episode(object):
    name: str
    levels: List[Q1Level]
    maxlevel: int
    bosslevel: int
