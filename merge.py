import pandas as pd
import os

dfs = []

for i in range(1, 40):
    file_path = os.path.join('All data files', f'nasa_exoplanets_part{i}.csv')
    dfs.append(pd.read_csv(file_path))

print(len(dfs))

combined_df = pd.concat(dfs, ignore_index=True)

combined_df.to_csv('nasa_exoplanets.csv', index=False)

print("Merged CSV file created: nasa_exoplanets.csv")
