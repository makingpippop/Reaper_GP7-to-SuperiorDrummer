from typing import Type


class Beat(object):
    def __init__(self, id, part_id, inst_obj):
        #chronological id in the measure (for the specified instrument)
        self.type       = self.__class__.__name__
        self._id        = id
        #part containing this note
        self._part      = part_id
        #instrument making the note
        self._inst      = inst_obj

        #choronological id in voice layer
        self.voice_id   = None
        #position in the measure (0.0 -> 1.0) 
        self._position  = 0
        #duration, in relation a the measure length (0.0 -> 4.0)
        self._duration  = None
        # self._duration_name    = None
        # self.duration_name_to_ratio = {  
        #                             'whole'     : 4,
        #                             'half'      : 2,
        #                             'quarter'   : 1,
        #                             'dotted-eight' : 0.75,
        #                             'eighth'    : 1/2,
        #                             '16th'      : 1/16,
        #                             '32nd'      : 1/32,
        #                             '64th'      : 1/64
        #                          }
        #is this a tuplet (triplet, quintuplet, sextuplet ...)
        self._tuplet            = False
        #ratio of note / beat (a triplet is 3:2, quintuplet 5:4)
        self._tuplet_ratio         = None
        #
        self._dotted        = False 
        #text entered in GP
        self._text = None 
    
    def __str__(self) -> str:
        return f'obj.{self.type} ({self._part}:{self._duration})'
    def __repr__(self) -> str:
        return f'obj.{self.type} ({self._part}:{self._duration})'

    # def _set_duration(self, duration_value):
    #     #if we set the duration with a name
    #     if type(duration_value) == str:
    #         duration_value = duration_value.lower()
    #         if duration_value not in self.duration_name_to_ratio:
    #             raise TypeError(f'"{duration_value}" is not a type of beat duration\nThe valid types are : {list(self.duration_name_to_ratio.keys())}')

    #         dur = self.duration_name_to_ratio[duration_value]
    #         self._duration_name = duration_value
    #     else:
    #         if duration_value not in self.duration_name_to_ratio.values():
    #             raise TypeError(f'"{duration_value}" is not a type of beat duration\nThe valid types are : {list(self.duration_name_to_ratio.items())}')
            
    #         dur         = duration_value
    #         dur_name    = [v for v in self.duration_name_to_ratio if self.duration_name_to_ratio[v] == duration_value]
    #         self._duration_name = dur_name

    #     return dur

    @property
    def id(self):
        return self._id
        
    @property
    def instrument(self):
        return self._inst

    @property
    def part_id(self):
        return self._part
    
    @property
    def voice(self):
        return self._voice_id
    @voice.setter
    def voice(self, value):
        self._voice_id = value

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, value):
        self._position = value

    @property
    def duration(self):
        return self._duration
    @duration.setter
    def duration(self, value):
        # dur = self._set_duration(value)
        self._duration = value

    # @property
    # def duration_name(self):
    #     return self._duration_name

    @property
    def tuplet(self):
        return self._tuplet
    @tuplet.setter
    def tuplet(self, value):
        self._tuplet = value

    @property
    def tuplet_ratio(self):
        return self._tuplet_ratio
    @tuplet_ratio.setter
    def tuplet_ratio(self, value):
        self._tuplet_ratio = value

    @property
    def dotted(self):
        return self._dotted
    @dotted.setter
    def dotted(self, value):
        self._dotted = value

    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, value):
        self._text = value
    

