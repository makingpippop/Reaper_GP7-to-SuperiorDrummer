import reapy
from reapy import prevent_ui_refresh
from musicxml import MusicXML


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
	n_track_left    = project.n_tracks - midi_track.index
	last_track_id   = n_track_left+midi_track.index
	new_track_id    = midi_track.index

	child_tracks    = []
	for track_id in range(last_track_id, new_track_id+1, -1):
		track = project.tracks[track_id-1]
		if new_track_id == track.parent_track.index :
			child_tracks.insert(0,track)
	#---------------------------------------------------------------------------
	#COMBINE MIDI FILES
	with reapy.inside_reaper():
		project.begin_undo_block()
		group_tracks = []
		track_to_delete = []
		for g in instrument_groups:
			g_name 			= g
			g_pitchs 		= instrument_groups[g]
			reaper_tracks 	= get_group_tracks(g_pitchs, child_tracks)
			group_tracks.append(reaper_tracks[-1])
			track_to_delete += combine_group_tracks(g_name, reaper_tracks)
		
		for t in track_to_delete:
			t.delete()
		project.end_undo_block()

		#glue items
		for t in group_tracks:
			for i,item in enumerate(t.items):
				make_unique = i == 0
				project.select_item(item, makeUnique=make_unique)
			#glue items
			project.perform_action(41588)

@prevent_ui_refresh()
def get_group_tracks(pitch_list, reaper_tracks) -> list:
	pitch_tracks = []
	for t in reaper_tracks:
		if not len(t.items):
			continue
		CC_notes = t.items[0].takes[0].notes
		if not len(CC_notes):
			continue
		CC_note = t.items[0].takes[0].notes[0].pitch
		if CC_note in pitch_list:
			pitch_tracks.append(t)
	
	return pitch_tracks

@prevent_ui_refresh()
def combine_group_tracks(group_name, reaper_tracks) -> list:
	track_to_delete = []
	if len(reaper_tracks):
		main_track = reaper_tracks.pop()
		main_track.name = group_name
		for t in reaper_tracks:
			t.items[0].track = main_track
			track_to_delete.append(t)
	return track_to_delete	
	  

if __name__ == "__main__":
	import_drums()