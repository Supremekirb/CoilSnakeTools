import click
import glob
import os
import yaml
from PIL import Image

def makeAnims(path, output):
    try:
        with open(f'{path}\\Animations\\animations.yml') as file:
            animations = yaml.safe_load(file)
    except:
        click.echo(f"Failed to open {path}\\Animations\\animations.yml")
        return
    
    for i in range(0, len(animations)):
        frames = [Image.open(image) for image in glob.glob(f"{path}\\Animations\\{i}\\*.png")]
        base = frames[0]
        base.save(f'{output}\\anim{i}.gif', save_all=True, append_images=frames, duration=int(16.666666666666668*animations[i]["unknown"]), loop=0) # I assume unknown is speed..? probably not but it looks about right
    click.echo(f"Saved animation gifs to {output}")

def makeSwirls(path, output):
    try:
        with open(f'{path}\\Swirls\\swirls.yml') as file:
            swirls = yaml.safe_load(file)
    except:
        click.echo(f"Failed to open {path}\\Swirls\\swirls.yml")
        return
    
    for i in range(1, len(swirls)):
        frames = [Image.open(image) for image in glob.glob(f"{path}\\Swirls\\{i}\\*.png")]
        base = frames[0]
        base.save(f'{output}\\swirl{i}.gif', save_all=True, append_images=frames, duration=int(16.666666666666668*swirls[i]["speed"]), loop=0) 
    click.echo(f"Saved swirl gifs to {output}")

