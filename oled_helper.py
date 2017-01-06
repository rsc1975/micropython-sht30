
grade = '''
···oo···
··o··o··
oo····oo
··o··o··
···oo···
········
········
········
'''

accent = '''
·····ooo
····oo··
···o····
········
········
········
········
········
'''


enne = '''
··ooo··o
·o···oo·
········
········
········
········
········
········
'''

grade = bytes([1 if g == 'o' else 0 for g in grade])
accent = bytes([1 if g == 'o' els e 0 for g in accent])
enne = bytes([1 if g == 'o' else 0 for g in enne])

special_chars = [
	('á', 'a', accent),
	('é', 'e', accent),
	('í', 'i', accent),
	('ó', 'o', accent),
	('ú', 'u', accent),
	('ñ', 'n', enne),
	('º', ' ', grade),
]
all_chars = ''.join(c[0] for c in special_chars)

def replace(txt):
	new_txt = ''
	for c in txt:
		if c in all_chars:
			new_txt += replace_char(c)
		else:
			new_txt += c
	return new_txt
	
def replace_char(char):
	for chars in special_chars.keys():
		if char in chars:


def text(display, txt, top_px=0, left_px=0):
				
	display.fill(0)
	display.text(txt,top_px, left_px)
	display.show()

'''
from machine import I2C, Pin
import time
i2c = I2C(scl=Pin(5), sda=Pin(4))
try: 
    i2c.start(); 
    i2c.writeto(0x45, b'\x2C\x10');
    time.sleep_ms(100)
    data = i2c.readfrom(0x45, 6)
    print(data)
except OSError as ex: 
    print(ex, ex.args)
i2c.stop(); 

from sht30 import SHT30
s = SHT30()
s.measure(); s.measure_int()

'''