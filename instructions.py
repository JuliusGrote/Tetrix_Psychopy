# This file contains the class for instructions based on the language defined in "config_paradigm_psychopy.txt"
# Is executed as a python script, so it if necessary alter the instruction texts inside the '...' but not the structure of the code!

class Instructions:
	## Check what is given in the config files and set instuctions accordingly.
	## naming is so that a "font" is used in a text stimulus in PsychoPy while stimuli that are used as images are "img" here
	def set_instructions(self,
					     language,
						 N_repeats,
						 play_Tetris_Duration,
						 motor_control_duration,
					  	 watch_Tetris_duration,
					  	 fixation_cross_duration):
		# since "font_explain_trials's" f-string uses interger calculation, if "main_trials" are disabled in the config N_repeats must be "0" instead of "None"...
		if N_repeats == None:
			N_repeats = 0
			
		# get amount of enabled conditions
		enabled_conditions = len([condition for condition in [play_Tetris_Duration, motor_control_duration, watch_Tetris_duration, fixation_cross_duration] if condition != 0 and condition is not None])
		
		# Language-specific instruction dictionaries
		instructions_dict = {
			'German': {
				'font_check_response': 'Bitte drücken Sie jede Taste der Responsebox zwei mal!',
				'font_check_response_2': 'Responsebox erfolgreich gecheckt!',
				'font_Intro_2': 'Willkommen zum Tetris-Experiment!',
				'font_continue': 'Beliebige Taste drücken, um fortzufahren!',
				'font_explanation_pretrial': 'Während diesem ersten Teil des Experiments werden Sie Tetris spielen und sich an das Setup gewöhnen! Die Level, die Sie in diesen ersten Runden erreichen, legen fest, welches Level Sie im Hauptteil spielen!',
				'font_how_to_play': 'Wie man Tetris spielt:',
				'img_explain_game_mechanics_1': 'Images/explain_game_mechanics_1_de.png',
				'img_explain_game_mechanics_2': 'Images/explain_game_mechanics_2_de.png',
				'img_explain_game_mechanics_3': 'Images/explain_game_mechanics_3_de.png',
				'font_explain_staircase': 'Bitte beachten Sie, dass in diesen ersten Runden das LEVEL, auf das Sie nach GAME OVER zurückgesetzt werden VARIIERT!',
				'img_explain_controls': 'Images/explain_controls_de.png',
				'font_Controls': 'So bewegen Sie die Tetris-Blöcke:',
				'font_start_pretrial': 'Beliebige Taste drücken, um das erste TETRIS-Spiel zu starten!',
				'font_pause_n_sec': 'Pause!',
				'font_intro_main': 'Jetzt beginnt der Hauptteil des Experiments!',
				'font_intro_structure': 'So ist das Experiment aufgebaut:',
				'font_Announcement': f'Während des Experiments werden Sie {enabled_conditions} verschiedene Symbole sehen:',
				'font_play_Tetris': 'Controller: Spielen Sie Tetris! Versuchen Sie vor Ihrem INNEREN AUGE zu VISUALISISEREN, wo der DERZEITIGE Tetris-Block und die NEXT (nächsten) Blöcke am besten hinpassen! Zwischen zwei Tetris-Teilen wird das Spiel IM HINTERGRUND PAUSIERT!',
				'font_explain_comp_load': 'Achtung! In jedem Tetris-Teil wird zufällig gewählt, ob es EIN oder DREI "Next-Blöcke" gibt.',
				'font_explain_comp_speed': 'Achtung! In jedem Tetris-Teil wird zufällig gewählt, ob in einem HÖHEREN (schnelleren) oder TIEFEREN (langsameren) Level gespielt wird!',
				'font_motor': 'Tastendruck: Drücken Sie die Tasten ABWECHSELND zum Rhythmus, der auf dem Bildschirm zu sehen ist!',
				'font_watch': 'Auge: Schauen Sie Tetris zu! Schauen Sie einfach nur zu, während eine Spiel-Aufzeichnung für Sie gespielt wird. Bitte Drücken Sie KEINE Tasten!',
				'font_cross': 'Fixationskreuz: Schauen Sie einfach das Kreuz in der Bildschirmmitte an und machen Sie nichts Anderes!',
				'font_explain_trials_equal': f'Jede Wiederholung startet mit einem Teil TETRIS SPIELEN, gefolgt von einem zufällig gewählten Teil TETRIS ZUZUSCHAUEN, TASTENDRÜCKEN oder FIXATIONSKREUZ! Jeder Teil dauert {play_Tetris_Duration} Sekunden und es gibt {int(N_repeats) * 3} Wiederholungen!',
				'font_explain_trials_unequal': f'Jede Wiederholung startet mit einem Teil TETRIS SPIELEN\n({play_Tetris_Duration} Sekunden), gefolgt von einem zufällig gewählten Teil TETRIS ZUZUSCHAUEN ({watch_Tetris_duration} Sekunden), TASTENDRÜCKEN\n({motor_control_duration} Sekunden) oder FIXATIONSKREUZ ({fixation_cross_duration} Sekunden)! Es gibt {int(N_repeats) * 3} Wiederholungen!',
				'font_start': 'Jetzt beginnt das Experiment!',
				'font_condition_ended': 'Teil beendet',
				'font_end': 'Vielen Dank für Ihre Teilnahme!',
			},
			'English': {
				'font_check_response': 'Please press each button on the responsebox twice!',
				'font_check_response_2': 'Responses checked successfully',
				'font_Intro_2': 'Welcome to the Tetris experiment!',
				'font_continue': 'Press any button to continue!',
				'font_explanation_pretrial': 'During this first part of the experiment, you will play Tetris and get used to the setup! The levels you reach in these first rounds will determine the level you play in the main part of the experiment!',
				'font_how_to_play': 'Here is how to play Tetris:',
				'img_explain_game_mechanics_1': 'Images/explain_game_mechanics_1_en.png',
				'img_explain_game_mechanics_2': 'Images/explain_game_mechanics_2_en.png',
				'img_explain_game_mechanics_3': 'Images/explain_game_mechanics_3_en.png',
				'font_explain_staircase': 'Please note that in these first rounds, the LEVEL that you will be put back to after GAME OVER VARIES!',
				'img_explain_controls': 'Images/explain_controls_en.png',
				'font_Controls': 'This is how you move the Tetris-Blocks:',
				'font_start_pretrial': 'Press any button to start the first TETRIS-GAME!',
				'font_pause_n_sec': 'Rest!',
				'font_intro_main': 'Now the main part of the experiment begins!',
				'font_intro_structure': 'This is how the experiment is structured:',
				'font_Announcement': f'During the experiment you will encounter {enabled_conditions} different symbols:',
				'font_play_Tetris': "Controller: Play Tetris! Try to VISUALIZE in your MIND'S EYE where the CURRENT Tetris block and the NEXTs blocks fit best! Between two Tetris parts the game is PAUSED in the BACKGROUND!",
				'font_explain_comp_load': 'Note! In each Tetris part, it is randomly chosen, whether there will be ONE or THREE "Next" blocks.',
				'font_explain_comp_speed': 'Note! In each Tetris part, it is randomly chosen, whether you will play in a HIGHER (faster) or LOWER (slower) level!',
				'font_motor': 'Button press: Press the Buttons ALTERNATELY (one after another) to the rhythm displayed on the screen!',
				'font_watch': 'Eye: Watch Tetris! Just watch while a game recording is played for you. Please DO NOT press any buttons!',
				'font_cross': 'Fixation Cross: Just look at the cross in the middle of the screen and do nothing else!',
				'font_explain_trials_equal': f'Each repetition starts with a round of PLAYING TETRIS followed by a randomly chosen part of WATCHING TETRIS GAMEPLAY, BUTTON PRESSES or FIXATION CROSS! Each part lasts {play_Tetris_Duration} seconds and there are {N_repeats * 3} repetitions!',
				'font_explain_trials_unequal': f'Each repetition starts with a round of PLAYING TETRIS\n({play_Tetris_Duration} seconds) followed by a randomly chosen part of WATCHING TETRIS GAMEPLAY ({watch_Tetris_duration} seconds), BUTTON PRESSES\n({motor_control_duration} seconds) or FIXATION CROSS ({fixation_cross_duration} seconds)! There are {N_repeats * 3} repetitions!',
				'font_start': 'Now, the experiment starts!',
				'font_condition_ended': 'Part ended',
				'font_end': 'Thank you for your Participation!',
			}
		}
		
		# Select appropriate language dictionary (default to English if not found)
		lang_dict = instructions_dict.get(language, instructions_dict['English'])
		
		# Set all attributes from the language dictionary
		for attr_name, attr_value in lang_dict.items():
			setattr(self, attr_name, attr_value)
		
		# Choose the correct explain_trials based on whether durations are equal
		if play_Tetris_Duration == watch_Tetris_duration == motor_control_duration == fixation_cross_duration:
			self.font_explain_trials = self.font_explain_trials_equal
		else:
			self.font_explain_trials = self.font_explain_trials_unequal
		
		# Clean up temporary attributes
		del self.font_explain_trials_equal, self.font_explain_trials_unequal
