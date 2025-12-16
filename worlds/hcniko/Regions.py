from typing import NamedTuple, List, Dict


class HereComesNikoRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, HereComesNikoRegionData] = {
    "Menu": HereComesNikoRegionData(["Home"]),
    "Home": HereComesNikoRegionData(["Hairball City","Turbine Town","Salmon Creek Forest","Public Pool",
                                     "Bathhouse","Tadpole HQ", "Gary's Garden", "ChatHome", "ChatParty", "Chatsanity"]),
    "Hairball City": HereComesNikoRegionData(["ChatHC", "BugsHC","ApplesHC"]),
    "Turbine Town": HereComesNikoRegionData(["ChatTT", "BugsTT","ApplesTT"]),
    "Salmon Creek Forest": HereComesNikoRegionData(["ChatSCF", "BugsSCF","ApplesSCF"]),
    "Public Pool": HereComesNikoRegionData(["ChatPP", "BugsPP","ApplesPP"]),
    "Bathhouse": HereComesNikoRegionData(["ChatBath", "BugsBath","ApplesBath"]),
    "Tadpole HQ": HereComesNikoRegionData(["Home Party", "ChatHQ", "BugsHQ","ApplesHQ"]),
    "Home Party": HereComesNikoRegionData([]),
    "Gary's Garden": HereComesNikoRegionData(["ChatGarden"]),
    "ChatHome": HereComesNikoRegionData([]),
    "ChatParty": HereComesNikoRegionData([]),
    "Chatsanity": HereComesNikoRegionData([]),
    "ChatHC": HereComesNikoRegionData([]),
    "ChatTT": HereComesNikoRegionData([]),
    "ChatSCF": HereComesNikoRegionData([]),
    "ChatPP": HereComesNikoRegionData([]),
    "ChatBath": HereComesNikoRegionData([]),
    "ChatHQ": HereComesNikoRegionData([]),
    "ChatGarden": HereComesNikoRegionData([]),
    "ApplesHC": HereComesNikoRegionData([]),
    "ApplesTT": HereComesNikoRegionData([]),
    "ApplesSCF": HereComesNikoRegionData([]),
    "ApplesPP": HereComesNikoRegionData([]),
    "ApplesBath": HereComesNikoRegionData([]),
    "ApplesHQ": HereComesNikoRegionData([]),
    "BugsHC": HereComesNikoRegionData([]),
    "BugsTT": HereComesNikoRegionData([]),
    "BugsSCF": HereComesNikoRegionData([]),
    "BugsPP": HereComesNikoRegionData([]),
    "BugsBath": HereComesNikoRegionData([]),
    "BugsHQ": HereComesNikoRegionData([]),
}

def get_exit(region, exit_name):
    for exit in region.exits:
        if exit.connected_region.name == exit_name:
            return exit