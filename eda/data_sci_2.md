Today we looked at the dataset and identified the variables that were not of interest or were not correlated with our dependent variables.
We also looked at the correlation of the variables we thought were of interest. Code detailing this can be found in our R markdown file.
For next class, we seek to finalize our variables of interset, as well as explore external data sources that may have features of interest.
We also made a rudimentary model to look at our variables of interest.

4/3/24
Removed likely bundled sales
Filtered out non-arms-length transactions and highest 5% sales prices
Added neighborhoods for spatial info and spatial price lag
filtered by residential category code '1 '
filtered by timestamps to include only 2022 - 2024 sales dates
Still narrowing down variables of interest

4/10/2024
Determined variables for model:
    fireplaces,
    garage_spaces,
    number_of_bathrooms,
    total_livable_area,
    price_lag,
    (district name) ABBREV

Decided to use random forest model