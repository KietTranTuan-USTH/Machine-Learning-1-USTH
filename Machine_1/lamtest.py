import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
Matches = pd.read_csv("WorldCupMatches.csv")
Champion = pd.read_csv("WorldCups.csv")
Ranking = pd.read_csv("fifa_ranking-2023-07-20.csv",parse_dates=["rank_date"])
start_date = pd.to_datetime('2022-01-01')
end_date = pd.to_datetime('2022-02-11')
Ranking = Ranking[(Ranking["rank_date"]>start_date)&(Ranking["rank_date"]<end_date)]
Ranking = Ranking.drop(["rank","country_abrv","previous_points","confederation","rank_change","rank_date"], axis = 1)
print(Ranking.head(10))
#Since variables like Year,Datetime,Stage
def info(df):
    variables = []
    data_types = []
    count = []
    unique = []
    missing_values = []
    #Getting the info of each columns and finding total missing values
    for item in df.columns:
        variables.append(item)
        data_types.append(df[item].dtype)
        count.append(len(df[item]))
        unique.append(len(df[item].unique()))
        missing_values.append(df[item].isna().sum())
        
    output = pd.DataFrame({
        'variable': variables, 
        'data type': data_types,
        'count': count,
        'unique': unique,
        'missing values': missing_values
    })    
        
    return output
#This shows that the Matches dataframe has null values
print(info(Matches))
Matches = Matches.dropna()


print(Matches.columns)

# sns.countplot(Champion["Country"])
# plt.show()
#Replacing names from the Soviet era
def replace(df):
    if(df['Home Team Name'] in ['German DR', 'Germany FR']):
        df['Home Team Name'] = 'Germany'
    elif(df['Home Team Name'] == 'Soviet Union'):
        df['Home Team Name'] = 'Russia'
    
    if(df['Away Team Name'] in ['German DR', 'Germany FR']):
        df['Away Team Name'] = 'Germany'
    elif(df['Away Team Name'] == 'Soviet Union'):
        df['Away Team Name'] = 'Russia'
    
    return df


    
matches = Matches.apply(replace, axis=1)
matches = matches.drop(["Year","Datetime","Stage",
              "Stadium","City","Win conditions",
              "Attendance","Half-time Home Goals",
              "Half-time Away Goals","Referee",
              'Assistant 1', 'Assistant 2',
              'RoundID', 'MatchID', 
              'Home Team Initials',
              'Away Team Initials'], axis = 1)
#relabeling the team name
matches = pd.merge(matches, Ranking, left_on="Home Team Name", right_on="country_full", how="left")
matches = pd.merge(matches, Ranking, left_on="Away Team Name", right_on="country_full", how="left", suffixes=("_home", "_away"))
def indexing_theteams(df):
    teams = {}
    index = 0
    for lab,row in matches.iterrows():
        if row["Home Team Name"] not in teams.keys():
            teams[row["Home Team Name"]] = index
            index += 1
        if row["Away Team Name"] not in teams.keys():
            teams[row["Away Team Name"]] = index
            index += 1
    return teams
teams_index = indexing_theteams(matches)
print(teams_index)
# def getfifapoint(row, df1):
#     if row["Home Team Name"] in df1["country_full"].values:
#         row["Home Team Fifa Point"] = df1.loc[df1["country_full"] == row["Home Team Name"], "total_points"].values[0]
#     if row["Away Team Name"] in df1["country_full"].values:
#         row["Away Team Fifa Point"] = df1.loc[df1["country_full"] == row["Away Team Name"], "total_points"].values[0]
#     return row

# matches = matches.apply(getfifapoint, args=(Ranking,))

matches["Home Team Name"] = matches["Home Team Name"].apply(lambda x: teams_index[x])
matches["Away Team Name"] = matches["Away Team Name"].apply(lambda x: teams_index[x])
matches["Who Wins"] = 0
matches["Goal Difference"] = 0
matches["Championship Won"] = 0
matches["Goal Difference"] = matches["Home Team Goals"] - matches["Away Team Goals"]

def gettingwhowins(df):
    if df["Goal Difference"] > 0:
        df["Who Wins"] = 1 #Home team wins
    if df["Goal Difference"] < 0:
        df["Who Wins"] = 0 #Away team wins
    return df

matches = matches.apply(gettingwhowins,axis = 1)
matches = matches.drop(["country_full_home","country_full_away"],axis = 1)

print(matches.head(10))

        