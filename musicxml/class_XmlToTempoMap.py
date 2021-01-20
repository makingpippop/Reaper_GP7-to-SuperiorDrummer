from GP5Xml_parser import GP5XmlParser as GPXml

class XMLToTempoMap():
	"""docstring for XMLToTempoMap"""
	def __init__(self, owner):
		self.owner 		= owner
		self.tempoMap 	= op("tempo_map")
		self.tempoMap.clear(keepFirstRow=True)

		self.gpXML 		= GPXml(f"{project.folder}/Data/What-Remains_XML_v1.xml").Data

		self.getSongInfos()

	def getSongInfos(self):
		partInfo = self.gpXML.find('part')
		measures = list(partInfo)
		oldMeasuresInfo = {'mBeat':None, 'mSub':None, 'length':None}
		lastBeatChange = 1
		for i,m in enumerate(measures):
			mID 	= m.get("number")
			timeTag = m.find("attributes").find("time")
			lastFrame = False if i != len(measures)-1 else True
			
			if timeTag != None:
				mBeat 		= timeTag.find("beats").text
				mSub  		= timeTag.find("beat-type").text
				mNbMeasure 	= lastBeatChange
				#if first measure
				if i == 0:
					oldMeasuresInfo = {'mBeat':mBeat, 'mSub':mSub, 'length':mNbMeasure}
					continue


				#if the time signature changed
				if mBeat != oldMeasuresInfo['mBeat'] or mSub != oldMeasuresInfo['mSub']:
					oldBeat = oldMeasuresInfo['mBeat']
					oldSub = oldMeasuresInfo['mSub']

					self.tempoMap.appendRow([oldBeat, oldSub, mNbMeasure])
					#save new signature
					oldMeasuresInfo = {'mBeat':mBeat, 'mSub':mSub, 'length':mNbMeasure}
					lastBeatChange = 1
				else:
					lastBeatChange+=1
				
			else:
				lastBeatChange+=1

			if lastFrame:
				oldBeat = oldMeasuresInfo['mBeat']
				oldSub = oldMeasuresInfo['mSub']

				self.tempoMap.appendRow([oldBeat, oldSub, lastBeatChange])


			
		#print(list(partInfo))
