# Maze Generator & Solver (Python)

A Python program that randomly generates a **proper maze** (a spanning tree) of size `R x C` and then finds a path from the left edge to the right edge using a backtracking algorithm. The maze is built dynamically by a “mouse” that eats through walls, and the solution is visualised with a red dot (current position) and blue dots (dead ends).

---

## Features

- **Proper maze generation** – every cell is connected by a unique path (no cycles, no isolated cells).
- **Stack‑based “mouse”** – implements a depth‑first search (DFS) to carve passages.
- **Visual generation** – watch the mouse eat walls in real time (Pygame / Tkinter).
- **Backtracking solver** – finds a path from start (left edge) to end (right edge) using a stack; dead ends turn blue.
- **Optional challenge** – after generation, the mouse eats extra walls (probability 1/20) to create cycles, breaking the “shoulder‑to‑the‑wall” rule.

---

## Maze Representation

The maze is stored using two 2D lists (or NumPy arrays):

- `northWall[r][c]` – `True` means a solid north (upper) wall exists for cell `(r, c)`.  
  The **zeroth row** is a phantom row whose north walls form the **bottom edge** of the actual maze.
- `eastWall[r][c]` – `True` means a solid east (right) wall exists for cell `(r, c)`.  
  The **zeroth column**’s east walls define gaps on the **left edge** of the maze.

All walls start as `True` (solid). The mouse “eats” a wall by setting the corresponding element to `False`.

---

## Maze Generation – Stack‑Based DFS “Mouse”

1. Place the mouse in an arbitrary starting cell.
2. Push that cell onto a stack.
3. While the stack is not empty:
   - Look at the current cell’s four neighbours (up, down, left, right).
   - For each neighbour that **has all four walls intact** (i.e. never visited), mark it as a candidate.
   - If there is at least one candidate:
     - Choose one randomly.
     - Eat the wall between the current cell and the chosen neighbour.
     - Push the current cell onto the stack (if needed) and move the mouse to the neighbour.
   - Else (no candidates – dead end):
     - Pop a cell from the stack (backtrack).
4. When the stack is empty, every cell has been visited and the maze is a proper spanning tree.

> **Why a stack?**  
> A stack produces a depth‑first exploration – the mouse goes deep into the maze, creating long winding corridors. A queue would produce a breadth‑first maze, with more branching and shorter paths. The assignment chooses the stack for its “tortuous” paths.

---

## Maze Solving – Backtracking with Red / Blue Dots

The solver uses a **separate stack** (Python list) to find a path from the **left‑edge opening** to the **right‑edge opening**:

1. Place the mouse at the start cell (any cell on the left edge where the west wall is missing).
2. Mark the target as the right edge (any cell on the right edge where the east wall is missing).
3. While the mouse is not at the target:
   - Look at the four neighbours. If there is **no wall** between the current cell and a neighbour, and that neighbour has **not been visited** by the solver, it is a candidate.
   - If candidates exist:
     - Choose one (randomly, or by a simple order).
     - Push the current cell onto the solver’s stack.
     - Move the mouse to the candidate; draw a **red dot** in the new cell.
   - Else (dead end):
     - Mark the current cell **blue** (dead end, will never be part of the final path).
     - Pop the previous cell from the stack and move the mouse back there (red dot follows).
4. When the target is reached, the stack contains the unique solution path.

The solver can optionally **put up a virtual wall** to avoid re‑entering dead ends, though the blue marking already serves a similar purpose.

---

## Optional Challenge – Creating Cycles

After the initial proper maze is generated, the mouse **eats extra walls** with a probability of **1/20** (5%). Each extra wall is chosen randomly from the remaining solid walls. Eating it creates a **cycle** in the graph.

**Effect on solving** – With cycles, the “shoulder‑to‑the‑wall” (left‑hand rule) method may fail because the cycle can encircle the exit. The backtracking solver, however, still works because it keeps a visited set and can backtrack out of loops.  
The program shows both behaviours: the deterministic left‑hand rule (if implemented) gets stuck, while the stack‑based search succeeds.

---

## Requirements & Usage

### Prerequisites
- Python 3.7+
- Pygame (or Tkinter – included in standard Python)
  ```bash
  pip install pygame
