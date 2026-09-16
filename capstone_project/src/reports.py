import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/github_repos_clean.csv")
# print(df)
df["language"].value_counts().plot(kind="bar")
plt.show()

df["size"].plot(kind="bar")
plt.show()

df["stargazers_count"].plot(kind="bar")
plt.show()


print(f"total repos i have on my github: {len(df)}")
print(f"most used language: {df['language'].value_counts().idxmax()}")

biggest = df.sort_values("size", ascending=False).iloc[0]
print(f"largest repo: {biggest['name']} ({biggest['size']} KB)")

most_starred = df.sort_values("stargazers_count", ascending=False).iloc[0]
print(f"most starred repo: {most_starred['name']} ({most_starred['stargazers_count']} stars)")