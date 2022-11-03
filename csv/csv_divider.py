import pandas as pd

df1 = pd.read_csv(r"tranco.csv")

df = df1.iloc[0:1000, [1]]
df.to_csv(r"1k.csv")
df = df1.iloc[1000:2000, [1]]
df.to_csv(r"2k.csv")
df = df1.iloc[2000:3000, [1]]
df.to_csv(r"3k.csv")
df = df1.iloc[3000:4000, [1]]
df.to_csv(r"4k.csv")
df = df1.iloc[4000:5000, [1]]
df.to_csv(r"5k.csv")
df = df1.iloc[5000:6000, [1]]
df.to_csv(r"6k.csv")
df = df1.iloc[6000:7000, [1]]
df.to_csv(r"7k.csv")
df = df1.iloc[7000:8000, [1]]
df.to_csv(r"8k.csv")
df = df1.iloc[8000:9000, [1]]
df.to_csv(r"9k.csv")
df = df1.iloc[9000:10000, [1]]
df.to_csv(r"10k.csv")
df = df1.iloc[10000:11000, [1]]
df.to_csv(r"11k.csv")
