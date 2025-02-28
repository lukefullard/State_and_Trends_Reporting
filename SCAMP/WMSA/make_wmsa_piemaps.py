import pandas as pd
import numpy as np
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import io	
import base64


settings = {
    'data_file'         :  r'../data/20241017_BaselineforPiegraphs.xlsx',
    'scenario_file'     :  r'../data/20241017_ScenariosforPiegraphs.xlsx',
    'TN_tab_name'       :  'TN',
    'TP_tab_name'       :  'TP',
    'scenario_1_tab'    :  {
                            'TN'  :  'Scenario1_TN',
                            'TP'  :  'Scenario1_TP',
                            },
    'scenario_2_tab'    :  {
                            'TN'  :  'Scenario2_TN',
                            'TP'  :  'Scenario2_TP',
                            },
    'wmsz_column'       :  'WMSZ',
    'use_colours'       :  {
                            'Sheep & Beef'         :  '#5a9bd7',
                            'Observable Erosion P' :  '#9cc3e9',
                            'Dairy'                :  '#c55c11',  
                            'Point Sources'        :  '#ec0507',
                            'Native'               :  '#00af50',
                            'Hort.'                :  '#7f7f7f',
                            'Lifestyle'            :  '#e809d5',
                            'Urban'                :  '#012160',
                            'Public'               :  '#e4f000',
                            'Arable'               :  '#d7cd1a',
                            'Forestry'             :  '#b2e7ca',
                            'Other'                :  '#c00002',
                                    },
    #
    'zoom_levek_map'       :  {'Rangitīkei-Turakina'    :  9,
                               'Waiopehu'               : 12,
                               'Whanganui'              : 9,
                               'Manawatū'               : 10,
                               'Whangaehu'              : 10,
                               'Puketoi ki Tai'         : 11,
                               'Kai Iwi'                : 12,
                               },
    'fmu_shapefile'    :  {'file'    :  r'//gisdata/GIS/Department/Catchment Information/Projects/POLICY/2020/48584_mapping_for_report/data/FMU_20210122.shp',
                             'name'    :  'Name',
                             'epsg'    :  2193,
                             }, 
    'wmsz_shapefile'   :  {'file'      :  r'//gisdata/GIS/Department/Policy/OnePlan/One_Plan/Operative_One_Plan/Shapefiles/Surface_Water/Water_Management_Subzones.shp',
                             'name'    :  'Zone_Code',
                             'epsg'    :  27200,
                             }, 
    
    #
    'tile_layer'        :  'cartodbpositron',
    'fmu_fill_color'    :    "#5d8785",
    'linecolor'         :    "black",
    'lineweight'        :    0.1,
    'fmu_lineweight'    :    0.25,
    'simplify_tolerance':  0.0005,
    'fmu_highlight_color': '#191919'
    
    }

