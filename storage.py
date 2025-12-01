import json
import os
from structures import bot_data, HistoryStack

# Saves bot data (houses and user histories) to a JSON file
def save_data():
    histories_export = {}
    for uid, stack in bot_data.user_histories.items():
        histories_export[uid] = {
            "username": bot_data.user_names.get(uid, "Inconnu"),
            "commands": stack.get_all()
        }

    data = {
        "houses": bot_data.houses,
        "histories": histories_export
    }
    
    with open("poudlard_data.json", "w") as f:
        json.dump(data, f, indent=4)

# Loads bot data (houses and user histories) from a JSON file
def load_data():
    if os.path.exists("poudlard_data.json"):
        with open("poudlard_data.json", "r") as f:
            try:
                data = json.load(f)
                
                # Load houses data
                raw_houses = data.get("houses", {})
                for uid, entry in raw_houses.items():
                    if isinstance(entry, str):  # Handle old data format
                        bot_data.houses[uid] = {
                            "username": "Ancien_Format", 
                            "house": entry
                        }
                    else:
                        bot_data.houses[uid] = entry
                
                # Load user histories
                raw_histories = data.get("histories", {})
                for uid, entry in raw_histories.items():
                    if isinstance(entry, list):  # Handle old data format
                        cmd_list = entry
                        username = "Inconnu"
                    else:
                        cmd_list = entry.get("commands", [])
                        username = entry.get("username", "Inconnu")
                    
                    bot_data.user_names[uid] = username
                    
                    # Rebuild the history stack
                    new_stack = HistoryStack()
                    for cmd in reversed(cmd_list):
                        new_stack.push(cmd)
                    bot_data.user_histories[uid] = new_stack
                    
            except json.JSONDecodeError:
                pass  # Ignore errors if the file is corrupted