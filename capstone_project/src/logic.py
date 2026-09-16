import json
import pandas as pd

with open("data.json","r") as f:
    j = json.load(f)
    # returns a list of dicts
    df = pd.DataFrame(j)
dff = df[["name", "language", "stargazers_count", "forks_count", "size", "created_at", "pushed_at", "fork"]]
# print("here ", j)
dff["language"] = dff["language"].fillna("notes")
dff["pushed_at"] = pd.to_datetime(dff["pushed_at"])
dff["created_at"] = pd.to_datetime(dff["created_at"])


print("SCRIPT STARTED!!!!!!!!!!!!!!!!!!!!!")
dff.to_csv("github_repos_clean.csv", index=False)
print("here ", dff)