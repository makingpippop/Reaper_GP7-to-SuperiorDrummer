from .beat import Beat

class Note(Beat):
	def __init__(self, id, part_id, inst_obj):
		super().__init__(id, part_id, inst_obj)
		#
		self._step      = None
		#
		self._octave    = None
		#pppp, ppp, pp, p, mf, ...
		self._dynamic   = ''
		#staccato, accent, marcato
		self._articulation  = ''
		#tremolo indicate that it's a roll
		self._tremolo 		= False
		#
		self._grace 		= False
		#grace with a slash should be before the beat, with no slash, on beat
		self._grace_slash 	= None
		#is this a tuplet (triplet, quintuplet, sextuplet ...)
	
	def get_note_dynamic(self, n_xml):
		dynamic = None
		dynamic_attr = n_xml.find('./notations/dynamics/')
		if dynamic_attr is not None :
			dynamic_attr = dynamic_attr.iter()
			dynamic = next(dynamic_attr).tag
		return dynamic

	@property
	def dynamic(self):
		return self._dynamic
	@dynamic.setter
	def dynamic(self, value):
		self._dynamic = value
