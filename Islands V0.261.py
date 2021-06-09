# For licencing, check LICENCE file.

import os
import SaveLoadEngine
import re
import random
resources_loader = SaveLoadEngine.SaveLoadEngine(os.getcwd() + "\\Islands_resources", "Islands_resources")

class Islands:
    class Character:
        def __init__(self, xpos, ypos, save_engine):
            self.xpos = xpos
            self.ypos = ypos
            self.inventory = save_engine.safe_load("player_inventory", [{"name": "wooden axe", "type": "axe", "specific type": "wooden axe", "worktime": 30, "durability" : 100, "stackable": False},
                              {"name": "iron axe", "type": "axe", "specific type": "iron axe", "worktime": 5,"stackable": False, "durability": 100}])
            self.hunger = 100
            self.thirst = 100
            self.energy = 100

    def __init__(self):
        self.save_engine = None
        self.time_in_minutes = None
        self.time_in_text = ""
        self.world = None
        self.world_data = []
        self.current_location = ""
        self.current_biome = ""
        self.player = None
        self.load_variables()
        self.random_staff = resources_loader.load("random_staff")
        self.first_play = None
        #print(self.random_staff)
        #self.set_world_data()

    def load_variables(self):
        self.save_engine = SaveLoadEngine.SaveLoadEngine(
            os.getcwd() + "\\Islands_save", "Islands_save")
        self.time_in_minutes = self.save_engine.safe_load("minutes", 720)
        self.world = self.save_engine.safe_load("world", self.generate_world(7))
        ypos = self.save_engine.safe_load("player_ypos", 3)
        xpos = self.save_engine.safe_load("player_xpos", 3)
        self.player = self.Character(xpos, ypos, self.save_engine)
        self.player.hunger = self.save_engine.safe_load("player_hunger", 100)
        self.player.thirst = self.save_engine.safe_load("player_thirst", 100)
        self.player.energy = self.save_engine.safe_load("player_energy", 100)

    def save_game(self):
        self.save_engine.save(self.world_data, "world_data")
        self.save_engine.save(self.player.inventory, "player_inventory")
        self.save_engine.save(self.time_in_minutes, "minutes")
        self.save_engine.save(self.player.ypos, "player_ypos")
        self.save_engine.save(self.player.xpos, "player_xpos")
        self.save_engine.save(self.player.hunger, "player_hunger")
        self.save_engine.save(self.player.thirst, "player_thirst")
        self.save_engine.save(self.player.energy, "player_energy")



    def calculate_time(self, minutes_from_0):
        while minutes_from_0 > 1440:
            minutes_from_0 -= 1440
        time = ""
        hours = int(minutes_from_0 / 60)
        minutes = minutes_from_0 % 60
        if hours < 10:
            time += "0"
        time += str(hours) + ":"
        if minutes < 10:
            time += "0"
        time += str(minutes)
        return time

    def update_time(self, add_time=0, ):
        self.time_in_minutes += add_time
        self.time_in_text = self.calculate_time(self.time_in_minutes)

    def generate_world(self, island_size):
        island_shape = []
        for y in range(island_size):
            island_shape.append([])
            for x in range(island_size):
                ocean = False
                if (y == 0 and x == 0) or (y == 6 and x == 0) or (y == 0 and x == 6) or (y == 6 and x == 6):
                    island_shape[y].append(0)
                    ocean = True
                elif y == 0 or x == 0 or y == island_size - 1 or x == island_size - 1:
                    chance = random.randint(0, 100)
                    if chance <= 75:
                        island_shape[y].append(0)
                        ocean = True
                if not ocean:
                    island_shape[y].append(random.randint(1, 4))
        return island_shape

    def show_map(self, full_map):
        string = "   "
        for i in range(len(self.world)):
            string += str(i) + " "
        print(string)
        print("-" * 16)
        num = 0
        for y in range(len(self.world)):
            string = str(num) + ") "
            for x in range(len(self.world[y])):
                if self.world_data[y][x]["Discovered"] is True:
                    string += str(self.world[y][x])
                else:
                    string += "?"
                string += "|"
            print(string)
            num += 1
        print("Your location: x=" + str(self.player.xpos), ", y=" + str(self.player.ypos))
        print("Map legend:")
        print("0 = ocean, 1 = forest, 2 = hills, 3 = plains, 4 = lake, ? = unknown")

    def update_variables(self):
        #self.current_location = self.world_data[self.player.ypos][self.player.xpos]["Biome"]
        self.current_biome = self.world_data[self.player.ypos][self.player.xpos]["Biome"]
        self.world_data[self.player.ypos][self.player.xpos]["Discovered"] = True

    def set_world_data(self):
        if self.save_engine.load("world_data") is not None:
            self.world_data = self.save_engine.load("world_data")
            return None
        world = self.world
        self.world_data = []
        for y in range(len(world)):
            self.world_data.append([])
            for x in self.world[y]:
                if x == 0:
                    self.world_data[y].append({"Discovered": False, "Biome": "Ocean", "Name": None,
                                               "Treasures": random.randint(2, 5)})
                elif x == 1:
                    self.world_data[y].append(
                        {"Discovered": False, "Biome": "Forest", "Name": None, "Trees": random.randint(5, 25)})
                elif x == 2:
                    self.world_data[y].append({"Discovered": False, "Biome": "Hills", "Name": None,
                                               "Caves": random.randint(2, 5)})
                elif x == 3:
                    self.world_data[y].append({"Discovered": False, "Biome": "Plains", "Name": None})
                elif x == 4:
                    self.world_data[y].append({"Discovered": False, "Biome": "Lake", "Name": None})
        self.save_engine.save(self.world_data, "world_data")

    def analyze_input(self, user_input):
        user_input.lower()
        input_array = user_input.split()
        if input_array[0] == ("exit" or "quit"):
            return "exit"
        elif (("chop" or "cut") and "tree") in user_input:
            return "chop a tree"
        elif "map" in user_input:
            return "show map"
        elif "go " in user_input:
            for i in range(len(input_array)):
                if input_array[i] == "go" and len(input_array) > i:
                    if input_array[i + 1] == "north":
                        return "go north"
                    elif input_array[i + 1] == "south":
                        return "go south"
                    elif input_array[i + 1] == "west":
                        return "go west"
                    elif input_array[i + 1] == "east":
                        return "go east"
            print("In the next time write where do you want to go")
        elif ("inventory" in user_input) or "backpack" in user_input:
            return "show inventory"
        elif "map" in user_input:
            return "show map"
        elif input_array[0] == "search" or "look":
            if len(input_array) > 1:
                if input_array[1] == "for":
                    del(input_array[1])
                if input_array[1] == "food":
                    return "search for food"
                elif input_array[1] == "water":
                    return "look for water"
                elif input_array[1] == "random":
                    return "look for random staff"
                else:
                    print("In the next time write what do you want to find.")
        else:
            return "unknown"

    def item_type_exist(self, item_type):
        for item in self.player.inventory:
            if item["type"] == item_type:
                return True
        return False

    def get_items_by_type(self, item_type):
        items = []
        for item in self.player.inventory:
            if item["type"] == item_type:
                items.append(item)
        return items

    def count_items_by_type(self, item_type):
        count = 0
        for item in self.player.inventory:
            if item["type"] == item_type:
                count += 1
        return count

    def find_item_index_by_name(self, name):
        for i in range(len(self.player.inventory)):
            if self.player.inventory[i]["name"] == name:
                return i

    def hard_work(self, worktime):
        self.update_time(worktime)
        self.player.hunger -= int(worktime / 3)
        self.player.thirst -= int(worktime / 3)
        self.player.energy -= int(worktime / 3)

    def normal_work(self, worktime):
        self.update_time(worktime)
        self.player.hunger -= int(worktime / 6)
        self.player.thirst -= int(worktime / 6)
        self.player.energy -= int(worktime / 6)

    def easy_work(self, worktime):
        self.update_time(worktime)
        self.player.hunger -= int(worktime / 10)
        self.player.thirst -= int(worktime / 10)
        self.player.energy -= int(worktime / 10)

    def look_for_water(self):
        if self.world_data[self.player.ypos][self.player.xpos]["Biome"] == "Lake":
            self.update_time(2)
            self.player.thirst = 100
            print("It took you 2 minutes to find a lake (you are in lake biome). you drinked from it and now your "
                  "thirst bar is full")

    def chop_a_tree(self, tile_info):
        if tile_info["Biome"] == "Forest" and self.item_type_exist("axe"):
            if tile_info["Trees"] > 0:
                if self.count_items_by_type("axe") > 0:
                    if self.count_items_by_type("axe") > 1:
                        print("Choose an axe to work with:")
                        axes = self.get_items_by_type("axe")
                        for i in range(len(axes)):
                            axe = axes[i]
                            print(str(i + 1) + ") " + axe["name"] + " (" + str(axe["worktime"]) + " minutes)")
                        while True:
                            inp = input().strip()
                            if is_int(inp):
                                num = int(inp)
                                if is_valid_number(num, 1, len(axes)):
                                    axe = axes[num - 1]
                                    break
                            print("Please choose")
                    else:
                        axe = self.get_items_by_type("axe")[0]
                    self.world_data[self.player.ypos][self.player.xpos]["Trees"] -= 1
                    worktime = self.player.inventory[self.find_item_index_by_name(axe["name"])]["worktime"]
                    self.hard_work(worktime)
                    if axe["specific type"] == "wooden axe":
                        self.player.inventory[self.find_item_index_by_name(axe["name"])]["durability"] -= 25
                    elif axe["specific type"] == "stone axe":
                        self.player.inventory[self.find_item_index_by_name(axe["name"])]["durability"] -= 10
                    elif axe["specific type"] == "iron axe":
                        self.player.inventory[self.find_item_index_by_name(axe["name"])]["durability"] -= 5
                    item = self.find_item_index_by_name("log")
                    logs_added = random.randint(2, 5)
                    if item is not None:
                        self.player.inventory[self.find_item_index_by_name("log")]["quantity"] += logs_added
                    else:
                        self.player.inventory.append({"name": "log", "type": "log", "quantity": logs_added, "stackable": True})
                    print("You cut down a tree with your " + axe["name"] + " and received " + str(logs_added) + " logs. It took you " + str(
                        worktime) + " minutes.")
                    if axe["durability"] < 5:
                        print("Your axe reached the minimum durability and broken")
                        del(self.player.inventory[self.find_item_index_by_name(axe["name"])])
                else:
                    print("You don't have any axe in your inventory")
            else:
                print("You are in Forest biome but you already cutted down all of the trees.")
        else:
            print("You must be in Forest biome to cut down trees")

    def look_for_random(self):
        worktime = None
        print("How long do you want to do this action? (in minutes)")
        while True:
            try:
                worktime = int(input())
                if is_valid_number(worktime, 1, 300):
                    break
                else:
                    print("The number that you entered is too big/ small. try again.")

            except:
                print("Please enter a number.")
        self.easy_work(worktime)
        staff = []
        result = []
        print(self.random_staff)
        for item in self.random_staff:
            quantity = random.randint(item["minimum"], item["maximum"])
            for i in range(quantity):
                staff.append({"name": item["name"], "frequency": item["frequency"]})
        staff = random_list(staff)
        for i in range(worktime):
            if i <= len(staff):
                chance = random.randint(1, 100)
                if chance <= item["frequency"]:
                    result.append(staff[i]["name"])
            else:
                break
        print(result)
        print_list(result)

    def game_tab(self):
        self.update_variables()
        print("Time: " + self.time_in_text, "|| Current Biome: " + self.current_biome + " || Hunger: "
              + str(self.player.hunger) + " || Thirst: " + str(self.player.thirst) + " || Energy: " + str(self.player.energy))
        print("What do you want to do now? (Enter help for help)")
        player_input = re.sub(" +", " ", input().strip())
        result = self.analyze_input(player_input)
        tile_info = self.world_data[self.player.ypos][self.player.xpos]
        last_ypos = self.player.ypos
        last_xpos = self.player.xpos
        player_moved = False
        if result == "exit":
            exit(0)
        elif result == "chop a tree":
            self.chop_a_tree(tile_info)
        elif result == "show inventory":
            self.show_inventory()
        elif result == "show map":
            self.show_map(False)
        elif result == "go north":
            if self.player.ypos >= 1:
                self.player.ypos -= 1
                player_moved = True
            else:
                print("You can't go there")
        elif result == "go south":
            if self.player.ypos <= 5:
                self.player.ypos += 1
                player_moved = True
            else:
                print("You can't go there")
        elif result == "go west":
            if self.player.xpos >= 1:
                self.player.xpos -= 1
                player_moved = True
            else:
                print("You can't go there")
        elif result == "go east":
            if self.player.xpos <= 5:
                self.player.xpos += 1
                player_moved = True
            else:
                print("You can't go there")
        elif result == "look for water":
            self.look_for_water()
        elif result == "look for random staff":
            self.look_for_random()
        else:
            print("Unknown")
        if player_moved:
            if self.world_data[last_ypos][last_xpos]["Biome"] == 4:
                self.normal_work(15)
            else:
                self.easy_work(10)
        self.save_game()

    def show_inventory(self):
        print("\nInventory:")
        for item in self.player.inventory:
            if item["stackable"] is True:
                print(str(item["quantity"]) + " " + item["name"] + "s")
            else:
                result = item["name"]
                #if "durability" in item.keys():
                    #result += " (durability " + str(item["durability"]) + ")"
                #print(result)
                if "durability" in item:
                    print_bar(item["durability"])

    def run_game(self):
        self.update_time(0)
        self.set_world_data()
        while True:
            self.game_tab()


def clear_shell():
    print("\n" * 100)


def is_int(string):
    try:
        int(string)
        return True
    except:
        return False


def is_valid_number(var, mini, maxi):
    try:
        if var >= mini and var <= maxi:
            return True
    finally:
        pass
    return False


def get_random_item(lst):
    return lst[random.randint(0, len(lst) - 1)]


def random_list(lst):
    result = []
    range_ = list(range(0, len(lst)))
    for i in range(len(lst)):
        num = get_random_item(range_)
        result.append(lst[num])
        range_.remove(num)
    return result


def print_list(lst):
    for i in range(len(lst)):
        print(str(i + 1) + ") " + lst[i])


def choose_list_element(lst):
    print_list(lst)
    while True:
        inp = input().strip()
        if is_int(inp):
            if is_valid_number(0, len(lst)):
                return int(inp)
        print("Please choose.")

def print_bar(percent):
    """
    percent is number 0-100
    """
    full=percent//10+(1 if percent%10>=5 else 0)
    empty=10-full
    print('#'*full+'-'*empty)
    
game = Islands()
game.run_game()



