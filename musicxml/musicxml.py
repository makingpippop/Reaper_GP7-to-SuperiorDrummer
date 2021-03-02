from pathlib import Path
import os
from sys import exc_info
import xml.etree.ElementTree as ET
from .obj import Score


class MusicXML():
	
	def __init__(self, filePath):
		self.data 		= None
		self.filePath 	= filePath
		self.fullPath 	= None
		self.exec_folder = Path(os.getcwd())

		
		#objects
		self._score 	= None
		self.openFile()

	def openFile(self):
		#combine filepath to current directory
		p = self.exec_folder / Path(self.filePath)
		self.fullPath = p.as_posix()
		#check if file exists
		if not p.exists():
			raise FileNotFoundError(f"The file '{self.fullPath}' could not be found")
		#make sure it's a XML
		if p.suffix.lower() != ".xml":
			raise TypeError('The file must be a XML')
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
			raise ET.ParseError(f"Unexpected error while loading the file:\n{self.fullPath}\n{exc_info()}")

		return content

	def load_score(self):
		xml_score_title = self.data.find("work/work-title")
		score_name = 'untitled' if xml_score_title is None else xml_score_title.text
		self._score = Score(score_name, self.data)
		self._score.load_parts()
		#create Measures
		self._score.load_notations()
		self._score.load_beats()
		return self._score


	@property
	def parts(self):
		return self._parts
	
	@property
	def part_list(self):
		return self._part_list

	@property
	def score(self):
		return self._score

