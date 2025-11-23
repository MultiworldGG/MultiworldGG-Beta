# The Legend of Zelda: Phantom Hourglass AP Setup Guide

## Required Software

* [MultiworldGG 0.7.150+](/tutorial/Archipelago/setup/en)
* [Bizhawk 2.10+](https://github.com/TASEmulators/BizHawk)
* Legally acquired Phantom Hourglass EU rom (US support coming soon). Apparently it only works in English
* [Latest tloz_ph.apworld](https://github.com/carrotinator/Archipelago/releases) (ships with MWGG)

## Recommended Software

* [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases)
* [Item Tracker](https://github.com/ZobeePlays/PH-AP-Item-Tracker/tree/main) (poptracker pack by @ZobeePlays. No map tracking)

## Setup

1. Find your MultiworldGG directory, and put `tloz_ph.apworld` in the `custom_worlds` folder (not needed with MWGG)
2. Create a yaml settings file, and put it in the MultiworldGG directories `players` folder. You can generate a template yaml with the archipelago launcher.
3. Generate your game
4. Host the game, either locally or via the MultiworldGG web hosting service
5. Open the `generic bizhawk client` in MultiworldGG, and connect to the server
6. Launch the vanilla game in bizhawk, and open the lua console. Add the `connector_bizhawk_generic.lua` script that can be found in `MultiworldGG\data\lua`. 
7. You are now ready to play! Start a new savefile and go! You can check that everything worked by checking if the bridge has been repaired.

## Further Reading

- [FAQ and Credits](https://github.com/carrotinator/Archipelago/blob/main/worlds/tloz_ph/docs/faq_and_credits.md)
- [Tricks and Skips](https://github.com/carrotinator/Archipelago/blob/main/worlds/tloz_ph/docs/tricks_and_skips.md)
- [wiki](https://github.com/carrotinator/Archipelago/wiki) contains locations, maps, groupings and stuff
