import json

with open("equippable.json", "r") as f:
	equippable_data = json.load(f)

class Equippable:
	def __init__(self,name):
		self._name = name
		selfnameneg9 = self._name[:-9]
		for key in equippable_data[selfnameneg9]:
			setattr(self, key, equippable_data[selfnameneg9][key])

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