#quiz_game.py
import json
from quiz import Quiz

FINAL_REQUIRED_KEYS = ['question', 'choices', 'answer', 'hint', 'explanation', 'answer_point']
ANSWER_RANGE_MIN = 1
ANSWER_RANGE_MAX = 4
CHOICES_NUM = 4
ANSWER_POINT_MIN = 1
ANSWER_POINT_MAX = 10
STR_LEN = 50

class QuizGame:
	def	__init__(self, config_path, load_path):
		try:
			self.config = self.load_data(config_path)
		except (Exception):
			exit()
		try:
			self.basic_data = self.load_quiz(load_path)
		except (Exception):
			exit()
		if (self.basic_data == None):
			exit()
		
		self.load_path = load_path
		self.is_running = True
		self.score = 0
		self.best_score = self.config['best_score']

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
			print(f"숫자를 입력해주세요(1~{len(self.config['menu_options'])}):")
			idx = self.advanced_input(0,len(self.config['menu_options']),0)
			if idx is None:
				pass
			else:
				func = self.config['menu_options'][idx - 1]['action']
				if hasattr(self, func):
					getattr(self, func)(*([self.set_basic_quiz()] if (idx - 1) == 0 else []))
				else :
					print("해당 함수가 정의되지 않았습니다")
					self.is_running = False

	def	advanced_input(self, range0 = 0, range1 = 0, mode = 0):
		try:
			choice = input().strip()
			idx = int(choice)
			if not (range0 <= (idx - 1) < range1):
				raise IndexError
		except (ValueError):
			print("범위내 숫자 이외에 입력하지 말아주세요" + (" 0점처리됩니다" if mode == 1 else ""))
			return None
		except (IndexError):
			if (mode == 0 or mode == 1):
				print("적절한숫자가아닙니다")
			else:
				print("힌트를보고 나면 정답을 입력해야합니다")
			return None
		except (KeyboardInterrupt, EOFError):
			print("사용자에의해 프로그램이 강제 종료됩니다.")
			self.is_running = False
			return None
		return idx
	
	def	solve_quiz(self, quiz):
		data = None
		hinted = 0
		print(f"\n해당문제의 배점은 {quiz.show_score() * self.config['game_settings']['answer_factor']} 입니다.\n\n{quiz.show_quiz()}")
		print(f"\n정답이외의 힌트가 필요하면 5를 누르세요. {quiz.show_score() * self.config['game_settings']['hint_factor']}점차감")
		while data is None:
			data = self.advanced_input(0, len(quiz.choices) + 1, 1)
			if (data == (len(quiz.choices) + 1) and hinted == 0):
				print(quiz.show_hint())
				self.score -= quiz.show_score() * self.config['game_settings']['hint_factor']
				data = self.advanced_input(0, len(quiz.choices), 2)
				hinted = 1
		return quiz.check_answers(data)

	def	start_quiz(self, quiz_list): 
		score = 0
		for i, a in enumerate(quiz_list, 1):
			answer = self.solve_quiz(a)
			print(f"정답입니다 축하합니다. {answer * self.config['game_settings']['answer_factor']}만큼 득점했습니다."
		  if answer > 0 else f"오답입니다 {answer * self.config['game_settings']['wrong_factor']}만큼 실점했습니다.")
			score += answer * self.config['game_settings']['answer_factor' if answer > 0 else 'wrong_factor']
		self.score = score

	def	set_basic_quiz(self):
		base_data = []
		try:
			for i, a in enumerate(self.basic_data, 1):
				base_data.append(Quiz(a['question'], a['choices'], a['answer'], a['hint'], a['explanation'], a['answer_point']))
		except (ValueError) as e:
			print(f"{e}")
		return base_data
	
	def	show_score(self):
		print(self.score)

	def	exit_game(self):
		self.is_running = False

	def	add_quiz(self):
		my_quiz = {}
		print("문제를 입력하세요.")
		my_str = input().strip()
		if not isinstance(my_str, str):
			print("문자열만 입력하세요")
			return None
		my_quiz[FINAL_REQUIRED_KEYS[0]] = my_str
		for i in range(4):
			print(f"{i}번 문제를 입력하세요:")
			my_str0 = input().strip()
			my_quiz[FINAL_REQUIRED_KEYS[i + 1]] = my_str0
		self.basic_data.append(my_quiz)
		self.save_quiz(self.basic_data)
		return True

	def	save_quiz(self, data):
		self.save_data(self.load_path, data)

	def	load_quiz(self, load_path):
		try:
			data = self.load_data(load_path)
		except (Exception) as e:
			raise e
		
		if not self.check_data(data):
			print("데이터가 적절하지않습니다")
			return None
		return data

	def	check_data(self, data):
		if not isinstance(data, list):
			print("데이터는 리스트 형식이어야 합니다.")
			return False
		
		for i, item in enumerate(data):
			if not isinstance(item, dict):
				print(f"데이터 항목 {i + 1}은 딕셔너리 형식이어야 합니다.")
				return False

			for key in FINAL_REQUIRED_KEYS:
				if key not in item:
					print(f"데이터 항목 {i + 1}에 '{key}' 키가 없습니다.")
					return False
				
				if not isinstance(item["question"], str) or not item["question"].strip():
					print(f"오류: 항목 {i + 1}의 질문이 비어있거나 문자열이 아닙니다.")
					return False
				
				choices = item["choices"]

				if not isinstance(choices, list) or len(choices) != CHOICES_NUM:
					print(f"오류: 항목 {i + 1}의 보기는 반드시 4개여야 합니다. (현재: {len(choices) if isinstance(choices, list) else '리스트 아님'})")
					return False

				if not all(isinstance(c, str) and c.strip() for c in choices):
					print(f"오류: 항목 {i + 1}의 모든 보기는 비어있지 않은 문자열이어야 합니다.")
					return False

				answer = item["answer"]

				if not isinstance(answer, int) or not (ANSWER_RANGE_MIN <= answer <= ANSWER_RANGE_MAX):
					print(f"오류: 항목 {i + 1}의 정답은 1에서 4 사이의 정수여야 합니다. (입력값: {answer})")
					return False
				
				point = item["answer_point"]
				if not isinstance(point, int) or not (ANSWER_POINT_MIN < point < ANSWER_POINT_MAX):
					print(f"오류: 항목 {i + 1}의 점수는 {ANSWER_POINT_MIN}보다 크고 {ANSWER_POINT_MAX}보다 작은 정수여야 합니다. (입력값: {point})")
					return False
		return True

	def	load_data(self, json_path):
		data = None
		try:
			with open(json_path, 'r', encoding='utf-8') as f:
				data = json.load(f)
		except (FileNotFoundError):
			print(f"{json_path} 파일이 존재하지 않습니다.")
		except (json.JSONDecodeError):
			print(f"{json_path} 파일이 올바른 JSON 형식이 아니거나 손상되었습니다.")
		except (PermissionError):
			print(f"{json_path} 파일에 접근할 권한이 없습니다.")
		except (Exception) as e:
			print(f"알 수 없는 오류가 발생했습니다: {e}")
		return data

	def	save_data(self, json_path, data):
		try:
			with open(json_path, 'w', encoding='utf-8') as f:
				json.dump(data, f, ensure_ascii=False, indent=4)
		except (PermissionError):
			print(f"{json_path} 파일에 접근할 권한이 없습니다.")
		except (Exception) as e:
			print(f"알 수 없는 오류가 발생했습니다: {e}")
	
if	__name__ == "__main__":
	game = QuizGame("config.json", "state.json")
	game.run()