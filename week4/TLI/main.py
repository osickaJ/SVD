from structure import Point, Cube
import numpy as np
import matplotlib.pyplot as plt

def visualize_cube_temp(points, target_pt, target_temp):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    px = [p.x for p in points]
    py = [p.y for p in points]
    pz = [p.z for p in points]
    pt = [p.t for p in points]

    # Set consistent color bounds based on vertex min/max
    t_min, t_max = min(pt), max(pt)

    # Plot vertices
    sc = ax.scatter(px, py, pz, c=pt, cmap='inferno', 
                    s=100, vmin=t_min, vmax=t_max, label='Vertices')
    
    # Plot center point using the SAME color scale (vmin/vmax)
    ax.scatter(target_pt[0], target_pt[1], target_pt[2], 
               c=[target_temp], cmap='inferno', 
               vmin=t_min, vmax=t_max, s=250, marker='*', 
               edgecolors='black', linewidths=1.5, label='Interpolated Center')

    plt.colorbar(sc, label='Temperature (°C)')
    plt.title(f'Heatmap: Center Temp is {target_temp:.2f}°C')
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
    plt.legend()
    plt.show()

def visualize_full_cube(my_cube, points, step=0.1):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # 1. Create a dense grid of points inside the [0, 1] cube
    grid_range = np.arange(0, 1 + step, step)
    gx, gy, gz = np.meshgrid(grid_range, grid_range, grid_range)
    
    # 2. Flatten and calculate temperatures for every point in the grid
    flat_x, flat_y, flat_z = gx.ravel(), gy.ravel(), gz.ravel()
    flat_temps = [my_cube.get_temperature_at(x, y, z) for x, y, z in zip(flat_x, flat_y, flat_z)]

    # 3. Plot the volume with transparency (alpha)
    # Using 'inferno' to match your original theme
    sc = ax.scatter(flat_x, flat_y, flat_z, c=flat_temps, cmap='inferno', 
                    alpha=0.4, s=20, edgecolors='none')

    # 4. Highlight the original 8 vertices for reference
    px = [p.x for p in points]; py = [p.y for p in points]
    pz = [p.z for p in points]; pt = [p.t for p in points]
    ax.scatter(px, py, pz, c=pt, cmap='inferno', s=100, 
               edgecolors='black', linewidths=2, label='Vertices')

    plt.colorbar(sc, label='Temperature (°C)')
    plt.title(f'Volumetric Heatmap (Step: {step})')
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
    plt.show()


def main():

    points = [
        Point(0, 0, 0, t=10.0), # Bottom-front-left
        Point(1, 0, 0, t=20.0), # Bottom-front-right
        Point(0, 1, 0, t=15.0), # Bottom-back-left
        Point(1, 1, 0, t=25.0), # Bottom-back-right
        Point(0, 0, 1, t=30.0), # Top-front-left
        Point(1, 0, 1, t=40.0), # Top-front-right
        Point(0, 1, 1, t=35.0), # Top-back-left
        Point(1, 1, 1, t=50.0)  # Top-back-right
    ]

    my_cube = Cube(points)

    target_x, target_y, target_z = 0.5, 0.5, 0.5
    temp_at_center = my_cube.get_temperature_at(target_x, target_y, target_z)
    print(f"Temperature at ({target_x}, {target_y}, {target_z}) is {temp_at_center}°C")

    step_size = 0.05
    visualize_full_cube(my_cube, points, step=step_size)

if __name__ == "__main__":

    main()
    