from Buff import Buff
from Stats import Stats

class Target:
    def __init__(self, hp, armor, hp_locked = False):
        self.stats = Stats()
        self.stats.max_hp = hp
        self.stats.current_hp = hp
        self.stats.armor = armor
        self.hp_locked = hp_locked
        self.buffs : dict[str, Buff] = {}

    def deal_damage(self, damage):
        if self.hp_locked : return
        self.stats.current_hp = max(self.stats.current_hp - damage, 200)

    def get_effective_armor(self, lethality, armor_pen = 0):
        """Calculate armor after penetration effects"""
        after_percent_reduce = self.stats.armor * (1 - armor_pen / 100)
        flat_reduced = max(after_percent_reduce - lethality, 0)
        return flat_reduced
    
    def add_buff(self, buff_name : str, buffed_stat : dict, expiration_time : float) -> None:
        self.buffs[buff_name] = Buff(buff_name, buffed_stat, expiration_time)