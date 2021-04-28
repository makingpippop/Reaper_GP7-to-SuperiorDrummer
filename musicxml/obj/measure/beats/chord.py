from .beat import Beat


class Chord(Beat):
	"""docstring for Chord"""
	def __init__(self, ref_note_obj):

		super().__init__(id, ref_note_obj.part_id, ref_note_obj.measure, ref_note_obj.instrument)
		self._ref_note = ref_note_obj
		self._notes = [ref_note_obj]

	def __str__(self) -> str:
		instruments = [i.name for i in self.instruments]
		return f'<obj.{self.type}> ({self.part_id}:{self.duration}) ({",".join(instruments)}) '

	def __repr__(self) -> str:
		instruments = [i.name for i in self.instruments]
		return f'<obj.{self.type}> ({self.part_id}:{self.duration}) ({",".join(instruments)}) '
	
	def add_note(self, note_obj):
		self._notes.append(note_obj)


	@property
	def notes(self):
		return self._notes


	@property
	def id(self):
		return self._ref_note.id
	
	
	@property
	def beat(self):
		return self._ref_note.beat

	@property
	def duration(self):
		#return the smallest duration of all the notes in the chord (in case there's a tie)
		return min([n.duration for n in self._notes])	
	
	@property
	def instruments(self):
		return [n.instrument for n in self._notes]
	

	@property
	def voice(self):
		return self._ref_note.voice
	