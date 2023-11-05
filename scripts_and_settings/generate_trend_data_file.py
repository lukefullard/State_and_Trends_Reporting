# -*- coding: utf-8 -*-
"""
script to prepare output data files from state analysis for uploading to public repo
"""
import pandas as pd
import geopandas as gpd
import os
import copy
import json

def load_settings():
    settings = {
        'data_files'               :  {
                        'Rivers'                 : 'RIVER FILE LOCATION HERE',
                        # 'Lakes'                  : 'LAKES FILE LOCATION HERE',
                        'Contact_Recreation'     : 'CONTACT REC FILE LOCATION HERE',
                        },
        #
        'save_folder'              :'FOLDER TO SAVE FILE TO',
        #
        #
        'remove_filter_fails'      : False,
        'filter_column_name'       : 'FilterOK',
        'attribute_column_name'    : 'npID', 
        #
        #
        'include_units'            : True,
        #
        'include_geospatial'       : True,
        'x_column'                 : 'NZTM.X',
        'y_column'                 : 'NZTM.Y',
        'epsg_code'                : 2193,
        'shapefiles'             : {'District'                   :{'location'     : r'FILE LOCAION',
                                                                    'column_name'  : 'TA2014_NAM'
                                                                    },
                                    'Freshwater Management Unit' :{'location'     : r'FILE LOCAION',
                                                                    'column_name' : 'Name'
                                                                    },
                                    'Water management Zone'      :{'location'     : r'FILE LOCAION',
                                                                    'column_name' : 'ManageZone'
                                                                    },
                                    'Water management Subzone'   :{'location'     : r'FILE LOCAION',
                                                                    'column_name' : 'Zone_Code'
                                                                    },
                                    },
        #
        'columns_to_keep'          : ['sID','npID','Trend_Period','Seasonal_trend','AnalysisNote',
                                      'Cd','prop.censored','prop.unique','no.censorlevels',
                                      'Median','AnnualSenSlope','Sen_Lci','Sen_Uci','Percent.annual.change',
                                      'Status','Improving_Confidence'
                                      ],
        'column_renaming_map'        : {
                    'sID'                   :'site name',
                    'npID'                  :'variable',
                    'Trend_Period'          :'trend period',
                    'Status'                :'site type',
                    'Seasonal_trend'        :'seasonal trend',
                    'AnalysisNote'          :'analysis note',
                    'Cd'                    :'confidence that trend direction is decreasing',
                    'prop.censored'         :'proportion of censored observations',
                    'prop.unique'           :'proportion of unique observations',
                    'no.censorlevels'       :'number of censor levels',
                    'Median'                :'median value for the trend period',
                    'AnnualSenSlope'        :'annual Sen slope (attribute units/year)',
                    'Sen_Lci'               :'lower confidence interval for annual Sen slope',
                    'Sen_Uci'               :'upper confidence interval for annual Sen slope',
                    'Percent.annual.change' :'percent annual change in Sen slope ',
                    'Improving_Confidence'  :'confidence of improving trend',
                    },   
        #
        'attribute_name_mapping'   : {
            'ASPM'      :'ASPM (Macroinvertebrate Average Score Per Metric)',    
            'CLAR'      :'Visual Clarity',
            'Chl_a'     :'Chlorophyll A',
            'DO_Conc'   :'Dissolved Oxygen Concentration',
            'DRP'       :'Dissolved Reactive Phosphorus',
            'ECOLI'     :'E. coli',
            'MCI'       :'MCI (Macroinvertebrate Community Index)',
            'NH4N_adj'  :'Ammoniacal Nitrogen (NH4)',
            'NO2'       :'Nitrite Nitrogen (NO2)',
            'NO3'       :'Nitrate Nitrogen (NO3)',
            'pH'        :'pH',
            'QMCI'      :'QMCI (Quantitative Macroinvertebrate Community Index)',
            'SIN'       :'SIN (Soluble Inorganic nitrogen)',
            'SSC'       :'Suspended Sediment Concentration',
            'TN'        :'Total Nitrogen',
            'TP'        :'Total Phosphorus',
            'TURB'      :'Turbidity',
                        },
        #
        #
        #
        'attribute_units'          : 
            
            {
                'ASPM'      :'',    
                'CLAR'      :'m',
                'Chl_a'     :'mg/m2',
                'DO_Conc'   :'g/m3',
                'DRP'       :'mg/L',
                'ECOLI'     :'E. coli/100 mL',
                'MCI'       :'',
                'NH4N_adj'  :'mg/L',
                'NO2'       :'mg/L',
                'NO3'       :'mg/L',
                'pH'        :'',
                'QMCI'      :'',
                'SIN'       :'g/m3',
                'SSC'       :'mg/L',
                'TN'        :'g/m3',
                'TP'        :'g/m3',
                'TURB'      :'NTU/FNU',
                            },
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
def get_site_location(gdf,reference_gdf,settings):
    nearest_results = gpd.sjoin_nearest(gdf, reference_gdf.to_crs(settings.get('epsg_code')), 
                                        distance_col='distance', max_distance=250,
                                        how = 'left')
    return nearest_results
    

###############################################################################
###############################################################################
###############################################################################
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
    os.makedirs(settings.get('save_folder'), exist_ok=True)
    
    for file_j in settings.get('data_files').keys():
        #load data
        data = load_data(settings.get('data_files').get(file_j))
        
        #remove filter fails
        if settings.get('remove_filter_fails'):
            data = data.loc[data[settings.get('filter_column_name')] == True].reset_index(drop=True)
            
        #remove unneeded attributes
        data = data.loc[data[settings.get('attribute_column_name')].isin(list(settings.get('attribute_name_mapping').keys()))].reset_index(drop=True)
         
        #columns to keep
        columns_to_keep = copy.deepcopy(settings.get('columns_to_keep'))
        if settings.get('include_geospatial'):
            columns_to_keep.append(settings.get('x_column'))
            columns_to_keep.append(settings.get('y_column'))
            for region_j in settings.get('shapefiles').keys():
                columns_to_keep.append(region_j)
                data[region_j] = ''
                data_copy = copy.deepcopy(data)
                gdf = gpd.GeoDataFrame(
                        data_copy, geometry=gpd.points_from_xy(data_copy[settings.get('x_column')], data_copy[settings.get('y_column')]), crs=f"EPSG:{settings.get('epsg_code')}"
                    )
                ref_gdf = gpd.read_file(settings.get('shapefiles').get(region_j).get('location'))
                region_result = get_site_location(gdf,ref_gdf,settings)

                if len(data) != len(region_result):
                    raise ValueError('Length of dataframe not equal to geodataframe')
                
                data[region_j] = list(region_result[settings.get('shapefiles').get(region_j).get('column_name')])    

                
        
        #add units
        if settings.get('include_units'):
            columns_to_keep.append('units')
            units = []
            for index_j,row_j in data.iterrows():
                units.append(settings.get('attribute_units').get(row_j[settings.get('attribute_column_name')],''))
            data['units'] = units    
    
        #remove unneeded columns
        #first check if columns exist
        columns_to_keep_final = [x for x in columns_to_keep if x in data.columns]
        data = data[columns_to_keep_final]
     
        #rename attributes
        new_attribute_name = []
        for index_k,row_k in data.iterrows():
            old_name = row_k[settings.get('attribute_column_name')]
            new_attribute_name.append(
                settings.get('attribute_name_mapping').get(old_name,old_name)
                )
        data[settings.get('attribute_column_name')]  = new_attribute_name    
     
        #rename columns
        data = data.rename(columns=settings.get('column_renaming_map'))
        
        #fix NOF grades
        if settings.get('fix_NOF_Grade'): 
            data.loc[~data[settings.get('nof_column_name')].isin(settings.get('allowed_nof_grades')), settings.get('nof_column_name')] = ""

        #save data 
        save_name = os.path.join(settings.get('save_folder'),file_j+'.xlsx')
        data.to_excel(save_name,index=False)
        
        
        
        sites_data = data[['site name'] + list(settings.get('shapefiles').keys())].drop_duplicates().reset_index(drop=True)
        sites_dict = {}
        for index_q,row_q in sites_data.iterrows():
            new_dict = {}
            for col_q in settings.get('shapefiles').keys():
                new_dict.update({col_q:row_q[col_q]})
            sites_dict.update({row_q['site name']:new_dict})
        
        # with open(f'{file_j}_sites.json', 'w') as fp:
        #     json.dump(sites_dict, fp)
            
        #create site list
        all_sites = list(data['site name'].unique())
        #create new folder
        new_folder = os.path.join(settings.get('save_folder'),file_j)
        os.makedirs(new_folder, exist_ok=True)
        for site_p in all_sites:
            clean_site_name = clean_text(site_p, add_hash=True)
            sub_data = data.loc[data['site name'] == site_p].reset_index(drop=True)
            #save data
            save_name = os.path.join(new_folder,clean_site_name + '.xlsx')
            sub_data.to_excel(save_name,index=False)
        

###############################################################################
###############################################################################
###############################################################################

if __name__ == '__main__':
    main()




