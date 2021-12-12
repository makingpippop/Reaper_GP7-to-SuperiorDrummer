from inspect import stack
from logging import getLevelName
import sys

from .TheLogging import TheLogging
from .TheLoggingConfig import LEVELS


class TheLogger(TheLogging):
	"""docstring for Logger"""
	def __init__(self, name, getExistingLogger=False, stream=None, file=None):
	
		#Inherit from Logging module
		TheLogging.__init__(self)


		self.logToLogger(f"Initializing Logger for '{name}'", 'INFO')


		#Name of the module (__name__) == absolute path of the DAT
		self.name 		= name

		self.loggerName = self.name
		
		if self.IN_TOUCHDESIGNER:
			#replace "/" by "." and remove the first "." if necessary
			self.loggerName = self._pathToLoggerName(self.name)

		#Get the name of the DAT operator
		self.nickname 	= self.loggerName.split(".")[-1:][0]
		self.defaultLabel = "default"
		
		
		if getExistingLogger:
			self.logToLogger(f"Getting  Logger '{self.loggerName}'", 'INFO')
			self.logger = self.GetLogger(self.loggerName)
			
			if self.logger == None :
				raise NameError('Logger called :', self.loggerName, "doesn't exists")
			
		else:
			#create of get existing logger
			self.logToLogger(f"Creating Logger '{self.loggerName}'", 'INFO')
			self.logger = self.createLogger(self.loggerName)

		#get existing handlers on this logger
		for h in self.logger.handlers:
			#the Handler's attribute _name is stored like so 		 : 	"HandlerType.Label"
			#for readability, in this module we store only the label : 	h._name.split(".")[1]
			self.addHandlerToDict(h, h._name.split(".")[1])

		if not getExistingLogger and stream is not None:
			if stream in LEVELS :
				#hName = self.handlers['StreamHandler']['config']['defaultLabel'].format(self.nickname)
				self.AddStream('stream', severity=stream)
			else:
				self.logToLogger(f"'{stream}' is not a valid severity level", 'CRITICAL')

		if not getExistingLogger and file is not None:
			if file in LEVELS :
				#hName = self.handlers['FileHandler']['config']['defaultLabel'].format(self.nickname)
				self.AddFile('', severity=file)
			else:
				self.logToLogger(f"'{file}' is not a valid severity level", 'CRITICAL')

		self.logToLogger(f"Initialzed Logger for '{name}'", 'INFO')
			
	def Log(self,msg, severity):
		if severity.upper() in LEVELS:
			severityID 	= LEVELS[severity.upper()]['numValue']
			extraDict 	= {'opName':self.nickname}
			#add stack info if enabled for this level
			if LEVELS[severity.upper()]['addStackInfo']:
				extraDict['stackInfo'] = self.buildStackMessage()
			
			# if severityID == 40 and severity == "exception":
			# 	print('EXCEP THE TION!')
			# 	self.logger.exception(msg)
			# else:
			self.logger.log(severityID, msg, extra=extraDict)
			#getattr(self.logger,severity.lower())(msg)

	def UpdateStreamSeverity(self,severity, label=None):
		self.updateHandlerSeverity(label,'StreamHandler', severity)

	def UpdateFileSeverity(self,severity, label=None):
		self.updateHandlerSeverity(label,'FileHandler', severity)
	
	def ListHandlers(self):
		return self.handlers['all']

	def DeleteHandler(self,label):
		if label in self.handlers['all']:
			hType 	= self.handlers['all'][label]
			h 		= self.handlers[hType]['handlers'][label]
			#delete handler
			self.logger.removeHandler(h)
			#remove from dict
			del h
			del hType

	def AddStream(self, label, severity='DEBUG'):
		hLabel = self._buildLabel('StreamHandler',label)
		self.addHandler(hLabel,'StreamHandler', severity,
		#class logging.StreamHandler(stream=None)
						stream=sys.stdout
						)
	
	def AddFile(self, label, severity='DEBUG'):
		hLabel = self._buildLabel('FileHandler',label)
		self.addHandler(hLabel,'FileHandler', severity,
		#class logging.FileHandler(filename, mode='a', encoding=None, delay=False)
						f"{self.logDir}/{hLabel}.log", mode='a', encoding='UTF-8'
						)

	#for parameters : https://docs.python.org/3.7/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler
	def AddTimedFile(self, label, when, interval, backupCount, severity='DEBUG'):
		hLabel = self._buildLabel('TimedRotatingFileHandler',label)
		
		self.addHandler(hLabel,'TimedRotatingFileHandler', severity,
		#class logging.handlers.TimedRotatingFileHandler(filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None)
						f"{self.logDir}/{hLabel}.log", when=when, interval=interval, backupCount=backupCount, encoding=None, delay=False, utc=False, atTime=None
						)


	def addHandler(self, label, hType, severity, *args, **kwargs):
		self.logToLogger(f"Creating {hType} for '{self.name}'", 'INFO')
		if label not in self.handlers['all']:
			self.logToLogger(f"Creating Handler : '{label}'\n\t-  Type : '{hType}'\n\t-  Severity : '{severity}", 'INFO')
			if severity.upper() in LEVELS:
				handler = self.createHandler(self.logger, label, hType, severity, *args, **kwargs)
				self.addHandlerToDict(handler, label)
				self.logToLogger(f"{label} - Created!", 'DEBUG')
			else:
				self.logToLogger(f"Error while creating Handler : '{label}'\n\t-  '{severity}' is not a valid severity level", 'CRITICAL')
		else:
			self.logToLogger(f"Error while creating Handler : '{label}'\n\t-  Already exists", 'DEBUG')

	def getHandler(self, label, hType):
		h = None
		hList = self.handlers[hType]['handlers']
		if label in hList:
			h = hList[label]
		return h

	#add handler to self.handlers based on the handler's class name and label
	def addHandlerToDict(self,handler, label):
		hType = handler.__class__.__name__
		self.handlers[hType]['handlers'][label] = handler
		self.handlers['all'][label] = hType

	def updateHandlerSeverity(self, label, hType, severity):
		#if label is not specified, use the default label
		label = self.handlers[hType]['config']['defaultLabel'].format(self.nickname) if label == None else None

		handler = self.getHandler(label, hType)
		if handler is not None:
			self.changeHandlerLevel(handler, severity)

	def buildStackMessage(self):
		#The first two elements in the stack will be this method
		#and the self.Log method. The last one is also useless (<string> line 1)
		stackMsg 		= '\n\t-> '
		stackInfo 		= stack(0)
		numFrameInfo 	= len(stackInfo)
		for i in range(numFrameInfo-3):
				f = stackInfo[numFrameInfo-2-i]
				stackMsg += f"File '{f.filename}', line {f.lineno}\n\t{' '*3}"
		return stackMsg

	def _buildLabel(self, hType, label):
		#nickname-label_defaultLabel
		preprendStr = f'{self.nickname}-{label}_' if label != "" else f'{self.nickname}_'
		return self.handlers[hType]['config']['defaultLabel'].format(preprendStr)



	@property
	def Name(self):
		return self.loggerName
	



	# def createParamPage(self):
	# 	parentCOMP 	= self.getParentCOMP(op(self.name))
	# 	pageDict 	= {}
	# 	if parentCOMP != None:
	# 		lPage = parentCOMP.appendCustomPage("Logger")

	# 		for hLabel in self.handlers['all']:
	# 			hType 	= self.handlers['all'][hLabel]
	# 			h 		= self.handlers[hType]["handlers"][hLabel]
	# 			hLevelName = getLevelName(h.level)

	# 			if hType not in pageDict:
	# 				pageDict[hType] = {}
	# 			'''
	# 			[('Aheader', OrderedDict([('name', 'Aheader'), ('label', 'AHeader'), ('page', 'Logger'), 
	# 			('style', 'Header'), ('default', ''), ('enable', True), ('startSection', False), 
	# 			('readOnly', False), ('enableExpr', None)])), 
	# 			'''

	# 			#print(TDJ.pageToJSONDict(lPage))
	# 			#self.addHandlerPar(lPage, hLabel, hType, hLevelName)
	# 			#print(hLevelName)
	# 		test = 	{
	# 					'Aheader':
	# 								{
	# 									'name' : 'Aheader',
	# 									'label' : 'AHeader',
	# 									'page'	: 'Autopage',
	# 									'style' : 'Header',
	# 									'default': '',
	# 									'enable' : True,
	# 									'startSection' : False,
	# 									'readOnly': False,
	# 									'enableExpr':None
	# 								},
	# 					'AFloat':
	# 								{
	# 									'name' : 'Afloat',
	# 									'label' : 'Afloat',
	# 									'page'	: 'Autopage',
	# 									'style' : 'Float',
	# 									'default': '',
	# 									'enable' : True,
	# 									'startSection' : False,
	# 									'readOnly': False,
	# 									'enableExpr':None
	# 								}
						
						
	# 				}
	# 		testPage = parentCOMP.appendCustomPage("Autopage")
	# 		TDJ.addParametersFromJSONDict(parentCOMP, test)

		#print()	
	def addParSection(self, page, hType):
		return
	def addHandlerPar(self, page, hLabel, hLevel):
		return
		#header = page.appendHeader(label=hType)

	def _pathToLoggerName(self, opPath):
		loggerName = opPath.replace("/",".")
		loggerName = loggerName[1:] if loggerName[0] == "." else loggerName
		return loggerName
	# def getParentCOMP(self, curOP):
	# 	parentOP = curOP.parent()

	# 	while isinstance(parentOP,baseCOMP) == False and isinstance(parentOP,containerCOMP) == False:
	# 		parentOP = parentOP.parent()
	# 		if parentOP == None:
	# 			break
	# 	return parentOP
	# 		