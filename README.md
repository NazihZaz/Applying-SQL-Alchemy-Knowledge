# sqlalchemy-challenge

This repository contains my solution of the SQL Alchemy homework GATECH Data Science and Analytics Bootcamp  - Surfs Up! and was completed in two steps:

> [Step 1 - Climate Analysis and Exploration](https://github.com/NazihZaz/sqlalchemy-challenge/blob/main/climate_starter.ipynb)

> [Step 2 - Climate App](https://github.com/NazihZaz/sqlalchemy-challenge/blob/main/app.py)

It also includes bonus parts of further temperature analysis:

> [Temperature Analysis I](https://github.com/NazihZaz/sqlalchemy-challenge/blob/main/temp_analysis_bonus_1_starter.ipynb)

> [Temperature Analysis II](https://github.com/NazihZaz/sqlalchemy-challenge/blob/main/temp_analysis_bonus_2_starter.ipynb)

## Analysis Breakdown

### Step 1	

a) To begin, I used Python, SQLAlchemy, Pands and Matplotlib  to do basic climate analysis and data exploration of the [climate database](https://github.com/NazihZaz/sqlalchemy-challenge/blob/main/Resources/hawaii.sqlite). Below is the final output that shows the precipiations in inches on a period of 12 months (08/23/2016 - 08/23/2017) in Hawaii:
![Precipitations](https://github.com/NazihZaz/sqlalchemy-challenge/blob/main/Images/PRCP.png)

b). Then, after retrieving the data for the most active station and querying the last 12 months of temperature of observation data (TOBS), I turned the query results into the plot below (Histogram with 12 bins):
![12 Month TOBS](https://github.com/NazihZaz/sqlalchemy-challenge/tree/main/Images)

### Step 2

Using [Flask](https://github.com/NazihZaz/sqlalchemy-challenge/blob/main/app.py), I designed an API based on queries developed in Step 1.
Here is the list of the different routes:

* `/` > Home page.

* `/api/v1.0/precipitation` > Dictionary of daily precipitations.

* `/api/v1.0/stations` > List of stations from the dataset.

* `/api/v1.0/tobs` > Temperature observations of the most active station for the last year of data.

* `/api/v1.0/<start>` > Temperature Minimum, Average and Maximum for all dates greater than and equal to the start date.

* `/api/v1.0/<start>/<end>` > Temperature Minimum, Average and Maximum for dates between the start and end date inclusive.

### Bonus Analysis

* Part 1:
- Identified the average temperature in June and December at all stations across all available years in the dataset.
- Used t-test to determine whether the difference in the means, if any, is statistically significant. This led to the below conclusion using a paired t-test:

	+ Given the returned P-value(0.00001452), the null hypothesis is rejected (P-value<0.05). Therefore, there is a meaningful difference between the temperature in 	June and December.

* Part 2:
- Calculated the Temperature Minimum, Average and Maximum for specific dates (In this case 08/01/2017 throuhg 08/10/2017).
- Turned the results of the query above into the plot below:
![Trip Avg Temp]()

- Calculated the daily normals for a range of dates (08/01/2017 throuhg 08/10/2017) and turned the results in the area plot shown below:
!Daily Temperature Normals]()
