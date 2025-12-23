import matplotlib.pyplot as plt
import math
import random
import numpy as np

# --- CONFIGURATION ---
STEPS = 50                 # How far the particle travels
GRID_SCALE = 1.0           # The size of a Trixle

def trixle_walk_simulation(steps):
    """
    Simulates a particle trying to move in a straight line (y=0)
    across a lattice that only allows diagonal movement (hexagonal/triangular projection).
    """
    
    # 1. INITIALIZATION
    true_x, true_y = 0.0, 0.0   # The 'Hidden Variable' (Real position)
    path_x = [0.0]
    path_y = [0.0]
    
    observed_x = [0]
    observed_y = [0]
    
    # The Trixle Geometry (2D Hexagonal/Triangular Projection)
    # A particle cannot move at 0 degrees. It must choose +30 or -30.
    move_up   = (math.cos(math.radians(30)), math.sin(math.radians(30)))
    move_down = (math.cos(math.radians(-30)), math.sin(math.radians(-30)))

    print(f"{'Step':<5} | {'True Position':<20} | {'Measurement'} | {'State'}")
    print("-" * 65)

    for i in range(steps):
        # 2. THE KERNEL LOGIC (Determinism / Median Voter)
        # The Universe tries to minimize the error from the centerline (y=0).
        
        if true_y > 0:
            # We are too high, forced to go down
            move = move_down
            state = "Zag (Correction)"
        elif true_y < 0:
            # We are too low, forced to go up
            move = move_up
            state = "Zig (Correction)"
        else:
            # Perfectly on the line? The lattice gap forces a choice.
            # This is Spontaneous Symmetry Breaking.
            move = random.choice([move_up, move_down])
            state = "Jitter (Gap)"

        # Apply Movement
        true_x += move[0]
        true_y += move[1]
        
        path_x.append(true_x)
        path_y.append(true_y)

        # 3. THE OBSERVER LOGIC (Measurement Aliasing)
        # The observer's instrument snaps to the nearest integer grid point.
        obs_x_val = round(true_x)
        obs_y_val = round(true_y)
        
        observed_x.append(obs_x_val)
        observed_y.append(obs_y_val)

    return path_x, path_y, observed_x, observed_y

if __name__ == "__main__":
    # Run Simulation
    tx, ty, ox, oy = trixle_walk_simulation(STEPS)

    # Visualization
    plt.figure(figsize=(12, 6))

    # Plot 1: The Hidden Variable (True Geometry)
    plt.plot(tx, ty, color='blue', alpha=0.5, label='True Path (Trixle Logic)', linewidth=1)
    plt.scatter(tx, ty, s=10, color='blue', alpha=0.5)

    # Plot 2: The Observed Data (Quantum Randomness)
    plt.step(ox, oy, color='red', where='mid', label='Measured Path (Observer)', linewidth=2)
    plt.scatter(ox, oy, s=30, color='red', marker='x')

    # Formatting
    plt.axhline(0, color='black', linestyle='--', alpha=0.3, label='Target Vector (Light Ray)')
    plt.title(f'The Trixle Effect: Deterministic Jitter vs. Observed Randomness\n(Steps: {STEPS})')
    plt.xlabel('Distance (Lattice Units)')
    plt.ylabel('Deviation (Lattice Units)')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', alpha=0.3)
    plt.ylim(-2, 2)
    plt.tight_layout()
    plt.show()