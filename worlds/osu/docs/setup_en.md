# osu! Setup Guide for MultiworldGG

## Prerequisites
* Make an osu! account if you don’t have one yet.
* Install the MultiworldGG Launcher - the osu! APWorld is included

## Create an osu! OAuth Application
* Go to: https://osu.ppy.sh/home/account/edit
* Scroll down to **OAuth** and click **New OAuth Application**.
* Name it something informative, e.g., **(YourName) osu!AP Client**.
* In **Application Callback URLs**, enter: `http://localhost:3914`
* Click **Register Application**.
* Copy your **Client ID** and **Client Secret** (do **not** share your Client Secret; you can reset it if needed).

## Find Your Player/User ID
* Open your osu! profile; the number in the URL is your ID (e.g., `https://osu.ppy.sh/users/10794430` → Player ID is `10794430`).

## Launch and Configure the Client
* Launch the client through the **MultiworldGG Launcher** (make sure the osu!ap world is installed).
* Set your credentials:
  * Client ID: `/set_client_id <your_client_id>`
  * Client Secret (API key): `/set_api_key <your_client_secret>`
  * Player ID: `/set_player_id <your_player_id>`
* Save keys for future launches: `/save_keys`
* On future launches, load them with: `/load_keys`

## Basic Play Commands
* See which songs are currently in logic: `/songs`
* Download a specific song by its **Song #** (the number before the `:` in `/songs`, not the Beatmap/Set ID): `/download <song_number>`
* Download the next song in logic: `/download next`

## Auto Tracking
* After loading your keys, start tracking a mode: `/Auto_Track [mode]`
* Valid modes: `Osu`, `Taiko`, `Fruits`, `Mania`
* The client checks for new scores about every 4 seconds; give it a moment for items to send.
* Converted maps count as the mode you played them in.

## Helpful Options & Saving Settings
* Automatically download the next song after a clear: `/auto_download`
* Switch to osu!direct downloads: `/download_type`
* Save your current settings: `/save_settings`
* Load your saved settings: `/load_settings`
* Once keys and settings are saved, quickly jump back in next time: `/load_all`

## Updating Score Sends
* If a score matches a song you’ve received/started with, it will send on update: `/update`
* With auto tracking enabled, sends also occur automatically every ~4 seconds.

## Progress & Goal
* After earning enough **Performance Points** (“Music Sheets”), your **Goal Song** will appear in `/songs`.
* Clear the Goal Song and finalize any remaining scores to **goal** your game.
