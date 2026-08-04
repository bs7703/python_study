#quiz_game.py
import json
from quiz import Quiz
from constants import *

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

	def	ui_format(self, line_char, line_length, text):
		return f"{line_char * line_length}\n{text}\n{line_char * line_length}"
	
	def	display_menu(self):
		print(self.config['game_title'])
		my_str = ""
		for	option in self.config['menu_options']:	
			my_str += option['label'] + "\n"
		print(self.ui_format(self.config['ui_style']['line_char'], self.config['ui_style']['line_length'], my_str))
		 
	def	run(self):
		while self.is_running:
			self.display_menu()
			print(FINAL_PROMPT_RANGED_NUM_REQUIRE_MSG.format(m = 1, n = len(self.config['menu_options'])))
			try:
				idx = self.advanced_input(1,len(self.config['menu_options']))
			except (KeyboardInterrupt, EOFError):
				print(FINAL_EOF_ERROR_MSG)
				try:
					self.save_quiz()
				except (Exception):
					pass
				finally:	
					self.is_running = False
					idx = None
			except (Exception):
				print("미확인 에러발생 프로그램종료")
				self.is_running = False
				idx = None
			if idx is None:
				pass
			else:
				func = self.config['menu_options'][idx - 1]['action']
				if hasattr(self, func):
					try:
						getattr(self, func)(*([self.set_basic_quiz()] if (idx - 1) == 0 else []))
					except (EOFError, KeyboardInterrupt):
						print(FINAL_EOF_ERROR_MSG)
						try:
							self.save_quiz()
						except (Exception):
							pass
						finally:
							self.is_running = False
					except (Exception):
						print("미확인 에러발생 프로그램종료")
						self.is_running = False
				else :
					print(FINAL_FUNC_NOT_DEFINED_ERROR_MSG)
					self.is_running = False

	def	advanced_input(self, range0 = 0, range1 = 0, val_err_msg = FINAL_VALUE_ERROR_MSG):
		is_running = True
		while is_running:
			try:
				choice = input().strip()
				idx = int(choice)
				if not (range0 <= idx <= range1):
					print(val_err_msg)
				else:
					is_running = False
			except (ValueError):
				print(FINAL_TYPE_NOT_SUPPORT_ERROR_MSG)
			except (KeyboardInterrupt, EOFError) as E:
				raise E
		return idx
	
	def	advanced_strinput(self, val_err_msg = FINAL_VALUE_ERROR_MSG):
		is_running = True
		while is_running:
			try:
				choices = input().strip()
				if not (FINAL_STR_LEN_MIN <= len(choices) <= FINAL_STR_LEN_MAX):
					print(val_err_msg)
				else:
					is_running = False
			except (ValueError):
				print(FINAL_TYPE_NOT_SUPPORT_ERROR_MSG)
			except (EOFError, KeyboardInterrupt) as E:
				raise E
		return choices
		
	def	solve_quiz(self, quiz):
		data = None
		hinted = False
		score = 0
		print(self.ui_format(self.config['ui_style']['line_char'], self.config['ui_style']['line_length'], FINAL_PROMPT_ANSWER_POINT_MSG.format(answer_point=quiz.show_score())))
		print(quiz.show_quiz())
		print(FINAL_PROMPT_HINT_SHOW_MSG.format(FINAL_HINT_NUM=FINAL_HINT_NUM, i=quiz.show_score() * self.config['game_settings']['hint_factor']))
		while data is None:
			data = self.advanced_input(1, len(quiz.choices) + 1)
			if (data == (len(quiz.choices) + 1) and quiz.show_hint() is None):
				print(FINAL_HINT_NOT_POSSIBLE_ERROR_MSG)
				data = None
			else:
				if (data == (len(quiz.choices) + 1) and hinted is False):
					print(quiz.show_hint())
					score -= quiz.show_score() * self.config['game_settings']['hint_factor']
					hinted = True
					data = None
				elif (data == (len(quiz.choices) + 1) and hinted is True) :
					print(FINAL_HINT_ONLY_ERROR_MSG)
					data = None
		score += quiz.check_answers(data)
		print(FINAL_PROMPT_ANSWER_SCORE_MSG.format(i = score) if score > 0 else FINAL_PROMPT_WRONG_SCORE_MSG.format(i = score))
		return data, score

	def	start_quiz(self, quiz_list): 
		score = 0
		answer_list = []
		choice_list = []
		print(FINAL_SETTINGS_START_QUIZ_MSG.format(answer_point=self.config['game_settings']['answer_factor'], wrong_point=self.config['game_settings']['wrong_factor'], hint_point=self.config['game_settings']['hint_factor']))
		for a in enumerate(quiz_list, 1):
			value, item_score = self.solve_quiz(a[1])
			score += item_score
			answer_list.append(a[1].get_answer())
			choice_list.append(value)
		print(FINAL_PROMPT_QUIZ_RESULT_MSG.format(c = choice_list, a = answer_list))
		print(FINAL_PROMPT_SHOW_SCORE_MSG.format(score = score))
		if (score > self.basic_data["best_score"]):
			self.basic_data["best_score"] = score

	def	set_basic_quiz(self):
		base_data = []
		try:
			for a in enumerate(self.basic_data['quizzes'], 1):
				base_data.append(Quiz(**{key: a[1][key] for key in FINAL_REQUIRED_KEYS}))
		except (ValueError) as e:
			print(f"{e}")
		return base_data
	
	def	show_score(self):
		print(self.basic_data["best_score"])

	def	exit_game(self):
		self.save_quiz()
		self.is_running = False

	def	show_quiz(self):
		key = FINAL_REQUIRED_KEYS[0]
		for i, item in enumerate(self.basic_data["quizzes"], 1):
			print(f"{i}번째 문제:{item[key]}")

	def	init_quiz_item(self):
		data = {}
		data[FINAL_REQUIRED_KEYS[0]] = str("")
		data[FINAL_REQUIRED_KEYS[1]] = []
		data[FINAL_REQUIRED_KEYS[2]] = 1
		data[FINAL_REQUIRED_KEYS[3]] = FINAL_BASE_ANSWER_POINT
		data[FINAL_REQUIRED_KEYS[4]] = "" 
		data[FINAL_REQUIRED_KEYS[5]] = ""
		return data
		
	def add_quiz(self):
		my_quiz = self.init_quiz_item()

		print(FINAL_PROMPT_INSERT_QUESTION_MSG + f"({FINAL_STR_LEN_MIN}~{FINAL_STR_LEN_MAX})")
		my_quiz[FINAL_REQUIRED_KEYS[0]] = self.advanced_strinput(FINAL_STR_ERROR_MSG)
		print(FINAL_PROMPT_INSERT_ANSWER_MSG + f"({FINAL_ANSWER_RANGE_MIN}~{FINAL_ANSWER_RANGE_MAX})")
		my_quiz[FINAL_REQUIRED_KEYS[2]] = self.advanced_input(FINAL_ANSWER_RANGE_MIN, FINAL_ANSWER_RANGE_MAX, FINAL_INT_RANGE_ERROR_MSG)
		for i in range(FINAL_CHOICES_NUM):
			print(f"{i + 1}" + FINAL_PROMPT_INSERT_CHOICE_MSG + f"{FINAL_STR_LEN_MIN}~{FINAL_STR_LEN_MAX}")
			choice = self.advanced_strinput(FINAL_STR_ERROR_MSG)
			my_quiz[FINAL_REQUIRED_KEYS[1]].append(choice)
		self.basic_data["quizzes"].append(my_quiz)
		print(FINAL_PROMPT_QUIZ_ADD_MSG)
		return True
	
	def	del_quiz(self):
		is_run = True
		while is_run:
			data = self.basic_data["quizzes"]
			print(FINAL_PROMPT_INSERT_DELETE_MSG.format(m = 0, n = len(data)))
			self.show_quiz()
			num = self.advanced_input(0, len(data))
			if not(isinstance(data, list)):
				return False
			if (num == 0):
				print(FINAL_PROMPT_QUIZ_NOTDEL_MSG)
				is_run = False
			elif not (1 <= num <= (len(data) + 1)):
				return
			del data[num - 1]
			print(FINAL_PROMPT_QUIZ_DEL_MSG)
	
	def	save_quiz(self):
		self.save_data(self.load_path, self.basic_data)
		print(FINAL_PROMPT_QUIZ_SAVED_MSG)

	def	load_quiz(self, load_path):
		try:
			data = self.load_data(load_path)
		except (Exception) as e:
			raise e
		if not self.check_data(data["quizzes"]):
			print(FINAL_DATA_INAPPROPRIATE_ERROR_MSG)
			raise ValueError
		return data
	def	check_data(self, data):
		if not isinstance(data, list):
			print(FINAL_DATA_NOT_LIST_ERROR_MSG)
			return False
		
		for i, item in enumerate(data):
			if not isinstance(item, dict):
				print(FINAL_DATA_ITEM_NOT_DICT_ERROR_MSG.format(i= i + 1))
				return False

			for key in FINAL_REQUIRED_KEYS:
				if key not in item:
					print(FINAL_DATA_ITEM_MISSING_KEY_ERROR_MSG.format(i= i + 1, key= key))
					return False
				
			if not isinstance(item["question"], str) or not item["question"].strip():
				print(FINAL_DATA_ITEM_INVALID_QUESTION_OR_CHOICES_ERROR_MSG.format(i= i + 1))
				return False
				
			choices = item["choices"]

			if not isinstance(choices, list) or len(choices) != FINAL_CHOICES_NUM:
				print(FINAL_CHOICES_NUM_ERROR_MSG.format(i= i + 1, FINAL_CHOICES_NUM= FINAL_CHOICES_NUM) + f" (현재: {len(choices) if isinstance(choices, list) else '리스트 아님'})")
				return False

			if not all(isinstance(c, str) and c.strip() for c in choices):
				print(FINAL_CHOICES_STR_ERROR_MSG.format(i= i + 1))
				return False

			answer = item["answer"]

			if not isinstance(answer, int) or not (FINAL_ANSWER_RANGE_MIN <= answer <= FINAL_ANSWER_RANGE_MAX):
				print(FINAL_ANSWER_RANGE_ERROR_MSG.format(i= i + 1, FINAL_ANSWER_RANGE_MIN= FINAL_ANSWER_RANGE_MIN, FINAL_ANSWER_RANGE_MAX= FINAL_ANSWER_RANGE_MAX))
				return False
				
			point = item["answer_point"]
			if not isinstance(point, int) or not (FINAL_ANSWER_POINT_MIN <= point <= FINAL_ANSWER_POINT_MAX):
				print(FINAL_ANSWER_POINT_RANGE_ERROR_MSG.format(i= i + 1, FINAL_ANSWER_POINT_MIN= FINAL_ANSWER_POINT_MIN, FINAL_ANSWER_POINT_MAX= FINAL_ANSWER_POINT_MAX))
				return False
		return True

	def	load_data(self, json_path):
		data = None
		try:
			with open(json_path, 'r', encoding='utf-8') as f:
				data = json.load(f)
		except (FileNotFoundError):
			print(f"{json_path}" + FINAL_FILE_NOT_FOUND_ERROR_MSG)
		except (json.JSONDecodeError):
			print(f"{json_path}" + FINAL_JSON_DECODE_ERROR_MSG)
		except (PermissionError):
			print(f"{json_path}" + FINAL_PERMISSION_ERROR_MSG)
		except (Exception) as e:
			print(f"{json_path}" + FINAL_UNKNOWN_ERROR_MSG + f" 상세 오류: {e}")
		return data

	def	save_data(self, json_path, data):
		try:
			with open(json_path, 'w', encoding='utf-8') as f:
				json.dump(data, f, ensure_ascii=False, indent=4)
		except (PermissionError) as e:
			print(f"{json_path}" + FINAL_PERMISSION_ERROR_MSG)
			raise e
		except (Exception) as e:
			print(f"{json_path}" + FINAL_UNKNOWN_ERROR_MSG + f" 상세 오류: {e}")
			raise e

if	__name__ == "__main__":
	game = QuizGame("config.json", "state.json")
	game.run()