wmsz_nice_names = {
    'West_1' : 'Northern Coastal',
'West_2' : 'Kai Iwi',
'West_3' : 'Mowhanau',
'Mana_10a' : 'Middle Manawatu',
'Mana_10b' : 'Upper Pohangina',
'Mana_10c' : 'Middle Pohangina',
'Mana_10d' : 'Lower Pohangina',
'Mana_10e' : 'Aokautere',
'Mana_11a' : 'Lower Manawatu',
'Mana_11b' : 'Turitea',
'Mana_11c' : 'Kahuterawa',
'Mana_11d' : 'Upper Mangaone Stream', 
'Mana_11e' : 'Lower Mangaone Stream',
'Mana_11f' : 'Main Drain',
'Mana_12a' : 'Upper Oroua',
'Mana_12b' : 'Middle Oroua',
'Mana_12c' : 'Lower Oroua',
'Mana_12d' : 'Kiwitea',
'Mana_12e' : 'Makino',
'Mana_13a' : 'Coastal Manawatu',
'Mana_13b' : 'Upper Tokomaru',
'Mana_13c' : 'Lower Tokomaru',
'Mana_13d' : 'Mangaore',
'Mana_13e' : 'Koputaroa',
'Mana_13f' : 'Foxton Loop',
'Mana_1a' : 'Upper Manawatu',
'Mana_1b' : 'Mangatewainui',
'Mana_1c' : 'Mangatoro',
'Mana_2a' : 'Weber - Tamaki',
'Mana_2b' : 'Mangatera',
'Mana_3' : 'Upper Tamaki',
'Mana_4' : 'Upper Kumeti',
'Mana_5a' : 'Tamaki - Hopelands', 
'Mana_5b' : 'Lower Tamaki',
'Mana_5c' : 'Lower Kumeti',
'Mana_5d' : 'Oruakeretaki',
'Mana_5e' : 'Raparapawai',
'Mana_6' : 'Hopelands - Tiraumea',
'Mana_7a' : 'Upper Tiraumea',
'Mana_7b' : 'Lower Tiraumea',
'Mana_7c' : 'Mangaone River',
'Mana_7d' : 'Makuri',
'Mana_7e' : 'Mangaramarama',
'Mana_8a' : 'Upper Mangatainoka', 
'Mana_8b' : 'Middle Mangatainoka',
'Mana_8c' : 'Lower Mangatainoka',
'Mana_8d' : 'Makakahi',
'Mana_9a' : 'Upper Gorge',
'Mana_9b' : 'Mangapapa',
'Mana_9c' : 'Mangaatua',
'Mana_9d' : 'Upper Mangahao',
'Mana_9e' : 'Lower Mangahao',
'Akit_1a' : 'Upper Akitio',
'Akit_1b' : 'Lower Akitio',
'Akit_1c' : 'Waihi',
'East_1' : 'East Coast',
'Owha_1' : 'Owahanga',
'Rang_1' : 'Upper Rangitikei',
'Rang_2a' : 'Middle Rangitikei',
'Rang_2b' : 'Pukeokahu - Mangaweka', 
'Rang_2c' : 'Upper Moawhango',
'Rang_2d' : 'Middle Moawhango',
'Rang_2e' : 'Lower Moawhango',
'Rang_2f' : 'Upper Hautapu',
'Rang_2g' : 'Lower Hautapu',
'Rang_3a' : 'Lower Rangitikei',
'Rang_3b' : 'Makohine',
'Rang_4a' : 'Coastal Rangitikei',
'Rang_4b' : 'Tidal Rangitikei',
'Rang_4c' : 'Porewa',
'Rang_4d' : 'Tutaenui',
'Tura_1a' : 'Upper Turakina',
'Tura_1b' : 'Lower Turakina',
'Tura_1c' : 'Ratana',
'West_5' : 'Southern Whanganui Lakes',
'West_6' : 'Northern Manawatu Lakes',
'Hoki_1a' : 'Lake Horowhenua',
'Hoki_1b' : 'Hokio',
'Ohau_1a' : 'Upper Ohau',
'Ohau_1b' : 'Lower Ohau',
'West_7' : 'Waitarere',
'West_8' : 'Lake Papaitonga',
'West_9a' : 'Waikawa',
'West_9b' : 'Manakau',
'Whau_1a' : 'Upper Whangaehu',
'Whau_1b' : 'Waitangi',
'Whau_1c' : 'Tokiahuru',
'Whau_2' : 'Middle Whangaehu',
'Whau_3a' : 'Lower Whangaehu',
'Whau_3b' : 'Upper Makotuku',
'Whau_3c' : 'Lower Makotuku',
'Whau_3d' : 'Upper Mangawhero',
'Whau_3e' : 'Lower Mangawhero',
'Whau_3f' : 'Makara',
'Whau_4' : 'Coastal Whangaehu',
'West_4' : 'Kaitoke Lakes',
'Whai_1' : 'Upper Whanganui',
'Whai_2a' : 'Cherry Grove',
'Whai_2b' : 'Upper Whakapapa',  
'Whai_2c' : 'Lower Whakapapa',
'Whai_2d' : 'Piopiotea',
'Whai_2e' : 'Pungapunga',
'Whai_2f' : 'Upper Ongarue',
'Whai_2g' : 'Lower Ongarue',
'Whai_3' : 'Te Maire',
'Whai_4a' : 'Middle Whanganui',
'Whai_4b' : 'Upper Ohura',
'Whai_4c' : 'Lower Ohura',
'Whai_4d' : 'Retaruke',
'Whai_5a' : 'Pipiriki',
'Whai_5b' : 'Tangarakau',
'Whai_5c' : 'Whangamomona',
'Whai_5d' : 'Upper Manganui o te Ao',
'Whai_5e' : 'Makatote',
'Whai_5f' : 'Waimarino',
'Whai_5g' : 'Middle Manganui o te Ao',
'Whai_5h' : 'Mangaturuturu',
'Whai_5i' : 'Lower Manganui o te Ao',
'Whai_5j' : 'Orautoha',
'Whai_6' : 'Paetawa',
'Whai_7a' : 'Lower Whanganui',
'Whai_7b' : 'Coastal Whanganui',
'Whai_7c' : 'Upokongaro',
'Whai_7d' : 'Matarawa',
}
###############################################################################
###############################################################################
###############################################################################
def make_legend(settings, nutrient_type='TP'):
    import branca
    legend_items = '''
    '''    
    for key_i, value_i in settings.get('use_colours').items():
        if (nutrient_type == 'TN') & (key_i == 'Observable Erosion P'):
            pass
        else:
            legend_items += f'''
    <p><span style="display:inline-block;color:{value_i};font-size:150%;margin-left:20px;">&#9632;</span>&emsp;{key_i}</p>
    '''        

    legend_html = """
    {% macro html(this, kwargs) %}
    <style>
        #legend {
            position: fixed;
            bottom: 75px;
            left: 25px;
            width: 200px;
            height: 480px;
            z-index: 9999;
            font-size: 14px;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 5px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
            cursor: move; /* Change cursor to indicate draggable */
        }
    </style>

    <div id="legend">
        {{ legend_items|safe }}
    </div>

    <script>
        // JavaScript to enable dragging
        const legend = document.getElementById('legend');
        let isDragging = false;
        let offsetX, offsetY;

        legend.addEventListener('mousedown', function(e) {
            isDragging = true;
            offsetX = e.clientX - legend.offsetLeft;
            offsetY = e.clientY - legend.offsetTop;
            legend.style.cursor = 'grabbing'; /* Change cursor to grabbing while dragging */
        });

        document.addEventListener('mousemove', function(e) {
            if (isDragging) {
                legend.style.left = (e.clientX - offsetX) + 'px';
                legend.style.top = (e.clientY - offsetY) + 'px';
            }
        });

        document.addEventListener('mouseup', function() {
            isDragging = false;
            legend.style.cursor = 'move'; /* Reset cursor to move */
        });
    </script>
    {% endmacro %}
    """
    legend_html = legend_html.replace('{{ legend_items|safe }}', legend_items)
    
    legend = branca.element.MacroElement()
    legend._template = branca.element.Template(legend_html)
    return legend

