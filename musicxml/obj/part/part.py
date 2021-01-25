from .instrument import Instrument


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
				inst.pitch 			= p_midi_inst.find('midi-unpitched').text
				inst.volume			= p_midi_inst.find('volume').text
				inst.pan 			= p_midi_inst.find('pan').text
				break
	
	def set_measure_xml(self, measure_xml):
		self.part_measure_xml = measure_xml

	def link_measure(self, measure_obj):
		self._measures.append(measure_obj)

	def load_beats(self):
		if self.part_measure_xml is None:
			raise Exception('No XML has been link this part')
		
		last_m_division = None
		for m_xml in self.part_measure_xml:
			m_id 	= int(m_xml.get('number'))
			m_obj 	= self._measures[m_id-1]
			#get measure smallest subdivision and, use subdivision from last measure if no info is provided
			m_division = m_obj.load_measure_division(m_xml)
			m_division = last_m_division if m_division == None else m_division
			#load notes
			note_counter 	= 0
			cur_voice 		= 1
			#print(f'MEASURE #{m_id} | Division : {m_division}')
			for n_xml in m_xml.findall('note'):
				inst 		= n_xml.find('instrument')
				inst_obj 	= None if inst == None else self._instruments[inst.get('id')]
				#inst_id 	= None if inst == None else inst.get('id')
				#check the voice (layer) of the note
				n_voice 	= int(n_xml.find('voice').text)
				#if we changed voice, reset the counter 
				if n_voice != cur_voice:
					note_counter 	= 0
					n_voice 		= cur_voice
				#add a beat to the measure
				beat_obj = m_obj.add_beat(note_counter, self.id, inst_obj)
				beat_obj.set_beat_xml(n_xml)
				self.load_beat(m_division, n_xml, beat_obj)

				
				note_counter += 1
			last_m_division = m_division
			

	def load_beat(self, m_division, b_xml, beat_obj):
		#voice (layer)
		beat_obj.voice 			= beat_obj.load_voice()
		#duration
		xml_beat_duration 		= beat_obj.load_duration()
		beat_duration 			= xml_beat_duration / m_division
		beat_obj.duration 		= beat_duration
		#dot
		beat_obj.dotted 		= beat_obj.load_dotted()
		#tuplet
		beat_obj.tuplet 		= beat_obj.load_tuplet()
		beat_obj.tuplet_ratio 	= beat_obj.load_tuplet_ratio()

		#NOTES
		if beat_obj.type == "Note":
			#dynamic
			n_dynamic = beat_obj.load_note_dynamic()
			n_dynamic = self.last_dynamic if n_dynamic == None else n_dynamic
			self.last_dynamic = n_dynamic
			beat_obj.dynamic = n_dynamic
			#step and octave
			beat_obj.step	= beat_obj.load_step()
			beat_obj.octave	= beat_obj.load_octave()
			#grace
			grace_slash 			= beat_obj.load_grace()
			is_grace 				= True if grace_slash is not None else False
			beat_obj.grace_slash 	= grace_slash
			beat_obj.grace 			= is_grace
			#articulation
			beat_obj.load_articulations()
			#tremolo
			beat_obj.tremolo = beat_obj.load_tremolo()
			
		#REST


		pass

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
	