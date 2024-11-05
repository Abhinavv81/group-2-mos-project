import numpy as np
import matplotlib.pyplot as plt

L = 8  
forces = [
    (2, 30),
    (4, 20),
    (6, 30),
]  
w = 30  
start_w = 4  
end_w = 8  

total_load = sum([magnitude for _, magnitude in forces])
udl_load = w * (end_w - start_w)
total_vertical_load = total_load + udl_load
moment_A = sum([magnitude * position for position, magnitude in forces]) + (
    w * (end_w - start_w) * (end_w + start_w) / 2
)
RB = moment_A / L
RA = total_vertical_load - RB


def shear_force(x):
    sf = RA
    if x >= start_w:
        if x <= end_w:
            sf -= w * (x - start_w)
        else:
            sf -= w * (end_w - start_w)  
    for pos, force in forces:
        if x >= pos:
            sf -= force
    return sf


def bending_moment(x):
    bm = RA * x
    for pos, force in forces:
        if x >= pos:
            bm -= force * (x - pos)
    if x >= start_w:
        if x <= end_w:
            bm -= w * (x - start_w) ** 2 / 2
        else:
            bm -= w * (end_w - start_w) * (x - (start_w + end_w) / 2)
    return bm


x_vals = np.sort(
    np.concatenate(
        [
            np.linspace(0, L, 100),
            np.array([pos - 0.001 for pos, _ in forces if pos > 0]),
            np.array([pos + 0.001 for pos, _ in forces if pos < L]),
        ]
    )
)

sf_vals = [shear_force(x) for x in x_vals]
bm_vals = [bending_moment(x) for x in x_vals]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

ax1.plot(x_vals, sf_vals, label="Shear Force", color="blue")
ax1.fill_between(
    x_vals,
    0,
    sf_vals,
    where=(np.array(sf_vals) > 0),
    color="blue",
    alpha=0.3,
    interpolate=True,
)
ax1.fill_between(
    x_vals,
    0,
    sf_vals,
    where=(np.array(sf_vals) < 0),
    color="red",
    alpha=0.3,
    interpolate=True,
)
ax1.set_title("Shear Force Diagram with Sharp Drops")
ax1.set_xlabel("Position along the beam (m)")
ax1.set_ylabel("Shear Force (kN)")
ax1.grid(True)

ax2.plot(x_vals, bm_vals, label="Bending Moment", color="green")
ax2.fill_between(
    x_vals,
    0,
    bm_vals,
    where=(np.array(bm_vals) > 0),
    color="green",
    alpha=0.3,
    interpolate=True,
)
ax2.fill_between(
    x_vals,
    0,
    bm_vals,
    where=(np.array(bm_vals) < 0),
    color="orange",
    alpha=0.3,
    interpolate=True,
)
ax2.set_title("Bending Moment Diagram")
ax2.set_xlabel("Position along the beam (m)")
ax2.set_ylabel("Bending Moment (kNm)")
ax2.grid(True)

plt.tight_layout()
plt.show()
