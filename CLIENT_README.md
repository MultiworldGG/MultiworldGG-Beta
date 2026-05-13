# MultiworldGG Client User Guide

This guide covers the standard configuration files, settings, and features available in the MultiworldGG client.

## Configuration File Locations

The client uses several configuration files stored in different locations:

### Installation Directory (Client Root)

These files are located in the MultiworldGG installation directory (where the executable is located, typically `C:\Program Files\MultiworldGG` on Windows):

- **persistent_storage.yaml**: Located in the installation root directory

### User Data Directory

These files are stored in platform-specific user data directories:

#### Windows
- **Base Directory**: `%USERPROFILE%\AppData\Local\MultiworldGG\`
- **client.ini**: `%USERPROFILE%\AppData\Local\MultiworldGG\data\client.ini`
- **config.ini** (Kivy config): `%USERPROFILE%\AppData\Local\MultiworldGG\data\config.ini`

#### macOS
- **Base Directory**: `~/Library/Application Support/MultiworldGG/`
- **client.ini**: `~/Library/Application Support/MultiworldGG/data/client.ini`
- **config.ini** (Kivy config): `~/Library/Application Support/MultiworldGG/data/config.ini`

#### Linux
- **Base Directory**: `~/.local/share/MultiworldGG/`
- **client.ini**: `~/.local/share/MultiworldGG/data/client.ini`
- **config.ini** (Kivy config): `~/.local/share/MultiworldGG/data/config.ini`

## Settings Screen

The settings screen is accessible from the main client interface and is organized into three main categories:

### Connection Settings

#### Profile Section
- **Avatar URL** (`client.ini` → `[client]` → `avatar`)
  - URL to your avatar image
  - Used for display in player lists and chat

- **Alias** (`client.ini` → `[client]` → `alias`)
  - Your display name/alias
  - Updates your slot name when connected

- **Pronouns** (`client.ini` → `[client]` → `pronouns`)
  - Freeform text field for pronouns (e.g., "he/him", "she/her", "they/them")
  - Displayed in player information

#### Status Section
- **In Call** (`client.ini` → `[client]` → `deafened`)
  - Boolean toggle (true/false)
  - Indicates if you're in a call/voice chat
  - Updates your player status

- **In BK** (`client.ini` → `[client]` → `in_bk`)
  - Boolean toggle (true/false)
  - Indicates if you're in "BK mode" (no available checks, grab yourself a burger)
  - Updates your player status

#### Multiworld Settings Section
- **Hostname** (`persistent_storage.yaml` → `client` → `last_server_hostname`)
  - Default: `multiworld.gg`
  - Server hostname or IP address to connect to
  - Stored in persistent storage for persistence across sessions

- **Port** (`persistent_storage.yaml` → `client` → `last_server_port`)
  - Default: `38281`
  - Server port number (1-65535)
  - Stored as an integer in persistent storage

- **Player Slot** (`persistent_storage.yaml` → `client` → `last_username`)
  - Your player slot name
  - Used when connecting to a server
  - Stored in persistent storage as `last_username`

- **Password** (`client.ini` → `[client]` → `password`)
  - Server connection password
  - Stored in plaintext in the config file

- **Admin Password** (`client.ini` → `[client]` → `admin_password`)
  - Admin authentication password for server administration
  - Used for executing admin commands on the server
  - Displayed as "********" in the settings UI for security

### Theming Settings

#### Theme Style Section
- **Dark/Light Mode** (`client.ini` → `[client]` → `theme_style`)
  - Toggle between "Light" and "Dark" theme
  - Default: `Dark`
  - Affects the entire UI appearance

#### Primary Palette Section
- **Color Palette** (`client.ini` → `[client]` → `primary_palette`)
  - Default: `Purple`
  - Selects the primary color scheme for the UI
  - Available palettes vary based on light/dark mode

#### Custom Color Settings Section
- **Text Colors** (stored in `persistent_storage.yaml`)
  - Customize colors for various text elements (markup tags)
  - Each color has separate settings for light and dark themes
  - Colors are stored as hex values in the persistent storage file
  - Includes a reset button to restore default colors

#### Font Settings Section
- **Font Size** (`client.ini` → `[client]` → `font_scale`)
  - Default: `1.0` (100%)
  - Range: 0.5 to 2.0 (50% to 200%)
  - Adjustable via increase/decrease buttons or reset to default
  - Affects all UI text scaling

- **Monospace Font** (`client.ini` → `[client]` → `monospace_font`)
  - Default: `Argon`
  - Font used for monospace text (console, code blocks, etc.)
  - Available options: Argon, Krypton, Neon, Radon, Xenon
  - Selectable via dropdown in the Font Settings section

### Interface Settings

#### Display Section
- **Fullscreen** (`config.ini` → `[graphics]` → `fullscreen`)
  - Boolean toggle (stored as "0" or "1")
  - Toggles fullscreen window mode
  - **Note**: This setting is stored in `config.ini` (Kivy's configuration file), not `client.ini`. The `config.ini` file is located in the same `data` directory as `client.ini` and is managed by the Kivy framework for graphics and window settings.

#### Layout Section
- **Compact Mode** (`client.ini` → `[client]` → `device_orientation`)
  - Boolean toggle (true/false, stored as "0" or "1")
  - Enables compact layout mode for smaller screens or different orientations

#### Scroll Section
- **Lines to Scroll** (`client.ini` → `[client]` → `scroll_lines`)
  - Default: `3`
  - Number of lines to scroll when using scroll controls
  - Config write is debounced (saves 30 seconds after last change)

- **Scroll Velocity** (`client.ini` → `[client]` → `scroll_velocity`)
  - Default: `0.5`
  - Range: 0.0 to 2.0 (displayed as 0-20 in slider, divided by 10)
  - Controls scroll speed/velocity
  - Config write is debounced (saves 30 seconds after last change)

#### Age Filter Section
- **Age Filter** (`client.ini` → `[client]` → `age_filter`)
  - Options: "Not Rated", "16 (Teen)", "12 (Everyone)", "AO (Adult Only)"
  - Filters the game list based on age rating
  - Requires confirmation dialog before applying
  - May take a few seconds to complete the filter update

## Additional Features

### Persistent Storage

The `persistent_storage.yaml` file is located in the MultiworldGG installation root directory and stores various client state and preferences that persist across sessions:

- **Client category**: Stores last username, avatar, pronouns, and other client-specific data
- **Custom text colors**: Stores customized markup tag colors for both light and dark themes
- **Other categories**: May contain additional persistent data for various features

The file uses YAML format and is automatically created if it doesn't exist. If the file becomes corrupted, the client will attempt to back it up with a `.corrupted` extension.

### Server Commands

The client supports server commands that are sent to the MultiworldGG server. These commands are prefixed with an exclamation point (`!`) and include:

- `!help` - Lists available commands
- `!license` - Shows software licensing information
- `!options` - Returns current server options
- `!players` - Shows information about connected players
- `!status` - Shows connection status and check completion
- `!countdown <seconds>` - Starts a countdown timer
- `!alias <alias>` - Sets your alias
- `!admin <command>` - Executes admin commands (requires admin password)

### Configuration File Format

#### client.ini
INI format with a `[client]` section containing all client-specific settings:
```ini
[client]
password = 
admin_password = 
scroll_lines = 3
theme_style = Dark
primary_palette = Purple
font_scale = 1.0
monospace_font = Argon
device_orientation = 0
hostname = multiworld.gg
port = 38281
slot = 
alias = 
avatar = 
pronouns = 
deafened = False
in_bk = False
age_filter = Not Rated
scroll_velocity = 0.5
```

#### config.ini (Kivy Configuration)
This file is managed by the Kivy framework and contains graphics and window settings. It's located in the same `data` directory as `client.ini`. The main setting used by the client is:
```ini
[graphics]
fullscreen = 0
width = 1099
height = 699
# ... other Kivy graphics settings
```
**Note**: Most users should not need to manually edit this file.

#### host.yaml / options.yaml
YAML format containing server-side settings, world-specific options, and generation settings. This file is located in the MultiworldGG installation root directory. It is primarily used by the server and launcher, but some client features may reference it.

#### persistent_storage.yaml
YAML format with categorized key-value pairs:
```yaml
client:
  last_username: "PlayerName"
  avatar: "https://example.com/avatar.png"
  pronouns: "they/them"
  # ... other client data
