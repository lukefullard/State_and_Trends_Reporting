# -*- coding: utf-8 -*-
"""
saves shapefiles as json WKT strings
"""
import json
import geopandas as gpd

def load_settings():
    settings = {
        'shapefiles'             : {'District'                   :{'location'     : r'FILE LOCATION',
                                                                    'column_name'  : 'TA2014_NAM'
                                                                    },
                                    'Freshwater Management Unit' :{'location'     : r'FILE LOCATION',
                                                                    'column_name' : 'Name'
                                                                    },
                                    'Water management Zone'      :{'location'     : r'FILE LOCATION',
                                                                    'column_name' : 'ManageZone'
                                                                    },
                                    'Water management Subzone'   :{'location'     : r'FILE LOCATION',
                                                                    'column_name' : 'Zone_Code'
                                                                    },
                                    },
        'simplify_geometry'    : True,
        'simplification_value' : 0.001,
        }
    return settings



def main():
    settings = load_settings()
    for region_type_i in settings.get('shapefiles').keys():
        gdf = gpd.read_file(settings.get('shapefiles').get(region_type_i).get('location'))
        temp_data = {}
        for name_i,geometry_i in zip(gdf[settings.get('shapefiles').get(region_type_i).get('column_name')],gdf['geometry']):
            if settings.get('simplify_geometry'):
                temp_data.update({name_i:geometry_i.simplify(tolerance = settings.get('simplification_value')).wkt})
            else:
                temp_data.update({name_i:geometry_i.wkt})
            
    
        with open(f'{region_type_i}_spatial_data.json', 'w') as fp:
            json.dump(temp_data, fp)    
        


if __name__ == '__main__':
    main()