###############################################################################
###############################################################################
###############################################################################
def make_pie_charts(df,settings, nutrient_type = 'TP'):
    fig = plt.figure(figsize=(1, 1))
    fig.patch.set_alpha(0)
    ax = fig.add_subplot(111)
    plots = []
    
    
    land_types   = list(settings.get('use_colours').keys())
    if nutrient_type == 'TN':
        land_types.remove('Observable Erosion P')
    land_colours = [settings.get('use_colours').get(x) for x in land_types]
    for iter_j,row_j in df.iterrows():
        land_use_percentages = []
        for land_type_j in land_types:
            try:land_use_percentages.append(max(0.,row_j[land_type_j]))
            except: 
                land_colours.remove(settings.get('use_colours').get(land_type_j))
                land_types.remove(land_type_j)
        center = (0, 0)
        large_radius = 10.
        small_radius = 0.05
        ax.pie(land_use_percentages,colors=land_colours, radius=large_radius,
               wedgeprops=dict(width=9.99,linewidth= 0.25, edgecolor='k'))
        
        # Create the ring (outer circle)
        outer_ring = Circle(center, large_radius + 0.05, color='black', fill=False, linewidth=1, linestyle='-')
        
        # Create the inner circle (to cut out the center)
        # inner_ring = Circle(center, small_radius, color='white', fill=True)
        # inner_ring_2 = Circle(center, small_radius, color='black', fill=False, linewidth=1, linestyle='-')
        
        # Add rings to the plot
        ax.add_patch(outer_ring)
        # ax.add_patch(inner_ring)
        # ax.add_patch(inner_ring_2)
        
        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')
        buff = io.StringIO()
        plt.savefig(buff, format="SVG")
        buff.seek(0)
        svg = buff.read()
        svg = svg.replace("\n", "")
        plots.append(svg)
        plt.cla()
    plt.clf()
    plt.close()
    return plots
