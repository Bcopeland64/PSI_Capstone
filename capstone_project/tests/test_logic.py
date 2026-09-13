"""
test_logic.py: Unit tests for logic.py using pytest.
"""
import pytest
import pandas as pd
from src.logic import DataPipeline

def test_pipeline_init():
    pipeline = DataPipeline(api_url="https://api.test.com")
    assert pipeline.api_url == "https://api.test.com"
    assert pipeline.df is None

def test_clean_and_transform_duplicates():
    pipeline = DataPipeline(api_url="https://api.test.com")
    pipeline.df = pd.DataFrame({"id": [1, 1, 2], "value": ["A", "A", "B"]})
    pipeline.clean_and_transform()
    assert len(pipeline.df) == 2