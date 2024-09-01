import json

import numpy as np
from dotenv import load_dotenv
from matplotlib import pyplot as plt

from angle_see.generate_simple_angle import generate_line_intersection_image

load_dotenv()  # take environment variables from .env.

plt.ion()
human = []
for _ in range(2):
    for angle in sorted(np.random.rand(7) * 360):
        image = generate_line_intersection_image(angle)
        plt.imshow(image)
        guessed_angle = float(input("Estimate the angle\n"))
        human.append((angle, guessed_angle))

with open("human_angles.json", "w") as f:
    json.dump(human, f)
