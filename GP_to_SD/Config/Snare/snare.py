#adds or remove velocity value
ARTICULATIONS = {
					'default': {
									#works for F, but not MF or MP
									'ghost'   : [30, 48], #mininum dynamic -
									'accent'  : [0, 7],   #maximum dynamic +
									'marcato' : [3, 12]	  #maximum dynamic +
					},
					#instrument name : [pitch]_[GP_inst_name]
					# '38_Snare (hit)': {
					# 				'ghost'   : [10, 15], #mininum dynamic -
					# 				'accent'  : [4, 8],   #maximum dynamic +
					# 				'marcato' : [0, 2]	  #maximum dynamic +
					# },

}

DYNAMICS = {
					'default': {},
					#instrument name : [pitch]_[GP_inst_name]
					'38_Snare (hit)': {
									'ppp'	: [1, 15],
									'pp'	: [20, 38],
									'p'		: [40, 60],
									'mp'	: [62, 74],
									'mf'	: [75, 88],
									'f'		: [102, 113],
									'ff'	: [113, 120],
									'fff'	: [121, 127]

					}, '38_Snare (rim shot)': {
									'ppp'	: [1, 15],
									'pp'	: [40, 52],
									'p'		: [54, 70],
									'mp'	: [74, 86],
									'mf'   	: [106, 111],
									'f'    	: [113, 118],
									'ff'   	: [116, 120],
									'fff'  	: [121, 127]
					},
}