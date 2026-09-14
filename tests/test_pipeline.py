import json
from pathlib import Path

import pandas as pd
import pytest
import requests

from proj import AnalyticsPipeline, PipelineConfig


SAMPLE_RECORDS = [
    {"id": 2, "userId": 1, "title": " Second post ", "body": "two   words"},
    {"id": 1, "userId": 1, "title": "First post", "body": "one word"},
    {"id": 3, "userId": "invalid", "title": "Ignored", "body": "record"},
]


def test_clean_data_normalizes_text_and_adds_metrics() -> None:
    cleaned = AnalyticsPipeline.clean_data(SAMPLE_RECORDS)

    assert list(cleaned["id"]) == [1, 2]
    assert cleaned.loc[1, "body"] == "two words"
    assert list(cleaned["body_word_count"]) == [2, 2]
    assert list(cleaned["title_length"]) == [10, 11]


def test_clean_data_rejects_missing_columns() -> None:
    with pytest.raises(ValueError, match="Missing required columns: body"):
        AnalyticsPipeline.clean_data([{"id": 1, "userId": 1, "title": "Title"}])


def test_summarize_returns_user_and_overall_metrics() -> None:
    cleaned = AnalyticsPipeline.clean_data(SAMPLE_RECORDS)

    user_summary, overall_summary = AnalyticsPipeline.summarize(cleaned)

    assert user_summary.to_dict("records") == [
        {
            "userId": 1,
            "post_count": 2,
            "average_body_words": 2.0,
            "average_title_words": 2.0,
        }
    ]
    assert overall_summary["total_posts"] == 2
    assert overall_summary["unique_users"] == 1
    assert overall_summary["longest_body_words"] == 2


def test_fetch_data_uses_cache_when_api_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    cache_path = output_dir / "raw_posts.json"
    cache_path.write_text(json.dumps(SAMPLE_RECORDS), encoding="utf-8")

    def raise_connection_error(*args: object, **kwargs: object) -> None:
        raise requests.ConnectionError("offline")

    monkeypatch.setattr(requests, "get", raise_connection_error)
    pipeline = AnalyticsPipeline(PipelineConfig(output_dir=output_dir))

    assert pipeline.fetch_data() == SAMPLE_RECORDS