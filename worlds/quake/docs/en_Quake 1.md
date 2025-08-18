# Quake 1 Randomizer for MultiworldGG

## Where is the options page?

The [player options page for this game](../player-options) contains most of the options you need to 
configure and export a config file. 

# How the randomizer works
All weapon and inventory pickups have been converted into AP locations. 
If enabled, secret sectors also get converted to locations if the selected goal does not include secrets.

Unlockable items are weapons, ammunition capacity and inventory items.
If enabled, the ability to jump, crouch, sprint, dive into water, open doors and use switches have to be unlocked. 

Progression inventory items are restored on every level entry. 
The logic is designed so that locations can be checked from the start of a level 
with the unlocked capacity thresholds, but not necessarily all locations can be checked in a single go. 
Simply restart a level to try again.

Ironwail_AP adds an inventory system to Quake.
The required keys need to be bound in Ironwail under Options->Key Setup.
The AP keybinds are at the bottom of the page.

AP Quad Damage: Activates Quad Damage
AP Invuln: Activate Invulnerability
AP Biosuit: Activate Biosuit
AP Backpack: Gives ammo equivalent to an ammo pickup of every weapon type
AP Medkit: Heals for 25 HP, HP over 100 gets reduced comparable to Megahealth.
AP Armor: Adds 25 armor. Armor type (green,yellow,red) is set based on armorvalue (50, 100, 200).
AP Automap: Shows a 3D view of the available items, secrets and exits if the automap for the level was received.
