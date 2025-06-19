from Champion import Champion
from Target import Target
from Item import ITEM

import random

DAMAGE_TARGET = True

def calculate(Champ : Champion, Dummy : Target, rng = random.Random(0), verbose = 0) -> float:
    end_time = 200
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
        if(verbose > 0) : verbose_str = f"[{current_time}s] <{Champ.name}> AA Dmg {str(damage_done).ljust(3, " ")} | {" Crit !" if is_crit else "No Crit"} | Current DPS {current_dps:.2f} | Total {total_damage} | Target HP {Dummy.stats.current_hp}"
        if(verbose > 1) : verbose_str += f"\n{" : ".join(items_messages.values())} | {sum_items_dmg}"
        if(verbose > 2) : verbose_str += f"\n{str(Champ)}"
        if(verbose > 0) : print(verbose_str)

    return total_damage/current_time

target = Target(1000, 0)
seed = random.random()

for l in range(1, 2):
    Jinx = Champion(59, 0.625, 3.25, 0.014, "Jinx", level=l)
    print(Jinx)
    DPS = calculate(Jinx, target, rng=random.Random(seed), verbose=1)
    print(str(l).rjust(2, " "), Jinx, DPS)
    
    Jinx = Champion(59, 0.625, 3.25, 0.014, "Jinx", level=l).add_item(ITEM.LDR)
    print(Jinx)
    DPS = calculate(Jinx, target, rng=random.Random(seed), verbose=1)
    print(str(l).rjust(2, " "), Jinx, DPS)