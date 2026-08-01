#quiz_game.py
import json
from quiz import Quiz
class QuizGame:
	def	__init__(self, config_path, basic_path):
		with open(config_path, 'r', encoding='utf-8') as f:
			self.config = json.load(f)
		with open(basic_path, 'r', encoding='utf-8') as f:
			self.basic_data = json.load(f)
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
			print("숫자를 입력해주세요(1~5):")
			idx = self.advanced_input(0,len(self.config['menu_options']),0)
			if idx is None:
				pass
			else:
				func = self.config['menu_options'][idx]['action']
				if hasattr(self, func):
					getattr(self, func)()
				else :
					print("해당 함수가 정의되지 않았습니다")
					self.is_running = False

	def	advanced_input(self, range0 = 0, range1 = 0, mode = 0):
		try:
			choice = input().strip()
			idx = int(choice) - 1
			if not (range0 <= idx < range1):
				raise IndexError
		except (ValueError):
			print("범위내 숫자 이외에 입력하지 말아주세요")
		except (IndexError):
			print("적절한숫자가아닙니다")
		except (KeyboardInterrupt, EOFError):
			print("사용자에의해 프로그램이 강제 종료됩니다.")
			self.isrunning = False
		return idx
	
	def	solve_quiz(self, quiz):
		pass

	def	start_quiz(self):
		pass

	def	set_basic_quiz(self):
		base_data = []
		try:
			for i, a in enumerate(self.basic_data, 1):
				base_data.append(Quiz(a['question'], a['choices'], a['answer'], a['hint'], a['explanation']))
		except (ValueError):
			print(f"{e}")
		return base_data
	def	show_score(self):
		pass

	def	exit_game(self):
		self.is_running = False

	def	add_quiz(self):
		pass

	def	save_data(self):
		pass

	def	load_data(self):
		pass

if	__name__ == "__main__":
	game = QuizGame("config.json", "basic_data.json")
	game.run()