# GitHub Repo Analytics Pipeline

## What this project does

This project fetches repository data from my GitHub account using the GitHub REST API, cleans and transforms it with Pandas, and generates visual charts and a text summary of my repos languages used, repo sizes, and star counts.

## Project structure

```
capstone_project/
├── data/
│   ├── data.json
│   └── github_repos_clean.csv
├── src/
│   ├── data_handler.py
│   ├── logic.py
│   └── reports.py
├── requirements.txt
└── .gitignore
```


## How to run

From the `src/` folder, run each script in this order:

```bash
cd src
py data_handler.py   # fetches raw data from GitHub API, saves data/data.json
py logic.py           # cleans the data, saves data/github_repos_clean.csv
py reports.py         # generates charts and prints a summary
```

## Requirements

Install dependencies with:
```bash
pip install -r requirements.txt
```
(pandas, matplotlib, requests)

## What the report shows

- A bar chart of repo count per programming language
- A bar chart of repo size per repo
- A bar chart of stargazer count per repo
- A printed text summary: total repo count, most-used language, largest repo, and most-starred repo

## Notes / limitations

- Some repos have no `language` value from the API (e.g. notes/documentation-only repos). These are manually labeled `"notes"` based on my own knowledge of each repo, not inferred from the data itself.
- The "most used language" stat uses `.idxmax()`, which picks the first match in case of a tie in this dataset, `"C"` and `"notes"` are actually tied at 5 repos each, but the summary only shows one.
- The `size` and `stargazers_count` charts use row index (0–15) on the x-axis rather than repo names, for simplicity.