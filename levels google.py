import google.generativeai as genai
import json
from collections import deque
import os
import random

genai.configure(api_key="AIzaSyC08c5Qpous-IXU954yat0PNCJweJczZVk")
model = genai.GenerativeModel('gemini-2.5-flash')

GRID_SIZE = 10
LEVELS_TO_GENERATE = 5

def generate_maze_algo(size=10):
    """
    Generates a perfect maze using Recursive Backtracker algorithm.
    0 = Path, 1 = Wall.
    """
    # 1. Start with a grid full of walls
    grid = [[1 for _ in range(size)] for _ in range(size)]
    
    # Directions: Up, Down, Left, Right (jumping 2 steps to leave walls between)
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    
    def is_valid(r, c):
        return 0 <= r < size and 0 <= c < size

    # 2. Carve paths
    # Start at (0,0)
    stack = [(0, 0)]
    grid[0][0] = 0
    
    while stack:
        current_r, current_c = stack[-1]
        
        # Find unvisited neighbors
        neighbors = []
        for dr, dc in directions:
            nr, nc = current_r + dr, current_c + dc
            if is_valid(nr, nc) and grid[nr][nc] == 1:
                neighbors.append((nr, nc, dr, dc))
        
        if neighbors:
            # Choose a random neighbor
            nr, nc, dr, dc = random.choice(neighbors)
            
            # Knock down the wall between current and neighbor
            wall_r, wall_c = current_r + (dr // 2), current_c + (dc // 2)
            grid[wall_r][wall_c] = 0
            grid[nr][nc] = 0
            
            stack.append((nr, nc))
        else:
            stack.pop()
            
    return grid

def add_spawns(grid):
    rows = len(grid)
    cols = len(grid[0])
    
    # Ensure start and end are open
    grid[0][0] = 2           # Mouse
    grid[rows-1][cols-1] = 4 # Exit
    
    # Ensure the path to exit is open (sometimes the algo leaves the very corner blocked)
    grid[rows-1][cols-2] = 0
    grid[rows-2][cols-1] = 0
    
    # Place Cat (3) at bottom left
    grid[rows-1][0] = 3
    
    return grid

def save_levels():
    vault_file = "levels.json"
    all_levels = []
    
    print(f"🔨 Designing {LEVELS_TO_GENERATE} levels manually...")
    
    for i in range(LEVELS_TO_GENERATE):
        # Generate raw grid
        raw_grid = generate_maze_algo(GRID_SIZE)
        
        # Add characters
        final_grid = add_spawns(raw_grid)
        
        level_data = {
            "level_id": i + 1,
            "difficulty": "procedural",
            "grid": final_grid
        }
        all_levels.append(level_data)
        print(f"✅ Level {i+1} generated.")

    # Save to file
    with open(vault_file, "w") as f:
        json.dump(all_levels, f, indent=4)
    
    print(f"\n🎉 Boom. {LEVELS_TO_GENERATE} levels saved to '{vault_file}'. Send it to your team!")

# --- RUN IT ---
if __name__ == "__main__":
    save_levels()