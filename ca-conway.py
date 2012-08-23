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
  for y in [(row-1) % numRows, row, (row+1) % numRows]:
    for x in [(col-1) % numCols, col, (col+1) % numCols]:
      if map[y][x]:
          count += 1
  if map[row][col]:
    count -= 1
  return count


if __name__ == '__main__':
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
    delay = .1

    # Create empty map
    map = [[False for col in cols] for row in rows]

    # Populate map with a floater
    map[10][10] = 1;
    map[10][11] = 1;
    map[10][9] = 1;
    map[9][11] = 1;
    map[8][10] = 1;

    # Draw map before iterations
    drawMap(screen, map, rows, cols)
    screen.refresh()
    time.sleep(delay)

    # Iterate cellular automata algorithm
    iteration = 0
    key = 0
    while key != 27:
      # Check if ESC has been hit
      key = screen.getch()

      # Initialize next map
      nextMap = [[False for col in cols] for row in rows]

      # Count the neighbors of each cell and populate next map
      for row in rows:
        for col in cols:
          count = countNeighbors(map, len(rows), len(cols), row, col)
          newState = False
          if map[row][col] == True and (count == 2 or count == 3):
            newState = True
          if map[row][col] == False and count == 3:
            newState = True
          nextMap[row][col] = newState

      # Update map
      map = nextMap

      # Draw map for each iteration
      drawMap(screen, map, rows, cols)
      screen.refresh()
      time.sleep(delay)

    screen.getch()

  # Restore terminal to regular state
  finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()
