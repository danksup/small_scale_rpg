import random
import json
import os
from fish import Fish
from helper import eight_digit_id_gen

with open("items.json", "r") as f:
	items_data = json.load(f)

with open("equippable.json", "r") as f:
	equippable_data = json.load(f)

with open("inventory.json", "r") as f:
	inventory_data = json.load(f)

with open("fish.json", "r") as f:
	fish_data = json.load(f)

class Inventory:
	def __init__(self, player_obj):
		self._player_obj = player_obj
		self._file = "inventory.json"

		if os.path.exists(self._file):
			with open(self._file, "r") as f:
				try:
					self._inventories = json.load(f)
				except json.JSONDecodeError:
					self._inventories = {}
		else:
			self._inventories = {}

		if self._player_obj._name not in self._inventories:
			self._inventories[self._player_obj._name] = {
				"inventory": {}
			}
		self.save()
	def __getitem__(self, item_name):
		return self._inventories[self._player_obj._name]["inventory"][item_name]

	def __str__(self):
		inv = self._inventories[self._player_obj._name]["inventory"]
		if not inv:
			return f"=== Inventory: {self._player_obj._name} ===\n(empty)"

		lines = [
			f"=== Inventory: {self._player_obj._name} ==="
		]
		
		for item_key, item_value in inv.items():
			try:
				item_type = item_value['type']
				
				if item_key in items_data:
					base = items_data[item_key]
					item_rarity = base['rarity']
					item_price = base['price']
					item_count = inv[item_key]['count']
					main_stat = f"{item_key} [{item_rarity}]"
					lines.append(main_stat)
					lines.append(f"  type: {item_type} | count: {item_count} | price: {item_price} | total worth: {int(item_count) * int(item_price)}")
					other_stats = ""
					for key2, value2 in base.items():
						if key2 in ['critrate', 'critdmg', 'atk', 'defense', 'heal']:
							other_stats += (f"  {key2}: {value2} |")
					lines.append(other_stats)
					lines.append("")

					
				else:
					if item_value['item_name'] in equippable_data:
						base = equippable_data[item_value['item_name']]
						equip_rarity = base['rarity']
						equip_price = base['price']
						equip_name = inv[item_key]['item_name']
						equip_id = inv[item_key]['id']
						equip_durability = inv[item_key]['durability']
						equipped = "equipped" if inv[item_key]['equipped'] else "not equipped"
						main_stat = f"{equip_name}({equip_id}) [{equip_rarity}] - {equipped}"
						lines.append(main_stat)
						lines.append(f"  type: {item_type} | price: {equip_price}")

						other_stats = ""
						for key2, value2 in base.items():
							if key2 in ['critrate', 'critdmg', 'atk', 'defense', 'health']:
								other_stats += (f"  {key2}: {value2} |")
						
						other_stats += f" durability: {equip_durability}"
						lines.append(other_stats)
						lines.append("")

			except KeyError:
				lines.append(f"[Error showing item: {item_key}] with type \"{item_type}\"")
				lines.append("")
				


		return "\n".join(lines)
				
	def save(self):
		with open(self._file, "w") as f:
			json.dump(self._inventories, f, indent=4)

	#todo: buat handle equippable/item biasa. not working. (done)
	def add_item(self, item_name, count=1):
		inv = self._inventories[self._player_obj._name]["inventory"]

		if item_name in equippable_data and item_name not in items_data:
			if equippable_data[item_name]['type'] in ["weapon", "armor_helmet", "armor_chestplate", "armor_leggings", "armor_boots"]:
				this_weapon = equippable_data[item_name] 
				current_id = eight_digit_id_gen()
				inv[f"{item_name}_{current_id}"] = {
					"id" : current_id,
					"weapon type": this_weapon['kind'],
					"rarity": this_weapon['rarity'],
					"item_name": item_name,
			        "count": 1,
			        "durability": this_weapon['durability'],
			        "type": this_weapon["type"],
			        "owner":self._player_obj.name,
			        "origin_owner": self._player_obj.name,
			        "equipped": False
			    }
		elif item_name in items_data and item_name not in equippable_data:
			if item_name in inv:
				inv[item_name]["count"] += count
			else:
				inv[item_name] = {
			        "count": count,
			        "type": items_data[item_name]["type"]
				    }
		else:
			if isinstance(item_name, Fish):
				print(item_name.name)

		self.save()

	def remove_item(self, item_name, count=1):
		inv = self._inventories[self._player_obj._name]["inventory"]

		if item_name in inv:
			inv[item_name]["count"] -= count
			if inv[item_name]["count"] <= 0:
				del inv[item_name]
			self.save()
		else:
			print(f"{item_name} not found in inventory.")

	def get_items(self):
		return self._inventories[self._player_obj._name]["inventory"]

	#todo, remove repetition(done)
	def use_item(self, item_name):
		inv = self._inventories[self._player_obj._name]["inventory"]
		player_obj = self._player_obj
		if item_name in inv:
			for key in items_data[item_name]:
				if key == "heal":
					self._player_obj._health += items_data[item_name]['heal']
				elif key in ['atk', 'critdmg', 'critrate', 'defense']:
					player_stat = getattr(player_obj, key)
					item_stat = items_data[item_name][key]
					setattr(player_obj, key, player_stat + item_stat)
			self.remove_item(item_name)

	def search_by_id(self, search_id):
		inv = self._inventories[self._player_obj._name]["inventory"]
		for key,value in inv.items():
			if value['id'] == search_id:
				return key

		return (None)