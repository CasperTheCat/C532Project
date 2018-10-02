import sys
from os import walk
import re
from html.parser import HTMLParser

EDamageTypes = ["Lightning", "Bleeding", "Poison", "Fire", "Falling", "Telekinetic", "Radiant", "Necrotic", "Psychic", "Ice", "Acid", "Thunder", "Physical"]

class TakenDamageParser(HTMLParser):
    def __init__(self, _x):
        self.x = _x;
        self.column = 0;
        self.row = 0;
        self.bStartCounting = False;
        self.characters = {};
        self.damageMap = {};
        self.damageType = "Physical"
        self.readStyle = False;
        self.registeredCharacters = []
        super(TakenDamageParser, self).__init__()

    def translate_to_damage_type(self, x):
        return x
        if x == "s7":
            return "Poison"
        return "Physical"

    def handle_starttag(self, tag, attrs):
        #print("Start tag:", tag)
        if tag == "tbody":
            self.bStartCounting = True;
        
        if self.bStartCounting and tag == "tr":
            self.row += 1;
            self.column = 0;

        if self.bStartCounting and tag == "td":
            self.column += 1;

        for attr in attrs:
            if "class" in attr:
                self.damageType = self.translate_to_damage_type(attr[1])
            
        if tag == "style":
            self.readStyle = True;
            #print ("     attr:", attr)

    #def handle_endtag(self, tag):
    #    print("End tag  :", tag)

    def parseColourToString(self, x):
        if x == "#6d9eeb":
            return "Lightning"
        elif x == "#dd7e6b":
            return "Bleeding"
        elif x == "#93c47d":
            return "Poison"
        elif x == "#ff9900":
            return "Fire"
        elif x == "#b7b7b7":
            return "Falling"
        elif x == "#ffe599":
            return "Telekinetic"
        elif x == "#ffff00":
            return "Radiant"
        elif x == "#736941":
            return "Necrotic"
        elif x == "#b4a7d6":
            return "Psychic"
        elif x == "#9fc5e8":
            return "Ice"
        elif x == "#00ff00":
            return "Acid"
        elif x == "#c27ba0":
            return EDamageTypes[11]
        else:
            return "Physical"

    def handle_char(self, data, x):
        # Handle Output to CSV
        if x not in self.registeredCharacters:
            self.registeredCharacters.append(x)

        if x == data and x not in self.characters:
            print(data + " found at r: " + str(self.row) + " c: " + str(self.column))
            self.characters[x] = [self.column, self.row, {}, {}, {}];

    def handle_damageTrans(self,data):
        if self.readStyle == True:
            css = list(filter(lambda a: a != '', re.split('{|\.|;|:|\n| |\\\\n\'b\'|\\\\n\"b\'|\\\\n\'b\"', data)))

            #print(css)

            for indexer in range(0,len(css)):
                if(css[indexer] == "ritz"):
                    if(css[indexer + 1] == "waffle"):
                        ident = css[indexer + 2];
                        bgcolour = ""
                        # find background colour
                        for nindexer in range(indexer + 2, len(css)):
 
                            if(css[nindexer] == "background-color"):
                                bgcolour = css[nindexer + 1]
                            elif css[nindexer] == "}":
                                break

                        #print(ident + " " + bgcolour)

                        if not bgcolour == "":
                            parseColour = self.parseColourToString(bgcolour);
                            if parseColour not in self.damageMap:
                                self.damageMap[parseColour] = [ident]
                            else:
                                self.damageMap[parseColour].append(ident)
                        
                        

            self.readStyle = False;
        #    parser = tinycss.make_parser('page3')
        #    ss = parser.parse_stylesheet(data)
        #    for each in ss.rules:
        #        print(each.selector.as_css());
        #        print(each.declarations)





    def handle_data(self, data):
        #print("Data     :", data)
        self.handle_damageTrans(data)

        self.handle_char(data, "Vex")
        self.handle_char(data, "Trinket")
        self.handle_char(data, "Vax")
        self.handle_char(data, "Grog")
        self.handle_char(data, "Keyleth")
        self.handle_char(data, "Percy")
        self.handle_char(data, "Scanlan")
        self.handle_char(data, "Pike")
        self.handle_char(data, "Tiberius")
        self.handle_char(data, "Taryon")
        self.handle_char(data, "Doty")
        self.handle_char(data, "Tova")

        localDamageType = ""
        for dTypes in self.damageMap:
            #print(dTypes)
            for each in self.damageMap[dTypes]:
                #print(each)
                if self.damageType == each:
                    localDamageType = dTypes;

        for element in self.characters:    
            if self.column == self.characters[element][0] and self.row > self.characters[element][1] + 2:
                try:
                    nDat = int(data);
                    #print(str(nDat))
                    if(localDamageType in self.characters[element][2]):
                        self.characters[element][2][localDamageType] += nDat;
                        self.characters[element][3][localDamageType] += 1;
                        self.characters[element][4][localDamageType].append(nDat);
                    else:
                        self.characters[element][2][localDamageType] = nDat;
                        self.characters[element][3][localDamageType] = 1;
                        self.characters[element][4][localDamageType] = [nDat];
                except ValueError as e:
                    break
                except:
                    raise
                

