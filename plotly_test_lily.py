#Testing out plotly commands
#
#

import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np

conn = sqlite3.connect('test.db')
sql_query = pd.read_sql_query('''select * from authors''', conn)
df = pd.DataFrame(sql_query, columns = ['author_identifier', 'first_name', 'last_name', 'institution', 'gender', 'country'])

#sql to pandas with gender and country counts
#sql_query1 = pd.read_sql_query('''select country, gender, count(*) from authors group by country, gender''', conn)
#df1 = pd.DataFrame(sql_query1, columns = ["country", "gender", "count"])
## didn't work (NaN for count column)

#Bar graph
#Per field (drop down menu):
#Percent women authors vs. rank

#gender_country_df = df.groupby(['gender','country']).size()#creates a series

df_gc = df.groupby(['gender','country']).size().to_frame('count').reset_index() #worked
countries10 = df_gc[df_gc['count']>10].reset_index(drop=True)
df = df.reset_index(drop=True) 

df_10c = df.merge(countries10['country'], on = 'country').reset_index(drop = True)
grpd = df_10c.groupby(['gender','country']).size().to_frame('count').reset_index()

# wrogn want perecent per country
#total_count = grpd['count'].sum()
#grpd['percent'] = grpd['count'].div(total_count)

#df_10c.groupby(['gender'])

 #df[df['country'] == countries10['country']] #Value Error

fig = px.bar(grpd, x="country", y="percent", color="gender", title="Gender breakdown by countries with > 10 authors")
fig.show()

#only returned single col of 45 rows??

#df['sales'] / df.groupby('state')['sales'].transform('sum')

#https://stackoverflow.com/questions/23377108/pandas-percentage-of-total-with-groupby
state_office = df.groupby(['state', 'office_id']).agg({'sales': 'sum'}) # Change: groupby state_office and divide by sum
country_gender = grpd.groupby(['country']).agg({'count':'sum'})
state_pcts = state_office.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
country_pcts = country_gender.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))