
import numpy as np
import pandas as pd



def preprocess(df,df_region):
    #filtering summer data
    df =df[df['Season']=='Summer']
    #merging file
    df = df.merge(df_region,on='NOC',how='left')
    #one hot encode
    medal_df = pd.get_dummies(df['Medal'])
    df = pd.concat([df,medal_df],axis=1)
    df.drop_duplicates(inplace=True)
    return df 