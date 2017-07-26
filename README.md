
![gu](https://pbs.twimg.com/profile_images/1899483763/GU_AbbreviatedMark_twitter_normal.png)
![python](https://www.python.org/static/favicon.ico)
![Sentiment](https://git.gitbook.com/raw/caiomsouza/u-tad-final-project/master/images/icon-sentiment.png?token=Y2Fpb21zb3V6YTo5YTllZmJhYi03NDg5LTQ4YTUtYThjMy05MDM2Yjc5ODgyMmM%3D)


Predicting the Severity of Diplomatic Events 
Georgetown Data Science – Predicting the Severity of Diplomatic Events Project - 2017

Team Members:  Melanie Huston, Carl Lofton, Gerhard Ottehenning, Makida W-Meskel, Michael Yamoah

Project Domain: Media and International Relations

Problem/Hypothesis:

	Use newspaper metadata and content to generate a sentiment analysis of media about specific countries. We are basing our analysis on Syria and Iran. 

Hypothesis: The results of sentiment analysis of reporting on Syria and the additional countries will be predictive of diplomatic conflict.

Available data sources

	LexisNexis – aggregated source of APIs from several newspapers
	Wikipedia -  Timeline Data
Data Science Pipeline Overview
 
Ingestion
	Collect the text and metadata for political articles from the New York Times and other news sources via LexisNexis with “Syria*” as the search term, published between 2009-2017. 

	Collect records of diplomatic events from Wikipedia Timeline data as csv format from 2010-2017 to allow for forecasting of 2010-present events from newspaper data beginning in 2009.

Tools: LexisNexis, Selenium, other tools TBD
Notes: 
	We transitioned to LexisNexis for collecting news articles since many newspaper APIs are no longer free to use
	We are reducing the range of the years of diplomatic data to collect, since granular data by day/month/year (instead of year only) generally begins around 2010 

Raw Data Storage

	MongoDB - We are splitting and storing the LexisNexis news articles in Mongo prior to wrangling the data
	SQLite – CSV files from Wikipedia Timeline data


Munging and Wrangling 

Ensure that the data from news sources have been created into instances and are ready to be used in computations.

Tools: MongoDB, Python, other tools TBD

Notes:
	The newspaper articles are extracted into individual documents in MongoDB for wrangling and sentiment analysis. 
	PDFs and other stores of diplomatic event data are processed. Diplomatic event data is rated by team members for severity (1,2,3)

Computation and Analysis

The Computations module rates (compiles) the news reports sentiment severity and compares against timing and severity of selected diplomatic events. 

Tools: Python, NLTK, other tools TBD

Forecasting Module 

The forecasting module uses the computation results and statistically forecasts selected diplomatic events.
Tools: Python, other tools TBD


Visualization

Provide a visualization of the predictive capability, or lack thereof. Provide an interface for customizing the visualization via variables such as country, granularity of time, or type of conflict. Provide analysis of successful or faulty predictive performance.
Tools: Python, Tableau, other tools TBD

Future Analysis and Applications
TBD
