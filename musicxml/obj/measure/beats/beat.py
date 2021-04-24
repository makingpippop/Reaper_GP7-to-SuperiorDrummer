from typing import Type


class Beat(object):
	def __init__(self, id, part_id, measure_id, inst_obj):
		self.type       = self.__class__.__name__
		#chronological id in the measure (for the specified instrument)
		self._id        = id
		#
		self.b_xml      = None
		#
		self._measure 	= measure_id
		#part containing this note
		self._part      = part_id
		#instrument making the note
		self._inst      = inst_obj

		#is this Note tied to other notes
		self._tie 		= None
		#choronological id in voice layer
		self.voice_id   = None
		#which beat in the measure
		self._beat      = 0
		#position in the measure (0.0 -> 1.0) 
		self._position  = 0
		#duration, in relation a the measure length (0.0 -> 4.0)
		self._duration  = None
		# self._duration_name    = None
		self.type_to_duration = {  
									'whole'           : 4,
									'half'            : 2,
									'quarter'         : 1,
									'dotted-eight'    : 1/1.33333,    #(0.75)
									'eighth'          : 1/2,          #(0.5)      
									'16th'            : 1/4,          #(0.25)
									'32nd'            : 1/8,          #(0.125)
									'64th'            : 1/16          #(0.0625)
								 }
		#is this a tuplet (triplet, quintuplet, sextuplet ...)
		self._tuplet            = False
		#ratio of note / beat (a triplet is 3:2, quintuplet 5:4)
		self._tuplet_ratio         = None
		#
		self._dotted        = False 
		#pppp, ppp, pp, p, mf, ...
		self._dynamic   = ''
		#text entered in GP
		self._text = None 

	
	def __str__(self) -> str:
		return f'<obj.{self.type}> ({self._part}:{self._duration})'

	def __repr__(self) -> str:
		return f'<obj.{self.type}> ({self._part}:{self._duration})'

	def set_beat_xml(self, b_xml):
		self.b_xml = b_xml

	def load_attributes(self, m_division, cur_beat, last_beats):
		#last beat processed
		last_beat 		= last_beats['any']
		#last beat of the same instrument
		#last_inst_beat 	= last_beats[self.instrument.id] if self.instrument and self.instrument.id in last_beats else None

		#voice (layer)
		self.voice 			= self.load_voice()
		#duration
		xml_beat_duration 	= self.load_duration()
		beat_duration 		= xml_beat_duration / m_division
		self.duration 		= beat_duration
		
		#if there were no beat evaluated before this one
		#or the last beat was owned by another measure
		if last_beat is None or last_beat.measure != self._measure:
			self.beat  = 1
		else:
			self.beat = cur_beat + last_beat.duration
			#*** HOW TO ACCESS NOTES BEFORE THIS BEAT
			#HOW TO FIND HIS POSITION IN THE MEASURE???
			#https://www.musicxml.com/tutorial/the-midi-compatible-part/chords/
			#***
		#if self._measure == 3:
		#	print(f'NOTE # {self._measure}.{self.id} | Inst : {self.instrument.id} | Type : {self.type} | Duration : {beat_duration} | Beat : {self.beat}')
		#if last_inst_beat:
			#print(f'LAST INST BEAT = {last_inst_beat._measure}.{last_inst_beat.id}') 
		
		#dot
		self.dotted 		= self.load_dotted()
		#tuplet
		self.tuplet 		= self.load_tuplet()
		self.tuplet_ratio 	= self.load_tuplet_ratio()
		#tie
		self._tie 			= self.load_tie()

	def load_duration(self):
		duration = None
		dur_attr = self.b_xml.find('duration')
		if dur_attr is not None:
			duration = int(dur_attr.text)
		#sometimes <duration> doesn't exist, it's the case for grace note
		#if it's the case use the <note><type>
		else:
			b_type_attr = self.b_xml.find('type').text
			duration    = self.type_to_duration[b_type_attr]

		return duration

	def load_voice(self):
		return int(self.b_xml.find('voice').text)

	def load_dotted(self):
		dot_tag = self.b_xml.findall('dot')
		return 0 if dot_tag == None else len(dot_tag)

	def load_tuplet(self):
		tuplet_tag 	= self.b_xml.find('notations/tuplet')
		return False if tuplet_tag == None else True

	def load_tuplet_ratio(self):
		tuplet_ratio = None
		tuplet_tag 	    = self.b_xml.find('notations/tuplet')
		if tuplet_tag is not None:
			tuplet_dur      = int(self.b_xml.find("time-modification/normal-notes").text)
			tuplet_num_note = int(self.b_xml.find("time-modification/actual-notes").text)
			tuplet_ratio    = [tuplet_num_note, tuplet_dur]
		return tuplet_ratio

	def load_tie(self):
		tied 		= None
		tie_tag		= self.b_xml.find('tie')
		if tie_tag is not None:
			tied = tie_tag.get('type')
		return tied
	# def load_(self, b_xml):
	#     return


	# def _set_duration(self, duration_value):
	#     #if we set the duration with a name
	#     if type(duration_value) == str:
	#         duration_value = duration_value.lower()
	#         if duration_value not in self.duration_name_to_ratio:
	#             raise TypeError(f'"{duration_value}" is not a type of beat duration\nThe valid types are : {list(self.duration_name_to_ratio.keys())}')

	#         dur = self.duration_name_to_ratio[duration_value]
	#         self._duration_name = duration_value
	#     else:
	#         if duration_value not in self.duration_name_to_ratio.values():
	#             raise TypeError(f'"{duration_value}" is not a type of beat duration\nThe valid types are : {list(self.duration_name_to_ratio.items())}')
			
	#         dur         = duration_value
	#         dur_name    = [v for v in self.duration_name_to_ratio if self.duration_name_to_ratio[v] == duration_value]
	#         self._duration_name = dur_name

	#     return dur

	@property
	def id(self):
		return self._id
		
	@property
	def instrument(self):
		return self._inst

	@property
	def part_id(self):
		return self._part
	
	@property
	def voice(self):
		return self._voice_id
	@voice.setter
	def voice(self, value):
		self._voice_id = value

	@property
	def position(self):
		return self._position
	@position.setter
	def position(self, value):
		self._position = value

	@property
	def duration(self):
		return self._duration
	@duration.setter
	def duration(self, value):
		# dur = self._set_duration(value)
		self._duration = value

	@property
	def dynamic(self):
		return self._dynamic
	@dynamic.setter
	def dynamic(self, value):
		self._dynamic = value
	
	@property
	def tuplet(self):
		return self._tuplet
	@tuplet.setter
	def tuplet(self, value):
		self._tuplet = value

	@property
	def tuplet_ratio(self):
		return self._tuplet_ratio
	@tuplet_ratio.setter
	def tuplet_ratio(self, value):
		self._tuplet_ratio = value

	@property
	def dotted(self):
		return self._dotted
	@dotted.setter
	def dotted(self, value):
		self._dotted = value

	@property
	def tie(self):
		return self._tie
	@tie.setter
	def tie(self, value):
		self._tie = value

	@property
	def text(self):
		return self._text
	@text.setter
	def text(self, value):
		self._text = value
	
	@property
	def beat(self):
		return self._beat
	@beat.setter
	def beat(self, value):
		self._beat = value

	@property
	def measure(self):
		return self._measure
	