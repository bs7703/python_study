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
			try:
				choice = int(input("원하는 메뉴 번호를 입력하세요(1~5):").strip())
				idx = choice - 1
				if not(0 <= idx < len(self.config['menu_options'])):
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