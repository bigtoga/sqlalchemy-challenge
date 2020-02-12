### Homework Requirements/Deliverables
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 1 | √ | Create a new repository for this project called `sqlalchemy-challenge`
| 2 | | Add your Jupyter notebook and `app.py` to this folder. These will be the main scripts to run for analysis.
| 3 | | Use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. 
| 4 | | Analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.
| 5 | | Choose a start date and end date for your trip. Make sure that your vacation range is approximately **3-15 days total**

### Hints
1. You will need to join the station and measurement tables for some of the analysis queries.
2. Use Flask **jsonify** to convert your API data into a valid JSON response object.

### Development Requirements - Step 1: Climate Analysis and Exploration
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 1 | | Use SQLAlchemy `create_engine` to connect to your sqlite database.
| 2 | | Use SQLAlchemy `automap_base()` to reflect your tables into classes and save a reference to those classes called `Station` and `Measurement`.
| 3 | | **Precipitation Data**: Design a query to retrieve the last 12 months of precipitation data.
| 4 | | Precipitation Data: Select only the `date` and `prcp` values.
| 5 | | Precipitation Data: Load the query results into a Pandas DataFrame and set the index to the date column.
| 6 | | Precipitation Data: Sort the DataFrame values by `date`.
| 7 | | Precipitation Data: Plot the results using the DataFrame `plot` method.
| 8 | | Precipitation Data: Use Pandas to print the summary statistics for the precipitation data.
| 11 | | **Station Analysis**: Design a query to calculate the total number of stations.
| 12 | | Station Analysis: Design a query to find the most active stations.
| 13 | | Station Analysis: List the stations and observation counts in descending order.
| 14 | | Station Analysis: Which station has the highest number of observations?
| 15 | | Station Analysis: **Hint**: You may need to use functions such as `func.min`, `func.max`, `func.avg`, and `func.count` in your queries.
| 16 | | Station Analysis: Design a query to retrieve the last 12 months of temperature observation data (tobs).
| 17 | | Station Analysis: Filter by the station with the highest number of observations.
| 18 | | Station Analysis: Plot the results as a histogram with `bins=12`.

### Development Requirements - Step 2: Climate App
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 1 | | Design a Flask API based on the queries that you have just developed.
| 2 | | Define the routes
| 3 | | **Route "\"** - home page
| 4 | | List all routes available
| 5 | | **Route "/api/v1.0/precipitation"** - Convert the query results to a Dictionary using **date** as the key and **prcp** as the value.
| 6 | | Return the JSON representation of your dictionary.
| 7 | | **Route "/api/v1.0/stations"** - Return a JSON list of stations from the dataset.
| 8 | | **Route "/api/v1.0/tobs"** - query for the dates and temperature observations from a year from the last data point.
| 9 | | Return a JSON list of Temperature Observations (tobs) for the previous year.
| 10 | | **Route "/api/v1.0/(start)"** - Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start without an end. "When given the start only, calculate TMIN, TAVG, and TMAX for **all dates greater than and equal to the start date**."
| 11 | | **Route "/api/v1.0/(start)/(end)"** - "When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date **inclusive**."

### From the grading rubric pdf:
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 1 | | **Precipitation** - Gets the correct results for the last year of data (the last day in the dataset is 8/23/2017)
| 2 | | Creates a pandas dataframe using the date and precipitation columns
| 3 | | Sorts the dataframe by date
| 4 | | Makes a plot using pandas with date as the x and precipitation as the y variables
| 5 | | **Station** - Correctly outputs the number of stations in the dataset (9)
| 6 | | Correctly finds the most active station by using count (USC00519281)
| 7 | | Gets the min, max, and average temperatures for the most active station (USC00519281)
| 8 | | Correctly plots a histogram for the last year of data using tobs as the column to count.
| 9 | | **Flask API** - Correctly generates the engine to the correct sqlite file 
| 10 | | Uses automap_base() and reflects the database schema
| 11 | | Correctly saves references to the tables in the sqlite file (measurement and station)
| 12 | | Correctly creates and binds the session between the python app and database
| 13 | | 
| 14 | | 
| 15 | | 
| 16 | | 
| 17 | | 
| 18 | | 
| 19 | | 
| 20 | | 

Precipitation route
✓ Returns the jsonified
precipitation data for the last
year in the database
✓ Returns json with the date as
the key and the value as the
precipitation
Stations route
✓ Returns jsonified data of all
of the stations in the database
Tobs route
✓ Returns jsonified data for the
most active station
(USC00519281) for the last
year of data
