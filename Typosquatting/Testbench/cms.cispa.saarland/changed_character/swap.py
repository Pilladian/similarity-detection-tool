# Python 3.8

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


def _swap(code_line, swap_phrase):
    swapped_line = ""
    _start = code_line.find(swap_phrase)
    _end = _start + len(swap_phrase)

    replacement = code_line[_start:_end]
    swapped_line += code_line[:_start]

    for a in replacement:
        if a == 'n':
            swapped_line += char_swap[a][1]
        elif a == 'a':
            swapped_line += char_swap[a][0]
        elif a == 'u':
            swapped_line += char_swap[a][0]
        else:
            swapped_line += a

    swapped_line += code_line[_end:]
    return swapped_line


with open('original_index.html', 'r') as f, open('swapped.html', 'w') as sw:
    new = ""
    phrases = ['Please register for this course if you intend to do the CyberSecurity Project (9CP) this winter term.',
               'CySec Project Winter Term 20/21',
               'Slides online and your next steps',
               'Please follow this procedure:',
               'Zoom details for kick-off event tomorrow',
               'Registration in LSF',
               'Datenschutz',
               'Impressum',
               'Bei technischen Problemen wenden Sie sich bitte an die Administratoren']
    read_content = f.readlines()

    for line in read_content:
        _line = line
        for phrase in phrases:
            if phrase in _line:
                _line = _swap(_line, phrase)
        new += _line

    sw.write(new)
