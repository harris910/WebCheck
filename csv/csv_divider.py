import pandas as pd

df1 = pd.read_csv(r"tranco.csv")

df = df1.iloc[0:3500, [1]]
df.to_csv(r"1k.csv")
df = df1.iloc[3500:7000, [1]]
df.to_csv(r"2k.csv")
df = df1.iloc[7000:10500, [1]]
df.to_csv(r"3k.csv")
df = df1.iloc[10500:14000, [1]]
df.to_csv(r"4k.csv")
df = df1.iloc[14000:17500, [1]]
df.to_csv(r"5k.csv")
df = df1.iloc[17500:21000, [1]]
df.to_csv(r"6k.csv")
df = df1.iloc[21000:24500, [1]]
df.to_csv(r"7k.csv")
df = df1.iloc[24500:28000, [1]]
df.to_csv(r"8k.csv")
df = df1.iloc[28000:31500, [1]]
df.to_csv(r"9k.csv")
df = df1.iloc[31500:35000, [1]]
df.to_csv(r"10k.csv")
df = df1.iloc[35000:38500, [1]]
df.to_csv(r"11k.csv")
