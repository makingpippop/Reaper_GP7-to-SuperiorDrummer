from .musicxml import MusicXMLError


class ScoreError(MusicXMLError):
	def __init__(self, msg, *args):
		super().__init__(msg, self.__class__.__bases__[0].__name__)


class ScoreNotFound(ScoreError):
	def __init__(self, filePath, logger):
		super().__init__(f"The file '{filePath}' could not be found")


class ScoreFileFormat(ScoreError, FileNotFoundError):
	def __init__(self, logger):
		super().__init__('The score must be a XML')	


class ScoreNotLoaded(ScoreError):
	def __init__(self, logger):
		msg = "The score has not been loaded yet. Please call 'MusicXML.load_score()'"
		logger.Log(msg, 'CRITICAL')
		super().__init__(msg)

class ScoreParsing(ScoreError):
	def __init__(self, filePath, err, logger):
		super().__init__(f"Unexpected error while loading the file:{filePath}\n\t{err}")
