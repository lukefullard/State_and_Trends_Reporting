# -*- coding: utf-8 -*-
"""
script to prepare output data files for raw data used in state analysis for uploading to public repo
"""
import pandas as pd
import os
import copy


def load_settings():
    settings = {
        'data_files'               :  {
                        'Rivers'         : 'RIVER FILE LOCATION HERE',
                        'Lakes'           : 'LAKES FILE LOCATION HERE',
                        'Contact_Recreation'      : 'CONTACT REC FILE LOCATION HERE',
                        },
        #
        'save_folder'              : 'FOLDER TO SAVE FILE TO',
        #

        'columns_to_keep'          : ['sID','npID','SampleDate','Value','Project','Method','Unit','QC','ph'],
        'column_renaming_map'      : {
                    'sID'          :'site name',
                    'npID'         :'parameter name',
                    'SampleDate'   :'date time',
                    'QC'           :'Quality code',
                    'ph'          :'pH',
                    },   
        #
        'site_name_new_column_name':'site name'
        }
    return settings

###############################################################################
###############################################################################
###############################################################################
def read_xlsx_or_csv(file_location,encoding):
    '''
    This function tries to open a provided file first as an xlsx then csv. 
    In case of failure, it throws a type error.

    Parameters
    ----------
    file_location : str
        String location of the file to load
    encoding : str
        String to define encoding to use to read csv files    

    Returns
    -------
    data : Pandas dataframe
        Data loaded as a Pandas dataframe

    '''
    
    try:
        data = pd.read_excel(file_location)
    except:
        try:
            data = pd.read_csv(file_location,encoding = encoding)
        except:
            raise TypeError('File MUST be of type either an xlsx or csv.')
            return None
    
    return data
###############################################################################
###############################################################################
###############################################################################
def load_data(data_file_location):
    #read data 
    try:
        data = read_xlsx_or_csv(data_file_location,'utf-8')
    except:
        try:
            data = read_xlsx_or_csv(data_file_location,'ISO-8859-1')
        except:
            try:
                data = read_xlsx_or_csv(data_file_location,'utf-8-sig')
            except:
                raise TypeError('File codec is incorrect.')
    return data            


###############################################################################
###############################################################################
###############################################################################
def clean_text(text, add_hash = False):
    '''
    Convenience function to clean text by removing unicode characters (such as macrons) and non-alpha-numeric characters (spaces, punctuation, symbols etc)

    Parameters
    ----------
    text : string
        DESCRIPTION: String to clean
        
    add_hash : Boolean, optional
        DESCRIPTION: The default is False. If True, adds an underscore + a hash to the text (to ensure uniqueness after cleaning).     

    Returns
    -------
    cleaned_text : string
        DESCRIPTION: cleaned string

    '''
    import unidecode
    cleaned_text = unidecode.unidecode(text)
    cleaned_text = ''.join(e for e in cleaned_text if e.isalnum())
    
    if add_hash:
        import hashlib 
        cleaned_text = cleaned_text + '_' + str(hashlib.shake_256(text.encode()).hexdigest(5))
    return cleaned_text
###############################################################################
###############################################################################
###############################################################################
def main():
    #load settings
    settings = load_settings()
    
    for file_j in settings.get('data_files').keys():
        #make output folder
        new_folder = os.path.join(settings.get('save_folder'),file_j)
        os.makedirs(new_folder, exist_ok=True)
        
        #load data
        data = load_data(settings.get('data_files').get(file_j))
        
        #columns to keep
        columns_to_keep_final = [x for x in settings.get('columns_to_keep') if x in data.columns]
        data = data[columns_to_keep_final]
        
        #rename columns
        data = data.rename(columns=settings.get('column_renaming_map'))
        
        #iterate through the sites in the data
        for site_j in data[settings.get('site_name_new_column_name')].unique():
            #filter data to site of interest
            sub_data = data.loc[data[settings.get('site_name_new_column_name')] == site_j].reset_index(drop=True)
            
            #get file compliant site name
            clean_site_name = clean_text(site_j, add_hash=True)
            
            #save data
            save_name = os.path.join(new_folder,clean_site_name + '.xlsx')
            sub_data.to_excel(save_name,index=False)

###############################################################################
###############################################################################
###############################################################################

###############################################################################
###############################################################################
###############################################################################

###############################################################################
###############################################################################
###############################################################################
if __name__ == '__main__':
    main()
