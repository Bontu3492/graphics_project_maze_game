import pygame
import random
import sys

# =========================
# ⚙️ SETTINGS (adjusted for button visibility)

ROWS, COLS = 15, 15
CELL_SIZE = 40                     # increased so the grid is wider
WIDTH = COLS * CELL_SIZE           # = 600
HEIGHT = ROWS * CELL_SIZE          # = 600
UI_HEIGHT = 80

# Ensure the window is wide enough for all buttons (minimum 600)
if WIDTH < 600:
    WIDTH = 600

CHALLENGE_MODE = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + UI_HEIGHT))
pygame.display.set_caption("Maze Generator & Solver – Left to Right")

# =========================
# 🧱 DATA STRUCTURES
# =========================
northWall = [[1] * COLS for _ in range(ROWS)]
eastWall  = [[1] * COLS for _ in range(ROWS)]
visited   = [[False] * COLS for _ in range(ROWS)]

dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

start_cell = (0, 0)
end_cell   = (0, COLS-1)

# =========================
# 🔘 BUTTON CLASS
# =========================
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.SysFont(None, 28)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = (170, 170, 170) if self.rect.collidepoint(mouse_pos) else (200, 200, 200)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        txt_surface = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# =========================
# 🔘 CREATE BUTTONS (now fully inside the visible area)
# =========================
btn_generate = Button(20, HEIGHT + 20, 110, 40, "Generate")
btn_solve    = Button(150, HEIGHT + 20, 110, 40, "Solve")
btn_reset    = Button(280, HEIGHT + 20, 110, 40, "Reset")
btn_challenge= Button(410, HEIGHT + 20, 130, 40, "Challenge")

