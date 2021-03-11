import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np

"""
Gender percent breakdown by countries with > 10 authors
"""

def gender_by_country(database_name, author_min):
    """
    Plots a bar graph showing percent of authors vs. country. The bars are broken down into 
    percent of each gender category. Only plots countries with a minimum number of authors.

    Inputs:
        database_name (str): database filepath and name
        author_min (int)
    """
    conn = sqlite3.connect(database_name)
    sql_query = pd.read_sql_query('''select * from authors''', conn)
    df = pd.DataFrame(sql_query, columns = ['author_identifier', 'first_name', 'last_name', 'institution', 'gender', 'country'])

    df_gc = df.groupby(['gender','country']).size().to_frame('count').reset_index() #worked
    countries10 = df_gc[df_gc['count'] > author_min].reset_index(drop=True)
    df = df.reset_index(drop=True) 

    df_10c = df.merge(countries10['country'], on = 'country').reset_index(drop = True)
    grpd = df_10c.groupby(['gender','country']).size().to_frame('count').reset_index()

    country_gender = grpd.groupby(['country', 'gender']).agg({'count':'sum'})
    country_pcts = country_gender.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))
    country_pcts.rename(columns = {"count": "percent"}, inplace = True)
    country_pcts.reset_index(inplace = True)

    fig = px.bar(country_pcts, x="country", y="percent", color="gender", title="Gender breakdown by countries with > 10 authors")
    fig.show()