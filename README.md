# Maze Generator & Solver – Randomized DFS + Backtracking

This project implements a **proper maze** (a spanning tree) using a stack-based "mouse" that eats through walls. It then solves the maze using backtracking, visualizing the path with **red dots** and **blue dead ends**.

## Features

- **Maze Generation** – Randomized Depth‑First Search (DFS) with animation.
- **Data Structure** – `northWall` and `eastWall` as per the assignment spec.
- **Solver** – Backtracking with visual feedback (red = current path, blue = dead end).
- **Start / End** – Openings on the left and right edges (random rows).
- **Bonus: Cycles** – Option to add extra walls (≈5% chance), creating cycles that break the left‑hand rule.
- **Interactive GUI** – Buttons to generate, solve, and toggle cycle mode.

## How It Works

### Generation (Stack‑based “Mouse”)

1. All walls are initially **intact**.
2. The mouse starts in a random cell, marks it visited, and pushes it onto a stack.
3. It looks for unvisited neighbours.
4. If one exists, it chooses randomly, **eats** the connecting wall, and moves there (pushing the new cell).
5. If none exist, it backtracks (pops the stack).
6. The process repeats until the stack is empty → all cells are connected uniquely.

### Solver (Backtracking with Colours)

- The mouse tries to move in a random direction where no wall exists and the cell hasn’t been visited by the solver.
- It pushes each step onto a stack and draws a **red dot**.
- When stuck, it turns the cell **blue** (dead end), pops the stack, and backtracks.
- Stops when the right‑edge exit is reached.

### Why a Queue Would Differ

- **Stack** → depth‑first → long, winding corridors (typical maze).
- **Queue** → breadth‑first → creates more “wave‑like” patterns, shorter dead ends.
- For generating a perfect maze, **stack (DFS)** is standard because it naturally produces a single, unique path between any two cells.

## Requirements

- Python 3.6+
- Tkinter (included with standard Python on most platforms)

## How to Run

1. Save the code as `maze.py`.
2. Run from terminal:
   ```bash
   python maze.py
   ```
