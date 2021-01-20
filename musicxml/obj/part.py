from .instrument import Instrument
from .measure import Measure

class Part():
	def __init__(self, name, id):
		self._name          = name
		self._id 			= id
		self._instruments   = {}
		self._measures 		= []
		print(f'New part : {self.name}')

	def add_instrument(self, inst_name, inst_id):
		if inst_name not in self._instruments:
			self._instruments[inst_id] = Instrument(inst_name, inst_id)

		return self._instruments[inst_id]
	
	def add_measure(self, id, subdivision, bpm, signature):
		"""
		docstring
		"""
		self._measures.append(Measure(id, subdivision, bpm, signature))
		return

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