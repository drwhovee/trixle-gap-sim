import matplotlib.pyplot as plt
import numpy as np
import random

# --- CONFIGURATION ---
STEPS = 100
GRID_SCALE = 1.0

def trixle_walk_3d(steps):
    """
    Simulates a particle moving through a 3D Tetrahedral Lattice.
    """
    
    # 1. SETUP THE GEOMETRY
    # A tetrahedron has 4 faces. From the center, the normal vectors 
    # pointing out to the neighbors are arranged at ~109.47 degrees.
    # We define these 4 directional options (normalized):
    
    sqrt2 = np.sqrt(2)
    vectors = [
        np.array([0, 0, 1]),                       # Up
        np.array([2*sqrt2/3, 0, -1/3]),            # Leg 1
        np.array([-sqrt2/3, np.sqrt(2/3)*sqrt2, -1/3]), # Leg 2
        np.array([-sqrt2/3, -np.sqrt(2/3)*sqrt2, -1/3]) # Leg 3
    ]
    
    # Current Position (True Hidden Variable)
    pos = np.array([0.0, 0.0, 0.0])
    
    # Target Direction: We want to move straight along X-axis (1, 0, 0)
    target_dir = np.array([1.0, 0.0, 0.0])
    
    # History for plotting
    path_x, path_y, path_z = [0], [0], [0]
    obs_x, obs_y, obs_z = [0], [0], [0]

    print(f"{'Step':<5} | {'Decision (Vector)':<20} | {'Measurement'}")
    print("-" * 60)

    for i in range(steps):
        # 2. THE KERNEL LOGIC (Median Voter in 3D)
        # We must pick one of the 4 vectors.
        # Rule: Pick the vector that maximizes our progress toward the Target.
        # (This is maximizing the Dot Product).
        
        best_score = -999
        chosen_move = None
        
        # Add a little "Frustration Noise" (The 7.36 degree gap)
        # The lattice isn't perfect, so the vectors wobble slightly.
        noise = np.random.normal(0, 0.1, 3) 
        
        for vec in vectors:
            # Calculate where we would be if we took this step
            potential_pos = pos + vec + (noise * 0.05)
            
            # How far along the X-axis (Target) would we be?
            score = np.dot(potential_pos, target_dir)
            
            if score > best_score:
                best_score = score
                chosen_move = vec

        # Apply the move
        pos = pos + chosen_move
        
        path_x.append(pos[0])
        path_y.append(pos[1])
        path_z.append(pos[2])
        
        # 3. THE OBSERVER (3D Aliasing)
        # We snap to the nearest integer grid point in 3D space.
        ox, oy, oz = round(pos[0]), round(pos[1]), round(pos[2])
        obs_x.append(ox)
        obs_y.append(oy)
        obs_z.append(oz)

    return (path_x, path_y, path_z), (obs_x, obs_y, obs_z)

if __name__ == "__main__":
    # Run
    (tx, ty, tz), (ox, oy, oz) = trixle_walk_3d(STEPS)

    # Visualize
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot 1: The Hidden Path (Blue) - The Spiral
    ax.plot(tx, ty, tz, color='blue', alpha=0.6, linewidth=1, label='True Path (Trixle)')
    
    # Plot 2: The Observed Path (Red) - The Quantum Leap
    ax.scatter(ox, oy, oz, color='red', s=20, alpha=1.0, label='Measured Particle')

    # Formatting
    ax.set_xlabel('X (Target Direction)')
    ax.set_ylabel('Y (Lateral Jitter)')
    ax.set_zlabel('Z (Vertical Jitter)')
    ax.set_title(f'3D Trixle Simulation: Emergent Spin\n(Particle trying to move straight along X)')
    ax.legend()
    
    # Set view angle to see the spiral better
    ax.view_init(elev=20, azim=-60)
    
    plt.tight_layout()
    plt.show()