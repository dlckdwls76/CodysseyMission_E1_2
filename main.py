"""터미널에서 실행하는 Python 기초 퀴즈 게임."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STATE_FILE = Path(__file__).resolve().parent / "state.json"


class Quiz:
    """문제, 선택지 네 개, 정답 번호를 표현하는 클래스."""

    def __init__(self, question: str, choices: list[str], answer: int) -> None:
        question = question.strip()
        cleaned_choices = [str(choice).strip() for choice in choices]

        if not question:
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if len(cleaned_choices) != 4:
            raise ValueError("선택지는 정확히 4개여야 합니다.")
        if any(not choice for choice in cleaned_choices):
            raise ValueError("선택지는 비어 있을 수 없습니다.")
        if answer not in range(1, 5):
            raise ValueError("정답 번호는 1~4 사이여야 합니다.")

        self.question = question
        self.choices = cleaned_choices
        self.answer = answer

    def display(self, number: int | None = None) -> None:
        """문제와 선택지를 터미널에 출력한다."""
        print("\n" + "-" * 40)
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def check_answer(self, user_answer: int) -> bool:
        """입력한 번호가 정답인지 반환한다."""
        return user_answer == self.answer

    def to_dict(self) -> dict[str, Any]:
        """JSON으로 저장할 수 있는 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Quiz":
        """딕셔너리 데이터로 Quiz 객체를 만든다."""
        return cls(
            question=str(data["question"]),
            choices=list(data["choices"]),
            answer=int(data["answer"]),
        )


def create_default_quizzes() -> list[Quiz]:
    """첫 실행 또는 파일 복구 때 사용할 기본 퀴즈를 반환한다."""
    return [
        Quiz(
            "Python에서 문자열을 나타내는 자료형은?",
            ["int", "str", "bool", "list"],
            2,
        ),
        Quiz(
            "조건에 따라 다른 코드를 실행할 때 사용하는 키워드는?",
            ["if", "for", "def", "import"],
            1,
        ),
        Quiz(
            "여러 값을 순서대로 저장하는 자료형은?",
            ["bool", "float", "list", "None"],
            3,
        ),
        Quiz(
            "함수를 정의할 때 사용하는 키워드는?",
            ["class", "return", "while", "def"],
            4,
        ),
        Quiz(
            "클래스의 인스턴스 자신을 가리키는 관례적인 이름은?",
            ["this", "self", "me", "object"],
            2,
        ),
    ]


class QuizGame:
    """메뉴, 퀴즈 진행, 점수, 파일 저장을 관리하는 클래스."""

    def __init__(
        self,
        state_file: Path | str = STATE_FILE,
        *,
        auto_load: bool = True,
    ) -> None:
        self.state_file = Path(state_file)
        self.quizzes: list[Quiz] = []
        self.best_score: dict[str, int] | None = None

        if auto_load:
            self.load_state()

    @staticmethod
    def read_number(prompt: str, minimum: int, maximum: int) -> int:
        """범위 안의 정수를 입력할 때까지 반복한다."""
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
        """비어 있지 않은 문자열을 입력할 때까지 반복한다."""
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
            quiz.display(number)
            user_answer = self.read_number("정답 입력 (1-4): ", 1, 4)

            if quiz.check_answer(user_answer):
                correct += 1
                print("✅ 정답입니다!")
            else:
                correct_choice = quiz.choices[quiz.answer - 1]
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 ({correct_choice})입니다.")

        score = round(correct / total * 100)
        print("\n" + "=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")

        if self.best_score is None or score > self.best_score["score"]:
            self.best_score = {
                "correct": correct,
                "total": total,
                "score": score,
            }
            print("🎉 새로운 최고 점수입니다!")
            self.save_state()
        else:
            print(f"현재 최고 점수는 {self.best_score['score']}점입니다.")
        print("=" * 40)

    def add_quiz(self) -> None:
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self.read_text("문제를 입력하세요: ")
        choices = [
            self.read_text(f"선택지 {number}: ")
            for number in range(1, 5)
        ]
        answer = self.read_number("정답 번호 (1-4): ", 1, 4)

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
            f"({self.best_score['total']}문제 중 "
            f"{self.best_score['correct']}문제 정답)"
        )

    def reset_to_defaults(self) -> None:
        self.quizzes = create_default_quizzes()
        self.best_score = None

    def load_state(self) -> None:
        """state.json을 불러오고 문제가 있으면 기본 데이터로 복구한다."""
        try:
            with self.state_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes_data = data["quizzes"]
            if not isinstance(quizzes_data, list):
                raise ValueError("quizzes는 목록이어야 합니다.")

            self.quizzes = [Quiz.from_dict(item) for item in quizzes_data]
            best_score = data.get("best_score")
            if best_score is not None:
                required_keys = {"correct", "total", "score"}
                if not isinstance(best_score, dict) or not required_keys.issubset(best_score):
                    raise ValueError("best_score 형식이 올바르지 않습니다.")
                self.best_score = {
                    "correct": int(best_score["correct"]),
                    "total": int(best_score["total"]),
                    "score": int(best_score["score"]),
                }
            else:
                self.best_score = None

            print(
                f"📂 저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(self.quizzes)}개)"
            )
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
        """현재 퀴즈와 최고 점수를 UTF-8 JSON 파일로 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }

        try:
            with self.state_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return True
        except OSError as error:
            print(f"⚠️ 데이터를 저장할 수 없습니다: {error}")
            return False

    def run(self) -> None:
        """메뉴를 반복 실행하고 예외 발생 시 안전하게 종료한다."""
        try:
            while True:
                self.show_menu()
                menu_number = self.read_number("선택: ", 1, 5)

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
                    return
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다.")
            self.save_state()
            print("가능한 데이터를 저장하고 안전하게 종료합니다.")


def main() -> None:
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()

