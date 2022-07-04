import numpy as np
import pandas as pd
from datetime import datetime

dateparse = lambda x: datetime.strptime(x, '%d-%m-%Y')

df1 = pd.read_csv("data/data_set_1.csv", parse_dates=[1], date_parser=dateparse, encoding='utf-8')
df2 = pd.read_csv("data/data_set_2.csv", parse_dates=[1], date_parser=dateparse, encoding='utf-8')

df = pd.concat([df1,df2]).reset_index(drop=True)
product_list = df['product'].unique()
print("No of Parts: ",len(product_list))

df_preprocessed = pd.DataFrame(columns=["Product","quantity"])
my_dict = {}
window_size = 6

inputs = ["x"+str(x) for x in np.arange(1,window_size+1)]
col = np.concatenate([['Product'],inputs,['y']])
df_preprocessed = pd.DataFrame(columns=col)
my_dict = {}

count = 0
month_threshold = 120
i=0

while(count<10): 
    df_prod = df.loc[df['product'] == product_list[i]]
    df_prod_month = df_prod.groupby(pd.Grouper(key='date', freq='M')).sum().reset_index()
    if len(df_prod_month) >= month_threshold:
        df1 = df_prod_month
        values = df1["quantity"].values
        local = pd.DataFrame(columns=["Product"])
        for j in range(window_size):
            local[inputs[j]] = values[j:len(values)-window_size+j-1]
        
        local['y'] = values[window_size:len(values)-window_size+window_size-1]
        local['Product'] = i
        my_dict[product_list[i]] = i
        
        df_preprocessed = pd.concat([df_preprocessed, local], axis = 0, sort = False,ignore_index=True)
        count+=1
    i+=1

df_preprocessed.to_csv("data/preprocessed.csv")
print(df_preprocessed)