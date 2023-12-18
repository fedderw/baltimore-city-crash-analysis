# baltimore-city-crash-analysis
## Data
This data reflects reports from crashes that resulted in an injury or fatality. The data was downloaded from the Maryland State Police's [Maryland Crash Data Download](https://mdsp.maryland.gov/Pages/Dashboards/CrashDataDownload.aspx) tool. 

To download this data set, we used the following filters to pull the desired data from 2018-01-01 to 2023-12-11
![image](https://github.com/fedderw/baltimore-city-crash-analysis/assets/16396180/1b6f68ca-9ce8-4fb8-9726-572e1d75767e)

There are many data points either with erroneously generated latitude and longitude or mislabeled county information.

Unfortunately, there are not enough data fields available for download to properly investigate these cases.

![image](https://github.com/fedderw/baltimore-city-crash-analysis/assets/16396180/28774340-9c43-440a-b87a-1a3e441127d3)

Since we are just focused on Baltimore City to generate our heatmap, we can use a spatial join to filter out the data points that fall outside of the city line.
