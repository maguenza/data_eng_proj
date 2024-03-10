Spotify Episodes is a data engineering project.

Architecture:
  1. source data - Spotify API, podcast episodes
  2. extract.py - Python code to extract JSON file
  3. transform.py - Python code to transform JSON file to Pandas dataframe
  4. load.py - Python code to load dataframe to Postgres SQL database
  5. textClassify.py - Tokenize and Count keywords within name and description of episodes

To Do:
https://medium.com/dev-genius/data-engineering-project-2-building-spotify-etl-using-python-and-airflow-432dd8e4ffa3 
  5. Docker
  6. Airflow

Next Steps:
  * decide on type of analytics for podcast with Spotify data
    - idea: tokenize and count words
    - idea: sentiment based on tokenization?
  * decide on ML model
    - k clusters of words
  * figure out how to get more than 20 rows of data
  * figure out how to get all the episode data for the Ringer podcasts
  * decide how to create unit tests and logging
  * decide on BI, what about dbt or looker (data studios)?
  * figure out automation (Airflow then Pachyderm)?