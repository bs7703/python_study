📝 Python Quiz Game Project (v1.0)
객체지향 아키텍처와 데이터 무결성 검증을 적용한 CLI 기반 퀴즈 시스템
본 프로젝트는 로직과 데이터를 엄격히 분리하고, 상세한 예외 처리와 상수 관리 시스템을 통해 안정적인 실행을 보장합니다.

개발 주소: https://github.com/bs7703/python_study

📂 1. 프로젝트 구조 및 파일 역할
text
📋 복사
📁 Project Root
├── 🐍 main.py          # Entry Point: QuizGame 인스턴스 생성 및 실행
├── 🐍 quiz_game.py     # Controller: 게임 흐름, 파일 I/O, 데이터 검증 로직
├── 🐍 quiz.py          # Model: 개별 퀴즈 객체의 속성 및 채점 행위 정의
├── 🐍 constants.py     # Config: 시스템 전체에서 사용하는 상수 및 에러 메시지 관리
├── 📄 config.json      # Settings: UI 스타일 및 게임 난이도 계수 설정
├── 📄 state.json       # Database: 사용자 점수 기록 및 퀴즈 저장소
└── 📄 basic_data.json  # Backup: 시스템 오류 시 복구용 초기 데이터
🛠 2. 클래스별 상세 함수 설명 (Full Reference)
🏗️ QuizGame 클래스 (quiz_game.py)
시스템의 전체적인 흐름을 제어하고 데이터의 유효성을 관리하는 핵심 클래스입니다.

[초기화 및 데이터 로드]
__init__(self): 설정 파일과 퀴즈 데이터를 로드합니다. 로드 실패 시 2단계 예외 처리(raise)를 통해 백업 데이터를 불러오는 트리거 역할을 합니다.
load_config(self): config.json을 읽어와 시스템 설정을 적용합니다.
check_config(self, config): 로드된 설정값에 필수 키가 있는지, 값이 유효한 범위인지 전수 검사합니다.
normalize_settings(self): 설정값이 누락되거나 잘못된 경우 constants.py에 정의된 기본값으로 자동 보정합니다.
load_data(self): state.json에서 퀴즈 목록과 점수 기록을 로드합니다.
check_data(self, data): 퀴즈 데이터의 스키마(질문, 옵션, 정답 등)가 올바른 형식인지 검증합니다.
check_score_list(self, data): 과거 점수 기록 데이터의 무결성을 확인합니다.
[사용자 입력 및 검증]
advanced_input(self, prompt, min_val, max_val): 숫자 입력 전용 함수입니다. 정수가 아닌 입력이나 범위를 벗어난 값, EOFError 등을 방어적으로 처리합니다.
advanced_strinput(self, prompt): 문자열 입력 전용 함수입니다. constants에 정의된 최소/최대 길이를 준수하는지 확인하여 빈 값 입력을 방지합니다.
[게임 실행 로직]
run(self): 프로그램의 메인 루프를 실행하며 메뉴 출력과 옵션 실행을 반복합니다.
display_menu(self): 현재 설정된 UI 스타일에 맞춰 메인 메뉴 화면을 터미널에 출력합니다.
execute_menu_option(self, choice): 사용자의 선택(1~5)에 따라 퀴즈 시작, 추가, 삭제, 종료 기능을 호출합니다.
start_quiz(self): 전체 퀴즈 세션을 관리합니다. 문제를 섞고(shuffle), 진행 상황을 표시하며, 최종 점수를 계산해 기록합니다.
solve_quiz(self, quiz_obj, current_num, total): 개별 문제 풀이 화면을 구성합니다. 힌트 사용 여부를 묻고 사용자의 입력을 받아 채점 결과를 반환합니다.
[데이터 관리]
add_quiz(self): 사용자로부터 새로운 퀴즈 정보를 입력받아 리스트에 추가하고 파일에 저장합니다.
del_quiz(self): 기존 퀴즈 목록을 보여주고, 선택한 인덱스의 문제를 안전하게 삭제합니다.
save_quiz(self): 현재 메모리의 퀴즈 데이터와 점수 기록을 state.json 파일에 물리적으로 저장합니다.
🧩 Quiz 클래스 (quiz.py)
개별 퀴즈의 데이터를 보유하고 채점 로직을 수행하는 모델 클래스입니다.

__init__(self, data): JSON 데이터를 객체 속성(질문, 4개 선택지, 정답, 힌트, 해설)으로 매핑합니다.
show_quiz(self): 질문과 선택지를 보기 좋게 포맷팅하여 문자열로 반환합니다.
check_answers(self, user_input, used_hint, factors):
사용자 정답을 판별합니다.
used_hint 여부에 따라 배점을 조절합니다.
오답 시 설정된 계수(factors)를 적용하여 감점 로직을 수행합니다.
show_hint(self): 해당 문제의 힌트를 반환합니다.
get_explanation(self): 문제의 상세 해설을 반환하며, 해설이 없을 경우 기본 안내 메시지를 출력합니다.
🛡️ 3. 예외 처리 및 복구 메커니즘
본 시스템은 파일 손상이나 누락에 대비하여 2단계 방어 체계를 갖추고 있습니다.

Primary Load: state.json 로드를 시도합니다.
Exception Propagation: 파일이 없거나 형식이 깨진 경우 raise를 통해 상위로 예외를 던집니다.
Secondary Recovery: 예외 발생 시 즉시 basic_data.json(공장 초기화 데이터)을 로드하여 프로그램이 비정상 종료되지 않도록 복구합니다.
Validation: 로드된 모든 데이터는 check_ 계열 함수를 통해 런타임 에러 가능성을 사전에 차단합니다.
📊 4. 성능 및 확장성 분석
🚀 대용량 데이터(1,000개 이상) 처리
현상: 현재 구조는 모든 JSON 데이터를 메모리에 적재(Full Loading)합니다. 데이터가 수만 건 이상이 되면 초기 로딩 속도와 RAM 사용량이 증가할 수 있습니다.
개선안:
SQLite 도입: 대용량 데이터의 경우 파일 대신 DB를 사용하여 필요한 문항만 쿼리(Query)하도록 개선 가능합니다.
Lazy Loading: 퀴즈를 시작할 때 전체를 로드하지 않고, 페이지 단위로 읽어오는 방식을 적용할 수 있습니다.
🌿 5. 개발 협업 및 커밋 규칙
🌳 브랜치 전략
main: 최종 배포 및 안정화 버전.
feature/**: 새로운 기능 개발(예: feature/add-timer)을 위한 독립 브랜치.
✉️ 커밋 메시지 규칙 (Conventional Commits)
Feat: 새로운 기능 구현
Fix: 버그 수정
Docs: 문서 수정 (README 등)
Refactor: 코드 구조 개선 (기능 변경 없음)
🎓 6. 학습 포인트
데이터 주도 설계: 코드 수정 없이 JSON 파일만으로 게임의 모든 설정과 콘텐츠를 제어합니다.
방어적 프로그래밍: 사용자의 잘못된 입력이나 파일 오류에도 시스템이 견고하게 동작하도록 설계했습니다.
객체지향(OOP): 각 클래스가 명확한 책임(데이터 관리 vs 흐름 제어)을 가지도록 분리하여 유지보수성을 높였습니다.
Created by [bs7703] - 2024 Python Study Project