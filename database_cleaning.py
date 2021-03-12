import sqlite3

CONN = sqlite3.connect('journals.db')

def country_not_found():
    c = CONN.cursor()
    q_str = "SELECT author_identifier, country FROM authors WHERE country = ''"
    query = c.execute(q_str)
    for author_id, country in query.fetchall():
        new_q = 'UPDATE authors SET country = ? WHERE author_identifier = ?'
        c.execute(new_q, ('country not found', author_id))
        CONN.commit()

def condense_country_entries():
    """
    Rewrites iterations of United States in country column to "united states of
    america". Assumes "us" and "united states" refers
    to United States of America. 

    Input:
        database_name (str): database name and filepath
    """
    c = CONN.cursor()
    iter_us = ["united sates of america", "united state of america", 
               "united states", "united states america", "us", "usa"]
    real_countries = dict.fromkeys(iter_us, 'united states of america')

    real_countries.update({'aotearoa new zealand':'new zealand', 
    'hong kong sar':'hong kong', 'p r china':'china', 'p. r. china':'china', 
    'p.r. china':'china', "people's republic of china":'china', 
    "people’s republic of china":'china', 'russian federation':'russia', 
    'uk':'united kingdom', '':'country not found'})

    q_bit = [' country = ? '] * len(real_countries.keys())
    query = "SELECT author_identifier, country from authors WHERE" + \
            'OR'.join(q_bit)
    bad_country_query = c.execute(query, tuple(real_countries.keys()))

    for author, bad_country in bad_country_query.fetchall():
        c.execute('UPDATE authors SET country = ? WHERE author_identifier = ?'\
                  , (real_countries[bad_country], author))
        CONN.commit()


def remove_the():
    '''
    Removes 'the ' from institution in database in order to not double 
    count institutions
    '''
    c = CONN.cursor()
    the_list = c.execute("SELECT author_identifier, institution from authors \
                          WHERE institution LIKE 'the %';")
    the_list = the_list.fetchall()
    for author, inst in the_list:
        new_inst = inst[4:]
        c.execute('UPDATE authors SET institution = ? \
                   WHERE author_identifier = ?', (new_inst, author))
        CONN.commit()

