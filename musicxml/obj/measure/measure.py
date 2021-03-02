from .beats import Rest, Note


class Measure(object):
	def __init__(self, id, m_xml=None, measure_ref=None):
		self._id			= id
		self._bpm			= None if measure_ref is None else measure_ref.bpm
		self._signature		= None if measure_ref is None else measure_ref.signature
		self._beats 		= {}
		self._notes			= {}
		self._beats 		= {}
		self._instruments	= []
	
	def __str__(self):
		return f'<obj.Measure> #{self._id} | {"/".join(map(str,self._signature))}'

	def __repr__(self):
		return f'<obj.Measure> #{self._id} | {"/".join(map(str,self._signature))}'

	def add_beat(self, beat_obj):
		beat_id = beat_obj.id
		if beat_id in self._beats:
			self._beats[beat_id].append(beat_obj)
		else:
			self._beats[beat_id] = [beat_obj]
			
	# def add_beat(self, beat_id, part_id, inst):
	# 	beat_args = (beat_id, part_id, self._id, inst)
	# 	beat = Rest(*beat_args) if inst is None else Note(*beat_args)

	# 	if beat_id in self._beats:
	# 		self._beats[beat_id].append(beat)
	# 	else:
	# 		self._beats[beat_id] = [beat]

	# 	#print(f'NEW BEAT ({beat.type}) #{beat.id} from instrument : {beat.instrument}')
	# 	return beat
	
	def add_instrument(self, inst_obj):
		pass

	def load_measure_signature(self, xml_measure):
		signature = None
		m_time_attr = xml_measure.find('attributes/time')

		if m_time_attr is not None:
			beat = int(m_time_attr.find("beats").text)
			beat_sub = int(m_time_attr.find("beat-type").text)
			signature = [beat, beat_sub]

		#if this is the first measure dans there's no signature
		if signature is None and self.id == 1:
			raise Exception('Error whithin the file. No time signature on the first measure')
		return signature

	def load_measure_bpm(self, xml_measure):
		bpm = None
		metronome_attr = xml_measure.find('./direction/direction-type/metronome')
		if metronome_attr is not None:
			bpm = int(metronome_attr.find("per-minute").text)

		#if this is the first measure dans there's no bpm
		if bpm is None and self.id == 1:
			raise Exception('Error whithin the file. No bpm on the first measure')
		return bpm
	
	def load_measure_division(self, xml_measure):
		subdivision		= None
		m_division_attr = xml_measure.find('attributes/divisions')
		if m_division_attr is not None:
			subdivision = int(m_division_attr.text)
		return subdivision

	@property
	def id(self):
		return self._id

	@property
	def bpm(self):
		return self._bpm

	@bpm.setter
	def bpm(self, value):
		self._bpm = value

	@property
	def signature(self):
		return self._signature

	@signature.setter
	def signature(self, value):
		self._signature = value

	@property
	def instruments(self):
		return self._instruments
	
	@property
	def beats(self):
		return self._beats
	
	#returns a list of parts that have notes in this measure
	@property
	def parts(self):
		return None
