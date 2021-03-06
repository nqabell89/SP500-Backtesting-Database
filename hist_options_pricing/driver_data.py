# Description: This script is designed to help retail investors get and analyze historical options pricing data for backtesting purposes.

import data_grab
import data_plot_master
import data_ui_helper

# TODO: add setting for weekly/monthly binning on /history/ plots

def check_sentinel(input): # Check if the user wants to exit the program everytime they input anything
    if (input.lower() == "exit"): print("User Requested Program Termination."); exit()


# Settings can also be modified at runtime (non-persistent)
settings = {'shouldPrintData'   : False,
            'API_KEY'           : 'Bearer UNAGUmPNt1GPXWwWUxUGi4ekynpj', #public key
            'darkMode'          : True, 
            'watermark'         : True, 
            'branding'          : "AbellAnalytics",
            'grid'              : True,
            'historyLimit'      : 10,             #when we switch form /timesales to /history endpoint(days)
            'binning'           : 5}             #1/5/15 for time/sales. (time/sales < 35 days.)

data_ui_helper.intro_screen(); # just some printing / instructions to introduce the program

symbol = input("Type 'settings' or enter a symbol to proceed: ").upper(); check_sentinel(symbol)
if (symbol == "SETTINGS"): # Does the user want to change the settings
    settings = data_grab.modify_settings(settings) #settings editting superloop
    symbol = input("Enter a symbol to proceed: ").upper(); check_sentinel(symbol) # prompt for symbol after settings optimized

description = data_grab.background_info(symbol, settings['API_KEY']) # Display some info about the underlying
optionType = data_grab.option_type(symbol) # Does the user want to look at call options or put options
dateList = data_grab.get_expiry_dates(symbol, settings['API_KEY']) # Download a list of all the expiry dates available

# Prompt the user to pick one of the expiry dates
date = input("Select an expiry date from the list above: "); check_sentinel(date)
if (date not in dateList):
    print("The date: " + date + " is not valid. Terminating Program."); exit()

# Format the date string for Tradier's API formatting
format_date = date.replace("-", "") # strip out the dashes from the selected date
format_date = format_date[2:len(format_date)] # strip the 20 off the front of 2020


strikeList = data_grab.get_strike_list(symbol, date, settings['API_KEY'])
selectedPrice = input("Select a strike from the list above: "); check_sentinel(selectedPrice)
if not (float(selectedPrice) in strikeList):
    print("No strike available for input price. Terminating Program."); exit()

selectedPrice = '{0:08d}'.format(int(float(selectedPrice)*1000)) #format the price string for Tradier
startDate, should_use_history_endpoint = data_grab.get_start_date(int(settings['historyLimit'])) #prompt user for date range
option_symbol = symbol + format_date + optionType + selectedPrice #full Tradier-formatted symbol for the option

data_name = symbol + " $" + str(float(selectedPrice)/1000)  + " Put Data Expiring " + date
if (optionType == "C"):
    data_name = symbol + " $" + str(float(selectedPrice) / 1000) + " Call Data Expiring " + date
print("Now grabbing " + data_name)


# Download the trade data and plot it
trade_data = data_grab.get_trade_data(option_symbol, startDate, settings['binning'], should_use_history_endpoint, settings['API_KEY'])
data_plot_master.plot_data(trade_data, should_use_history_endpoint, data_name, settings)

if (settings['shouldPrintData']):
    print(trade_data)
    
print("Program Reached End Of Execution."); exit()
