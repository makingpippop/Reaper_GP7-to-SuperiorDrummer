from musicxml.obj.score import Score

from .group import Group
from .config import GROUPS as instrument_group_config

class GP_to_SD3(object):
    def __init__(self, score_obj:Score) -> None:
        super().__init__()
        self._score_ref     = score_obj
        self._groups        = {}

        #using config, prepare groups
        self.create_groups()

    def create_groups(self):
        part_inst = self._score_ref.parts['P1'].instruments
        
        #for every group
        for group_name in instrument_group_config:
            g = self._create_group(group_name)
            g_info_dict = instrument_group_config[group_name]
            g_info = self._get_config_group_info(g_info_dict)
            # print('GROUP :', group_name)
            #for every instrument in the part
            for inst_id in part_inst:
                #get instrument infos
                inst_obj = part_inst[inst_id]
                inst_name = inst_obj.name.lower()
                inst_pitch  = int(inst_obj.pitch)
                #if the name if the instrument is in the group
                if inst_name in g_info['names']:
                    name_index = g_info['names'].index(inst_name)
                    #if the name matches the 
                    if g_info['pitchs'][name_index] == inst_pitch:
                        #print('ADDING :',inst_name, inst_pitch)
                        g.add_instrument(inst_obj)
                        g_info['names'].pop(name_index)
                        g_info['pitchs'].pop(name_index)
                        continue
                #if the group is complete
                if not len(g_info['names']):
                    break
        pass

    
    def _create_group(self, group_name):
        if group_name not in self._groups:
            self._groups[group_name] = Group(group_name, self._score_ref)
        
        return self._groups[group_name]

    def _get_config_group_info(self, group_config):
        g_inst_name = []
        g_inst_pitch = []
        for i in group_config:
            g_inst_name.append(i['GP_inst_name'].lower())
            g_inst_pitch.append(i['GP_pitch'])
        return {'names' : g_inst_name, 'pitchs' : g_inst_pitch}

    
    @property
    def groups(self):
        return self._groups