"""퀴즈 데이터 모델과 기본 문제를 정의한다."""

from __future__ import annotations

from typing import Any

CHOICE_COUNT = 4


class Quiz:
    """문제, 선택지 네 개, 정답 번호를 표현하는 클래스."""

    def __init__(self, question: str, choices: list[str], answer: int) -> None:
        question = question.strip()
        cleaned_choices = [str(choice).strip() for choice in choices]
        if not question:
            raise ValueError("문제는 비어 있을 수 없습니다.")
        if len(cleaned_choices) != CHOICE_COUNT:
            raise ValueError(f"선택지는 정확히 {CHOICE_COUNT}개여야 합니다.")
        if any(not choice for choice in cleaned_choices):
            raise ValueError("선택지는 비어 있을 수 없습니다.")
        if answer not in range(1, CHOICE_COUNT + 1):
            raise ValueError(f"정답 번호는 1~{CHOICE_COUNT} 사이여야 합니다.")
        self.question = question
        self.choices = cleaned_choices
        self.answer = answer

    def display(self, number: int | None = None) -> None:
        print("\n" + "-" * 40)
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def check_answer(self, user_answer: int) -> bool:
        return user_answer == self.answer

    def to_dict(self) -> dict[str, Any]:
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Quiz":
        return cls(str(data["question"]), list(data["choices"]), int(data["answer"]))


def create_default_quizzes() -> list[Quiz]:
    """첫 실행 또는 파일 복구 때 사용할 기본 퀴즈를 반환한다."""
    return [
        Quiz("Python에서 문자열을 나타내는 자료형은?", ["int", "str", "bool", "list"], 2),
        Quiz("조건에 따라 다른 코드를 실행할 때 사용하는 키워드는?", ["if", "for", "def", "import"], 1),
        Quiz("여러 값을 순서대로 저장하는 자료형은?", ["bool", "float", "list", "None"], 3),
        Quiz("함수를 정의할 때 사용하는 키워드는?", ["class", "return", "while", "def"], 4),
        Quiz("클래스의 인스턴스 자신을 가리키는 관례적인 이름은?", ["this", "self", "me", "object"], 2),
    ]
