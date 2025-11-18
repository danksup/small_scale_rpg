import json
import ast

items_attr = {
	'fish': ["species", "weight_min", "weight_max", "base_price", "sellable", "rarity"],
	'mutation': [],
	'fishing_rod': [],
	'equippable': [],
	'bobber': [],
	'items': [],
	'test': ['ayam', 'bau', 'goreng'],
}
def push():
	category = input("category: ")
	if category in items_attr.keys():
		try:
			with open(f"{category}.json", "r") as f:
				data = json.load(f)
		except FileNotFoundError:
			data = {}

		temp = {}
		key_name = input("key name: ")
		key_name = key_name.strip().replace(" ", "_").lower()
		if key_name in data:
			print('already exists. pls update instead')
		else:
			for value in items_attr[category]:
				val_inp = input(f"add value for {value}: ")
				if val_inp.strip() == "":
					continue
				try:
					val_inp = ast.literal_eval(val_inp)
				except (ValueError, SyntaxError):
					print("error, treating input as string")
					val_inp = val_inp

				temp[value] = val_inp

			data[key_name] = temp
			confirm_text = f'you are about to add "{key_name}" into "{category}" with values:\n'
			for k, v in temp.items():
				confirm_text += f"  {k}: {v}\n"
			confirm_text += "continue? (y/n) "
			confirm_add = input(confirm_text)
			if confirm_add in ['y', 'yes']:
				with open(f"{category}.json", "w") as f:
					json.dump(data,f, indent=4)
			else:
				print('cancelled adding')
			
def update():
	category = input("category: ")
	if category not in items_attr:
		print("invalid category")
		return
	
	try:
		with open(f"{category}.json", "r") as f:
			data = json.load(f)
	except FileNotFoundError:
		print("no data file found for this category")
		return

	new_attr = input("attribute to add: ").strip()
	if not new_attr:
		print("attribute name cannot be empty")
		return

	print(f'adding attribute "{new_attr}" to {len(data)} keys:')
	for key in data:
		print("  -", key)

	val_inp = input(f'value for "{new_attr}" (same for all): ')
	try:
		val_inp = ast.literal_eval(val_inp)
	except (ValueError, SyntaxError):
		print("error, treating as string")
	
	confirm = input("continue? (y/n) ")
	if confirm not in ["y", "yes"]:
		print("cancelled")
		return

	for key in data:
		data[key][new_attr] = val_inp

	with open(f"{category}.json", "w") as f:
		json.dump(data, f, indent=4)

	print(f'added attribute "{new_attr}" to all existing keys in "{category}"')
