import os
from sys import path as PYTHONPATH
import reapy
from reapy import prevent_ui_refresh
#local imports
from the_logger import TheLogger
from musicxml import MusicXML
from GP_to_SD import GP_to_SD3
from helpers.reaper import get_nested_tracks, get_track_by_CC_pitch, combine_items_from_track_group, glue_all_items_on_track
from helpers.musicxml import link_MIDI_to_notation
#Add this package to the list of python package -------------
currentdir = os.path.dirname(os.path.realpath(__file__))
PYTHONPATH.append(currentdir)
#------------------------------------------------------------
#from itertools import chain

loggername 	= __name__ if __name__ != "__main__" else 'REAPER_GP7-to-SD3'
LOGGER 		= TheLogger(loggername, file='INFO', stream='INFO')

FILE_PATH  		= "G:/Shared drives/_Cydemind/Recordings/The-descent/SD3/05_Hemlock/Assets/MIDI/A"
FILENAME 		= "05_Hemlock_v3_Part-A"
DRUM_PART_ID 	= 1

def import_drums():
	##################################################
	#################################################
	#FIX ERROR WHEN FIRST MEASURE HAS NO NOTES
	##################################################
	##################################################
	musicXML 	= MusicXML(f"{FILE_PATH}/{FILENAME}.xml")
	score 		= musicXML.load_score()
	#print(musicXML.score)
	#return
	# for m in score.parts.P1.measures:
	# 	print(f'{m.id} ---------------------------------------')
	# 	#print('Num beats :', len(m.beats))
	# 	#for each beat ID 
	# 	for b_id in m.beats:
	# 		notes = m.beats[b_id]
	# 		#loop the notes
	# 		for i,n in enumerate(notes):
	# 			num_notes = 1 if n.type != "Chord" else len(n.notes)
	# 			print(f'NOTE #{n.voice}.{n.id} | Type : {n.type} ({n.instrument}) | Duration : {n.duration} | Beat : {n.beat} | Num note values : {num_notes}')
	# 			if n.type == "Chord":
	# 				for n_chord in n.notes:
	# 					print(f'\t{n_chord.instrument.pitch} : {n_chord.instrument.name} | Duration : {n_chord.duration} | Played : {n_chord.played}')
	# return

	# inst_variation_dict = {}
	# for m in score.measures:
	# 	for b in m.beats:
	# 		notes = m.beats[b]
	# 		notes = [n for n in notes if n.type == 'Note']
	# 		for n in notes:
	# 			if n.part_id == "P1":
	# 				inst = n.instrument
	# 				if inst.id not in inst_variation_dict:
	# 					inst_variation_dict[inst.id] = {"name" : inst.name, "pitch" : inst.pitch}

	# print(inst_variation_dict)

	#create groups
	gp_converter 	= GP_to_SD3(score)
	inst_groups		= gp_converter.groups
	#print( inst_groups['Snare'].articulations )
	#return
	# g_notes 		= inst_groups['Snare'].get_notes_from_part('P1')
	# #convert 2D into 1D list
	# g_notes 		= list(chain.from_iterable(g_notes))
	# print(g_notes)
	# return

	#get REAPER project
	project = reapy.Project()
	#set cursor to begining
	project.cursor_position = 0
	#import MIDI file
	print(project.__dict__)
	midi_item = project.import_media(f'{FILE_PATH}/{FILENAME}.mid')
	midi_track = midi_item.track
	#Add SD3 to the track's FX
	#midi_track.add_fx("Superior Drummer 3 (Toontrack) (32 out)")
	
	#select the imported item
	project.select_item(midi_item, makeUnique=True)
	print('Creating new tracks by MIDI pitch')
	#explode action (to seperate the imported midi into multiple tracks by pitch) ID 40920
	project.perform_action(40920)

	#get child tracks ----------------------------------------------------------
	child_tracks = get_nested_tracks(project, midi_track)
	
	#---------------------------------------------------------------------------
	#COMBINE MIDI FILES
	main_tracks = []
	ununsed_tracks = []

	project.begin_undo_block()
	with reapy.inside_reaper():
		for g in inst_groups:
			print(f'Merging track by instrument group : {g}')
			g_name 			= g
			g_pitchs 		= inst_groups[g].pitchs
			group_tracks 	= get_track_by_CC_pitch(g_pitchs, child_tracks)
			if len(group_tracks):
				#keep the last track (items from other tracks will be moved to this one)
				group_track = group_tracks[-1]
				main_tracks.append(group_track)
				ununsed_tracks += combine_items_from_track_group(g_name, group_tracks)

			print('\tDone!')
	project.end_undo_block()

	
	print('Deleting ununsed tracks')
	project.begin_undo_block()
	with reapy.inside_reaper():
		for t in ununsed_tracks:
			t.delete()
		midi_item.delete()
	project.end_undo_block()


	#glue items
	for t in main_tracks:
		project.begin_undo_block()
		with reapy.inside_reaper():
			print(f'Merging MIDI notes takes from group {g} ...')
			glue_all_items_on_track(project, t)
			print('\tDone!')
			#get associated group
			g = inst_groups[t.name]
			g.process(t, f'P{DRUM_PART_ID}')
		project.end_undo_block()
		

if __name__ == "__main__":
	import_drums()
