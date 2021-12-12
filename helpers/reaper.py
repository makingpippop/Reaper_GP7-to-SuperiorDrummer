import reapy
from typing import List

R_track 	= reapy.Track
R_tracks 	= List[R_track]
R_project 	= reapy.Project

def get_nested_tracks(project:R_project, track:R_track) -> R_tracks:
	with reapy.inside_reaper():
		child_tracks    = []
		n_track_left    = project.n_tracks - track.index
		last_track_id   = n_track_left+track.index
		new_track_id    = track.index

		for track_id in range(last_track_id, new_track_id+1, -1):
			track = project.tracks[track_id-1]
			if new_track_id == track.parent_track.index :
				child_tracks.insert(0,track)
	return child_tracks

@reapy.prevent_ui_refresh()
def get_track_by_CC_pitch(pitch_list:List[int], tracks:R_tracks) -> R_tracks:
	with reapy.inside_reaper():
		pitch_tracks = []
		#loop tracks
		for t in tracks:
			#skip if there's no item on the track
			if not len(t.items):
				continue
			CC_notes = t.items[0].takes[0].notes
			#skip if there's no note on the track
			if not len(CC_notes):
				continue
			#get pitch of the first note
			CC_note = t.items[0].takes[0].notes[0].pitch
			if CC_note in pitch_list:
				pitch_tracks.append(t)
	
	return pitch_tracks

@reapy.prevent_ui_refresh()
def combine_items_from_track_group(group_name:str, tracks:R_tracks) -> R_tracks:
	unused_tracks = []
	with reapy.inside_reaper():
		if len(tracks):
			main_track 		= tracks.pop()
			main_track.name = group_name

			for t in tracks:
				t.items[0].track = main_track
				unused_tracks.append(t)
	return unused_tracks	

def glue_all_items_on_track(project:R_project, track:R_track) -> None:
	with reapy.inside_reaper():
		for i,item in enumerate(track.items):
			#make unique selection if it's the first item in the loop
			make_unique = i == 0
			project.select_item(item, makeUnique=make_unique)
		#glue items
		project.perform_action(42432)

