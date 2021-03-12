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

    conn = sqlite3.connect('/home/lilymansfield/group_2/journals.db')
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
        create_html(bool)
        show_graph(bool)
    """
    #conn = sqlite3.connect(database_name)
    #sql_query = pd.read_sql_query('''select * from authors''', conn)
    #df = pd.DataFrame(sql_query, columns = ['author_identifier', 'first_name', 'last_name', 'institution', 'gender', 'country'])

    df_gc = df.groupby(['country']).size().to_frame('count').reset_index() #worked
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
    
    #if create_html:
        #fig.write_html('gen_countryByGender_' + str(author_min) + '.html', include_plotlyjs = False) #html code
    #fig.show()

def gender_by_institution(df, author_min, show_graph = True):
    """
    Plots a bar graph showing percent of authors by gender vs. institution. The bars are broken down into 
    percent of each gender category. Only plots institutions with a minimum number of authors.

    Inputs:
        df (Pandas DataFrame)
        author_min (int)
        create_html(bool)
        show_graph(bool)
    """
    df_count = df.groupby(['institution']).size().to_frame('count').reset_index() #worked
    institution_min = df_count[df_count['count'] > author_min].reset_index(drop=True)
    #df = df.reset_index(drop=True) 

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
        create_html(bool)
        show_graph(bool)
    """

    #conn = sqlite3.connect(database_name)
    #sql_query = pd.read_sql_query('''select gender, rank from authors join author_key_rank on authors.author_identifier = author_key_rank.author_identifier''', conn)
    #df = pd.DataFrame(sql_query, columns = ['gender', 'rank'])

    grp_df = df.groupby(['gender','rank']).size().to_frame('count').reset_index() #worked

    rank_gender = grp_df.groupby(['rank','gender']).agg({'count':'sum'})
    rank_pcts = rank_gender.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))#need to change count column to percent column
    rank_pcts.reset_index(inplace = True)

    fig = px.bar(rank_pcts, x="rank", y="count", color="gender", title="Gender breakdown by rank")
    #if create_html: 
        #fig.write_html('bar_rankByGender.html', include_plotlyjs = False) #html code
    if show_graph:
        fig.show()
    
    return fig



"""
DELETE FUNCTION
"""
def gender_by_rank_condensed(database_name, create_html = False, show_graph = True):
    """
    Plots a bar graph showing percent of authors by gender vs. rank (1, 2, 3, and 4+).

    Inputs:
        database_name (str)
        create_html(bool)
        show_graph(bool)
    """
    #conn = sqlite3.connect(database_name)
    #sql_query = pd.read_sql_query('''select gender, rank from authors join author_key_rank on authors.author_identifier = author_key_rank.author_identifier''', conn)
    #df = pd.DataFrame(sql_query, columns = ['gender', 'rank'])

    grp_df = df.groupby(['gender','rank']).size().to_frame('count').reset_index() #worked

    rank_gender = grp_df.groupby(['rank','gender']).agg({'count':'sum'})
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
    if create_html:
        fig.write_html('bar_rankByGender_condensed.html', include_plotlyjs = False) #html code
    if show_graph:
        fig.show()

def gender_by_field(df, show_graph = True):
    """
    Plots a bar graph showing percent of authors by gender vs. field for all fields, then
    calls function to create individual versions for each field.

    Inputs:
        database_name (str)
        show_graph (bool)
    """
    #conn = sqlite3.connect(database_name)
    #sql_query = pd.read_sql_query('''select gender, field from authors join author_key_rank on authors.author_identifier = author_key_rank.author_identifier join papers on author_key_rank.paper_identifier = papers.paper_identifier''', conn)
    #df = pd.DataFrame(sql_query, columns = ['gender', 'field'])# count didn't save

    grp_df = df.groupby(['gender','field']).size().to_frame('count').reset_index()

    field_gender = grp_df.groupby(['field','gender']).agg({'count':'sum'})
    field_pcts = field_gender.groupby(level = 0).apply(lambda x: 100 * x / float(x.sum()))#need to change count column to percent column
    field_pcts.reset_index(inplace = True)
    field_pcts.rename(columns = {"count": "percent"}, inplace = True)

    fig = px.bar(field_pcts, x="field", y="percent", color="gender", title="Gender breakdown by field", labels = {'percent': "Percent %", "field": "Field"})
    #if create_html:
        #fig.write_html('bar_fieldByGender.html', include_plotlyjs = False) #html code
    
    if show_graph:
        fig.show()

    return fig

def gender_by_field_individual(database_name, field_pcts, create_html = False, show_graph = True):
    """
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


