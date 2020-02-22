### Homework Requirements/Deliverables
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 1 | √ | Create a new repository for this project called `sqlalchemy-challenge`
| 2 | √ | Add your Jupyter notebook and `app.py` to this folder. These will be the main scripts to run for analysis.
| 3 | √ | Use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. 
| 4 | √ | Analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.
| 5 | √ | Choose a start date and end date for your trip. Make sure that your vacation range is approximately **3-15 days total**

### Hints
1. You will need to join the station and measurement tables for some of the analysis queries.
2. Use Flask **jsonify** to convert your API data into a valid JSON response object.

### Development Requirements - Step 1: Climate Analysis and Exploration
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 01 | √ | Use SQLAlchemy `create_engine` to connect to your sqlite database.
| 02 | √ | Use SQLAlchemy `automap_base()` to reflect your tables into classes and save a reference to those classes called `Station` and `Measurement`.
| 03 | √ | **Precipitation Data**: Design a query to retrieve the last 12 months of precipitation data.
| 04 | √ | Precipitation Data: Select only the `date` and `prcp` values.
| 05 | √ | Precipitation Data: Load the query results into a Pandas DataFrame and set the index to the date column.
| 06 | √ | Precipitation Data: Sort the DataFrame values by `date`.
| 07 | √ | Precipitation Data: Plot the results using the DataFrame `plot` method.
| 08 | √ | Precipitation Data: Use Pandas to print the summary statistics for the precipitation data.
| 09 | √ | **Station Analysis**: Design a query to calculate the total number of stations.
| 10 | √ | List the stations and observation counts in descending order.
| 11 | √ | Station Analysis: Which station has the highest number of observations?
| 12 | √ | Station Analysis: Get the last 12 months of temperature observation data (tobs) for the most active station
| 13 | √ | Gets the min, max, and average temps for the most active station
| 14 | √ | Station Analysis: Plot the results as a histogram with `bins=12`

### Development Requirements - Step 2: Climate App using Flask API
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 1 | √ | **Route "\"** - home page
| 2 | √ | List all routes available
| 3 | √ | **Route "/api/v1.0/precipitation"** - Convert the query results to a Dictionary using **date** as the key and **prcp** as the value.
| 4 | √ | Return the JSON representation of your dictionary.
| 5 | √ | **Route "/api/v1.0/stations"** - Return a JSON list of stations from the dataset.
| 6 | √ | **Route "/api/v1.0/tobs"** - query for the dates and temperature observations from a year from the last data point.
| 7 | √ | Return a JSON list of Temperature Observations (tobs) for the previous year.
| 8 | √ | **Route "/api/v1.0/(start)"** - Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start without an end. "When given the start only, calculate TMIN, TAVG, and TMAX for **all dates greater than and equal to the start date**."
| 9 | √ | **Route "/api/v1.0/(start)/(end)"** - "When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date **inclusive**."

### From the grading rubric pdf:
#### Precipitation Analysis
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 1 | √ | Gets the correct results for the last year of data (the last day in the dataset is 8/23/2017)
| 2 | √ | Creates a pandas dataframe using the date and precipitation columns
| 3 | √ | Sorts the dataframe by date
| 4 | √ | Makes a plot using pandas with date as the x and precipitation as the y variables

#### Station Analysis
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 01 | √ | Correctly outputs the number of stations in the dataset (9)
| 02 | √ | Correctly finds the most active station by using count (USC00519281)
| 03 | √ | Gets the min, max, and average temperatures for the most active station (USC00519281)
| 04 | √ | Correctly plots a histogram for the last year of data using tobs as the column to count.

#### API SQLite Connection & Landing Page 
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 01 | √ | Correctly generates the engine to the correct sqlite file 
| 02 | √ | Uses automap_base() and reflects the database schema
| 03 | √ | Correctly saves references to the tables in the sqlite file (measurement and station)
| 04 | √ | Correctly creates and binds the session between the python app and database

#### API Static Routes
##### Precipitation route
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 01 | √ | Returns the **jsonified** precipitation data for the last year in the database
| 02 | √ | Returns json with the **date as the key** and the **value as the precipitation**

##### Stations route
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 01 | √ | Returns jsonified data of all of the stations in the database

##### Tobs route
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 01 | √ | Returns jsonified data for the most active station (USC00519281) for the last year of data

#### API Dynamic Routes

##### Start Date only route
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 01 | √ | Route accepts the start date as a parameter from the URL
| 02 | √ | Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
 
##### Start Date and End Date route
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 01 | √ | Route accepts the start and end dates as parameters from the URL
| 02 | √ | Returns the min, max, and average temperatures calculated from the given start date to the end date (inclusive)

#### Bonus

##### Trip Temperature Analysis
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 01 | √ | Uses the calc_temps function to get the min, max, and average temperatures for a date range of their choosing
| 02 | √ | Uses the calculated temperatures to generate a bar chart with an error bar.

##### Daily Rainfall Average
| Step | √ | Requirement |
| :---: | :---: | :--- 
| 01 | √ | Calculates the min, max, and average temperatures for each day of their trip and appends them to a list.
| 02 | √ | Creates a dataframe from the list and generates a stacked line chart plotting the min, max, and average temps for each day of their trip

