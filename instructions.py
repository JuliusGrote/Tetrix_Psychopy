# This file contains the class for instructions based on the language defined in "config_paradigm_psychopy.txt"
# Is executed as a python script, so it if necessary alter the instruction texts inside the '...' but not the structure of the code!

class Instructions:
	## Check what is given in the config files and set instuctions accordingly.
	def set_instructions(self, language):
		if language == 'german':
			self.font_check_response = 'Bitte pressen Sie jede Taste der Responsebox zwei mal!'
			self.font_check_response_2 = 'Responsebox erfolgreich gecheckt!'
			self.font_Intro_2 = 'Willkommen zum Tetris-Experiment!'
			self.font_continue = 'Beliebige Taste drücken, um fortzufahren!'
			self.font_explanation_pretrial = 'Während diesem ersten Teil des Experiments werden Sie Tetris spielen und sich an das Setup gewöhnen! \n \n Wie man spielt:'
			self.img_explain_game_mechanics = 'Images/explain_game_mechanics_de.png'
			self.img_explain_controls = 'Images/explain_controls_de.png'
			self.font_Controls = 'So bewegen Sie die Tetris-Blöcke:'
			self.font_start_pretrial = 'Beliebige Taste drücken, um das erste TETRIS-Spiel zu starten!'
			self.font_intro_main = 'Jetzt beginnt der Hauptteil des Experiments!'
			self.font_Announcement = 'Während des Experiments werden Sie 4 verschiedene Symbole sehen:'
			self.font_play_Tetris = 'Controller: Spielen Sie Tetris! Konzentrieren Sie sich darauf, die Blöcke beim Spielen MENTAL ZU ROTIEREN! Das Start-Level basiert auf den Leveln, die Sie im ersten Teil erreicht haben!' # <-- Alternative: Versuchen Sie zu VISUALISISEREN, wo der DERZEITIGE Tetris-Block und die NEXT (nächsten) Blöcke am besten hinpassen. 
			self.font_motor = 'Hand: Drücken Sie die Tasten ABWECHSELND zum Rhythmus, der auf dem Bildschirm zu sehen ist!'
			self.font_watch = 'Auge: Schauen Sie Tetris! Schauen Sie einfach nur zu, während eine Spiel-Aufzeichnung für Sie gespielt wird. Bitte Drücken Sie KEINE Tasten!'
			self.font_cross = 'Fixationskreuz: Schauen Sie einfach das Kreuz in der Bildschirmmitte an und machen Sie nichts Anderes!'
			self.font_start = 'Jetzt beginnt das Experiment!'
			self.font_condition_ended = 'Block beendet'
			self.font_end = 'Vielen Dank für Ihre Teilnahme!'
			
		else:
			self.font_check_response = 'Please press each button on the responsebox twice!' 
			self.font_check_response_2 = 'Responses checked successfully'
			self.font_Intro_2 = 'Welcome to the Tetris experiment!'
			self.font_continue = 'Press any button to continue!'
			self.font_explanation_pretrial = 'During this first part of the experiment, you will play Tetris and get used to the setup! \n How to play:'
			self.img_explain_game_mechanics = 'Images/explain_game_mechanics_en.png'
			self.img_explain_controls = 'Images/explain_controls_en.png'
			self.font_Controls = 'This is how you move the Tetris-Blocks:'
			self.font_start_pretrial = 'Press any button to start the first TETRIS-GAME!'
			self.font_intro_main = 'Now the main part of the experiment begins!'
			self.font_Announcement = 'During the Experiment you will encounter 4 different symbols:'
			self.font_play_Tetris = 'Controller: Play Tetris! Focus on MENTALLY ROTATING the blocks when playing! The starting level is adjusted based on the levels you reached in the first part!'# <-- Alternative: Try to VISUALIZE where the CURRENT Tetris block and the NEXTs blocks fit best. 
			self.font_motor = 'Hand: Press the Buttons ALTERNATELY (one after another) to the rhythm displayed on the screen!'
			self.font_watch = 'Eye: Watch Tetris! Just watch while a game recording is played for you. Please DO NOT press any buttons!'
			self.font_cross = 'Fixation Cross: Just look at the cross in the middle of the screen and do nothing else!'
			self.font_start = 'Now, the experiment starts!'
			self.font_condition_ended = 'Block ended'
			self.font_end = 'Thank you for your Participation!'
			
			
			
			
		
		