###############################################################################
###############################################################################
###############################################################################
#load geospatial file
fmu_gdf = gpd.read_file(settings.get('fmu_shapefile').get('file'))
fmu_gdf = fmu_gdf.to_crs(4326)


########################################################################
# TN First
data = pd.read_excel(settings.get('data_file'),sheet_name=settings.get('TN_tab_name'))


#load geospatial files and assign subzones to fmus
fmu_gdf = gpd.read_file(settings.get('fmu_shapefile').get('file'))
fmu_gdf = fmu_gdf.to_crs(4326)
wmsz_gdf = gpd.read_file(settings.get('wmsz_shapefile').get('file'))
wmsz_gdf = wmsz_gdf.to_crs(4326)
wmsz_gdf['centroid'] = wmsz_gdf.representative_point()
wmsz_centroids = gpd.GeoDataFrame(wmsz_gdf, geometry='centroid')
# Perform spatial join to assign centroids to FMU
wmsz_fmu_joined = gpd.sjoin(wmsz_centroids, fmu_gdf, how="left", op="within")

#merge the data with the wmsz
merged_data = pd.merge(data, wmsz_fmu_joined[[settings.get('wmsz_shapefile').get('name'), 'centroid',settings.get('fmu_shapefile').get('name')]], left_on=settings.get('wmsz_column'),right_on = settings.get('wmsz_shapefile').get('name'), how='left')


