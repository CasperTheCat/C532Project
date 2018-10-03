from CritRole.Potion import DPotionTranslation

EDamageTypes = ["Lightning", "Poison", "Fire", "Falling", "Radiant", "Necrotic", "Psychic", "Ice", "Acid", "Thunder", "Physical"]

def validOrZero(x):
    if x == x:
        return x
    else:
        return 0




def EffectParser(_target, _potion,_effect):
    target = ""
    subject = 0
    effect = "None"

    if _effect == _effect: # Check that Effect is not NAN
        effects = _effect.split(' ')
    
        if effects[1] == "heals":
            # target of the sentence
            target = effects[0]
            effect = "Heal"

            # subject
            if not effects[2].lower() == "unknown":
                subject = effects[2]
            else:
                # average potion value
                subject = DPotionTranslation[_potion]
        else:
            # Handler for other potion types
            potionNameSplit = _potion.split(' ')
            effect = potionNameSplit[len(potionNameSplit) - 1]
            if effect.lower() == "resistance":
                subject = potionNameSplit[len(potionNameSplit) - 2]
            elif effect.lower() == "breathing":
                subject = potionNameSplit[len(potionNameSplit) - 2]
            elif effect.lower() == "scrying":
                # This works... badly but it works. NLP is difficult
                subject = effects[len(effects) - 2] + " " + effects[len(effects) - 1]

            # handle attribute increases, only fox's cunning and str
            elif effect.lower() == "cunning":
                effect = "AttributeBoost"
                subject = ["Intelligence", "Advantage"]
            elif effect.lower() == "strength":
                effect = "AttributeBoost"
                subject = ["Strength", "Set", "23"]
            target = _target

    else:
        # Effect is infinite, or NAN
        target = _target
        effect = "ERROR"
        subject = -1

    return effect, target, subject
