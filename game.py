"""터미널 퀴즈 게임의 진행과 사용자 입출력을 담당한다."""

import json
from pathlib import Path

from quiz import CHOICE_COUNT, Quiz, create_default_quizzes
from storage import STATE_FILE, StateStore


class QuizGame:
    """메뉴, 퀴즈 진행, 점수와 저장 흐름을 관리한다."""

    def __init__(self, state_file: Path | str = STATE_FILE, *, auto_load: bool = True) -> None:
        self.store = StateStore(state_file)
        self.state_file = self.store.state_file
        self.quizzes: list[Quiz] = []
        self.best_score: dict[str, int] | None = None
        if auto_load:
            self.load_state()

    @staticmethod
    def read_number(prompt: str, minimum: int, maximum: int) -> int:
        while True:
            raw_value = input(prompt).strip()
            if not raw_value:
                print("⚠️ 빈 입력은 사용할 수 없습니다. 다시 입력하세요.")
                continue
            try:
                value = int(raw_value)
            except ValueError:
                print(f"⚠️ {minimum}~{maximum} 사이의 숫자를 입력하세요.")
                continue
            if value < minimum or value > maximum:
                print(f"⚠️ {minimum}~{maximum} 사이의 숫자를 입력하세요.")
                continue
            return value

    @staticmethod
    def read_text(prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("⚠️ 빈 입력은 사용할 수 없습니다. 다시 입력하세요.")

    def show_menu(self) -> None:
        print("\n" + "=" * 40)
        print("        Python 기초 퀴즈 게임")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def play_quiz(self) -> None:
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return
        total = len(self.quizzes)
        correct = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")
        for number, quiz in enumerate(self.quizzes, start=1):
            if self.ask_quiz(quiz, number):
                correct += 1
        score = self.calculate_score(correct, total)
        print("\n" + "=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.update_best_score(correct, total, score):
            print("🎉 새로운 최고 점수입니다!")
            self.save_state()
        else:
            print(f"현재 최고 점수는 {self.best_score['score']}점입니다.")
        print("=" * 40)

    def ask_quiz(self, quiz: Quiz, number: int) -> bool:
        quiz.display(number)
        user_answer = self.read_number(f"정답 입력 (1-{CHOICE_COUNT}): ", 1, CHOICE_COUNT)
        if quiz.check_answer(user_answer):
            print("✅ 정답입니다!")
            return True
        correct_choice = quiz.choices[quiz.answer - 1]
        print(f"❌ 오답입니다. 정답은 {quiz.answer}번 ({correct_choice})입니다.")
        return False

    @staticmethod
    def calculate_score(correct: int, total: int) -> int:
        return round(correct / total * 100)

    def update_best_score(self, correct: int, total: int, score: int) -> bool:
        if self.best_score is not None and score <= self.best_score["score"]:
            return False
        self.best_score = {"correct": correct, "total": total, "score": score}
        return True

    def add_quiz(self) -> None:
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self.read_text("문제를 입력하세요: ")
        choices = [self.read_text(f"선택지 {number}: ") for number in range(1, CHOICE_COUNT + 1)]
        answer = self.read_number(f"정답 번호 (1-{CHOICE_COUNT}): ", 1, CHOICE_COUNT)
        self.quizzes.append(Quiz(question, choices, answer))
        if self.save_state():
            print("✅ 퀴즈가 추가되고 저장되었습니다!")
        else:
            print("⚠️ 퀴즈는 추가되었지만 파일 저장에는 실패했습니다.")

    def list_quizzes(self) -> None:
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def show_best_score(self) -> None:
        if self.best_score is None:
            print("\n📭 아직 퀴즈를 푼 기록이 없습니다.")
            return
        print(
            "\n🏆 최고 점수: "
            f"{self.best_score['score']}점 "
            f"({self.best_score['total']}문제 중 {self.best_score['correct']}문제 정답)"
        )

    def reset_to_defaults(self) -> None:
        self.quizzes = create_default_quizzes()
        self.best_score = None

    def load_state(self) -> None:
        try:
            self.quizzes, self.best_score = self.store.load()
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)")
        except FileNotFoundError:
            print("📂 저장 파일이 없어 기본 퀴즈를 사용합니다.")
            self.reset_to_defaults()
            self.save_state()
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print(f"⚠️ 저장 파일이 손상되었습니다: {error}")
            print("기본 퀴즈 데이터로 복구합니다.")
            self.reset_to_defaults()
            self.save_state()
        except OSError as error:
            print(f"⚠️ 저장 파일을 읽을 수 없습니다: {error}")
            print("현재 실행에서는 기본 퀴즈를 사용합니다.")
            self.reset_to_defaults()

    def save_state(self) -> bool:
        try:
            self.store.save(self.quizzes, self.best_score)
            return True
        except OSError as error:
            print(f"⚠️ 데이터를 저장할 수 없습니다: {error}")
            return False

    def handle_menu(self, menu_number: int) -> bool:
        if menu_number == 1:
            self.play_quiz()
        elif menu_number == 2:
            self.add_quiz()
        elif menu_number == 3:
            self.list_quizzes()
        elif menu_number == 4:
            self.show_best_score()
        else:
            self.save_state()
            print("\n👋 데이터를 저장하고 게임을 종료합니다.")
            return False
        return True

    def run(self) -> None:
        try:
            while True:
                self.show_menu()
                if not self.handle_menu(self.read_number("선택: ", 1, 5)):
                    return
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다.")
            self.save_state()
            print("가능한 데이터를 저장하고 안전하게 종료합니다.")
