import sqlite3


def condense_US_entries(database_name):
    """
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
    
  