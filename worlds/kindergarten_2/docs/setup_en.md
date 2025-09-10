# Kindergarten 2 MultiworldGG Setup Guide

## Required Software
- [MultiworldGG](https://github.com/MultiworldGG/MultiworldGG/releases)
- A version of Kindergarten 2 on PC
- The latest [Archipelagarten Mod](https://github.com/agilbert1412/Archipelagarten/releases)

## Configuring your YAML file

### What is a YAML file and why do I need one?

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a YAML file?

You can customize your options by visiting the [Kindergarten 2 Player Options Page](/games/kindergarten_2/player-options)

## Joining a MultiWorld Game

### Connect to the MultiServer
- Optional, but recommended: Make a copy of your Kindergarten 2 game directory, to avoid modding your original game.
- Extract the downloaded Archipelagarten zip file into your (copied) Kindergarten 2 game directory (you should see the `BepInEx` folder alongside other data in the root of the game directory)
- Edit the `ArchipelagoConnectionInfo.json` and enter the ip, port, slot name, etc.
- Run Kindergarten2.exe. It should automatically connect, or fail to do so and tell you in the console

## Note
Your MultiworldGG save will take up all 3 save slots, and your original saves will be unaffacted, but inaccessible as long as you remain modded (This is why making a copy of the original, to have a vanilla game available, was recommended).