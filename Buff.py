class Buff:
    def __init__(self, name : str, buffed_stats : dict, expiration_time : float):
        self.name = name
        self.buffed_stats : dict[str, int] = buffed_stats
        self.expiration_time = expiration_time
        self.hasToBeApplied = False
    
    def update(self, current_time : float):
        """
        Returns
            0 if nothing to do
            -1 if buff has ran off
            1 if buff has to be applied
        """
        if not self.hasToBeApplied : 
            self.hasToBeApplied = True
            return 1
        if current_time > self.expiration_time : return -1
        return 0
    
    def __str__(self) -> str:
        return f"{self.buffed_stats} Expires at {self.expiration_time}"
    
    def __repr__(self) -> str:
        return self.__str__()

        