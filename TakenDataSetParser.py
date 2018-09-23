import pandas as pd
from os import walk

EDamageTypes = ["Lightning", "Bleeding", "Poison", "Fire", "Falling", "Telekinetic", "Radiant", "Necrotic", "Psychic", "Ice", "Acid", "Thunder", "Physical"]

def validOrZero(x):
    if x == x:
        return x
    else:
        return 0

def process_file(root, x):
    if not x == "1.html.csv" and not x == "44.html.csv" and not x == "33.html.csv":
        return
    print("Processing file: " + str(x))
    eviFrame = pd.read_csv(root + x, index_col=0);
    print(eviFrame.shape[0])
    for i in range(0, int(eviFrame.shape[0])):
        tList = [int(s) for s in eviFrame['PhysicalInstVals'][i].split(',')]
        iDamageMax = max(tList)
        iAvgDamage = validOrZero(eviFrame['Physical'][i] / eviFrame['PhysicalInstances'][i]);
        print(str(eviFrame.index[i]) + "\n\tMaxTaken: " + str(iDamageMax) + "\n\tAvgTaken: " + str(iAvgDamage))
        
# Enumerate the folder
damageTakens = []
rootDirectory = "./ParsedDamageTaken/"
for (dirpath, dirnames, filenames) in walk(rootDirectory):
    damageTakens.extend(filenames)


for singleFile in damageTakens:
    process_file(rootDirectory, singleFile)