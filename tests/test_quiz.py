import json
import tempfile
import unittest
from pathlib import Path

from main import Quiz, QuizGame, create_default_quizzes


class QuizTest(unittest.TestCase):
    def test_check_answer(self) -> None:
        quiz = Quiz("정답은?", ["1", "2", "3", "4"], 3)

        self.assertTrue(quiz.check_answer(3))
        self.assertFalse(quiz.check_answer(1))

    def test_quiz_requires_four_choices(self) -> None:
        with self.assertRaises(ValueError):
            Quiz("문제", ["1", "2", "3"], 1)

    def test_quiz_round_trip(self) -> None:
        quiz = Quiz("문제", ["하나", "둘", "셋", "넷"], 2)

        restored_quiz = Quiz.from_dict(quiz.to_dict())

        self.assertEqual(restored_quiz.question, "문제")
        self.assertEqual(restored_quiz.choices, ["하나", "둘", "셋", "넷"])
        self.assertEqual(restored_quiz.answer, 2)


class QuizGameTest(unittest.TestCase):
    def test_default_quizzes_are_at_least_five(self) -> None:
        self.assertGreaterEqual(len(create_default_quizzes()), 5)

    def test_calculate_score(self) -> None:
        self.assertEqual(QuizGame.calculate_score(4, 5), 80)

    def test_update_best_score_only_keeps_higher_score(self) -> None:
        game = QuizGame(auto_load=False)

        self.assertTrue(game.update_best_score(3, 5, 60))
        self.assertFalse(game.update_best_score(2, 5, 40))
        self.assertEqual(game.best_score, {"correct": 3, "total": 5, "score": 60})

    def test_save_and_load_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_file = Path(directory) / "state.json"
            game = QuizGame(state_file, auto_load=False)
            game.quizzes = create_default_quizzes()
            game.best_score = {"correct": 4, "total": 5, "score": 80}

            self.assertTrue(game.save_state())

            loaded_game = QuizGame(state_file)
            self.assertEqual(len(loaded_game.quizzes), 5)
            self.assertEqual(loaded_game.best_score["score"], 80)

            with state_file.open("r", encoding="utf-8") as file:
                saved_data = json.load(file)
            self.assertIn("quizzes", saved_data)
            self.assertIn("best_score", saved_data)

    def test_missing_state_uses_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_file = Path(directory) / "missing.json"

            game = QuizGame(state_file)

            self.assertGreaterEqual(len(game.quizzes), 5)
            self.assertTrue(state_file.exists())

    def test_broken_state_recovers_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_file = Path(directory) / "state.json"
            state_file.write_text("{broken json", encoding="utf-8")

            game = QuizGame(state_file)

            self.assertGreaterEqual(len(game.quizzes), 5)
            self.assertIsNone(game.best_score)

    def test_save_state_keeps_three_rolling_backups(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state_file = Path(directory) / "state.json"
            game = QuizGame(state_file, auto_load=False)
            game.quizzes = create_default_quizzes()

            for score in (10, 20, 30, 40, 50):
                game.best_score = {"correct": 1, "total": 5, "score": score}
                self.assertTrue(game.save_state())

            backups = [
                state_file.with_name(f"state.json.bak.{version}")
                for version in range(1, 4)
            ]
            self.assertTrue(all(backup.exists() for backup in backups))
            self.assertFalse(state_file.with_name("state.json.bak.4").exists())

            backup_scores = []
            for backup in backups:
                with backup.open("r", encoding="utf-8") as file:
                    backup_scores.append(json.load(file)["best_score"]["score"])
            self.assertEqual(backup_scores, [40, 30, 20])


if __name__ == "__main__":
    unittest.main()
