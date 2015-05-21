# Author @Yingping Su
# Date: 2015/05/16
# demo of trading_system 
# task 1 : find all stocks for given exchange on available days
# task 2 : obtain necessary data for stocks  
# task 3 : build object contains get_edge 
# task 4 : calculate all edges for all stocks and pass it to set_total_edge

from trading_system import TradingSystem
from sys import argv
import datetime

exchange = argv[1]

trd_sys = TradingSystem()
#find all available days
DaySeries = trd_sys.get_days(exchange)
BusinessDays = sorted(filter(lambda x : 1 <= x.date.weekday() and x.date.weekday() <= 5, DaySeries),reverse = True) 
#extract the current available day
currentBusinessDay = BusinessDays[0]

#get recent stocks from a given exchange, return a list of symbol
stocks_symbol_list = map(lambda x : x[0] , list(set(filter(lambda x : x[1] == exchange, trd_sys.get_stocks(currentBusinessDay)))));
#tell trd_sys a set of stocks we need
trd_sys.set_stocks(stocks_symbol_list) 

class stock:
    def __init__(self, _symbol):
        self.symbol = _symbol
    def get_stock_price_perday(self, day):
        return getattr(trd_sys, "get_stock_data_" + self.symbol)(day) if hasattr(trd_sys, "get_stock_data_" + self.symbol) else None
    def get_edge(self, current_price): 
        edgeList = []
        #check valid:
        if(trd_sys.is_valid_symbol(self.symbol, exchange)): 
            count = 0
            i = 0
            while(len(edgeList)<10):
                stock_price_perday = self.get_stock_price_perday(BusinessDays[i]);
                if not stock_price_perday:
                    i += 1
                    continue
                if stock_price_perday.get('high') >= stock_price_perday.get('low'):
                    edgeList += [current_price - stock_price_perday.get('close')]
                    count = 0
                else:
                    count += 1
                    if count == 5:
                        edgeList += [current_price - stock_price_perday.get('close')]
                        count = 0  
                i += 1
                           
        #calculate mean and variance of EdgeList       
        meanEdge = float(reduce(lambda x,y : x+y, edgeList)) / len(edgeList)
        varEdge = reduce(lambda x,y: x+y, map(lambda xi: (xi-meanEdge)**2, edgeList))/ len(edgeList)
        total_edge = sum(edgeList)
        return total_edge, meanEdge, varEdge
		
#calculate all edges from total stocks 
total_stocks_edge = []
for sym in stocks_symbol_list:
    singleStock = stock(sym)
    if hasattr(trd_sys, "set_stocks_param_" + sym):
        getattr(trd_sys, "set_stocks_param_" + sym)(singleStock)
    current_price = getattr(trd_sys, "get_stock_data_" + sym)(currentBusinessDay).get('close')
    total_stocks_edge += [singleStock.get_edge(current_price)]
	
#pass sum of list of total_stocks_edge  
edge_total_value = sum(total_stocks_edge)
trd_sys.set_total_edge(edge_total_value)