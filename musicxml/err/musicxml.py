#https://julien.danjou.info/python-exceptions-guide/#:~:text=In%20Python%2C%20the%20base%20exception%20class%20is%20named%20BaseException%20.&text=The%20only%20other%20exceptions%20that,builtin%20exceptions%20inherits%20from%20Exception%20.

class MusicXMLError(Exception):
	"""Base class for exceptions in this module."""
	def __init__(self, msg, child_excep):

		if msg is None:
			msg = "MusicXMLError!"

		self.msg = msg
		self.child_excep = child_excep
		super().__init__(msg)

	def __str__(self):
		return f"\n# MusicXMLError -> {self.child_excep}\n\t{self.msg}"
