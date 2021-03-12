#T


import plot_functions
import sqlite3
import pandas as pd
import plotly.express as px
import numpy as np




def get_top_k_underscore(field, k, c):
    tops_query = 'SELECT ' + field + ' FROM authors GROUP BY ' + field + \
                 ' ORDER BY COUNT(*) DESC LIMIT ' + str(k)
    tops = [itsy[0].split() for itsy in c.execute(tops_query).fetchall()]
    finals = ['_'.join(i) for i in tops]
    return finals


def get_top_k(field, k, c):
    """
    Returns a list of the top k entries for specified field based on count 
    (number of entries).

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

conn = sqlite3.connect('../journals.db')
c = conn.cursor()

countries = get_top_k('country', 100, c)
institutions = get_top_k('institution', 100, c)

ranks = ['1', '2', '3', '4plus']
df.loc[df['rank'] > 3, 'rank'] = '4plus'
df['rank'] = df['rank'].astype(str)

fields = ['biological-sciences', 'business-and-commerce', 
              'earth-and-environmental-sciences','health-sciences',
              'humanities', 'physical-sciences', 
              'scientific-community-and-society','social-science']
author_sizes = [0, 10, 50, 100, 500]


#reasonable field configurations in which to search
#[country, field, rank, institution, author_size]
#True = general (allcountry) False = specific (loop through top 100 inst)
valid_configs = [
[True, True, True, True, True],
[True, True, True, True, False],
[True, True, True, False, True],
[True, True, False, True, True],
[True, True, False, False, True],
[True, False, True, True, True],
[True, False, True, False, True],
[True, False, False, True, True],
[True, False, False, False, True],
[False, True, True, True, True],
[False, True, False, True, True],
[False, False, True, True, True],
[False, False, False, True, True]] 

def get_plots(filtered_df, config, author_min = 0, institution = '', 
              field = '', rank = '', country = ''):
    '''
    writes pyplot html plots in pyplot_htmls_final/ (see README.md) from 
    filtered dataframe and field names

    Input:
    filtered_df, pd.DataFrame of journals.db filtered on category
    config, boolean mask of which fields are general and which specific
    author_min, int, mininum author size to select in plot
    institution, str, specific institution name
    field, str, specific field of study
    rank, str, specific rank (see README.md)
    country, str, specific country name
    '''
    
    #country
    gen_country, gen_field, gen_rank, gen_inst, gen_as = config
    country_fig = plot_functions.gender_by_country(filtered_df, author_min, 
                  False)
    if not gen_country:
        country_name = country.split()
        country_name = ('_').join(country_name)
    else:
        country_name = 'allcountry'

    #field
    field_fig = plot_functions.gender_by_field(filtered_df, False)
    if not gen_field:
        field_name = field.split(sep = '-')
        field_name = ('_').join(field_name)
    else:
        field_name = 'allfield'

    #rank
    rank_fig = plot_functions.gender_by_rank(filtered_df, False)
    if not gen_rank:
        rank_name = rank
    else:
        rank_name = 'allrank'

    #institution
    institution_fig = plot_functions.gender_by_institution(filtered_df, 
                      author_min, False)
    if not gen_inst:
        inst_name = institution.split()
        inst_name = ('_').join(inst_name)
    else:
        inst_name = 'allinstitution'

    #author size
    if author_min == 0:
        min_name = 'nomin'
    else:
        min_name = str(author_min)

    direc = 'pyplot_htmls_final/'
    country_fig.write_html(direc + 'gen_' + country_name + '_' + inst_name + \
                           "_" + min_name + "_" + field_name + "_" + \
                            rank_name + ".html", include_plotlyjs = False)
    institution_fig.write_html(direc + 'ins_' + country_name + '_' + \
                               inst_name + "_" + min_name + "_" + field_name \
                               + "_" + rank_name + ".html", include_plotlyjs \
                               = False)
    field_fig.write_html(direc + 'fld_' + country_name + '_' + inst_name + \
                         "_" + min_name + "_" + field_name + "_" + rank_name \
                         + ".html", include_plotlyjs = False)
    rank_fig.write_html(direc + 'rnk_' + country_name + '_' + inst_name + "_" \
                        + min_name + "_" + field_name + "_" + rank_name + \
                        ".html", include_plotlyjs = False)

def generate_plots():
    for i, config in enumerate(valid_configs):
        print(i)

        #DELETE THIS
        if i < 11:
            continue


        if i == 0:
            filtered_df = df
            get_plots(filtered_df, config)
        
        if i == 1:
            for size in author_sizes:
                filtered_df = df
                get_plots(filtered_df, config, size)

        if i == 2:
            for institution in institutions:
                filtered_df = df[df['institution'] == institution]
                get_plots(filtered_df, config, institution = institution)
        
        if i == 3:
            for rank in ranks:
                filtered_df = df[df['rank'] == rank]
                get_plots(filtered_df, config, rank=rank)

        if i == 4:
            for rank in ranks:
                for institution in institutions:
                    filtered_df = df[(df['rank'] == rank) & \
                                     (df['institution'] == institution)]
                    get_plots(filtered_df, config, rank = rank, 
                              institution = institution)
        
        if i == 5:
            for field in fields:
                filtered_df = df[df['field'] == field]
                get_plots(filtered_df, config, field = field)
        
        if i == 6:
            for field in fields:
                for institution in institutions:
                    filtered_df = df[(df['field'] == field) & \
                                     (df['institution'] == institution)]
                    if filtered_df.shape[0] > 0:
                        get_plots(filtered_df, config, field = field, 
                                  institution = institution)

        if i == 7:
            for field in fields:
                for rank in ranks:
                    filtered_df = df[(df['field'] == field) & \
                                     (df['rank'] == rank)]
                    get_plots(filtered_df, config, field = field, 
                              rank = rank)
        '''
        #too many combinations, but possible with our vision
        if i == 8:
            for field in fields:
                for rank in ranks:
                    for institution in institutions:
                        filtered_df = df[(df['field'] == field) & \
                                         (df['rank'] == rank) & \
                                         (df['institution'] == institution)]
                        if filtered_df.shape[0] > 0:
                            get_plots(filtered_df, config, field = field, 
                                      rank = rank, institution = institution)
        '''

        if i == 9:
            for country in countries:
                filtered_df = df[df['country'] == country]
                get_plots(filtered_df, config, country = country)

        if i == 10:
            for country in countries:
                for rank in ranks:
                    filtered_df = df[(df['country'] == country) & \
                                     (df['rank'] == rank)]
                    if filtered_df.shape[0] > 0:
                        get_plots(filtered_df, config, country = country, 
                                  rank = rank)

        if i == 11:
            for country in countries:
                for field in fields:
                    filtered_df = df[(df['country'] == country) & \
                                     (df['field'] == field)]
                    if filtered_df.shape[0] > 0:
                        get_plots(filtered_df, config, country = country, 
                                  field = field)
        '''
        #too many combinations, but possible with our vision
        if i == 12:
            for country in countries:
                for field in fields:
                    for rank in ranks:
                        filtered_df = df[(df['country'] == country) & \
                                         (df['field'] == field) & \
                                         (df['rank'] == rank)]
                        get_plots(filtered_df, config, country = country,
                                  field = field, rank = rank)
        '''
    



