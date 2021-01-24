from sys import settrace
from .note import Note

class Measure(object):
	def __init__(self, id, m_xml):
		self.m_xml          = m_xml
		self._id            = id
		self._bpm           = None
		self._signature     = None
		self._subdivision   = None
		self._notes         = []
		self._instruments   = []

	def add_note(self, part, inst):
		return
	
	def add_instrument(self,inst_obj):
		pass

	def load_measure_signature(self, xml_measure):
		signature = None
		m_time_attr = xml_measure.find('attributes/time')

		if m_time_attr is not None :
			beat = int(m_time_attr.find("beats").text)
			beat_sub = int(m_time_attr.find("beat-type").text)
			signature = [beat, beat_sub]

		#if this is the first measure dans there's no signature
		if signature == None and self.id == 1:
			raise Exception('Error whithin the file. No time signature on the first measure')
		return signature

	def load_measure_bpm(self, xml_measure):
		bpm = None
		metronome_attr = xml_measure.find('./direction/direction-type/metronome')
		if metronome_attr is not None :
			bpm = int(metronome_attr.find("per-minute").text)

		#if this is the first measure dans there's no bpm
		if bpm == None and self.id == 1:
			raise Exception('Error whithin the file. No bpm on the first measure')
		return bpm
	
	def load_measure_division(self, xml_measure):
		subdivision		= None
		m_division_attr = xml_measure.find('attributes/divisions')
		if m_division_attr is not None :
			subdivision = int(m_division_attr.text)
		return subdivision

	@property
	def id(self):
		return self._id

	@property
	def bpm(self):
		return self._bpm
	@bpm.setter 
	def bpm (self, value):
		self._bpm = value

	@property
	def signature(self):
		return self._signature
	@signature.setter 
	def signature (self, value):
		self._signature = value

	@property
	def subdivision(self):
		return self._subdivision
	@subdivision.setter 
	def subdivision (self, value):
		self._subdivision = value

	@property
	def instruments(self):
		return self._instruments