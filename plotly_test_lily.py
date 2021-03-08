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

fig = px.bar(grpd, x="country", y="count", color="gender", title="Long-Form Input")
fig.show()

# countries with more than 10 entries
df_10 = df.groupby(["country"]).apply(lambda x: x > 10)).reset_index(drop=True)
# select top N rows within each continent
g.groupby('continent').head(1)