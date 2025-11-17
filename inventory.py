import json
import os
from fish import Fish
from helper import eight_digit_id_gen, parse_number, pagination
from datetime import datetime
import re

with open("items.json", "r") as f:
	items_data = json.load(f)

with open("equippable.json", "r") as f:
	equippable_data = json.load(f)

with open("inventory.json", "r") as f:
	inventory_data = json.load(f)

with open("fish.json", "r") as f:
	fish_data = json.load(f)

with open("fishing_rod.json", "r") as f:
	rod_data = json.load(f)

with open("bobber.json", "r") as f:
	bobber_data = json.load(f)

rarity_dict = {
	"common":800000,
	"uncommon":100000,
	"rare": 50000,
	"epic": 35000,
	"legend":10000,
	"mythic": 4450,
	"secret": 550
}

datenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

	def __contains__(self, item_name):
		return item_name in self._inventories[self._player_obj._name]["inventory"]

	def __str__(self):
		inv = self._inventories[self._player_obj._name]["inventory"]
		if not inv:
			return f"=== Inventory: {self._player_obj._name} ===\n(empty)"

		lines = [
			f"=== Inventory: {self._player_obj._name} ==="
		]
		
		for item_key, item_value in inv.items():
			lines.append(self.item_formating(item_key))

		return "\n".join(lines)
	
	def printinv(self, page):
		inv = self._inventories[self._player_obj._name]["inventory"]
		if not inv:
			return f"=== Inventory: {self._player_obj._name} ===\n(empty)"
		print(f"=== Inventory: {self._player_obj._name} ===")
		lines = [
			
		]
		
		for item_key, item_value in inv.items():
			lines.append(self.item_formating(item_key))

		pagination(lines, page)
		# return "\n".join(lines)

	def item_formating(self, item_input):
		inv = self._inventories[self._player_obj._name]["inventory"]
		lines = []
		try:
			item_key = item_input
			item_value = inv[item_key]
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

			elif item_key in rod_data:
				base = rod_data[item_key]
				item_rarity = base['rarity']
				item_price = base['price']
				equipped = "equipped" if inv[item_key]['equipped'] else "not equipped"
				main_stat = f"{item_key} [{item_rarity}] - {equipped}"
				lines.append(main_stat)
				lines.append(f"  type: {item_type} | price: {int(item_price)}")
				other_stats = ""
				for key2, value2 in base.items():
					if key2 in ['fishing_luck', 'reeling_speed', 'fishing_speed']:
						other_stats += (f"  {key2}: {value2} |")
				lines.append(other_stats)
				lines.append("")
			elif item_key in bobber_data:
				base = bobber_data[item_key]
				item_rarity = base['rarity']
				item_price = base['price']
				equipped = "equipped" if inv[item_key]['equipped'] else "not equipped"
				main_stat = f"{item_key} [{item_rarity}] - {equipped}"
				lines.append(main_stat)
				lines.append(f"  type: {item_type} | price: {int(item_price)}")
				other_stats = ""
				for key2, value2 in base.items():
					if key2 in ['fishing_luck', 'reeling_speed', 'fishing_speed']:
						other_stats += (f"  {key2}: {value2} |")
				lines.append(other_stats)
				lines.append("")
				
			else:
				if item_value['type'] != 'fish' and item_value['item_name'] in equippable_data:
					base = equippable_data[item_value['item_name']]
					equip_rarity = base['rarity']
					equip_price = base['price']
					equip_name = inv[item_key]['item_name']
					equip_id = inv[item_key]['id']
					equip_durability = inv[item_key]['durability']
					origin_owner = inv[item_key]['origin_owner']
					obtained_at = inv[item_key]['obtained_at']
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
					lines.append(f"  obtained by: {origin_owner} at {obtained_at}")
					lines.append("")
				else:
					if item_value['type'] == 'fish':
						#base = fish_data[item_value['species']]
						fish_weight = item_value['weight']
						fish_mutation = item_value['mutation']
						fish_price = item_value['price']
						fish_rarity = item_value['rarity']
						fish_caught_by = item_value['caught_by']
						fish_caught_at = item_value['caught_at']
						fish_species = item_value['species']
						fish_id = item_value['id']

						main_stat = f"{fish_species}({fish_id}) [{fish_rarity}]"
						lines.append(main_stat)
						lines.append(f"  type: {item_type} | price: {fish_price}")

						other_stats = f"  weight: {fish_weight} | mutation: {fish_mutation} |\n  caught by: {fish_caught_by} at {fish_caught_at}"
						lines.append(other_stats)
						lines.append("")


		except KeyError as e:
			try:
				lines.append(f"[Error showing item: {item_key}] with type \"{item_type}\"")
				import traceback
				error_trace = traceback.format_exc()
				lines.append("Traceback (most recent call last):")
				lines.append(error_trace)
				lines.append("")
			except UnboundLocalError:
				print('lol')
				import traceback
				error_trace = traceback.format_exc()
				lines.append("Traceback (most recent call last):")
				lines.append(error_trace)
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
					"weapon_type": this_weapon['kind'],
					"rarity": this_weapon['rarity'],
					"item_name": item_name,
			        "count": 1,
			        "durability": this_weapon['durability'],
					"enchanment": None,
			        "type": this_weapon["type"],
			        "owner":self._player_obj.name,
			        "origin_owner": self._player_obj.name,
					"obtained_at": datenow,
			        "equipped": False,
			    }
		elif item_name in items_data and item_name not in equippable_data:
			if item_name in inv:
				inv[item_name]["count"] += count
			else:
				inv[item_name] = {
			        "count": count,
			        "type": items_data[item_name]["type"]
				    }
		elif item_name in rod_data:
			this_rod = rod_data[item_name]
			inv[f"{item_name}"] = {
				"type": this_rod['type'],
				"rarity": this_rod['rarity'],
				"item_name": item_name,
				"enchanment": None,
				"obtained_at": datenow,
				"count": 1,
			    "equipped": False,
			}
		elif item_name in bobber_data:
			this_bobber = bobber_data[item_name]
			inv[f"{item_name}"] = {
				"type": this_bobber['type'],
				"rarity": this_bobber['rarity'],
				"item_name": item_name,
				"obtained_at": datenow,
				"count": 1,
			    "equipped": False,
			}
		else:
			if isinstance(item_name, Fish):
				id_gen = eight_digit_id_gen()
				if item_name.mutation == None:
					fish_name = f"{item_name.name}_{id_gen}"
				else:
					fish_name = f"{item_name.mutation}_{item_name.name}_{id_gen}"
				inv[fish_name] = {
					"species": item_name.name,
					"id": id_gen,
					"type": 'fish',
					"weight": item_name.weight,
					"mutation":item_name.mutation,
			        "count": 1,
					"price": item_name.price,
					"rarity": item_name.rarity,
					"caught_by": self._player_obj.name,
					"caught_at": datenow
				}
				

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
			player_obj.save_player()

	def search_by_id(self, search_id):
		inv = self._inventories[self._player_obj._name]["inventory"]
		for key,value in inv.items():
			if 'id' in value:
				if value['id'] == search_id:
					return key

		return None

	def query_inv_base(self, args, tosort):
		inv = self._inventories[self._player_obj._name]["inventory"]
		grouping = {}

		for key, value in inv.items():
			type_val = value['type']
			if type_val not in grouping:
				grouping[type_val] = []
			grouping[type_val].append(key)

		if args.lower() == "sortby":
			tosplit = tosort.replace(' ','').split(',')
			if tosplit[0] in grouping:
				try:
					operators = {
						'>=': lambda a, b: a >= b,
						'<=': lambda a, b: a <= b,
						'<': lambda a, b: a < b,
						'>': lambda a, b: a > b,   
						'=': lambda a, b: a == b,
						'!=': lambda a, b: a != b,
					}
					
					for op in sorted(operators.keys(), key=len, reverse=True):  
						if op in tosplit[1]:
							op_index = tosplit[1].index(op)
							based = tosplit[1][:op_index]
							sort_arg = tosplit[1][op_index+1:]
							op_func = operators[op]
							set1 = set()
							
							if len(op) > 1:
								sort_arg = tosplit[1][op_index+2:]
							for i in grouping[tosplit[0]]:
								if based == 'rarity':
									local_op = operators.copy()
									for key,value in local_op.items():
										if key == '<':
											local_op[key] = operators['>']
										elif key == '>':
											local_op[key] = operators['<']
										elif key == '>=':
											local_op[key] = operators['<=']
										elif key == '<=':
											local_op[key] = operators['>=']
									op_func = local_op[op]
									if inv[i][based] in rarity_dict and sort_arg in rarity_dict:
										if op_func(rarity_dict[inv[i][based]], rarity_dict[sort_arg]):
											set1.add(i)
									else:
										if inv[i][based] not in rarity_dict:
											print(f"item with unknown rarity: {i}")
										if sort_arg not in rarity_dict:
											print(f"Unknown rarity: {sort_arg}")
											break
								else:
									if based in inv[i]:
										item_attr = inv[i][based]
										sort_arg_num = parse_number(sort_arg)
										if sort_arg_num in ['none', 'None']:
											sort_arg_num = None
										if op_func(item_attr, sort_arg_num):
											set1.add(i)
									else:
										converted_name = inv[i]['item_name']
										if based in equippable_data[converted_name]:
											item_attr = equippable_data[converted_name][based]
											sort_arg_num = parse_number(sort_arg)
											if op_func(item_attr, sort_arg_num):
												set1.add(i)
							break
					return set1
				except IndexError:
					return grouping[tosplit[0]]

			
	def query_inv(self, args, tosort):
		tosplit = tosort.replace(' ','').split(',')
		try:
			split_cond = re.split(r'\s*(or|and|not)\s*', tosplit[1])
			split_cond = [x for x in split_cond if x]
			set1 = self.query_inv_base(args, f"{tosplit[0]},{split_cond[0]}")
			
			if set1:
				index = 1
				while index < len(split_cond) - 1:
					set2 = set()
					if split_cond[index] == 'or':
						index += 1
						if split_cond[index] == 'not':
							print('aselole')
							index += 1
						else:
							set2 = self.query_inv_base(args, f"{tosplit[0]},{split_cond[index]}")
							set1 |= set2
							index += 1
					elif split_cond[index] == 'and':
						index += 1
						if split_cond[index] == 'not':
							index += 1
							set2 = set2 = self.query_inv_base(args, f"{tosplit[0]},{split_cond[index]}")
							set1 -= set2
							print('logic untested')
						else:
							set2 = self.query_inv_base(args, f"{tosplit[0]},{split_cond[index]}")
							set1 &= set2
							index += 1
				if set1:
					return set1
				else:
					return None
			else:
				return None
		except IndexError:
			set1 = self.query_inv_base(args, tosplit[0])
			return set1

	def display_inv(self, args, tosort, compact=False):
			inv = self._inventories[self._player_obj._name]["inventory"]
			with_cons = False
			try:
				cleaned = tosort.replace(" ", "").split(',')
				print(tosort)
				logics = ['and', 'not', 'or']
				operators = ["<=", '>=', '!=', '=', '<', '>']
				split_cond = re.split(r'\s*(or|and|not)\s*', cleaned[1])
				split_cond = [x for x in split_cond if x and x not in logics]
				
				keys = set()
				for cond in split_cond:
					for op in operators:
						if op in cond:
							keys.add(cond.split(op)[0])
							break
				with_cons = True
				queried = self.query_inv(args, tosort)
		
			except IndexError:
				print('indexerr')
				queried = self.query_inv(args, tosort)
			if queried:
				print('queried')
				for i in queried:
					if compact in [True, 'true', 'yes', 'True']:
						chuubaco = f"{i}"
						print(chuubaco)

					elif compact in [False, 'false', 'no', "False"]:
						chuubaco = f"{i}"
						
						if with_cons:
							for j in keys:
								if j in inv[i]:
									chuubaco += f" {j}: {inv[i][j]}"
								else:
									if keys[0] == 'fish':
										chuubaco += f" {j}: {fish_data[inv[i]['species']][j]}"
									elif keys[0].startswith('armor_') or keys[0] == 'weapon':
										chuubaco += f" {j}: {equippable_data[inv[i]['item_name']][j]}"
							print(chuubaco)
						
						else:
							print(chuubaco)
					elif compact == 'detailed':
						print(self.item_formating(i))
								