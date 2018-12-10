# Interview Challenge

1. A program to fetch the historical prices and dates of gold and silver from these 2 URLs:

•            https://www.investing.com/commodities/gold-historical-data

•            https://www.investing.com/commodities/silver-historical-data

and store them locally (in a file or database, as you see fit).

(You can just extract the default data range in each case: no need to interact with the UI elements.)

 

2. A second program that takes the following 3 command line arguments:

•            Start date (in the format 2017-05-10)

•            End date (in the format 2017-05-22)

•            Commodity type (either "gold" or silver”)

and then returns (via the locally stored data) the mean and variance of the commodity’s price over the specified date range.

For example, the program might be called like so:

./getCommodityPrice 2017-05-01 2017-05-03 gold

and would print out a tuple such as:

gold 1253.66 35.79
