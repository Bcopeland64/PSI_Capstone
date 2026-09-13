import tempfile
from pathlib import Path

from src.database import Database
from src.logic import InvestigationService


def test_suspect_score_is_ranked_by_reliability():
    with tempfile.TemporaryDirectory() as tmp:
        db = Database(str(Path(tmp) / "test.db"))
        service = InvestigationService(db)

        case_id = service.add_case(
            "Test Case", "Victim", "Vienna", "2026-09-01"
        )
        suspect_a = service.add_suspect(
            case_id, "A", 30, "Engineer", "Friend", "Alibi"
        )
        suspect_b = service.add_suspect(
            case_id, "B", 30, "Teacher", "Friend", "Alibi"
        )
        service.add_evidence(
            case_id, "DNA", "Strong evidence", 95, suspect_a
        )
        service.add_evidence(
            case_id, "Witness", "Weak evidence", 40, suspect_b
        )

        scores = service.calculate_scores(case_id)
        assert scores[0]["name"] == "A"
        assert scores[0]["score"] > scores[1]["score"]

        db.close()
