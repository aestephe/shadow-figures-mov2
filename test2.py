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

s = scamp.Session(tempo = 180)
inst1 = s.new_midi_part("IAC Driver IAC Bus 1")
inst2 = s.new_midi_part("IAC Driver IAC Bus 2")
delay_incrementer = s.new_osc_part("incrementer", 7800, "127.0.0.1")

a = 59.0
b = 56.5

s.start_transcribing()
# s.fast_forward_in_beats(600)

note_list = []

class Note:
	def __init__(self, midi_number, partial_number):
		self.midi_number = midi_number
		self.partial_number = partial_number

j = 0
a_limit = 65.0
while j <= 10:
	i = 0
	i_limit = 10
	while i <= i_limit:
		# a = 8, b = 7
		note_list.append(Note(a, 11*1.33333))
		note_list.append(Note(b, 9))
		i += 1
	# while i <= i_limit/2:
	# 	# a = 8, b = 7
	# 	note_list.append(Note(a, 8))
	# 	note_list.append(Note(b+3, 8))
	# 	note_list.append(Note(b, 7*2))
	# 	note_list.append(Note(b+3, 8))
	# 	i += 1
	a += 1
	note_list.append(Note(0, 0))
	i = 0
	while i <= i_limit:
		# b = 9, a = 11
		note_list.append(Note(a, 11*1.33333))
		note_list.append(Note(b, 9))
		i += 1
	# while i <= i_limit:
	# 	# b = 9, a = 11
	# 	note_list.append(Note(a, 11*1.33333))
	# 	note_list.append(Note(b, 9))
	# 	note_list.append(Note(a+3, 8))
	# 	i += 1
	b += 1
	note_list.append(Note(0, 0))
	j += 1


print("list built")

base_length = 1/16

s.new_osc_part("master_reset", 7700, "127.0.0.1").play_note(0, 0.0, 0.01)
s.wait(3)

for n in note_list:
	length = Utilities.quantize(base_length * n.partial_number, 0.25)
	if n.midi_number == 0:
		delay_incrementer.play_note(0, 0.0, 0.01)

	else:
		if n.midi_number.is_integer():
			inst1.play_chord([n.midi_number, n.midi_number+7], length = length, volume = 0.7)
		else:
			inst2.play_chord([math.ceil(n.midi_number), math.ceil(n.midi_number+7)], length = length, volume = 0.7)

print(s.time())
score = s.stop_transcribing().to_score(time_signature = "2/4")
score.show()

