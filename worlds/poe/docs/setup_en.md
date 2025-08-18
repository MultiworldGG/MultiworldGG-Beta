# Path of Exile Archipelago Setup Guide

---

## 1) Prerequisites

- Path of Exile installed and playable.
- Python 3.12 installed. (Python 3.13 will not work)
- MultiworldGG (latest release).
- If not used with WMGG: The Path of Exile `.apworld` file from the Path of Exile APWorld release page. (https://github.com/stubobis1/Archipelago/releases)

---

## 2) Download & Install Archipelago

1. Download the latest MultiworldGG release:
   - https://github.com/MultiworldGG/MultiworldGG/releases
2. Install Python if needed:
   - https://www.python.org/downloads/release/python-31210/
---

## 3) Add the Path of Exile `.apworld` (not needed with MWGG)

1. Download the `.apworld`:
   - https://github.com/stubobis1/Archipelago/releases
2. Place the `.apworld` file into the `MultiworldGG/custom_worlds/` folder.

---

## 4) Generate / Join a Multiworld

1. Launch `MultiworldGGLauncher.exe` from your Archipelago folder.
2. Generate Template Options
3. Modify `MultiworldGG/Players/Templates/Path of Exile.yaml` to change options to your liking.
4. Setup a Multiworld session:
  - If self-hosting / playing single player:
    - place the `Path of Exile.yaml` in your Players directory
    - run `MultiworldGGLauncher.exe`
    - Select **Generate Game**.
    - Select **Host**, and select the generated file from `/output`
    - By default the server will run on port `38281`
  - If playing with others:
    - Send your `yaml` to whomever is generating and hosting
    - Get your slot name from the host, and the server address (IP or domain) and port.


---

## 5) Setup Poptracker (Optional but Highly Recommended)

1. Download Poptracker from: https://github.com/black-sliver/PopTracker/releases
2. Extract / Setup Poptracker to a folder of your choice.
3. Download the PoE Archipelago Poptracker pack from: https://github.com/stubobis1/PathOfExilePoptracker/releases
4. Place the zip file into the `poptracker/packs` directory.
5. Launch `PopTracker.exe`.
6. Click on the `AP` button at the top.
7. Enter your slot name and server address from step 4. (Example: `127.0.0.1:38281`, slot `Player1`, no password)
8. If the `AP` button is green you are connected.


---

## 6) Start the Client

1. In `MultiworldGGLauncher.exe` run `Path of Exile` from the client list.
2. Enter the slot name and server address in the top bar 
   - something like `Player1:@127.0.0.1:38281` 
     - (note the `:` after the slot name is where you would put the password, if one was set by the host).
3. Click **Connect**.
4. (optional) Run `/received` to see which class you have received. (not needed if you setup poptracker)
5. Run `/poe_auth` in the client console to authenticate your PoE account.
6. Set the character you will be playing with `/char YourCharacterName`.
7. Set your `client.txt` path by running `/client "C:\PathOfExile\logs\Client.txt"` (adjust path as needed). Note the Quotation marks.
8. Set your item filter path by running `/filter <filterName>.filter` 
    - this should be a local filter, and exist at something like `C:\Users\<USERNAME>\Documents\My Games\Path of Exile`
9. (Optional) Enable or Disable DeathLink with `/deathlink` if you want to share deaths with other players.
10. If you haven't already, Launch Path of Exile and **LOGIN**. 
11. Run `/start` in the client console and enjoy!


---


## 7) In‑Game Chat Commands (Whisper Yourself)

Send whispers **to your own character** using `@YourCharacterName` followed by a command. Example:
```
@YourCharacterName !gems
```

Commands:
```
!ap char                  - Set your character
!deathlink                - Toggle DeathLink
!goal                     - View your current goal
!passive or !p            - List usable passive points
!usable skill gems        - List usable skill gems (by level)
!usable support gems      - List usable support gems
!usable utility gems      - List usable utility gems
!usable gems              - List all usable gems
!main gems                - Show main skill gems received
!support gems             - Show support gems received
!utility gems             - Show utility gems received
!all gems or !gems        - Show all gems received
!gear                     - Show usable gear
!weapons                  - Show usable weapons
!armor                    - Show usable armor
!links                    - Show maximum link allowance
!flasks                   - Show flask unlocks
!ascendancy               - Show unlocked ascendancies
!help                     - Show help message
```

Note: Commands must be whispered to **yourself** (not global chat) using `@YourCharacterName`.

---

## 8) Tips & Troubleshooting

- Keep the MultiworldGG client running while you play PoE.
- If you pick up an item and no check is sent, **enter a new zone** to trigger a check.
- Make sure your PoE logs are being read (client should detect zone changes and chat whispers).
- If the item filter isn’t changing, run `/filter` in the client console.
- DeathLink: When enabled, your deaths (and others’) can be shared as events across players.
- OAuth/API: Ensure your PoE account is properly authenticated if the client needs character data from the API.

---

## 9) Quick Start Summary

1. Install Python (3.12) and MultiworldGG.
2. Drop the PoE `.apworld` into `Archipelago/custom_worlds/`.
3. Use the Launcher to generate or connect to a multiworld.
4. Start playing PoE with the client open.
5. Whisper yourself for status/info commands and change zones to send checks.

---

Happy mapping, and good luck with your drops!
