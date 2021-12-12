import logging


LEVELS = 	{
				'NOTSET' 	: {'numValue':0, 'addStackInfo':False},
				'DEBUG'		: {'numValue':10, 'addStackInfo':False},
				'INFO'		: {'numValue':20, 'addStackInfo':False},
				'WARNING' 	: {'numValue':30, 'addStackInfo':False},
				'ERROR' 	: {'numValue':40, 'addStackInfo':True},
				'CRITICAL'	: {'numValue':50, 'addStackInfo':True},
				'EXCEPTION' : {'numValue':40, 'addStackInfo':False}
			}

#this class give the possibility to change the formater after initialisation 
class AdaptiveFormatter(logging.Formatter):
	def __init__(self, fmts, datefmt=None):
		self._level_formatters = {}
		for level, strFormat in fmts.items():
			if level != 'default':
				self._level_formatters[level] = logging.Formatter(fmt=strFormat, datefmt=datefmt)

			super().__init__(fmt=fmts['default'], datefmt=datefmt)

	def format(self, record):
		if record.levelno in self._level_formatters:
			return self._level_formatters[record.levelno].format(record)

		return super().format(record)

#if the logging level is not specified, it will use the ['default'] value
'''
templateFormatter = {
						'default'		: '# %(asctime)s | %(levelname)-8s -> %(message)s',
						logging.DEBUG 	: '',
						logging.INFO 	: '',
						logging.WARNING : '',
						logging.ERROR 	: '',
					
	
					}
'''
streamFormatter = {
						'default'		: '%(opName)s:%(levelname)-8s -> %(message)s',
						logging.ERROR 	: '%(opName)s:%(levelname)-8s -> %(message)s %(stackInfo)s',
						logging.CRITICAL: '%(opName)s:%(levelname)-8s -> %(message)s %(stackInfo)s',
					}

fileFormatter = {
						'default'		: '# %(asctime)s | %(levelname)s\n\t-> %(message)s',
						logging.WARNING : '# %(asctime)s | %(levelname)s\n\t-> %(message)s %(stackInfo)s',
						logging.ERROR 	: '# %(asctime)s | %(levelname)s\n\t-> %(message)s %(stackInfo)s',
						logging.CRITICAL: '# %(asctime)s | %(levelname)s\n\t-> %(message)s %(stackInfo)s'
					}

#Logging module formatters
projectFormatter = {
					'default'		: '# %(asctime)s | %(levelname)s\n\t%(name)s\n\t-> %(message)s',
					logging.WARNING : '# %(asctime)s | %(levelname)s\n\t%(name)s\n\t-> %(message)s %(stackInfo)s',
					logging.ERROR 	: '# %(asctime)s | %(levelname)s\n\t%(name)s\n\t-> %(message)s %(stackInfo)s',
					logging.CRITICAL: '# %(asctime)s | %(levelname)s\n\t%(name)s\n\t-> %(message)s %(stackInfo)s'
				}
defaultProjectFileFormatter 	= AdaptiveFormatter(projectFormatter)
defaultLoggingFileFormatter 	= AdaptiveFormatter(fileFormatter)




CONFIG = {
			'defaultProjectLoggers':{
								"projectFileFormatter" : defaultProjectFileFormatter,
								"LoggingFileFormatter" : defaultLoggingFileFormatter
							},
			'StreamHandler':{
								'config':{
											'defaultLabel': '{0}Stream',
											'defaultFilter': None,
											'defaultFormatter' : AdaptiveFormatter(streamFormatter) 
										},
								'handlers':{}
							},



			'FileHandler':{
								'config':{
											'defaultLabel': '{0}Logs',
											'defaultFilter': None,
											'defaultFormatter' : AdaptiveFormatter(fileFormatter)  
										},
								'handlers':{}
							},



			'SMTPHandler':{
								'config':{
											'defaultLabel': '{0}SMTP',
											'defaultFilter': None,
											'defaultFormatter' : AdaptiveFormatter(fileFormatter)  
										},
								'handlers':{}
							},



			'TimedRotatingFileHandler':{
								'config':{
											'defaultLabel': '{0}TimedLogs',
											'defaultFilter': None,
											'defaultFormatter' : AdaptiveFormatter(fileFormatter)  
										},
								'handlers':{}
							},



			'RotatingFileHandler':{
								'config':{
											'defaultLabel': '{0}RotatingLogs',
											'defaultFilter': None,
											'defaultFormatter' : AdaptiveFormatter(fileFormatter)  
										},
								'handlers':{}
							},



			'SocketHandler':{
								'config':{
											'defaultLabel': '{0}Socket',
											'defaultFilter': None,
											'defaultFormatter' : AdaptiveFormatter(fileFormatter)  
										},
								'handlers':{}
							},



			'DatagramHandler':{
								'config':{
											'defaultLabel': '{0}Datagram',
											'defaultFilter': None,
											'defaultFormatter' : AdaptiveFormatter(fileFormatter)  
										},
								'handlers':{}
							}


		}



		
