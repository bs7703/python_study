
"""
CONSTANTS SECTION
"""

FINAL_REQUIRED_KEYS = ['question', 'choices', 'answer', 'answer_point', 'hint', 'explanation']
FINAL_ANSWER_RANGE_MIN = 1
FINAL_ANSWER_RANGE_MAX = 4
FINAL_CHOICES_NUM = 4
FINAL_ANSWER_POINT_MIN = 1
FINAL_ANSWER_POINT_MAX = 10
FINAL_STR_LEN_MAX = 50
FINAL_STR_LEN_MIN = 5
FINAL_BASE_ANSWER_POINT = 1
FINAL_HINT_NUM = 5

"""
CONSTANTS SECTION
"""

"""
ERROR_MSG_SECTION
"""

FINAL_VALUE_ERROR_MSG = "입력값이 적절하지 않습니다. 다시 입력해주세요."
FINAL_EOF_ERROR_MSG =   "프로그램이 비정상적으로 종료됩니다"
FINAL_STR_ERROR_MSG = "문자열의 길이가 적절하지 않거나 문자열이 아닙니다. 다시 입력해주세요."
FINAL_STR_RANGE_ERROR_MSG = f"문자열의 길이가 {FINAL_STR_LEN_MIN}~{FINAL_STR_LEN_MAX}자 사이여야합니다. 다시 입력해주세요."
FINAL_ANSWER_RANGE_ERROR_MSG = f"정답은 {FINAL_ANSWER_RANGE_MIN}~{FINAL_ANSWER_RANGE_MAX} 사이의 숫자여야합니다. 다시 입력해주세요."
FINAL_ANSWER_POINT_RANGE_ERROR_MSG = f"점수는 {FINAL_ANSWER_POINT_MIN}보다 크고 {FINAL_ANSWER_POINT_MAX}보다 작은 정수여야합니다. 다시 입력해주세요."
FINAL_CHOICES_NUM_ERROR_MSG = f"선택지는 반드시 {FINAL_CHOICES_NUM}개여야합니다. 다시 입력해주세요."
FINAL_CHOICES_STR_ERROR_MSG = f"선택지는 반드시 {FINAL_CHOICES_NUM}개의 비어있지 않은 문자열이어야합니다. 다시 입력해주세요."
FINAL_INT_RANGE_ERROR_MSG = "적절한 범위의 값이 아닙니다."
FINAL_FUNC_NOT_DEFINED_ERROR_MSG = "해당 함수가 정의되지 않았습니다."
FINAL_FILE_NOT_FOUND_ERROR_MSG = "파일을 찾을 수 없습니다. 경로를 확인해주세요."
FINAL_JSON_DECODE_ERROR_MSG = "파일이 올바른 JSON 형식이 아니거나 손상되었습니다."
FINAL_PERMISSION_ERROR_MSG = "파일에 접근할 권한이 없습니다. 권한을 확인해주세요."
FINAL_UNKNOWN_ERROR_MSG = "알 수 없는 오류가 발생했습니다. 다시 시도해주세요."
FINAL_DATA_NOT_LIST_ERROR_MSG = "데이터는 리스트 형식이어야 합니다."
FINAL_DATA_ITEM_NOT_DICT_ERROR_MSG = "데이터 항목 {i}은 딕셔너리 형식이어야 합니다."
FINAL_DATA_ITEM_MISSING_KEY_ERROR_MSG = "데이터 항목 {i}에 '{key}' 키가 없습니다."
FINAL_DATA_ITEM_INVALID_QUESTION_OR_CHOICES_ERROR_MSG = "데이터 항목 {i}의 질문이나 선택지가 비어있거나 올바른 형식이 아닙니다."
FINAL_DATA_INAPPROPRIATE_ERROR_MSG = "데이터가 적절하지않습니다"
FINAL_CHOICES_NUM_ERROR_MSG = "데이터 항목 {i}의 선택지는 반드시 {FINAL_CHOICES_NUM}개여야 합니다."
FINAL_CHOICES_STR_ERROR_MSG = "데이터 항목 {i}의 선택지는 반드시 비어있지 않은 문자열이어야 합니다."
FINAL_ANSWER_RANGE_ERROR_MSG = "데이터 항목 {i}의 정답은 {FINAL_ANSWER_RANGE_MIN}에서 {FINAL_ANSWER_RANGE_MAX} 사이의 정수여야 합니다."
FINAL_ANSWER_POINT_RANGE_ERROR_MSG = "데이터 항목 {i}의 점수는 {FINAL_ANSWER_POINT_MIN}보다 크고 {FINAL_ANSWER_POINT_MAX}보다 작은 정수여야 합니다."
FINAL_TYPE_NOT_SUPPORT_ERROR_MSG = "해당 타입은 입력받을수없습니다."
FINAL_HINT_NOT_POSSIBLE_ERROR_MSG = "힌트가 없습니다."
FINAL_HINT_ONLY_ERROR_MSG = "힌트는 한 번만 사용할 수 있습니다."
"""
ERROR_MSG_SECTION
"""

"""
PROMPT_MSG_SECTION
"""
FINAL_SETTINGS_START_QUIZ_MSG = "퀴즈를 시작합니다. 각문제에는 각문제의 배점이 존재하며 각 항목당 배점과 계수를 곱해 점수가 책정됩니다. \n 정답을 맞추면 계수{answer_point}, 틀리면 계수{wrong_point}, 힌트를 쓰면 계수{hint_point}가 적용됩니다"
FINAL_PROMPT_ANSWER_POINT_MSG = "해당문제의 배점은 {answer_point}점입니다."
FINAL_PROMPT_ANSWER_SCORE_MSG = "정답입니다 축하합니다. {i}만큼 득점했습니다."
FINAL_PROMPT_WRONG_SCORE_MSG = "오답입니다 {i}만큼 실점했습니다."
FINAL_PROMPT_QUIZ_SCORE_MSG = "정답은 {answer}입니다. 사용자의 선택은{choice}입니다. 현재득점 {i}점 (점수가 음수면 틀린것.)"
FINAL_PROMPT_HINT_SHOW_MSG = "\n정답이외의 힌트가 필요하면 {FINAL_HINT_NUM}를 누르세요. {i}점차감"
FINAL_PROMPT_QUIZ_ADD_MSG = "문제가 성공적으로 추가되었습니다!"
FINAL_PROMPT_QUIZ_SAVED_MSG = "퀴즈가 성공적으로 저장됬습니다."
FINAL_PROMPT_QUIZ_DEL_MSG = "퀴즈가 성공적으로 삭제됬습니다."
FINAL_PROMPT_QUIZ_NOTDEL_MSG = "퀴즈를 삭제하지않습니다."
FINAL_PROMPT_RANGED_NUM_REQUIRE_MSG = "메뉴를 선택해주세요. {m}~{n}"
FINAL_PROMPT_INSERT_ANSWER_MSG = "정답을 입력하세요"
FINAL_PROMPT_INSERT_QUESTION_MSG = "문제를 입력하세요"
FINAL_PROMPT_INSERT_CHOICE_MSG = "번 문항을 입력하세요"
FINAL_PROMPT_INSERT_DELETE_MSG = "삭제할 문항을 고르세요 {m} ~ {n}. 0 입력시 미삭제"
FINAL_PROMPT_QUIZ_RESULT_MSG = "사용자 선택항목 {c}\n 정답            {a}"
FINAL_PROMPT_SHOW_SCORE_MSG = "최종점수: {score}"
"""
PROMPT_MSG_SECTION
"""