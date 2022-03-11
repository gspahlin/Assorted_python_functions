#excel_tools
import pandas as pd
import numpy as np
import xlwings as xw

#function for DataFraming an Excel Sheet

def dframe_a_sheet(sheet_name, cell_range, file_path):
    
    #create an xw Book object from the file path
    db_book = xw.Book(file_path)

    #create a sheet object for a sheet in bht book db_book
    dummy_sheet = db_book.sheets[sheet_name]
    
    #dataframe it
    dummy_df = dummy_sheet[cell_range].options(pd.DataFrame, index = False, header = True).value
    
    #return the dataframe
    return dummy_df
