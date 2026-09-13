from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def export_case_csv(service, case_id, output_dir="reports"):
    """Export ranked suspect analysis to CSV."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    rows = service.calculate_scores(case_id)
    path = Path(output_dir) / f"case_{case_id}_suspects.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def create_score_chart(service, case_id, output_dir="reports"):
    """Create a simple suspect-score chart."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    rows = service.calculate_scores(case_id)
    if not rows:
        return None

    df = pd.DataFrame(rows)
    path = Path(output_dir) / f"case_{case_id}_scores.png"

    plt.figure(figsize=(9, 5))
    plt.bar(df["name"], df["score"])
    plt.ylim(0, 100)
    plt.ylabel("Suspicion Score")
    plt.title(f"CASE-X Suspect Ranking - Case {case_id}")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    return path