def makeTownMaps(path, output):
    try:
        with open(f'{path}\\TownMaps\\icon_positions.yml') as file:
            icon_positions = yaml.safe_load(file)
    except:
        click.echo(f"Failed to open {path}\\TownMaps\\icon_positions.yml")
        return

    mapIcons = Image.open(f"{path}\\TownMaps\\icons.png").convert("RGBA")
    icons_loaded = mapIcons.load()
    width, height = mapIcons.size # convert the two BG colours to transparency
    for y in range(height):
        for x in range(width):
            if icons_loaded[x, y] == (0, 0, 0, 255) or icons_loaded[x, y] == (0, 0, 248, 255):
                icons_loaded[x, y] = (255, 255, 255, 0)

    mapIcons_Cropped = {
        "mapIcon_TwosonWest" : mapIcons.crop((0, 0, 48, 24)),
        "mapIcon_DesertEast" : mapIcons.crop((48, 0, 96, 24)),
        "mapIcon_FoodBurger" : mapIcons.crop((96, 0, 128, 24)),

        "mapIcon_DesertWest" : mapIcons.crop((0, 24, 48, 48)),
        "mapIcon_Hospital" : mapIcons.crop((48, 24, 88, 48)),
        "mapIcon_DeptStore" : mapIcons.crop((88, 24, 128, 48)),

        "mapIcon_TwosonSouth" : mapIcons.crop((0, 48, 40, 72)),
        "mapIcon_Threed" : mapIcons.crop((40, 48, 80, 72)),
        "mapIcon_Toto" : mapIcons.crop((80, 48, 120, 72)),
        "mapIcon_Bus" : mapIcons.crop((120, 48, 128, 56)),

        "mapIcon_FoodBakery" : mapIcons.crop((0, 72, 32, 96)),
        "mapIcon_FoodRestaurant" : mapIcons.crop((32, 72, 64, 96)),
        "mapIcon_Hint" : mapIcons.crop((64, 72, 88, 96)),
        "mapIcon_Onett" : mapIcons.crop((96, 72, 128, 88)),

        "mapIcon_Hotel" : mapIcons.crop((96, 88, 120, 112)),

        "mapIcon_Shop" : mapIcons.crop((0, 96, 24, 120)),
    }

    def layerIcons(map, i): # defs inside defs? this is what happens when you're lazy and copy over code from other projects like I do
        """Puts town map icons on maps"""
        for icon in icon_positions[i]: 
            match icon["Icon"]: 
                case "west to twoson":
                    iconToPlace = mapIcons_Cropped["mapIcon_TwosonWest"]
                case "east to desert":
                    iconToPlace = mapIcons_Cropped["mapIcon_DesertEast"]
                case "hamburger shop":
                    iconToPlace = mapIcons_Cropped["mapIcon_FoodBurger"]
                case "west to desert":
                    iconToPlace = mapIcons_Cropped["mapIcon_DesertWest"]
                case "hospital":
                    iconToPlace = mapIcons_Cropped["mapIcon_Hospital"]
                case "dept store":
                    iconToPlace = mapIcons_Cropped["mapIcon_DeptStore"]
                case "south to twoson":
                    iconToPlace = mapIcons_Cropped["mapIcon_TwosonSouth"]
                case "south to threed":
                    iconToPlace = mapIcons_Cropped["mapIcon_Threed"]
                #case "east to toto":
                #    iconToPlace = mapIcons_Cropped["mapIcon_Toto"]
                # unused? does not exist in icon_positions.yml
                case "bus stop":
                    iconToPlace = mapIcons_Cropped["mapIcon_Bus"]
                case "bakery":
                    iconToPlace = mapIcons_Cropped["mapIcon_FoodBakery"]
                case "restaurant":
                    iconToPlace = mapIcons_Cropped["mapIcon_FoodRestaurant"]
                case "hint":
                    iconToPlace = mapIcons_Cropped["mapIcon_Hint"]
                case "north to onett":
                    iconToPlace = mapIcons_Cropped["mapIcon_Onett"]
                case "hotel":
                    iconToPlace = mapIcons_Cropped["mapIcon_Hotel"]
                case "shop":
                    iconToPlace = mapIcons_Cropped["mapIcon_Shop"]
                case _:
                    print(f"Unrecognized icon name ({icon['Icon']})! This will not be shown on the map.")
                    break
            map.paste(iconToPlace, (icon["X"], icon["Y"]), mask=iconToPlace)
            map.save(f"{output}\\icons_{mapNames[i]}")

    # Generate a list of map filenames
    mapNames = [os.path.basename(map) for map in glob.glob(f'{path}/TownMaps/[!i]*')] # exclude *i*cons.png and *i*con_positions.yml. why arent these numbered
    # aaand it's out of order. let's fix that...
    mapNames = [mapNames[i] for i in [1, 5, 4, 0, 2, 3]] # this is so ugly ugh i should just initialise them manually        

    layerIcons(Image.open(f"{path}/TownMaps/Onett.png").convert("RGBA"), 0)
    layerIcons(Image.open(f"{path}/TownMaps/Twoson.png").convert("RGBA"), 1)
    layerIcons(Image.open(f"{path}/TownMaps/Threed.png").convert("RGBA"), 2)
    layerIcons(Image.open(f"{path}/TownMaps/Fourside.png").convert("RGBA"), 3)
    layerIcons(Image.open(f"{path}/TownMaps/Scaraba.png").convert("RGBA"), 4) # Scaraba comes before Summers for some reason
    layerIcons(Image.open(f"{path}/TownMaps/Summers.png").convert("RGBA"), 5)

    return


