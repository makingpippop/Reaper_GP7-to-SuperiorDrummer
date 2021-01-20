class Note(object):
    def __init__(self, id):
        #chronological id in the measure
        self._id        = id
        #choronological id in voice layer
        self.voice_id   = None
        #position in the measure (0 -> 1) based on a subdivision of 64
        self._position = 0
        #pppp, ppp, pp, p, mf, ...
        self._dynamic   = ''
        #staccato, accent, marcato
        self._articulation  = ''
        #tremolo indicate that it's a roll
        self._tremolo 		= False
        #
        self._grace 		= False
        #grace with a slash should be before the beat, with no slash, on beat
        self._grace_slash 	= None
        #text entered in GP
        self._text = None 

  
    @property
    def id(self):
        return self._id
