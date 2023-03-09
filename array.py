# Some variables to define the height and width of the array in characters
GRID_HEIGHT = 10
GRID_WIDTH = 10

# Creating the array
array = [["_"]*GRID_HEIGHT]*GRID_WIDTH

# Printing the array
for y in range(GRID_HEIGHT):
  for x in range(GRID_WIDTH):
    print(array[y][x])