def getLevel(path, output): 
    try:
        with open(f'{path}\\exp_table.yml') as file:
            exp_table = yaml.safe_load(file)
    except:
        click.echo(f"Failed to open {path}\\exp_table.yml")
        return
    
    try:
        with open(f'{path}\\stats_growth_vars.yml') as file:
            stats_growth_vars = yaml.safe_load(file)
    except:
        click.echo(f"Failed to open {path}\\stats_growth_vars.yml")
        return

    with open(f'{output}\\LevelDump.txt', 'w') as out:
        out.write("""EarthBound level stat dump - Generated by CoilSnakeTools\n""")
        for char in range(0, 4):
            out.write(f"\n===== Character {char} =====\n")
            for level in range(1, 100):
                # Code from EB data bot below:

                # Starmen.net:
                # Stat gain = ((growth rate * old level) - ((stat-2) * 10)) * r/50 
                # r is given by one of the following:
                # * If the stat is vitality or IQ, and the new level is 10 or lower, r=5.
                # * Otherwise, if the new level is divisible by 4, r is a random number from 7 to 10.
                # * Otherwise, r is a random number from 3 to 6.
                #
                # HP and PP are based on vitality and IQ respectively. 
                # HP tries to increase to 15vitality, and PP tries to increase to 5IQ normally or 10*IQ for Ness after Magicant. 
                # If either of these results in a gain of less than 2, 
                # the stat instead gains by a random number in the range 1-3 (HP) or 0-2 (PP).

                # Verified against ebsrc and this one level stat dump I found on gamefaqs

                maxOff=maxDef=maxSpd=maxGut=maxLuc=maxVit=maxIQ=2 # i hate this so much AAAA
                maxHP=maxPP=2
                minOff=minDef=minSpd=minGut=minLuc=minVit=minIQ=2
                minHP=minPP=2

                for i in range(1, level+1): # calc worst possible stats
                    if i == 1:
                        minOff = minOff + (((stats_growth_vars[char]['Offense']*(i)) - ((minOff-2)*10)) * 7/50)
                        minDef = minDef + (((stats_growth_vars[char]['Defense']*(i)) - ((minDef-2)*10)) * 7/50)
                        minSpd = minSpd + (((stats_growth_vars[char]['Speed']*(i)) - ((minSpd-2)*10)) * 7/50)
                        minGut = minGut + (((stats_growth_vars[char]['Guts']*(i)) - ((minGut-2)*10)) * 7/50)
                        minLuc = minLuc + (((stats_growth_vars[char]['Luck']*(i)) - ((minLuc-2)*10)) * 7/50)
                        minVit = minVit + (((stats_growth_vars[char]['Vitality']*(i)) - ((minVit-2)*10)) * 5/50)
                        minIQ = minIQ + (((stats_growth_vars[char]['IQ']*(i)) - ((minIQ-2)*10)) * 5/50)

                    elif i%4 == 0:
                        minOff = minOff + (((stats_growth_vars[char]['Offense']*(i-1)) - ((minOff-2)*10)) * 7/50)
                        minDef = minDef + (((stats_growth_vars[char]['Defense']*(i-1)) - ((minDef-2)*10)) * 7/50)
                        minSpd = minSpd + (((stats_growth_vars[char]['Speed']*(i-1)) - ((minSpd-2)*10)) * 7/50)
                        minGut = minGut + (((stats_growth_vars[char]['Guts']*(i-1)) - ((minGut-2)*10)) * 7/50)
                        minLuc = minLuc + (((stats_growth_vars[char]['Luck']*(i-1)) - ((minLuc-2)*10)) * 7/50)
                        if i <= 10:
                            minVit = minVit + (((stats_growth_vars[char]['Vitality']*(i-1)) - ((minVit-2)*10)) * 5/50)
                            minIQ = minIQ + (((stats_growth_vars[char]['IQ']*(i-1)) - ((minIQ-2)*10)) * 5/50)
                        else: 
                            minVit = minVit + (((stats_growth_vars[char]['Vitality']*(i-1)) - ((minVit-2)*10)) * 7/50)
                            minIQ = minIQ + (((stats_growth_vars[char]['IQ']*(i-1)) - ((minIQ-2)*10)) * 7/50)
                            
                    else:
                        minOff = minOff + (((stats_growth_vars[char]['Offense']*(i-1)) - ((minOff-2)*10)) * 3/50)
                        minDef = minDef + (((stats_growth_vars[char]['Defense']*(i-1)) - ((minDef-2)*10)) * 3/50)
                        minSpd = minSpd + (((stats_growth_vars[char]['Speed']*(i-1)) - ((minSpd-2)*10)) * 3/50)
                        minGut = minGut + (((stats_growth_vars[char]['Guts']*(i-1)) - ((minGut-2)*10)) * 3/50)
                        minLuc = minLuc + (((stats_growth_vars[char]['Luck']*(i-1)) - ((minLuc-2)*10)) * 3/50)
                        if i <= 10:
                            minVit = minVit + (((stats_growth_vars[char]['Vitality']*(i-1)) - ((minVit-2)*10)) * 5/50)
                            minIQ = minIQ + (((stats_growth_vars[char]['IQ']*(i-1)) - ((minIQ-2)*10)) * 5/50)
                        else: 
                            minVit = minVit + (((stats_growth_vars[char]['Vitality']*(i-1)) - ((minVit-2)*10)) * 3/50)
                            minIQ = minIQ + (((stats_growth_vars[char]['IQ']*(i-1)) - ((minIQ-2)*10)) * 3/50)

                    minOff = int(minOff)
                    minDef = int(minDef)
                    minGut = int(minGut)
                    minIQ = int(minIQ)
                    minVit = int(minVit)
                    minSpd = int(minSpd)
                    minLuc = int(minLuc)

                    if minHP + (minVit * 15) < minHP + 2:
                        minHP = minHP + 1
                    else: minHP = (minVit * 15)
                    if minPP + (minIQ * 5) < minPP + 2:
                        minPP = minPP + 0
                    else: minPP = (minIQ * 5)

                    minHP = int(minHP)
                    minPP = int(minPP)

                for i in range(1, level+1): # calc best possible stats
                        if i == 1:
                            maxOff = maxOff + (((stats_growth_vars[char]['Offense']*(i)) - ((maxOff-2)*10)) * 10/50)
                            maxDef = maxDef + (((stats_growth_vars[char]['Defense']*(i)) - ((maxDef-2)*10)) * 10/50)
                            maxSpd = maxSpd + (((stats_growth_vars[char]['Speed']*(i)) - ((maxSpd-2)*10)) * 10/50)
                            maxGut = maxGut + (((stats_growth_vars[char]['Guts']*(i)) - ((maxGut-2)*10)) * 10/50)
                            maxLuc = maxLuc + (((stats_growth_vars[char]['Luck']*(i)) - ((maxLuc-2)*10)) * 10/50)
                            maxVit = maxVit + (((stats_growth_vars[char]['Vitality']*(i)) - ((maxVit-2)*10)) * 5/50)
                            maxIQ = maxIQ + (((stats_growth_vars[char]['IQ']*(i)) - ((maxIQ-2)*10)) * 5/50)

                        elif i%4 == 0:
                            maxOff = maxOff + (((stats_growth_vars[char]['Offense']*(i-1)) - ((maxOff-2)*10)) * 10/50)
                            maxDef = maxDef + (((stats_growth_vars[char]['Defense']*(i-1)) - ((maxDef-2)*10)) * 10/50)
                            maxSpd = maxSpd + (((stats_growth_vars[char]['Speed']*(i-1)) - ((maxSpd-2)*10)) * 10/50)
                            maxGut = maxGut + (((stats_growth_vars[char]['Guts']*(i-1)) - ((maxGut-2)*10)) * 10/50)
                            maxLuc = maxLuc + (((stats_growth_vars[char]['Luck']*(i-1)) - ((maxLuc-2)*10)) * 10/50)
                            if i <= 10:
                                maxVit = maxVit + (((stats_growth_vars[char]['Vitality']*(i-1)) - ((maxVit-2)*10)) * 5/50)
                                maxIQ = maxIQ + (((stats_growth_vars[char]['IQ']*(i-1)) - ((maxIQ-2)*10)) * 5/50)
                            else: 
                                maxVit = maxVit + (((stats_growth_vars[char]['Vitality']*(i-1)) - ((maxVit-2)*10)) * 10/50)
                                maxIQ = maxIQ + (((stats_growth_vars[char]['IQ']*(i-1)) - ((maxIQ-2)*10)) * 10/50)
                                
                        else:
                            maxOff = maxOff + (((stats_growth_vars[char]['Offense']*(i-1)) - ((maxOff-2)*10)) * 6/50)
                            maxDef = maxDef + (((stats_growth_vars[char]['Defense']*(i-1)) - ((maxDef-2)*10)) * 6/50)
                            maxSpd = maxSpd + (((stats_growth_vars[char]['Speed']*(i-1)) - ((maxSpd-2)*10)) * 6/50)
                            maxGut = maxGut + (((stats_growth_vars[char]['Guts']*(i-1)) - ((maxGut-2)*10)) * 6/50)
                            maxLuc = maxLuc + (((stats_growth_vars[char]['Luck']*(i-1)) - ((maxLuc-2)*10)) * 6/50)
                            if i <= 10:
                                maxVit = maxVit + (((stats_growth_vars[char]['Vitality']*(i-1)) - ((maxVit-2)*10)) * 5/50)
                                maxIQ = maxIQ + (((stats_growth_vars[char]['IQ']*(i-1)) - ((maxIQ-2)*10)) * 5/50)
                            else: 
                                maxVit = maxVit + (((stats_growth_vars[char]['Vitality']*(i-1)) - ((maxVit-2)*10)) * 6/50)
                                maxIQ = maxIQ + (((stats_growth_vars[char]['IQ']*(i-1)) - ((maxIQ-2)*10)) * 6/50)
                                
                        maxOff = int(maxOff)
                        maxDef = int(maxDef)
                        maxGut = int(maxGut)
                        maxIQ = int(maxIQ)
                        maxVit = int(maxVit)
                        maxSpd = int(maxSpd)
                        maxLuc = int(maxLuc)

                        if maxHP + (maxVit * 15) < maxHP + 2:
                            maxHP = maxHP + 3
                        else: maxHP = (maxVit * 15)
                        if maxPP + (maxIQ * 5) < maxPP + 2:
                            maxPP = maxPP + 2
                        else: maxPP = (maxIQ * 5)

                        maxHP = int(maxHP)
                        maxPP = int(maxPP)
                
                if char == 2: # Jeff does not earn PP
                    minPP=maxPP = 0
                
                out.write(f"Level {level}:\n")
                out.write(f"   {exp_table[char][f'Level {level:02d} EXP']} exp to reach\n")
                out.write(f"   HP: {minHP} - {maxHP}\n")
                out.write(f"   PP: {minPP} - {maxPP}\n")
                out.write(f"   Offense: {minOff} - {maxOff}\n")
                out.write(f"   Defense: {minDef} - {maxDef}\n")
                out.write(f"   Speed: {minSpd} - {maxSpd}\n")
                out.write(f"   Guts: {minGut} - {maxGut}\n")
                out.write(f"   Luck: {minLuc} - {maxLuc}\n")
                out.write(f"   Vitality: {minVit} - {maxVit}\n")
                out.write(f"   IQ: {minIQ} - {maxIQ}\n\n")
    click.echo(f"Wrote level stat dump to {output}\\LevelDump.txt.")
    return

