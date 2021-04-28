from musicxml.obj.part.instrument import Instrument
from random import randint

from typing import List
from .config import PITCHS, VELOCITIES, MODIFIERS

class Group(object):
	def __init__(self, name, score_ref) -> None:
		super().__init__()
		self._score_ref         = score_ref
		self._pitchs            = []
		self._names             = []
		self._ids               = []
		self._instruments       = {}
		self._group_name        = name

	
	def add_instrument(self, inst_obj:Instrument):
		if not isinstance(inst_obj, Instrument):
			raise TypeError('The argument must be time musicxml.obj.Part.Instrument')
		
		self._pitchs.append(inst_obj.pitch)
		self._names.append(inst_obj.name)
		self._ids.append(inst_obj.id)
		self._instruments[f'{inst_obj.pitch}_{inst_obj.name}'] = inst_obj
		pass
	
	def get_notes_from_part(self, part_id):
		measures = self._score_ref.parts[part_id].measures
		notes = []
		#loop measures

		for m in measures:
			#print("MEASURE #",m.id)
			notes.append([])
			#loop beats
			for b in m.beats:
				#print(f'\t{m.beats[b]}')
				#loop each beat entry(note/rest/chord) of every voice 
				for n in m.beats[b]:
					#if a chord
					if n.type == "Chord":
						#loop each note in the chord
						for n_chord in n.notes:
							#check if it's played (not tied to the last)
							if n_chord.played:
								g_inst_id = self._get_inst_id(n_chord)
								if g_inst_id is not None and g_inst_id in self._instruments:
									#notes[m.id-1].insert(0,n_chord)
									#print(f'\t\tAdding {n_chord}')
									notes[m.id-1].append(n_chord)
					#if a note
					elif n.type == 'Note':
						g_inst_id = self._get_inst_id(n)
						if g_inst_id is not None and g_inst_id in self._instruments:
							#notes[m.id-1].insert(0,n)
							#print(f'\t\tAdding {n}')
							notes[m.id-1].append(n)

		
		return notes
	def _get_inst_id(self, n):
		inst = n.instrument
		g_inst_id = f'{inst.pitch}_{inst.name}'
		return g_inst_id

	def process(self, r_track, gp_part_id):
		print(f'Starting process for : {self._group_name}')
		def _convert_pitchs():
			if inst_id in PITCHS:
				pitchs 			= PITCHS[inst_id]
				default_pitch 	= pitchs['default']
				final_pitch 	= default_pitch
				for p in pitchs:
					if p != 'default':
						articulation_pitch = getattr(gp_n, p)						
						if bool(articulation_pitch):
							final_pitch = pitchs[p]

				if type(final_pitch) is list:
					rand_pitch 	= randint(0, len(final_pitch) - 1)
					final_pitch = final_pitch[rand_pitch]

				r_n.pitch = int(final_pitch)
			else:
				print(inst_id, 'not in config')
				#print(default_pitch)
			pass
		def _convert_velocity():
			note_dyn 	= gp_n.dynamic
			vel_range 	= VELOCITIES['default'][note_dyn]
			#if there's a specific range for this group
			if self._group_name in VELOCITIES:
				group_vel = VELOCITIES[self._group_name]
				#if there's a specific range for this instrument
				if inst_id in group_vel and note_dyn in group_vel[inst_id]:
					vel_range 	= group_vel[inst_id][note_dyn]
				elif 'default' in group_vel and note_dyn in group_vel['default']:
					vel_range 	= group_vel['default'][note_dyn]
				
			
			final_vel 		= randint(vel_range[0], vel_range[1])
			r_n.velocity 	= final_vel

		def _adjust_dynamics():
			for m in MODIFIERS:
				#if the note contains one of the modifiers
				if m in gp_n._articulations:
					m_range 	= MODIFIERS[m]['default']

					if self._group_name in MODIFIERS[m]:
						group_mod = MODIFIERS[m][self._group_name]
						#if there's a specific range for this instrument
						if inst_id in group_mod:
							m_range 	= group_mod[inst_id]
						elif 'default' in group_mod:
							m_range 	= group_mod['default']

					m_val 		= randint(m_range[0], m_range[1])
					m_val 		= 1-m_val if m == 'ghost' else m_val
					new_vel 	= r_n.velocity + m_val
					r_n.velocity = new_vel

			pass


		gp_notes = self.get_notes_from_part(gp_part_id)
		abs_beat = 0
		for m in self._score_ref.measures:
			t_m_notes 	= r_track.items[0].takes[0].notes.in_measure(m.id)
			#sort the list using the absolute beat value
			t_m_notes.sort(key=lambda x: x.beat)
			gp_m_notes	= gp_notes[m.id-1]
			#if there's not the same number of notes
			if  len(t_m_notes) != len(gp_m_notes):
				self._print_note_comparaison(m.id, t_m_notes, gp_m_notes)
				#check if there's an error in the MIDI file import and there two of the same notes
				#if REAPER has more note than GP
				if len(t_m_notes) > len(gp_m_notes):
					t_m_notes = self._del_reaper_doublon(t_m_notes)

				#re-check length
				if len(t_m_notes) != len(gp_m_notes): 
					#self._print_note_comparaison(m.id, t_m_notes, gp_m_notes)
					raise Exception
			for i, r_n in enumerate(t_m_notes):
				gp_n 	= gp_m_notes[i]
				inst_id = self._get_inst_id(gp_n)
				_convert_pitchs()
				_convert_velocity()
				_adjust_dynamics()

				# print(f'\t\t{n.pitch} | BEAT : {n.beat+1} # {(gp_n.beat) + abs_beat}')
				# print(f'\t\t\tGhost\t\t:\t{gp_n.ghost}')
				# print(f'\t\t\tStaccato\t:\t{gp_n.staccato}')
				# print(f'\t\t\tAccent\t\t:\t{gp_n.accent}')
				# print(f'\t\t\tMarcato\t\t:\t{gp_n.marcato}')
				# print(f'\t\t\tTremolo\t\t:\t{gp_n.tremolo}')
				#print('\t\t',n.infos)
			abs_beat += m.duration

		print('\tDone!')

	def _print_note_comparaison(self, m_id, track_notes, gp_notes):
		r_notes = [f'{n.beat} | {n.start:.2f}-{n.end:.2f}' for n in track_notes]
		print(f'ERROR : {self._group_name} - Measure #{m_id} | Length : R:{len(track_notes)} GP:{len(gp_notes)}')
		#print(f'\t R : {r_notes}')
		#print(f'\t G : {gp_notes}')

	def _del_reaper_doublon(self, track_notes):
		for r_n in track_notes:
			beat 	= r_n.beat
			start 	= f'{r_n.start:.3f}'
			pitch 	= r_n.pitch
			for i,r_nx in enumerate(track_notes):
				if r_nx is not r_n:
					xbeat 	= r_nx.beat
					xstart 	= f'{r_nx.start:.3f}'
					xpitch 	= r_nx.pitch
					if xpitch == pitch and xbeat == beat and xstart == start:
						print('\tResolved!')
						del track_notes[i]
						continue
		return track_notes

	@property
	def group_name(self):
		return self._group_name
	

	@property
	def names(self):
		return self._names

	@property
	def pitchs(self):
		return self._pitchs
	
	@property
	def instruments(self):
		return self._instruments
	
	#