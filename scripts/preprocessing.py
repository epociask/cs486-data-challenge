import pandas as pd 
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from math import sin
from geopy.geocoders import Nominatim
import json 

geolocator = Nominatim(user_agent="DelayPredictor")
le = LabelEncoder()
      
##encode_cats --> Encode categorical columns 
#Encodes string categorical columns to numeric labels in each column using LabelEncoder 
def encode_cats(df: pd.DataFrame)->pd.DataFrame:
    global le 
    df["ORIGIN"] = le.fit_transform(df["ORIGIN"])
    df["DEST"] = le.fit_transform(df["DEST"])
    df['UNIQUE_CARRIER'] = le.fit_transform(df['UNIQUE_CARRIER'])
    return df

##osc_transform --> Oscilation tranformation for range bounded columns
#Transforms MONTH && DAY_OF_WEEK columsn to range bounded values between -1 to 1 instead of 
# range(1,7) && range(1,12)
def osc_transform(df: pd.DataFrame) -> pd.DataFrame:
    df['MONTH'] = [sin(e) for e in df['MONTH']]
    df['DAY_OF_WEEK'] = [sin(e) for e in df['DAY_OF_WEEK']]
    return df


#is_busy_time --> outputs 1 if 
#Conditional dates found from https://getawaytips.azcentral.com/busiest-time-air-travel-3409.html
def is_busy_time(val, busy_days) -> int:
    if val in busy_days:
        return 0 

    return 1 

#Constructs and adds BUSY_TIME binary column to dataframe 
def add_busy_feature(df, cut_off) -> pd.DataFrame:
    new_list: list = []

    for key,val in df["FL_DATE"].value_counts().items():
        if val >= cut_off:
            new_list.append(key)
    df["BUSY_TIME"] = [is_busy_time(e, new_list) for e in df["FL_DATE"]]
    return df 

#Drops unecessary columns from dataframe 
def drop_values(df):
    df = df.drop(columns=["ORIGIN_CITY_NAME", "DEST_CITY_NAME"])
    df = df.drop(columns=['Unnamed: 13'])
    df = df.drop(columns=['FL_NUM'])
    return df



def get_coordinates(city_list: list) -> list:
    return [str(geolocator.geocode(e)[0:2]) for e in city_list]

def get_delayed_not_delayed_counts(cmpr_list: list, delayed_list: list) -> tuple:
    delayed, not_delayed = {}, {}
    for val in zip(cmpr_list, delayed_list):
        if val[1] == 1.0:
            if val[0] in delayed:
                delayed[val[0]] = delayed[val[0]] + 1
            else:
                delayed[val[0]] = 1

        else:
             if val[0] in not_delayed:
                not_delayed[val[0]] = not_delayed[val[0]] + 1
             else:
                not_delayed[val[0]] = 1

    return delayed, not_delayed
