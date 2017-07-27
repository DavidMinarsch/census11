import pandas as pd
import numpy as np
import math as m

ge_15 = pd.read_csv("/Users/davidminarsch/Desktop/Census11/2015_RESULTS_FOR_ANALYSIS.csv")
ge_15 = ge_15[['Press Association Reference', 'Constituency Name', 'Constituency ID', 'Region', 'Electorate', 'Votes', 'Con', 'Lab', 'LD', 'Grn', 'UKIP', 'PC']]
ge_15['Votes'] = ge_15['Votes'].str.replace(',','').astype(float) 
ge_15['Electorate'] = ge_15['Electorate'].str.replace(',','').astype(float) 
ge_15['Other'] = ge_15['Votes'] - ge_15.fillna(0)['Con'] - ge_15.fillna(0)['Lab'] - ge_15.fillna(0)['LD'] - ge_15.fillna(0)['Grn'] - ge_15.fillna(0)['UKIP']  - ge_15.fillna(0)['PC']
ge_15["Don't vote"] = ge_15['Electorate'] - ge_15['Votes']
ge_15 = ge_15[ge_15['Region'] != 'Scotland']
ge_15 = ge_15[ge_15['Region'] != 'Northern Ireland']
cols = ['Electorate', 'Votes', 'Con', 'Lab', 'LD', 'Grn', 'UKIP', 'PC', 'Other', "Don't vote"]
for i in range(0, len(cols)):
    ge_15[cols[i]] = ge_15[cols[i]].apply(lambda x: 0 if m.isnan(x) else int(x))
ge_15.drop(['Region'], axis=1, inplace=True)
ge_15.rename(columns={'Constituency ID': 'PCON16CD'}, inplace=True)
lookup = pd.read_csv("/Users/davidminarsch/Desktop/Census11/pc17_to_region_id_official.csv")
ge_15 = pd.merge(ge_15, lookup, how='left', on = ['PCON16CD'])
print(ge_15.isnull().any().any())
print((ge_15['Press Association Reference'] == ge_15['PA_ID']).any())
ge_15.drop(['Press Association Reference', 'Constituency Name', 'ID'], axis=1, inplace=True)
cols = ['PA_ID', 'PCON16CD', 'PCON16NM', 'region', 'Electorate', 'Votes', "Don't vote", 'Con', 'Lab', 'LD', 'Grn', 'UKIP', 'PC', 'Other']
ge_15 = ge_15[cols]
ge_15_share = ge_15[['Votes', 'Con', 'Lab', 'LD', 'Grn', 'UKIP', 'PC', 'Other']]
ge_15_share = ge_15_share.div(ge_15_share['Votes'], axis=0)
ge_15_share.drop(['Votes'], axis=1, inplace=True)
ge_15_share[['PA_ID', 'PCON16CD', 'PCON16NM', 'region']] = ge_15[['PA_ID', 'PCON16CD', 'PCON16NM', 'region']]
ge_15_share_2 = ge_15[['Electorate', 'Votes', "Don't vote"]]
ge_15_share_2 = ge_15_share_2.div(ge_15_share_2['Electorate'], axis=0)
ge_15_share[['voter_share', "non_voter_share"]] = ge_15_share_2[['Votes', "Don't vote"]]
ge_15_share = ge_15_share[['PA_ID', 'PCON16CD', 'PCON16NM', 'region', 'voter_share', 'non_voter_share', 'Con', 'Lab', 'LD', 'Grn', 'UKIP', 'PC', 'Other']]
ge_15_share.rename(columns={'Con': 'con_vote_share', 'Lab': 'lab_vote_share', 'LD': 'libdem_vote_share', 'Grn': 'green_vote_share', 'UKIP': 'ukip_vote_share', 'PC': 'plaid_vote_share', 'Other': 'other_vote_share'}, inplace=True)
ge_15.rename(columns={'Electorate': 'electorate', 'Votes': 'votes', "Don't vote": 'non_votes', 'Con': 'con_votes', 'Lab': 'lab_votes', 'LD': 'libdem_votes', 'Grn': 'green_votes', 'UKIP': 'ukip_votes', 'PC': 'plaid_votes', 'Other': 'other_votes'}, inplace=True)
ge_15.drop(['PCON16CD', 'PCON16NM', 'region'], axis=1, inplace=True)
ge_15_share.drop(['PCON16CD', 'PCON16NM', 'region'], axis=1, inplace=True)
ge_15 = ge_15.sort_values(by=['PA_ID'], ascending=[True])
ge_15 = ge_15.reset_index(drop=True)
ge_15_share = ge_15_share.sort_values(by=['PA_ID'], ascending=[True])
ge_15_share = ge_15_share.reset_index(drop=True)
ge_15.to_csv("/Users/davidminarsch/Desktop/Census11/2015_results_england_wales_by_constituency.csv", index=False)
ge_15_share.to_csv("/Users/davidminarsch/Desktop/Census11/2015_results_england_wales_by_constituency_shares.csv", index=False)

