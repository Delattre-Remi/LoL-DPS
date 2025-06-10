class Champion:
    def __init__(self, base_ad, base_as, ad_per_level, as_per_level, name, level=18):
        self.name = name
        self.base_ad = base_ad
        self.ad_per_level = ad_per_level
        self.growth_ratio = (level-1) * (0.7025 + 0.0175 * (level-1))
        self.ad = base_ad + self.growth_ratio * ad_per_level
        self.crit_chance = 0      # Stored as decimal (0-1)
        self.crit_dmg = 1.75       # Base 175% damage
        self.base_as = base_as
        self.as_per_level = as_per_level
        self.bonus_as = 0         # Total attack speed bonuses
        self.lethality = 0        # Flat armor penetration
        self.armor_pen = 0        # % Armor pen (multiplicative stack)
        self.on_hit_effects = []
        self.items = []
        self.is_ranged = True
        self.level = level

    def get_AS(self):
        return self.base_as * (1 + self.bonus_as + self.as_per_level * self.growth_ratio)

    def get_aa_time(self):
        return 1 / self.get_AS()

    def get_aa_damage(self, target, current_time):
        """Calculate average auto-attack damage"""
        # Crit calculations
        crit_multiplier = 1 + self.crit_chance * (self.crit_dmg - 1)
        base_dmg = self.ad * crit_multiplier
        
        # Armor penetration
        effective_armor = target.get_effective_armor(self.armor_pen)
        dmg_multiplier = 100 / (100 + effective_armor)
        
        # On-hit effects
        on_hit_dmg = 0
        for item_passive in self.on_hit_effects:
            on_hit_dmg += item_passive(self, target, current_time)
        
        return (base_dmg + on_hit_dmg) * dmg_multiplier

    def add_item(self, item):
        """Apply item stats to champion"""
        self.ad += item.ad
        self.crit_chance += item.crit / 100
        self.bonus_as += item.atk_speed / 100
        self.lethality += item.lethality
        self.on_hit_effects.append(item.on_hit)
        
        # Multiplicative armor pen stacking
        if item.armor_pen > 0:
            self.armor_pen = 1 - (1 - self.armor_pen) * (1 - item.armor_pen)
        
        # Critical damage modifiers
        if item.crit_dmg > 0:
            self.crit_dmg = 1 + (self.crit_dmg - 1) + item.crit_dmg / 100
        
        self.items.append(item)
        return self

    def __str__(self) -> str:
        return f"<{self.name}> AD {self.ad} AS {self.get_AS():.4f} | Items {self.items}"
