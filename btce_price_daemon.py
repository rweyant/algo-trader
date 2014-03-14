#!/usr/bin/python
import btceapi
from collections import deque
import csv
import time
import pickle
from trades import trades

def mean(x):
    return sum(x)/len(x)

def getPrice(connection,f,tmp_f,pair="btc_usd"):
    
    #get ticker
    ticker = btceapi.getTicker(pair, connection)
    #print ticker.high
    
    #get asks/bids
    asks, bids = btceapi.getDepth(pair)
    ask_prices, ask_volumes = zip(*asks)
    bid_prices, bid_volumes = zip(*bids)

    #start list with all of the ticker info
    curTrades = trades(coin='ltc',updated=ticker.updated,server_time=ticker.server_time,buy=ticker.buy,sell=ticker.sell)
    #print out_list
    #now we have a huge list with all the info, write to a single line in the csv file
    
    line = ','.join((pair,str(time.mktime(time.localtime())),str(curTrades.buy)))+'\n'
    #print line
    f.write(line)
    tmp_f.write(line)
    # Pickle class using protocol 0.
    
    
def collect_data(wait=60):
       
    # infinite loop
    while 1:
        # Keep a running list of everything
        btc_usd_f = open('/media/Big Daddy/New_Documents/python/python_projects/trading/data/btc_usd_btce.txt', 'a')
        ltc_btc_f = open('/media/Big Daddy/New_Documents/python/python_projects/trading/data/ltc_usd_btce.txt', 'a')
        ltc_usd_f = open('/media/Big Daddy/New_Documents/python/python_projects/trading/data/ltc_btc_btce.txt', 'a')

        # Temporary files for loading into observers
        btc_usd_tmp = open('/media/Big Daddy/New_Documents/python/python_projects/trading/data/btc_usd_btce.tmp', 'w')
        ltc_btc_tmp = open('/media/Big Daddy/New_Documents/python/python_projects/trading/data/ltc_usd_btce.tmp', 'w')
        ltc_usd_tmp = open('/media/Big Daddy/New_Documents/python/python_projects/trading/data/ltc_btc_btce.tmp', 'w')

        #initialize connection
        connection = btceapi.BTCEConnection()
        
        try:    getPrice(connection,btc_usd_f,btc_usd_tmp,'btc_usd')
        #if connection is lost, just try to reconnect (this does seem to happen, so this line is actually pretty important for long data collects)
        except:
            print 'BTC problemo'
            connection = btceapi.BTCEConnection()

        try:    getPrice(connection,ltc_btc_f,ltc_btc_tmp,'ltc_btc')
        #if connection is lost, just try to reconnect (this does seem to happen, so this line is actually pretty important for long data collects)
        except: 
            print 'ltc-btc problem'
            connection = btceapi.BTCEConnection()
        
        try:    getPrice(connection,ltc_usd_f,ltc_usd_tmp,'ltc_usd')
        #if connection is lost, just try to reconnect (this does seem to happen, so this line is actually pretty important for long data collects)
        except: 
            print 'ltc-usd problem'
            connection = btceapi.BTCEConnection()        
     
        print 'done loop'

        # Close everything in between runs so that there are 
        # no issues with simultaneous read/write
        btc_usd_f.close()
        ltc_btc_f.close()
        ltc_usd_f.close()
        
        btc_usd_tmp.close()
        ltc_usd_tmp.close()
        ltc_btc_tmp.close()
     
        #sleep for X seconds
        time.sleep(wait)

def main():
    collect_data(wait=60)
    
if __name__ == '__main__':
    main()