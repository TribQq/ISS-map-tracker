# RPG Damage Calculator :bow_and_arrow: :dagger: :shield:


This is a small calculator for calculating damage in a
[pen & paper RPG](https://en.wikipedia.org/wiki/Tabletop_role-playing_game).
It is also a small experiment to try out client-side web programming with [brython](https://brython.info/) and
system testing with web browser automation using [selenium](https://www.selenium.dev/).


![desc_img](https://github.com/TribQq/mini_apps/blob/master/rpg_dmg_calc(brython%2C%20%20selenium)/description/rpg_dmc_calc.jpg)



## How to run it locally:

Clone the repository and start a small HTTP server
```
virtualenv rpg_calc_env -p python3.10
source rpg_calc_env/bin/activate
pip install -r requirements.txt
python -m http.server
```
=> web browser http://localhost:8000/

## The algorithm

Given a table that calculates penetration modifiers based on damage type, armor type and armor points, the resulting damage is calculated as

```
algorithm calculate-damage is
    input: damage type (string),
           damage (int >= 0),
           penetration (int >= 0),
           armor
    output: damage taken

    remaining penetration ← penetration
    remaining damage ← damage
    for each armor layer (string armor type, int armor points) in armor do
        penetration modifier ← looked up in a table based on (damage type, armor type, armor points)
        remaining penetration ← max(0, remaining penetration - penetration modifier)
        remaining armor points ← max(0, armor points - remaining penetration)
        remaining penetration ← max(0, remaining penetration - armor points)
        remaining damage ← max(0, remaining damage - 2*remaining armor points)
    return remaining damage
```


## License

The styling of the calculator is using [CSS](https://codepen.io/retractedhack/pen/gPLpWe) from [Chad Chartered](https://codepen.io/retractedhack).