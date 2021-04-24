import musicxml
from musicxml.obj.measure.beats import Note, Rest
#
from .instrument 	import Instrument
from ..measure 		import Measure


class Part():
	def __init__(self, name, id, part_xml):
		self.part_xml 			= part_xml
		self.part_measure_xml 	= None
		self._name          	= name
		self._id 				= id
		self._instruments   	= {}
		self._measures 			= []

		self.last_dynamic = None
		print(f'New part : {self.name}')
		#print(musicxml.score)

	def __str__(self) -> str:
		return f'<obj.Part> ({self._id}:{self._name})'

	def __repr__(self) -> str:
		return f'<obj.Part> ({self._id}:{self._name})'
		
	def load_instruments(self):
		#loop <part-list><score-instrument> for the list of instrument on this track
		for p_inst in self.part_xml.findall('score-instrument'):
			inst_id 		= p_inst.get("id")
			inst_name 	= p_inst.find('instrument-name').text
			if inst_id not in self._instruments:
				self._instruments[inst_id] = Instrument(inst_name, inst_id, self.id)
			inst = self._instruments[inst_id]
			#loop the <part-list><midi-instrument> to get more info on the instrument
			self.load_midi_instruments(inst)


	def load_midi_instruments(self, inst):
		for p_midi_inst in self.part_xml.findall('midi-instrument'):
			midi_inst_id = p_midi_inst.get('id')
			#if the midi instrument ID matches the current track instrument ID
			if inst.id == midi_inst_id:
				inst.midiChannel 	= p_midi_inst.find('midi-channel').text
				#TO INVESTIGATE (GP PITCH IN XML IS ALWAYS 1 HIGHER)
				inst.pitch 			= int(p_midi_inst.find('midi-unpitched').text) - 1
				inst.volume			= p_midi_inst.find('volume').text
				inst.pan 			= p_midi_inst.find('pan').text
				break
	
	def set_measure_xml(self, measure_xml):
		self.part_measure_xml = measure_xml

	def add_measure(self, measure_obj):
		newMeasure = Measure(measure_obj.id, measure_ref=measure_obj)
		self._measures.append(newMeasure)

	def load_beats(self):
		if self.part_measure_xml is None:
			raise Exception('No XML has been link this part')
		
		last_m_division 	= None
		last_beats  		= {'any': None}
		for m_xml in self.part_measure_xml:
			m_id 	= int(m_xml.get('number'))
			m_obj 	= self._measures[m_id - 1]
			#get measure smallest subdivision and, use subdivision from last measure if no info is provided
			m_division = m_obj.load_measure_division(m_xml)
			m_division = last_m_division if m_division is None else m_division
			#load notes
			note_counter 	= 0
			cur_voice 		= 1
			cur_beat		= 1
			
			#print(f'MEASURE #{m_id} | Division : {m_division}')
			for n_xml in m_xml.findall('note'):
				inst 		= n_xml.find('instrument')
				inst_obj 	= None if inst is None else self._instruments[inst.get('id')]
				beatHasInst = inst_obj is not None 
				#inst_id 	= None if inst == None else inst.get('id')
				#check the voice (layer) of the note
				n_voice 	= int(n_xml.find('voice').text)
				#if we changed voice, reset the counter
				new_voice = n_voice != cur_voice
				note_counter = 0 if new_voice else note_counter

				#add a beat to the measure
				beat_args	= (note_counter, self.id, m_obj.id, inst_obj)
				beat_obj 	= Rest(*beat_args) if inst is None else Note(*beat_args)
				#beat_obj = m_obj.add_beat(note_counter, self.id, inst_obj)
				beat_obj.set_beat_xml(n_xml)
				beat_obj.load_attributes(m_division, cur_beat, last_beats)


				#check for tie
				mergeThisBeat = False
				last_inst_beat 	= last_beats[inst_obj.id] if beatHasInst and inst_obj.id in last_beats else None
				if last_inst_beat is not None and beat_obj.tie is not None:
					#if the current beat is the end of the tie, or the last beat was the start
					if beat_obj.tie == 'stop' or last_inst_beat.tie == 'start':
						mergeThisBeat = True
						#update duration of the Note that started the tie
						last_inst_beat.duration += beat_obj.duration
						#print(f'THIS BEAT {m_obj.id}.{beat_obj.id} IS TIED TO : {m_obj.id}.{last_inst_beat.id}\nNew duration :{last_inst_beat.duration}')

				#save the last beat processed
				last_beats['any'] 	= beat_obj

				if new_voice:
					cur_beat 	= 1
					n_voice 	= cur_voice
				else:
					cur_beat = beat_obj.beat

				#if this beat is not a tie
				if not mergeThisBeat:
					#the last beat of this instrument will be the processed beat
					if beatHasInst:
						last_beats[inst_obj.id] = beat_obj
					m_obj.add_beat(beat_obj)
					note_counter += 1
				#if this beat is a tie
				else:
					#the last beat of this instrument is the begining of the tie
					last_beats[inst_obj.id] = last_inst_beat
				
				
			last_m_division = m_division
			
	@property
	def id(self):
		return self._id

	@property
	def name(self):
		return self._name
	
	@property
	def instruments(self):
		return self._instruments
	
	@property
	def measures(self):
		return self._measures
