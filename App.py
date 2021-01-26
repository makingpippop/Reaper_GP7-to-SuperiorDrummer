import reapy
from reapy import prevent_ui_refresh
from musicxml import MusicXML
from helpers import get_nested_tracks, get_track_by_CC_pitch, combine_items_from_track_group, glue_all_items_on_track

def import_drums():
	musicXML 	= MusicXML("GP/_exports/All-drums-notation.xml")
	score 		= musicXML.load_score()
	
	inst_variation_dict = {}
	for m in score.measures:
		for b in m.beats:
			notes = m.beats[b]
			notes = [n for n in notes if n.type == 'Note']
			for n in notes:
				if n.part_id == "P3":
					inst = n.instrument
					if inst.id not in inst_variation_dict:
						inst_variation_dict[inst.id] = {"name" : inst.name, "pitch" : inst.pitch}
	
	print(inst_variation_dict)

	# snares = 	{
	# 				"39" : {
	# 							'names' 	: ['Snare (hit)', 'Snare (rim shot)'],
	# 							'SD3-notes' : [39, 40]
	# 				},
	# 				"38" : {
	# 							'names' 	: ['Snare (side stick)'],
	# 							'SD3-notes' : [36]
	# 				}
	# 			}
	#GP Pitch
	#COMMENTED = PITCH FROM MUSICXML
	#sidestick, hit, rimshot
	snare_group 	= [37, 38, 38] #[38, 39, 39]
	#hit, open
	bass_drum_group = [36, 35] #[37, 36]
	#hi, med, low, floor1, floor2
	toms_group 		= [48, 47, 45, 50, 43] #[49, 48, 46, 51, 44]
	#closed, half, open, pedal
	hi_hat_group 	= [42, 46, 46, 44] #[43, 47, 47, 45]
	#middle, edge, bell
	ride_group 		= [51, 51, 53] #[52, 52, 54]
	#crash medium, crash high, splash, china
	cymbals_group 	= [57, 49, 55, 52] #[58, 50, 56, 53]

	instrument_groups = 	{
								'Snare' 	: snare_group,
								'Bass-drum' : bass_drum_group,
								'Toms' 		: toms_group,
								'Hi-hat'	: hi_hat_group,
								'Ride' 		: ride_group,
								'Cymbals'	: cymbals_group
							}

	project = reapy.Project()

	midi_item = project.import_media("D:/Documents/DAW/Reaper/Custom-actions/04_Call-of-the-Void_v2.mid")
	midi_track = midi_item.track
	#select the new item
	project.select_item(midi_item, makeUnique=True)

	#explode action (to seperate the imported midi into multiple tracks by pitch) ID 40920
	project.perform_action(40920)

	#get child tracks ----------------------------------------------------------
	child_tracks = get_nested_tracks(project, midi_track)
	
	#---------------------------------------------------------------------------
	#COMBINE MIDI FILES
	with reapy.inside_reaper():
		project.begin_undo_block()
		main_tracks = []
		ununsed_tracks = []
		for g in instrument_groups:
			g_name 			= g
			g_pitchs 		= instrument_groups[g]
			group_tracks 	= get_track_by_CC_pitch(g_pitchs, child_tracks)
			if len(group_tracks):
				#keep the last track (items from other tracks will be moved to this one)
				main_tracks.append(group_tracks[-1])
				ununsed_tracks += combine_items_from_track_group(g_name, group_tracks)
		
		for t in ununsed_tracks:
			t.delete()
		project.end_undo_block()

		#glue items
		for t in main_tracks:
			glue_all_items_on_track(project, t)


	  

if __name__ == "__main__":
	import_drums()