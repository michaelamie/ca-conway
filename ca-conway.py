#!/usr/bin/env python
import curses, random, time


def drawGrid(screen, grid, rows, cols):
  screen.clear()
  for row in rows:
    for col in cols:
      if grid[row][col] == True:
        screen.addch(row, col, '*')

def countNeighbors(grid, numRows, numCols, row, col):
  count = 0
  for y in [(row-1) % numRows, row, (row+1) % numRows]:
    for x in [(col-1) % numCols, col, (col+1) % numCols]:
      if grid[y][x]:
          count += 1
  if grid[row][col]:
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
    delay = .8

    # Create empty grid
    grid = [[False for col in cols] for row in rows]

    # Populate grid with a floater
    grid[10][10] = 1
    grid[10][11] = 1
    grid[10][9] = 1
    grid[9][11] = 1
    grid[8][10] = 1

    # Draw grid before iterations
    drawGrid(screen, grid, rows, cols)
    screen.refresh()
    time.sleep(delay)

    # Iterate cellular automata algorithm
    iteration = 0
    key = 0
    while key != 27:
      # Check if ESC has been hit
      key = screen.getch()

      # Initialize next grid
      nextGrid = [[False for col in cols] for row in rows]

      # Count the neighbors of each cell and populate next grid
      for row in rows:
        for col in cols:
          count = countNeighbors(grid, len(rows), len(cols), row, col)
          newState = False
          if grid[row][col] == True and (count == 2 or count == 3):
            newState = True
          if grid[row][col] == False and count == 3:
            newState = True
          nextGrid[row][col] = newState

      # Update grid
      grid = nextGrid

      # Draw grid for each iteration
      drawGrid(screen, grid, rows, cols)
      screen.refresh()
      time.sleep(delay)

    screen.getch()

  # Restore terminal to regular state
  finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()
