import random


# 8-char id generator
def eight_digit_id_gen():
	alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	num = '1234567890'

	gen_id = ''

	while len(gen_id) < 8:
		num_or_alpha = random.randrange(0,2)
		digit_picker = random.randrange(0,10)
		alpha_picker = random.randrange(0,26)
		if num_or_alpha == 0:
			gen_id += alphabet[alpha_picker]
		else:
			gen_id += num[digit_picker]

	return gen_id
###################################################################

