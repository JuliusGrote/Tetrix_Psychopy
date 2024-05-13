# This file contains the class for instructions based on the language defined in "config_paradigm_psychopy.txt"
# Is executed as a python script, so it if necessary alter the instruction texts inside the '...' but not the structure of the code!

class Instructions:
	## Check what is given in the config files and set instuctions accordingly.
	## naming is so that a "font" is used in a text stimulus in PsychoPy while stimuli that are used as images are "img" here
	def set_instructions(self, language, Targeted_duration, N_repeats):
		#since "font_explain_trials's" f-string uses interger calculation, if "main_trials" are disabled in the config N_repeats must be "0" instead of "None"...
		if N_repeats == None:
			N_repeats  = 0
			
		if language == 'German':
			self.font_check_response = 'Bitte pressen Sie jede Taste der Responsebox zwei mal!'
			self.font_check_response_2 = 'Responsebox erfolgreich gecheckt!'
			self.font_Intro_2 = 'Willkommen zum Tetris-Experiment!'
			self.font_continue = 'Beliebige Taste drücken, um fortzufahren!'
			self.font_explanation_pretrial = 'Während diesem ersten Teil des Experiments werden Sie Tetris spielen und sich an das Setup gewöhnen! Die Level, die Sie in diesen ersten Runden erreichen, legen fest, welches Level Sie im Hauptteil spielen!'
			self.font_how_to_play = 'Wie man Tetris spielt:'
			self.img_explain_game_mechanics = 'Images/explain_game_mechanics_de.png'
			self.font_explain_staircase = 'Bitte beachten Sie, dass in diesen ersten Runden das LEVEL, auf das Sie nach GAME OVER zurückgesetzt werden VARIIERT!'
			self.img_explain_controls = 'Images/explain_controls_de.png'
			self.font_Controls = 'So bewegen Sie die Tetris-Blöcke:'
			self.font_start_pretrial = 'Beliebige Taste drücken, um das erste TETRIS-Spiel zu starten!'
			self.font_pause_n_sec ='Pause!'
			self.font_intro_main = 'Jetzt beginnt der Hauptteil des Experiments!'
			self.font_intro_structure = 'So ist das Experiment aufgebaut:'
			self.font_Announcement = 'Während des Experiments werden Sie 4 verschiedene Symbole sehen:'
			self.font_play_Tetris = 'Controller: Spielen Sie Tetris! Konzentrieren Sie sich darauf, die Blöcke beim Spielen MENTAL ZU ROTIEREN! Zwischen zwei Tetris-Teilen wird das Spiel IM HINTERGRUND PAUSIERT!' # <-- Alternative: Versuchen Sie zu VISUALISISEREN, wo der DERZEITIGE Tetris-Block und die NEXT (nächsten) Blöcke am besten hinpassen.
			self.font_explain_comp_load = 'Achtung! In jedem Tetris-Teil wird zufällig gewählt, ob es EIN oder DREI "Next-Blöcke" gibt.'
			self.font_explain_comp_speed = 'Achtung! In jedem Tetris-Teil wird zufällig gewählt, ob in einem HÖHEREN (schnelleren) oder TIEFEREN (langsameren) Level gespielt wird!'
			self.font_motor = 'Hand: Drücken Sie die Tasten ABWECHSELND zum Rhythmus, der auf dem Bildschirm zu sehen ist!'
			self.font_watch = 'Auge: Schauen Sie Tetris zu! Schauen Sie einfach nur zu, während eine Spiel-Aufzeichnung für Sie gespielt wird. Bitte Drücken Sie KEINE Tasten!'
			self.font_cross = 'Fixationskreuz: Schauen Sie einfach das Kreuz in der Bildschirmmitte an und machen Sie nichts Anderes!'
			self.font_explain_trials = f'Jede Wiederholung startet mit einem Teil TETRIS SPIELEN, gefolgt von einem zufällig gewählten Teil TETRIS ZUZUSCHAUEN, TASTENDRÜCKEN oder FIXATIONSKREUZ! Jeder Teil dauert {Targeted_duration} Sekunden und es gibt {int(N_repeats) * 3} Wiederholungen!'
			self.font_start = 'Jetzt beginnt das Experiment!'
			self.font_condition_ended = 'Teil beendet'
			self.font_end = 'Vielen Dank für Ihre Teilnahme!'
			
		else:
			self.font_check_response = 'Please press each button on the responsebox twice!' 
			self.font_check_response_2 = 'Responses checked successfully'
			self.font_Intro_2 = 'Welcome to the Tetris experiment!'
			self.font_continue = 'Press any button to continue!'
			self.font_explanation_pretrial = 'During this first part of the experiment, you will play Tetris and get used to the setup! The levels you reach in these first rounds will determine the level you play in the main part of the experiment!'
			self.font_how_to_play = 'Here is how to play Tetris:'
			self.img_explain_game_mechanics = 'Images/explain_game_mechanics_en.png'
			self.font_explain_staircase = 'Please note that in these first rounds, the LEVEL that you will be put back to after GAME OVER VARIES!'
			self.img_explain_controls = 'Images/explain_controls_en.png'
			self.font_Controls = 'This is how you move the Tetris-Blocks:'
			self.font_start_pretrial = 'Press any button to start the first TETRIS-GAME!'
			self.font_pause_n_sec ='Rest!'
			self.font_intro_main = 'Now the main part of the experiment begins!'
			self.font_intro_structure = 'This is how the experiment is structured:'
			self.font_Announcement = 'During the experiment you will encounter 4 different symbols:'
			self.font_play_Tetris = 'Controller: Play Tetris! Focus on MENTALLY ROTATING the blocks when playing! Between two Tetris parts the game is PAUSED in the BACKGROUND!'# <-- Alternative: Try to VISUALIZE where the CURRENT Tetris block and the NEXTs blocks fit best. 
			self.font_explain_comp_load = 'Note! In each Tetris part, it is randomly chosen, whether there will be ONE or THREE "Next" blocks.'
			self.font_explain_comp_speed = 'Note! In each Tetris part, it is randomly chosen, whether you will play in a HIGHER (faster) or LOWER (slower) level!'
			self.font_motor = 'Hand: Press the Buttons ALTERNATELY (one after another) to the rhythm displayed on the screen!'
			self.font_watch = 'Eye: Watch Tetris! Just watch while a game recording is played for you. Please DO NOT press any buttons!'
			self.font_cross = 'Fixation Cross: Just look at the cross in the middle of the screen and do nothing else!'		
			self.font_explain_trials = f'Each repetition starts with a round of PLAYING TETRIS followed by a randomly chosen part of WATCHING TETRIS GAMEPLAY, BUTTON PRESSES or FIXATION CROSS! Each part lasts {Targeted_duration} seconds and there are {N_repeats * 3} repetitions!'
			self.font_start = 'Now, the experiment starts!'
			self.font_condition_ended = 'Part ended'
			self.font_end = 'Thank you for your Participation!'
