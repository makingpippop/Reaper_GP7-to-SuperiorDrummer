from .beat import Beat
from math import floor

class Note(Beat):
	def __init__(self, id, part_id, measure_id, inst_obj):
		super().__init__(id, part_id, measure_id, inst_obj)
		#
		self._step      = None
		#
		self._octave    = None
		#staccato, accent, marcato
		self.articulations_table = {"accent" : "_accent", "strong-accent": "_marcato", "staccato" : "_staccato",  "tenuto" : "_tenuto"}
		self._articulations  = []
		self._staccato 		= False
		self._accent 		= False
		self._marcato		= False
		self._tenuto 		= False
		self._ghost 		= False
		#tremolo indicate that it's a roll. This value will be equal to the ratio of tremolo subdivision (eight, 16th, 32th)
		self._tremolo 			= 0
		self._nb_tremolo_note 	= 0
		#
		self._grace 		= False
		#grace with a slash should be before the beat, with no slash, on beat
		self._grace_slash 	= None
		#is this a tuplet (triplet, quintuplet, sextuplet ...)

	def __str__(self) -> str:
		return f'<obj.{self.type}> ({self.part_id}|B:{self.beat} D:{self.duration})({self.instrument.name}) '

	def __repr__(self) -> str:
		return f'<obj.{self.type}> ({self.part_id}|B:{self.beat} D:{self.duration}) ({self.instrument.name}) '


	def load_attributes(self, *args):
		super().load_attributes(*args)
		last_beats = args[2]
		last_beat 	= last_beats['any']
		#dynamic
		n_dynamic 			= self.load_note_dynamic()
		n_dynamic 			= last_beat.dynamic if n_dynamic == None else n_dynamic
		self.dynamic 		= n_dynamic
		#step and octave
		self.step			= self.load_step()
		self.octave			= self.load_octave()
		#grace
		grace_slash			= self.load_grace()
		is_grace 			= True if grace_slash is not None else False
		self.grace_slash 	= grace_slash
		self.grace 			= is_grace
		#articulation
		self.load_articulations()
		#tremolo
		self._tremolo = self.load_tremolo()
		
	def load_note_dynamic(self):
		dynamic = None
		dynamic_attr = self.b_xml.find('./notations/dynamics/')
		if dynamic_attr is not None :
			dynamic_attr = dynamic_attr.iter()
			dynamic = next(dynamic_attr).tag
		return dynamic
	
	def load_tremolo(self):
		tremolo = 0
		tremolo_xml = self.b_xml.find('./notations/ornaments/tremolo')
		if tremolo_xml is not None :
			#get tremolo value (1, 2 or 3) and convert to note ratio
			tremolo = 1/(2**int(tremolo_xml.text))
			self._nb_tremolo_note =  floor(self.duration / tremolo)
		return tremolo
	
	def load_step(self):
		return self.b_xml.find('unpitched/display-step').text
	
	def load_octave(self):
		return int(self.b_xml.find('unpitched/display-octave').text)
	
	def load_grace(self):
		grace = self.b_xml.find('grace')
		if grace is not None :
			grace = grace.get('slash')
		return grace

	def load_articulations(self):
		articulation_attr = self.b_xml.find("./notations/articulations")
		if articulation_attr is not None :
			articulations_attr = articulation_attr.findall("./*")
			for a in articulations_attr:
				converted_accent = self.articulations_table[a.tag]
				self._articulations.append(converted_accent[1:])
				setattr(self,converted_accent,True)

		ghost_attr = self.b_xml.find("./notehead").get("parentheses")
		if ghost_attr is not None:
			self._articulations = ['ghost']
			self._ghost 		= True


	
	@property
	def step(self):
		return self._step
	@step.setter
	def step(self, value):
		self._step = value

	@property
	def octave(self):
		return self._octave
	@octave.setter
	def octave(self, value):
		self._octave = value

	@property
	def dynamic(self):
		return self._dynamic
	@dynamic.setter
	def dynamic(self, value):
		self._dynamic = value
	
	@property
	def grace(self):
		return self._grace
	@grace.setter
	def grace(self, value):
		self._grace = value
	
	@property
	def grace_slash(self):
		return self._grace_slash
	@grace_slash.setter
	def grace_slash(self, value):
		self._grace_slash = value

	@property
	def articulations(self):
		return self._articulations
	@articulations.setter
	def articulations(self, value):
		self._articulations = value
	
	@property
	def accent(self):
		return self._accent
	@accent.setter
	def accent(self, value):
		self._accent = value

	@property
	def marcato(self):
		return self._marcato
	@marcato.setter
	def marcato(self, value):
		self._marcato = value

	@property
	def staccato(self):
		return self._staccato
	@staccato.setter
	def staccato(self, value):
		self._staccato = value
	
	@property
	def ghost(self):
		return self._ghost
	@ghost.setter
	def ghost(self, value):
		self._ghost = value

	@property
	def played(self):
		return True if self._tie is None or self._tie == 'start' else False
	
	@property
	def tremolo(self):
		return self._tremolo
	@property
	def nb_tremolo_note(self):
		return 0 if self._tremolo == 0 else self._nb_tremolo_note-1
	
	