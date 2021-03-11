import sqlite3


def condense_US_entries(database_name):
    """
    (Lily)
    Rewrites iterations of United States in country column to "united states of america". Assumes "us" and "united states" refers
    to United States of America. 

    Input:
        database_name (str): database name and filepath
    """
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    iter_us = ("united sates of america", "united state of america", "united states", "united states america", "us", "usa")
    lst_usa_entries = c.execute("SELECT author_identifier, country from authors WHERE country = ? OR country = ? OR country = ?\
        OR country = ? OR country = ? OR country = ?", iter_us).fetchall()

    for author, country in lst_usa_entries:
        c.execute('UPDATE authors SET country = ? WHERE author_identifer = ?', ('united states of america', author))
    

#replace empty country with "not found"?

def remove_the():
    '''
    (Peter)
    Removes 'the ' from institution in database in order to not double count institutions
    '''
    conn = sqlite3.connect('journals.db')
    c = conn.cursor()
    the_list = c.execute("SELECT author_identifier, institution from authors WHERE institution LIKE 'the %';")
    the_list = the_list.fetchall()
    for author, inst in the_list:
        new_inst = inst[4:]
        c.execute('UPDATE authors SET institution = ? WHERE author_identifier = ?', (new_inst, author))
        conn.commit()