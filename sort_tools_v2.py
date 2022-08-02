#sort_tools module
#version 2
#now organized with a class structure
#file contains two classes: Sort_tools and Db_tools
#Sort_tools contains functions for munging and manipulating data
#Db_tools contains functions for interacting with database and solving db related problems

import pandas as pd
import numpy as np

class Sort_tools:

    @staticmethod
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

    

    @staticmethod
    def print_unique(df:object, key_list:list) -> None:
        
        '''Takes a list of keys from a df, iterates through and prints unique values for each'''
        
        for key in key_list:
        
            u_vals = set(df[key].to_list())
        
            print(f'unique values in column {key} are: {u_vals}')

        return

    @staticmethod        
    def find_unique(dataframe:object, key:str) -> set:

        '''This function takes a dataframe and key, 
        and returns a set of unique values from that column of the df'''
        
        #send the dataframe[key] column to a list
        fun_list = dataframe[key]
        
        #use set() to find unique values in the list
        fun_set = set(fun_list)
        
        return fun_set

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    #switcheroo_v3 is the best and fastest function I've written for swapping key values
    def switcheroo_v3(translate_df:object, target_df:object, target_key:str) -> object:
        
        '''Use a traslator table between two keys to swap keys

        Translate_df: df with one column for the desired key, and one for the old key.
        
        This function is way better for long columns than v2
        '''
        
        target_df = pd.merge(translate_df, target_df, on = target_key, how = 'right')
        
        target_df = target_df.drop(columns = [target_key])
        
        return target_df 

    @staticmethod
    #use merges to count matching values
    def count_matching(df1:object, df2:object, match_key:str) -> int:
        
        '''Returns a count based on the records that match in two different dataframes '''
        
        match = pd.merge(df1, df2, how = 'inner', on = match_key)
        
        match_count = len(match)
        
        return match_count

    @staticmethod
    def count_loop(df_list:list, name_list:list, comp_df:object, match_key:str) -> object:
        
        '''
        create a dataframe with counts based on matching entries in another dataframe

        uses the count matching function
        
        '''
        def count_matching(df1:object, df2:object, match_key:str) -> int:
        
            '''Returns a count based on the records that match in two different dataframes '''
        
            match = pd.merge(df1, df2, how = 'inner', on = match_key)
        
            match_count = len(match)
        
            return match_count
        
        results_list = []
        
        for df in df_list:
            
            result = count_matching(df, comp_df, match_key)
            
            results_list.append(result)
            
        result_df = pd.DataFrame({'category': name_list, 'count': results_list})
        
        return result_df

    @staticmethod
    #use this function to iteratively filter dfs
    def filter_base(df:object, lower_bound:int, upper_bound:int, key_string:str) -> object:
        
        '''filters a dataframe based on a key string and interger lower and upper bounds'''
        
        age_bound = df[(df[key_string] >= lower_bound) & (df[key_string] < upper_bound)]
        
        return age_bound

    @staticmethod
    def count_groups(df:object, group_key:str, count_key:str) -> object:
        
        '''
        Does a groupby calculation to enumerate the members of a group in a particular dataframe
        
        Returns a dataframe in the format I generally find desirable for this kind of analysis
        
        '''
        
        prune_df = df[[group_key, count_key]].copy()
        
        prune_df = prune_df.groupby(group_key).count()
        
        prune_df = prune_df.reset_index()
        
        prune_df = prune_df.rename(columns = {count_key: 'count'})
        
        return prune_df

    @staticmethod
    def substring_filter(df:object, ta_key:str, keywords:list, delimiter:str) -> object:
        
        '''
        Filter a dataframe using substrings in a string column.
        
        df: the dataframe to process
        
        ta_key: key corresponding to your column of string values
        
        keywords: a list of strings. rows whose index include any of these substrings in the ta_key column will be included in
        the dataframe returned by the function
        
        delimiter: what value will substrings in the string column will be separated by

        originally called 'text_array_filter'
        
        '''
        
        #add the array to a list
        df_list = df[ta_key].to_list()
        
        #lower the case of the keyword
        keywords = [key.lower() for key in keywords]
        
        #setup a list for a binary value referring to the presence or absence of the keyword
        key_binary = []
        
        #prepare the key binary list to hold a pass or fail score for presence of the keyword    
        for l in df_list:
            
            #decompose on the delimiter
            string_comps = l.split(delimiter)
            
            #lower the case
            string_comps = [s.lower() for s in string_comps]
            
            #look for the keywords in string comps
            
            key_bit = 0
            
            for k in keywords:
            
                if k in string_comps:
                
                    #make key_bit = 1
                    key_bit = 1
                    
            key_binary.append(key_bit)

                
        #add key_binary to the dataframe as a new column
        df['key_binary'] = key_binary
        
        #filter for key_binary = 1
        df = df[df['key_binary'] == 1]
        
        #drop the key_binary column
        df = df.drop(columns = ['key_binary'])
        
        return df


class Db_tools:

    @staticmethod
    def clob_destroyer(clob_list:list) -> list:
    
        '''This function converts a list or array of clobs to their string values
        The function is designed for an oracle database, and requires cx_Oracle.read()
        
        '''
        
        out_list = []
        
        for clob in clob_list:
        
            c_text = clob.read()
            
            out_list.append(c_text)
            
        return out_list

    @staticmethod
    def construct_table(df:object, name_string:str, dtype_dict:dict, p_key:str, fk_list:list, ref_list:list, eng:object) -> str:
        
        '''
        This function inserts a df into a database, and automatically 

        This is a function that relies on sql alchemy to create a table in an oracle database
        eng is a sql alchemy engine object

        function uses Oracle SQL

        '''
        
        #make table with pd.df.to_sql()
        df.to_sql(name_string, eng, if_exists = 'replace', index = False, dtype = dtype_dict)
        
        #set primary key
        pk_query = f'ALTER TABLE {name_string} ADD PRIMARY KEY ({p_key})'
        
        eng.execute(pk_query)
        
        #set foreign keys
        if fk_list == True:
        
            for k, r in zip(fk_list, ref_list):
            
                fk_query = f'ALTER TABLE {name_string} ADD FOREIGN KEY ({k}) REFERENCES {r}({k})'
            
                eng.execute(fk_query)
            
        return f'{name_string} table created'

    @staticmethod
    def wipe_db(table_list:list, eng:object) -> str:
        
        '''
        Wipe a full database using an sql alchemy engine
        
        For this to work you need to pass a list, that is correctly ordered in a way that the table can be dropped
        A table cannot be dropped if it contains foreign keys that reference a primary key in another table; that 
        table with the primary key must be dropped first. Drop the central tables first, then the ones at the periphery

        function uses Oracle SQL
        '''
        
        for table in table_list:
            
            drop_query = f'DROP TABLE {table}'
            
            try:
                eng.execute(drop_query)
                print(f'query {drop_query} executed')
                
            except:
                print(f'query {drop_query} not executed due to error')
                
        return 'Database Wipe Executed'