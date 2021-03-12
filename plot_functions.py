# 
# 
# Functions for plotting bar graph breakdown by gender for institutions, countries, fields and paper rank
# with plotly.
#
#Resources used:
#https://stackoverflow.com/questions/55910004/get-continent-name-from-country-using-pycountry
#https://stackoverflow.com/questions/17995024/how-to-assign-a-name-to-the-a-size-column
#https://stackoverflow.com/questions/23377108/pandas-percentage-of-total-with-groupby

import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np

def create_pd_dataframe():
    """
    Creates a Pandas DataFrame from SQL database.

    Returns:
        df (Pandas DataFrame)
    """

    conn = sqlite3.connect('journals.db')
    sql_query = pd.read_sql_query('''select field, institution, gender, rank, country\
         from authors join author_key_rank on authors.author_identifier = author_key_rank.author_identifier join papers on papers.paper_identifier = author_key_rank.paper_identifier''', conn)
    df = pd.DataFrame(sql_query, columns = ['field', 'institution', 'gender', 'rank', 'country'])

    return df


def gender_by_country(df, author_min, show_graph = True):
    """
    Plots a bar graph showing percent of authors by gender vs. country. The bars are broken down into 
    percent of each gender category. Only plots countries with a minimum number of authors.

    Inputs:
        database_name (str): database filepath and name
        author_min (int)
        show_graph(bool)
    """
    df_gc = df.groupby(['country']).size().to_frame('count').reset_index() 
    countries_min = df_gc[df_gc['count'] > author_min].reset_index(drop=True)
    df = df.reset_index(drop=True) 

    df_10c = df.merge(countries_min['country'], on = 'country').reset_index(drop = True)
    grpd = df_10c.groupby(['gender','country']).size().to_frame('count').reset_index()

    country_gender = grpd.groupby(['country', 'gender']).agg({'count':'sum'})
    country_pcts = country_gender.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))
    country_pcts.rename(columns = {"count": "percent"}, inplace = True)
    country_pcts.reset_index(inplace = True)

    fig = px.bar(country_pcts, x = "country", y = "percent", color = "gender", title = "Gender breakdown by countries with > " + str(author_min) + " authors")
    if show_graph:
        fig.show()

    return fig


def gender_by_institution(df, author_min, show_graph = True):
    """
    Plots a bar graph showing percent of authors by gender vs. institution. The bars are broken down into 
    percent of each gender category. Only plots institutions with a minimum number of authors.

    Inputs:
        df (Pandas DataFrame)
        author_min (int)
        show_graph(bool)
    """
    df_count = df.groupby(['institution']).size().to_frame('count').reset_index() 
    institution_min = df_count[df_count['count'] > author_min].reset_index(drop=True)
    df = df.reset_index(drop=True) 

    df_minfiltered = df.merge(institution_min['institution'], on = 'institution').reset_index(drop = True)
    grpd = df_minfiltered.groupby(['gender','institution']).size().to_frame('count').reset_index()

    inst_gender = grpd.groupby(['institution', 'gender']).agg({'count':'sum'})
    inst_pcts = inst_gender.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))
    inst_pcts.rename(columns = {"count": "percent"}, inplace = True)
    inst_pcts.reset_index(inplace = True)

    fig = px.bar(inst_pcts, x = "institution", y = "percent", color = "gender", title = "Gender breakdown by institution with > " + str(author_min) + " authors")
    if show_graph:
        fig.show()

    return fig


def gender_by_rank(df, show_graph = True):
    """
    Plots a bar graph showing percent of authors by gender vs. rank.

    Inputs:
        database_name (str)
        show_graph(bool)
    """
    grp_df = df.groupby(['gender','rank']).size().to_frame('count').reset_index() 

    rank_gender = grp_df.groupby(['rank','gender']).agg({'count':'sum'})
    rank_pcts = rank_gender.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))
    rank_pcts.rename(columns = {"count": "percent"}, inplace = True)
    rank_pcts.reset_index(inplace = True)

    fig = px.bar(rank_pcts, x="rank", y="percent", color="gender", title="Gender breakdown by rank")
    if show_graph:
        fig.show()
    
    return fig


def gender_by_field(df, show_graph = True):
    """
    Plots a bar graph showing percent of authors by gender vs. field for all fields, then
    calls function to create individual versions for each field.

    Inputs:
        database_name (str)
        show_graph (bool)
    """

    grp_df = df.groupby(['gender','field']).size().to_frame('count').reset_index()

    field_gender = grp_df.groupby(['field','gender']).agg({'count':'sum'})
    field_pcts = field_gender.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))#need to change count column to percent column
    field_pcts.reset_index(inplace = True)
    field_pcts.rename(columns = {"count": "percent"}, inplace = True)

    fig = px.bar(field_pcts, x="field", y="percent", color="gender", title="Gender breakdown by field", labels = {'percent': "Percent %", "field": "Field"})

    if show_graph:
        fig.show()

    return fig


def gender_by_field_individual(database_name, field_pcts, create_html = False, show_graph = True):
    """
    Deprecated function - more general function of gender_by_field used. 
    Plots a bar graph showing percent of authors by gender vs. field for each field.

    Inputs:
        database_name (str)
        create_html (bool)
        field_pcts (Pandas DataFrame)
        show_graph (bool)
    """
    fields = ['biological-sciences', 'business-and-commerce', 
              'earth-and-environmental-sciences','health-sciences',
              'humanities', 'physical-sciences', 
              'scientific-community-and-society','social-science']

    for field in fields:
        fig = px.bar(field_pcts[field_pcts['field'] == field], x="field", y="percent", color="gender", title="Gender breakdown by field", labels = {'percent': "Percent %", "field": "Field"})
        if show_graph:
            fig.show()
        if create_html:
            fig.write_html('bar_fieldByGender_' + field + '.html', include_plotlyjs = False)


