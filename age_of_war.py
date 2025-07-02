from itertools import permutations


class Platoon:
    """
     group of soldiers of the same class.
    """

    ADVANTAGE_MAP = {
        "Militia": ["Spearmen", "LightCavalry"],
        "Spearmen": ["LightCavalry", "HeavyCavalry"],
        "LightCavalry": ["FootArcher", "CavalryArcher"],
        "HeavyCavalry": ["Militia", "FootArcher", "LightCavalry"],
        "CavalryArcher": ["Spearmen", "HeavyCavalry"],
        "FootArcher": ["Militia", "CavalryArcher"],
    }

    def __init__(self, unit_class, size):
        self.unit_class = unit_class
        self.size = size

    def has_advantage_over(self, enemy):
        """
        Checks if this platoon has an advantage over the enemy platoon.
        """
        return enemy.unit_class in self.ADVANTAGE_MAP.get(self.unit_class, [])

    def effective_strength_against(self, enemy):
        """
        Returns the effective fighting strength of this platoon against the enemy platoon.
        """
        multiplier = 2 if self.has_advantage_over(enemy) else 1
        return self.size * multiplier

    def battle_outcome(self, enemy):
        """
        Determines the battle outcome: win, draw or lose.
        """
        my_strength = self.effective_strength_against(enemy)
        if my_strength > enemy.size:
            return "win"
        elif my_strength == enemy.size:
            return "draw"
        else:
            return "lose"

    def __str__(self):
        return f"{self.unit_class}#{self.size}"


class Army:
    """
    Represents an army, which is a list of platoons.
    """

    def __init__(self, platoons):
        self.platoons = platoons

    @staticmethod
    def from_input(input_line):

        if not input_line:
            raise ValueError("Input cannot be empty.")

        platoons = []
        for token in input_line.strip().split(";"):
            token = token.strip()
            if not token:
                continue
            if "#" not in token:
                raise ValueError(f"Invalid platoon format: '{token}'")
            unit_class, size_str = token.split("#")
            try:
                size = int(size_str.strip())
            except ValueError:
                raise ValueError(f"Invalid number of soldiers in: '{token}'")
            platoons.append(Platoon(unit_class.strip(), size))
        return Army(platoons)

    def __str__(self):
        return ";".join(str(platoon) for platoon in self.platoons)


class WarSimulator:
    """
    Simulates the war and finds a winning permutation if possible.
    """

    def __init__(self, own_army, enemy_army):
        self.own_army = own_army
        self.enemy_army = enemy_army

    def find_winning_arrangement(self):
        """
        Returns a permutation of own army platoons that results in at least 3 wins.
        """
        for permutation in permutations(self.own_army.platoons):
            wins = 0
            for own, enemy in zip(permutation, self.enemy_army.platoons):
                result = own.battle_outcome(enemy)
                if result == "win":
                    wins += 1
            if wins >= 3:
                return Army(list(permutation))
        return None


def main():
    print("Welcome to the Medieval War Simulator!")
    try:
        own_input = input("Enter own platoons: ").strip()
        enemy_input = input("Enter enemy platoons: ").strip()

        own_army = Army.from_input(own_input)
        enemy_army = Army.from_input(enemy_input)

        simulator = WarSimulator(own_army, enemy_army)
        winning_army = simulator.find_winning_arrangement()

        if winning_army:
            print("One possible winning arrangement:")
            print(winning_army)
        else:
            print("There is no chance of winning.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")


if __name__ == "__main__":
    main()
