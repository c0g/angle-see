import numpy as np
import itertools
import json
import io
from dotenv import load_dotenv
import base64

from tqdm import tqdm

from angle_see.general import encode_image, cached_completion
from angle_see.generate_simple_angle import generate_line_intersection_image
from matplotlib import pyplot as plt

load_dotenv()  # take environment variables from .env.

plt.ion()
human = []
for _ in range(2):
    for angle in sorted(np.random.rand(7) * 360):
        image = generate_line_intersection_image(angle)
        plt.imshow(image)
        guessed_angle = float(input("Estimate the angle\n"))
        human.append((angle, guessed_angle))

with open('human_angles.json', 'w') as f:
    json.dump(human, f)
