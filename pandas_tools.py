#pandas tools
import pandas as pd
import numpy as np

#a simple function for finding unique values in the column of a dataframe

def find_unique(dataframe, key):
    
    #send the dataframe[key] column to a list
    fun_list = dataframe[key]
    
    #use set() to find unique values in the list
    fun_set = set(fun_list)
    
    return fun_set