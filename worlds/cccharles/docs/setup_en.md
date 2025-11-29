# Choo-Choo Charles MultiWorld Setup Guide
This page is a simplified guide of the [Choo-Choo Charles Multiworld Randomizer Mod page](https://github.com/lgbarrere/CCCharles-Random?tab=readme-ov-file#cccharles-random).

## Requirements and Required Softwares
* A computer running Windows (the Mod is not handled by Linux or Mac)
* [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases)
* A legal copy of the Choo-Choo Charles original game (can be found on [Steam](https://store.steampowered.com/app/1766740/ChooChoo_Charles/))

## Mod Installation for playing
### Mod Download
All the required files of the Mod can be found in the [Releases](https://github.com/lgbarrere/CCCharles-Random/releases).
To use the Mod, download and unzip **CCCharles_Random.zip** somewhere safe, then follow the instructions in the next sections of this guide. This archive contains:
* The **Obscure/** folder loading the Mod itself, it runs the code handling all the randomized elements
* The **cccharles.apworld** file containing the randomization logic, used by the host to generate a random seed with the others games

### Game Setup
The Mod can be installed and played by following these steps (see the [Mod Download](setup_en#mod-download) section to get **CCCharles_Random.zip**):
1. Copy the **Obscure/** folder from **CCCharles_Random.zip** to **\<GameFolder\>** (where the **Obscure/** folder and **Obscure.exe** are placed)
2. Launch the game, if "OFFLINE" is visible in the upper-right corner of the screen, the Mod is working

### Create a Config (.yaml) File
The purpose of a YAML file is described in the [Basic Multiworld Setup Guide](https://multiworld.gg/tutorial/Archipelago/setup/en#generating-a-game).

The [Player Options page](/games/Choo-Choo%20Charles/player-options) allows to configure personal options and export a config YAML file.

## Joining a MultiWorld Game
Before playing, it is highly recommended to check out the **[Known Issues](setup_en#known-issues)** section
* The game console must be opened to type MultiworldGG commands, press "F10" key or "`" (or "~") key in querty ("²" key in azerty)
* Type ``/connect <IP> <PlayerName>`` with \<IP\> and \<PlayerName\> found on the hosting MultiworldGG web page in the form ``multiworld.gg:XXXXX`` and ``CCCharles``
* Disconnection is automatic at game closure, but can be manually done with ``/disconnect``

## Hosting a MultiWorld or Single-Player Game
See the [Mod Download](setup_en#mod-download) section to get the **cccharles.apworld** file.

In this section, **MultiworldGG/** refers to the path where [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases) is installed locally.

Follow these steps to host a remote multiplayer or a local single-player session:
2. Put the **CCCharles.yaml** to **Archipelago/Players/** with the YAML of each player to host
3. Launch the MultiworldGG launcher and click "Generate" to configure a game with the YAMLs in **MultiworldGG/output/**
4. For a multiplayer session, go to the [MultiworldGG HOST GAME page](https://multiworld.gg/uploads)
5. Click "Upload File" and select the generated **AP_\<seed\>.zip** in **MultiworldGG/output/**
6. Send the generated room page to each player

For a local single-player session, click "Host" in the MultiworldGG launcher by using the generated **AP_\<seed\>.zip** in **MultiworldGG/output/**

## Known Issues
### Major issues
No major issue found.

### Minor issues
* The current version of the command parser does not accept console commands with a player names containing whitespaces. It is recommended to use underscores "_" instead, for instance: CCCharles_Player_1.
