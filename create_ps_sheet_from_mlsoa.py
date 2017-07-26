import pandas as pd
import numpy as np

# https://www.nomisweb.co.uk/query/construct/summary.asp?mode=construct&version=0&dataset=651
# http://geoportal.statistics.gov.uk/datasets?q=Ward%20to%20Westminster%20Parliamentary%20Constituency%20to%20Local%20Authority%20District%20Lookup&sort=name
# http://geoportal.statistics.gov.uk/datasets/65544c20a5804677a2594fe750bf4482_0

# load data:
census_11_mlsoa_male_white = pd.read_csv("/Users/davidminarsch/Desktop/Census11/mlsoa_male_white.csv")
census_11_mlsoa_male_asian = pd.read_csv("/Users/davidminarsch/Desktop/Census11/mlsoa_male_asian.csv")
census_11_mlsoa_male_black = pd.read_csv("/Users/davidminarsch/Desktop/Census11/mlsoa_male_black.csv")
census_11_mlsoa_male_mixed = pd.read_csv("/Users/davidminarsch/Desktop/Census11/mlsoa_male_mixed.csv")
census_11_mlsoa_male_other = pd.read_csv("/Users/davidminarsch/Desktop/Census11/mlsoa_male_other.csv")
census_11_mlsoa_female_white = pd.read_csv("/Users/davidminarsch/Desktop/Census11/mlsoa_female_white.csv")
census_11_mlsoa_female_asian = pd.read_csv("/Users/davidminarsch/Desktop/Census11/mlsoa_female_asian.csv")
census_11_mlsoa_female_black = pd.read_csv("/Users/davidminarsch/Desktop/Census11/mlsoa_female_black.csv")
census_11_mlsoa_female_mixed = pd.read_csv("/Users/davidminarsch/Desktop/Census11/mlsoa_female_mixed.csv")
census_11_mlsoa_female_other = pd.read_csv("/Users/davidminarsch/Desktop/Census11/mlsoa_female_other.csv")
mlsoa11_to_w16_lookup = pd.read_csv("/Users/davidminarsch/Desktop/Census11/Middle_Layer_Super_Output_Area_2011_to_Ward_to_Local_Authority_District_December_2016_Lookup_in_England_and_Wales.csv", encoding='latin-1')
w16_to_pc16_lookup = pd.read_csv("/Users/davidminarsch/Desktop/Census11/Ward_to_Westminster_Parliamentary_Constituency_to_Local_Authority_District_December_2016_Lookup_in_the_United_Kingdom.csv")

print(np.where(mlsoa11_to_w16_lookup['MSOA11CD'].apply(lambda x: x == '')))
print(np.where(mlsoa11_to_w16_lookup['WD16CD'].apply(lambda x: x == '')))
print(np.where(w16_to_pc16_lookup['WD16CD'].apply(lambda x: x == '')))
print(np.where(w16_to_pc16_lookup['PCON16NM'].apply(lambda x: x == '')))
mlsoa11_to_w16_lookup.drop(['MSOA11NM', 'LAD16CD', 'LAD16NM', 'FID'], axis=1, inplace=True)
w16_to_pc16_lookup.drop(['WD16NM', 'LAD16CD', 'LAD16NM', 'FID'], axis=1, inplace=True)

n_sex = 2
n_ethnicity = 5
n_constituency = 573
n_age = 17

# Lookup identifiers:
for sex in ['male', 'female']:
    for ethnicity in ['white', 'asian', 'black', 'mixed', 'other']:
        census_11_mlsoa = globals()['census_11_mlsoa_' + sex + '_' + ethnicity]
        census_11_mlsoa.rename(columns={'mnemonic': 'MSOA11CD', '2011 super output area - middle layer': 'MSOA11NM'}, inplace=True)
        print(np.where(census_11_mlsoa['MSOA11CD'].apply(lambda x: x == '')))
        census_11_mlsoa11_w16 = pd.merge(census_11_mlsoa, mlsoa11_to_w16_lookup, how='left', on = ['MSOA11CD'])
        census_11_mlsoa11_w16_pc16 = pd.merge(census_11_mlsoa11_w16, w16_to_pc16_lookup, how='left', on = ['WD16CD'])
        census_11_mlsoa11_w16_pc16.to_csv("/Users/davidminarsch/Desktop/Census11/mlsoa11_w16_pc16_" + sex + "_" + ethnicity + ".csv")
        # For now merge low ages:
        census_11_mlsoa11_w16_pc16['Age 15'] = census_11_mlsoa11_w16_pc16['Age 0 to 4'] +   census_11_mlsoa11_w16_pc16['Age 5 to 7'] + census_11_mlsoa11_w16_pc16['Age 8 to 9'] + census_11_mlsoa11_w16_pc16['Age 10 to 14'] + census_11_mlsoa11_w16_pc16['Age 15']
        census_11_mlsoa11_w16_pc16.drop(['Age 0 to 4', 'Age 5 to 7', 'Age 8 to 9', 'Age 10 to 14'], axis=1, inplace=True)
        census_11_mlsoa11_w16_pc16.rename(columns={'Age 15': 'Age 15 and below'}, inplace=True)
        # Downsample to constituency:
        census_11_pc16 = census_11_mlsoa11_w16_pc16.drop(['WD16CD', 'WD16NM', 'MSOA11NM', 'MSOA11CD'], axis=1)
        census_11_pc16 = census_11_pc16.groupby(['PCON16CD', 'PCON16NM'], as_index=False).sum()
        globals()['census_11_pc16_' + sex + '_' + ethnicity] = census_11_pc16

census_11 = pd.DataFrame(columns={'sex', 'ethnicity', 'constituency', 'age', 'N'})
census_11_str = pd.DataFrame(columns={'sex', 'ethnicity', 'constituency', 'age', 'N'})
for c in range(0, n_constituency):
  print(c)
  for e in range(0, n_ethnicity):
    for s in range(0, n_sex):
      for a in range(0, n_age):
        if s == 0:
          sex = 'male'
        else:
          sex = 'female'
        if e == 0:
          ethnicity = 'white'
        elif e == 1:
          ethnicity = 'mixed'
        elif e == 2:
          ethnicity = 'asian'
        elif e == 3:
          ethnicity = 'black'
        else:
          ethnicity = 'other'
        selection = globals()['census_11_pc16_' + sex + '_' + ethnicity]
        val = selection.iloc[c, a + 2]
        if not isinstance( val, np.int64 ):
          val = int(val.replace(',', ''))
        data = pd.DataFrame({'sex': [s], 'ethnicity': [e], 'constituency': [c], 'age': [a], 'N': [val]})
        census_11 = census_11.append(data)
        constituency = selection['PCON16CD'][c]
        age = selection.columns[a + 2]
        data = pd.DataFrame({'sex': [sex], 'ethnicity': [ethnicity], 'constituency': [constituency], 'age': [age], 'N': [val]})
        census_11_str = census_11_str.append(data)

census_11 = census_11.astype(int)
census_11_str.N = census_11_str.N.astype(int)

census_11.to_csv("/Users/davidminarsch/Desktop/Census11/census_11_pc16_four_way_joint_distribution.csv", index=False)
census_11_str.to_csv("/Users/davidminarsch/Desktop/Census11/census_11_pc16_four_way_joint_distribution_str.csv", index=False)