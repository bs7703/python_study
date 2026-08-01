#quiz_game.py
import json
class QuizzGame:
	def	__init__(self, config_path):
		with open(config_path, 'r', encoding='utf-8') as f:
			self.config = json.load(f)
		self.is_running = True
		pass

	def	display_menu(self):
		#화면에 메뉴를 표시함
		print(f"\n=== {self.config['game_title']} ===")
		print(f"{self.config['ui_style']['line_char']}" * self.config['ui_style']['line_length'])
		for	option in self.config['menu_options']:	
			print(option['label'])
		print(f"{self.config['ui_style']['line_char']}" * self.config['ui_style']['line_length'])
	def	run(self):
		while self.is_running:
			self.display_menu()
			try:
				choice = int(input("원하는 메뉴 번호를 입력하세요:").strip())
				idx = choice - 1
				if idx >= 3 or idx < 0:
					raise IndexError
				func = self.config['menu_options'][idx]['action']
				if hasattr(self, func):
					getattr(self, func)()
				else :
					print("해당 함수가 정의되지 않았습니다")
					self.is_running = False
			except (ValueError) :
				print("범위내 숫자 이외에 입력하지 말아주세요")
			except (IndexError) :
				print(f"{choice}는 적절한 번호가아닙니다 다시입력해주세요")
			except (KeyboardInterrupt, EOFError):
				print("사용자에의해 프로그램이 강제로종료됩니다")
				self.is_running = False
		pass

	def	start_quiz(self):
		pass

	def	show_score(self):
		pass

	def	exit_game(self):
		self.is_running = False

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