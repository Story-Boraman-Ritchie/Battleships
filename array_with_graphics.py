# Importing the "randint" function from the random library, which is used to place the mines
from random import randint

# Variables that define the height and width of the array
GRID_HEIGHT = 10
GRID_WIDTH = 10

# Defining the number of mines in the array
NUM_MINES = 5

# Defining characters for the Unicode graphics
sea_char = "~"
mine_char = "✱"

# Creating the arrays, "array" is for logical functions and "disp_array" is to be displayed
array = [[sea_char for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
disp_array = [[sea_char for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]

# Place mines in random tiles thoughout the map
for i in range(NUM_MINES):
  array[randint(0, GRID_WIDTH - 1)][randint(0, GRID_HEIGHT - 1)] = mine_char

# Defining the function to place the ships
# If the ship is placed on the same tile as the mine, then the ship is not printed
def place_ship(x, y):
  if not array[x][y] == "✱":
    disp_array[x][y] = "#"

playerinput = list(input("coordinates:\n"))

# Checking if the player input can be cast as an integer
try:
  for i in range (0,1):
    inputx, inputy = int(playerinput[i])
except ValueError:
  raise IndexError("Please use integers for a coordinate")

# Placing the ship at the player's provided co-ordinates
inputx = int(playerinput[0])
inputy = int(playerinput[1])
place_ship(inputx,inputy)

# Print the array
for y in range(GRID_HEIGHT):
  for x in range(GRID_WIDTH):
    print(disp_array[y][x], end=" ")

  # Print a new line after each row is printed
  print()
