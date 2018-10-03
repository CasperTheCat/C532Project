import pandas as pd
from os import walk
from CritRole.Common import EDamageTypes
from CritRole.Common import EffectParser
import re

#EDamageTypes = ["Lightning", "Bleeding", "Poison", "Fire", "Falling", "Telekinetic", "Radiant", "Necrotic", "Psychic", "Ice", "Acid", "Thunder", "Physical"]

def sanitiseDate(x):
    safexl = x.split(' ')
    safex = safexl[len(safexl) - 1]
    return safex
    #return re.sub('[^0-9]','', safex)

def parseForTarget(x):
    #print(x)
    func, targ, param = EffectParser(x["To"], x["Potion"], x["Effect"])
    return [func, targ, param]

potionFrame = pd.read_csv("Potions/potions.csv")

# Fix the oddities in Timestamps
potionFrame["Time"] = potionFrame["Time"].map(sanitiseDate)

# frame["Potion"] is for UI, the parser should handle that data

# parse the Effect field
#potionFrame["Effect"] = potionFrame["Effect"].map(parseForTarget)
potionFrame["Effect"] = potionFrame.loc[:,"To":"Effect"].apply(parseForTarget, axis=1)

print(potionFrame[30:90])
potionFrame.to_csv("dummy.csv")
