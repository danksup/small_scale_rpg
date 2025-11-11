import json

with open("items.json", "r+") as f:
	items_data = f

all_items = items_data

def push(self):
	with open("items.json" "w") as f:
		json.dump(all_items, f, indent=4)