#    def handle_comment(self, data):
#        ## Make this identify the player indices
#        print("Comment  :", data)
#
#    def handle_entityref(self, name):
#        c = unichr(name2codepoint[name])
#        print("Named ent:", c)
#
#    def handle_charref(self, name):
#        if name.startswith('x'):
#            c = unichr(int(name[1:], 16))
#        else:
#            c = unichr(int(name))
#        print("Num ent  :", c)
#
#    def handle_decl(self, data):
#        print("Decl     :", data)

    def close(self):
        print(self.characters)
        #print(self.damageMap)
        print(self.x)

        with open("ParsedDamageTaken/" + self.x + ".csv", "w") as outf:
            # Generate line header
            header = "Character,"

            for damageType in EDamageTypes:
                header += damageType + ","
            
            for damageType in EDamageTypes:
                header += damageType + "Instances,"

            for damageType in EDamageTypes:
                header += damageType + "InstVals,"

            outf.write(header + "\n")
            
            for toon in self.registeredCharacters:
                # Building string
                lineout = toon + ","

                if toon not in self.characters:
                  for i in EDamageTypes:
                      lineout += "0,0,0,"  

                else:
                    # Damage Taken
                    for damageType in EDamageTypes:
                        if damageType in self.characters[toon][2]:
                            #print(toon + " " + damageType + str(self.characters[toon][2][damageType]))
                            lineout += str(self.characters[toon][2][damageType])
                        else:
                            lineout += "0"

                        lineout += ","

                    for timesTaken in EDamageTypes:
                        if timesTaken in self.characters[toon][3]:
                            lineout += str(self.characters[toon][3][timesTaken])
                        else:
                            lineout += "0"

                        lineout += ","

                    for dtypes in EDamageTypes:
                        if dtypes in self.characters[toon][4]:
                            lineout += "\""
                            for instances in self.characters[toon][4][dtypes]:
                                #print("inst: " + str(instances))
                                lineout += str(instances) + ","
                            lineout += "0\""
                        else:
                            lineout += "\"0\""
                        lineout += ","  
                outf.write(lineout + "\n")

        super(TakenDamageParser, self).close()


def process_file(root, x):
    #if not x == "1.html" and not x == "5.html" and not x == "33.html":
    #    return
    print("Processing file: " + str(x))
    with open(root + x, "rb") as f:
        localParser = TakenDamageParser(x);
        localLines = f.readlines();
        strInput = ''.join(str(e) for e in localLines)
        localParser.feed(strInput);
        localParser.close()
        




# Enumerate the folder
damageTakens = []
rootDirectory = "./DamageTaken/"
for (dirpath, dirnames, filenames) in walk(rootDirectory):
    damageTakens.extend(filenames)


for singleFile in damageTakens:
    process_file(rootDirectory, singleFile)
