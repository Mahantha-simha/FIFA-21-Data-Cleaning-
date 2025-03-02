import pandas as pd
import numpy as np
import re

# pd.set_option('display.max_columns', None) 


# Load the data
df=pd.read_csv("fifa21 raw data v2.csv")

# print(df.sample(5))
# print(df.shape) # (18278, 104) the data has 18278 rows and 104 columns
# print(df.columns)
# print(df.dtypes)
# print(df.info())# check for missing values
# print(df.describe()) # check for missing values


#make a copy of the data
data=df.copy()  
# print(data.sample(5))

# column no 10
data['Club']= data['Club'].str.strip() # remove white spaces from the club column
print(data['Club'].unique())    # check for unique values in the club column


# column no 11

data['Contract']
# print(data['Contract'].dtype) # check for unique values in the contract column

# search for the word 'On Loan' and 'free' in the contract column
# for i , row in data.iterrows():
#     if 'On Loan' in row['Contract'] or 'Free' in row['Contract']:
#         print(row['Contract'])

# here we are creating a new column start_date and end_date and contract_length from the contract column

def extract_contract_length(Contract):
    if Contract =='Free' or Contract=='On Loan':
        Start_date=np.nan
        End_date=np.nan
        Contract_length=1
    else:
        try:
            Start_date, End_date = Contract.split(' ~ ')
        except ValueError:
            Start_date = End_date = np.nan
            Contract_length = np.nan
            return Start_date, End_date, Contract_length
        
        Startyear=int(Start_date[:4])
        Endyear=int(End_date[:4])
        Contract_length=Endyear-Startyear
        
        return Start_date, End_date, Contract_length
    
data[['Start_date', 'End_date', 'Contract_length']] = data['Contract'].apply(lambda x: pd.Series(extract_contract_length(x)))

#now we done the start date, end date and contract length columns we have some data left in the contract column
#like on loan and free we need to remove that data and and put in different column called contract status

def extract_contract_status(Contract):
    if 'Free' in Contract:
        Contract_status = 'Free'
    elif 'On Loan' in Contract:#we should this in Contract column here we are checking for the word 'On Loan' in the contract column
        Contract_status = 'On Loan'
    else:
        Contract_status = 'Contract'

    return Contract_status    

data['Contract_status'] = data['Contract'].apply(lambda x:pd.Series(extract_contract_status(x)))

# Reorder the columns to place 'Start_date', 'End_date', and 'Contract_length' after the 10th position
cols = list(data.columns)
cols.insert(11, cols.pop(cols.index('Start_date')))
cols.insert(12, cols.pop(cols.index('End_date')))
cols.insert(13, cols.pop(cols.index('Contract_length')))
cols.insert(14, cols.pop(cols.index('Contract_status')))
data = data[cols]

# Display the first few rows of the modified dataframe

# data.to_csv(' modefied fifa21_cleaned_data.csv',index=False)# save the data to a csv file

# row number 13 height column
# print(data['Height'].dtype) # check for unique values in the height column
# print(data['Height'].unique()) # check for unique values in the height column

def height_to_cm(height):
    if 'cm' in height:
        Height = height#here we can use height.replace('cm','') to remove the cm from the height column and you can convert the height to int
    else:
      match = re.match(r"(\d+)'(\d+)\"", height)
      if match:
            feet = int(match.group(1))
            inches = int(match.group(2))
            Hei=round((feet * 30.48) + (inches * 2.54)) # 1 foot = 30.48 cm and 1 inch = 2.54 cm
            Height = str(Hei) + 'cm'
    return Height.replace('cm','')

data['Height'] = data['Height'].apply(height_to_cm)
data=data.rename(columns={'Height':'Height_cm'})
# print(data['Height'].unique())

# row number 14 weight column

# print(data['Weight'].dtype) # check for unique values in the weight column
# print(data['Weight'].unique()) # check for unique values in the weight column

def weight_to_kg(weight):

    if 'kg' in weight:
        Weight = weight
    else:
        Weight = str(round(int(weight.replace('lbs','')) * 0.453592)) + 'kg' # 1 pound = 0.453592 kg
    return Weight.replace('kg','')

data['Weight'] = data['Weight'].apply(weight_to_kg).rename('Weight_kg', inplace=True)
data=data.rename(columns={'Weight':'Weight_kg'})

# number 19 Loan Date End column

def end_data(date):
    if 'On Loan' in date:
        Loan_date_end = "On Loan"
    elif 'Free' in date:
        Loan_date_end = "Free"
    else:
        Loan_date_end =date.split(' ~ ')[-1]   
    return Loan_date_end        

data['Loan Date End'] = data['Contract'].apply(end_data)
# print(data['Loan Date End'].unique())

# a=data[data['Loan Date End']=='On Loan']
# print(a[['Start_date','Loan Date End','Contract']])#IMPORTANT




# column number 66 W/F
#we need to remove the * from the W/F column

data['W/F'] = data['W/F'].str.replace('★','')
# print(data['W/F'].unique()) # check for unique values in the W/F column

data['SM'] = data['SM'].str.replace('★','')
# print(data['SM'].unique()) # check for unique values in the SM column

data['IR'] = data['IR'].str.replace('★','')
# print(data['IR'].unique()) # check for unique values in


#column 77 Hits column

def hits(hits):

    if 'K' in hits: 
        return str(int(float(hits.replace('K', '')) * 1000))
    elif '.' in hits: 
        return str(int(float(hits) * 1000))
    else:  
        return hits

data['Hits'] = data['Hits'].astype(str).apply(hits)
# print(data['Hits'].unique())

data.to_csv('final fifa21_cleaned_data.csv',index=False)# save the data to a csv file