# =========================
# 🧠 HELPER FUNCTIONS
# =========================
def valid(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def remove_wall(r1, c1, r2, c2):
    if r1 == r2:
        if c1 < c2:
            eastWall[r1][c1] = 0
        else:
            eastWall[r2][c2] = 0
    else:
        if r1 < r2:
            northWall[r2][c2] = 0
        else:
            northWall[r1][c1] = 0

def set_start_end():
    global start_cell, end_cell
    start_row = random.randint(0, ROWS-1)
    end_row   = random.randint(0, ROWS-1)
    start_cell = (start_row, 0)
    end_cell   = (end_row, COLS-1)

def apply_start_end_openings():
    r_end, c_end = end_cell
    eastWall[r_end][c_end] = 0   # remove east wall on the right edge

# =========================
# 🎨 DRAW MAZE
# =========================
def draw_maze():
    screen.fill((255, 255, 255))

    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL_SIZE
            y = r * CELL_SIZE

            # North wall
            if northWall[r][c]:
                pygame.draw.line(screen, (0, 0, 0), (x, y), (x + CELL_SIZE, y), 2)

            # East wall
            if eastWall[r][c]:
                pygame.draw.line(screen, (0, 0, 0), (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)

            # South wall (bottom boundary)
            if r == ROWS - 1:
                pygame.draw.line(screen, (0, 0, 0), (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)

            # West wall (left boundary) – skip for start cell
            if c == 0 and (r, c) != start_cell:
                pygame.draw.line(screen, (0, 0, 0), (x, y), (x, y + CELL_SIZE), 2)

    # Start (green) and end (orange) markers
    sr, sc = start_cell
    er, ec = end_cell
    pygame.draw.circle(screen, (0, 200, 0), (sc * CELL_SIZE + CELL_SIZE//2, sr * CELL_SIZE + CELL_SIZE//2), CELL_SIZE//5)
    pygame.draw.circle(screen, (255, 165, 0), (ec * CELL_SIZE + CELL_SIZE//2, er * CELL_SIZE + CELL_SIZE//2), CELL_SIZE//5)

    draw_ui()
    pygame.display.update()

def draw_ui():
    pygame.draw.rect(screen, (220, 220, 220), (0, HEIGHT, WIDTH, UI_HEIGHT))
    btn_generate.draw(screen)
    btn_solve.draw(screen)
    btn_reset.draw(screen)
    btn_challenge.draw(screen)

# =========================
# 🔥 MAZE GENERATION (DFS with animation)
# =========================
def generate_maze():
    global northWall, eastWall, visited

    northWall = [[1] * COLS for _ in range(ROWS)]
    eastWall  = [[1] * COLS for _ in range(ROWS)]
    visited   = [[False] * COLS for _ in range(ROWS)]

    # Random starting cell for the mouse (not necessarily the final start)
    start_r = random.randint(0, ROWS-1)
    start_c = random.randint(0, COLS-1)
    stack = [(start_r, start_c)]
    visited[start_r][start_c] = True

    while stack:
        r, c = stack[-1]

        neighbours = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if valid(nr, nc) and not visited[nr][nc]:
                neighbours.append((nr, nc))

        if neighbours:
            nr, nc = random.choice(neighbours)
            remove_wall(r, c, nr, nc)
            visited[nr][nc] = True
            stack.append((nr, nc))

            # Animate the "mouse eating"
            draw_maze()
            mx = c * CELL_SIZE + CELL_SIZE//2
            my = r * CELL_SIZE + CELL_SIZE//2
            pygame.draw.circle(screen, (255, 0, 0), (mx, my), CELL_SIZE//4)
            pygame.display.update()
            pygame.time.delay(15)
        else:
            stack.pop()

    # Place start/end on left/right edges
    set_start_end()
    apply_start_end_openings()

    # Challenge mode: add cycles
    if CHALLENGE_MODE:
        for r in range(ROWS):
            for c in range(COLS):
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if valid(nr, nc) and random.randint(1, 20) == 1:
                        if dr == -1 and northWall[r][c] == 1:
                            northWall[r][c] = 0
                        elif dr == 1 and northWall[nr][nc] == 1:
                            northWall[nr][nc] = 0
                        elif dc == -1 and eastWall[nr][nc] == 1:
                            eastWall[nr][nc] = 0
                        elif dc == 1 and eastWall[r][c] == 1:
                            eastWall[r][c] = 0

    draw_maze()

# =========================
# 🧭 SOLVER (Backtracking)
# =========================
def solve_maze():
    stack = [start_cell]
    visited_solve = [[False] * COLS for _ in range(ROWS)]
    visited_solve[start_cell[0]][start_cell[1]] = True

    while stack:
        r, c = stack[-1]

        draw_maze()
        mx = c * CELL_SIZE + CELL_SIZE//2
        my = r * CELL_SIZE + CELL_SIZE//2
        pygame.draw.circle(screen, (255, 0, 0), (mx, my), CELL_SIZE//4)
        pygame.display.update()
        pygame.time.delay(40)

        if (r, c) == end_cell:
            print("Path found!")
            return

        moved = False
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        random.shuffle(directions)

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not valid(nr, nc) or visited_solve[nr][nc]:
                continue

            # Wall checks
            if dr == -1 and northWall[r][c] == 0:
                stack.append((nr, nc))
                visited_solve[nr][nc] = True
                moved = True
                break
            if dr == 1 and northWall[nr][nc] == 0:
                stack.append((nr, nc))
                visited_solve[nr][nc] = True
                moved = True
                break
            if dc == -1 and eastWall[nr][nc] == 0:
                stack.append((nr, nc))
                visited_solve[nr][nc] = True
                moved = True
                break
            if dc == 1 and eastWall[r][c] == 0:
                stack.append((nr, nc))
                visited_solve[nr][nc] = True
                moved = True
                break

        if not moved:
            # Dead end → blue dot
            pygame.draw.circle(screen, (0, 0, 255), (mx, my), CELL_SIZE//4)
            pygame.display.update()
            pygame.time.delay(40)
            stack.pop()

    print("No path found? (Should not happen)")
    draw_maze()

# =========================
# ♻️ RESET
# =========================
def reset_maze():
    global northWall, eastWall, visited
    northWall = [[1] * COLS for _ in range(ROWS)]
    eastWall  = [[1] * COLS for _ in range(ROWS)]
    visited   = [[False] * COLS for _ in range(ROWS)]
    apply_start_end_openings()
    draw_maze()

# =========================
# 🚀 MAIN LOOP
# =========================
def main():
    global CHALLENGE_MODE
    clock = pygame.time.Clock()
    generate_maze()          # initial maze
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn_generate.is_clicked(pos):
                    generate_maze()
                elif btn_solve.is_clicked(pos):
                    solve_maze()
                elif btn_reset.is_clicked(pos):
                    reset_maze()
                elif btn_challenge.is_clicked(pos):
                    CHALLENGE_MODE = not CHALLENGE_MODE
                    print(f"Challenge Mode: {'ON' if CHALLENGE_MODE else 'OFF'}")
                    generate_maze()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
