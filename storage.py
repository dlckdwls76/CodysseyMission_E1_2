"""퀴즈 게임의 JSON 저장과 롤링 백업을 담당한다."""

import json
import shutil
from pathlib import Path
from typing import Any

from quiz import Quiz

STATE_FILE = Path(__file__).resolve().parent / "state.json"
BACKUP_LIMIT = 3


class StateStore:
    """게임 상태의 직렬화, 파일 입출력, 백업을 관리한다."""

    def __init__(self, state_file: Path | str = STATE_FILE) -> None:
        self.state_file = Path(state_file)

    def load(self) -> tuple[list[Quiz], dict[str, int] | None]:
        with self.state_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
        quizzes_data = data["quizzes"]
        if not isinstance(quizzes_data, list):
            raise ValueError("quizzes는 목록이어야 합니다.")
        quizzes = [Quiz.from_dict(item) for item in quizzes_data]
        return quizzes, self.parse_best_score(data.get("best_score"))

    def save(self, quizzes: list[Quiz], best_score: dict[str, int] | None) -> None:
        self.create_backup()
        with self.state_file.open("w", encoding="utf-8") as file:
            json.dump(self.to_dict(quizzes, best_score), file, ensure_ascii=False, indent=2)

    @staticmethod
    def parse_best_score(best_score: Any) -> dict[str, int] | None:
        if best_score is None:
            return None
        required_keys = {"correct", "total", "score"}
        if not isinstance(best_score, dict) or not required_keys.issubset(best_score):
            raise ValueError("best_score 형식이 올바르지 않습니다.")
        return {
            "correct": int(best_score["correct"]),
            "total": int(best_score["total"]),
            "score": int(best_score["score"]),
        }

    @staticmethod
    def to_dict(quizzes: list[Quiz], best_score: dict[str, int] | None) -> dict[str, Any]:
        return {"quizzes": [quiz.to_dict() for quiz in quizzes], "best_score": best_score}

    def backup_path(self, version: int) -> Path:
        return self.state_file.with_name(f"{self.state_file.name}.bak.{version}")

    def create_backup(self) -> None:
        if not self.state_file.exists():
            return
        for version in range(BACKUP_LIMIT, 1, -1):
            older_backup = self.backup_path(version - 1)
            next_backup = self.backup_path(version)
            if older_backup.exists():
                older_backup.replace(next_backup)
        shutil.copy2(self.state_file, self.backup_path(1))
