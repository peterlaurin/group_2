# group_2
CS122 group project

Summary:
This project analyzes gender disparities across academic disciplines and institutions. We scrape authorship data from journal websites and article search engines, assign gender to author names, and analyze the distribution of gender in specific academic disciplines, institutions, and geographic regions. 

To run website: 
You run this file runing "google-chrome website.html" in the terminal.    

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

make_website/ : This directory includes the files used to crease the website. First, we found the names of all the files in 
pyplot_htmls_final via the terminal and saved that in plots.txt. Make_js_plots_final.py took plots.txt to iterate through the html
files in plots_html_final, extract the javascript portion of the html, and write a javascript file that includes each plot javascript as a function. We called the resulting javascript file java_functions_final, added an additional function, and then referenced this file through website.html. 
  -plot.txt: a text file with the names of all the files in pyplot_htmls_final (at the time we made it)
  -make_js_plots_final.py: writes javascript file as described above
  -java_functions_final.js; javascript functions (on_press() and one function per plot) that are used by website.html 


Files: 

website.html: the html code for the website, with embedded javascript 



nature_crawler.py: a python script that crawls Nature journals and extracts authors and authorship information

PLOS_webcrawler.py: a python script that crawls PLOS_ONE and extracts authors and authorship information

gender.py: a utility function that assigns gender to authors

create_database.py: a script that sets up our database of author information, paper information, and author rankings in each paper

journals.db: the database of author information, paper information, and author rankings in each paper

database_cleaning.py: a set of utility functions to clean data and make database more accurate

author_regression.ipynb: a python notebook regressing gender on some of our data and getting a priority of data to visualize on the website

create_html_plots.py: a script that iterates through all possible combinations of filters (country, field, rank, institution, minimum number of authors) from our website dropdown menus and generates hmtl code for each plot

plot_functions.py: a script that generates pyplots breaking down gender percentages based on country, field, rank and institution



Directories/files:

make_database: scripts to recerate journals.dv

make_website: scripts that made javascript files used by website.html  
- make_js_plots_final.py: takes html for plots and extracts the javascript from them, writes a javascript file with each plot as a function, changes the div ids of the plots to match div ids from website.html 
- java_functions_final.js: includes helper javascript functions for the website.html, including every plot as a javascript function
- plots.txt: the names of the files in pyplot_htmls_final 

make_plots: scripts to create pyplots and their html files based on journals.db
- create_html_plots.py: creates html files for all website graphs
- plot_functions.py: functions to create pyplot graphs 

regression: exploratory regression analysis
- author_regression.ipynb: jupyter notebook explaining exploratory linear regression

pyplots_html_final: html files for all graphs to be displayed on website based on user filtering

test_code: code used to test and build various scripts

project_proposal: project proposal documents










