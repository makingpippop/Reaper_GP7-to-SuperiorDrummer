# #COMMENTED = PITCH FROM MUSICXML
# #sidestick, hit, rimshot
# snare_group 	= [37, 38, 38] #[38, 39, 39]
# #hit, open
# bass_drum_group = [36, 35] #[37, 36]
# #hi, med, low, floor1, floor2
# toms_group 		= [48, 47, 45, 50, 43] #[49, 48, 46, 51, 44]
# #closed, half, open, pedal
# hi_hat_group 	= [42, 46, 46, 44] #[43, 47, 47, 45]
# #middle, edge, bell
# ride_group 		= [51, 51, 53] #[52, 52, 54]
# #crash medium, crash high, splash, china
# cymbals_group 	= [57, 49, 55, 52] #[58, 50, 56, 53]


GROUPS =    {
                'Snare'     :   [
                                    {'GP_inst_name' : 'Snare (hit)'         , 'GP_pitch' : 38},
                                    {'GP_inst_name' : 'Snare (side stick)'  , 'GP_pitch' : 37},
                                    {'GP_inst_name' : 'Snare (rim shot)'    , 'GP_pitch' : 38},
                                    {'GP_inst_name' : 'Electric Snare (hit)', 'GP_pitch' : 40}
                                    
                                ],
                'Bass-drum' :   [
                                    {'GP_inst_name' : 'Kick (hit)'         , 'GP_pitch' : 35},
                                    {'GP_inst_name' : 'Kick (hit)'         , 'GP_pitch' : 36}
                                ],
                'Toms'      :   [
                                    {'GP_inst_name' : 'High Tom (hit)'      , 'GP_pitch' : 48},
                                    {'GP_inst_name' : 'Mid Tom (hit)'       , 'GP_pitch' : 47},
                                    {'GP_inst_name' : 'Low Tom (hit)'       , 'GP_pitch' : 45},
                                    {'GP_inst_name' : 'Very Low Tom (hit)'  , 'GP_pitch' : 43},
                                    {'GP_inst_name' : 'High Floor Tom (hit)', 'GP_pitch' : 50},
                                    {'GP_inst_name' : 'Low floor Tom (hit)' , 'GP_pitch' : 41}
                                ],
                'Hi-hat'    :   [
                                    {'GP_inst_name' : 'Hi-Hat (closed)'     , 'GP_pitch' : 42},
                                    {'GP_inst_name' : 'Hi-Hat (half)'       , 'GP_pitch' : 46},
                                    {'GP_inst_name' : 'Hi-Hat (open)'       , 'GP_pitch' : 46},
                                    {'GP_inst_name' : 'Pedal Hi-Hat (hit)'  , 'GP_pitch' : 44}
                                ],
                'Ride'      :   [
                                    {'GP_inst_name' : 'Ride (edge)'         , 'GP_pitch' : 51},
                                    {'GP_inst_name' : 'Ride (middle)'       , 'GP_pitch' : 51},
                                    {'GP_inst_name' : 'Ride (bell)'         , 'GP_pitch' : 53},
                                    {'GP_inst_name' : 'Ride (choke)'        , 'GP_pitch' : 51}
                                ],
                'Cymbals'   :   [
                                    {'GP_inst_name' : 'Splash (hit)'        , 'GP_pitch' : 55},
                                    {'GP_inst_name' : 'Splash (choke)'      , 'GP_pitch' : 55},
                                    {'GP_inst_name' : 'China (hit)'         , 'GP_pitch' : 52},
                                    {'GP_inst_name' : 'China (choke)'       , 'GP_pitch' : 52},
                                    {'GP_inst_name' : 'Crash High (hit)'    , 'GP_pitch' : 49},
                                    {'GP_inst_name' : 'Crash High (choke)'  , 'GP_pitch' : 49},
                                    {'GP_inst_name' : 'Crash Medium (hit)'  , 'GP_pitch' : 57},
                                    {'GP_inst_name' : 'Crash Medium (choke)', 'GP_pitch' : 57},
                                ],
                
            }

