from .beat import Beat

class Rest(Beat):
	def __init__(self, id, part_id, measure_id, inst_obj):
		super().__init__(id, part_id, measure_id, inst_obj)

	def load_attributes(self, *args):
		super().load_attributes(*args)
		last_beats 	= args[2]
		last_beat 	= last_beats['any']
		#dynamic
		self.dynamic = last_beat.dynamic

