import requests
import pandas as pd
import json
import geopandas as gpd
import shapely
import datetime
import scipy.stats as stats

class TrafficBuffer:
    def __init__(self, traffic_data_T):
        self.traffic_data_T = traffic_data_T
        
    def buffering(self):
        buffer_zone = 10
        buffer_ = self.traffic_data_T.geometry.buffer(buffer_zone)
        buffer_T = gpd.GeoDataFrame(geometry = buffer_, crs = 3857)
        buffer_T["implemented_YYYYMM"] = self.traffic_data_T["implemented_YYYYMM"]
        return buffer_T
    
class Intersect:
    def __init__(self, buffer_T, accident):
        self.traffic = buffer_T
        self.accident = accident
    
    def buffer_join(self):
        accidents_within_buffer = gpd.sjoin(self.accident, self.traffic, how = "inner", predicate = "intersects")
        return accidents_within_buffer

def reference_date_1before (row):
    ref_date = str(int(row["implemented_YYYYMM"]) - 100)
    return datetime.datetime(int(ref_date[:4]), int(ref_date[4:6]), 1).strftime('%Y-%m')

def reference_date_1after (row):
    ref_date = str(int(row["implemented_YYYYMM"]) + 100)
    return datetime.datetime(int(ref_date[:4]), int(ref_date[4:6]), 1).strftime('%Y-%m')

def get_accident_date (row):
    accident_date = str(row['AccidentYear']) + str(row['AccidentMonth'])
    if len(accident_date) < 6:
        accident_date = accident_date[:4] + '0' + accident_date[4:]
    return datetime.datetime(int(accident_date[:4]), int(accident_date[4:6]), 1).strftime('%Y-%m')

def format_implementdate (row):
    implemented_date = datetime.datetime(int(row['implemented_YYYYMM'][:4]),
                                         int(row['implemented_YYYYMM'][4:6]), 1).strftime('%Y-%m')
    return implemented_date

class FormatAccident:
    def __init__(self, accidents_within_buffer):
        self.accidents_within_buffer = accidents_within_buffer

    def implement_date(self):
        accident = self.accidents_within_buffer
        accident["ref_date"] = accident.apply(reference_date_1before, axis=1)
        accident["accident_date"] = accident.apply(get_accident_date, axis=1)
        accident["implemented_date"] = accident.apply(format_implementdate, axis=1)
        accident["ref_date_after"] = accident.apply(reference_date_1after, axis=1)
        return accident

    def calculate_before(self):
        accidents_beforeimply = self.accidents_within_buffer[
            (self.accidents_within_buffer['accident_date'] >= self.accidents_within_buffer['ref_date']) &
            (self.accidents_within_buffer['accident_date'] <= self.accidents_within_buffer['implemented_date'])]
        return accidents_beforeimply

    def calculate_after(self):
        accidents_afterimply = self.accidents_within_buffer[
            (self.accidents_within_buffer['accident_date'] >= self.accidents_within_buffer['implemented_date']) &
            (self.accidents_within_buffer['accident_date'] <= self.accidents_within_buffer['ref_date_after'])]
        return accidents_afterimply

