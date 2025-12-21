# Majora's Mask Recompiled Setup Guide

## Required Software

- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases)
- [Visual Studio C++ Redist](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-microsoft-visual-c-redistributable-version)
- [Latest MMRecompRando](https://github.com/RecompRando/MMRecompRando/releases/latest)
- [Zelda64Recomp](https://github.com/Zelda64Recomp/Zelda64Recomp/releases)
- Majora's Mask NTSC-U Rom File

## Optional Software

- [Mods from Thunderstore](https://thunderstore.io/c/zelda-64-recompiled/)
- [Poptracker Bundle](https://github.com/G4M3RL1F3/Majoras-Mask-AP-PopTracker-Pack/releases/latest)

## Mod Setup

1. Download the latest [Visual Studio C++ Redist](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-microsoft-visual-c-redistributable-version).
2. Optionally download any additional mods or texture packs you'd like from [Thunderstore](https://thunderstore.io/c/zelda-64-recompiled/).
    1. You only need to drag and drop mod zips from Thunderstore onto the game window to install them.
3. Download [MMRecompRando.zip](https://github.com/RecompRando/MMRecompRando/releases/latest).
4. Place the mods within the zip into the Zelda64Recomp mods folder, as well as any texture packs you've downloaded.
    1. If on Windows, this is located at `%LOCALAPPDATA%\Zelda64Recompiled\mods`.
    2. If on Linux, this is located at `~/.config/Zelda64Recompiled/mods`.
5. You can also download [poptracker](https://github.com/black-sliver/PopTracker/releases/latest) along with [G4M3RL1F3's fork of Seto's pack](https://github.com/G4M3RL1F3/Majoras-Mask-AP-PopTracker-Pack/releases/latest)
6. Open `Zelda64Recompiled`, select your ROM, and hit Start Game.

## FAQ

### I launched this mod and my save is gone? Did rando delete my save?

Don't worry, your vanilla saves are intact. When playing this mod, a per-session savefile will be created. Your normal save file will not be touched.

### I got Letter to Kafei and now I can't use the Pendant of Memories! Is it just gone?

Try moving your cursor to the Letter to Kafei and pressing the N64's L button. That should cycle through all quest items in that slot. That's true for the Moon's Tear item slot and the Room Key item slot as well.

### I opened a chest/got a check and it always shows a grey Archipelago item, what's wrong with you?

The phantom AP item means the check is not yet implemented. Please use a text client or Seto's/G4M3RL1F3's amazing poptracker pack from step 5 to see checks that you can definitely get (though some implemented checks may be missing until the tracker is updated).

If you picked up a phantom on a check that should be implemented, you can open an issue on this repo letting us know!

## Known Issues

- Kotake sometimes does not show the price of her shopsanity item in the second dialogue.
