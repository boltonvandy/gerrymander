# Grant Redfield
import pandas as pd
import numpy as np
import math
import bitarray
from bitstring import BitArray
from scipy.sparse import csr_matrix
from scipy.sparse import coo_matrix

pd.set_option('display.max_columns', None)
# https://stackoverflow.com/questions/11869910/pandas-filter-rows-of-dataframe-with-operator-chaining
# use this for filtering my dataframe

class NDSparseMatrix:
  def __init__(self):
    self.elements = {}

  def addValue(self, tuple, value):
    self.elements[tuple] = value

  def readValue(self, tuple):
    try:
      value = self.elements[tuple]
    except KeyError:
      value = 0
    return value

# Load in my Data
precinct_data = pd.read_csv('C://Users//Grant//Desktop//Random//CS_CLASS//Gerry//azvreg_precinct.csv')

precinct_data = precinct_data.dropna()

# Lets only look at two districts, and restrict it down to Two parties (REP and DEM)


precinct_data = precinct_data[((precinct_data["DistCD"] == 7) | (precinct_data["DistCD"] == 8)) & (
            (precinct_data["CDE_PARTY"] == "REP") | (precinct_data["CDE_PARTY"] == "DEM"))]


# Lets transform our data so each presinct has data on one row
precinct_data = pd.merge(precinct_data, precinct_data, on='PCTCD', how="left")

# Remove Duplicates due to Left Join Logic
precinct_data = precinct_data[
    ((precinct_data["CDE_PARTY_x"] == "DEM") & (precinct_data["CDE_PARTY_x"] != precinct_data["CDE_PARTY_y"]))]

# Drop Unnecessary Columns
precinct_data = precinct_data.drop(
    columns=['DistCD_x', 'DistLD_x', 'DistCD_y', 'DistLD_y', 'CDE_PARTY_x', 'CDE_PARTY_y'], axis=1)

# Rename Columns
precinct_data.columns = ['Precinct', 'DEM_VOTES', 'REP_VOTES']

precinct_data['Total_Votes'] = precinct_data['DEM_VOTES'] + precinct_data['REP_VOTES']



#Need to restrict it to this amount.....Algo doesnt take many rows well
precinct_data = precinct_data.head(4)

Total_Votes = precinct_data['Total_Votes'].sum()

Number_of_Precincts = len(precinct_data)

Half_Precincts = math.ceil(Number_of_Precincts / 2)

precinct_data = precinct_data.reset_index(drop=True)

rows, cols = (Number_of_Precincts, Half_Precincts)


print("Total_Votes", Total_Votes)
print("Unique Precincts ",Number_of_Precincts )


SuperMatrix = NDSparseMatrix()
SuperMatrix.addValue((0,0,0,0), 1)


def Final_Solution():
    Current_J = 0
    Current_K = 0
    for j in range(1, Number_of_Precincts +1):
        for k in range(1, Number_of_Precincts+1):
            for x in range(0, Total_Votes+1):
                for y in range(0, Total_Votes+1):
                    if Current_J != j:
                        Current_J = j
                        print("J", j)
                        print("K", k)
                        print("X", x)
                        print("Y", y)
                        print("precinct_data['REP_VOTES'][j]", precinct_data['REP_VOTES'][j])
                    if Current_K != k:
                        Current_K = k
                        print("K", k)

                    if SuperMatrix.readValue((j - 1,k - 1, x - precinct_data['REP_VOTES'][j],y)) == 1 or SuperMatrix.readValue((j - 1,k,x,y - precinct_data['REP_VOTES'][j])) == 1:
                        SuperMatrix.addValue((j, k, x, y), 1)
                    #SuperMatrix.addValue((j,k,x,y), SuperMatrix.readValue((j - 1,k - 1, x - precinct_data['REP_VOTES'][j],y)) or SuperMatrix.readValue((j - 1,k,x,y - precinct_data['REP_VOTES'][j])) )
                    if SuperMatrix.readValue((j, k, x, y)) == 1:
                        print("DID THIS CHANGE?", SuperMatrix.readValue((j, k, x, y)))
                        print("K", k)
                        print("X", x)
                        print("Y", y)
                        print("SUCCESSSSSSSS")
                    if j == (Number_of_Precincts) and k == (Half_Precincts) and x > Total_Votes/4 and y > Total_Votes/4 and SuperMatrix.readValue((j, k, x, y)) == 1:
                        print("final J", j)
                        print("final K", k)
                        print("final X", x)
                        print("final Y", y)
                        return True
                        break
    return False


LetsRun = Final_Solution()

if LetsRun:
    print("GerryMandering is possible")
else:
    print("GerryMandering is not possible")



