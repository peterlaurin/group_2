import sqlite3
import pandas as pd
import plotly.express as px 
import numpy 

def make_df():
    conn = sqlite3.connect('test.db')
    sql_query = pd.read_sql_query('''select * from authors''', conn)
    df = pd.DataFrame(sql_query, columns = ['author_identifier', 'first_name', 'last_name', 'institution', 'gender', 'country'])
    return df

def make_charts(df):
    base = df["gender"].value_counts()
    val = base.values 
    label = base.index
    pie = px.pie(values = val, names = label)
    bar = px.histogram(df, x = "gender")
    return pie, bar

def get_html(chart):
    
    #return 1

    return chart.write_html("test_bar_html.html", include_plotlyjs = False)

