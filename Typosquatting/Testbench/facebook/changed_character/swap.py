# Python 3.8

import random

char_swap = {}

char_swap['a'] = ['ɑ', 'α']
char_swap['b'] = ['Ꮟ', 'b']
char_swap['c'] = ['ｃ']
char_swap['d'] = ['ᑯ', 'Ꮷ']
char_swap['e'] = ['ｅ']
char_swap['f'] = ['ｆ', 'ſ', ]
char_swap['g'] = ['ƍ', 'ｇ', 'ᶃ']
char_swap['h'] = ['ｈ']
char_swap['i'] = ['ɩ']
char_swap['j'] = ['ｊ']
char_swap['k'] = ['к']
char_swap['l'] = ['｜', 'I']
char_swap['m'] = ['м', 'ʍ']
char_swap['n'] = ['п', 'ո']
char_swap['o'] = ['൦', 'ס']
char_swap['p'] = ['ρ']
char_swap['q'] = ['գ', 'զ']
char_swap['r'] = ['ｒ']
char_swap['s'] = ['ƽ', 'ｓ']
char_swap['t'] = ['ᴛ', 'τ']
char_swap['u'] = ['ᴜ']
char_swap['v'] = ['ѵ']
char_swap['w'] = ['ɯ', 'ѡ']
char_swap['x'] = ['᙮']
char_swap['y'] = ['ʏ']
char_swap['z'] = ['ｚ']

with open('original_index.html', 'r') as f:
	new = ""
	lines = f.readlines()
	
	for line in lines[:-1]:
		for char in line:
			try:
				ind = random.randint(0, len(char_swap[char]))
				new += char_swap[char][ind]
			except:
				new += char
		new += "\n"
	
	with open('swapped.html', 'w') as sw:
		sw.write(new)


