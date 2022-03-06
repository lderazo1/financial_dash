import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import geopandas as gpd
import pyproj

#Initial connection Google Sheets

######   V1.0 Only get Cantones

CREDS_JSON = 'credentials.json'
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

def get_selected_dataframe(sheet_name, key):
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_JSON, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(key) # Open the spreadhseet
    base_sheet = sheet.worksheet(sheet_name)
    df = pd.DataFrame(base_sheet.get_all_records())
    return df

def get_geojson():
    geo = gpd.read_file('ec.geojson', driver="GeoJSON")
    geo.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
    return geo