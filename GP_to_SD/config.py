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
													'marcato'	: 35,	#hit                                         
												},
					'36_Kick (hit)'             : {  
													'default'   : 35,   #hit   
													'ghost'		: 36, 	#open                                          
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
													'default'   : [64,24],   #open edge 0 || open edge 1
													'marcato'    : 25,   #open edge 1 || open edge 2
													'accent'	: 25
													'ghost'		: [13,14], 	 #open tip 1 || open tip 2
													'tremolo'	: 65, 		#sequenced hits                                      
												},
					'46_Hi-Hat (open)'     		: {  
													'default'   : 25,   #open edge 3
													'accent'	: [26,60],
													'marcato'    : [26,60],  	 #open edge 3 || open edge 4
													'ghost'		: [14,15], 	 #open tip 2 || open tip 3
												},
					'44_Pedal Hi-Hat (hit)'		: {  
													'default'   : 21,   #closed pedal
													'accent'	: 23, 	#open pedal
												},

					#RIDE -----------------------------------------------------------------------------------
					'51_Ride (edge)'  			: {  
													'default'   : 29,   #bow shank
													'accent' 	: 59 	#edge
												},
					'51_Ride (middle)'			: {  
													'default'   : 51,   #bow tip
													'accent' 	: 29 	#bow shank
												},
					'53_Ride (bell)'  			: {  
													'default'   : 30,   #bell tip
													'marcato' 	: 53 	#bell shank
												},
					'51_Ride (choke)' 			: {  
													'default'   : 118,   #Mute hit
												},
					#CYMBALS ---------------------------------------------------------------------------------
					#SD Cymbal 3
					'55_Splash (hit)'   		: {  
													'default'   : 55,   #bow shank
													'ghost' 	: 96 	#bow tip
												},     
					'55_Splash (choke)'			: {  
													'default'   : 56,   #mute hit
												},
					#SD Cymbal 5   
					'52_China (hit)'    		: {  
													'default'   : 52,   #bow shank
													'ghost' 	: 108 	#bow tip
												},       
					'52_China (choke)'			: {  
													'default'   : 54   #mute hit
												},
					#SD Cymbal 2    
					'49_Crash high (hit)'    	: {  
													'default'   : 49,   #bow shank
													'ghost' 	: 27 	#bow tip
												},
					'49_Crash high (choke)'		: {  
													'default'   : 50,   #mute hit
												},
					#SD Cymbal 4
					'57_Crash medium (hit)'  	: {  
													'default'   : 57,   #bow shank
													'ghost' 	: 31 	#bow tip
												},
					'57_Crash medium (choke)'	: {  
													'default'   : 58,   #mute hit
												},

				}

#how much velocity to add to the default
MODIFIERS =     {	
					#will remove
					'ghost'		: 	{
										'default' 	: [12,18],
										'Snare'		: 	{
															'default' :[25,50],
														}
									},
									
					#will add
					'accent'    : 	{
										'default'	: [4,9]
									},
					'marcato'   :	{
										'default'	: [8,15]
									},
				}

VELOCITIES =    {
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
					'Snare'			: {

											'38_Snare (hit)'		:		{	
																				'ppp'	: [15, 30],
																				'pp'	: [39, 57],
																				'p'		: [55, 75],
																				'mp'	: [80, 98],
																				'mf'    : [99,113],
																				'f'		: [107,115],
																				'ff'	: [112, 121],
																				'fff'	: [120, 127]
																			},
											'38_Snare (rim shot)'   :     	{	
																				'ppp'	: [17, 35],
																				'pp'	: [40, 52],
																				'p'		: [54 ,70],
																				'mp'	: [74, 86],
																				'mf'    : [100,110],
																				'f'     : [108,119],
																				'ff'    : [116,124],
																				'fff'   : [125, 127]
																			},
											'53_Ride (bell)'		:		{
																				'mf'    : [85,103],
																				'f'     : [104,112],
																				'ff'    : [113,120],
																				'fff'   : [120, 127]
																			}
										}
				}