from .note import Note

class Measure(object):
    def __init__(self, id, subdivision, bpm, signature):
        self._id            = id
        self._bpm           = bpm
        self._signature     = signature
        self._subdivision   = subdivision
        self._notes         = []

        print(f'NEW MEASURE #{id} | {subdivision} | {bpm} bpm | {signature[0]}/{signature[1]}')

    def add_note(self):
        
        return

    @property
    def id(self):
        return self._id
    @property
    def bpm(self):
        return self._bpm
    @property
    def signature(self):
        return self._signature
    @property
    def subdivision(self):
        return self._subdivision