import plot_functions
import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np
'''
def get_top_k_underscore(field, k, c):

    tops_query = 'SELECT ' + field + ' FROM authors GROUP BY ' + field + ' ORDER BY COUNT(*) DESC LIMIT ' + str(k)
    tops = [i[0].split() for i in c.execute(tops_query).fetchall()]
    finals = ['_'.join(i) for i in tops]
    return finals
'''

def get_top_k(field, k, c):
    """
    Returns a list of the top k entries for specified field based on count (number of entries).

    Inputs:
        field (str)
        k (int)
        c (cursor for sqlite3)
    """
    tops_query = 'SELECT ' + field + ' FROM authors GROUP BY ' \
                 + field + ' ORDER BY COUNT(*) DESC LIMIT ' + str(k)
    tops = [i[0] for i in c.execute(tops_query).fetchall()]
    return tops


#create Pandas DataFrame for w
df = plot_functions.create_pd_dataframe()

conn = sqlite3.connect('journals.db')
c = conn.cursor()

top_countries = get_top_k('country', 100, c)
top_countries.insert(0, 'all_countries')
top_institutions = get_top_k('institution', 100, c)
top_institutions.insert(0, 'all_institutions')

lst_ranks = ['1', '2', '3', '4plus']
df.loc[df['rank'] > 3, 'rank'] = '4plus'
df = df['rank'].astype(str)

lst_fields = ['allfields', 'biological-sciences', 'business-and-commerce', 
              'earth-and-environmental-sciences','health-sciences',
              'humanities', 'physical-sciences', 
              'scientific-community-and-society','social-science']
author_min = [0, 10, 50, 100, 500]



for country in top_countries:
    for field in lst_fields:
        for rank in lst_ranks:
            for institution in top_institutions:
                if institution == 'all_institutions' and country == 'all_countries':
                    filtered_df = df[(df['field'] == field) & (df['rank'] == rank)]
                    country_fig = plot_functions.gender_by_country(filtered_df, 0, False)
                    country = country.split()
                    institution = institution.split()
                    field = field.split(sep = '-')

                    country_fig.write_html('gen_' + 'allcountry' + '_' + ('_').join(institution) + '_nomin_' + ('_').join(field) + "_" + rank +'.html', include_plotlyjs = False)
                    country_fig.write_html('ins_' + 'allcountry' + '_' + ('_').join(institution) + '_nomin_' + ('_').join(field) + "_" + rank +'.html', include_plotlyjs = False)
                    
                    field_fig = plot_functions.gender_by_field(filtered_df, False)
                    field_fig.write_html('fld_' + 'allcountry' + '_' + ('_').join(institution) + '_nomin_' + ('_').join(field) + "_" + rank +'.html', include_plotlyjs = False)

                    rank_fig = plot_functions.gender_by_rank(filtered_df, False)
                    rank_fig.write_html('rnk_' + 'allcountry' + '_' + ('_').join(institution) + '_nomin_' + ('_').join(field) + "_" + rank +'.html', include_plotlyjs = False)
                
            
                if institution == 'all_institutions':
                    filtered_df = df[(df['field'] == field) & (df['rank'] == rank) & (df['country'] == country)]
                    country_fig = plot_functions.gender_by_country(filtered_df, 0, False)
                    country = country.split()
                    institution = institution.split()
                    field = field.split(sep = '-')

                    country_fig.write_html('gen_' + 'allcountry' + '_' + ('_').join(institution) + '_nomin_' + ('_').join(field) + "_" + rank +'.html', include_plotlyjs = False)
                    country_fig.write_html('ins_' + 'allcountry' + '_' + ('_').join(institution) + '_nomin_' + ('_').join(field) + "_" + rank +'.html', include_plotlyjs = False)
                    
                    field_fig = plot_functions.gender_by_field(filtered_df, False)
                    field_fig.write_html('fld_' + 'allcountry' + '_' + ('_').join(institution) + '_nomin_' + ('_').join(field) + "_" + rank +'.html', include_plotlyjs = False)

                    rank_fig = plot_functions.gender_by_rank(filtered_df, False)
                    rank_fig.write_html('rnk_' + 'allcountry' + '_' + ('_').join(institution) + '_nomin_' + ('_').join(field) + "_" + rank +'.html', include_plotlyjs = False)
                else:
                    filtered_df = df[(df['field'] == field) & (df['rank'] == rank) & (df['institution'] == institution)]
                    country_fig = plot_functions.gender_by_country(filtered_df, 0, False)
                    country = country.split()
                    institution = institution.split()
                    field = field.split(sep = '-')

                    country_fig.write_html('gen_' + 'allcountry' + '_' + ('_').join(institution) + '_nomin_' + ('_').join(field) + "_" + rank +'.html', include_plotlyjs = False)
                    country_fig.write_html('ins_' + 'allcountry' + '_' + ('_').join(institution) + '_nomin_' + ('_').join(field) + "_" + rank +'.html', include_plotlyjs = False)
                    
                    field_fig = plot_functions.gender_by_field(filtered_df, False)
                    field_fig.write_html('fld_' + 'allcountry' + '_' + ('_').join(institution) + '_nomin_' + ('_').join(field) + "_" + rank +'.html', include_plotlyjs = False)

                    rank_fig = plot_functions.gender_by_rank(filtered_df, False)
                    rank_fig.write_html('rnk_' + 'allcountry' + '_' + ('_').join(institution) + '_nomin_' + ('_').join(field) + "_" + rank +'.html', include_plotlyjs = False)

                for min in author_min:
                    if country == 'allcountry':
                        if field == 'allfields':
                            filtered_df = df[(df['field'] == field) & (df['rank'] == rank)]
                            country_fig = plot_functions.gender_by_country(filtered_df, min, False)
                            country_fig.write_html('gen_' + country + '_' + 'countryByGender_' + str(author_min) + '.html', include_plotlyjs = False) #html code
                    if institution == 'allinstitution':
                        filtered_df = df



