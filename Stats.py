class Stats:
    def __init__(self):
        # Global
        self.max_hp : float = 0
        self.current_hp : float = 0
        self.armor : float = 0
        self.ad : float = 0
        self.ap : float = 0
        self.crit_chance : int = 0      # 0 - 100
        self.crit_dmg : int    = 175    # Base 175% damage
        self.lethality : int   = 0      # Flat armor penetration
        self.armor_pen : int   = 0      # % Armor pen (multiplicative stack) 0 - 100
        self.ms : int          = 0
        self.lifesteal : int   = 0
        
        # Champion Specific
        self.level : int = 1
        self.base_ad : float = 0
        self.ad_per_level : float = 0
        self.growth_ratio : float = (self.level-1) * (0.7025 + 0.0175 * (self.level-1))
        self.base_as : float = 0
        self.as_per_level : float = 0
        self.bonus_as : int = 0         # Total attack speed bonuses
        self.bonus_ms : int = 0
