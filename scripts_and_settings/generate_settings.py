# -*- coding: utf-8 -*-
"""
script to create json file for settings in web state application 
"""
import json
settings = {
    'pages'    :    {'Rivers'               :    r'https://github.com/lukefullard/State_and_Trends_Reporting/blob/main/state_results/Rivers_data_file.xlsx',
                     'Lakes'                :    r'https://github.com/lukefullard/State_and_Trends_Reporting/blob/main/state_results/lakes_data_file.xlsx',
                     'Contact Recreation'   :    r'https://github.com/lukefullard/State_and_Trends_Reporting/blob/main/state_results/contactrec_data_file.xlsx',
                     },
    #
    #geospatial
    'x_column'                 : 'NZTM.X',
    'y_column'                 : 'NZTM.Y',
    'epsg_code'                : 2193,
    #
    
    
    }

with open('app_settings.json', 'w') as fp:
    json.dump(settings, fp)