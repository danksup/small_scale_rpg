from player import Player
# import json
# import os

# with open("players.json", "r") as f:
#     player_data = json.load(f)

# def main_loop(acc):
#     while True:
#         print(f"playing as {acc.name}")
#         print(f"{'-'*50}")
#         user_input = input("at your command: ").lower().split()
#         command = user_input[0]
#         args = user_input[1:]
        
#         if command == "whoami":
#             print(acc)
#         elif command in ['inv', 'inventory']:
#             if args:
#                 try:
#                     acc.inventory.printinv(int(args[0]))
#                 except ValueError:
#                     print("invalid value")
#             else:
#                 print(acc.inventory)
#         elif command in ['coin', 'coins']:
#             print(acc.coins)
#         elif command == 'gacha':
#             acc.gacha()
#         elif command == 'equip':
#             if args:
#                 to_equip = args[0]
#                 acc.equip(to_equip)
#             else:
#                 print('invalid input')
#         elif command == 'deequip':
#             if args:
#                 to_deequip = args[0]
#                 acc.deequip(to_deequip)
#             else:
#                 print('invalid input')
#         elif command == "fish":
#             acc.fish()
#         elif command == 'buy':
#             if args:
#                 try:
#                     to_buy = args[0]
#                     count = args[1]
#                     acc.buy(to_buy, int(count))
#                 except ValueError:
#                     print('invalid arguments')
#         elif command == 'sell':
#             if args:
#                 try:
#                     to_sell = args[0]
#                     count = args[1]
#                     acc.sell(to_sell, int(count))
#                 except ValueError:
#                     print('invalid arguments')           
#         elif command in ['clear', 'cls']:
#             os.system('clear')
#         elif command in ['break', 'exit', 'esc']:
#             break


# name = "iii3jwo0wik23mjfoemco3mmefkmdwkemded"  # input("choose your account: ")

# if name in player_data:
#     acc = Player(name)
#     os.system('clear')
#     print(f"you are now logged in as {acc.name}")

#     main_loop(acc)
# else:
#     make = input("acc not found. make one? ").lower()
#     if make in ['y', 'yes', 'yeah', 'ok', 'sure']:
#         acc = Player.create_player(name) 
        
#         main_loop(acc)  
#     else:
#         print('exiting')

debug = Player("iii3jwo0wik23mjfoemco3mmefkmdwkemded")
print(debug)