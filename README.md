# 🚀 Python Quiz Game Project
> **안정적인 데이터 관리와 객체지향 설계를 적용한 지능형 퀴즈 시스템**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

본 프로젝트는 단순한 퀴즈 프로그램을 넘어, **데이터 무결성 검증, 2단계 예외 복구, 상수 기반 설정 관리** 등 실무적인 소프트웨어 설계 원칙을 학습하고 적용한 결과물입니다.

---

## 📌 핵심 기능 (Key Features)
- **데이터 분리**: 로직(Python)과 데이터(JSON)를 완벽히 분리하여 유지보수 용이
- **강력한 검증**: 모든 입력값과 JSON 데이터에 대한 전수 검사(`Check_**` 로직)
- **자동 복구**: 파일 손상 시 백업 데이터(`basic_data.json`)로 즉시 복구
- **동적 설정**: `config.json` 수정을 통해 게임 난이도 및 UI 스타일 실시간 변경

---

## 📂 프로젝트 구조 (Architecture)
```bash
.
├── main.py              # [Entry Point] 프로그램 시작 및 메인 루프 실행
├── quiz_game.py         # [Controller] 핵심 비즈니스 로직 및 데이터 관리
├── quiz.py              # [Model] 퀴즈 객체 정의 및 채점 로직
├── constants.py         # [Config] 시스템 상수, 메시지, 기본값 관리
├── config.json          # [Settings] UI 및 게임 규칙 설정 데이터
├── state.json           # [Database] 사용자 진행 상태 및 퀴즈 저장소
└── basic_data.json      # [Backup] 시스템 복구용 초기 백업 데이터
```

---

## 🛠 클래스별 상세 명세 (Full API Reference)

모든 함수는 데이터의 안전성과 사용자 경험을 최우선으로 설계되었습니다. 각 항목을 클릭하여 상세 내용을 확인하세요.

<details>
<summary><b>1. QuizGame 클래스 (핵심 제어부) - 상세 보기</b></summary>
<div markdown="1">

### 🔹 초기화 및 데이터 검증
- **`__init__()`**: 시스템 환경 구축 및 데이터 로드 프로세스 시작.
- **`load_config()`**: 설정 파일을 읽어 게임 환경(UI, 계수 등)을 메모리에 적재.
- **`check_config(config)`**: 로드된 설정값의 필수 키 존재 여부 및 데이터 타입 검증.
- **`normalize_settings()`**: 설정값이 비정상적일 경우 `constants`의 기본값으로 자동 치환.
- **`load_data()`**: 사용자 데이터(`state.json`) 로드 및 실패 시 예외 전파.
- **`check_data(data)`**: 퀴즈 문항의 구조(질문, 보기, 정답 등)가 스키마에 맞는지 전수 검사.
- **`check_score_list(data)`**: 누적된 점수 기록 데이터의 손상 여부 확인.

### 🔹 입력 핸들링
- **`advanced_input(prompt, min, max)`**: 숫자 입력 전용. 범위 밖의 값이나 문자 입력 시 재입력을 유도하며 `EOFError` 등 예외 방어.
- **`advanced_strinput(prompt)`**: 문자열 입력 전용. 빈 값이나 너무 짧은/긴 입력(5~50자)을 제한.

### 🔹 게임 흐름 제어
- **`run()`**: 메인 메뉴 루프를 관리하며 프로그램의 생명 주기 제어.
- **`display_menu()`**: `config`에 설정된 테마에 맞춰 메뉴 화면 렌더링.
- **`execute_menu_option(choice)`**: 사용자의 메뉴 선택에 따른 기능 분기 처리.
- **`start_quiz()`**: 퀴즈 세션 생성, 문제 셔플, 최종 점수 산출 및 기록 갱신.
- **`solve_quiz(quiz, cur, total)`**: 개별 문제의 UI 출력, 힌트 사용 처리 및 실시간 채점.

### 🔹 데이터 유지보수
- **`add_quiz()`**: 새로운 퀴즈를 입력받아 검증 후 리스트에 동적 추가.
- **`del_quiz()`**: 인덱스 기반으로 문제를 안전하게 삭제하고 데이터 동기화.
- **`save_quiz()`**: 현재의 모든 상태(퀴즈, 점수)를 JSON 파일로 물리적 저장.

</div>
</details>

<details>
<summary><b>2. Quiz 클래스 (데이터 모델) - 상세 보기</b></summary>
<div markdown="1">

- **`__init__(data)`**: 딕셔너리 데이터를 객체 속성으로 변환하여 캡슐화.
- **`show_quiz()`**: 질문과 4지선다형 보기를 가독성 있게 포맷팅하여 출력.
- **`check_answers(user_input, used_hint, factors)`**: 
  - 정답 여부 판별.
  - 힌트 사용 시 점수 차감 적용.
  - 오답 시 설정된 계수(`factors`)에 따른 감점 로직 수행.
- **`show_hint()`**: 문제에 포함된 힌트 텍스트 반환.
- **`get_explanation()`**: 정답 확인 후 사용자 학습을 위한 상세 해설 제공.

</div>
</details>

---

## 🛡️ 예외 처리 및 복구 시스템
프로그램의 중단 없는 실행을 위해 **2단계 복구 메커니즘**을 적용했습니다.

1.  **예외 감지**: `state.json` 로드 중 `FileNotFound` 또는 `JSONDecodeError` 발생 시 즉시 감지.
2.  **강제 전파**: `raise`를 통해 상위 로직으로 에러를 전달하여 불완전한 상태로 실행되는 것을 방지.
3.  **최종 복구**: 예외 발생 시 즉시 `basic_data.json`을 로드하여 시스템을 초기 상태로 복구하고 실행 유지.

---

## 📈 성능 분석 및 확장 계획
- **대용량 데이터 처리**: 현재의 JSON 로드 방식은 1,000개 이상의 데이터에서 메모리 병목이 발생할 수 있습니다. 향후 **SQLite DB** 도입을 통해 필요한 데이터만 쿼리하는 방식으로 개선할 예정입니다.
- **Git 전략**: `feature/` 브랜치를 활용한 기능 단위 개발과 `Conventional Commits` 규칙을 준수하여 협업 효율성을 높였습니다.

---

## ✍️ 학습 포인트
- **Data-Driven**: 코드를 고치지 않고 데이터 파일만으로 프로그램의 동작을 제어하는 설계 학습.
- **Robustness**: 수많은 `check_` 함수를 통해 "터지지 않는 프로그램"을 만드는 방어적 프로그래밍 실천.
- **OOP**: 각 클래스에 명확한 역할과 책임을 부여하여 코드 재사용성 극대화.

---
