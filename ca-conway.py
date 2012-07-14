#!/usr/bin/env python
import curses, random, time


def drawMap(screen, map, rows, cols):
  screen.clear()
  for row in rows:
    for col in cols:
      if map[row][col] == True:
        screen.addch(row, col, '*')

def countNeighbors(map, numRows, numCols, row, col):
  count = 0
  # Left column
  if row-1 >= 0 and col-1 >= 0 and map[row-1][col-1] == True:
    count += 1
  if col-1 >= 0 and map[row][col-1] == True:
    count += 1
  if row+1 < numRows and col-1 >= 0 and map[row+1][col-1] == True:
    count += 1
  # Center column
  if row-1 >= 0 and map[row-1][col] == True:
    count += 1
  if row+1 < numRows and map[row+1][col] == True:
    count += 1
  # Right column
  if row-1 >= 0 and col+1 < numCols and map[row-1][col+1] == True:
    count += 1
  if col+1 < numCols and map[row][col+1] == True:
    count += 1
  if row+1 < numRows and col+1 < numCols and map[row+1][col+1] == True:
    count += 1
  return count

################################################################################

# Set up curses
try:
  screen = curses.initscr()
  curses.noecho()
  curses.cbreak()
  curses.curs_set(0)
  screen.nodelay(True)

  # Values
  rows = range(23)
  cols = range(80)

  # Populate and randomize map
  map = [[False for col in cols] for row in rows]
  for row in rows[1:len(rows)/4]:
    for col in cols[1:len(cols)/4]:
      map[row][col] = random.randint(1, 100) < 36

  # Draw map before iterations
  drawMap(screen, map, rows, cols)
  screen.refresh()
  time.sleep(.1)

  # Iterate cellular automata algorithm
  iteration = 0
  while True:
    key = screen.getch()
    # Check if ESC has been hit
    if key == 27:
      break
    changed = False
    for row in rows:
      for col in cols:
        count = countNeighbors(map, len(rows), len(cols), row, col)
        # Modify the current cell
        if map[row][col] == True and count < 2:
          map[row][col] = False
          changed = True
        elif map[row][col] == True and (count > 3):
          map[row][col] = False
          changed = True
        elif map[row][col] == False and count == 3:
          map[row][col] = True
          changed = True

    # Draw map for each iteration
    drawMap(screen, map, rows, cols)
    screen.refresh()
    time.sleep(.1)

    # Break out of the loop if we've reached equilibrium
    if not changed:
      screen.nodelay(False)
      break

  screen.getch()

# Restore terminal to regular state
finally:
  curses.echo()
  curses.nocbreak()
  curses.endwin()
