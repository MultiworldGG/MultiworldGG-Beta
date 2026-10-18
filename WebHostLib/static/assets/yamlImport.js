function loadFileDialog() {
    var input = document.createElement('input');
    input.type = 'file';
    input.setAttribute("accept", ".yml,.yaml");
    input.click();

    input.onchange = e => { 
        document.getElementById("yamlImport").disabled = true;
        var file = e.target.files[0]; 

        // setting up the reader
        var reader = new FileReader();
        reader.readAsText(file,'UTF-8');

        // here we tell the reader what to do when it's done reading...
        reader.onload = readerEvent => {
            var content = readerEvent.target.result; // this is the content!
            parseYML(content)
        }

        setTimeout(() => {
            document.getElementById("yamlImport").disabled = false;
        }, 3500);
     }
}

function parseYML(yaml) {
    var jsonObj = jsyaml.load(yaml); 
    var storageObj = {
        "inputs": {},
        "checkboxes": {}
    }

    //console.log(jsonObj);

    if ("name" in jsonObj)
        storageObj.inputs["player-name"] = jsonObj.name;
        storageObj.inputs["game-options-preset"] = "custom";
        storageObj.inputs["progression_balancing-select"] = "custom";
    
    if ("game" in jsonObj) {
        Object.keys(jsonObj[jsonObj.game]).forEach(key => {
            let settingValue = jsonObj[jsonObj.game][key];

            if (key == "sprite") //remove sprite
                return;

            if (Array.isArray(settingValue)) {
                storageObj.inputs[key] = settingValue;
            }
            else if (settingValue == "random" && key != "map_shuffle_seed") //exception for FFMQ
                storageObj.checkboxes["random-" + key] = true;
            else {
                if (["local_items", "non_local_items", "start_hints", "start_location_hints", "exclude_locations", "priority_locations"].includes(key)) {
                    storageObj.checkboxes[`${key}-${settingValue}`] = true;
                }
                else if ((key == "start_inventory" || key == "start_inventory_from_pool") && settingValue != {}) {
                    let startingItems = Object.keys(jsonObj[jsonObj.game][key]);
                    for (var i=0; i<startingItems.length; i++) {
                        let item = startingItems[i];
                        storageObj.inputs[`${key}-${item}-qty`] = jsonObj[jsonObj.game][key][item].toString()
                    }
                } else {
                    storageObj.inputs[key] = settingValue;
                }
            }
        });

        loadSettings(storageObj);
    }
    
}
