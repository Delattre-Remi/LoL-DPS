from Champion import Champion
from Target import Target
from Item import ITEM
from colorama import Fore, Back, Style

import random

DAMAGE_TARGET = True

def calculate(Champ : Champion, Dummy : Target, testTime : int = 200, rng = random.Random(0), verbose = 0) -> float:
    end_time = testTime
    current_time = 0
    total_damage = 0
    current_dps = 0
    sum_items_dmg = {}

    while end_time > current_time:
        Champ.update(current_time)
        
        # Auto Attack
        damage_done, items_dmg, is_crit = Champ.get_aa_damage(Dummy, current_time, rng=rng)
        total_damage += damage_done
        current_time = round(current_time + Champ.get_aa_time(), 2)
        if DAMAGE_TARGET : Dummy.deal_damage(damage_done)
        current_dps = total_damage / current_time
        
        # Log Items DPS
        for key in items_dmg.keys() :
            if key not in sum_items_dmg.keys() and items_dmg[key] == 0 : continue # Avoid adding No Damage Items (eg Yun Tal) to the sum_items_dmg dict
            if key not in sum_items_dmg.keys(): sum_items_dmg[key] = {"Total_Dmg":0, "DPS":0}
            sum_items_dmg[key]["Total_Dmg"] += items_dmg[key]
            sum_items_dmg[key]["DPS"] = round(sum_items_dmg[key]["Total_Dmg"] / current_time, 2)

        # Log Items Passives
        items_messages = {}
        for item in Champ.items: 
            items_messages[item.name] = f"[{item.name}]"
            for key in item.passive.keys() :
                items_messages[item.name] += f" {key.title()} {item.passive[key]}"
        
        verbose_str = ""
        if(verbose > 0) : 
            prefix = f"{Fore.LIGHTBLACK_EX}[{current_time:.2f}s]{Fore.RESET}"
            aa_dmg = f"{Fore.LIGHTYELLOW_EX if is_crit else Fore.LIGHTBLACK_EX}AA Dmg {str(damage_done).ljust(3, " ")}{Fore.RESET}"
            current_dps_str = f"{Fore.YELLOW}Current DPS {current_dps:.2f}{Fore.RESET}"
            dummy_str = f"{Fore.LIGHTGREEN_EX}Target HP {Dummy.stats.current_hp} {Fore.LIGHTBLUE_EX + "(L)" if Dummy.hp_locked else ''}{Fore.RESET}"
            verbose_str = f"{prefix: >18} | {aa_dmg} | {current_dps_str} | {dummy_str}"
        if(verbose > 1) : verbose_str += f" | Items Passives : {" : ".join(items_messages.values())} | {sum_items_dmg}"
        if(verbose > 2) : verbose_str += f"\n{str(Champ)}"
        if(verbose > 0) : print(verbose_str)

    return total_damage/current_time

target = Target(2000, 30, hp_locked=True)
seed = random.random()
seededRandom = random.Random(seed)
VERBOSE = 1
testTime = 20

if(testTime > 100) : VERBOSE = 0

l = 18
Jinx = Champion(59, 0.625, 325, 3.25, 0.014, "Jinx", level=l).add_item(ITEM.BRK)
DPS = calculate(Jinx, target, testTime, rng=seededRandom, verbose=VERBOSE)
print(str(l).rjust(2, " "), Jinx, "| DPS :", DPS)

Jinx = Champion(59, 0.625, 325, 3.25, 0.014, "Jinx", level=l).add_item(ITEM.YunTal)
DPS = calculate(Jinx, target, testTime, rng=seededRandom, verbose=VERBOSE)
print(str(l).rjust(2, " "), Jinx, "| DPS :", DPS)