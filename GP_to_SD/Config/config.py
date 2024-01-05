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

from .Snare import *
from .Bass_drum import *
from .Toms import *
from .Ride import *
from .Cymbals import *
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
									{'GP_inst_name' : 'Crash high (hit)'    , 'GP_pitch' : 49},
									{'GP_inst_name' : 'Crash high (choke)'  , 'GP_pitch' : 49},
									{'GP_inst_name' : 'Crash medium (hit)'  , 'GP_pitch' : 57},
									{'GP_inst_name' : 'Crash medium (choke)', 'GP_pitch' : 57},
								],
				
			}

#key = [pitch]_[GP_inst_name]
PITCHS     =   {
					#SNARE ----------------------------------------------------------------------------
					'38_Snare (hit)'          :    {  
													'default'   : 38,   #center                                             
													'ghost'     : 125,  #off center
													'grace'     : 125,  #off center
													'tremolo'   : 39    #closed roll
												},
					'38_Snare (rim shot)'     :    {  
													'default'   : 40,   #rimshot                                             
													'ghost'     : 38,   #center
													'grace'     : 38,   #center
													'tremolo'   : 38    #center
												},
					'37_Snare (side stick)'   :    {  
													'default'   : 37,   #sidestick                                             
												},
					'40_Electric Snare (hit)' : {  
													'default'   : 38,   #center                                             
												},
					#BASS DRUM -------------------------------------------------------------------------
					'35_Kick (hit)'             : {  
													'default'   : 36,   #open    
														},
					'36_Kick (hit)'             : {  
													'default'   : 35,   #hit                                           
												},
					#TOMS ------------------------------------------------------------------------------
					#tom 2
					'48_High Tom (hit)'     	: {  
													'default'   : 47,   #center                                             
													'marcato'    : 80,   #rimshot                                         
												}, 
					#tom 3
					'47_Mid Tom (hit)'      	: {  
													'default'   : 45,   #center
													'marcato'    : 78,   #rimshot                                           
												},
					#floor 1
					'45_Low Tom (hit)'      	: {  
													'default'   : 43,   #center
													'marcato'    : 75,   #rimshot                                          
												}, 
					#floor 2
					'43_Very Low Tom (hit)' 	: {  
													'default'   : 41,   #center
													'marcato'    : 73,   #rimshot                                          
												},
					#tom 1 (highest tom on GP!?)
					'50_High Floor Tom (hit)'	: {  
													'default'   : 48,   #center
													'marcato'    : 82,   #rimshot                                           
												},
					'41_Low floor Tom (hit)' 	: {  
													'default'   : 43,   #center
													'marcato'    : 75,   #rimshot                                           
												},
					#HI-HAT ------------------------------------------------------------------------------

					'42_Hi-Hat (closed)'   		: {  
													'default'   : 61,   #closed tip
													'marcato'    : 22,   #closed edge
													'ghost'		: 63, 	#tight tip
													'tremolo'	: 65, 	#sequenced hits                                      
												},
					'46_Hi-Hat (half)'     		: {  
													'default'   : 64,   #open edge 0
													'marcato'   : 24,   #open edge 1
													'accent'	: 24,
													'ghost'		: [13,14], 	 #open tip 1 || open tip 2
													'tremolo'	: 65, 		#sequenced hits                                      
												},
					'46_Hi-Hat (open)'     		: {  
													'default'   : 24,   	#open edge 1
													'accent'	: 25, 		#open edge 2
													'marcato'   : [25,36], 	#open edge 2 || open edge 3
													'ghost'		: [13,14], 	#open tip 1 || open tip 2
												},
					'44_Pedal Hi-Hat (hit)'		: {  
													'default'   : 21,   #closed pedal
													'accent'	: 23, 	#open pedal
												},

					#RIDE -----------------------------------------------------------------------------------
					'51_Ride (edge)'  			: {  
													'default'   : 56,   #bow shank
													'accent' 	: 55 	#edge
												},
					'51_Ride (middle)'			: {  
													'default'   : 57,   #bow tip
													'accent' 	: 56 	#bow shank
												},
					'53_Ride (bell)'  			: {  
													'default'   : 59,   #bell tip
													'marcato' 	: 58 	#bell shank
												},
					'51_Ride (choke)' 			: {  
													'default'   : 54,   #Mute hit
												},
					#CYMBALS ---------------------------------------------------------------------------------
					#SD Cymbal 3
					'55_Splash (hit)'   		: {  
													'default'   : 85,   #bow shank
													'ghost' 	: 86 	#bow tip
												},     
					'55_Splash (choke)'			: {  
													'default'   : 88,   #STAX
												},
					#SD Cymbal 5   
					'52_China (hit)'    		: {  
													'default'   : 109,   #Crash
													'ghost' 	: 111 	#bow tip
												},       
					'52_China (choke)'			: {  
													'default'   : 108   #mute hit
												},
					#SD Cymbal 2    
					'49_Crash high (hit)'    	: {  
													'default'   : 97,   #Crash
													'ghost' 	: 99 	#bow tip
												},
					'49_Crash high (choke)'		: {  
													'default'   : 96,   #mute hit
												},
					#SD Cymbal 4
					'57_Crash medium (hit)'  	: {  
													'default'   : 103,  #Crash
													'ghost' 	: 105 	#bow tip
												},
					'57_Crash medium (choke)'	: {  
													'default'   : 102,   #mute hit
												},

				}



ARTICULATIONS = {
				#default for every instrument
				'default': {
							#mininum dynamic - [min, max]
							'ghost': [12, 18],
											
							#maximum dynamic + [min, max]
							'accent': [4, 9],
							'marcato': [8, 15]
				#Group name
				},
				'Snare'		: SNARE_ARTICULATIONS,
				'Bass-drum'	: BASS_DRUM_ARTICULATIONS,
				'Toms'		: TOMS_ARTICULATIONS,
				'Ride'		: RIDE_ARTICULATIONS,
				'Cymbals'	: CYMBALS_ARTICULATIONS,

					
}

DYNAMICS =    {		#default for every instrument
					'default'		:  {
												'pppp'  : [5,20],
												'ppp'   : [21,35],
												'pp'    : [36,50],
												'p'     : [51,70],
												'mp'    : [71,90],
												'mf'    : [91,106],
												'f'     : [107,113],
												'ff'    : [114,120],
												'fff'   : [121, 127]
									  },
					#group name
					'Snare'			: SNARE_DYNAMICS,
					'Bass-drum'		: BASS_DRUM_DYNAMICS,
					'Toms'			: TOMS_DYNAMICS,
					'Ride'			: RIDE_DYNAMICS,
					'Cymbals'		: CYMBALS_DYNAMICS,

				}