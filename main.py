import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp


# Define the differential equations for the three-body problem
def three_body_equations(t, y, m1, m2, m3):
    x1, y1, vx1, vy1, x2, y2, vx2, vy2, x3, y3, vx3, vy3 = y

    # Compute distances
    r12 = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    r13 = np.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2)
    r23 = np.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)

    # Compute accelerations
    ax1 = -(m2 / r12**3) * (x1 - x2) - (m3 / r13**3) * (x1 - x3)
    ay1 = -(m2 / r12**3) * (y1 - y2) - (m3 / r13**3) * (y1 - y3)
    ax2 = -(m1 / r12**3) * (x2 - x1) - (m3 / r23**3) * (x2 - x3)
    ay2 = -(m1 / r12**3) * (y2 - y1) - (m3 / r23**3) * (y2 - y3)
    ax3 = -(m1 / r13**3) * (x3 - x1) - (m2 / r23**3) * (x3 - x2)
    ay3 = -(m1 / r13**3) * (y3 - y1) - (m2 / r23**3) * (y3 - y2)

    return [vx1, vy1, ax1, ay1, vx2, vy2, ax2, ay2, vx3, vy3, ax3, ay3]


# Initial conditions
m1 = 1.0  # Mass of the first body
m2 = 1.0  # Mass of the second body
m3 = 1.0  # Mass of the third body
initial_conditions = [
    0,
    1.0,
    0.0,
    -0.5,
    -0.55,
    0,
    1,
    1,
    0.46,
    0.0,
    -1,
    1,
]  # [x1, y1, vx1, vy1, x2, y2, vx2, vy2, x3, y3, vx3, vy3]

# Time array
t_span = (0, 20)  # Time span for the simulation
t_eval = np.linspace(
    t_span[0], t_span[1], int(1e5)
)  # Time points where the solution is computed

# Solve the differential equations
solution = solve_ivp(
    fun=lambda t, y: three_body_equations(t, y, m1, m2, m3),
    t_span=t_span,
    y0=initial_conditions,
    t_eval=t_eval,
)

# Plotting the animation
fig, ax = plt.subplots()
(line,) = ax.plot([], [], "bo", markersize=5)
lines_traj = [ax.plot([], [], lw=1)[0] for _ in range(3)]  # Trajectories of each body


def init():
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    for traj in lines_traj:
        traj.set_data([], [])
    return [line] + lines_traj


def update(frame):
    x1, y1, _, _, x2, y2, _, _, x3, y3, _, _ = solution.y[:, frame]
    line.set_data([x1, x2, x3], [y1, y2, y3])

    # Compute trajectories
    for i, traj in enumerate(lines_traj):
        traj.set_data(solution.y[i * 4, :frame], solution.y[i * 4 + 1, :frame])

    return [line] + lines_traj


ani = FuncAnimation(
    fig, update, frames=len(solution.t), init_func=init, blit=True, interval=1e-3
)
ani.save("./animation/animation_00.mp4", fps=30)
