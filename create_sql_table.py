#
# Creates SQL database with three tables (authors, papers, author_key_rank)
#
#

def create_sql_database(database_name):
    """
    Creates the three table schemas for the SQL database: AUTHORS, 
    PAPERS, and AUTHOR_KEY_RANK.
    """
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE authors ([author_identifier] INTEGER PRIMARY KEY, [first_name] text, [last_name] text, [institution] text, [gender] text, [country] text, CONSTRAINT full_name UNIQUE (first_name, last_name))''')
    c.execute('''CREATE TABLE papers ([paper_identifier] INTEGER PRIMARY KEY, [title] text UNIQUE, [year] text, [journal] text, [field] text, [num_authors] integer)''')
    c.execute('''CREATE TABLE author_key_rank ([author_identifier] integer, [paper_identifier] integer, [rank] integer)''')
    conn.commit()