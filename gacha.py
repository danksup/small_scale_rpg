import json
import random

with open("equippable.json", "r") as f:
	equippable_data = json.load(f)

rarity_dict = {
	"common":800000,
	"uncommon":100000,
	"rare": 50000,
	"epic": 35000,
	"legend":10000,
	"mythic": 4450,
	"secret": 550
}

weight_total = sum(rarity_dict.values())

items_within_rarity = {}  
for key, value in equippable_data.items():
	if value['gacha'] == True:
		rarity = value['rarity']
		if rarity not in items_within_rarity:
			items_within_rarity[rarity] = []
		items_within_rarity[rarity].append(key)


def gacha_base(occurence, luck = 0):
    local_rarity_dict = rarity_dict.copy()
    for key,value in local_rarity_dict.items():
          if key in ['mythic', 'secret']:
                local_rarity_dict[key] = value + (value* (luck/100))
    weight_total_adjusted = int(sum(local_rarity_dict.values()))
    
    res = []

    for _ in range(occurence):
        cum = 0
        number_roll = random.randrange(0, weight_total_adjusted + 1)
        for key, value in local_rarity_dict.items():
            cum += value
            if number_roll <= cum:
                selected_rarity = key
                break

        if selected_rarity not in items_within_rarity or not items_within_rarity[selected_rarity]:
            continue

        chosen = random.choice(items_within_rarity[selected_rarity])
        res.append(chosen)
    
    return res

