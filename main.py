import pandas as pd
import csv

def levenshtein(s, t):
    """ 
        iterative_levenshtein(s, t) -> ldist
        ldist is the Levenshtein distance between the strings 
        s and t.
        For all i and j, dist[i,j] will contain the Levenshtein 
        distance between the first i characters of s and the 
        first j characters of t
    """
    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]
    # source prefixes can be transformed into empty strings 
    # by deletions:
    for i in range(1, rows):
        dist[i][0] = i
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for i in range(1, cols):
        dist[0][i] = i
        
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = 1
            dist[row][col] = min(dist[row-1][col] + 1,      # deletion
                                 dist[row][col-1] + 1,      # insertion
                                 dist[row-1][col-1] + cost) # substitution
    # for r in range(rows):
        # print(dist[r])
    
 
    return dist[row][col]

df = pd.read_csv('dataset.csv')
removed_df = pd.DataFrame(columns = df.columns)
print(df.columns)

rows = df.shape[0]

mark = [True]*rows
drop_index = []

for i in range(rows):

    if mark[i] == False:
        continue

    fn1 = df.at[i,'fn'].split(' ')[0]
    ln1 = df.at[i,'ln'].split(' ')[0]

    for j in range(i+1,rows):
        if mark[j] == False:
            continue

        if df.at[i,'dob'] == df.at[j,'dob'] and df.at[i,'gn'] == df.at[j,'gn']:

            fn2 = df.at[j,'fn'].split(' ')[0]
            ln2 = df.at[j,'ln'].split(' ')[0]

            if fn1 == fn2 and ln1 == ln2:
                mark[j] = False
                drop_index.append(j)

removed_df = removed_df.append(df.loc[drop_index]);
removed_df = removed_df.reset_index()

df.drop(df.index[drop_index],inplace=True)
df = df.reset_index()


print("\n\nRemoval1---------------------------------------------->>\n\n")
print(df)
print("\nREMOVED ONES----->>\n")
print(removed_df)
print("\n\n\n\n\n")

# Checking spellings using Levenshtein distance

THRESH = 2

rows = df.shape[0]

mark = [True]*rows
drop_index = []

for i in range(rows):

    if mark[i] == False:
        continue

    fn1 = df.at[i,'fn'].split(' ')[0]
    ln1 = df.at[i,'ln'].split(' ')[0]

    for j in range(i+1,rows):
        if mark[j] == False:
            continue

        if df.at[i,'dob'] == df.at[j,'dob'] and df.at[i,'gn'] == df.at[j,'gn']:

            fn2 = df.at[j,'fn'].split(' ')[0]
            ln2 = df.at[j,'ln'].split(' ')[0]
            L=max(len(fn1),len(fn2))
            M=max(len(ln1),len(ln2))
            l=min(len(fn1),len(fn2))
            m=min(len(ln1),len(ln2))
            Fa=L-levenshtein(fn1,fn2)
            La=M-levenshtein(ln1,ln2)
            
            if float(Fa)/l >= 0.5 and float(La)/m >=0.5 :
                mark[j] = False
                drop_index.append(j)


removed_df = removed_df.append(df.loc[drop_index]);
removed_df = removed_df.reset_index()

df.drop(df.index[drop_index],inplace=True)
df = df.reset_index()

print('******************************')
print('Improved with spellings')
print('******************************\n\n')
print(df)
print("\nREMOVED ONES------->>\n\n")
print(removed_df.to_string())
df.to_csv('Output_file.csv')


#print(df[1][1])
