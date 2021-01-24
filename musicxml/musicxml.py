from pathlib import Path
import os
from sys import exc_info
import xml.etree.ElementTree as ET

from .obj.score import Score

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
		try :
			with open(self.filePath, 'r') as file:
				xmlFile = ET.parse(file)
				rootObj = xmlFile.getroot()
				content = rootObj
		except:
			raise ET.ParseError(f"Unexpected error while loading the file:\n{self.fullPath}\n{exc_info()}")

		return content

	def load_score(self):
		xml_score_title = self.data.find("work/work-title")
		score_name = 'untitled' if xml_score_title == None else xml_score_title.text
		self._score = Score(score_name, self.data)
		self._score.load_parts()
		self._score.load_notations()
		self._score.load_beats()
		return self._score
		"""
		#NOTES ------------------------------------------------------------------------
		#depth layers of guitar pro
		old_voice 	= 1
		old_dynamic = ''
		note_inc 	= 0
		for n in m.findall('note'):
			voice 			= int(n.find('voice').text)
			inst 			= n.find("instrument")
			inst_id 		= None
			rest 			= False
			articulation 	= None
			dynamic 		= 'pppp'
			ghost 			= False
			tremolo 		= False
			grace 			= False
			grace_type 		= None
			
			if inst is not None :
				inst_id = inst.get("id")
			else:
				rest = True if n.find("rest") is not None else False
			
			duration 	= n.find("duration")
			
			if voice != old_voice:
				old_voice = voice
				note_inc = 0
			
			#ADD NOTE HERE
			#part.measures[m_id-1].add_note()
			#n_duration 	= 
		"""
	
	
	@property
	def parts(self):
		return self._parts
	
	@property
	def part_list(self):
		return self._part_list
