#!/usr/bin/python

'''
This class follows one strategy...
need something more helpful here
'''

from common import *
from observer import *
from overlord import *
import numpy as np
from numpy import mean
import matplotlib.pyplot as plt


class GrandObserver:
    # constructor
    def __init__(self,source=None):
        '''
        '''
        # what do here?
        self.worth=[]
        self.percents_list = []
        self.action_list = []
        self.keys = []

        self.absolute_max = []
        self.orders = []
        self.order_time_index=[]
        self.actions = []   
        
    def loadData(self):
        ''' 
        '''
        # read in price data
        price_data = loadData('data/btc_usd_btce.txt')
        self.max_time = price_data[1,:]
        self.price = price_data[0,:]
        
        # initial load
        x = dict()
        
        # open up every daily_percent* file and add it in.
        # store it in temporary dictionary x, eventually into x_array
        i = 0
        results_dir = [result for result in os.listdir('results/')  if 'daily_percent' in result]
        for result in results_dir:
            i = i+1
            if i > 3: break
            with open('results/'+result,'rb') as f:
                while True:
                    try:
                        tmp = pickle.load(f)
                        x = dict(x.items() + tmp.items())
                    except EOFError:
                        print 'Done Loading results/%s' % result
                        break
                
        # extract daily percent increase and action lists from temporary dictionary x

        for key in x.keys():
            self.keys.append(key)
            self.percents_list.append(x[key][0])
            self.action_list.append(x[key][1])
            
        # make everything the same length
        self.individual_time = [self.max_time[len(i)] for i in self.percents_list ]
        self.individual_time_index = [len(i) for i in self.percents_list]
        self.timeFrame=min(self.individual_time_index)
        
        current_max_method_index = -1

        # go through whole history and make historical trades.  
        # update 3 lists: orders, actions, absolute_max.
        for i in range(self.timeFrame):
            
            # if we are past the first entry, and action in (-1,1)
            # then place a historical order
            if current_max_method_index != -1 and self.action_list[current_max_method_index][i] != 0:
                self.orders.append(self.price[i])
                self.order_time_index.append(i)
                self.actions.append(self.action_list[current_max_method_index][i])
            
            # max VALUE at current time
            current_slice = [line[i] for line in self.percents_list]
            current_max_value=max(current_slice)
            
            # INDEX strategy that maximuzes
            current_max_method_index= current_slice.index(current_max_value)
            current_max_method = self.keys[current_max_method_index]
            # add max value
            self.absolute_max.append((current_max_value,current_max_method_index))
        

    def update(self,price,time):
        '''
        '''
        results_dir = 'results/'
        # find all short_daily_percent files
        i = 0
        results_listing = [result for result in os.listdir(results_dir)  if 'short_dp' in result]
        
        # load all short_daily_percent info
        initial_load = []
        for result in results_listing:
            # multiple line files
            # id, time, parameters,daily profit, action
            with open(results_dir+result,'r') as f:
                for line in f:
                    (time,ma,md,smooth,percent,riseTol,lossTol,dp, action) = line.split(',')
                    newLine = (time,(ma,md,smooth,percent,riseTol,lossTol),dp, action)
                    initial_load.append(newLine)
       
        # remove short_daily_percent files
        #for result in results_dir:
        #    os.remove(results_dir+result)
        
        # sort new entries by time
        if len(initial_load) > 1:
            tmpArray = np.array(initial_load)
            initial_load = tmpArray[tmpArray[:,0].argsort()].tolist()

        # find unique parameter sets
        parameterSets = set([line[1] for line in initial_load])

        # for each unique parameter set, update in order.        
        for params in parameterSets:
            currentUpdates = [line for line in initial_load if line[1] == params]
    
            # step through short_daily_percent info and see load it into grand-observer
            for line in currentUpdates:
                (time,parameters,daily_profit,action) = line
                current_method = self.keys.index(parameters)
                # if current time beyond last time point
                if time > self.individual_time[current_method]:
                    self.individual_time_index[current_method] = self.max_time.index(time)
                    self.individual_time[current_method] = time
                    self.action_list[current_method].append(action)
                    self.percents_list[current_method].append(daily_profit)

        # make everything the same length
        oldTimeFrame = self.timeFrame
        self.timeFrame=min(self.individual_time_index)
        current_max_method_index = -1
                    
        # if any action needs to be taken, alert.
        for i in range(self.timeFrame):
            
            # if we are past the first entry, and action in (-1,1)
            # then place a historical order
            if current_max_method_index != -1 and self.action_list[current_max_method_index][i] != 0:
                self.orders.append(self.price[i])
                self.order_time_index.append(i)
                self.actions.append(self.action_list[current_max_method_index][i])
            
            # max VALUE at current time
            current_slice = [line[i] for line in self.percents_list]
            current_max_value=max(current_slice)
            
            # INDEX strategy that maximuzes
            current_max_method_index= current_slice.index(current_max_value)
            current_max_method = self.keys[current_max_method_index]
            # add max value
            self.absolute_max.append((current_max_value,current_max_method_index))

        

    def buy(self):
        ''' 
        This function simulates buying BTC with USD
        Right now, it exchanges all USD for BTC.
        '''
        pass

        
    def sell(self,ALERT=False, EXECUTE=False):
        ''' 
        This function simulates selling BTC for USD
        Exchange ALL BTC for USD
        '''
        pass
        
    def step(self,price,time,backup=0):
        pass

    def current_profit(self,start=0):
        ''' 
        quick calculation of current profit status 
        based off of self.orders list
        includes fees
        trade_type  = -1 for buys ($/price)
                    =  1 for sells ($*price)
        *** would be nice to find a way to window this to past X days or something
        '''
        pass


test = GrandObserver()
test.loadData()