#Tools for sorting data direct outputs

#this version of the function is current as of 5/23/2022
#contains code for patients who don't have procedures of a certain kind
#modded to avoid side effects and return a tuple of lists - one for quantifying longest procedure interval, and one for a list of procedure dates

import pandas as pd
import numpy as np

def pt_date_interval(pt_list:list, evnt_tbl_pt_list:list, date_list:list) -> tuple:
    
    '''
    calculate procedure intervals and retrieve a list of procedure dates for a list of patients
    
    args:
    pt_list - a filtered patient list with more than 2 ct scans or some other criterion possibly
    
    evnt_tbl_pt_list - a full list of patient ids from a list of procedures or other events
    
    date_list - the corresponding list of dates (datetime values) from those events
    
    returns:
    delta_list - a list that holds the number of days between the first and last procedure or event for a patient, as an integer
    
    pt_date_list - the dates of each CT scan or other procedure for each patient. Returned as a list of strings for each patient
    
    '''
    #start by generating a list for interval deltas and dates
    pt_date_list = []
    
    delta_list = []
    
    #start by looking through the target patient list
    for pt in pt_list:
        
        #make a list for relevant dates
        pt_dates = [] 
        
        #initialize counter
        
        counter = 0
        
        #iterate through the pt_id_coulumn
        for p in evnt_tbl_pt_list:

             
            #look for a match with the current patient number
            if pt == p:
                
                #store the information from the date column in a variable when found
                sig_dt = date_list[counter]
                
                #append sig_dt to pt_dates
                pt_dates.append(sig_dt)
                
            #count up each time loop runs to keep track of position
            counter += 1
            
        #test for an empty list here
        if pt_dates:
        
            #Order the dates chronologically (early to late)
            pt_dates.sort()
        
            #Calcuate time elapsed from first to last
            time_el = pt_dates[-1] - pt_dates[0]
            
            #convert time_el from timedelta to integer (days)
            time_el = pd.to_numeric(time_el.days, downcast = 'integer')
            
            #format the dates as dates by converting to string
            pt_date_strings = []
            
            for d in pt_dates:
                day = d.strftime('%d')
                month = d.strftime('%m')
                year = d.strftime('%Y')
                date_st = f'{month}/{day}/{year}'
                
                pt_date_strings.append(date_st)
      
            #add found dates to pt_date_list
            pt_date_list.append(pt_date_strings)
        
            #append time elapsed to the return list
            delta_list.append(time_el)
            
        #in case the list is empty it will evaluate as false
        #if this happens I need placeholders to keep things lined up properly 
        
        else:
            pt_date_list.append('No Procedures Found')
            delta_list.append('N/A')
                
                
    return (delta_list, pt_date_list)

#print_unique and find_unique are both for finding unique values in dataframe columns 

def print_unique(df:object, key_list:list) -> None:
    
    '''Takes a list of keys from a df, iterates through and prints unique values for each'''
    
    for key in key_list:
    
        u_vals = set(df[key].to_list())
    
        print(f'unique values in column {key} are: {u_vals}')

    return
        

def find_unique(dataframe:object, key:str) -> list:

    '''This function takes a dataframe and key, 
    and returns a set of unique values from that column of the df'''
    
    #send the dataframe[key] column to a list
    fun_list = dataframe[key]
    
    #use set() to find unique values in the list
    fun_set = set(fun_list)
    
    return fun_set

#I used this to set up and key tables in my database

def unique_val_table(df:object, id_string:str) -> object:
    
    '''Takes a table with repeating values, drops dupes, resets index and sets up an integer key with 
    the column title given by the id_string. df should be a dataframe, and id_string should be a string '''
    
    #find unique values and scrub initial index values

    df = df.drop_duplicates()

    df = df.reset_index()

    df = df.drop(columns = ['index'])
    
    #adding 1 so that I can index from one instead of zero
    extnt = len(df)+1
    
    #set up a key value using a series from numpy
    df[id_string] = np.arange(1, extnt)
    
    return df

def switcheroo_v2(key_list:list, value_list:list, input_list:list) -> list:
    
    ''' This function takes two ordered lists and a list to be transformed. The values in the input_list should match one
    of the ordered lists, and there should be no overlap between the contents of the two lists. The function switches a matching
    value with its counterpart in the other list. 
    
    This version only works well for short columns or arrays. It is very slow for large ones. 
    '''
    
    #instantiate a list for output
    out_list = []    
      
    #iterate through the list to look for values in the codex
    for i in input_list:     
        
        #iterate through the key lists and look for a match where i == k
        for k, v in zip(key_list, value_list):
            
            if k == i:
                
                #in case of a match append v
                out_list.append(v)
                
            elif v == i:
                
                #if no match is found see if v matches i. If it does append k
                out_list.append(k)
                
    return out_list

#switcheroo_v3 is the best and fastest function I've written for swapping key values
def switcheroo_v3(translate_df:object, target_df:object, target_key:str) -> object:
    
    '''Use a traslator table between two keys to swap keys

    Translate_df: df with one column for the desired key, and one for the old key.
    
    This function is way better for long columns than v2
    '''
    
    target_df = pd.merge(translate_df, target_df, on = target_key, how = 'right')
    
    target_df = target_df.drop(columns = [target_key])
    
    return target_df

#use merges to count matching values
def count_matching(df1:object, df2:object, match_key:str) -> int:
    
    '''Returns a count based on the records that match in two different dataframes '''
    
    match = pd.merge(df1, df2, how = 'inner', on = match_key)
    
    match_count = len(match)
    
    return match_count

def count_loop(df_list:list, name_list:list, comp_df:object, match_key:str) -> object:
    
    '''create a dataframe with counts based on matching entries in another dataframe

    uses the count matching function
       
    '''
    
    results_list = []
    
    for df in df_list:
        
        result = count_matching(df, comp_df, match_key)
        
        results_list.append(result)
        
    result_df = pd.DataFrame({'category': name_list, 'count': results_list})
    
    return result_df

#use this function to iteratively filter dfs
def filter_base(df:object, lower_bound:int, upper_bound:int, key_string:str) -> object:
    
    '''filters a dataframe based on a key string and interger lower and upper bounds'''
    
    age_bound = df[(df[key_string] >= lower_bound) & (df[key_string] < upper_bound)]
    
    return age_bound

def clob_destroyer(clob_list:list) -> list:
    
    '''This function converts a list or array of clobs to their string values
    The function is designed for an oracle database, and requires cx_Oracle.read()
    
    '''
    
    out_list = []
    
    for clob in clob_list:
    
        c_text = clob.read()
        
        out_list.append(c_text)
        
    return out_list