```

## Troubleshooting

### Configuration Files Not Found
If configuration files are missing, the client will create them with default values on first run:
- `client.ini` and `config.ini` will be created in the user data directory
- `host.yaml` and `persistent_storage.yaml` will be created in the MultiworldGG installation root directory

### Settings Not Saving
- Ensure you have write permissions to the configuration directory
- Check that the files aren't read-only
- On Windows, the directory is typically writable, but if running from a restricted location, settings may be stored in the user's AppData directory

### Corrupted persistent_storage.yaml
If the persistent storage file becomes corrupted:
1. The client will attempt to back it up with a `.corrupted` extension
2. A new empty file will be created
3. You can manually restore from the backup if needed (after fixing any YAML syntax errors)

### Settings Changes Not Taking Effect
- Some settings require a client restart to take full effect
- Theme and color changes apply immediately
- Scroll settings are debounced and save 30 seconds after the last change
- Fullscreen changes apply immediately

## Notes

- Passwords in `client.ini` are stored in plaintext. Keep this file secure if you're concerned about password exposure.
- The admin password field in the UI shows "********" as a placeholder, but the actual password is stored in plaintext in both the config file and host.yaml.
- Font scale changes apply globally to all UI text elements.
- Age filter changes require confirmation and may take several seconds to process as they download and replace the index file.
- Custom text colors are stored separately for light and dark themes, allowing different color schemes for each mode.