ge_10 = pd.read_csv("/Users/davidminarsch/Desktop/Census11/GE2010.csv")
ge_10 = ge_10[['Press Association Reference', 'Constituency Name', 'Region', 'Electorate', 'Votes', 'Con', 'Lab', 'LD', 'Grn', 'UKIP','PC']]
ge_10['Other'] = ge_10['Votes'] - ge_10.fillna(0)['Con'] - ge_10.fillna(0)['Lab'] - ge_10.fillna(0)['LD'] - ge_10.fillna(0)['Grn'] - ge_10.fillna(0)['UKIP']  - ge_10.fillna(0)['PC']
ge_10["Don't vote"] = ge_10['Electorate'] - ge_10['Votes']
ge_10 = ge_10[ge_10['Region'] != 'Scotland']
ge_10 = ge_10[ge_10['Region'] != 'Northern Ireland']
cols = ['Electorate', 'Votes', 'Other', "Don't vote", 'Con', 'Lab', 'LD', 'Grn', 'UKIP', 'PC']
for i in range(0, len(cols)):
    ge_10[cols[i]] = ge_10[cols[i]].apply(lambda x: 0 if m.isnan(x) else int(x))
ge_10.drop(['Region'], axis=1, inplace=True)
ge_10.rename(columns={'Press Association Reference': 'PA_ID'}, inplace=True)
lookup = pd.read_csv("/Users/davidminarsch/Desktop/Census11/pc17_to_region_id_official.csv")
ge_10 = pd.merge(ge_10, lookup, how='left', on = ['PA_ID'])
print(ge_10.isnull().any().any())
ge_10.drop(['Constituency Name', 'ID'], axis=1, inplace=True)
cols = ['PA_ID', 'PCON16CD', 'PCON16NM', 'region', 'Electorate', 'Votes', "Don't vote", 'Con', 'Lab', 'LD', 'Grn', 'UKIP', 'PC', 'Other']
ge_10 = ge_10[cols]
ge_10_share = ge_10[['Votes', 'Con', 'Lab', 'LD', 'Grn', 'UKIP', 'PC', 'Other']]
ge_10_share = ge_10_share.div(ge_10_share['Votes'], axis=0)
ge_10_share.drop(['Votes'], axis=1, inplace=True)
ge_10_share[['PA_ID', 'PCON16CD', 'PCON16NM', 'region']] = ge_10[['PA_ID', 'PCON16CD', 'PCON16NM', 'region']]
ge_10_share_2 = ge_10[['Electorate', 'Votes', "Don't vote"]]
ge_10_share_2 = ge_10_share_2.div(ge_10_share_2['Electorate'], axis=0)
ge_10_share[['voter_share', "non_voter_share"]] = ge_10_share_2[['Votes', "Don't vote"]]
ge_10_share = ge_10_share[['PA_ID', 'PCON16CD', 'PCON16NM', 'region', 'voter_share', 'non_voter_share', 'Con', 'Lab', 'LD', 'Grn', 'UKIP', 'PC', 'Other']]
ge_10_share.rename(columns={'Con': 'con_vote_share', 'Lab': 'lab_vote_share', 'LD': 'libdem_vote_share', 'Grn': 'green_vote_share', 'UKIP': 'ukip_vote_share', 'PC': 'plaid_vote_share', 'Other': 'other_vote_share'}, inplace=True)
ge_10.rename(columns={'Electorate': 'electorate', 'Votes': 'votes', "Don't vote": 'non_votes', 'Con': 'con_votes', 'Lab': 'lab_votes', 'LD': 'libdem_votes', 'Grn': 'green_votes', 'UKIP': 'ukip_votes', 'PC': 'plaid_votes', 'Other': 'other_votes'}, inplace=True)
ge_10.drop(['PCON16CD', 'PCON16NM', 'region'], axis=1, inplace=True)
ge_10_share.drop(['PCON16CD', 'PCON16NM', 'region'], axis=1, inplace=True)
ge_10 = ge_10.sort_values(by=['PA_ID'], ascending=[True])
ge_10 = ge_10.reset_index(drop=True)
ge_10_share = ge_10_share.sort_values(by=['PA_ID'], ascending=[True])
ge_10_share = ge_10_share.reset_index(drop=True)
ge_10.to_csv("/Users/davidminarsch/Desktop/Census11/2010_results_england_wales_by_constituency.csv", index=False)
ge_10_share.to_csv("/Users/davidminarsch/Desktop/Census11/2010_results_england_wales_by_constituency_shares.csv", index=False)

earnings = pd.read_csv("/Users/davidminarsch/Desktop/Census11/earnings_15.csv", encoding='latin-1')
cols = ['Self employment income mean', 'Self employment income median', 'Employment income mean', 'Employment income median', 'Pension income mean', 'Pension income median', 'Total income mean', 'Total income median']
for i in range(0, len(cols)):
    earnings[cols[i]] = earnings[cols[i]].apply(lambda x: x.replace(',','').replace('.','') if isinstance( x , str ) else x)
    earnings[cols[i]] = earnings[cols[i]].apply(lambda x: 0 if (x == '' or m.isnan(x)) else int(x))
earnings.rename(columns={'Constituency': 'PCON16NM'}, inplace=True)
earnings.set_value(572, 'PCON16NM', 'Ynys Môn')
earnings = pd.merge(earnings, lookup, how='left', on = ['PCON16NM'])
earnings.rename(columns={'Self employment income mean': 'self_employ_income_mean', 'Self employment income median': 'self_employ_income_median', 'Employment income mean': 'employ_income_mean', 'Employment income median': 'employ_income_median', 'Total income mean': 'income_mean', 'Total income median': 'income_median'}, inplace=True)
earnings = earnings[['PA_ID', 'self_employ_income_mean', 'self_employ_income_median', 'employ_income_mean', 'employ_income_median', 'income_mean', 'income_median']]
earnings.to_csv("/Users/davidminarsch/Desktop/Census11/earnings_15_by_constituency.csv", index=False)
earnings = earnings.sort_values(by=['PA_ID'], ascending=[True])
earnings = earnings.reset_index(drop=True)
