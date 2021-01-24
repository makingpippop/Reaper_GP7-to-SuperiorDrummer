from .measure 	import Measure
from .part		import Part

class Score(object):
	def __init__(self, title, score_xml) -> None:
		print('Creating Score :', title)
		self.score_xml 		= score_xml
		self._title         = title
		self._composers     = []
		self._software      = ""
		self._date          = ""

		self._part_list 	= []
		self._parts = {}
		
	def load_parts(self):
		xml_part_list = self.score_xml.find("part-list")
		#PART LIST ------------------------------------------------------------------------------
		#loop <part-list> for saving info on each track
		for p in xml_part_list:
			part_name 	= p.find("part-name").text
			part_id 	= p.get("id")
			#create obj
			part = Part(part_name, part_id, p)
			part.load_instruments()
			#save obj
			self._part_list.append([part_name,part_id])
			self._parts[part_id] = part
		
		#save measure info
		xml_part_measures = self.score_xml.findall("part")
		for p in xml_part_measures:
			p_id = p.get("id")
			part = self._parts[p_id]
			part.set_measure_xml(p)

	def load_notations(self):
		#find all the <part> for getting info on each track
		xml_parts 	= self.score_xml.findall("part")
		#if there's no track
		if len(xml_parts) == 0 :
			return
		#get measure info from the first part
		xml_measures 		= xml_parts[0].findall("measure")
		last_bpm 			= None
		last_signature 		= None
		last_subdivision 	= None
		#loop the <part><measure> to get info on the measure
		for m in xml_measures:
			m_id = int(m.get("number"))
			measure = Measure(m_id, m)
			#get time signature, use signature from last measure if there's no info provided
			signature = measure.load_measure_signature(m)
			signature = last_signature if signature == None else signature
			#get measure smallest subdivision and, use subdivision from last measure if no info is provided
			subdivision = measure.load_measure_division(m)
			subdivision = last_subdivision if subdivision == None else subdivision
			#get bpm, use bpm from last measure if no info is provided
			bpm = measure.load_measure_bpm(m)
			bpm = last_bpm if bpm == None else bpm
			#apply to measure
			measure.bpm 		= bpm
			measure.signature 	= signature
			measure.subdivision = subdivision
			#save for next measures
			last_bpm 			= bpm
			last_signature 		= signature
			last_subdivision 	= subdivision

			#print(f'MEASURE #{measure.id} | {measure.signature[0]}/{measure.signature[1]} | {measure.bpm} bpm | 1/{measure.subdivision}')
			#add measure to parts
			for p in self._parts:
				p.add_measure(measure)
		







	# def add_measure(self, id, subdivision, bpm, signature):
	# 	return
	
	# def add_part(self, name, id):
	# 	pass
