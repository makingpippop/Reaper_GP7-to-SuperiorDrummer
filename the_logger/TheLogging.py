import logging, logging.handlers
from pathlib import Path
from copy import deepcopy

from .TheLoggingConfig import CONFIG, LEVELS



class TheLogging:
	"""docstring for Logger"""
	def __init__(self):

		self.IN_TOUCHDESIGNER = True
		logsDir 	= "."
		projectName = "Project-logs"

		try :
			var('TOUCHBUILD')
			logsDir 		= project.folder
			#project filename without the version and the .toe extension
			projectName 	= project.name.split(".")[:-2]
			projectName 	= ".".join(projectName)
		except NameError:
			self.IN_TOUCHDESIGNER = False


		self.handlers = deepcopy(CONFIG)
		self.handlers['all'] = {}
		
		#The logs will be saved in a subfolder located
		#in TD 		: Where the project (.toe) is located
		#in Python 	: Where the script has been launched
		self.logDir 		= self.createLogDir(logsDir)

		self.loggingLogger 	= logging.getLogger("Logging-logger")

		
		self.projectName 	= projectName
		

		self.projectLogger 	= logging.getLogger("Logging")

		self.loggingLogger.setLevel(logging.DEBUG)
		self.projectLogger.setLevel(logging.INFO)

		
		
		#if the project logger has no handler
		if not self.projectLogger.hasHandlers():
			#create handlers
			fileHandler = logging.FileHandler(f"{self.logDir}/_{self.projectName}.log")
			fileHandler.setFormatter(CONFIG["defaultProjectLoggers"]['projectFileFormatter'])
			#set severity
			fileHandler.setLevel(logging.INFO)
			#apply to main logger
			self.projectLogger.addHandler(fileHandler)

		if not self.loggingLogger.hasHandlers():
			fileHandler = logging.FileHandler(f"{self.logDir}/_{self.projectName}_Logging-module.log")
			fileHandler.setFormatter(CONFIG["defaultProjectLoggers"]['LoggingFileFormatter'])
			fileHandler.setLevel(logging.DEBUG)
			self.loggingLogger.addHandler(fileHandler)


	def createLogDir(self, projectFolder):
		logDir=None
		try :
			logDir = Path(f"{projectFolder}/Logs")
			#create all directories in the path if they do not exists
			logDir.mkdir(parents=True, exist_ok=True)
		except:
			print("Logging ERROR : Unexpected error while creating the logging directory:", sys.exc_info()[0])
			raise
		finally:
			return logDir

	def logToProject(self, msg, severity):
		self.projectLogger.log(LEVELS[severity.upper()]['numValue'], msg)

	def logToLogger(self, msg, severity):
		self.loggingLogger.log(LEVELS[severity.upper()]['numValue'], msg)

	def ChangeLevel(self, level):
		self.projectLogger.setLevel(level)

	def changeHandlerLevel(self, handler, level):
		try:
			handler.setLevel(level.upper())
			print('Updated', handler._name,'to level :',level.upper())
		except ValueError:
			print("Logging level '",level,"' does not exists")

			


	def createLogger(self, loggerName):
		
		logger 	= self.projectLogger.getChild(loggerName)
		logger.setLevel(logging.DEBUG)
		return logger

	def createHandler(self,logger, label, handlerType, severity, *args, **kwargs):
		#loop all the handlers of this Logger and validate that the _name attribute does not already exists
		for h in logger.handlers:
			if h._name == f"{handlerType}.{label}":
				return h

		if handlerType == 'StreamHandler' or handlerType == 'FileHandler':
			handler = getattr(logging,handlerType)(*args, **kwargs)
		else:
			handler = getattr(logging.handlers ,handlerType)(*args, **kwargs)

		handler.setLevel(LEVELS[severity.upper()]['numValue'])
		
		configDict 	= self.handlers[handlerType]['config']
		#hFilter 	= configDict["defaultFilter"](opName)
		hFormatter 	= configDict['defaultFormatter']

		#handler.addFilter(hFilter)
		handler.setFormatter(hFormatter)
		
			
		#set _name attribute
		handler._name = f"{handlerType}.{label}"
		#apply handler to logger
		logger.addHandler(handler)

		return handler


	def GetLevel(self):
		return self.projectLogger.getEffectiveLevel()

	def GetLogger(self,name):
		existingLogger = self.projectLogger.getChild(name)
		hasHandlers = True if len(existingLogger.handlers) else False
		return existingLogger if len(existingLogger.handlers) else None

	def GetLoggersList(self):
		return [logging.getLogger(name) for name in logging.root.manager.loggerDict]


