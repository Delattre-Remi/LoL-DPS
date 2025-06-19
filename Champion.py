from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Item import Item
    from Target import Target
    
from random import Random
from Buff import Buff
from Stats import Stats


class Champion:
    def __init__(self, base_ad, base_as, ad_per_level, as_per_level, name, level=18):
        self.name : str = name
        self.stats = Stats()
        self.stats.level = level
        self.stats.base_ad = base_ad
        self.stats.ad_per_level = ad_per_level
        self.stats.growth_ratio = (level-1) * (0.7025 + 0.0175 * (level-1))
        self.stats.ad = base_ad + self.stats.growth_ratio * ad_per_level
        self.stats.crit_chance = 0
        self.stats.crit_dmg = 175
        self.stats.base_as = base_as
        self.stats.as_per_level = as_per_level
        self.stats.bonus_as = 0
        self.stats.lethality = 0
        self.stats.armor_pen = 0
        self.is_ranged = True
        self.items : list[Item] = []
        self.buffs : dict[str, Buff] = {}
        
    def update(self, current_time : float) -> None:
        # Buffs
        self.stats_from_buffs = {"bonus_as" : 0}
        for buff_name in list(self.buffs.keys()):
            buff = self.buffs[buff_name]
            buff_state = buff.update(current_time)
            if buff_state == 1: # buff_hasToBeApplied
                self.bonus_as += buff.buffed_stats.get("bonus_as", 0)
            elif buff_state == -1 : # buff_hasRanOff
                self.bonus_as -= buff.buffed_stats.get("bonus_as", 0)
                del self.buffs[buff_name]
               
    def add_buff(self, buff_name : str, buffed_stat : dict, expiration_time : float) -> None:
        self.buffs[buff_name] = Buff(buff_name, buffed_stat, expiration_time)

    def get_AS(self) -> float:
        return self.stats.base_as * (1 + (self.stats.bonus_as / 100) + self.stats.as_per_level * self.stats.growth_ratio)

    def get_aa_time(self) -> float:
        return 1 / self.get_AS()

    def get_aa_damage(self, target : Target, current_time : float, rng : Random = Random(1)) -> tuple[float, dict, bool]:
        """Calculate average auto-attack damage"""
        
        # Crit calculations
        is_crit = rng.random() < (self.stats.crit_chance / 100)
        base_dmg = self.stats.ad * (self.stats.crit_dmg / 100 if is_crit else 1)
        
        # Armor penetration
        effective_armor = target.get_effective_armor(self.stats.armor_pen)
        dmg_multiplier = 100 / (100 + effective_armor)
        
        # On-hit effects
        on_hit_dmg = {}
        for item in self.items:
            if(item.on_hit is None) : continue
            on_hit_dmg[item.name] = round(item.on_hit(self, target, current_time, is_crit=is_crit) * dmg_multiplier)
            
        sum_on_hit = sum(on_hit_dmg.values())
        return round(base_dmg * dmg_multiplier) + sum_on_hit, on_hit_dmg, is_crit

    def add_item(self, item: Item):
        """Apply item stats to champion"""
        self.stats.ad += item.stats.ad
        self.stats.crit_chance += item.stats.crit_chance
        self.stats.bonus_as += item.stats.bonus_as
        self.stats.lethality += item.stats.lethality
        
        # Multiplicative armor pen stacking
        if item.stats.armor_pen > 0:
            self.stats.armor_pen = 1 - (1 - self.stats.armor_pen) * (1 - item.stats.armor_pen)
        
        # Critical damage modifiers
        if item.stats.crit_dmg > 0:
            self.stats.crit_dmg = 1 + (self.stats.crit_dmg - 1) + item.stats.crit_dmg
        
        self.items.append(item)
        return self

    def __str__(self) -> str:
        ad_str = str(int(self.stats.ad)).ljust(3, ' ')
        as_str = str(round(self.get_AS(), 4)).ljust(6, '0')
        return f"<{self.name}> | AD {ad_str} | AS {as_str} | Items {self.items} | Buffs {self.buffs}"
