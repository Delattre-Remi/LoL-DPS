from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Champion import Champion
    from Target import Target

from Stats import Stats

class Item:
    def __init__(self, name="PLACEHOLDER", ad=0, crit_chance=0, atk_speed=0, 
                 lethality=0, armor_pen=0, on_hit=None, crit_dmg=0):
        self.name : str = name
        self.stats = Stats()
        self.stats.ad = ad
        self.stats.bonus_as = atk_speed
        self.stats.lethality = lethality
        self.stats.armor_pen = armor_pen
        self.stats.crit_chance = crit_chance
        self.stats.crit_dmg = crit_dmg
        self.on_hit = on_hit 
        self.passive = {}

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()

class _Kraken(Item):
    def __init__(self):
        super().__init__(name="Kraken", ad=45, atk_speed=40)
        self.on_hit = self.BringItDown
        self.passive = {'stacks' : 0}

    def BringItDown(self, holder : Champion, target : Target, current_time : float, is_crit=False) -> float:
        self.passive["stacks"] = self.passive["stacks"] + 1
        self.last_proc_time = current_time

        if self.last_proc_time - current_time > 3 : self.passive["stacks"] = 0
        
        if self.passive["stacks"] == 3:
            health_ratio = (target.stats.max_hp - target.stats.current_hp) / target.stats.max_hp

            #(Melee 150 – 200 | Ranged 120 – 160) (based on level)
            base_dmg = 120 if holder.is_ranged else 150
            based_on_level = 4 if holder.is_ranged else 50
            added_by_level = based_on_level / (1 + ((holder.stats.level - 18)/18))
            scaled_dmg = (base_dmg + added_by_level) * (1 + health_ratio/2)
            self.passive["stacks"] = 0
            return round(scaled_dmg, 4)
        return 0

class _YunTal(Item):
    """Passed from Huntress to Huntress, to fell foe after foe."""
    def __init__(self):
        super().__init__(name="Yun Tal Wildarrows", ad=55, atk_speed=35, crit_chance=25)
        self.on_hit = self.Flurry
        self.passive : dict[str, float] = {'cooldown' : 0}
        self.last_time = 0

    def Flurry(self, holder : Champion, target : Target, current_time : float, is_crit=False) -> float:
        """Unique - Flurry: on-attacking an enemy champion, 
        gain 30% bonus attack speed for 6 seconds. 
        Attacks reduce this cooldown by 1 second, 
        increased to 2 seconds with  critical strikes (30 second cooldown)."""
        
        # Give buff is available
        if(self.passive["cooldown"] <= 0) : 
            holder.add_buff("Flurry",  {"bonus_as": 30}, current_time + 6)
            self.passive["cooldown"] = 30
        
        # Reduce cooldown on auto-attack
        self.passive["cooldown"] -= 2 if is_crit else 1
        self.passive["cooldown"] = round(self.passive["cooldown"] - (current_time - self.last_time), 2)
        if(self.passive["cooldown"] < 0) : self.passive["cooldown"] = 0
        
        self.last_time = current_time
        
        return 0

class _LDR(Item):
    def __init__(self):
        super().__init__(name="Lord Dominik's Regards", ad=35, crit_chance=25, armor_pen=35)


class ITEM(enumerate):
    YunTal = _YunTal()
    Kraken = _Kraken()
    LDR = _LDR()