import pandas as pd

data=pd.read_csv('cricket.csv')
print(data.head())



# pd.set_option('display.max_columns', None) 

# column no 10

# a['Club']=a['Club'].str.strip() # remove white spaces from the club column
# print(a['Club'].unique())    # check for unique values in the club column

# a['IR']=a['IR'].str.replace("★",'') # remove white spaces from the club column
# print(a['IR'].unique())    # check for unique values in the club column

# a.to_csv(' clean fifa21 raw data v3.csv', index=False) # save the cleaned data to a new csv file

  # check for unique values in the contract column