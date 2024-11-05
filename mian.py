import numpy as np
import matplotlib.pyplot as plt
n_forces = int(input("Enter the number of point forces (minimum 3): "))
while n_forces < 3:
    n_forces = int(input("Please enter at least 3 point forces: "))

forces = []
for i in range(n_forces):
    position = float(input(f"Enter the position of point force {i + 1} (m): "))
    magnitude = float(input(f"Enter the magnitude of point force {i + 1} (kN): "))
    forces.append((position, magnitude))

L = float(input("Enter the length of the beam (m): "))

w = float(input("Enter the magnitude of the uniformly distributed load (kN/m): "))
start_w = float(input("Enter the start position of the UDL (m): "))
end_w = float(input(f"Enter the end position of the UDL (m, should be <= {L}): "))
while end_w > L:
    end_w = float(input(f"End position should be <= {L}. Enter again: "))


total_load = sum([magnitude for _, magnitude in forces])

udl_load = w * (end_w - start_w)

total_vertical_load = total_load + udl_load

moment_A = sum([magnitude * position for position, magnitude in forces]) + (
    (w * (end_w - start_w)) * ((end_w + start_w) / 2)
)

RB = moment_A / L

RA = total_vertical_load - RB

print(f"\nReaction at A (RA): {RA:.2f} kN")
print(f"Reaction at B (RB): {RB:.2f} kN")


def shear_force(x):
    sf = RA
    if x >= start_w:
        sf -= w * min(x - start_w, end_w - start_w)
    for pos, force in forces:
        if x >= pos:
            sf -= force
    return sf


def bending_moment(x):
    bm = RA * x
    for pos, force in forces:
        if x >= pos:
            bm -= force * (x - pos)
    if start_w <= x <= end_w:
        bm -= (w * (x - start_w)) * ((x - start_w) / 2)
    return bm


print(f"Bending moment at x=0: {bending_moment(0)}")
print(f"Bending moment at x=L: {bending_moment(L)}")

# x_vals = np.linspace(0, L, 100)
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


print("\nShear Force and Bending Moment at key points:")
for x in [0, L] + [pos for pos, _ in forces]:
    sf = shear_force(x)
    bm = bending_moment(x)
    print(f"At x = {x} m: Shear Force = {sf} kN, Bending Moment = {bm} kNm")


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))


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
ax1.set_title("Shear Force Diagram")
ax1.set_xlabel("Position along the beam (m)")
ax1.set_ylabel("Shear Force (kN)")
ax1.grid(True)


ax2.plot(x_vals, bm_vals, label="Bending Moment", color="green")
ax2.fill_between(
    x_vals,
    0,
    bm_vals,
    where=(np.array(bm_vals) >= 0),
    color="green",
    alpha=0.3,
    interpolate=True,
)
ax2.fill_between(
    x_vals,
    0,
    bm_vals,
    where=(np.array(bm_vals) <= 0),
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
