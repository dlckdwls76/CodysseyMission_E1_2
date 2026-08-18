"""Python 기초 퀴즈 게임의 실행 진입점."""

from game import QuizGame
from quiz import Quiz, create_default_quizzes

__all__ = ["Quiz", "QuizGame", "create_default_quizzes", "main"]


def main() -> None:
    """게임을 생성하고 실행한다."""
    QuizGame().run()


if __name__ == "__main__":
    main()
