from pathlib import Path
import os
from sys import exc_info
import xml.etree.ElementTree as ET
from musicxml.obj import Part

class MusicXML():
	
	def __init__(self, filePath):
		self.data 		= None
		self.filePath 	= filePath
		self.fullPath 	= None
		self.exec_folder = Path(os.getcwd())

		#objects
		self._part_list = []
		self._parts = {}
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
		#split
		self.split_file()

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

	def split_file(self):
		xml_part_list = self.data.find("part-list")
		#PART LIST ------------------------------------------------------------------------------
		#loop <part-list> for saving info on each track
		for p in xml_part_list:
			part_name 	= p.find("part-name").text
			part_id 	= p.get("id")
			part = Part(part_name, part_id)
			self._part_list.append([part_name,part_id])
		#INSTRUMENTS ------------------------------------------------------------------------
			#loop <part-list><score-instrument> for the list of instrument on this track
			for p_inst in p.findall('score-instrument'):
				id 		= p_inst.get("id")
				name 	= p_inst.find('instrument-name').text
				inst 	= part.add_instrument(name,id)
				#loop the <part-list><midi-instrument> to get more info on the instrument
				for p_midi_inst in p.findall('midi-instrument'):
					midi_inst_id = p_midi_inst.get('id')
					#if the midi instrument ID matches the current track instrument ID
					if id == midi_inst_id:
						inst.midiChannel 	= p_midi_inst.find('midi-channel').text
						inst.pitch 			= p_midi_inst.find('midi-unpitched').text
						inst.volume			= p_midi_inst.find('volume').text
						inst.pan 			= p_midi_inst.find('pan').text
						break
				
			self._parts[part_id] = part
		#PARTS ------------------------------------------------------------------------
		#loop <part> for getting info on each track
		xml_parts = self.data.findall("part")
		for i,p in enumerate(xml_parts):
			part_id 	= p.get("id")
			part 		= self._parts[part_id]
		#MEASURES ------------------------------------------------------------------------
			xml_measures 		= p.findall("measure")
			last_bpm 			= None
			last_signature 		= None
			last_subdivision 	= None
			#loop the <part><measure> to get info on the measure
			for m in xml_measures:
				m_id = int(m.get("number"))
				#get time signature
				signature = self.get_measure_signature(m)
				if signature == None:
					#the first measure should have a time signature
					if m_id == 1:
						raise Exception('Error whithin the file. No time signature on the first measure')
					#save for next measures
					signature = last_signature
				#get measure smallest subdivision and get from last measure if no info is provided
				subdivision = self.get_measure_division(m)
				subdivision = last_subdivision if subdivision == None else subdivision
				#get bpm (only available on first track)
				bpm = None
				#if we are on the first track
				if i == 0:
					bpm = self.get_measure_bpm(m)
					if bpm == None:
						#the first mesure should have a bpm
						if m_id == 1:
							raise Exception('Error whithin the file. No bpm on the first measure')
						bpm = last_bpm
					#save for next measures
					last_bpm = bpm
				#if we are not on the first track, get info from the first track
				else:
					first_part_id 	= self._part_list[0][1]
					first_part 		= self._parts[first_part_id]
					bpm 			= first_part.measures[m_id-1].bpm
					pass
				
				#create measure
				part.add_measure(m_id,subdivision,bpm,signature)
				last_signature 		= signature
				last_subdivision 	= subdivision
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
				
	
	def get_measure_signature(self, xml_measure):
		signature = None
		m_time_attr = xml_measure.find('attributes/time')

		if m_time_attr is not None :
			beat = int(m_time_attr.find("beats").text)
			beat_sub = int(m_time_attr.find("beat-type").text)
			signature = [beat, beat_sub]
		
		return signature

	def get_measure_bpm(self, xml_measure):
		bpm = None
		metronome_attr = xml_measure.find('./direction/direction-type/metronome')
		if metronome_attr is not None :
			bpm = int(metronome_attr.find("per-minute").text)
	
		return bpm
	
	def get_measure_division(self, xml_measure):
		subdivision		= None
		m_division_attr = xml_measure.find('attributes/divisions')
		if m_division_attr is not None :
			subdivision = int(m_division_attr.text)
		return subdivision
	@property
	def parts(self):
		return self._parts
	
	@property
	def part_list(self):
		return self._part_list
