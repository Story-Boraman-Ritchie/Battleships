import os
import time
import keyboard
import configparser 

print(config.get("Text", "game_over_message"))

config = configparser.ConfigParser()
config.read('config.ini')

# Reading the base values from the "config.ini file"
GRID_HEIGHT = config.get("Grid", "HEIGHT")
GRID_WIDTH = config.get("Grid", "WIDTH")

cursorx = config.get("Grid", "cursorx_start")
cursory = config.get("Grid", "cursory_start")
cursor_direction = config.get("Grid", "cursor_direction_start")

SEA_CHAR = config.get("Characters", "SEA")
SHIP_CHAR = config.get("Characters", "SHIP")
HIT_SHOT_CHAR = config.get("Characters", "HIT_SHOT")
MISS_SHOT_CHAR = config.get("Characters", "MISS_SHOT")

player = config.get("Misc", "starting_player")
player_shots = 1
ship_length = 3

# Defining the arrays
cursor_array = [[" " for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
ship_array_0 = [[SEA_CHAR for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
shot_array_0 = [[SEA_CHAR for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
ship_array_1 = [[SEA_CHAR for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
shot_array_1 = [[SEA_CHAR for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]

# Dictionary to refrence the arrays
arrays = {
    0: {"ship": ship_array_0, "shot": shot_array_0},
    1: {"ship": ship_array_1, "shot": shot_array_1},
}

# Setting the current arrays being used to the current player
current_ship_array = arrays[player]["ship"]
current_shot_array = arrays[player]["shot"]

# Allowing any array to be printed in a readable format
def print_array(array):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            print(array[y][x], end=" ")
        print()

# Placing the ship
def place_ship(player, ship_length, startx, starty, direction):
    current_ship_array = arrays[player]["ship"]
    for i in range(ship_length):
        if direction == 0:
            if startx+i < GRID_WIDTH:
                if starty > 0:
                    current_ship_array[starty-1][startx+i] = SEA_CHAR
                current_ship_array[starty][startx+i] = SHIP_CHAR
                if starty < GRID_HEIGHT-1:
                    current_ship_array[starty+1][startx+i] = SEA_CHAR
            if startx+i-ship_length >= 0:
                if starty > 0:
                    current_ship_array[starty-1][startx+i-ship_length] = SEA_CHAR
                current_ship_array[starty][startx+i-ship_length] = SEA_CHAR
                if starty < GRID_HEIGHT-1:
                    current_ship_array[starty+1][startx+i-ship_length] = SEA_CHAR
        elif direction == 1:
            if starty+i < GRID_HEIGHT:
                if startx > 0:
                    current_ship_array[starty+i][startx-1] = SEA_CHAR
                current_ship_array[starty+i][startx] = SHIP_CHAR
                if startx < GRID_WIDTH-1:
                    current_ship_array[starty+i][startx+1] = SEA_CHAR
            if starty+i-ship_length >= 0:
                if startx > 0:
                    current_ship_array[starty+i-ship_length][startx-1] = SEA_CHAR
                current_ship_array[starty+i-ship_length][startx] = SEA_CHAR
                if startx < GRID_WIDTH-1:
                    current_ship_array[starty+i-ship_length][startx+1] = SEA_CHAR

# Handling the input for the cursor
def handle_cursor_input():

    time.sleep(0.5)
    global cursor_direction, cursorx, cursory

    keypress = keyboard.read_event()

    if keypress.name == config.get("Keys", "cursor_turn_left"):
        cursor_direction ^= 1
    elif keypress.name == config.get("Keys", "cursor_turn_right"):
        cursor_direction ^= 0
    elif keypress.name == config.get("Keys", "cursor_up"):
        cursory -= 1
    elif keypress.name == config.get("Keys", "cursor_left"):
        cursorx -= 1
    elif keypress.name == config.get("Keys", "cursor_down"):
        cursory += 1
    elif keypress.name == config.get("Keys", "cursor_right"):
        cursorx += 1

def turn(player):
    global player_shots

    while True:

        handle_cursor_input()

        if keyboard.is_pressed(" "):
            if current_shot_array[cursory][cursorx] == SHIP_CHAR:
                current_shot_array[cursory][cursorx] = HIT_SHOT_CHAR
                player_shots -=1

            else:
                current_shot_array[cursory][cursorx] = MISS_SHOT_CHAR
                player_shots -=1
                current_shot_array[cursory][cursorx] = MISS_SHOT_CHAR

        if player_shots == 0:
            player ^= 1
            break

# Part one of the gameplay loop
while True:

    # Checking if cursor is out of bounds
    if cursorx < 0:
        cursorx = 0
    elif cursorx >= GRID_WIDTH:
        cursorx = GRID_WIDTH - 1

    if cursory < 0:
        cursory = 0
    elif cursory >= GRID_HEIGHT:
        cursory = GRID_HEIGHT - 1

    handle_cursor_input()

    place_ship(player, ship_length, cursorx, cursory, cursor_direction)
    # Clear the terminal
    os.system("cls" if os.name == "nt" else "clear")
    
    # Print the gamescreen
    print_array(current_ship_array)
    print(player, cursorx, cursory, cursor_direction)

    # If the enter key is pressed, break the first part of the gameplay loop and move to part two
    if keyboard.read_event().name == config.get("Keys", "continue"):
        break

# Part two of the gameplay loop
while True:

    # Display the player's grid with the opponent's shots
    print(config.read("Text", "opponent_shot_message"))
    print_array(arrays[player ^ 1]["shot"])

    # Handle the current player's turn
    turn(player)

    # check if the current player has won
    if all(cell != SHIP_CHAR for cell in row):
        break

os.system("cls" if os.name == "nt" else "clear")
print(config.get("Text", "game_over_screen"))
print(config.get("Text", "game_over_message"))
