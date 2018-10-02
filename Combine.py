import pandas as pd
from os import walk
from CritRole.Common import EDamageTypes
from CritRole.Common import validOrZero

#EDamageTypes = ["Lightning", "Bleeding", "Poison", "Fire", "Falling", "Telekinetic", "Radiant", "Necrotic", "Psychic", "Ice", "Acid", "Thunder", "Physical"]

#def validOrZero(x):
#    if x == x:
#        return x
#    else:
#        return 0

globalData = {}
accmData = []

def process_file(root, x):
#    if not x == "64.html.csv":# and not x == "44.html.csv" and not x == "33.html.csv":
#       return
    print("Processing file: " + str(x))
    eviFrame = pd.read_csv(root + x, index_col=0);
    eviFrame = eviFrame.loc[:, EDamageTypes[0]:EDamageTypes[len(EDamageTypes) - 1]+"Instances"]
    if len(accmData) > 0:
        accmData[0] += eviFrame;
    else:
        accmData.append(eviFrame);
    #print(eviFrame)
    #print(accmData)
#    print(eviFrame.shape[0])
    for i in range(0, len(EDamageTypes)):
        #print(eviFrame.columns[i]);
        dAgg = eviFrame[eviFrame.columns[i]];

        if EDamageTypes[i] in globalData:
            globalData[EDamageTypes[i]][0] += dAgg
        else:
            globalData[EDamageTypes[i]] = []
            globalData[EDamageTypes[i]].append(dAgg)
#        DamageAgg = eviFrame[''
        
# Enumerate the folder
damageTakens = []
rootDirectory = "./ParsedDamageTaken/"
for (dirpath, dirnames, filenames) in walk(rootDirectory):
    damageTakens.extend(filenames)


for singleFile in damageTakens:
    process_file(rootDirectory, singleFile)

#print(globalData)
print(accmData)
accmData[0].to_csv("comb.csv")
