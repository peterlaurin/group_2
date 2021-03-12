# group_2
CS122 group project

This project analyzes gender disparities across academic disciplines and institutions. We scrape authorship data from journal websites and article search engines, assign gender to author names, and analyze the distribution of gender in specific academic disciplines, institutions, and geographic regions. 

Group Members: 
Lily Mansfield, 
Peter Laurin, 
Maxwell Kay, 
Sadie Morriss

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







