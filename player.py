from equippable import Equippable
from inventory import Inventory
from gacha import gacha_base
from fish import Fish
import random
import json

with open("items.json", "r") as f:
	items_data = json.load(f)
with open("equippable.json", "r") as f:
	equippable_data = json.load(f)
with open("players.json", "r") as f:
	player_data = json.load(f)
player_stat_list = ['critrate', 'critdmg', 'health', 'defense', 'atk']

class Player:
	def __init__(self, name):
		self._health = None
		self._weapon = None
		self._armor_helmet = None
		self._armor_chestplate = None
		self._armor_leggings = None
		self._armor_boots = None
		self._inventory = None

		self.name = name  
		if self.name in player_data:
			for key,value in player_data[self.name].items():
				if key != "equipment" and key != "inventory":
					setattr(self,key, value)
				elif key == "inventory":
					setattr(self,key, Inventory(self))
				elif key == "equipment":
					for equipment_key, equipment_value in value.items():
						if equipment_value is not None:
							setattr(self, equipment_key, Equippable(equipment_value))
		else:
			self.create_player(name)
	
	@classmethod
	def create_player(cls, name):
		all_player = player_data
		if name not in player_data:
			data = {
            "health": 100,
            "defense": 10,
            "atk": 20,
            "level": 1,
            "exp": 0,
			"luck":0,
            "coins": 0,
			"critrate": 0,
			"critdmg": 0,
			"defense": 0,
            "equipment": {
                "weapon": None,
                "armor_helmet": None,
                "armor_chestplate": None,
                "armor_leggings": None,
                "armor_boots": None
            },
			"inventory": {}
        }
			all_player[name] = data
			with open("players.json", "w") as f:
				json.dump(all_player, f, indent=4)
		return cls(name)
			

	def __str__(self):
		if self.weapon is not None:
			weapon_info = self.weapon.name
		else:
			weapon_info = None
		return f"name: {self.name}\nhealth: {int(self.health)}\ndefense: {self.defense}\natk: {self.atk}\nlevel: {self.level}\nexp: {self.exp}\ncoins: {self.coins}\ncrit rate: {self.critrate}\ncritdmg: {self.critdmg}\nweapon: {weapon_info}\nhelmet armor: {self.armor_helmet}\nchestplate armor: {self.armor_chestplate}\nlegging armor: {self.armor_leggings}\nboot armor: {self.armor_boots}\ninventory: {self._inventory._inventories[self.name]['inventory']}"

	# getters and setters
	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, name):
		self._name = name

	@property
	def health(self):
		return self._health
	@health.setter
	def health(self, health):
		if health < 0:
			self._health = 0
		else:
			self._health = health

	@property
	def exp(self):
		return self._exp
	@exp.setter
	def exp(self, exp):
		self._exp = exp

	@property
	def level(self):
		return self._level
	@level.setter
	def level(self, level):
		self._level = level

	@property
	def coins(self):
		return self._coins
	@coins.setter
	def coins(self, coins):
		if coins <= 0:
			self._coins = 0
		else:
			self._coins = coins

	@property
	def atk(self):
		return self._atk
	@atk.setter
	def atk(self, atk):
		self._atk = atk

	@property
	def critdmg(self):
		return self._critdmg
	@critdmg.setter
	def critdmg(self, critdmg):
		self._critdmg = critdmg

	@property
	def critrate(self):
		return self._critrate
	@critrate.setter
	def critrate(self, critrate):
		self._critrate = critrate

	@property
	def weapon(self):
		return self._weapon
	@weapon.setter
	def weapon(self, weapon):
		self._weapon = weapon

	@property
	def defense(self):
		return self._defense
	@defense.setter
	def defense(self, defense):
		self._defense = defense

	@property
	def armor_helmet(self):
		return self._armor_helmet
	@armor_helmet.setter
	def armor_helmet(self, armor_helmet):
		self._armor_helmet = armor_helmet

	@property
	def armor_chestplate(self):
		return self._armor_chestplate
	@armor_chestplate.setter
	def armor_chestplate(self, armor_chestplate):
		self._armor_chestplate = armor_chestplate

	@property
	def armor_leggings(self):
		return self._armor_leggings
	@armor_leggings.setter
	def armor_leggings(self, armor_leggings):
		self._armor_leggings = armor_leggings

	@property
	def armor_boots(self):
		return self._armor_boots
	@armor_boots.setter
	def armor_boots(self, armor_boots):
		self._armor_boots = armor_boots
	
	@property
	def inventory(self):
		return self._inventory
	@inventory.setter
	def inventory(self, inventory):
		self._inventory = inventory

	@property
	def luck(self):
		return self._luck
	@luck.setter
	def luck(self, luck):
		self._luck = luck

	def to_dict(self):
		return {
			"name": self.name,
			"health": self.health,
			"defense": self.defense,
			"exp": self.exp,
			"level": self.level,
			"coins": self.coins,
			"atk": self.atk,
			"critrate": self.critrate,
			"critdmg": self.critdmg,
			"equipment": {
				"weapon": self.weapon.name if self.weapon else None,
				"armor_helmet": self.armor_helmet.name if self.armor_helmet else None,
				"armor_chestplate": self.armor_chestplate.name if self.armor_chestplate else None,
				"armor_leggings": self.armor_leggings.name if self.armor_leggings else None,
				"armor_boots": self.armor_boots.name if self.armor_boots else None,
			},
			"inventory": self.inventory.get_items()
		}

	def save_player(self):
		try:
			with open("players.json", "r") as f:
				all_players = json.load(f)
		except (FileNotFoundError, json.JSONDecodeError):
			all_players = {}

		all_players[self.name] = self.to_dict()

		with open("players.json", "w") as f:
			json.dump(all_players, f, indent=4)
		print(f"Player '{self.name}' data saved successfully!")

	#modifier
	def hurt(self, damage):
		self.health -= damage
		self.save_player()

	def heal(self, healed):
		self.health += healed
		self.save_player()

	def attack(self, other):
		dealt = self.atk

		is_crit = random.random()
		if is_crit < self.critrate / 100:
			dealt *= int((1 + self.critdmg / 100))

		if other.defense <= 20:
			damage_reduction = other.defense 
		else:
			damage_reduction = 20 + (other.defense - 20) * (20 / ((other.defense - 20) + 20))

		final_damage = dealt * (1 - (damage_reduction / 100))
		other.health -= final_damage

		if self.weapon is not None:
			self._inventory[self.weapon.name]['durability'] -= 1
			self._inventory.save()
			if self._inventory[self.weapon.name]['durability'] <= 0:
				equiped_weapon_name = self.weapon.name
				self.deequip("weapon")
				self._inventory.remove_item(equiped_weapon_name)
		print(f"{self.name} to {other.name}/dealt {dealt}/{'crit' if is_crit < self.critrate/100 else 'not crit'}/actual damage = {final_damage}(damage reduction: {damage_reduction}%)")

		self.save_player()

	def deequip(self, target):
		
		target_dict = {
			"weapon" : self.weapon,
			"armor_helmet" : self.armor_helmet,
			"armor_chestplate" : self.armor_chestplate,
			"armor_leggings" : self.armor_leggings,
			"armor_boots" : self.armor_boots,
		}
		
		base = target_dict[target]

		if getattr(self, target):
			for key in equippable_data[base.name[:-9]]:
				if key in player_stat_list:
					self_stat = getattr(self, key)
					target_stat = getattr(base, key)
					setattr(self, key, self_stat - target_stat)
			self._inventory.get_items()[target_dict[target].name]['equipped'] =  False

		setattr(self, target, None)

		self._inventory.save()
		self.save_player()

	def equip(self, equip_id):
		inv = self._inventory.get_items()
		check_exist = self._inventory.search_by_id(equip_id)
		if check_exist is not None:
			weapon_type = inv[check_exist]['type']

			if getattr(self, weapon_type):
				self.deequip(weapon_type)
				self._inventory.get_items()[check_exist]['equipped'] =  False
			
			setattr(self, weapon_type, Equippable(check_exist))

			for key in equippable_data[inv[check_exist]['item_name']]:
				if key in player_stat_list:
					self_stat = getattr(self,key)
					equipped_item = getattr(self, weapon_type)
					equipped_stat = getattr(equipped_item, key)
					setattr(self, key, self_stat + equipped_stat)

			self._inventory.get_items()[check_exist]['equipped'] =  True

			# print('FOR TESTING [since player object is not saved, while inventory is in a json file, inventory is automatically displayed and equippable is deequipped automatically. remember to delete this if player object saving feature is implemented]')
			# print(self._inventory)
			# self.deequip(weapon_type)
			
			self._inventory.save()
			self.save_player()

		#todo handle both equippable and reg items (done) comment: not needed, equippable only obtained from gacha
	def buy(self, item_name, count=1):

		if item_name in items_data:
			item = items_data[item_name]
			player_coin = self.coins
			item_tot_price = item['price'] * count

			if 'coin' in item['buyable_with']:
				if item_tot_price <= player_coin:
					print(item_tot_price)
					self.coins -= item_tot_price
					self._inventory.add_item(item_name, count)
				else:
					print("insufficient coins")
			else:
				print("item not buyable")
		elif item_name in equippable_data:
			print("cant buy this item")
		else:
			print("item does not exist")

	def gacha(self, occurence): 
		luck_increase = self.luck
		items_gacha = gacha_base(occurence, luck_increase)

		for i in items_gacha:
			self._inventory.add_item(i)

		self.save_player()
		print(f"you got {items_gacha}")


	def fish(self):
		luck_increase = self.luck
		self._inventory.add_item(Fish.fish_base(luck_increase))