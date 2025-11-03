# Super Mario 64 Hacks Setup Guide

## NOTE
Use and discussion of this apworld (unfortunately) is not allowed anymore in the main archipelago server. Please ask for support in our Discord, or join [this one](https://discord.gg/Nu4X9gmGDR) instead if you want help, or just want to share a json file.

## Required Software
* [Luna's Project64](https://github.com/Luna-Project64)
* [PJ64 Connector Script](https://github.com/DNVIC/archipelago-sm64hacks/releases/latest)

## Video Guide
A Video guide can be found [here](https://youtu.be/ugKJhTIC1OE), which describes the setup process in detail. Note that in the MultiworldGG client, the json files go in data/sm64hacks/

## JSON Generation
While the websites provides a selection of common romhacks, custom ones can be used with this apworld and then be generated locally.

First, create a json file using [this website](http://dnvic.com/ArchipelagoGenerator/index.html), using a .jsml file. You can get a .jsml file for a hack by loading up a hack in PJ64/Mupen64/Retroarch, opening [stardisplay](https://github.com/aglab2/SM64StarDisplay), and finding the layout folder in the same folder the exe file is in.
You can also get premade json files [here](https://github.com/DNVIC/sm64hack-archipelago-jsons)

Then, get the .jsml file from the layout folder located where the stardisplay .exe is.

Input the jsml file into the website, and fill out the requirements for everything in the hack, by clicking on the stars, cannons, caps/keys, or courses. Most hacks only really have star and key requirements, and maybe per-star cap requirements, but some hacks have more complicated requirements. If a cannon exists, select it, hit the exists checkbox, add requirements, and hit save. Same with keys/caps. Conditional requirements are a bit more confusing, but are necessary if for example you can get to a level with either the vanish cap or key 2. You'd create one conditional requirement for the vanish cap, and one for key 2, and that'll make it so only one is required.

Click on the victory text at the bottom, and put whatever is required to achieve "Victory" in the hack. As it is, this will not be automatically be achieved in the rando when you get it, since its impossible to know what constitutes victory for an arbitrary hack, but its still important since the rando makes sure that victory is possible. If you want to, you can say when you get victory by running the "Victory.js" script when playing the game. It's the honor system, but the best I can do.

Export the .json file, and put it data/sm64hacks/ in your MultiworldGG folder

Copy the template.yaml, change json_file to be the json file you just made (and if you want keys to be progressive, enable that as well), and place it in the worlds folder.

Once your world is generated, open the hack you want to play, and delete/move files A and B (this is important)
Open the rom in [Luna's Project64](https://github.com/Luna-Project64), and open the generic bizhawk client (DO NOT use BizHawk, despite the name. It might work on BizHawk, but I haven't tested it and I am not providing any support to BizHawk users.) Go to Debugger -> Scripts (enable debugger if it isn't enabled), download the two .js files from the releases page, put them in the scripts folder (the scripts folder is in the folder that opens when you hit the ... button in the bottom left), run the 'connector_pj64_generic.js', and you should be ready to go! 


## Join a World

Open the rom in PJ64/Mupen/Retroarch, open the [stardisplay client](https://github.com/DNVIC/Archipelago-StarDisplay), right click -> archipelago, log in, and you should be ready to go!
