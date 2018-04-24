from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Create black magic
fire = Spell("Fire", 10, 500, "black")
thunder = Spell("Thunder", 12, 580, "black")
blizzard = Spell("Blizzard", 10, 500, "black")
meteor = Spell("Meteor", 20, 980, "black")
quake = Spell("Quake", 12, 600, "black")

# Create white magic
cure = Spell("Cure", 12, 370, "white")
cura = Spell("Cura", 18, 650, "white")

# Create some Items
# Potions
potion = Item("Potion", "potion", "Heals 200 HP", 200)
hi_potion = Item("Hi-Potion", "potion", "Heals 400 HP", 400)
super_potion = Item("Super Potion", "potion", "Heals 800 HP", 800)
# Elixirs
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
mega_elixir = Item("Mega Elixir", "elixir", "Fully restores party's HP/MP", 9999)
# Damage
grenade = Item("Grenade", "damage", "Deals 500 damage", 800)

# Spells lists
player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]

# Items lists
player_items = [{"item": potion, "quantity": 15},
                {"item": hi_potion, "quantity": 5},
                {"item": super_potion, "quantity": 2},
                {"item": elixir, "quantity": 5},
                {"item": mega_elixir, "quantity": 2},
                {"item": grenade, "quantity": 2}]

# Instantiate People
# Players
player1 = Person("Valos:", 1350, 500, 400, 34, player_spells, player_items)
player2 = Person("Jamie:", 1020, 480, 540, 34, player_spells, player_items)
player3 = Person("Frost:", 1270, 700, 360, 34, player_spells, player_items)
# Enemies
enemy1 = Person("Imp    ", 1250, 130, 560, 325, [], [])
enemy2 = Person("Magus ", 18200, 690, 460, 25, [], [])
enemy3 = Person("Imp    ", 1250, 130, 560, 325, [], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("==========================================")

    # print("\n\n")
    print("NAME                    HP                                      MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    " + "Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage!")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    " + "Choose magic:")) - 1
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + enemies[enemy].name.replace(" ", "") + "." + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    " + "Choose item:")) - 1
            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "You don't have more " + item.name + "s." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP." + bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "Mega Elixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP." + bcolors.ENDC)
            elif item.type == "damage":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop),
                      "points of damage to " + enemies[enemy].name.replace(" ", "") + "." + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    enemy_choice = 1
    players_len = len(players)
    target = random.randrange(0, int(players_len))
    enemy_dmg = enemies[1].generate_damage()
    players[target].take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg, "points of damage.")

    defeated_enemies = 0
    defeated_players = 0

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False
