from pathlib import Path
import json
import os
import pytest

import pandas as pd
import geopandas as gpd
from requests import Response
from shapely.geometry import Point

from utils import get_raw_data, create_folder, write_df_to_json, get_overpass_gdf, transform_dataframe
from fetch import fetch_osm_pumps


@pytest.fixture(scope="module")
def test_fetch_uses_provided_query_string(mocker):
    mock_get_raw_data = mocker.patch('utils.get_raw_data')
    mocker.patch('utils.create_folder')
    mocker.patch('utils.get_overpass_gdf')
    mocker.patch('utils.transform_dataframe')
    mocker.patch('utils.write_df_to_json')

    outpath = "out/pumps.geojson"
    fetch_osm_pumps(Path(outpath), outpath, 'test query string')

    mock_get_raw_data.assert_called_once_with('test query string')


@pytest.fixture(scope="module")
def test_fetch_uses_berlin_as_default_query(mocker):
    mock_get_raw_data = mocker.patch('utils.get_raw_data')
    mocker.patch('utils.create_folder')
    mocker.patch('utils.get_overpass_gdf')
    mocker.patch('utils.transform_dataframe')
    mocker.patch('utils.write_df_to_json')

    outpath = "out/pumps.geojson"
    fetch_osm_pumps(Path(outpath), outpath, '')

    mock_get_raw_data.assert_called_once_with('[out:json];(area["ISO3166-2"="DE-BE"]["admin_level"="4"];)->.searchArea;(node["man_made"="water_well"]["network"="Berliner Straßenbrunnen"](area.searchArea););out;>;out;')


def test_get_raw_data(query_fixture):
    response = get_raw_data(query_fixture)
    assert isinstance(response, Response)
    assert response.ok


def test_create_folder(path_fixture):
    create_folder(path_fixture)
    assert path_fixture.parent.exists()
    path_fixture.parent.rmdir()
    assert not path_fixture.parent.exists()


def test_get_overpass_gdf(response_fixture):
    result = get_overpass_gdf(response_fixture)
    assert result["type"] is not None
    assert result["id"] is not None
    assert result["lat"] is not None
    assert result["lon"] is not None
    assert result["tags"] is not None
    assert result["geometry"] is not None
    assert isinstance(result, pd.DataFrame) == True
    assert isinstance(result["geometry"][0], Point) == True


def test_transform_dataframe(response_fixture):
    gdf = get_overpass_gdf(response_fixture)
    cleaned_gdf = transform_dataframe(gdf)
    assert "drinking_water" in cleaned_gdf.columns
    assert "geometry" in cleaned_gdf.columns
    assert "has_no_lat_lon" not in cleaned_gdf.values


def test_write_df_to_json(path_fixture, dataframe_fixture):
    json_path = path_fixture
    min_json_path = Path(str(path_fixture)+".min.json")
    create_folder(json_path)
    write_df_to_json(dataframe_fixture, str(json_path))
    assert json_path.is_file
    assert min_json_path.is_file
    assert dataframe_fixture.equals(gpd.read_file(str(json_path)))
    json_path.unlink()
    min_json_path.unlink()
    json_path.parent.rmdir()
    assert not json_path.parent.exists()


def test_write_df_to_json_handles_KeyError(path_fixture, dataframe_fixture):
    json_path = path_fixture
    min_json_path = Path(str(path_fixture)+".min.json")
    create_folder(json_path)
    del os.environ["GITHUB_OUTPUT"]
    write_df_to_json(dataframe_fixture, str(json_path))
    json_path.unlink()
    min_json_path.unlink()
    json_path.parent.rmdir()
