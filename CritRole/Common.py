EDamageTypes = ["Lightning", "Poison", "Fire", "Falling", "Radiant", "Necrotic", "Psychic", "Ice", "Acid", "Thunder", "Physical"]

def validOrZero(x):
    if x == x:
        return x
    else:
        return 0

def EffectParser(x):
    print(x)

    target = ""

    if x == x:
        xs = x.split(' ')
    
        if xs[1] == "heals":
        # target of the sentence
            target = xs[2]
        

    return target, "heals", "e"