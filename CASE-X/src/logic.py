from collections import defaultdict
from .database import Database


class InvestigationService:
    """Business logic for cases, suspects, evidence and scoring."""

    def __init__(self, db: Database):
        self.db = db

    def add_case(self, title, victim, location, case_date, status="Open"):
        cur = self.db.execute(
            """INSERT INTO cases(title, victim, location, case_date, status)
               VALUES (?, ?, ?, ?, ?)""",
            (title, victim, location, case_date, status),
        )
        return cur.lastrowid

    def add_suspect(self, case_id, name, age, occupation, relationship, alibi):
        cur = self.db.execute(
            """INSERT INTO suspects
               (case_id, name, age, occupation, relationship, alibi)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (case_id, name, age, occupation, relationship, alibi),
        )
        return cur.lastrowid

    def add_evidence(
        self, case_id, evidence_type, description, reliability, suspect_id=None
    ):
        cur = self.db.execute(
            """INSERT INTO evidence
               (case_id, suspect_id, evidence_type, description, reliability)
               VALUES (?, ?, ?, ?, ?)""",
            (case_id, suspect_id, evidence_type, description, reliability),
        )
        return cur.lastrowid

    def list_cases(self):
        return self.db.fetchall("SELECT * FROM cases ORDER BY id DESC")

    def get_case(self, case_id):
        return self.db.fetchone("SELECT * FROM cases WHERE id = ?", (case_id,))

    def get_suspects(self, case_id):
        return self.db.fetchall(
            "SELECT * FROM suspects WHERE case_id = ? ORDER BY id", (case_id,)
        )

    def get_evidence(self, case_id):
        return self.db.fetchall(
            """SELECT e.*, s.name AS suspect_name
               FROM evidence e
               LEFT JOIN suspects s ON e.suspect_id = s.id
               WHERE e.case_id = ?
               ORDER BY e.id""",
            (case_id,),
        )

    def calculate_scores(self, case_id):
        """Return suspects ranked by a transparent evidence-based score."""
        suspects = self.get_suspects(case_id)
        evidence = self.get_evidence(case_id)

        grouped = defaultdict(list)
        for item in evidence:
            if item["suspect_id"] is not None:
                grouped[item["suspect_id"]].append(item)

        results = []
        for suspect in suspects:
            items = grouped[suspect["id"]]
            if not items:
                score = 0.0
            else:
                # Weight strong/reliable evidence while keeping the model explainable.
                total = sum(item["reliability"] for item in items)
                type_bonus = min(len(items) * 5, 20)
                score = min(100.0, total / len(items) + type_bonus)

            results.append({
                "id": suspect["id"],
                "name": suspect["name"],
                "occupation": suspect["occupation"],
                "relationship": suspect["relationship"],
                "score": round(score, 1),
                "evidence_count": len(items),
            })

        return sorted(results, key=lambda x: x["score"], reverse=True)

    def dashboard_data(self, case_id):
        evidence = self.get_evidence(case_id)
        scores = self.calculate_scores(case_id)
        return {
            "suspect_count": len(self.get_suspects(case_id)),
            "evidence_count": len(evidence),
            "average_reliability": (
                round(sum(e["reliability"] for e in evidence) / len(evidence), 1)
                if evidence else 0
            ),
            "scores": scores,
        }
