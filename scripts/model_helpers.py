import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def split_train_predict(df: pd.DataFrame, rf) -> float:
    X = df.drop(columns=['ARR_DEL15'])
    Y = df['ARR_DEL15']
    train_x, test_x, train_y, test_y = train_test_split(X, Y)
    rf.fit(train_x, train_y)
    return rf.predict(test_x), test_y 

def get_standard_df(df: pd.DataFrame):
    return StandardScaler().fit_transform(df)

