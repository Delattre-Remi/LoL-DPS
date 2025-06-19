from Stats import Stats

class Target:
    def __init__(self, hp, armor):
        self.stats = Stats()
        self.stats.max_hp = hp
        self.stats.current_hp = hp
        self.stats.armor = armor

    def deal_damage(self, damage):
        self.stats.current_hp = max(self.stats.current_hp - damage, 200)

    def get_effective_armor(self, lethality, armor_pen = 0):
        """Calculate armor after penetration effects"""
        flat_reduced = self.stats.armor - lethality
        effective_armor = max(flat_reduced * (1 - armor_pen / 100), 0)
        return effective_armor