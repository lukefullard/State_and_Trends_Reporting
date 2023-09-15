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
                        # 'Rivers'                 : 'RIVER FILE LOCATION HERE',
                        # 'Lakes'                  : 'LAKES FILE LOCATION HERE',
                        # 'Contact_Recreation'     : 'CONTACT REC FILE LOCATION HERE',
                        'Rivers'                 : r'\\ares\Science\Luke\State and Trends\2023\OUTPUTS\Rivers\Rivers_State_Water_Years_2023-06-16.csv',
                        'Lakes'                  : r'\\ares\Science\Luke\State and Trends\2023\OUTPUTS\Lakes\Lakes_State_Water_Years_2023-09-15.csv',
                        'Contact_Recreation'     : r'\\ares\Science\Luke\State and Trends\2023\OUTPUTS\ContactRec\ContactRec_State_Water_Years_2023-06-15.csv',
                        
                        },
        #
        # 'save_folder'              : 'FOLDER TO SAVE FILE TO',
        'save_folder'              : r'\\ares\Science\Luke\State and Trends\reporting\State_and_Trends_Reporting\state_results',
        #
        #
        'remove_filter_fails'      : True,
        'filter_column_name'       : 'FilterOK',
        'attribute_column_name'    : 'Attr', 
        #
        #
        'include_units'            : True,
        #
        'include_geospatial'       : True,
        'x_column'                 : 'NZTM.X',
        'y_column'                 : 'NZTM.Y',
        'epsg_code'                : 2193,
        'shapefiles'             : {'District'                   :{'location'     : r'//ares/Hydrology GIS/External Data/District Boundaries/Districts.shp',
                                                                    'column_name'  : 'TA2014_NAM'
                                                                    },
                                    'Freshwater Management Unit' :{'location'     : r'//gisdata/GIS/Department/Catchment Information/Projects/POLICY/2020/48584_mapping_for_report/data/FMU_20210122.shp',
                                                                    'column_name' : 'Name'
                                                                    },
                                    'Water management Zone'      :{'location'     : r'//gisdata/GIS/Department/Policy/OnePlan/One_Plan/Operative_One_Plan/Shapefiles/Surface_Water/Water_Management_Zones.shp',
                                                                    'column_name' : 'ManageZone'
                                                                    },
                                    'Water management Subzone'   :{'location'     : r'//gisdata/GIS/Department/Policy/OnePlan/One_Plan/Operative_One_Plan/Shapefiles/Surface_Water/Water_Management_Subzones.shp',
                                                                    'column_name' : 'Zone_Code'
                                                                    },
                                    },
        #
        'fix_NOF_Grade'            : True,
        'allowed_nof_grades'       : ['A','B','C','D','E'],
        'nof_column_name'          : 'NOF_Grade',
        #
        'columns_to_keep'          : ['sID','Attr','NOF_Grade','yearz','Status',
                                      'Median','Mean','AnnMax','Q95','G540','G260','Median_Summer','p80','p83','p92'
                                      ],
        'column_renaming_map'      : {
                    'sID'          :'site name',
                    'Attr'         :'attribute type',
                    'yearz'        :'year range',
                    'Status'       :'site type',
                    'AnnMax'       :'Annual Maximum',
                    'Q95'          :'95th percentile',
                    'p80'          :'80th percentile',
                    'p83'          :'83rd percentile',
                    'p92'          :'92nd percentile',
                    'G540'         :'percentage of samples > 540 MPN',
                    'G260'         :'percentage of samples > 260 MPN',
                    'Median_Summer':'Median over summer period'
                    },   
        #
        'attribute_name_mapping'   : {
            'NOF.ASPM'             :'ASPM',
            'NOF.BIOVOL.p80'       :'Cyanobacteria Biovolume (80th percentile)',
            # 'NOF.CLAR.Med'         :'Clarity (Suspended fine sediment)',
            'NOF.Chl_a.p92'        :'Chlorophyll A (92nd Percentile)',
            'NOF.Chl_a.p83'        :'Chlorophyll A (83rd Percentile)',
            # 'NOF.Chl_a'            :'Chlorophyll A',
            'NOF.Chl_a.Med'        :'Chlorophyll A (Median)',
            'NOF.Chl_a.AMax'       :'Chlorophyll A (Annual Maximum)',

            # 'NOF.DRP.Combined'     :'DRP (Combined)',
            'NOF.DRP.Med'          :'DRP (Median)',
            'NOF.DRP.p95'          :'DRP (95th Percentile)',
            # 'NOF.Dep_Sed.Med'      :'Deposited Sediment (Median)',
            # 'NOF.ECOLI.Combined'   :'E coli (Combined)',
            'NOF.ECOLI.G260'       :'E coli (>260)',
            'NOF.ECOLI.G540'       :'E coli (>540)',
            'NOF.ECOLI.Med'        :'E coli (Median)',
            'NOF.ECOLI.p95'        :'E coli (95th Percentile)',
            'NOF.ECOLI_PC.p95'     :'E. coli (Primary Contact)',
            'NOF.MCI'              :'MCI',
            # 'NOF.NH4N.Combined'    :'Ammoniacal-N (Combined)',
            # 'NOF.NH4N.Max'         :'Ammoniacal-N (Max)',
            'NOF.NH4N.p95'         :'Ammoniacal-N (95th Percentile)',
            'NOF.NH4N.Med'         :'Ammoniacal-N (Median)',
            # 'NOF.NO3.Combined'     :'Nitrate-N (Combined)',
            'NOF.NO3.Med'          :'Nitrate-N (Median)',
            'NOF.NO3.p95'          :'Nitrate-N (95th Percentile)',
            'NOF.QMCI'             :'QMCI',
            'NOFc1'                :'Visual Clarity (Sediment class 1)',
            'NOFc2'                :'Visual Clarity (Sediment class 2)',
            'NOFc3'                :'Visual Clarity (Sediment class 3)',
            'NOFc4'                :'Visual Clarity (Sediment class 4)',
            # 'NOFds1'               :'Deposited Sediment (class 1)',
            # 'NOFds2'               :'Deposited Sediment (class 2)',
            # 'NOFds3'               :'Deposited Sediment (class 3)',
            # 'NOFds4'               :'Deposited Sediment (class 4)',
            'NOF.SIN.Med'          :'Soluble Inorganic Nitrogen (Median)',
            'NOF.SIN.p95'          :'Soluble Inorganic Nitrogen (95th Percentile)',
            # 'NOF.TN.Combined'      :'Total Nitrogen (Median)',
            'NOF.TN.MedSS'         :'Total Nitrogen (Median, stratified)',
            'NOF.TN.MedPoly'       :'Total Nitrogen (Median, polymictic)',
            'NOF.TN.Med'           :'Total Nitrogen (Median)',
            'NOF.TN.p95'           :'Total Nitrogen (95th Percentile)',
            'NOF.TP.p95'           :'Total Phosphorus (95th Percentile)',
            'NOF.TP.Med'           :'Total Phosphorus (Median)',
            'NOF.pH.Med'           :'pH (Median)',
            },
        #
        #
        #
        'attribute_units'          : {
            'NOF.ASPM'             :'',
            'NOF.BIOVOL.p80'       :'mg chl-a /m3',
            'NOF.CLAR.Med'         :'m',
            'NOF.Chl_a.p92'        :'mg chl-a /m2',
            'NOF.Chl_a.p83'        :'mg chl-a /m2',
            'NOF.Chl_a'            :'mg chl-a /m2',
            'NOF.Chl_a.Med'        :'mg chl-a /m2',
            'NOF.Chl_a.AMax'       :'mg chl-a /m2',
            'NOF.DRP.Combined'     :'mg/L',
            'NOF.DRP.Med'          :'mg/L',
            'NOF.DRP.p95'          :'mg/L',
            'NOF.ECOLI.Combined'   :'',
            'NOF.ECOLI.G260'       :'% exceedances over 260/100 mL',
            'NOF.ECOLI.G540'       :'% exceedances over 540/100 mL',
            'NOF.ECOLI.Med'        :'E. coli/100 mL',
            'NOF.ECOLI.p95'        :'E. coli/100 mL',
            'NOF.ECOLI_PC.p95'     :'E. coli/100 mL',
            'NOF.MCI'              :'',
            'NOF.NH4N.Combined'    :'',
            'NOF.NH4N.Max'         :'mg NH4-N/L',
            'NOF.NH4N.p95'         :'mg NH4-N/L',
            'NOF.NH4N.Med'         :'mg NH4-N/L',
            'NOF.NO3.Combined'     :'',
            'NOF.NO3.Med'          :'mg NO3-N/L',
            'NOF.NO3.p95'          :'mg NO3-N/L',
            'NOF.QMCI'             :'',
            'NOFc1'                :'m',
            'NOFc2'                :'m',
            'NOFc3'                :'m',
            'NOFc4'                :'m',
            'NOF.SIN.Med'          :'g/m3',
            'NOF.SIN.p95'          :'g/m3',
            'NOF.TN.Combined'      :'g/m3',
            'NOF.TN.MedSS'         :'g/m3',
            'NOF.TN.MedPoly'       :'g/m3',
            'NOF.TN.Med'           :'g/m3',
            'NOF.TN.p95'           :'g/m3',
            'NOF.TP.p95'           :'g/m3',
            'NOF.TP.Med'           :'g/m3',
            'NOF.pH.Med'           :'',
            }
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
        
        #create site list
        all_sites = list(data['site name'].unique())
        with open(f'{file_j}_sites.json', 'w') as fp:
            json.dump(all_sites, fp)
        
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




