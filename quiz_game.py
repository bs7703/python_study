#quiz_game.py
import json
class QuizzGame:
	def	__init__(self, config_path):
		with open(config_path, 'r', encoding='utf-8') as f:
			self.config = json.load(f)
		self.isrunning = True
		pass

	def	display_menu(self):
		#화면에 메뉴를 표시함
		print(f"\n=== {self.config['game_title']} ===")
		print(f"{self.config['ui_style']['line_char']}" * self.config['ui_style']['line_length'])
		for	option in self.config['menu_options']:	
			print(option)
		print(f"{self.config['ui_style']['line_char']}" * self.config['ui_style']['line_length'])
	def	run(self):
		self.display_menu()
		pass

	def	play_quiz(self):
		pass

	def	add_quiz(self):
		pass

	def	save_data(self):
		pass

	def	load_data(self):
		pass

if	__name__ == "__main__":
	game = QuizzGame("config.json")
	game.run()