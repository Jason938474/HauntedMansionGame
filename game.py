
# "h" indicates a room in the house
themap = {
    "Car": {"n": "Front Door", "e": "Car Trunk", "h":False},
    "Car Trunk": {"w": "Car", "n": "Front Door", "h":False},
    "Front Door": {"s": "Car", "w": "Garden Shed", "h":False},
    "Garden Shed" : {"e": "Front Door", "h":False},
    "Entryway" : {"s":"Front Door", "e": "Great Room", "w": "Library", "h":True},
    "Great Room" : {"w": "Entryway", "h":True},
    "Library" : {"e": "Entryway", "n": "Kitchen", "h":True},
    "Kitchen" : {"s": "Library", "h": True }
}

items = {
    "Car Trunk": ["Car Jack", "Water Bottle"],
    "Garden Shed": ["Old Key", "Firewood"],
    "Kitchen": ["Matches"]
}

desc = {
    "Car": "You are in your car. The rain pelts the glass and you sit shivering.  It will not start since you ran out of gas",
    "Car Trunk": "You are in the back of the car near the trunk.  The rain pelts you",
    "Front Door": "You stand on the rickety front porch of the old house.  It's obvious that this structure is a shadow of it's former self.\nThrough the bushes to the west, you see what looks like a small shed",
    "Entryway": "You are in the entryway of the old mansion",
    "Great Room": "This is the front room of the mansion where guests would wait. \nThe furniture is arranged around an enormous fireplace, which dominates the room\nThis huge fireplace was obviously designed to heat the entire house",
    "Library": "This looks to be a library.  Old booksheves line the walls completely and the books are starting to fall apart",
    "Garden Shed": "You are in a small garden shed. It's very dusty in here. The cheap walls are covered in spiderwebs and it smells like mildew",
    "Kitchen": "You are in a kitchen with large marble countertops, an old fashioned icebox, and an old, broken stove.\nThe window overlooks the backyard and through the mist you can see the vague outlines of gravestones"
}

inv = ["Cellphone"]

class playerClass:
    def __init__(self):
        self.location = "Car"
        self.coldness = 0
        self.remainingWater = 4
        
player = playerClass()

coldLevels = {0:"warm", 4:"somewhat cold", 8:"uncomfortably cold", 12:"freezing", 16:"painfully cold", 20:"very numb all over your body"}
coldLocations = []

# all possible directions north south east west up down
dirs = {'n':"North",'s':"South",'e':"East",'w':"West",'u':"Up",'d':"Down"}

def main():

    #init all locations to be cold
    for nxt in themap:
        coldLocations.append(nxt)

    print("After driving in the rain on a lonely road, your car has run out of gas");
    print("Luckily, you were able to turn off the road into what looks like an abandonded old home");
    print("Your job is to find a way to get back home\n");

    while True:
        describeRoom()
        coldCheck()
                
        while True: 
            cmd = input("\nWhat do you want to do? ")
            cmd = normalize(cmd)
            if cmd == "":
                continue
            if cmd in dirs:
                if not cmd in themap[player.location] :
                    print("\n*****You cannot go that way******")
                    continue
                else:
                    #print(f"\nYou have travelled {dirs[cmd]}...")
                    player.location = themap[player.location][cmd]
                    break
            
            if cmd == "i": 
                print(f"Your inventory is: {inv}");
                continue
            
            if cmd == 'quit':
                print("Thank you for playing, good bye!")
                quit()

            if cmd == 'l':
                describeRoom()
                continue
            
            # Complex command - split into 2 pieces if possible
            try :
                verb, obj = cmd.split(" ", 1)
                obj = obj.title();
            except :
                ## We get here if split fails or anything else goes wrong
                print("I do not understand your command, please try again")
                continue

            if verb == 'get' or verb == "take":
               take(obj)
            elif verb == 'drop':
                drop(obj)
            elif verb == 'use':
                use(obj)
            else:
                print("I do not understand your command, please try again")
                                

