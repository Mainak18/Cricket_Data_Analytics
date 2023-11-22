#abd v bumrah -
#comparison based upon ball by ball data in ipl

#-----------------------------------------------------------------------------------------------------------------------

#######             getting the data-


#importing requierd files-
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

#to display rows and collumns-
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

# ipl_ball_by_ball_data
df=pd.read_csv('IPL_ball_by_ball_updated.csv')
print(df.head(1))

#lets see the innings data  -
print(df['innings'].unique(),"\n")
#innings 3 & 4 reprsent the superover data and innings 5 & 6 represent the double superover data.
#so we will be using just the match information to do the matchups
df=df[(df['innings']==1) | (df['innings']==2)]
print(df['innings'].unique(),"\n")

#1st questoin is -
# What are the numbers when ABD faces Bumrah?
# step 1: Filter by player names - Done
# step 2: Use these names & assign it to striker & bowler - Done
# step 3: Get the required columns - Done

# step 1: Filter by player names - Done-
#print(df[df['bowling_team']=='Mumbai Indians']['bowler'].unique()) # it will show all the bowler of mumbai indians
#print(df[df['batting_team']=='Royal Challengers Bangalore']['striker'].unique())# it will show all the batting striker  of rcb
# player 1: JJ Bumrah
# player 2: AB de Villiers

requier_df=df[(df['striker']=='AB de Villiers') & (df['bowler']=='JJ Bumrah')] #so we have collected the requierd data frame where the striker is abd and the bowler is jj bumrah
print(requier_df.head(2),"\n")

#-----------------------------------------------------------------------------------------------------------------------



####               pre-processing the datas or calculating the kpi -
# No of runs scored?
# No of balls faced?
# No of times dismissed?

# No of runs scored?
no_runs_scored=sum(requier_df['runs_off_bat'])
print(f"total No of runs scored by abd against bumrah- {no_runs_scored}")

# No of balls faced? - just calculate total  no.rows that abd v bumrah faced
no_of_balls_faced=len(requier_df)
print(f"total No of balls faced by abd against bumrah- {no_of_balls_faced}")
# No of times dismissed?
no_of_times_dismissed=len(requier_df[df['player_dismissed']=='AB de Villiers'])
print(f"total No of times bumrah dismissed abd- {no_of_times_dismissed}\n")

#strike rate
sr=100*(no_runs_scored/no_of_balls_faced)
print(f"abd sr against bumrah- {sr}\n")



# Comparision against all batsman Bumrah has bowled to
bumrah_df=df[df['bowler']=='JJ Bumrah']
#total runs scored by this batsman
bumrah_df1=pd.DataFrame(bumrah_df.groupby('striker')['runs_off_bat'].sum()).reset_index() #as group by makes the data in a series we have to use panda data frame to
# keep this things inside a dtat frame to merge it later & we  have used .rest_index at the  end so that it could store the data in a collumn manner
print(bumrah_df1.head(2),'\n')
#total ball faced by this batsman-
bumrah_df2=pd.DataFrame(bumrah_df.groupby('striker')['ball'].count()).reset_index()
print(bumrah_df2.head(),"\n")
#merging striker information to balls
bumrah_df3=bumrah_df1.merge(bumrah_df2,on='striker',how='left') # as we are doing for baller we have to merge it on=striker
print(bumrah_df3.head(1),"\n")
#strike rate -
bumrah_df3['strike rate']=100*(bumrah_df3['runs_off_bat']/bumrah_df3['ball'])
print(bumrah_df3.head(3),'\n')
#minimum critereia that u have faced atleast 30 balls or more than that
bumrah_df3 =bumrah_df3[bumrah_df3['ball']>=30]
print(bumrah_df3.head(3),'\n')


