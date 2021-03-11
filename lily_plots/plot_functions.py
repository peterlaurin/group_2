import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np

"""
Gender percent breakdown by countries with > 10 authors
"""

def gender_by_country(database_name, author_min):
    """
    Plots a bar graph showing percent of authors by gender vs. country. The bars are broken down into 
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

def gender_by_rank(database_name):
    """
    Plots a bar graph showing percent of authors by gender vs. rank.

    Inputs:
        database_name (str)
    """

    conn = sqlite3.connect(database_name)
    sql_query = pd.read_sql_query('''select gender, rank from authors join author_key_rank on authors.author_identifier = author_key_rank.author_identifier''', conn)
    df = pd.DataFrame(sql_query, columns = ['gender', 'rank'])

    grp_df = df.groupby(['gender','rank']).size().to_frame('count').reset_index() #worked

    rank_gender = grp_df.groupby(['rank','gender']).agg({'count':'sum'})
    rank_pcts = rank_gender.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))#need to change count column to percent column
    rank_pcts.reset_index(inplace = True)

    fig = px.bar(rank_pcts, x="rank", y="count", color="gender", title="Gender breakdown by rank")
    #fig.write_html('test.html', include_plotlyjs = False) #html code
    fig.show()


def gender_by_rank_condensed(database_name):
    """
    Plots a bar graph showing percent of authors by gender vs. rank (1, 2, 3, and 4+).

    Inputs:
        database_name (str)
    """
    #create a 4+ table
    rank_gender.reset_index(inplace = True) #need to define rank_gender from above function
    df_4plus = rank_gender[rank_gender['rank'] > 4]
    df_4plus_agg = df_4plus.groupby('gender').agg({'count':'sum'})
    df_4plus_agg.reset_index(inplace = True)
    df_4plus_agg['rank'] = '4+'

    #create 1-3 table
    df_rest = rank_gender[rank_gender['rank'] < 4].reset_index(drop = True)

    #combine
    df_combined = pd.concat([df_rest, df_4plus_agg])

    #calculate percents
    grp_df_combined = df_combined.groupby(['rank', 'gender']).agg({'count':'sum'})

    rank_pcts = grp_df_combined.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))#need to change count column to percent column
    rank_pcts.reset_index(inplace = True)

    rank_pcts['rank'] = rank_pcts['rank'].apply(str)

    fig = px.bar(rank_pcts, x="rank", y="count", color="gender", title="Gender breakdown by rank", labels = {'count': "Percent %"})
    #fig.write_html('test.html', include_plotlyjs = False) #html code
    fig.show()