class Target:
    def __init__(self, hp, armor):
        self.base_hp = hp
        self.current_hp = hp
        self.armor = armor

    def deal_damage(self, damage):
        self.current_hp = max(self.current_hp - damage, 200)

    def get_effective_armor(self, lethality, armor_pen = 0):
        """Calculate armor after penetration effects"""
        flat_reduced = self.armor - lethality
        effective_armor = max(flat_reduced * (1 - armor_pen), 0)
        return effective_armor