#lets get same information for abd (abd v every one in his carrer) -
abd_df=df[df['striker']=='AB de Villiers']
#total runs scored by abd when he was facing this bowlers
abd_df1=pd.DataFrame(abd_df.groupby('bowler')['runs_off_bat'].sum()).reset_index()
print(abd_df1.head(),"\n")
#total balls faced by abd when he was facing this bowlers
abd_df2=pd.DataFrame(abd_df.groupby('bowler')['ball'].count()).reset_index()
print(abd_df2.head(),"\n")
abd_df3=abd_df1.merge(abd_df2,on='bowler',how='left')# as we are doing for baller we have to merge it on=bowler
print(abd_df3.head(),"\n")
#strike rate=
abd_df3['strike rate']=100*(abd_df3['runs_off_bat']/abd_df3['ball'])
print(abd_df3.head(),'\n')
#criteria-
#minimum critereia that u have faced atleast 30 balls or more than that
abd_df3 =abd_df3[abd_df3['ball']>=30]
print(abd_df3.head(3),'\n')

#reseting the indexing values so that it could start from 0
bumrah_df3.reset_index(inplace = True, drop = True)
abd_df3.reset_index(inplace = True, drop = True)

#so now we have the two data frame of that is abd_df3 & bumrah_df3
# so if we want to sort it -
print(bumrah_df3.sort_values('strike rate',ascending=False).head(),'\n')
print(abd_df3.sort_values('strike rate',ascending=False).head(),'\n')


#-----------------------------------------------------------------------------------------------------------------------

#######################         visualizations-

#bumrah against all batsmen-
print(bumrah_df3.head(),"\n")
plt.figure(figsize = (16,8))
plt.scatter(bumrah_df3['strike rate'],bumrah_df3['runs_off_bat'])
for i in range(len(bumrah_df3)): #to dd names on those dots at the chart
#     plt.text(x, y, text)- x controls name postion towards left(-) & right(+) ,y controls name postion towards down(-) & upp(+)
    if bumrah_df3['striker'][i] == 'V Kohli': #to modify virat kholi name towards left side and other names
        plt.text(bumrah_df3['strike rate'][i] - 7, bumrah_df3['runs_off_bat'][i] - 1, bumrah_df3['striker'][i] )
    else:
        plt.text(bumrah_df3['strike rate'][i] + 1, bumrah_df3['runs_off_bat'][i] - 1, bumrah_df3['striker'][i] )
#adding line horizontal & vertical lines  to differentiate more properly
plt.axvline(120, ls = '--', color = 'grey')#120 is starting point ls is the type of the line or the design and colour is thcolor noob
plt.axhline(60, ls = '--', color = 'grey')
plt.title('Batsmen against Bumrah in IPL(minimum 30 balls faced)')
plt.xlabel("strike rate (x)")
plt.ylabel("runs_off_bat (y)")
plt.show()


#abd against all bowlers-
print(abd_df3.head())
plt.figure(figsize = (16,8))
plt.scatter(abd_df3['strike rate'],abd_df3['runs_off_bat'])
for i in range(len(abd_df3)):
    if abd_df3['bowler'][i] == 'RA Jadeja':
        plt.text(abd_df3['strike rate'][i] - 7, abd_df3['runs_off_bat'][i] - 1, abd_df3['bowler'][i] )
    else:
        plt.text(abd_df3['strike rate'][i] + 1, abd_df3['runs_off_bat'][i] - 1, abd_df3['bowler'][i] )
plt.axvline(120, ls = '--', color = 'grey')
plt.axhline(60, ls = '--', color = 'grey')
plt.title('ABD against all bowlers in IPL(minimum 30 balls faced)')
plt.xlabel("strike rate (x)")
plt.ylabel("runs_off_bat (y)")
plt.show()


#-----------------------------------------------------------------------------------------------------------------------




######           conclusion of the case study-

print("----------------------------------------------------------conclusion-------------------------------------------------------------------------")

print("matchups : AB de Villiers vs Bumrah (only IPL Data)")
print(f"Balls: {no_of_balls_faced}")
print(f"Runs: {no_runs_scored}")
print(f"Outs: {no_of_times_dismissed}")
print(f"SR: {sr}\n")

print("Best Batsmen against Bumrah in IPL(minimum 30 balls faced) - ABD and many more refer to the given chart.")
print("ABD against all bowlers in IPL(minimum 30 balls faced)- Bumrah and many more refer to the given chart.")
print("so if you have gone through the charts and all the information that have mentioned before you can see clearly ABD has dominated over Bumrah.")
print("\nWinner - AB de Villiers ")



print("-----------------------------------------------------------------------------------------------------------------------------------------------")