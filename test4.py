import itertools
import math
from pyalex.chord import Chord
from pyalex.pitch import Pitch
from pyalex.polyphony import VoiceManager
from pyalex.rand import RandomizerGroup
from pyalex.utilities import Utilities, LengthMultiplier, LengthMultiplierManager
import random
import scamp
import statistics
import sys	
import threading

FUND = 0
IS_FORKING_POSSIBLE = True
                                                       
bar_lengths = itertools.cycle(	[ 3.0,    3.0,    3.0,    3.0,    3.0,    3.0,    3.0,   3.5,    4.5,    6.5,    9.5])      
macro_ratios = itertools.cycle(	[[2, 1], [2, 3], [1, 1], [2, 3], [1, 1], [2, 3], [1, 2], [1, 2], [2, 3], [2, 3], [2, 3]])
micro_ratios = itertools.cycle(	[[1, 1], [2, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [2, 1], [2, 1], [2, 1]])

s = scamp.Session(tempo = 252)
inst1 = s.new_midi_part("IAC Driver IAC Bus 1")
inst2 = s.new_midi_part("IAC Driver IAC Bus 2")
delay_incrementer = s.new_osc_part("delay_incrementer", 7800, "127.0.0.1")

a = 59.0
b = 56.5

class Note:
	def __init__(self, midi_number, fundamental):
		self.midi_number = midi_number
		self.fundamental = fundamental

def low_notes():
	global FUND, IS_FORKING_POSSIBLE
	while IS_FORKING_POSSIBLE:
		scamp.wait(2)
		if FUND.is_integer():
			inst1.play_note(FUND + 31, 1, 1)
		else:
			inst2.play_note(math.ceil(FUND + 31 + 12), 1, 1)			
		scamp.wait(1)

note_list = []
note_list.append(Note(0, 0))

p_min, p_max = 7, 11
q_min, q_max = 7, 11
i = 0
j = True

for _ in range(12):

	p = 0
	while p < random.randrange(p_min, p_max):
		# a = 8, b = 7
		note_list.append(Note(a, fundamental = a-36))
		note_list.append(Note(b, fundamental = a-36))
		p += 1
	a += 1
	i += 1

	q = 0
	while q < random.randrange(q_min, q_max):
		# b = 9, a = 11
		note_list.append(Note(a, fundamental = b-40))
		note_list.append(Note(b, fundamental = b-40))
		q += 1
	b += 1
	i += 1

	if i%2 == 0 and i>=6:
		note_list.append(Note(0, 0))
		j = True

bar_line_list = []

s.new_osc_part("master_reset", 7700, "127.0.0.1").play_note(0, 0.0, 0.01, blocking = False)

s.start_transcribing()
# s.fast_forward_in_beats(1000)

# intro
for _ in range(random.randrange(7, 11)):
	inst1.play_chord([59], length = 1, volume = 1)
	inst1.play_chord([66], length = 1, volume = 1)
	s.wait(1)
	bar_line_list.append(s.beat())

played_a = False
played_b = False

for n in note_list:
	if n.midi_number == 0:
		bar_length = next(bar_lengths)
		macro_ratio = next(macro_ratios)
		micro_ratio = next(micro_ratios)
		txt = str(bar_length) + ", " + str(macro_ratio[0]) + ":" + str(macro_ratio[1]) + ", " + str(micro_ratio[0]) + ":" + str(micro_ratio[1])
		delay_incrementer.play_note(0, 0.0, 0.01, blocking = False, properties = scamp.StaffText(txt))
		print("---------------------------------------------------")
		print(str(bar_length))
		print(str(macro_ratio))
		print(str(micro_ratio))
		# if bar_length == 5.5:
		# 	s.fork(low_notes)
	else:
		if n.midi_number.is_integer():
			FUND = n.fundamental
			inst1.play_chord([n.midi_number, n.midi_number+3], length = bar_length*(macro_ratio[0]/(macro_ratio[0]+macro_ratio[1]))*(micro_ratio[0]/(micro_ratio[0]+micro_ratio[1])), volume = 1)
			inst1.play_chord([n.midi_number+4, n.midi_number+7], length = bar_length*(macro_ratio[0]/(macro_ratio[0]+macro_ratio[1]))*(micro_ratio[1]/(micro_ratio[0]+micro_ratio[1])), volume = 1)
			played_a = True
		else:
			FUND = n.fundamental
			inst2.play_chord([math.ceil(n.midi_number+7)], length = bar_length*(macro_ratio[1]/(macro_ratio[0]+macro_ratio[1]))*(micro_ratio[0]/(micro_ratio[0]+micro_ratio[1])), volume = 1)
			inst2.play_chord([math.ceil(n.midi_number)], length = bar_length*(macro_ratio[1]/(macro_ratio[0]+macro_ratio[1]))*(micro_ratio[1]/(micro_ratio[0]+micro_ratio[1])), volume = 1)
			played_b = True
		if played_a and played_b:
			bar_line_list.append(s.beat())
			played_a = False
			played_b = False

IS_FORKING_POSSIBLE = False

inst1.play_chord([24, 36, 48], length = 7.5, volume = 1)
inst1.play_chord([55], length = 7.5, volume = 1)
inst1.play_chord([64, 76, 88], length = 13, volume = 1)
inst2.play_chord([58], length = 39, volume = 1)

score = s.stop_transcribing().to_score(bar_line_locations = bar_line_list, max_divisor = 5)
score.show()

