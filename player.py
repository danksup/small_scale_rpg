from equippable import Equippable
from inventory import Inventory
from gacha import gacha_base
from fish import Fish
import time
import random
import json

with open("items.json", "r") as f:
	items_data = json.load(f)
with open("fish.json", "r") as f:
	fish_data = json.load(f)
with open("equippable.json", "r") as f:
	equippable_data = json.load(f)
with open("players.json", "r") as f:
	player_data = json.load(f)
with open("inventory.json", "r") as f:
	inv_data = json.load(f)
with open("fishing_rod.json", "r") as f:
	rod_data = json.load(f)
with open("bobber.json", "r") as f:
	bobber_data = json.load(f)
player_stat_list = ['critrate', 'critdmg', 'health', 'defense', 'atk', 'general_luck', 'fishing_luck']

class Player:
	def __init__(self, name):
		self._weapon = None
		self._armor_helmet = None
		self._armor_chestplate = None
		self._armor_leggings = None
		self._armor_boots = None
		self._fishing_rod = None
		self._fishing_bobber = None
		self._inventory = None

		self.name = name  
		if self.name in player_data:
			for key,value in player_data[self.name].items():
				if key != "equipment" and key != "inventory" and key != 'luck':
					setattr(self,key, value)
				elif key == "inventory":
					setattr(self,key, Inventory(self))
				elif key == 'luck':
					for luck_key, luck_value in value.items():
						if luck_value is not None:
							setattr(self, luck_key, luck_value)
				elif key == "equipment":
					for equipment_key, equipment_value in value.items():
						if equipment_value is not None:
							setattr(self, equipment_key, Equippable(equipment_value))
		else:
			print("create first")

	def to_dict(self):
		return {
			"name": self.name,
			"health": self.health,
			"defense": self.defense,
			"exp": self.exp,
			"level": self.level,
			"coins": self.coins,
			"luck":{
				"general_luck":self.general_luck,
				"fishing_luck":self.fishing_luck,
			},
            "diamond": self.diamond,
			"atk": self.atk,
			"critrate": self.critrate,
			"critdmg": self.critdmg,
			"equipment": {
				"weapon": self.weapon.name if self.weapon else None,
				"armor_helmet": self.armor_helmet.name if self.armor_helmet else None,
				"armor_chestplate": self.armor_chestplate.name if self.armor_chestplate else None,
				"armor_leggings": self.armor_leggings.name if self.armor_leggings else None,
				"armor_boots": self.armor_boots.name if self.armor_boots else None,
				"fishing_rod": self.fishing_rod.name if self.fishing_rod else None,
				"fishing_bobber": self.fishing_bobber.name if self.fishing_bobber else None,
			},
			"inventory": self.inventory.get_items()
		}
	
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
			"luck":{
				"general_luck":0,
				"fishing_luck":0,
			},
            "coins": 0,
            "diamond": 0,
			"critrate": 0,
			"critdmg": 0,
			"defense": 0,
            "equipment": {
                "weapon": None,
                "armor_helmet": None,
                "armor_chestplate": None,
                "armor_leggings": None,
                "armor_boots": None,
                "fishing_rod": None,
				"fishing_bobber": None
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

		counting = {}
		for key,value in self.inventory.get_items().items():
			if value['type'] not in counting:
				counting[value['type']] = 1
			else:
				counting[value['type']] += 1

		return (
        f"=== PLAYER STATUS ===\n"
        f"Name          : {self.name}\n\n"
        f"--- Stats ---\n"
        f"Health        : {int(self.health)}\n"
        f"Defense       : {self.defense}\n"
        f"Attack        : {self.atk}\n"
        f"Luck\n"
		f"  general luck: {self.general_luck}\n"
		f"  fishing luck: {self.fishing_luck}\n"
        f"Level         : {self.level}\n"
        f"Experience    : {self.exp}\n"
        f"Coins         : {self.coins}\n\n"
        f"--- Critical ---\n"
        f"Crit Rate     : {self.critrate}\n"
        f"Crit Damage   : {self.critdmg}\n\n"
        f"--- Equipment ---\n"
        f"Weapon        : {weapon_info}\n"
        f"Helmet        : {self.armor_helmet.name if self.armor_helmet else 'None'}\n"
        f"Chestplate    : {self.armor_chestplate.name if self.armor_chestplate else 'None'}\n"
        f"Leggings      : {self.armor_leggings.name if self.armor_leggings else 'None'}\n"
        f"Boots         : {self.armor_boots.name if self.armor_boots else 'None'}\n"
        f"Fishing Rod   : {self.fishing_rod.name if self.fishing_rod else 'None'}\n"
        f"  Fishing bobber   : {self.fishing_bobber.name if self.fishing_bobber else 'None'}\n\n"
        f"--- Inventory ---\n"
        f"{counting}"
    )
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
	def fishing_rod(self):
		return self._fishing_rod
	@fishing_rod.setter
	def fishing_rod(self, fishing_rod):
		self._fishing_rod = fishing_rod
	
	@property
	def fishing_bobber(self):
		return self._fishing_bobber
	@fishing_bobber.setter
	def fishing_bobber(self, fishing_bobber):
		self._fishing_bobber = fishing_bobber
	
	@property
	def inventory(self):
		return self._inventory
	@inventory.setter
	def inventory(self, inventory):
		self._inventory = inventory

	@property
	def general_luck(self):
		return self._general_luck
	@general_luck.setter
	def general_luck(self, general_luck):
		self._general_luck = general_luck
	
	@property
	def fishing_luck(self):
		return self._fishing_luck
	@fishing_luck.setter
	def fishing_luck(self, fishing_luck):
		self._fishing_luck = fishing_luck
	
	@property
	def diamond(self):
		return self._diamond
	@diamond.setter
	def diamond(self, diamond):
		self._diamond = diamond

	def save_player(self):
		try:
			with open("players.json", "r") as f:
				all_players = json.load(f)
		except (FileNotFoundError, json.JSONDecodeError):
			all_players = {}

		all_players[self.name] = self.to_dict()

		with open("players.json", "w") as f:
			json.dump(all_players, f, indent=4)

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
			"fishing_rod" : self.fishing_rod,
			"fishing_bobber" : self.fishing_bobber,
		}
		
		base = target_dict[target]

		if getattr(self, target):
			if target != 'fishing_rod' and target != 'fishing_bobber':
				keys = equippable_data[base.name[:-9]]
			else:
				if target == 'fishing_rod':
					keys = rod_data[self.fishing_rod.name]
				elif target == 'fishing_bobber':
					keys = bobber_data[self.fishing_bobber.name]

			for key in keys:
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
			keys = equippable_data[inv[check_exist]['item_name']]
			setattr(self, weapon_type, Equippable(check_exist))
		else:
			check_exist = equip_id
			if equip_id in rod_data:
				if getattr(self, 'fishing_rod'):
					self.deequip('fishing_rod')
					self._inventory.get_items()[equip_id]['equipped'] =  False
			
				keys = rod_data[equip_id]
				setwhat = 'fishing_rod'
			elif equip_id in bobber_data:
				if getattr(self, 'fishing_bobber'):
					self.deequip('fishing_bobber')
					self._inventory.get_items()[equip_id]['equipped'] =  False
			
				keys = bobber_data[equip_id]
				setwhat = 'fishing_bobber'
			setattr(self, setwhat, Equippable(equip_id))

		for key in keys:
			if key in player_stat_list:
				self_stat = getattr(self,key)
				equipped_item = getattr(self, 'fishing_rod')
				equipped_stat = getattr(equipped_item, key)
				setattr(self, key, self_stat + equipped_stat)

		self._inventory.get_items()[check_exist]['equipped'] =  True
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
		
		self.save_player()
	
	def base_sell(self, item_name, count= 1):
		inv = self.inventory.get_items()
		if item_name in inv:
			item_type = inv[item_name]['type']

			if item_type == 'fish':
				sellable = fish_data[inv[item_name]['species']]['sellable']
				if 'coin' in sellable:
					fish_price = inv[item_name]['price']
					self.coins += fish_price
					self.inventory.remove_item(item_name)
					print(f"sold {item_name} for {fish_price}")
			elif item_type == 'weapon' or item_type.startswith('armor_'):
				sellable = fish_data[inv[item_name]['item_name']]['sellable']
				if 'coin' in sellable:
					equ_price = equippable_data[inv[item_name]['item_name']]['price']
					self.coins += equ_price
					self.inventory.remove_item(item_name)
					print(f"sold {item_name} for {equ_price}")
			else:
				item_count = inv[item_name]['count']
				sellable = items_data[item_name]['sellable']
				if 'coin' in sellable:
					if count <= item_count:
						item_price = items_data[item_name]['price']
						self.coins += item_price * count
						self.inventory.remove_item(item_name, count)
						print(f"sold {count} {item_name} for {item_price*count}")
					else:
						print('cant')


	def sell(self, args, count=1):
		try:
			clean_args = args.replace(' ','').split(',')
			to_sell = clean_args[0]
			where = clean_args[1]
			a = self.inventory.query_inv('sortby', f"{to_sell},{where}")
			if a is not None:
				confirm = input(f"you're about to sell {a}\ncontinue: ")
				if confirm in ['y', 'yes']:
					for i in a:
						self.base_sell(i)
				else:
						print('canceled')
		except IndexError:
			a = self.inventory.query_inv('sortby', f"{to_sell}")
			if a is not None:
				confirm = input(f"you're about to sell {a}\ncontinue: ")
				if confirm in ['y', 'yes']:
					for i in a:
						self.base_sell(i)
				else:
						print('canceled')
			else:
				sell_equi = self.inventory.search_by_id(args) if  self.inventory.search_by_id(args) is not None else None
				if sell_equi is not None:
					confirm = input(f"you're about to sell {sell_equi}\ncontinue: ")
					if confirm in ['y', 'yes']:
						self.base_sell(sell_equi)
					else:
						print('canceled')
				else:
					confirm = input(f"you're about to sell {count} {args}\ncontinue: ")
					if confirm in ['y', 'yes']:
						self.base_sell(args, count)
					else:
						print('canceled')
		
		self.save_player()

	def gacha(self, occurence=10): 
		luck_increase = self.general_luck
		gacha_one_pull_price = 50
		reduction = 0

		if "gacha_ticket" in self.inventory:
			ticket_count = self.inventory['gacha_ticket']['count']
			if ticket_count  < occurence:
				reduction = gacha_one_pull_price * ticket_count
				self.inventory.remove_item("gacha_ticket", ticket_count)

			elif ticket_count >= occurence:
				reduction = occurence*gacha_one_pull_price
				self.inventory.remove_item("gacha_ticket", occurence)
		

		tot_dia = (gacha_one_pull_price * occurence) - reduction

		if self.diamond >= tot_dia:
			items_gacha = gacha_base(occurence, luck_increase)

			for i in items_gacha:
				self._inventory.add_item(i)
			
			self.diamond -= tot_dia
			self.save_player()
			print(f"you got {items_gacha}")
		else:
			print('diamond not enough')

	def fish(self):
		if self.fishing_rod and self.fishing_bobber:
			rod = self.fishing_rod
			general_luck = self.general_luck
			fishing_luck = self.fishing_luck
			total_luck = general_luck + fishing_luck

			base_bite_time = 8  
			fishing_speed = rod.fishing_speed 
			bite_time = base_bite_time / fishing_speed
			bite_time *= random.uniform(0.8, 1.2)  # slight randomization
			print(f"Waiting for a fish to bite... (~{bite_time:.2f}s)")
			time.sleep(bite_time)

			base_reel_time = 5 
			reeling_speed = rod.reeling_speed
			reel_time = base_reel_time / reeling_speed
			reel_time *= random.uniform(0.9, 1.1)  
			print(f"Reeling in... (~{reel_time:.2f}s)")
			time.sleep(reel_time)

			fish_caught = Fish.fish_base(total_luck)
			print(f"you caught {fish_caught.name}")
			self._inventory.add_item(fish_caught)

		else:
			print('fishing equipment not fully equipped')