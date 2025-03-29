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

s = scamp.Session(tempo = 500)
inst1 = s.new_midi_part("IAC Driver IAC Bus 1")
inst2 = s.new_midi_part("IAC Driver IAC Bus 2")

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
a_limit = 72.0
while a <= a_limit:
	i = 0
	while i <= 8:
		# a = 8, b = 7
		note_list.append(Note(a, 8))
		note_list.append(Note(b, 7*2))
		i += 1
	a += 2
	b += 1
	i = 0
	if a <= a_limit:
		while i <= 6:
			# b = 9, a = 11
			note_list.append(Note(a, 11*1.33333))
			note_list.append(Note(b, 9))
			if i in [2, 6]:
				note_list.append(Note(a-2, 10))
			if i % 3 == 0 and i > 0:
				note_list.append(Note(a+3, 10))
			i += 1
		b += 2
		a += 1
	j += 1

base_length = 0.25
for n in note_list:
	print(n.midi_number)
	if n.midi_number.is_integer():
		inst1.play_chord([n.midi_number, n.midi_number+3, n.midi_number+7], length = base_length * n.partial_number, volume = 0.7)
	else:
		inst2.play_chord([math.ceil(n.midi_number), math.ceil(n.midi_number+3), math.ceil(n.midi_number+7)], length = base_length * n.partial_number, volume = 0.7)

print(s.time())
s.stop_transcribing().to_score().show()