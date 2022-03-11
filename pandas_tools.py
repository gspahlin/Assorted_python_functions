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


#write a function to split a column with a range of numbers into two
#the function takes the name of a dataframe, a key, and a delimiter as arguments
#the key and delimiter are passed as strings



def range_split(df, key, delimiter):
    
    #make the dataframe column a list
    range_list = df[key].to_list()
    
    #instantiate two lists to catch max and min values
    max_list = []
    min_list = []
    
    #Loop through the range list, splitting at the delimiter
    for r in range_list:
        
        #check to see if r is a null value
        if r is not None:
        
            #form a list for r containing the range of values
            r_values = r.split(delimiter)
                                        
            #loop through r_values and strip whitespace
            r_values = [v.strip() for v in r_values]
            
            #change the type to the float datatype if it isn't already
            r_values = list(map(float, r_values))
            
            #sort the list so values are in ascending order
            r_values.sort()
            
            #append values to appropriate lists
            min_list.append(r_values[0])
            
            max_list.append(r_values[-1])
        
        #in case of None append the None to each list
        else:
            
            min_list.append(None)
            
            max_list.append(None)
    
    #create new names for the lists
    
    max_name = f'{key}_max'
    
    min_name = f'{key}_min'
    
    #add the new columns to the dataframe
      
    
    df[min_name] = min_list
    
    df[max_name] = max_list
    
    #drop the original column 
    
    df.drop(columns = [key], inplace = True)
    
    all_good = f'{key} column split, no errors'
    
    return all_good
