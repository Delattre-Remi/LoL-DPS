from Champion import Champion
from Target import Target

def nothing():
    return 0

class Item:
    def __init__(self, name="PLACEHOLDER", ad=0, crit=0, atk_speed=0, 
                 lethality=0, armor_pen=0, on_hit=nothing, crit_dmg=0):
        self.name = name
        self.ad = ad
        self.crit = crit
        self.atk_speed = atk_speed
        self.lethality = lethality
        self.armor_pen = armor_pen
        self.on_hit = on_hit 
        self.crit_dmg = crit_dmg

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()

class _Kraken(Item):
    def __init__(self):
        super().__init__(name="Kraken")
        self.ad = 45
        self.atk_speed = 40
        self.on_hit = self.BringItDown
        self.passive = {'stacks' : 0}

    def BringItDown(self, holder : Champion, target : Target, current_time) -> float:
        self.passive["stacks"] = self.passive["stacks"] + 1
        self.last_proc_time = current_time

        if self.last_proc_time - current_time > 3 : self.passive["stacks"] = 0
        
        if self.passive["stacks"] == 3:
            health_ratio = (target.base_hp - target.current_hp) / target.base_hp

            #(Melee 150 – 200 | Ranged 120 – 160) (based on level)
            base_dmg = 120 if holder.is_ranged else 150
            based_on_level = 4 if holder.is_ranged else 50
            added_by_level = based_on_level / (1 + (holder.level - 18)/18)

            scaled_dmg = (base_dmg + added_by_level) * (1 + health_ratio/2)
            self.passive["stacks"] = 0
            return round(scaled_dmg, 4)
        return 0

Kraken = _Kraken()