@click.command()
@click.option('-p', '--path', type=str, default=os.getcwd(), help="Path of a CoilSnake project. If blank, uses the current directory.")
@click.option('-m', '--mode', 
               type=click.Choice(['anim', 'swirl', 'level', 'townmap', 'all'], case_sensitive=False), required=True, help="Function to execute.")
@click.option('-o', '--output', type=str, default=os.getcwd(), help="Output location. If blank, uses the current directory.")
def coilsnaketools(path, mode, output):
    # path = str of path
    # mode = anim / swirl / level / townmap / all (str)
    # output = str of path
    if not os.path.isdir(path):
        click.echo(f"{path} is not a valid path for input!")
        return

    if not os.path.isdir(output):
        click.echo(f"{output} is not a valid path for output!")
        return
    
    match(mode):
        case 'anim':
            makeAnims(path, output)
            return
        case 'swirl':
            makeSwirls(path, output)
            return
        case 'level':
            getLevel(path, output)
            return
        case 'townmap':
            makeTownMaps(path, output)
            return
        case 'all':
            makeAnims(path, output)
            makeSwirls(path, output)
            makeTownMaps(path, output)
            getLevel(path, output)
            return
        case _:
            click.echo("Something went horribly wrong. Try again.")


if __name__ == '__main__':
    coilsnaketools()