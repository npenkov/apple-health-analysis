import xml.etree.ElementTree as ET
import pandas as pd
import datetime as dt 

# create element tree object 
print('Loading data...')
tree = ET.parse('apple_health_export/export.xml')

# extract the attributes of health record
print('Extracting data...')
root = tree.getroot()
record_list = [x.attrib for x in root.iter('Record')]

print('Loading in DataFrame...')
# create a DataFrame from record_list
record_data = pd.DataFrame(record_list)

print('Cleaning data...')
# remove 'sourceName', 'sourceVersion',
# 'device', 'creationDate', 'endDate' columns
record_data_cleaned = record_data.drop(['sourceName',
                                        'sourceVersion',
                                        'device',
                                        'creationDate',
                                        'endDate'], axis=1)
if (record_data_cleaned is None):
    print('No data to clean!')
    exit()
record_data_cleaned['Date'] = pd.to_datetime(record_data['startDate'])\
        .dt.strftime('%Y-%m-%d')

# value is numeric, NaN if fails
record_data_cleaned['value'] = pd.to_numeric(record_data['value'],
                                             errors='coerce')

# shorter observation names
record_data_cleaned['type'] = record_data_cleaned['type'].str\
        .replace('HKQuantityTypeIdentifier', '')
record_data_cleaned['type'] = record_data_cleaned['type'].str\
        .replace('HKCategoryTypeIdentifier', '')

print('Record types: ', record_data_cleaned['type'].unique())

# reorder 'record_data' columns
record_data_cleaned = record_data_cleaned[['type', 'Date', 'value', 'unit']]

# dictionary of DataFrames for filtered 'record_data'
record_data_df_dict = {}
# filter 'type' of 'record_data'
record_types = [
   'BodyMass',
   'BloodPressureSystolic',
   'BloodPressureDiastolic'
   ]
#    'ActiveEnergyBurned',
#    'BasalEnergyBurned',
#    'DistanceWalkingRunning',
#    'StepCount',
#    'AppleStandTime',
#    'WalkingSpeed',
#    'RunningSpeed',
#    'HeartRateVariabilitySDNN',
#    'RestingHeartRate',
#    'WalkingHeartRateAverage',
#    'VO2Max',
#    'HeartRateRecoveryOneMinute'

print('Filtering only for ', record_types)
# create new DataFrame for every interested data
for record_type in record_types:
    record_data_df_dict[record_type] = \
           record_data_cleaned.loc[
                   (record_data_cleaned['type'].str.match(record_type+'$'))]\
           .rename(columns={"value": record_type})\
           .sort_values(by='Date')\
           .drop_duplicates(subset=['Date'], keep='first')
#            .groupby('Date', group_keys=True).first().sort_values(by='Date')
# for record_type in record_types:
#    record_data_df_dict[record_type] = record_data_cleaned.filter(
#            regex=record_type, axis=0)

print(record_data_df_dict)

# Export to csv
print('Exporting to csv...')
for record_type in record_types:
    record_data_df_dict[record_type]\
            .to_csv('apple_health_export/'+record_type+'.csv', index=False)
