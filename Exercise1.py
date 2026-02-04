#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 00:33:24 2026

@author: adonischeng
"""

import zipfile
from pathlib import Path
import pandas as pd
import altair as alt
from IPython.display import display, Markdown


def get_babynames_data() -> pd.DataFrame:
    """Download and parse SSA baby names data."""
    zip_path = Path("/Users/adonischeng/Desktop/Data_Visualization/names.zip")
    
    if not zip_path.exists():
        raise FileNotFoundError(
            "names.zip not found. Please place it in the same folder as Exercise1.py"
        )
    
    dfs: list[pd.DataFrame] = []
    with zipfile.ZipFile(zip_path) as zf:
        for filename in zf.namelist():
            if filename.startswith('yob') and filename.endswith('.txt'):
                with zf.open(filename) as f:
                    df = pd.read_csv(f, names=['name', 'sex', 'n'])
                    df['year'] = int(filename[3:7])
                    dfs.append(df)
    
    df = pd.concat(dfs, ignore_index=True)
    df['prop'] = df.groupby(['year', 'sex'])['n'].transform(lambda x: x / x.sum())
    return df

babynames = get_babynames_data()
latest_year = babynames['year'].max()
print(f"Data loaded through {latest_year}")

babynames.info()
babynames.head()

print(f"Unique names: {babynames['name'].nunique():,}")
print(f"Total babies: {babynames['n'].sum() / 1e6:.1f} million")

james_df = babynames[babynames['name'] == "James"]

alt.Chart(james_df).mark_line().encode(
    x='year:Q',
    y=alt.Y('n:Q', title='Number of Babies'),
    color='sex:N'
).properties(
    title='Popularity of the name "James" over time',
    width=600
)
    
    
top10 = (babynames.groupby(['sex', 'name'])['n']
         .sum()
         .reset_index()
         .sort_values('n', ascending=False)
         .groupby('sex')
         .head(10))

print("Top 10 Female Names:")
display(top10[top10['sex'] == 'F'])
print("Top 10 Male Names:")
display(top10[top10['sex'] == 'M'])

top10_female_names = top10[top10['sex'] == 'F']['name'].tolist()
female_trends = babynames[(babynames['sex'] == 'F') & (babynames['name'].isin(top10_female_names))]

alt.Chart(female_trends).mark_line().encode(
    x='year:Q',
    y=alt.Y('n:Q', title='Number of Female Babies'),
    color='name:N'
).properties(
    title='Top 10 Female Names Over Time',
    width=600
)

    

latest_df = (babynames[babynames['year'] == latest_year]
             .sort_values('prop', ascending=False)
             .head(10))

alt.Chart(latest_df).mark_bar().encode(
    x=alt.X('prop:Q', title=f'Proportion of Babies in {latest_year}'),
    y=alt.Y('name:N', sort='-x', title=''),
    color='sex:N'
).properties(
    title=f'Top 10 Baby Names in {latest_year}',
    width=500
)

# Exercises

#1.  Plot the most common names in the latest year over the entire period.



    

