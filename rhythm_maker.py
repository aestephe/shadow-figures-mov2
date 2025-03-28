
# 0123
# 0231
# 0312

# (0123)
# 2130
# 3102

# (0123)
# 1320
# 3021

# (0123)
# 1203
# 2013


import scamp

scamp.playback_settings.try_system_fluidsynth_first = True
scamp.playback_settings.make_persistent()

s = scamp.Session(tempo = 252)

bar_length, time_sig = 5, "5/4"

# ratio between piano's total notes vs. keyboard's total notes 
macro_ratio = [3, 7]

# ratio between individual notes within the piano or keyboard
micro_ratio = [6, 5]

# 0 = piano note 1
# 1 = piano note 2
# 2 = piano note 3
# 3 = piano note 4
note_order = [0, 3, 1, 2]

upper_staff = s.new_midi_part(name = "Keyboard", midi_output_device = "IAC Driver Bus 1")
lower_staff = s.new_midi_part(name = "Piano", midi_output_device = "IAC Driver Bus 1")

s.start_transcribing()

for n in note_order:
	if n == 0:
		lower_staff.play_chord([60], length = bar_length*(macro_ratio[0]/(macro_ratio[0]+macro_ratio[1]))*(micro_ratio[0]/(micro_ratio[0]+micro_ratio[1])), volume = 1)
	elif n == 1:
		lower_staff.play_chord([60], length = bar_length*(macro_ratio[0]/(macro_ratio[0]+macro_ratio[1]))*(micro_ratio[1]/(micro_ratio[0]+micro_ratio[1])), volume = 1)
	elif n == 2:
		upper_staff.play_chord([60], length = bar_length*(macro_ratio[1]/(macro_ratio[0]+macro_ratio[1]))*(micro_ratio[1]/(micro_ratio[0]+micro_ratio[1])), volume = 1)
	elif n == 3:
		upper_staff.play_chord([60], length = bar_length*(macro_ratio[1]/(macro_ratio[0]+macro_ratio[1]))*(micro_ratio[0]/(micro_ratio[0]+micro_ratio[1])), volume = 1)

score = s.stop_transcribing().to_score(time_signature = time_sig)
score.show()



