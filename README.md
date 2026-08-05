# Python 기초 퀴즈 게임

Python 기본 문법, 클래스, JSON 파일 입출력, 예외 처리를 연습하기 위해 만든 터미널 퀴즈 게임입니다. 퀴즈 풀기, 퀴즈 추가, 목록 보기, 최고 점수 확인 기능을 제공하며 프로그램을 다시 실행해도 추가한 퀴즈와 최고 점수가 유지됩니다.

## 프로젝트 개요

이 프로젝트의 목표는 동작하는 콘솔 프로그램을 처음부터 끝까지 구현하며 다음 내용을 익히는 것입니다.

- 변수와 `int`, `str`, `bool`, `list`, `dict` 자료형
- `if/elif/else` 조건문과 `for`, `while` 반복문
- 함수의 매개변수와 반환값
- 클래스, 객체, `__init__`, `self`, 속성, 메서드
- `try/except`를 활용한 예외 처리
- UTF-8 JSON 파일 저장 및 불러오기
- Git 커밋, 브랜치, 병합, clone, pull 흐름

## 퀴즈 주제와 선정 이유

퀴즈 주제는 **Python 기초**입니다. 프로그램을 만들면서 사용하는 변수, 자료형, 조건문, 반복문, 함수, 클래스 등의 개념을 퀴즈로 다시 확인하면 학습 내용을 반복해서 복습할 수 있기 때문에 이 주제를 선택했습니다.

기본 퀴즈 5개가 포함되어 있으며 사용자가 직접 새 문제를 추가할 수 있습니다.

## 개발 환경

| 항목 | 내용 |
| --- | --- |
| 운영체제 | macOS |
| 개발 도구 | Visual Studio Code |
| Python | 3.10 이상 |
| 버전 관리 | Git / GitHub |
| 외부 라이브러리 | 사용하지 않음 |

## 실행 방법

### 저장소 복제

```bash
git clone https://github.com/dlckdwls76/CodysseyMission_E1_2.git
cd CodysseyMission_E1_2
```

### Python 버전 확인

```bash
python3 --version
```

### 프로그램 실행

```bash
python3 main.py
```

실행하면 다음 메뉴가 나타납니다.

```text
========================================
        Python 기초 퀴즈 게임
========================================
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 종료
========================================
```

### 테스트 실행

외부 라이브러리 없이 Python 표준 라이브러리인 `unittest`를 사용합니다.

```bash
python3 -m unittest discover -s tests -v
```

## 기능 목록

### 퀴즈 풀기

- 저장된 퀴즈를 차례대로 출제합니다.
- 문제마다 4개의 선택지를 표시합니다.
- 정답 번호를 입력하면 정답 또는 오답 여부를 알려 줍니다.
- 모든 문제를 풀면 정답 수와 100점 기준 점수를 표시합니다.
- 기존 최고 점수보다 높으면 최고 기록을 갱신합니다.

### 퀴즈 추가

- 문제, 선택지 4개, 정답 번호를 입력하여 문제를 추가합니다.
- 빈 입력과 범위를 벗어난 정답 번호를 처리합니다.
- 추가한 문제를 `state.json`에 즉시 저장합니다.

### 퀴즈 목록

- 저장된 퀴즈의 번호와 문제 내용을 확인합니다.
- 퀴즈가 없는 경우 안내 메시지를 표시합니다.

### 점수 확인

- 최고 점수, 정답 수, 전체 문제 수를 확인합니다.
- 아직 게임을 하지 않은 경우 기록이 없음을 알려 줍니다.

### 예외 처리와 안전한 종료

- 입력값 앞뒤 공백 제거
- 빈 입력 처리
- 숫자가 아닌 입력 처리
- 허용 범위를 벗어난 숫자 처리
- 잘못된 입력 후 재입력
- `Ctrl+C`와 `EOFError` 발생 시 저장 후 안전하게 종료
- `state.json`이 없을 때 기본 퀴즈 사용
- `state.json`이 손상되었을 때 기본 데이터로 복구
- 파일 읽기와 쓰기 오류 안내

## 클래스 구조

### `Quiz`

개별 퀴즈 한 문제를 표현합니다.

| 종류 | 이름 | 역할 |
| --- | --- | --- |
| 속성 | `question` | 문제 내용 |
| 속성 | `choices` | 선택지 4개 |
| 속성 | `answer` | 1~4 범위의 정답 번호 |
| 메서드 | `display()` | 문제와 선택지 출력 |
| 메서드 | `check_answer()` | 사용자 답과 정답 비교 |
| 메서드 | `to_dict()` | JSON 저장용 딕셔너리 변환 |
| 메서드 | `from_dict()` | 딕셔너리에서 객체 생성 |

