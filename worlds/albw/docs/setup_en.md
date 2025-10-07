# A Link Between Worlds Setup Guide

This guide has been directly copied from the wiki, [please go there](https://github.com/Legendgreat/setting-up-albw-ap/wiki/Setting-up-ALBW-for-Archipelago) for the most up to date information.

# Setting up ALBW for Archipelago

## Preface

If you came here to troubleshoot while joining or hosting a sync/async, I recommend switching to another game for now and troubleshooting later.

The setup is a little finnicky and the reason it doesn't work on your machine can have lots of different reasons.

You don't wanna be the person who is troubleshooting for an hour while the rest is waiting on you.

## Platform disclaimer

##### Windows

This guide should work flawlessly for any machine running Windows 10+.

##### Linux

For Linux, I recommend getting the `.tar.gz` version of Archipelago; this guide should work for that version. The `AppImage` version is more complex and I might make a guide for that in the future, but currently this guide will not work.

## What you need

- [ ] The latest version of [Azahar](https://azahar-emu.org/) ([GitHub releases](https://github.com/azahar-emu/azahar/releases)) or Citra/Lime3DS.
- [ ] A decrypted, untrimmed and North American version of The Legend of Zelda: A Link Between Worlds ROM.
- [ ] All 3 files of the latest release of [albw-archipelago](https://github.com/randomsalience/albw-archipelago/releases) by randomsalience.
  - `A.Link.Between.Worlds.yaml` (you can have Archipelago generate a template yaml as well after setting up the other two)
  - `albw.apworld`
  - `albwrandomizer.zip`
- [ ] Some patience and perseverance.

## Setting up Archipelago

If you have somehow come to this guide and not already installed Archipelago, click [here](https://archipelago.gg/tutorial/) for in-depth guides on Archipelago and how to use it.

First you want to open the Archipelago data folder, by opening the Archipelago launcher and clicking on `Browse Files`. In there, you should have a bunch of folders and ArchipelagoXXXXXXXX.exe files.
The folders we are interested in are:

- `custom_worlds`
- `lib`
- `Players`

In `custom_worlds`, you simply drag and drop the `albw.apworld` file.

In `lib`, we want to extract the _contents_ of the `albwrandomizer.zip`. It should be a folder called `albwrandomizer`.

Finally, in `Players` you place the `A.Link.Between.Worlds.yaml` file. This yaml file contains your randomization options, and you will want to adjust those, or at the very least change the Player name in there. I recommend [VSCode](https://code.visualstudio.com/) or [Notepad++](https://notepad-plus-plus.org/) for this.

If you want to change your options, most of the settings have comments above them about what they do and how to set them, but there is a more detailed guide [here](https://github.com/rickfay/z17-randomizer/blob/master/README.md) that explains in detail what all the options do. There is another even more detailed guide [here](https://archipelago.gg/tutorial/Archipelago/advanced_settings/en) on Archipelago's website that explains .yaml files in general, how they work and all the ways you can configure them.

<sub>You can name this file anything you'd like, it doesn't have to be A.Link.Between.Worlds.yaml, I'm just maintaining this name for the guide.</sub>

If you have done all this, Archipelago should be set up properly, and should look like the following outline:

<pre>
Archipelago
├─ custom_worlds
│  └─ albw.apworld
├─ lib
│  └─ albwrandomizer
│     ├─ __init__.py
│     ├─ albwrandomizer.cp311-win_amd64.pyd
│     └─ ...
├─ Players
│  └─ A.Link.Between.Worlds.yaml
└─ ...
</pre>

## Setting up Azahar/Citra/Lime3DS

Now that you have Archipelago set up correctly, we can move on to setting up your emulator so that it's ready for ALBW.

It's recommended to use Azahar as Azahar is the only 3DS emulator that is still being maintained. That being said, Citra and Lime3DS will work fine if you already have one of those installed, although file paths might be slightly different. If you run into any Citra/Lime3DS specific issues, please upgrade to Azahar before asking for help. I will refer to Azahar often from this point in the guide, but if you are using Citra or Lime3DS just mentally swap the name.

Assuming you have Azahar installed properly, we want to set up 3 things to be able to play ALBW in Archipelago.

- Dumping a valid patchable ROM
- Creating a patch folder
- Turning on RPC server
- Duplicating your ROM (optional)

### Dumping a valid patchable ROM

This guide does not condone piracy, and as such will not help with finding illicit ROMs. Instead we will focus on dumping a legal game from 3DS hardware.

The ROM we need should be in the _North America_ region. If you already have a ROM, you can quickly see if it's of North American region by opening up Azahar and adding an application directory pointing to the ROM. Under "Region" it should say "North America", if it doesn't, you will need a different ROM.

##### Dumping and decrypting a ROM

There is a very in-depth guide [here](https://3ds.hacks.guide/dumping-titles-and-game-cartridges.html#dumping-a-game-cartridge) (see section of "Dumping a game cartridge") that explains in detail how to dump a ROM and what you need, which I recommend you follow to the tee if you don't want to accidentally brick your 3DS. At the very bottom of the same guide [here](https://3ds.hacks.guide/dumping-titles-and-game-cartridges.html#encrypting-decrypting-a-cia-file), there is also a guide on how to decrypt ROMs. Alternatively, you can decrypt on Windows as well using [this](https://gbatemp.net/download/batch-cia-3ds-decryptor.35098/), if you forgot this step and already moved your ROM to your machine.

When you dump your rom, make sure to have Godmode9 make an untrimmed version of .3ds format, and decrypt it as well. The next step will _not_ work with an encrypted, or trimmed version of the ROM.

### Creating a patch folder

Assuming you now have decrypted, untrimmed and North American version of ALBW in `.3ds` format, we can continue with creating a patch folder that you will need to randomize your game and connect to the Archipelago client.

To do so, you will need a `.apalbw` file.

##### Getting a .apalbw file

To get your `.apalbw` file, Archipelago will need to generate a seed. Again, I recommend doing this in a test gen or for a solo run before trying to do this while joining or hosting a sync/async, to avoid having to troubleshoot while other players are waiting on you.

If you are joining a sync/async, you can get this file from the host. Ask them for the zip file, or the `.apalbw` file inside the zip.

If you are doing a solo run or hosting a sync/async, we will first need to generate a seed. To do this, simply click on `Generate` in the Archipelago Launcher, and click on `Browse Files` after that and browse to the `output` folder. In there you will find a `AP_xxxxxxx.zip` file, which will contain your `.apalbw` file. If you instead got an error trying to generate, refer to the troubleshooting section below.

##### Creating a patch folder

Now that you have your `.apalbw` file, either drag your file onto the Archipelago Launcher, or click on `Open Patch` in the launcher. This will open a file select that will ask you to point to the patch (only if you clicked on "Open Patch"), and next another file select that will ask you to point to your ROM (only when doing this for the first time). After you did this, you will find a `AP_xxx...\_P#\_Player.zip` file next to your .apalbw file.

If you opened an invalid ROM during this step, and `Open Patch` keeps selecting that invalid ROM by default, you can rename it or delete it to get the ROM file select menu again.

##### Loading your mod

Back in Azahar, click on `File > Open Azahar Folder`. In there, you will see folder named `load`, if you don't, create one. In the `load` folder, you will see a folder named `mods`, again if it's not there, create that as well.

In the `mods` folder, you will want to extract the _contents_ of the `AP_xxx...\_P#\_Player.zip` file we just made.

If done properly, it should look something like this:

<pre>
Azahar
├─ load
│  └─ mods
│     └─ 00040000000EC300
│        ├─ romfs
│        ├─ code.ips
│        └─ exheader.bin
└─ ...
</pre>

### Turning on RPC server (only in Azahar v2121+)

Azahar has an RPC server that allows the ALBW patch to connect to Archipelago. By default, it's turned off and it won't connect. To turn it on, simply go to `Azahar > Emulation > Configure > Debug` and `Enable RPC server`.

### Emulator language

Changing the emulator language is akin to changing your 3DS language, in that the game itself will mimic the language. This is to say that the randomized game only works in English. If you have your emulator language set to French or Spanish, the game will not work properly with AP. Any other language besides those two will default back to English and work properly, except French and Spanish.

### Duplicating your ROM file (optional)

Azahar does not allow you to use `.3ds` files to play games, only `.cci` files, but we need a `.3ds` file to patch. As such, you might find it handy to duplicate your `.3ds` rom (copy > paste), and simply changing the file extension from `.3ds` to `.cci`. This works perfectly fine, and will allow Azahar to run the game.

If you have done all these steps correctly, you should be able to simply start the game in Azahar, and connect to your Archipelago room port (`archipelago.gg:#####`). If working correctly, the Archipelago Client should say `Connected` and all the `Room Information` below. If you do not see `Emulator connected`, refer to the troubleshooting section below.

## Test your setup

A final test you can do to see if everything is working properly is to start your game in Azahar, going to file select, and see if the code of the seed is displayed in a bunch of symbols at the top. If it is, it means you properly genned, patched, and set up Azahar.

## Troubleshooting

### Archipelago exceptions

##### Exception: No world found to handle game A Link Between Worlds

If you get this error trying to generate, check if your Archipelago folder matches this outline:

<pre>
Archipelago
├─ custom_worlds
│  └─ albw.apworld
├─ lib
│  └─ albwrandomizer
│     ├─ __pycache__
│     └─ ...
├─ Players
│  └─ A.Link.Between.Worlds.yaml
└─ ...
</pre>

The location of the `albw.apworld` file and `albwrandomizer` folder are very specific, and need to be exactly in the places they are in the outline.

If your folder structure matches the outline, see if either the `.apworld` or `albwrandomizer` are outdated.

<sub>If you are trying to do this on Linux, please use the `.tar.gz` version of Archipelago instead of `AppImage`. This outline will _not_ work on the `AppImage` version.</sub>

##### The running game was not patched with an Archipelago patch.

If you got this error on Archipelago Client after patching and running the game in Azahar, chances are you used a _trimmed_ version of the ROM to create a patch folder. To fix this, you will have to dump an untrimmed version of the ROM and run the patch again.

### Azahar crashes

##### Playing ALBW after extracting into load/mods

If Azahar crashes when loading ALBW after extracting your mod folder into `load/mods`, follow these steps:

1. Make sure you used a valid ROM to patch your game. If the ROM was not decrypted, and of North American region, the patch will not work and instead crash Azahar.
2. Make sure you extracted to the correct location. See the "Loading your mods" section for an outline of how your folders should look like.
3. See if Azahar crashes even when removing the `00040000000EC300` folder from `load/mods`. If it does, you might want to troubleshoot Azahar instead.
4. See if any game loads in Azahar if you have any other games. If they don't, you might have screwed up your `load/mods` folder previously and corrupted Azahar's game data. You will need to delete your `%Appdata%/Azahar/nand/data` folder. This will delete all your save files so make sure to make a backup of this folder if you want to keep any save files.
5. If none of these steps worked, you can ask for further help in the Archipelago Discord at the channel `future-game-design > The Legend of Zelda: A Link Between Worlds`.

### Connecting to emulator...

Make sure you have enabled the RPC server in Azahar by going to `Emulation > Configure > Debug` and enabling RPC server.

### Archipelago is connected to the emulator but the game isn't randomized

Please make sure your game is English and not French or Spanish. The randomizer only works in English. To change this, change the emulator language to any language *but* French or Spanish. Non English/French/Spanish emulator languages will default to English on the North American version.