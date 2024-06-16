import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = {
    'Term': ['surveillance', 'bailout', 'transparency', 'lobbying', 'precedent', 'subpoena', 'impeachment', 'asylum', 'veto', 'constitution'],
    'Normalized frequency': [0.81, np.nan, 0.9, 0.42, 0.78, np.nan, 0, 0.84, 0.66, 0.56],
    'PMI': [0.24, np.nan, 0.31, 0.1, 0.18, np.nan, 0, 0.28, 0.17, 0.24],
    'Word2Vec': [0.11, np.nan, 0.08, 0.06, 0.09, np.nan, np.nan, -0.009, 0.13, 0.08]
}

df = pd.DataFrame(data)

#remove row if all 3 values = NaN
df.dropna(how='all', subset=['Normalized frequency', 'PMI', 'Word2Vec'], inplace=True)

for approach1, approach2 in [('Normalized frequency', 'PMI'), ('Normalized frequency', 'Word2Vec'), ('PMI', 'Word2Vec')]:
    plt.figure(figsize=(8, 6))
    for index, row in df.iterrows():
        if not np.isnan(row[approach1]) and not np.isnan(row[approach2]):
            plt.scatter(row[approach1], row[approach2], label=row['Term'], s=100)
    plt.title(f'{approach1} vs {approach2}')
    plt.xlabel(approach1)
    plt.ylabel(approach2)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'visualizations/{approach1}_vs_{approach2}.png')
    plt.close()

#test correlations
corr1 = df['Normalized frequency'].corr(df['PMI'])
corr2 = df['Normalized frequency'].corr(df['Word2Vec'])
corr3 = df['PMI'].corr(df['Word2Vec'])
print(corr1, corr2, corr3)
