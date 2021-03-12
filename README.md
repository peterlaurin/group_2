# group_2
CS122 group project

Summary:
This project analyzes gender disparities across academic disciplines and institutions. We scrape authorship data from journal websites and article search engines, assign gender to author names, and analyze the distribution of gender in specific academic disciplines, institutions, and geographic regions. 

Group Members: 
Lily Mansfield, 
Peter Laurin, 
Maxwell Kay, 
Sadie Morriss

Note: Our scripts were reorganized for clarity's sake and have been organized such that running our scripts will not overwrite final versions of our final database (journals.db) and our generated html files for our pyplots that are used by the website. If scripts are run they will recreate our work in files/directories marked by the prefix "dummy" (i.e. if you attempt to rerun our database scripts they will start building a new database called dummy_journals.db). We have also added notes to the top of our scripts restating this information. 

Code description:

make_database/ : This directory contains scripts used to generate and clean our final database of authors and papers (journals.db). To recreate our database:
- create_database.py: create the SQL database with three tables (authors, papers, author_key_rank)
- nature_crawler.py: crawls the Nature journals, adding to the SQL database
- PLOS_webcrawler.py: crawls the PLOS One journal, adding to the SQL database 
- database_cleaning.py: cleans the database (rewrite different spellings of top countries. remove "the" from institutions, etc.)

make_plots/ : This directory contains scripts used to generate pyplot graphs and to generate the html files for the graphs for the website based on our final journals.db database. We created html files for all the pyplots based on the selection criteria from the website. We had filtering for country, institution, field, rank (place in order of authors). If country and institution are NOT selected (default 'all' is selected) then you can also filter for minimum number of authors (graph will only show institutions or countries with more than 10, 50, 100 or 500 authors). To recreate html files for our graphs:
- create_html_plots.py: creates html files of graphs for all possible filtering options for the website to display. 
  Uses:
  - plot_functions.py: functions to create plots for gender breakdown by country, gender breakdown by field, gender breakdown by institution, gender breakdown by rank.




Files: 

nature_crawler.py: a python script that crawls Nature journals and extracts authors and authorship information

PLOS_webcrawler.py: a python script that crawls PLOS_ONE and extracts authors and authorship information

gender.py: a utility function that assigns gender to authors

create_database.py: a script that sets up our database of author information, paper information, and author rankings in each paper

journals.db: the database of author information, paper information, and author rankings in each paper

database_cleaning.py: a set of utility functions to clean data and make database more accurate

author_regression.ipynb: a python notebook regressing gender on some of our data and getting a priority of data to visualize on the website

create_html_plots.py: a script that iterates through all possible combinations of filters (country, field, rank, institution, minimum number of authors) from our website dropdown menus and generates hmtl code for each plot

plot_functions.py: a script that generates pyplots breaking down gender percentages based on country, field, rank and institution

Directories:

lily_plots: test code for making pyplots

peter_plots: test code for making pyplots

project_proposal: project proposal documents

pyplot_htmls: html files for plots for website

nature_crawler_test: test code for making Nature journal crawler







