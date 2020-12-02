import pandas as pd 
from sklearn.preprocessing import LabelEncoder
from math import sin

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
def is_busy_column(date: str, month: int, day_of_week: int) -> int:
    if month in [6,7,8] and day_of_week == 5:
        return 1
    if "2016-11-22" in date or "11-23" in date or "2017-11-24" in date: ## Thanksgiving && Thanksgiving eve
        return 1
    if "12-24" in date or "12-25" in date or "12-26" in date or "12-27" in date: ## End of christas
        return 1
    if "12-28" in date or "12-29" in date or "12-30" in date or "12-31" in date or "01-01" in date: ## To New Year's day
        return 1
    return 0

#Constructs and adds BUSY_TIME binary column to dataframe 
def add_busy_feature(df: pd.DataFrame) -> pd.DataFrame:
    df["BUSY_TIME"] = [isBusyTime(e) for e in df["FL_DATE"]]
    return df 

#Drops unecessary columns from dataframe 
def drop_values(df):
    df = df.drop(columns=["ORIGIN_CITY_NAME", "DEST_CITY_NAME"])
    df = df.drop(columns=['Unnamed: 13'])
    df = df.drop(columns=['FL_NUM'])
    return df


