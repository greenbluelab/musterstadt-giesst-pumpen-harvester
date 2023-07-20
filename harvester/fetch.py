import json

from utils import create_folder, get_raw_data, get_overpass_gdf, transform_dataframe, write_df_to_json


def fetch_osm_pumps(path, outpath, query_string):

    create_folder(path)

    # specify query
    # Default to Berlin pumps when query string isn't provided
    if not query_string or not query_string.strip():
        query_string = '[out:json];(area[name=Dresden];)->.searchArea;(node[amenity=fountain](area.searchArea););out;>;out;'
    # get data and write to json
    raw_data = get_raw_data(query_string)
    json = raw_data.json()
    
    # transform and write to dataframe
    gdf = get_overpass_gdf(json)
    cleaned_gdf = transform_dataframe(gdf)
    write_df_to_json(cleaned_gdf,outpath)
