#!/usr/bin/python

#Loading the libraries required 
import requests
from bs4 import BeautifulSoup as bs
import csv
import sys
import os
import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore')

#print(os.getcwd())

#Hardcoding the URL 
API_url = 'https://www.investing.com/instruments/HistoricalDataAjax'

###################################### Scraping Investing.com, store the Dates and Price to a file #############################################

def get_prices(start_date, end_date, g_s):
    """ Takes the URL, start & end dates and g_s (for gold/silver) and stores the output to a csv file """
        
    #hardcoding the ID's
    if g_s == 'gold': g_s_id = '8830' #gold
    else : g_s_id = '8836' #silver   
        
    HEADERS = {
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
              }
     
    # This is the only data required by the api 
    # To send back the price data
    data = {
                "curr_id": g_s_id,
                "smlID": "300004",
                "st_date": start_date,
                "end_date": end_date,
                "interval_sec": "Daily",
                "sort_col": "date",
                "sort_ord": "DESC",
                "action": "historical_data"
            }
    
    # Making the post request
    try:
        response = requests.post(API_url, data=data, headers=HEADERS)
    except:
        print("Wrong input data parameters. Please correct.")
        
    #To turn the Beautiful Soup parse tree into a nicely formatted Unicode string
    soup = bs(response.text, 'html.parser')
    
    #Parsing through the header tags
    headers = [header.text for header in soup.find_all('th')]
    
    rows = []
    for row in soup.find_all('tr'):
        rows.append([val.text for val in row.find_all('td')])
    rows = rows[:-1]
    print("Writing the retrieved data to the csv file")
    with open('output_file_'+g_s+'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(row for row in rows if row)

############################################## Calculating the stats  ##################################################

def get_stats(file_name,commodity,start_date, end_date):
    """ Takes file name and commodity type as input, prints out the mean & variance """
    data = pd.read_csv(file_name,parse_dates=['Date'],na_values=['-'])
    #print(data.head())
    data_fil = data.loc[(data["Date"] >= start_date) & (data["Date"] <= end_date)]
    #print("###########")
    #print(data_fil.head())
    #print(data_fil["Price"].head())
    #print(data_fil.dtypes)
    if commodity == 'gold':
        data_fil["Price"] = data_fil["Price"].str.replace(',','')
        #print(data_fil["Price"].head())
        avg = round(pd.to_numeric(data_fil["Price"]).mean(),2)
        var = round(pd.to_numeric(data_fil["Price"]).std(),2)
        print("Commodity:{0}  Average:{1} Standard_Deviation:{2}".format(commodity, avg, var))
    elif commodity == 'silver':
        avg = round(data_fil["Price"].mean(),2)
        std = round(data_fil["Price"].std(),2)
        print("Commodity:{0} Average:{1} Standard_Deviation:{2}".format(commodity, avg, std))       
        

def stats(start_date, end_date, g_s):
    """" Parses through the available output files and calls the get_stats function which prints out the statistics"""
    file_name = 'output_file_'+g_s+'.csv'
    #print(file_name)
    if os.path.exists(file_name):
        #print(file_name, g_s, start_date, end_date)
        get_stats(file_name, g_s, start_date, end_date)
    else:
        print("File related to gold & silver doesn't exist")
        sys.exit(1)

def args_parsing(args):
    """ Takes the arguments and assigns the respective values"""
    start_date = ''
    end_date = ''
    g_s = ''
    try:
        if args[0] == '--start_date' and args[2] == '--end_date' and args[4] == '--g_s':
            start_date = args[1]
            end_date = args[3]
            g_s = args[5]
            del args[0:6]
    except:
        print("All the arguments (--start_date <mm/dd/yyyy> --end_date <mm/dd/yyyy> --g_s <'gold' or 'silver'>) needed") 
        sys.exit(1)
    return (start_date, end_date, g_s)

########################################## Main #####################################################

def main():
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: python [--start_date <mm/dd/yyyy> --end_date <mm/dd/yyyy> --g_s <'gold' or 'silver'>] or  \
		      python [--stats --start_date <mm/dd/yyyy> --end_date <mm/dd/yyyy> --g_s <'gold' or 'silver'>]");
        sys.exit(1)
    
    if args[0] == '--stats':
        args = args[1:]
        #print(args)
        start_date, end_date, g_s = args_parsing(args)
        #print(start_date, end_date, g_s)
        stats(start_date, end_date, g_s) 

    else:
        start_date, end_date, g_s = args_parsing(args)
        #print(start_date, end_date, g_s)
        get_prices(start_date, end_date, g_s)

if __name__ == "__main__":
    main()

