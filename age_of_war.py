from itertools import permutations

class Platoon:
    """A group of soldiers of the same type."""
    
    # What beats what
    beats = {
        "Militia": ["Spearmen", "LightCavalry"],
        "Spearmen": ["LightCavalry", "HeavyCavalry"], 
        "LightCavalry": ["FootArcher", "CavalryArcher"],
        "HeavyCavalry": ["Militia", "FootArcher", "LightCavalry"],
        "CavalryArcher": ["Spearmen", "HeavyCavalry"],
        "FootArcher": ["Militia", "CavalryArcher"],
    }
    
    def __init__(self, type, count):
        self.type = type
        self.count = count
    
    def can_beat(self, other):
        """Check if we beat the other guy"""
        return other.type in self.beats.get(self.type, [])
    
    def power_vs(self, other):
        """How strong are we against them?"""
        if self.can_beat(other):
            return self.count * 2
        else:
            return self.count
    
    def fight(self, other):
        """Fight another platoon - return win/draw/lose"""
        my_power = self.power_vs(other)
        their_count = other.count
        
        if my_power > their_count:
            return "win"
        elif my_power == their_count:
            return "draw"
        else:
            return "lose"
    
    def __str__(self):
        return f"{self.type}#{self.count}"

class Army:
    """Just a bunch of platoons"""
    
    def __init__(self, units):
        self.units = units
    
    @staticmethod
    def parse(text):
        """Turn text into an army"""
        if not text.strip():
            raise ValueError("Need some input!")
            
        units = []
        parts = text.strip().split(";")
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
                
            if "#" not in part:
                raise ValueError(f"Bad format: {part}")
                
            unit_type, num = part.split("#")
            unit_type = unit_type.strip()
            
            try:
                num = int(num.strip())
            except:
                raise ValueError(f"Bad number in: {part}")
                
            units.append(Platoon(unit_type, num))
            
        return Army(units)
    
    def __str__(self):
        return ";".join(str(u) for u in self.units)

class War:
    """Runs the war simulation"""
    
    def __init__(self, my_army, enemy_army):
        self.mine = my_army
        self.theirs = enemy_army
    
    def find_winning_setup(self):
        """Try different orders to find one that wins"""
        
        # Try every possible order of our units
        for order in permutations(self.mine.units):
            wins = 0
            
            # Fight each battle
            for i in range(len(order)):
                my_unit = order[i] 
                their_unit = self.theirs.units[i]
                result = my_unit.fight(their_unit)
                
                if result == "win":
                    wins += 1
            
            # Need at least 3 wins
            if wins >= 3:
                return Army(list(order))
        
        return None

def main():
    print("Medieval War Simulator")
    
    try:
        my_input = input("Your army: ")
        enemy_input = input("Enemy army: ")
        
        my_army = Army.parse(my_input)
        enemy_army = Army.parse(enemy_input)
        
        war = War(my_army, enemy_army)
        winner = war.find_winning_setup()
        
        if winner:
            print("Found a winning:")
            print(winner)
        else:
            print("No way to win :(")
            
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()
