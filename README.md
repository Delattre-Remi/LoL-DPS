# League of Legends Auto Attack Simulator
A Python-based simulation for auto-attack damage, item synergies, and buff interactions, inspired by League of Legends mechanics. The simulator supports easy extensibility for custom champions, targets (dummies), and items, allowing quick comparisons of builds and effects.

## Features
- Champion Stat Growth: Simulates scaling with level, including AD, attack speed, crit chance, and more.
- Buff & Debuff System: Dynamic addition/removal of effects (e.g. attack speed buffs, slows).
- Itemization: Full item system, including unique passives, on-hit effects, and cooldown-based triggers.
- DPS Calculation: Simulates a test period for accurate DPS measurement, supporting different item combinations.
- Verbose Logging: Optional per-attack logging with colored outputs for debugging or analysis.
## Project Structure
```
main.py           # Entry point and example builds
Champion.py       # Champion class, stat growth, item addition, buff handling
Target.py         # Target ("dummy") to apply damage and buffs/debuffs
Item.py           # Item & item passive logic, on-hit and cooldown mechanics
Buff.py           # Buff structure and expiration handling
Stats.py          # (Assumed) Stat container for champ/target/item
```

## Usage Example
Edit main.py to define your champion, items, and target.
Use or extend the provided classes to try new builds or mechanics.
Example snippet:

```python
from Champion import Champion
from Target import Target
from Item import ITEM
import random

l = 18
Jinx = Champion(59, 0.625, 325, 3.25, 0.014, "Jinx", level=l).add_item(ITEM.BRK)
target = Target(2000, 30, hp_locked=True)
seededRandom = random.Random(random.random())
DPS = calculate(Jinx, target, testTime=20, rng=seededRandom, verbose=1)
print(str(l).rjust(2, " "), Jinx, "| DPS :", DPS)
```
## Items Implemented
- Blade of the Ruined King (BRK)
- Yun Tal Wildarrows
- Kraken
- Lord Dominik's Regards
- Infinity Edge
- Youmuu's Ghostblade
- Bloodthirster

(See Item.py for full details & mechanics.)

# To-Do
- Unit Testing: Implement unittests for champion, item, and buff interactions.
- More Champions: Create templates and presets for other champions with unique passives/spells.
- Ability Simulation: Extend from basic auto-attacks to include ability damage and spell passives.
- Stat Progression Graphing: Integrate with plotting library (e.g., matplotlib) for DPS over time/build.

#### Disclaimer: Data and mechanics are for simulation purposes only and not affiliated with Riot Games.