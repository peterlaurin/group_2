#Testing out plotly commands
#
#

import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np

"""
Gender percent breakdown by countries with > 10 authors
"""

conn = sqlite3.connect('test.db')
sql_query = pd.read_sql_query('''select * from authors''', conn)
df = pd.DataFrame(sql_query, columns = ['author_identifier', 'first_name', 'last_name', 'institution', 'gender', 'country'])

df_gc = df.groupby(['gender','country']).size().to_frame('count').reset_index() #worked
countries10 = df_gc[df_gc['count']>10].reset_index(drop=True)
df = df.reset_index(drop=True) 

df_10c = df.merge(countries10['country'], on = 'country').reset_index(drop = True)
grpd = df_10c.groupby(['gender','country']).size().to_frame('count').reset_index()

country_gender = grpd.groupby(['country', 'gender']).agg({'count':'sum'})
country_pcts = country_gender.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))
country_pcts.reset_index(inplace = True)

fig = px.bar(country_pcts, x="country", y="count", color="gender", title="Gender breakdown by countries with > 10 authors")
fig.show()

"""
Per field: percent women authors vs. rank
"""
conn = sqlite3.connect('test.db')
sql_query = pd.read_sql_query('''select gender, rank from authors join author_key_rank on authors.author_identifier = author_key_rank.author_identifier''', conn)
df = pd.DataFrame(sql_query, columns = ['gender', 'rank'])

grp_df = df.groupby(['gender','rank']).size().to_frame('count').reset_index() #worked

rank_gender = grp_df.groupby(['rank','gender']).agg({'count':'sum'})
rank_pcts = rank_gender.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))#need to change count column to percent column
rank_pcts.reset_index(inplace = True)

fig = px.bar(rank_pcts, x="rank", y="count", color="gender", title="Gender breakdown by rank")
#fig.write_html('test.html', include_plotlyjs = False) #html code
fig.show()

"""
Per field: percent women authors vs rank - 4+ category
"""
#create a 4+ table
rank_gender.reset_index(inplace = True)
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

"""
Test code and notes
"""

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



#only returned single col of 45 rows??

#df['sales'] / df.groupby('state')['sales'].transform('sum')

#https://stackoverflow.com/questions/23377108/pandas-percentage-of-total-with-groupby
#state_office = df.groupby(['state', 'office_id']).agg({'sales': 'sum'}) # Change: groupby state_office and divide by sum
country_gender = grpd.groupby(['country', 'gender']).agg({'count':'sum'})
#state_pcts = state_office.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
country_pcts = country_gender.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))
country_pcts.reset_index(inplace = True)

fig = px.bar(country_pcts, x="country", y="count", color="gender", title="Gender breakdown by countries with > 10 authors")
fig.show()