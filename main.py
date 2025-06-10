from Champion import Champion
from Target import Target
from Item import Item, Kraken

DAMAGE_TARGET = True

def calculate(Champ, Dummy, verbose=0):
    end_time = 200
    current_time = 0
    total_damage = 0
    current_dps = 0

    while end_time > current_time:
        # Auto Attack
        damage_done = round(Champ.get_aa_damage(Dummy, current_time))
        total_damage += damage_done
        current_time += round(Champ.get_aa_time(), 4)
        if DAMAGE_TARGET :Dummy.deal_damage(damage_done)
        current_dps = total_damage / current_time

        items_messages = []
        for item in Champ.items: items_messages.append(f"[{item.name}] Stacks {item.passive["stacks"]}")
        
        if(verbose > 0) : print(f"[{current_time:.2f}s] <{Champ.name}> AA Dmg {damage_done} | Current DPS {current_dps:.2f} | Total {total_damage} | Target HP {Dummy.current_hp} | {" : ".join(items_messages)}")

    return total_damage/current_time

target = Target(1000, 0)

for l in range(19):
    Jinx = Champion(59, 0.625, 3.25, 0.014, "Jinx", level=l)
    DPS = calculate(Jinx, target)
    print(l, Jinx)
    #print(f"DPS {DPS}")