import json
import os
from structures import bot_data, HistoryStack

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

def load_data():
    if os.path.exists("poudlard_data.json"):
        with open("poudlard_data.json", "r") as f:
            try:
                data = json.load(f)
                
                raw_houses = data.get("houses", {})
                for uid, entry in raw_houses.items():
                    if isinstance(entry, str):
                        bot_data.houses[uid] = {
                            "username": "Ancien_Format", 
                            "house": entry
                        }
                    else:
                        bot_data.houses[uid] = entry
                
                raw_histories = data.get("histories", {})
                for uid, entry in raw_histories.items():
                    if isinstance(entry, list):
                        cmd_list = entry
                        username = "Inconnu"
                    else:
                        cmd_list = entry.get("commands", [])
                        username = entry.get("username", "Inconnu")
                    
                    bot_data.user_names[uid] = username
                    
                    new_stack = HistoryStack()
                    for cmd in reversed(cmd_list):
                        new_stack.push(cmd)
                    bot_data.user_histories[uid] = new_stack
                    
            except json.JSONDecodeError:
                pass