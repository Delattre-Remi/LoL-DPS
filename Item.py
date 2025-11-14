from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Champion import Champion
    from Target import Target

from Stats import Stats

class Item:
    def __init__(self, name="PLACEHOLDER", ad=0, crit_chance=0, atk_speed=0, 
                 lethality=0, armor_pen=0, on_hit=None, crit_dmg=0, bonus_ms=0, lifesteal=0):
        self.name : str = name
        self.stats = Stats()
        self.stats.ad = ad
        self.stats.bonus_as = atk_speed
        self.stats.lethality = lethality
        self.stats.armor_pen = armor_pen
        self.stats.crit_chance = crit_chance
        self.stats.crit_dmg = crit_dmg
        self.stats.bonus_ms = bonus_ms
        self.stats.lifesteal = lifesteal
        self.on_hit = on_hit 
        self.passive = {}

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()

class ItemWithCooldown(Item):
    def __init__(self, name, baseCooldown:int, ad=0, crit_chance=0, atk_speed=0, lethality=0, armor_pen=0, on_hit=None, crit_dmg=0, bonus_ms=0, lifesteal=0):
        super().__init__(name, ad, crit_chance, atk_speed, lethality, armor_pen, on_hit, crit_dmg, bonus_ms, lifesteal)
        self.on_hit = on_hit
        self.baseCooldown = baseCooldown
        self.passive : dict[str, float] = {'cooldown' : 0}
        self.lastCooldownUpdate : float = 0.0
        
    def isPassiveReady(self):
        return self.passive["cooldown"] <= 0
    
    def usePassive(self):
        self.passive["cooldown"] = self.baseCooldown
        
    def updateCooldown(self, current_time:float):
        self.passive["cooldown"] = round(self.passive["cooldown"] - (current_time - self.lastCooldownUpdate), 3)
        self.lastCooldownUpdate = current_time
        
        if(self.passive["cooldown"] < 0) : self.passive["cooldown"] = 0

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

class _YunTal(ItemWithCooldown):
    """Passed from Huntress to Huntress, to fell foe after foe."""
    def __init__(self):
        super().__init__(name="Yun Tal Wildarrows", baseCooldown=30, ad=55, atk_speed=35, crit_chance=25)
        self.on_hit = self.Flurry

    def Flurry(self, holder : Champion, target : Target, current_time : float, is_crit=False) -> float:
        """Unique - Flurry: on-attacking an enemy champion, 
        gain 30% bonus attack speed for 6 seconds. 
        Attacks reduce this cooldown by 1 second, 
        increased to 2 seconds with  critical strikes (30 second cooldown)."""
        
        # Give buff is available
        if(self.isPassiveReady()) : 
            holder.add_buff("Flurry", {"bonus_as": 30}, current_time + 6)
            self.usePassive()
        
        # Reduce cooldown on auto-attack
        self.passive["cooldown"] -= 2 if is_crit else 1
        self.updateCooldown(current_time)
        
        return 0

class _YoumuusGhostblade(ItemWithCooldown):
    """The dearly beloved gathered, but soon there would be much more to mourn."""
    def __init__(self):
        super().__init__(name="Youmuu's Ghostblade", baseCooldown=45, ad=55, lethality=18, bonus_ms=4)
        self.on_hit = self.WraithStep

    def WraithStep(self, holder : Champion, target : Target, current_time : float, is_crit=False):
        """ Unique - Wraith Step: 
        Gain (20% / 15%) bonus movement speed and 
        ghosting for (6 / 4) seconds (45 second cooldown)."""
        
        # Give buff is available
        if(self.isPassiveReady()) : 
            holder.add_buff("Wraith Step", {"bonus_ms": 10 if holder.is_ranged else 20}, current_time + (4 if holder.is_ranged else 6))
            self.usePassive()
        
        self.updateCooldown(current_time)
        
        return 0
 
class _BRK(ItemWithCooldown):
    def __init__(self):
        super().__init__(name="Blade of the Ruined King", baseCooldown=15, ad=40, atk_speed=25, lifesteal=10)
        self.on_hit = [self.MistsEdge, self.ClawingShadows]
        self.passive['stacks'] = 0

    def MistsEdge(self, holder : Champion, target : Target, current_time : float, is_crit=False):
        """Unique - Mist's Edge: 
        Basic attacks deal bonus physical damage on-hit 
        equal to (8% / 5%) of the target's current health, 
        with a maximum of 100 against  minions and  monsters."""
        
        return target.stats.current_hp * (0.05 if holder.is_ranged else 0.08)
        
    def ClawingShadows(self, holder : Champion, target : Target, current_time : float, is_crit=False):
        """Unique - Clawing Shadows:
        Basic attacks on-hit against enemy champions 
        apply a stack for 6 seconds, stacking up to 3 times. 
        The third stack consumes them all to 
        slow the target by 30% for 1 second (15 second cooldown)."""
        
        # Give buff is available
        if(self.isPassiveReady()) : 
            self.passive["stacks"] = self.passive["stacks"] + 1
            if(self.passive["stacks"] == 3):
                target.add_buff("Clawing Shadows", {"bonus_ms": -30}, current_time + 1)
                self.passive["stacks"] = 0
            self.usePassive()
        
        self.updateCooldown(current_time)
        
        return 0
    
        
class _LDR(Item):
    def __init__(self):
        super().__init__(name="Lord Dominik's Regards", ad=35, crit_chance=25, armor_pen=35)
     
class _IE(Item):
    def __init__(self):
        super().__init__(name="Infinity Edge", ad=70, crit_chance=25, crit_dmg=40)

class _BT(Item):
    def __init__(self):
        super().__init__(name="Bloodthirster", ad=80, lifesteal=15)


class ITEM(enumerate):
    YunTal = _YunTal()
    Kraken = _Kraken()
    LDR = _LDR()
    Youmuus = _YoumuusGhostblade()
    IE = _IE()
    BT = _BT()
    BRK = _BRK()