"""Data Analytics & Automation Pipeline.

Fetches post data from a JSON API, cleans and enriches it with pandas, then
creates reusable CSV, JSON, and PNG outputs.
"""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import requests


DEFAULT_API_URL = "https://jsonplaceholder.typicode.com/posts"
LOGGER = logging.getLogger("analytics_pipeline")


@dataclass(frozen=True)
class PipelineConfig:
	"""Runtime settings for one pipeline execution."""

	api_url: str = DEFAULT_API_URL
	output_dir: Path = Path("output")
	timeout_seconds: int = 15


class AnalyticsPipeline:
	"""Fetch, transform, analyze, and publish post analytics."""

	def __init__(self, config: PipelineConfig) -> None:
		self.config = config
		self.cache_path = config.output_dir / "raw_posts.json"

	def fetch_data(self) -> list[dict[str, Any]]:
		"""Fetch JSON records, falling back to the local cache if needed."""
		try:
			response = requests.get(
				self.config.api_url,
				timeout=self.config.timeout_seconds,
			)
			response.raise_for_status()
			records = response.json()
			if not isinstance(records, list) or not records:
				raise ValueError("The API returned no usable records.")
			self.cache_path.write_text(
				json.dumps(records, indent=2), encoding="utf-8"
			)
			LOGGER.info("Fetched %s records from the API.", len(records))
			return records
		except (requests.RequestException, ValueError, json.JSONDecodeError) as error:
			if not self.cache_path.exists():
				raise RuntimeError(
					"The API request failed and no local cache is available."
				) from error
			LOGGER.warning("API unavailable (%s); using cached data.", error)
			cached = json.loads(self.cache_path.read_text(encoding="utf-8"))
			if not isinstance(cached, list) or not cached:
				raise RuntimeError("The local cache does not contain usable data.")
			return cached

	@staticmethod
	def clean_data(records: list[dict[str, Any]]) -> pd.DataFrame:
		"""Validate records and add analysis-friendly text metrics."""
		frame = pd.DataFrame(records)
		required_columns = {"id", "userId", "title", "body"}
		missing_columns = required_columns.difference(frame.columns)
		if missing_columns:
			raise ValueError(
				f"Missing required columns: {', '.join(sorted(missing_columns))}"
			)

		frame = frame.dropna(subset=required_columns).copy()
		frame["title"] = frame["title"].astype(str).str.strip()
		frame["body"] = frame["body"].astype(str).str.replace(
			r"\s+", " ", regex=True
		).str.strip()
		frame = frame[(frame["title"] != "") & (frame["body"] != "")]
		frame["userId"] = pd.to_numeric(frame["userId"], errors="coerce")
		frame = frame.dropna(subset=["userId"])
		frame["userId"] = frame["userId"].astype(int)
		frame["title_length"] = frame["title"].str.len()
		frame["body_word_count"] = frame["body"].str.split().str.len()
		frame["title_word_count"] = frame["title"].str.split().str.len()
		return frame.sort_values("id").reset_index(drop=True)

	@staticmethod
	def summarize(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
		"""Build per-user metrics and a compact overall summary."""
		user_summary = (
			frame.groupby("userId", as_index=False)
			.agg(
				post_count=("id", "count"),
				average_body_words=("body_word_count", "mean"),
				average_title_words=("title_word_count", "mean"),
			)
			.round(2)
			.sort_values("post_count", ascending=False)
		)
		overall_summary = {
			"total_posts": int(len(frame)),
			"unique_users": int(frame["userId"].nunique()),
			"average_body_words": round(float(frame["body_word_count"].mean()), 2),
			"longest_body_words": int(frame["body_word_count"].max()),
			"generated_at_utc": datetime.now(timezone.utc).isoformat(),
		}
		return user_summary, overall_summary

	@staticmethod
	def create_chart(user_summary: pd.DataFrame, chart_path: Path) -> None:
		"""Create a bar chart showing post volume by user."""
		chart = user_summary.sort_values("userId")
		figure, axis = plt.subplots(figsize=(10, 5))
		axis.bar(chart["userId"], chart["post_count"], color="#176b87")
		axis.set_title("Posts per User")
		axis.set_xlabel("User ID")
		axis.set_ylabel("Number of Posts")
		axis.grid(axis="y", alpha=0.25)
		figure.tight_layout()
		figure.savefig(chart_path, dpi=150)
		plt.close(figure)

	def run(self) -> dict[str, Any]:
		"""Execute the complete pipeline and return the generated summary."""
		self.config.output_dir.mkdir(parents=True, exist_ok=True)
		records = self.fetch_data()
		cleaned_data = self.clean_data(records)
		user_summary, overall_summary = self.summarize(cleaned_data)

		cleaned_data.to_csv(self.config.output_dir / "cleaned_posts.csv", index=False)
		user_summary.to_csv(self.config.output_dir / "user_summary.csv", index=False)
		(self.config.output_dir / "summary.json").write_text(
			json.dumps(overall_summary, indent=2), encoding="utf-8"
		)
		self.create_chart(user_summary, self.config.output_dir / "posts_by_user.png")
		return overall_summary


def parse_args() -> PipelineConfig:
	"""Parse and validate command-line options."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--api-url", default=DEFAULT_API_URL)
	parser.add_argument("--output-dir", type=Path, default=Path("output"))
	parser.add_argument("--timeout", type=int, default=15)
	args = parser.parse_args()
	if args.timeout <= 0:
		parser.error("--timeout must be greater than zero")
	return PipelineConfig(
		api_url=args.api_url,
		output_dir=args.output_dir,
		timeout_seconds=args.timeout,
	)


def main() -> None:
	"""Run the pipeline from the command line."""
	logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
	config = parse_args()
	LOGGER.info("Pipeline configuration: %s", asdict(config))
	summary = AnalyticsPipeline(config).run()
	LOGGER.info("Pipeline completed: %s", summary)


if __name__ == "__main__":
	main()
