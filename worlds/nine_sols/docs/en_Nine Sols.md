# Nine Sols MultiworldGG Randomizer

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a 
config file.

## What This Mod Changes

- The MultiworldGG/AP items and locations are Yi's core movement abilities, almost every chest in the game (including the jin-only chests), every enemy drop, most of the objects you can examine for "database" entries, and several of the item-granting NPC interactions in FSP.
	- For now, none of the "post-PonR" content is randomized (except that the goal is defeating Eigong).
	- For now, none of the "post-all poisons" / Shennong questline / True Ending content is randomized.
	- For now, no shop items or skill tree upgrades are randomized.
- Starting a New Game will prompt you for MultiworldGG connection info, then put you immediately into the Four Seasons Pavilion (with power already on) instead of the usual intro sequence.
	- Teleport is immediately unlocked, along with one other root node for you to teleport too.
		- For now, this "first node" is always Apeman Facility (Monitoring).
		- This randomizer also depends on the TeleportFromAnywhere mod because you may need it to escape from a "dead end" with an important item.
	- The FSP's front door is "jammed" (i.e. the exit load zone is disabled), so you won't have immediate access to Central Hall.
	- Shuanshuan and Shennong are there immediately.
	- For now, Chiyou will move to FSP after checking the "Factory (GH): Raise the Bridge for Chiyou" location.
		- In vanilla it's triggered by escaping Prison and being rescued by Chiyou, which in randomizer would be too easy to skip over, and IMO would push too many things into a fixed/non-random order.
	- Like in vanilla, Kuafu will move to FSP after checking the "Kuafu's Vital Sanctum" location.
- Many scripted events are now either triggered by sol seal counts, unlocked immediately and forever, or skipped entirely.
	- The Jiequan 1 fight and Prison sequence become available after collecting (for now) 3 sol seals and Mystic Nymph: Scout Mode. Unlike the vanilla game, that's *any* 3 sol seals.
	- The Lady Ethereal Soulscape entrance appears after collecting (for now) any 4 sol seals.
	- For now, the New Kunlun Control Hub entrance opens after collecting 8 sol seals, instead of the Point of no Return cutscenes. This does make Tianhou Research Institute completely optional, but it should also ensure you have to do a lot more than find the SMB item to reach the final Eigong fight.
	- The Peach Blossom Village rescue can be done as soon as you find the Abandoned Mines Access Token and can reach the gate it unlocks. It's no longer tied to escaping Prison and being rescued by Chiyou.
	- All "Limitless Realm" segments are disabled/skipped for now.
	- Ji remains at Daybreak Tower to give you the Ancient Sheet Music even if he's supposed to be somewhere else.
	- Chiyou remains at the Factory (Great Hall) bridge until you check the "Factory (GH): Raise the Bridge for Chiyou" location, even if you do Boundless Repository first.

## Roadmap

High-priority big features:
- randomize Wall Climb, Grapple and Ledge Grab starting abilities
- hard/glitch/trick logic
- random "spawn" / first root node

These are the priorities because they are heavily interconnected, and prerequisites for many other features.

Major features I'll probably do later:
- entrance randomization
- randomizing shop items
- randomizing the skill tree

Smaller features I haven't made up my mind on:
- trap items (Sniper Trap? Prison State Trap? Internal Damage Trap? etc)
- turning root node unlocks into items, like HK's shuffle stag stations option
- decide on additional goals, how to handle post-PonR content, and whether to do anything with the Chien/Chiyou/Shennong quests and True Ending
- in-game hints from the Shanhai 9000s
- randomize BGM

## Credits

- GameWyrm, Gregório, Hopop, Juanba, mynameis, XDrotkon and others in various Nine Sols and Archipelago-related Discord servers for feedback, discussion and encouragement
- dubi steinkek, yuki.kako, N00byKing and others from the "Nine Sols Modding" Discord server for help modding Nine Sols and for creating the other Nine Sols mods that this randomizer relies on or is often played with
- Flitter for talking me into trying out Archipelago randomizers in the first place
- All the Archipelago contributors who made that great multi-randomizer system
- Everyone at Red Candle Games who made this great game