import json
import random

with open("fish.json", "r") as f:
	fish_data = json.load(f)
with open("mutation.json", "r") as f:
	mutation_data = json.load(f)

all_mutations = []
for key in mutation_data:
	all_mutations.append(key)

rarity_dict = {
	"common":800000,
	"uncommon":100000,
	"rare": 50000,
	"epic": 35000,
	"legend":10000,
	"mythic": 4450,
	"secret": 550
}

fish_within_rarity = {}  
for key, value in fish_data.items():
	rarity = value['rarity']
	if rarity not in fish_within_rarity:
		fish_within_rarity[rarity] = []
	fish_within_rarity[rarity].append(key)

class Fish:
	def __init__(self, name ):
		self.name = name
		self.species = fish_data[name]['species']
		self.weight_min = fish_data[name]['weight_min']
		self.weight_max = fish_data[name]['weight_max']
		self.base_price =  fish_data[name]['base_price']
		self.rarity = fish_data[name]['rarity']

	@property
	def species(self):
		return self._species
	@species.setter
	def species(self, species):
		self._species =species

	@property
	def weight_min(self):
		return self._weight_min
	@weight_min.setter
	def weight_min(self, weight_min):
		self._weight_min = weight_min

	@property
	def weight_max(self):
		return self._weight_max
	@weight_max.setter
	def weight_max(self, weight_max):
		self._weight_max = weight_max

	@property
	def base_price(self):
		return self._base_price
	@base_price.setter
	def base_price(self, base_price):
		self._base_price = base_price

	@property
	def rarity(self):
		return self._rarity
	@rarity.setter
	def rarity(self, rarity):
		self._rarity = rarity

	@classmethod
	def fish_base(cls, luck=0):
		local_rarity_dict = rarity_dict.copy()
		for key, value in local_rarity_dict.items():
			if key in ['mythic', 'secret']:
				local_rarity_dict[key] = value + (value * (luck / 100))
		weight_total_adjusted = int(sum(local_rarity_dict.values()))

		def roll_rarity():
			cum = 0
			number_roll = random.randrange(0, weight_total_adjusted + 1)
			for key, value in local_rarity_dict.items():
				cum += value
				if number_roll <= cum:
					return key

		selected_rarity = roll_rarity()
		while selected_rarity not in fish_within_rarity:
			selected_rarity = roll_rarity()

		
		chosen = random.choice(fish_within_rarity[selected_rarity])

		fish_obj = cls(chosen)
		fish_weight_min = fish_obj.weight_min
		fish_weight_max = fish_obj.weight_max
		fish_base_price = fish_obj.base_price

		fish_weight = random.uniform(fish_weight_min, fish_weight_max)
		fish_price = round(fish_base_price * ((fish_weight / fish_weight_min) ** 2))

		mutated_chance = 8
		mutated_roller = random.randrange(0,11)
		if mutated_roller >= mutated_chance:
			chosen_mutation = random.choice(all_mutations)
	
			if chosen_mutation == "golden":
				fish_price *= (mutation_data['golden']['coin_mul']/100)
			elif chosen_mutation == "big": #mutation big will make the fish to be its maximum size
				big_mutation = mutation_data['big']
				weight_mul =  random.uniform(big_mutation['min_size_mul'], big_mutation['max_size_mul'])
				fish_weight = fish_weight_max *( weight_mul/100)
		else:
			chosen_mutation = None
	
		return CaughtFish(Fish(chosen), fish_weight, fish_price, chosen_mutation)

class CaughtFish(Fish):
	def __init__(self,base_fish: Fish, weight,price,mutation):
		super().__init__(base_fish.name)
		self.weight = weight
		self.price = price
		self.mutation = mutation