for fmu_j in settings.get('zoom_levek_map').keys():
    sub_data = merged_data.loc[merged_data[settings.get('fmu_shapefile').get('name')]==fmu_j].reset_index(drop=True)
    
    plots = make_pie_charts(sub_data,settings, nutrient_type = 'TN')
    legend = make_legend(settings,nutrient_type = 'TN')
    sub_data['plots'] = plots
    # sub_gdf = gdf.loc[gdf[settings.get('fmu_column')] == fmu_j].reset_index(drop=True)
    sub_gdf = gpd.GeoDataFrame(sub_data, geometry='centroid',crs="EPSG:4326")
    
    
    sub_fmu_gdf = wmsz_fmu_joined.loc[wmsz_fmu_joined[settings.get('fmu_shapefile').get('name')]==fmu_j].reset_index(drop=True)
    sub_fmu_gdf = gpd.GeoDataFrame(sub_fmu_gdf, geometry='geometry')
    sub_fmu_gdf["geometry"] = sub_fmu_gdf["geometry"].simplify(tolerance=settings.get('simplify_tolerance'),
                                                                   preserve_topology=True)
    
    m = folium.Map(location=(np.mean([sub_gdf.geometry.y.max(),sub_gdf.geometry.y.min()]),np.mean([sub_gdf.geometry.x.max(),sub_gdf.geometry.x.min()])), 
                   zoom_start=settings.get('zoom_levek_map').get(fmu_j),
                   tiles = None)
    folium.raster_layers.TileLayer(tiles=settings.get('tile_layer'), show=True,control=False).add_to(m)
    geojson  = folium.GeoJson(sub_fmu_gdf['geometry'], style_function=lambda x: {"fillColor": settings.get('fmu_fill_color'),
                                                      "color": settings.get('linecolor'), 
                                                      "weight": settings.get('fmu_lineweight'),
                                                      },
                                                  highlight_function= lambda feat: {'fillColor': settings.get('fmu_highlight_color')},
                                                      control = False).add_to(m)
    for iter_k, row_k in sub_gdf.iterrows():
        hover_text = f'<b>{wmsz_nice_names.get(row_k[settings.get("wmsz_column")])}</b><br><b>{row_k[settings.get("wmsz_column")]}</b><br><br>'
        for col_k in list(settings.get('use_colours').keys()):
            try:hover_text += f"<b>{col_k}:</b> {100*row_k[col_k]:.2f}% <br>"
            except: print(f'no column named {col_k} found')
        
        marker = folium.Marker(location = (row_k['centroid'].y, row_k['centroid'].x))
        
        ####
        png_link = f'./TN/{row_k[settings.get("wmsz_column")]}_TN.png'
        if png_link:  # Check if the PNG link exists
            # popup_content = folium.Popup(f'<img src="{png_link}" width="1200">', max_width=1200)
            popup_content = folium.Popup(f'<img src="{png_link}" style="max-width: 75vw;">')
            marker.add_child(popup_content)
        #####
        
        icon = folium.DivIcon(html=row_k['plots'],icon_anchor=(50, 50))
        marker.add_child(icon)
        # Add tooltip with hover text
        tooltip_text = hover_text
        tooltip = folium.Tooltip(tooltip_text)
        marker.add_child(tooltip)
        m.add_child(marker)
    m.get_root().add_child(legend)
    
    # m.save(f'TN_{fmu_j.replace("/","_")}.html')
    map_bytes = io.BytesIO()
    m.save(map_bytes, close_file=False)
    map_bytes.seek(0)  # Go to the beginning of the BytesIO object
    map_content = map_bytes.getvalue()
    encoded_content = base64.b64encode(map_content).decode('utf-8')
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <script>
            document.write(atob("{encoded_content}"));
        </script>
    </body>
    </html>
    """

    with open(f'TN_{fmu_j.replace("/","_").replace("ī","i").replace("ū","u").replace(" ","_").replace("-","_")}.html', 'w') as encoded_file:
        encoded_file.write(html_template)
 
    

########################################################################
# TP Next
data = pd.read_excel(settings.get('data_file'),sheet_name=settings.get('TP_tab_name'))


#load geospatial files and assign subzones to fmus
fmu_gdf = gpd.read_file(settings.get('fmu_shapefile').get('file'))
fmu_gdf = fmu_gdf.to_crs(4326)
wmsz_gdf = gpd.read_file(settings.get('wmsz_shapefile').get('file'))
wmsz_gdf = wmsz_gdf.to_crs(4326)
wmsz_gdf['centroid'] = wmsz_gdf.representative_point()
wmsz_centroids = gpd.GeoDataFrame(wmsz_gdf, geometry='centroid')
# Perform spatial join to assign centroids to FMU
wmsz_fmu_joined = gpd.sjoin(wmsz_centroids, fmu_gdf, how="left", op="within")

#merge the data with the wmsz
merged_data = pd.merge(data, wmsz_fmu_joined[[settings.get('wmsz_shapefile').get('name'), 'centroid',settings.get('fmu_shapefile').get('name')]], left_on=settings.get('wmsz_column'),right_on = settings.get('wmsz_shapefile').get('name'), how='left')


for fmu_j in settings.get('zoom_levek_map').keys():
    sub_data = merged_data.loc[merged_data[settings.get('fmu_shapefile').get('name')]==fmu_j].reset_index(drop=True)
    
    plots = make_pie_charts(sub_data,settings, nutrient_type = 'TP')
    legend = make_legend(settings,nutrient_type = 'TP')
    sub_data['plots'] = plots
    # sub_gdf = gdf.loc[gdf[settings.get('fmu_column')] == fmu_j].reset_index(drop=True)
    sub_gdf = gpd.GeoDataFrame(sub_data, geometry='centroid',crs="EPSG:4326")
    
    
    sub_fmu_gdf = wmsz_fmu_joined.loc[wmsz_fmu_joined[settings.get('fmu_shapefile').get('name')]==fmu_j].reset_index(drop=True)
    sub_fmu_gdf = gpd.GeoDataFrame(sub_fmu_gdf, geometry='geometry')
    sub_fmu_gdf["geometry"] = sub_fmu_gdf["geometry"].simplify(tolerance=settings.get('simplify_tolerance'),
                                                                   preserve_topology=True)
    
    m = folium.Map(location=(np.mean([sub_gdf.geometry.y.max(),sub_gdf.geometry.y.min()]),np.mean([sub_gdf.geometry.x.max(),sub_gdf.geometry.x.min()])), 
                   zoom_start=settings.get('zoom_levek_map').get(fmu_j),
                   tiles = None)
    folium.raster_layers.TileLayer(tiles=settings.get('tile_layer'), show=True,control=False).add_to(m)
    geojson  = folium.GeoJson(sub_fmu_gdf['geometry'], style_function=lambda x: {"fillColor": settings.get('fmu_fill_color'),
                                                      "color": settings.get('linecolor'), 
                                                      "weight": settings.get('fmu_lineweight'),
                                                      },
                                                  highlight_function= lambda feat: {'fillColor': settings.get('fmu_highlight_color')},
                                                      control = False).add_to(m)
    for iter_k, row_k in sub_gdf.iterrows():
        hover_text = f'<b>{wmsz_nice_names.get(row_k[settings.get("wmsz_column")])}</b><br><b>{row_k[settings.get("wmsz_column")]}</b><br><br>'
        for col_k in list(settings.get('use_colours').keys()):
            try:hover_text += f"<b>{col_k}:</b> {100*row_k[col_k]:.2f}% <br>"
            except: print(f'no column named {col_k} found')
        
        marker = folium.Marker(location = (row_k['centroid'].y, row_k['centroid'].x))
        ####
        png_link = f'./TP/{row_k[settings.get("wmsz_column")]}_TP.png'
        if png_link:  # Check if the PNG link exists
            # popup_content = folium.Popup(f'<img src="{png_link}" width="1200">', max_width=1200)
            popup_content = folium.Popup(f'<img src="{png_link}" style="max-width: 75vw;">')
            marker.add_child(popup_content)
        #####
        
        icon = folium.DivIcon(html=row_k['plots'],icon_anchor=(50, 50))
        marker.add_child(icon)
        # Add tooltip with hover text
        tooltip_text = hover_text
        tooltip = folium.Tooltip(tooltip_text)
        marker.add_child(tooltip)
        m.add_child(marker)
    m.get_root().add_child(legend)
    

    map_bytes = io.BytesIO()
    m.save(map_bytes, close_file=False)
    map_bytes.seek(0)  # Go to the beginning of the BytesIO object
    map_content = map_bytes.getvalue()
    encoded_content = base64.b64encode(map_content).decode('utf-8')
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <script>
            document.write(atob("{encoded_content}"));
        </script>
    </body>
    </html>
    """

    with open(f'TP_{fmu_j.replace("/","_").replace("ī","i").replace("ū","u").replace(" ","_").replace("-","_")}.html', 'w') as encoded_file:
        encoded_file.write(html_template)