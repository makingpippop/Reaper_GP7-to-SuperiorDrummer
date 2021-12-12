import os
from sys import exc_info
from pathlib import Path
import xml.etree.ElementTree as ET


from .obj import Score
from .err import *
from the_logger import TheLogger


class MusicXML():
	
	def __init__(self, filePath):
		self.logger = TheLogger(__name__, stream='INFO', file='INFO')

		self.data 			= None
		self.filePath 		= filePath
		self.fullPath 		= None
		self.exec_folder 	= Path(os.getcwd())

		
		#objects
		self._score = None
		self.openFile()

	def openFile(self):
		#combine filepath to current directory
		p = self.exec_folder / Path(self.filePath)
		self.fullPath = p.as_posix()
		self.logger.Log(f"Getting the file : {self.fullPath}", 'INFO')
		#check if file exists
		if not p.exists():
			raise ScoreNotFound(self.fullPath)
		#make sure it's a XML
		if p.suffix.lower() != ".xml":
			raise ScoreFileFormat
		#load data
		self.data = self.loadXML()
		
	def loadXML(self):
		content = None
		try:
			with open(self.filePath, 'r') as file:
				xmlFile = ET.parse(file)
				rootObj = xmlFile.getroot()
				content = rootObj
		except ET.ParseError:
			raise ScoreParsing(self.fullPath, exc_info())

		return content

	def load_score(self):
		xml_score_title = self.data.find("work/work-title")
		#set default name of the score if not set
		score_name = 'untitled' if xml_score_title is None else xml_score_title.text
		#create Score object
		self._score = Score(score_name, self.data)
		self._score.load_parts()
		#create Measures
		self._score.load_notations()
		self._score.load_beats()
		return self._score


	@property
	def score(self):
		if not self._score:
			raise ScoreNotLoaded(self.logger)
		return self._score

