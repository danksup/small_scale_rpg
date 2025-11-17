import json

with open("equippable.json", "r") as f:
	equippable_data = json.load(f)
with open("fishing_rod.json", "r") as f:
	rod_data = json.load(f)
with open("bobber.json", "r") as f:
	bobber_data = json.load(f)

class Equippable:
	def __init__(self,name):
		self._name = name
		selfnameneg9 = self._name[:-9]
		if selfnameneg9 in equippable_data and  selfnameneg9 not in rod_data:
			for key in equippable_data[selfnameneg9]:
				setattr(self, key, equippable_data[selfnameneg9][key])
		else:
			if name in rod_data:
				for key in rod_data[name]:
					setattr(self, key, rod_data[name][key])
			elif name in bobber_data:
				for key in bobber_data[name]:
					setattr(self, key, bobber_data[name][key])

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, name):
		self._name = name

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
	def durability(self):
		return self._durability
	@durability.setter
	def durability(self, durability):
		self._durability = durability

	@property
	def defense(self):
		return self._defense
	@defense.setter
	def defense(self, defense):
		self._defense = defense

	@property
	def health(self):
		return self._health
	@health.setter
	def health(self, health):
		self._health = health

	@property
	def fishing_speed(self):
		return self._fishing_speed
	@fishing_speed.setter
	def fishing_speed(self,fishing_speed):
		self._fishing_speed = fishing_speed
	
	@property
	def reeling_speed(self):
		return self._reeling_speed
	@reeling_speed.setter
	def reeling_speed(self,reeling_speed):
		self._reeling_speed = reeling_speed