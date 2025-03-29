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

bar_lengths = itertools.cycle(	[ 3,      3,      3,     3,      3,      3,      3])
macro_ratios = itertools.cycle(	[[2, 1], [3, 1], [3, 2], [3, 1], [1, 2], [1, 2], [1, 1]])
micro_ratios = itertools.cycle(	[[1, 1], [2, 1], [2, 1], [1, 1], [1, 1], [3, 1], [3, 1]])

s = scamp.Session(tempo = 270)
inst1 = s.new_midi_part("IAC Driver IAC Bus 1")
inst2 = s.new_midi_part("IAC Driver IAC Bus 2")
delay_incrementer = s.new_osc_part("incrementer", 7800, "127.0.0.1")

a = 59.0
b = 56.5

note_list = []
bar_types = []

class Note:
	def __init__(self, midi_number):
		self.midi_number = midi_number

class NoteTypeDurationPair:
	def __init__(self, note_type_names, duration):
		self.note_type_names = note_type_names
		self.duration = duration

bar_types.append([	NoteTypeDurationPair(["a", "a+4"], 1),
					NoteTypeDurationPair(["a+3", "a+7"], 1),
					NoteTypeDurationPair(["b+3", "b+7"], 1/2),
					NoteTypeDurationPair(["b", "b+4"], 1/2)])




p_limit = 17
q_limit = 23
note_list.append(Note(0))

for _ in range(0, 4):
	p = 0
	while p < p_limit:
		# a = 8, b = 7
		note_list.append(Note(a))
		note_list.append(Note(b))
		p += 1
	# while i <= i_limit/2:
	# 	# a = 8, b = 7
	# 	note_list.append(Note(a, 8))
	# 	note_list.append(Note(b+3, 8))
	# 	note_list.append(Note(b, 7*2))
	# 	note_list.append(Note(b+3, 8))
	# 	i += 1
	a += 1
	# p_limit -= 2
	note_list.append(Note(0))

	q = 0
	while q < q_limit:
		# b = 9, a = 11
		note_list.append(Note(a))
		note_list.append(Note(b))
		q += 1
	# while i <= i_limit:
	# 	# b = 9, a = 11
	# 	note_list.append(Note(a, 11*1.33333))
	# 	note_list.append(Note(b, 9))
	# 	note_list.append(Note(a+3, 8))
	# 	i += 1
	b += 1
	# q_limit += 2
	note_list.append(Note(0))


print("list built")

base_length = 1/16

s.new_osc_part("master_reset", 7700, "127.0.0.1").play_note(0, 0.0, 0.01, blocking = False)
s.wait(3)

s.start_transcribing()
# s.set_tempo_target(150, 800, 0)
# s.fast_forward_in_beats(4000)

for n in note_list:
	# length = Utilities.quantize(base_length * n.partial_number, 0.25)
	if n.midi_number == 0:
		bar_length = next(bar_lengths)
		macro_ratio = next(macro_ratios)
		micro_ratio = next(micro_ratios)
		txt = str(bar_length) + ", " + str(macro_ratio[0]) + ":" + str(macro_ratio[1]) + ", " + str(micro_ratio[0]) + ":" + str(micro_ratio[1])
		delay_incrementer.play_note(0, 0.0, 0.01, blocking = False, properties = scamp.StaffText(txt))
		# print(s.tempo)
	else:
		if n.midi_number.is_integer():
			inst1.play_chord([n.midi_number, n.midi_number+3], length = bar_length*(macro_ratio[0]/(macro_ratio[0]+macro_ratio[1]))*(micro_ratio[0]/(micro_ratio[0]+micro_ratio[1])), volume = 0.7)
			inst1.play_chord([n.midi_number+4, n.midi_number+7], length = bar_length*(macro_ratio[0]/(macro_ratio[0]+macro_ratio[1]))*(micro_ratio[1]/(micro_ratio[0]+micro_ratio[1])), volume = 0.7)
		else:
			inst2.play_chord([math.ceil(n.midi_number+4)], length = bar_length*(macro_ratio[1]/(macro_ratio[0]+macro_ratio[1]))*(micro_ratio[0]/(micro_ratio[0]+micro_ratio[1])), volume = 0.7)
			inst2.play_chord([math.ceil(n.midi_number)], length = bar_length*(macro_ratio[1]/(macro_ratio[0]+macro_ratio[1]))*(micro_ratio[1]/(micro_ratio[0]+micro_ratio[1])), volume = 0.7)

print(s.time())
print(s.beat())
score = s.stop_transcribing().to_score(time_signature = "3/4")
score.show()

