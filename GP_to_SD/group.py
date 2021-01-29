from musicxml.obj.part.instrument import Instrument
 
from typing import List


class Group(object):
    def __init__(self, name, score_ref) -> None:
        super().__init__()
        self._score_ref         = score_ref
        self._pitchs            = []
        self._names             = []
        self._ids               = []
        self._instruments       = {}
        self._group_name        = name

    
    def add_instrument(self, inst_obj:Instrument):
        if not isinstance(inst_obj, Instrument):
            raise TypeError('The argument must be time musicxml.obj.Part.Instrument')
        
        self._pitchs.append(inst_obj.pitch)
        self._names.append(inst_obj.name)
        self._ids.append(inst_obj.id)
        self._instruments[f'{inst_obj.pitch}_{inst_obj.name}'] = inst_obj
        pass
    
    def get_notes(self):
        print(list(self._instruments.keys()))
        notes = []
        #loop measures
        for m in self._score_ref.measures:
            print("MEASURE #",m.id)
            notes.append([])
            #loop beats
            for b in m.beats:
                for n in m.beats[b]:
                    print('NOTE #', n.id, " - ", n.instrument.name)
                    inst = n.instrument
                    g_inst_id = f'{inst.pitch}_{inst.name}'
                    if g_inst_id in self._instruments:
                        notes[m.id-1].insert(0,n)
        
        return notes

    def convert_pitchs(self):

        pass

    @property
    def names(self):
        return self._names

    @property
    def pitchs(self):
        return self._pitchs
    
    @property
    def instruments(self):
        return self._instruments
    
    #