### `QuizGame`

게임 전체 흐름과 데이터를 관리합니다.

| 종류 | 이름 | 역할 |
| --- | --- | --- |
| 속성 | `quizzes` | `Quiz` 객체 목록 |
| 속성 | `best_score` | 최고 점수 기록 |
| 메서드 | `run()` | 메뉴 반복과 안전한 종료 관리 |
| 메서드 | `play_quiz()` | 문제 출제와 점수 계산 |
| 메서드 | `add_quiz()` | 새 문제 등록 |
| 메서드 | `list_quizzes()` | 문제 목록 출력 |
| 메서드 | `show_best_score()` | 최고 점수 출력 |
| 메서드 | `load_state()` | JSON 데이터 불러오기 |
| 메서드 | `save_state()` | JSON 데이터 저장하기 |

## 파일 구조

```text
CodysseyMission_E1_2/
├── main.py
├── state.json
├── README.md
├── .gitignore
├── tests/
│   └── test_quiz.py
└── docs/
    ├── GIT_PRACTICE.md
    └── screenshots/
        └── README.md
```

| 경로 | 역할 |
| --- | --- |
| `main.py` | `Quiz`, `QuizGame` 클래스와 실행 코드 |
| `state.json` | 퀴즈와 최고 점수 저장 파일 |
| `tests/test_quiz.py` | 핵심 클래스와 파일 저장 기능 테스트 |
| `docs/GIT_PRACTICE.md` | clone, pull 등 Git 명령 실습 기록 안내 |
| `docs/screenshots/` | 제출용 실행 화면 이미지 보관 |

## state.json 설명

데이터는 프로젝트 루트의 `state.json`에 UTF-8로 저장합니다.

```json
{
  "quizzes": [
    {
      "question": "Python에서 문자열을 나타내는 자료형은?",
      "choices": ["int", "str", "bool", "list"],
      "answer": 2
    }
  ],
  "best_score": {
    "correct": 4,
    "total": 5,
    "score": 80
  }
}
```

| 필드 | 자료형 | 설명 |
| --- | --- | --- |
| `quizzes` | `list` | 전체 퀴즈 목록 |
| `question` | `str` | 문제 내용 |
| `choices` | `list` | 4개의 선택지 |
| `answer` | `int` | 1~4 범위의 정답 번호 |
| `best_score` | `dict` 또는 `null` | 최고 정답 수, 문제 수, 점수 |

## Git 작업 확인

전체 커밋과 브랜치 병합 기록은 다음 명령으로 확인합니다.

```bash
git log --oneline --graph --all --decorate
```

개발이 끝난 뒤 clone과 pull 실습은 [Git 실습 안내](docs/GIT_PRACTICE.md)에 따라 직접 수행하고 결과를 캡처합니다.

## 실행 화면

아래 화면을 직접 실행한 후 `docs/screenshots/`에 저장합니다.

- `environment.png`: VS Code, Python 버전, Git 설정
- `menu.png`: 메인 메뉴
- `play.png`: 퀴즈 풀기
- `add_quiz.png`: 퀴즈 추가
- `list.png`: 퀴즈 목록
- `score.png`: 최고 점수 확인
- `git-log.png`: `git log --oneline --graph --all --decorate` 결과

## 제출 전 체크리스트

- [x] Python 3.10 이상에서 실행 가능한 코드 작성
- [x] 기본 퀴즈 5개 이상 작성
- [x] 퀴즈 풀기, 추가, 목록, 점수 확인, 종료 기능 구현
- [x] `Quiz`, `QuizGame` 클래스 정의
- [x] 잘못된 입력과 종료 예외 처리
- [x] `state.json` 저장 및 불러오기 구현
- [x] 데이터 파일 없음 또는 손상 상황 처리
- [x] GitHub 공개 저장소에 프로젝트 파일 구성
- [ ] 로컬 터미널에서 Git 명령어 7종 직접 실행
- [ ] clone 후 변경·push하고 기존 폴더에서 pull 실습
- [ ] 개발 환경과 프로그램 실행 화면 캡처 추가
- [ ] 최종 `git log` 화면 캡처 추가

## 저장소

- GitHub: <https://github.com/dlckdwls76/CodysseyMission_E1_2>
- 작성자: 이창진

