import math
import pandas as pd
from os import walk
import matplotlib.pyplot as plt
from CritRole.Common import EDamageTypes
from CritRole.Common import validOrZero
import numpy as np

colorsLookup = [
    (0.40,0.20,0.00),    # Vex
    (0.05,0.85,0.05),    # Trinket
    (0.20,0.20,0.20),    # Vax
    (0.70,0.70,0.70),    # Grog
    (0.00,0.80,0.00),    # Keyleth
    (0.80,0.20,0.20),    # Percy
    (0.80,0.00,0.80),    # Scanlan
    (1.00,0.80,0.05),    # Pike
    (0.06,0.06,0.06)     # BorderColour
]

globalData = {}
accmData = []
gindex = 0
takenData = []
hindex = 0
ldpi = 120#99
lfs = (27,27)
totalBarScale = 1.2
barwidth = 0.12
spacingwidth = 0.072
innerBarScalar = 1.92
bgc = (0.06,0.06,0.06) 
baredge = colorsLookup[len(colorsLookup) - 1]
eqray = np.ones(len(colorsLookup) - 1)


def plotDiagram(charDamageDealt, charDamageTaken, episode, fig, ax):

    #bgc = (1,1,1)

    #Intersparse the array
    midring = []
    midcolour = []
    outerring = []
    outercolour = []
    totalDamage = np.sum(charDamageDealt)
    totalTake = np.sum(charDamageTaken)
    total = 0
    to = 0

    oneOverLength = 1 / len(charDamageDealt)

    maximalPercentile = 0

    for i in range(0, len(charDamageDealt)):
        #damageAsPercentage = charDamageDealt[i] / totalDamage
        #total += damageAsPercentage * (len(charDamageDealt) - 1)
        #to += (1 - damageAsPercentage)
        #midring.append(damageAsPercentage * (len(charDamageDealt)))
        #midring.append(1.0 - damageAsPercentage)
        damageAsPercentage = 0

        if(totalDamage > 0):
            damageAsPercentage = charDamageDealt[i] / totalDamage

            if damageAsPercentage > maximalPercentile:
                maximalPercentile = damageAsPercentage
        
        #print(chararr[i] + " Dealt " + str(damageAsPercentage) + "% ")
        #print("Scaling to % of total circle: " + str(damageAsPercentage * oneOverLength))

        takenAsPercentage = 0
        if(totalTake > 0):
            takenAsPercentage = charDamageTaken[i] / totalTake

            if takenAsPercentage > maximalPercentile:
                maximalPercentile = takenAsPercentage
        #print(chararr[i] + " took " + str(takenAsPercentage) + "% ")
        #print("Scaling to % of total circle: " + str(takenAsPercentage * oneOverLength))
    

    print(maximalPercentile)

    scalar = 1 / max(math.sqrt(maximalPercentile), 1e-10)

    print(scalar)

    for i in range(0, len(charDamageDealt)):
        #damageAsPercentage = charDamageDealt[i] / totalDamage
        #total += damageAsPercentage * (len(charDamageDealt) - 1)
        #to += (1 - damageAsPercentage)
        #midring.append(damageAsPercentage * (len(charDamageDealt)))
        #midring.append(1.0 - damageAsPercentage)
        damageAsPercentage = 0
        if(totalDamage > 0):
            damageAsPercentage = charDamageDealt[i] / totalDamage
            damageAsPercentage *= scalar

        takenAsPercentage = 0
        if(totalTake > 0):
            takenAsPercentage = charDamageTaken[i] / totalTake
            takenAsPercentage *= scalar

        # Flip
        half = len(charDamageDealt) / 2
        flip = half - i
        print(flip)

        if not flip > 0:
            midring.append(damageAsPercentage)
            midcolour.append(colorsLookup[i])

            midring.append(1.0 - damageAsPercentage)
            midcolour.append(baredge)

            outerring.append(takenAsPercentage)
            outercolour.append(colorsLookup[i])

            outerring.append(1.0 - takenAsPercentage)
            outercolour.append(baredge)
        else:
            midring.append(1.0 - damageAsPercentage)
            midcolour.append(baredge)

            midring.append(damageAsPercentage)
            midcolour.append(colorsLookup[i])
            
            outerring.append(1.0 - takenAsPercentage)
            outercolour.append(baredge)

            outerring.append(takenAsPercentage)
            outercolour.append(colorsLookup[i])

            
        

        
    print(total)
    print(to)
        
    # Create colors
    #a, b, c=[plt.cm.Blues, plt.cm.Reds, plt.cm.Greens]
    
    # First Ring (outside)

    
    ax.axis('equal')

    mypie, _ = ax.pie(outerring, radius=totalBarScale, colors=outercolour)
    plt.setp( mypie, width=barwidth, edgecolor=baredge)
    
    # Second Ring (Inside)
    mypie2, _ = ax.pie(midring, radius=totalBarScale - (barwidth + spacingwidth), labeldistance=0.7, colors=midcolour);# colors=[a(0.5), a(0.4), a(0.3), b(0.5), b(0.4), c(0.6), c(0.5), c(0.4), c(0.3), c(0.2)])
    plt.setp( mypie2, width=barwidth, edgecolor=baredge)
    plt.margins(0,0)

    # Second Ring (Inside)
    mypie3, _ = ax.pie(eqray, radius=totalBarScale - 2 * (barwidth + spacingwidth), labeldistance=0.7, colors=colorsLookup) #colors=[a(0.5), a(0.4), a(0.3), b(0.5), b(0.4), c(0.6), c(0.5), c(0.4), c(0.3), c(0.2)])
    plt.setp( mypie3, width=barwidth * innerBarScalar, edgecolor=baredge)
    plt.margins(0,0)

    fig.set_facecolor(bgc)
    ax.set_facecolor(bgc)
    
    # show it
    #plt.show()
    
    plt.savefig("hud/episode." + str(episode) + ".png", transparent=True)
    plt.cla()
    plt.clf()
    plt.close()