def use(obj):
    
    if obj not in inv:
        print(f"You don't have a {obj}");
        return

    ## From here we don't need to check in inventory
    
    if obj.startswith("Cellphone"):
        print("You try to use the cellphone but the battery is dead and it doesn't turn on. \nYou will have to charge it before you can do anything else")
        return

    if obj == "Old Key" and player.location == "Front Door" :
        print("You try the old key on the front door and with a satisfying *click*, the lock opens and you can enter the house")
        themap["Front Door"]["n"] = "Entryway"
        return

    if obj == "Water Bottle":
        if player.remainingWater > 0:
            print("You take a refreshing drink")
            player.remainingWater = player.remainingWater - 1
            return
        else:
            print("The water bottle is empty")
            return

    if obj == "Matches" and player.location != "Great Room" :
        print("You strike the match and watch the flame brighten but then go out")
        return

    if player.location == "Great Room" :
        if obj == "Firewood" and "Matches" not in inv :
            print("You might be able to burn the firewood if you had something to light the wood with")
        elif obj == "Matches" and "Firewood" not in inv :
            print("As you strike a match, your eye drifts to the large fireplace in this room.  It was obviously designed to heat the house.  If you only had something to burn...")
        elif (obj == "Firewood" and "Matches" in inv) or (obj == "Matches" and "Firewood" in inv):
            print("You stack the firewood into the huge fireplace and light the match.  Soon the fire burns cheerily and starts to warm the entire house")
            inv.remove("Firewood")
            # Make the whole house warm
            for loc in themap:
                if themap[loc]["h"] == True :
                    #print(f"Removing {loc} from cold Location")
                    coldLocations.remove(loc)
        return
        
    print(f"I don't know how to use {obj}")

def take(obj):
    if player.location in items and obj in items[player.location] :
        print(f"You pick up {obj}...");
        items[player.location].remove(obj)
        inv.append(obj)
    else:
        print(f"You dont see any {obj} here")
        
def drop(obj):
    if obj not in inv :
        print(f"You do not have a {obj}");
        return
    
    print(f"You drop the {obj}");
    inv.remove(obj)
    if player.location not in items :
        items[player.location] = []
    items[player.location].append(obj)
    
def describeRoom():
    print(f"\n**** {player.location} ****")
    print(f"{desc[player.location]}")

    printExtraText()
    
    if player.location in items and len(items[player.location]) > 0 :
        print(f"\nYou see the following items here: {items[player.location]}");

    print("\nPossible Directions are as follows:")
    for d in dirs.keys() :
        if d in themap[player.location]:
            print(f"{dirs[d]} leads to {themap[player.location][d]}")
    print("")


def coldCheck() :
    if player.location in coldLocations:
        player.coldness = player.coldness + 1
        if player.coldness == max(coldLevels) :
            print("The cold numbs you deeply and forces you to stumble and fall. You have frozen to death.")
            quit()
        elif player.coldness in coldLevels :
            print(f"You are getting colder and now feel {coldLevels[player.coldness]}\n")
    elif player.coldness > 1 :
        player.coldness = player.coldness - 1
        print(f"This is a warm location - you are warming up")
    elif player.coldness == 1 :
        player.coldness = 0
        print(f"You are now completely warm")

        
def printExtraText() :
    # any conditonal descriptive text goes here
    if player.location == "Front Door" and "n" not in themap["Front Door"] :
        print("\nThis front door looks very stout and solidly locked.  If only you had a key...");

    
def normalize(cmd) :
    cmd = cmd.lower()
    if cmd == "north":
        return "n"
    if cmd == "east":
        return "e"
    if cmd == "west":
        return "w"
    if cmd == "south":
        return "s"
    if cmd == "quit" or cmd == "bye" or cmd == "exit":
        return "quit"
    if cmd == "inventory" or cmd == "inv" or cmd == "i":
        return "i"
    if cmd == "look" or cmd == "examine":
        return "l"
    return cmd
            
if __name__ == "__main__":
    main()        
    

