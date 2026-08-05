# quiz_game.py
import json
import random
import datetime
from quiz import Quiz
from constants import *


class QuizGame:
    def __init__(self, config_path, load_path):
        try:
            self.config = self.load_data(config_path)
            if not self.check_config(self.config):
                exit()
        except Exception:
            exit()

        try:
            self.basic_data = self.load_quiz(load_path)
        except Exception:
            try:
                self.basic_data = self.load_quiz(FINAL_BASIC_DATA_PATH)
            except Exception as e:
                print(e)
                exit()

        if self.basic_data is None:
            exit()

        self.load_path = load_path
        self.is_running = True

    def display_menu(self):
        print(self.config['game_title'])
        menu_text = ''
        for option in self.config['menu_options']:
            menu_text += option['label'] + '\n'
        print(self.ui_format(self.config['ui_style']['line_char'], self.config['ui_style']['line_length'], menu_text))

    def ui_format(self, line_char, line_length, text):
        return f"{line_char * line_length}\n{text}\n{line_char * line_length}"

    def execute_menu_option(self, idx):
        action_name = self.config['menu_options'][idx - 1]['action']
        if not hasattr(self, action_name):
            print(FINAL_FUNC_NOT_DEFINED_ERROR_MSG)
            self.is_running = False
            return
        try:
            getattr(self, action_name)()
        except Exception:
            print("미확인 에러발생 프로그램종료")
            self.is_running = False

    def handle_exit(self):
        print(FINAL_EOF_ERROR_MSG)
        try:
            self.save_quiz()
        except Exception:
            pass


    def run(self):
        while self.is_running:
            self.display_menu()
            print(FINAL_PROMPT_RANGED_NUM_REQUIRE_MSG.format(m=1, n=len(self.config['menu_options'])))
            idx = self.advanced_input(1, len(self.config['menu_options']))
            self.execute_menu_option(idx)

    def advanced_input(self, range0=0, range1=0, val_err_msg=FINAL_VALUE_ERROR_MSG):
        while True:
            try:
                choice = input().strip()
                idx = int(choice)
                if not (range0 <= idx <= range1):
                    print(val_err_msg)
                    continue
                return idx
            except ValueError:
                print(FINAL_TYPE_NOT_SUPPORT_ERROR_MSG)
            except (KeyboardInterrupt, EOFError):
                self.handle_exit()
                exit()

    def advanced_strinput(self, val_err_msg=FINAL_VALUE_ERROR_MSG):
        while True:
            try:
                choices = input().strip()
                if not (FINAL_STR_LEN_MIN <= len(choices) <= FINAL_STR_LEN_MAX):
                    print(val_err_msg)
                    continue
                return choices
            except ValueError:
                print(FINAL_TYPE_NOT_SUPPORT_ERROR_MSG)
            except (KeyboardInterrupt, EOFError):
                self.handle_exit()
                exit()

    def add_quiz(self):
        new_quiz = self.init_quiz_item()

        print(FINAL_PROMPT_INSERT_QUESTION_MSG + f"({FINAL_STR_LEN_MIN}~{FINAL_STR_LEN_MAX})")
        new_quiz[FINAL_REQUIRED_KEYS[0]] = self.advanced_strinput(FINAL_STR_ERROR_MSG)

        print(FINAL_PROMPT_INSERT_ANSWER_MSG + f"({FINAL_ANSWER_RANGE_MIN}~{FINAL_ANSWER_RANGE_MAX})")
        new_quiz[FINAL_REQUIRED_KEYS[2]] = self.advanced_input(FINAL_ANSWER_RANGE_MIN, FINAL_ANSWER_RANGE_MAX)

        for i in range(FINAL_CHOICES_NUM):
            print(f"{i + 1}" + FINAL_PROMPT_INSERT_CHOICE_MSG + f"{FINAL_STR_LEN_MIN}~{FINAL_STR_LEN_MAX}")
            choice = self.advanced_strinput(FINAL_STR_ERROR_MSG)
            new_quiz[FINAL_REQUIRED_KEYS[1]].append(choice)

        self.basic_data['quizzes'].append(new_quiz)
        print(FINAL_PROMPT_QUIZ_ADD_MSG)
        return True

    def del_quiz(self):
        while True:
            quizzes = self.basic_data['quizzes']
            print(FINAL_PROMPT_INSERT_DELETE_MSG.format(m=0, n=len(quizzes)))
            self.show_quiz()
            num = self.advanced_input(0, len(quizzes))
            if num == 0:
                print(FINAL_PROMPT_QUIZ_NOTDEL_MSG)
                return
            elif not (1 <= num <= len(quizzes)):
                continue
            else:
                del quizzes[num - 1]
                print(FINAL_PROMPT_QUIZ_DEL_MSG)

    def exit_game(self):
        self.save_quiz()
        self.is_running = False

    def init_quiz_item(self):
        return {
            FINAL_REQUIRED_KEYS[0]: '',
            FINAL_REQUIRED_KEYS[1]: [],
            FINAL_REQUIRED_KEYS[2]: FINAL_BASE_ANSWER,
            FINAL_REQUIRED_KEYS[3]: FINAL_BASE_ANSWER_POINT,
            FINAL_REQUIRED_KEYS[4]: '',
            FINAL_REQUIRED_KEYS[5]: ''
        }



    def show_quiz(self):
        for i, item in enumerate(self.basic_data['quizzes'], 1):
            print(f"{i}번째 문제: {item[FINAL_REQUIRED_KEYS[0]]}")

    def show_score(self):
        print(self.basic_data['best_score'])

    def solve_quiz(self, quiz):
        hinted = False
        score = 0

        print(self.ui_format(self.config['ui_style']['line_char'], self.config['ui_style']['line_length'], FINAL_PROMPT_ANSWER_POINT_MSG.format(answer_point=quiz.show_score())))
        print(quiz.show_quiz())
        print(FINAL_PROMPT_HINT_SHOW_MSG.format(FINAL_HINT_NUM=FINAL_HINT_NUM, i=quiz.show_score() * self.config['game_settings']['hint_factor']))

        answer = None
        while answer is None:
            choice = self.advanced_input(1, len(quiz.choices) + 1)
            if choice == len(quiz.choices) + 1:
                if quiz.show_hint() is None:
                    print(FINAL_HINT_NOT_POSSIBLE_ERROR_MSG)
                elif not hinted:
                    print(quiz.show_hint())
                    score -= quiz.show_score() * self.config['game_settings']['hint_factor']
                    hinted = True
                else:
                    print(FINAL_HINT_ONLY_ERROR_MSG)
                continue
            answer = choice

        result = quiz.check_answers(answer)
        score += result * (self.config['game_settings']['answer_factor'] if result > 0 else self.config['game_settings']['wrong_factor'])

        if self.config['game_settings']['show_explanation']:
            print(self.ui_format(self.config['ui_style']['line_char'], self.config['ui_style']['line_length'], quiz.get_explanation()))

        print(FINAL_PROMPT_ANSWER_SCORE_MSG.format(i=score) if score > 0 else FINAL_PROMPT_WRONG_SCORE_MSG.format(i=score))
        return answer, score

    def start_quiz(self):
        quizzes_total = len(self.basic_data.get('quizzes', []) if isinstance(self.basic_data, dict) else [])
        if quizzes_total == 0:
            print(FINAL_DATA_INAPPROPRIATE_ERROR_MSG)
            return
        print(FINAL_PROMPT_RANGED_NUM_REQUIRE_MSG.format(m=1, n=quizzes_total))
        n = self.advanced_input(1, quizzes_total)
        quiz_list = self.build_quiz_sequence(n)
        answer_list = []
        choice_list = []
        score_list = self.build_score_data(n)
        self.basic_data["score_list"].append(score_list)
        print(FINAL_SETTINGS_START_QUIZ_MSG.format(answer_point=self.config['game_settings']['answer_factor'], wrong_point=self.config['game_settings']['wrong_factor'], hint_point=self.config['game_settings']['hint_factor']))
        for idx, quiz in enumerate(quiz_list, start=1):
            selected, item_score = self.solve_quiz(quiz)
            answer_list.append(quiz.get_answer())
            choice_list.append(selected)
            score_list['total_quiz_solved_count'] += 1
            score_list['score'] += item_score

        print(FINAL_PROMPT_QUIZ_RESULT_MSG.format(c=choice_list, a=answer_list))
        print(FINAL_PROMPT_SHOW_SCORE_MSG.format(score=score_list['score']))

        if score_list['score'] > self.basic_data['best_score']:
            self.basic_data['best_score'] = score_list['score']

    def build_score_data(self, quiz_num):
        score_data = {}
        score_data['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        score_data['selected_quiz_count'] = quiz_num
        score_data['total_quiz_solved_count'] = 0
        score_data['score'] = 0
        return score_data



    def build_quiz_sequence(self, num_items):
        quizzes = self.basic_data.get('quizzes', []) if isinstance(self.basic_data, dict) else []
        total = len(quizzes)
        if total == 0:
            return []

        if not isinstance(num_items, int) or num_items <= 0:
            num = total
        else:
            num = min(num_items, total)

        indices = list(range(total))
        random.shuffle(indices)
        chosen = indices[:num]

        sequence = []
        for i in chosen:
            item = quizzes[i]
            sequence.append(Quiz(**{key: item[key] for key in FINAL_REQUIRED_KEYS}))
        return sequence


    def load_data(self, json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError as e:
            print(f"{json_path}" + FINAL_FILE_NOT_FOUND_ERROR_MSG)
            raise e
        except json.JSONDecodeError as e:
            print(f"{json_path}" + FINAL_JSON_DECODE_ERROR_MSG)
            raise e
        except PermissionError as e:
            print(f"{json_path}" + FINAL_PERMISSION_ERROR_MSG)
            raise e
        except Exception as e:
            print(f"{json_path}" + FINAL_UNKNOWN_ERROR_MSG + f" 상세 오류: {e}")
            raise e

    def load_quiz(self, load_path):
        data = self.load_data(load_path)
        if not self.check_data(data['quizzes']):
            print(FINAL_DATA_INAPPROPRIATE_ERROR_MSG)
            raise ValueError
        if 'best_score' not in data or not isinstance(data['best_score'], int):
            """
            best score는 일회성이므로 대체지급가능할수도
            """
            raise ValueError
        if 'score_list' not in data or not self.check_score_list(data['score_list']):
            """
            score_list는 초기화후 다시밀수도
            """
            raise ValueError
        return data

    def save_data(self, json_path, data):
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except PermissionError as e:
            print(f"{json_path}" + FINAL_PERMISSION_ERROR_MSG)
            raise e
        except Exception as e:
            print(f"{json_path}" + FINAL_UNKNOWN_ERROR_MSG + f" 상세 오류: {e}")
            raise e

    def save_quiz(self):
        self.save_data(self.load_path, self.basic_data)
        print(FINAL_PROMPT_QUIZ_SAVED_MSG)

    def check_config(self, config):
        if not isinstance(config, dict):
            print(FINAL_CONFIG_NOT_DICT_ERROR_MSG)
            return False

        for key in FINAL_REQUIRED_CONFIG_KEYS:
            if key not in config:
                print(FINAL_CONFIG_MISSING_KEY_ERROR_MSG.format(key=key))
                return False

        if not isinstance(config['game_title'], str) or not config['game_title'].strip():
            print(FINAL_CONFIG_INVALID_TITLE_ERROR_MSG)
            return False

        if not isinstance(config['exit_message'], str) or not config['exit_message'].strip():
            print(FINAL_CONFIG_INVALID_EXIT_MESSAGE_ERROR_MSG)
            return False

        if not self.check_menu_options(config['menu_options']):
            print(FINAL_CONFIG_INVALID_MENU_OPTIONS_ERROR_MSG)
            return False

        if not self.check_ui_style(config['ui_style']):
            print(FINAL_CONFIG_INVALID_UI_STYLE_ERROR_MSG)
            return False

        if not isinstance(config['game_settings'], dict):
            print(FINAL_CONFIG_INVALID_GAME_SETTINGS_ERROR_MSG)
            return False

        config['game_settings'] = self.normalize_game_settings(config['game_settings'])
        if not self.check_game_settings(config['game_settings']):
            return False

        if not isinstance(config['best_score'], int) or config['best_score'] < 0:
            print(FINAL_CONFIG_INVALID_BEST_SCORE_ERROR_MSG)
            config['best_score'] = 0

        return True

    def check_data(self, data):
        if not isinstance(data, list):
            print(FINAL_DATA_NOT_LIST_ERROR_MSG)
            return False

        for i, item in enumerate(data, 1):
            if not isinstance(item, dict):
                print(FINAL_DATA_ITEM_NOT_DICT_ERROR_MSG.format(i=i))
                return False

            for key in FINAL_REQUIRED_KEYS:
                if key not in item:
                    print(FINAL_DATA_ITEM_MISSING_KEY_ERROR_MSG.format(i=i, key=key))
                    return False

            if not isinstance(item['question'], str) or not item['question'].strip():
                print(FINAL_DATA_ITEM_INVALID_QUESTION_OR_CHOICES_ERROR_MSG.format(i=i))
                return False

            choices = item['choices']
            if not isinstance(choices, list) or len(choices) != FINAL_CHOICES_NUM:
                print(FINAL_CHOICES_NUM_ERROR_MSG.format(i=i, FINAL_CHOICES_NUM=FINAL_CHOICES_NUM) + f" (현재: {len(choices) if isinstance(choices, list) else '리스트 아님'})")
                return False

            if not all(isinstance(c, str) and c.strip() for c in choices):
                print(FINAL_CHOICES_STR_ERROR_MSG.format(i=i))
                return False

            answer = item['answer']
            if not isinstance(answer, int) or not (FINAL_ANSWER_RANGE_MIN <= answer <= FINAL_ANSWER_RANGE_MAX):
                print(FINAL_ANSWER_RANGE_ERROR_MSG.format(i=i, FINAL_ANSWER_RANGE_MIN=FINAL_ANSWER_RANGE_MIN, FINAL_ANSWER_RANGE_MAX=FINAL_ANSWER_RANGE_MAX))
                return False

            point = item['answer_point']
            if not isinstance(point, int) or not (FINAL_ANSWER_POINT_MIN <= point <= FINAL_ANSWER_POINT_MAX):
                print(FINAL_ANSWER_POINT_RANGE_ERROR_MSG.format(i=i, FINAL_ANSWER_POINT_MIN=FINAL_ANSWER_POINT_MIN, FINAL_ANSWER_POINT_MAX=FINAL_ANSWER_POINT_MAX))
                return False

        return True
    
    def check_score_list(self, score_list):
        if not isinstance(score_list, list):
            print("score_list는 리스트여야 합니다.")
            return False

        for i, item in enumerate(score_list, 1):
            if not isinstance(item, dict):
                print(f"score_list 항목 {i}는 딕셔너리여야 합니다.")
                return False

            required_keys = ['date', 'selected_quiz_count', 'total_quiz_solved_count', 'score']
            for key in required_keys:
                if key not in item:
                    print(f"score_list 항목 {i}에 '{key}' 키가 없습니다.")
                    return False

            if not isinstance(item['date'], str) or not item['date'].strip():
                print(f"score_list 항목 {i}의 date는 비어있지 않은 문자열이어야 합니다.")
                return False
            if not isinstance(item['selected_quiz_count'], int) or item['selected_quiz_count'] < 0:
                print(f"score_list 항목 {i}의 selected_quiz_count는 0 이상의 정수여야 합니다.")
                return False
            if not isinstance(item['total_quiz_solved_count'], int) or item['total_quiz_solved_count'] < 0:
                print(f"score_list 항목 {i}의 total_quiz_solved_count는 0 이상의 정수여야 합니다.")
                return False
            if item['total_quiz_solved_count'] > item['selected_quiz_count']:
                print(f"score_list 항목 {i}의 total_quiz_solved_count는 selected_quiz_count를 초과할 수 없습니다.")
                return False
            if not isinstance(item['score'], int):
                print(f"score_list 항목 {i}의 score는 정수여야 합니다.")
                return False

        return True

    def check_game_settings(self, settings):
        for key in FINAL_REQUIRED_GAME_SETTINGS_KEYS:
            if key not in settings:
                print(FINAL_CONFIG_MISSING_GAME_SETTINGS_KEY_ERROR_MSG.format(key=key))
                return False

        if not isinstance(settings['answer_factor'], int) or not (FINAL_ANSWER_FACTOR_MIN <= settings['answer_factor'] <= FINAL_ANSWER_FACTOR_MAX):
            print(FINAL_CONFIG_INVALID_GAME_SETTINGS_VALUE_ERROR_MSG.format(key='answer_factor'))
            return False

        if not isinstance(settings['hint_factor'], int) or not (FINAL_HINT_FACTOR_MIN <= settings['hint_factor'] <= FINAL_HINT_FACTOR_MAX):
            print(FINAL_CONFIG_INVALID_GAME_SETTINGS_VALUE_ERROR_MSG.format(key='hint_factor'))
            return False

        if not isinstance(settings['wrong_factor'], int) or not (FINAL_WRONG_FACTOR_MIN <= settings['wrong_factor'] <= FINAL_WRONG_FACTOR_MAX):
            print(FINAL_CONFIG_INVALID_GAME_SETTINGS_VALUE_ERROR_MSG.format(key='wrong_factor'))
            return False

        if not isinstance(settings['show_explanation'], bool):
            print(FINAL_CONFIG_INVALID_GAME_SETTINGS_VALUE_ERROR_MSG.format(key='show_explanation'))
            return False

        return True

    def check_menu_options(self, menu_options):
        if not isinstance(menu_options, list) or len(menu_options) == 0:
            return False

        for item in menu_options:
            if not isinstance(item, dict):
                return False
            if 'label' not in item or 'action' not in item:
                return False
            if not isinstance(item['label'], str) or not item['label'].strip():
                return False
            if not isinstance(item['action'], str) or not item['action'].strip():
                return False

        return True

    def check_ui_style(self, ui_style):
        if not isinstance(ui_style, dict):
            return False

        line_char = ui_style.get('line_char')
        line_length = ui_style.get('line_length')

        if not isinstance(line_char, str) or len(line_char) != 1:
            return False
        if not isinstance(line_length, int) or line_length <= 0:
            return False

        return True

    def normalize_game_settings(self, settings):
        if not isinstance(settings, dict):
            settings = {}
        if not isinstance(settings.get('answer_factor'), int) or not (FINAL_ANSWER_FACTOR_MIN <= settings.get('answer_factor') <= FINAL_ANSWER_FACTOR_MAX):
            settings['answer_factor'] = FINAL_BASE_ANSWER_FACTOR
        if not isinstance(settings.get('hint_factor'), int) or not (FINAL_HINT_FACTOR_MIN <= settings.get('hint_factor') <= FINAL_HINT_FACTOR_MAX):
            settings['hint_factor'] = FINAL_BASE_HINT_FACTOR
        if not isinstance(settings.get('wrong_factor'), int) or not (FINAL_WRONG_FACTOR_MIN <= settings.get('wrong_factor') <= FINAL_WRONG_FACTOR_MAX):
            settings['wrong_factor'] = FINAL_BASE_WRONG_FACTOR
        if not isinstance(settings.get('show_explanation'), bool):
            settings['show_explanation'] = FINAL_SHOW_EXPLANATION

        return settings


if __name__ == "__main__":
    game = QuizGame(FINAL_CONFIG_PATH, FINAL_QUIZ_DATA_PATH)
    game.run()