def process_file(root, x, character):
    global gindex
    fileindex = x.split('.')[0].split(' ')[1].zfill(3)
#    if not x == "64.html.csv":# and not x == "44.html.csv" and not x == "33.html.csv":
#       return
    #print("Processing file: " + str(x))
    eviFrame = pd.read_csv(root + x, index_col=0);
    retable = eviFrame.index.values
    #print(eviFrame["PhysicalInstVals"][0:20])
    #eviFrame = eviFrame.loc[:, EDamageTypes[0]:EDamageTypes[len(EDamageTypes) - 1]+"Instances"]
    #eviFrame = eviFrame.loc[:, EDamageTypes[0]:EDamageTypes[len(EDamageTypes) - 1]]
    #eviFrame = eviFrame.loc[:, "Physical":"LightningInstances"]
    nFrame = pd.DataFrame()
    nFrame["Physical"] = eviFrame["Physical"]
    nFrame["PhysicalInstVals"] = eviFrame["PhysicalInstVals"]
    #eviFrame = eviFrame["Physical"]
    nFrame = nFrame.iloc[[(character)]]
    #eviFrame = eviFrame.rename(index={1: gindex})
    nFrame.index.name = "Episode"
    last = nFrame.index[-1]
    nFrame = nFrame.rename(index={last: str(fileindex)})
    #eviFrame["Episode"] = fileindex
    gindex += 1
    # + eviFrame[2:8]
    #eviFrame = eviFrame.drop(['Trinket'])
    
    #print(character)
    if len(accmData) > character:
        #accmData[0].append(eviFrame, ignore_index=True);
        accmData[character] = pd.concat([accmData[character], nFrame]);
        #print(gindex)
        #print(accmData[0])
    else:
        accmData.append(nFrame);
    return retable
        
def process_filet(root, x, character):
    global hindex
    fileindex = x.split('.')[0].zfill(3)
#    if not x == "64.html.csv":# and not x == "44.html.csv" and not x == "33.html.csv":
#       return
    #print("Processing file: " + str(x))
    eviFrame = pd.read_csv(root + x, index_col=0);
    retable = eviFrame.index.values
    #print(eviFrame["PhysicalInstVals"][0:20])
    #eviFrame = eviFrame.loc[:, EDamageTypes[0]:EDamageTypes[len(EDamageTypes) - 1]+"Instances"]
    #eviFrame = eviFrame.loc[:, EDamageTypes[0]:EDamageTypes[len(EDamageTypes) - 1]]
    #eviFrame = eviFrame.loc[:, "Physical":"LightningInstances"]
    nFrame = pd.DataFrame()
    nFrame["Physical"] = eviFrame.loc[:, EDamageTypes[0]:EDamageTypes[len(EDamageTypes) - 1]].apply(np.sum, axis=1)
    #nFrame["PhysicalInstVals"] = eviFrame["PhysicalInstVals"]
    #eviFrame = eviFrame["Physical"]
    nFrame = nFrame.iloc[[(character)]]
    #eviFrame = eviFrame.rename(index={1: gindex})
    nFrame.index.name = "Episode"
    last = nFrame.index[-1]
    nFrame = nFrame.rename(index={last: str(fileindex)})
    #eviFrame["Episode"] = fileindex
    hindex += 1
    # + eviFrame[2:8]
    #eviFrame = eviFrame.drop(['Trinket'])

    #print(character)
    if len(takenData) > character:
        #accmData[0].append(eviFrame, ignore_index=True);
        takenData[character] = pd.concat([takenData[character], nFrame]);
        #print(gindex)
        #print(accmData[0])
    else:
        takenData.append(nFrame)
        
# Enumerate the folder
damageTaken = []
damageTakens = []
chararr = []

rootDirectoryt = "./ParsedDamageTaken/"
for (dirpath, dirnames, filenames) in walk(rootDirectoryt):
    damageTaken.extend(filenames)

rootDirectory = "./ParsedDamageDealt/"
for (dirpath, dirnames, filenames) in walk(rootDirectory):
    damageTakens.extend(filenames)

    
for chars in range(0,8):
    for singleFile in damageTakens:
        chararr = process_file(rootDirectory, singleFile, chars)

    for singleFilet in damageTaken:
        process_filet(rootDirectoryt, singleFilet, chars)
        
    accmData[chars] = accmData[chars].sort_index()      
    takenData[chars] = takenData[chars].sort_index()      

#print("Done")

for i in range(1, 116):
    episode = i
    episodeSelector = str(episode).zfill(3)
    charDamageDealt = []
    charDamageTaken = []
    for e in range(0, len(accmData)):
        sums = pd.DataFrame()
        sums["Physical"] = accmData[e]["Physical"]
        
        # NaN check
        temp = sums.transpose()[episodeSelector]

        if temp.any():
            charDamageDealt.append(int(temp))
        else:
            charDamageDealt.append(0)



        sums["Physical"] = takenData[e]["Physical"]

        temp = sums.transpose()[episodeSelector]

        if temp.any():
            charDamageTaken.append(int(temp))
        else:
            charDamageTaken.append(0)
        #sums = sums.apply(np.sum)
    print(charDamageDealt)
    print(charDamageTaken)
    fig, ax = plt.subplots(figsize=lfs, dpi=ldpi)
    print("Plotting: " + episodeSelector)
    plotDiagram(charDamageDealt, charDamageTaken, episodeSelector, fig, ax)
